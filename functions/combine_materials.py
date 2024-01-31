import bpy
import re
from core.common import get_armature, get_meshes, clean_material_names
from core.translations import t

def materials_match(mat1, mat2):
    return mat1.diffuse_color == mat2.diffuse_color and mat1.roughness == mat2.roughness

def get_base_name(name):
    mat_match = re.match(r"^(.*)\.\d{3}$", name)
    return mat_match.group(1) if mat_match else name

def report_consolidated(self, num_combined):
    self.report({'INFO'}, f'{num_combined} materials combined')

class CombineMaterials(bpy.types.Operator):
    bl_idname = "rinasplugin.combine_materials"
    bl_label = t("CombineMaterials.label")
    bl_description = t("CombineMaterials.description")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        # Switch to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
    
        armature = get_armature(context)
        if not armature:
            return {'CANCELLED'}
            
        meshes = get_meshes(armature)
        if not meshes:
            return {'CANCELLED'}
        
        # Switch to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        self.consolidate_materials(meshes)
        
        self.cleanmatslots()
        self.remove_unused_materials()

        # Switch to Object Mode before cleaning material slots
        bpy.ops.object.mode_set(mode='OBJECT')

        self.clean_material_names(meshes)  # Call the clean_material_names method

        # Switch to Object Mode again before setting the active object
        bpy.ops.object.mode_set(mode='OBJECT')

        # Set the active object to the armature
        bpy.context.view_layer.objects.active = armature
        
        return {'FINISHED'}

    def consolidate_materials(self, objects):
        mat_mapping = {}
        num_combined = 0

        # Set to keep track of used materials
        used_materials = set()

        for ob in objects:
            for slot in ob.material_slots:
                mat = slot.material
                if mat is not None:
                    used_materials.add(mat)

                    base_name = get_base_name(mat.name)

                    if base_name in mat_mapping:
                        base_mat = mat_mapping[base_name]
                        if materials_match(base_mat, mat):    
                            num_combined += 1
                            slot.material = base_mat
                    else:
                        mat_mapping[base_name] = mat
        
        report_consolidated(self, num_combined)

    def cleanmatslots(self):
        # Update the context
        bpy.context.view_layer.update()
        objs = bpy.context.selected_editable_objects

        for ob in objs:
            if ob.type == 'MESH':
                bpy.context.view_layer.objects.active = ob  # Set the active object
                bpy.ops.object.material_slot_remove_unused()
    
    def remove_unused_materials(self):
        # Set to keep track of materials actually assigned to faces
        assigned_materials = set()

        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for face in obj.data.polygons:
                    assigned_materials.add(obj.data.materials[face.material_index])

        # Remove materials not assigned to any faces
        for mat in bpy.data.materials:
            if mat not in assigned_materials:
                bpy.data.materials.remove(mat, do_unlink=True)

    def clean_material_names(self, objects):
        for obj in objects:
            if obj.type == 'MESH':
                clean_material_names(obj)
