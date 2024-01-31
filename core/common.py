import bpy
import re
import bmesh
from core.translations import t

def get_armature(context):
    """Fetch armature from scene"""
    for ob in context.scene.objects:
        if ob.type == 'ARMATURE':
            return ob
            
def get_meshes(armature):
   """Get armature's mesh children"""
   meshes = []
   for ob in armature.children:
       if ob.type == 'MESH':
           meshes.append(ob)
   return meshes

### Clean up material names in the given mesh by removing the '.001' suffix.
def clean_material_names(mesh):
    for j, mat in enumerate(mesh.material_slots):
        if mat.name.endswith('.001'):
            mesh.active_material_index = j
            mesh.active_material.name = mat.name[:-4]
        if mat.name.endswith(('. 001', ' .001')):
            mesh.active_material_index = j
            mesh.active_material.name = mat.name[:-5]

# This will fix faulty uv coordinates, cats did this a other way which can have unintended consequences, 
# this is the best way i could of think of doing this for the time being.

def fix_uv_coordinates(context):
    obj = context.object

    # Check if the object is in Edit Mode
    if obj.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')

    # Check if the object has any mesh data
    if obj.type == 'MESH' and obj.data:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.average_islands_scale()

        # Switch back to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("Object is not a valid mesh with UV data")

import bpy
import bmesh

class RemoveDoubles(bpy.types.Operator):
    bl_idname = "rinasplugin.remove_doubles"    
    bl_label = t("RemoveDoubles.label")
    bl_description = t('RemoveDoubles.description')
    bl_options = {'REGISTER', 'UNDO'}

    distance_threshold: bpy.props.FloatProperty(
        name="Merge Distance",
        default=0.0001,
        precision=4,
        description="Maximum distance between elements to merge"
    )

    @classmethod
    def poll(cls, context):
        return get_armature(context) is not None

    def execute(self, context):
        armature = get_armature(context)
        meshes = get_meshes(armature)

        # Switch to Object Mode to ensure correct context
        bpy.ops.object.mode_set(mode='OBJECT')
        
        if not meshes:
            return {'CANCELLED'}

        for mesh in meshes:
            obj = mesh

            # Check if shape keys are present
            if obj.data.shape_keys:
                continue  # Skip mesh if it has shape keys

            bpy.ops.object.select_all(action='DESELECT') 
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            
            # Shape key save
            shape_keys = obj.data.shape_keys
            shape_key_coords = []
            if shape_keys:
                for key_block in shape_keys.key_blocks:
                    coords = [v.co.copy() for v in key_block.data]
                    shape_key_coords.append(coords)
                    
            # Enter edit mode
            bpy.ops.object.mode_set(mode='EDIT')
            
            # Get bmesh, remove doubles
            bm = bmesh.from_edit_mesh(obj.data)
            
            # Remove doubles using merge_by_distance
            bpy.ops.mesh.select_all(action='SELECT')

            bpy.ops.mesh.remove_doubles(threshold=self.distance_threshold)
            
            # Write bmesh back
            bmesh.update_edit_mesh(obj.data)
            
            # Exit edit mode
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Restore shape keys
            if shape_keys:
                for key_block, coords in zip(shape_keys.key_blocks, shape_key_coords):
                    for i, v in enumerate(key_block.data):
                        v.co = coords[i]
                        
        return {'FINISHED'}