import bpy
import bmesh
import numpy as np


import mathutils
from functools import lru_cache
from core.translations import t
from bpy.types import Object, ShapeKey
from bmesh import new
from bmesh.types import BMVert

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
        if mat.name.endswith(('.0+', ' 0+')):
            mesh.active_material_index = j
            mesh.active_material.name = mat.name[:-len(mat.name.rstrip('0')) - 1]

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

def has_shapekeys(mesh_obj: Object) -> bool:
    return mesh_obj.data.shape_keys is not None

@lru_cache(maxsize=None)
def _get_shape_key_co(shape_key: ShapeKey) -> np.ndarray:
    return np.array([v.co for v in shape_key.data])

def remove_doubles(mesh_obj: Object, threshold: float, save_shapes: bool = True) -> int:
    if not isinstance(mesh_obj, Object):
        raise TypeError("mesh_obj must be an instance of Object")
    if threshold <= 0:
        raise ValueError("Threshold must be positive")

    mesh = mesh_obj.data

    if not has_shapekeys(mesh_obj) or len(mesh.shape_keys.key_blocks) == 1:
        return 0

    pre_polygons = len(mesh.polygons)

    if save_shapes:
        vertex_selection = np.full(len(mesh.vertices), True, dtype=bool)
        cached_co_getter = lru_cache(maxsize=None)(_get_shape_key_co)
        for kb in mesh.shape_keys.key_blocks[1:]:
            relative_key = kb.relative_key
            if kb == relative_key:
                continue
            same = cached_co_getter(kb) == cached_co_getter(relative_key)
            vertex_not_moved_by_shape_key = np.all(same.reshape(-1, 3), axis=1)
            vertex_selection &= vertex_not_moved_by_shape_key
        del cached_co_getter

        if not vertex_selection.any():
            return 0

        if vertex_selection.all():
            save_shapes = False
        else:
            bpy.context.view_layer.objects.active = mesh_obj
            bpy.ops.object.mode_set(mode='EDIT')
            verts = list(bmesh.from_edit_mesh(mesh).verts)
            for v in verts:
                v.select = vertex_selection[v.index]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.update()
    else:
        bmesh.ops.select_all(bm, action='DESELECT')

    bm = bmesh.new()
    bm.from_mesh(mesh)
    if save_shapes:
        verts = [v for v in bm.verts if v.select]
    else:
        verts = bm.verts

    total_verts = len(verts)
    progress_steps = 100
    progress_step_size = total_verts // progress_steps
    progress = 0

    bmesh.ops.remove_doubles(bm, verts=verts, dist=threshold)

    while progress < total_verts:
        bm.select_flush(True)
        bpy.context.view_layer.update()
        bpy.context.window_manager.progress_update(progress / total_verts)
        progress += progress_step_size

    bm.to_mesh(mesh)

    return pre_polygons - len(mesh.polygons)
