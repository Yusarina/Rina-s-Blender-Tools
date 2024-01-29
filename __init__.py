bl_info = {
    "name": "Rina's Blender Tools",
    "author": "Yusarina",
    "version": (0, 0, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar",
    "description": "Bunch of Tools to help you make your models for VRChat",
    "warning": "",
    "doc_url": "",
    "category": "",
}


import bpy
import sys
import os
import importlib

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import core.common
import functions.combine_materials
import functions.join_meshes
import functions.separate_meshes
import ui.main

importlib.reload(core.common)
importlib.reload(functions.combine_materials)
importlib.reload(functions.join_meshes)
importlib.reload(functions.separate_meshes)
importlib.reload(ui.main)

def register():
    bpy.utils.register_class(functions.combine_materials.CombineMaterials)
    bpy.utils.register_class(functions.join_meshes.JoinAllMeshes)
    bpy.utils.register_class(functions.join_meshes.JoinSelectedMeshes)
    bpy.utils.register_class(functions.separate_meshes.SeparateByMesh)
    bpy.utils.register_class(ui.main.RinasBlenderToolsPanel)

def unregister():
    bpy.utils.unregister_class(functions.combine_materials.CombineMaterials)
    bpy.utils.unregister_class(functions.join_meshes.JoinAllMeshes)
    bpy.utils.unregister_class(functions.join_meshes.JoinSelectedMeshes)
    bpy.utils.unregister_class(functions.separate_meshes.SeparateByMesh)
    bpy.utils.unregister_class(ui.main.RinasBlenderToolsPanel)

if __name__ == '__main__':
    register()
