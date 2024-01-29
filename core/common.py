import bpy
import re

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
