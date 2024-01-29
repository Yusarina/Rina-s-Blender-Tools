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

def clean_material_names(mesh):
    for j, mat in enumerate(mesh.material_slots):
        if mat.name.endswith('.001'):
            mesh.active_material_index = j
            mesh.active_material.name = mat.name[:-4]
        if mat.name.endswith(('. 001', ' .001')):
            mesh.active_material_index = j
            mesh.active_material.name = mat.name[:-5]
