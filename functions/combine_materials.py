import bpy
import re
from core.common import get_armature, get_meshes, clean_material_names  
from core.translations import t

def textures_match(tex1, tex2):
    return tex1.image == tex2.image and tex1.extension == tex2.extension

def consolidate_nodes(node1, node2):
    # Copy settings from node1 to node2
    node2.color_space = node1.color_space
    node2.coordinates = node1.coordinates

# Copy texture slots
def copy_tex_nodes(mat1, mat2):
    for node1 in mat1.node_tree.nodes:
        if node1.type == 'TEX_IMAGE':
            node2 = mat2.node_tree.nodes.get(node1.name)
            if node2:
                node2.mapping = node1.mapping
                node2.projection = node1.projection  

def consolidate_textures(mat1, mat2):
    if mat1.node_tree and mat2.node_tree:
        for node1 in mat1.node_tree.nodes:
            if node1.type == 'TEX_IMAGE':
                # Handle node groups
                if node1.node_tree:
                    consolidate_textures(node1.node_tree, mat2.node_tree)
                
                for node2 in mat2.node_tree.nodes:
                    if (node2.type == 'TEX_IMAGE' and
                        node1.image == node2.image):  
                            
                        consolidate_nodes(node1, node2)
                        node2.image = node1.image

                        # Copy texture slots
                        copy_tex_nodes(mat1, mat2)

def color_match(col1, col2, tolerance=0.01):
    return abs(col1[0] - col2[0]) < tolerance 
                
def materials_match(mat1, mat2, tolerance=0.01):
    if not color_match(mat1.diffuse_color, mat2.diffuse_color, tolerance): 
        return False
    
    if mat1.roughness != mat2.roughness:
        return False
        
    consolidate_textures(mat1, mat2)  
    
    return True

def get_base_name(name):
    mat_match = re.match(r"^(.*)\.\d{3}$", name)
    return mat_match.group(1) if mat_match else name

def report_consolidated(self, num_combined):
    self.report({'INFO'}, t('CombineMaterials.info.combine_materials').format(count=num_combined))

class CombineMaterials(bpy.types.Operator):
    bl_idname = "rinasplugin.combine_materials"
    bl_label = t("CombineMaterials.label")
    bl_description = t("CombineMaterials.description")
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return get_armature(context) is not None
    
    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')   
    
        armature = get_armature(context)
        if not armature:
            return {'CANCELLED'}
            
        meshes = get_meshes(armature)
        if not meshes:
            return {'CANCELLED'}
        
        bpy.ops.object.mode_set(mode='OBJECT')

        self.consolidate_materials(meshes)
        self.remove_unused_materials()
        self.cleanmatslots()
        self.clean_material_names()  

        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.context.view_layer.objects.active = armature
        
        return {'FINISHED'}

    def consolidate_materials(self, objects):        
        mat_mapping = {}
        num_combined = 0
        for ob in objects:
            for slot in ob.material_slots:
                mat = slot.material
                if mat:
                
                    base_name = get_base_name(mat.name)
                    

                    if base_name in mat_mapping:
                        base_mat = mat_mapping[base_name]
                        if materials_match(base_mat, mat):
                            # Consolidate textures
                            consolidate_textures(base_mat, mat)
                        
                            num_combined += 1
                            slot.material = base_mat
                        
                    else:
                        mat_mapping[base_name] = mat
                    
        report_consolidated(self, num_combined)    
    
    def remove_unused_materials(self):
        meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']
        
        for obj in meshes:
            obj.select_set(True)

        assigned_materials = set()

        for obj in meshes:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    assigned_materials.add(slot.material)

        for mat in bpy.data.materials:
            if mat not in assigned_materials:
                bpy.data.materials.remove(mat, do_unlink=True)
            
        for obj in meshes:
            obj.select_set(False)
            
    def cleanmatslots(self):
        meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']
    
        for obj in meshes:
            obj.select_set(True)
        
        bpy.context.view_layer.objects.active = meshes[0]  

        bpy.ops.object.material_slot_remove_unused()
    
        for obj in meshes:
            obj.select_set(False)
         
    def clean_material_names(self):
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                clean_material_names(obj)