bl_info = {
    "name": "Rina's Blender Tools",
    "author": "Yusarina",
    "version": (0, 0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar",
    "description": "An set of tools to help shorten steps needed to optimize models into VRChat or other Games. Currently only does a few things but I planning to build even more features into these tools.",
    "warning": "",
    "doc_url": "",
    "category": "",
}

import bpy
import sys
import os
import importlib
import addon_utils

# Check if Blender version is supported
if bpy.app.version < (4, 0, 0):
    raise Exception("This addon requires Blender 4.0 or newer, 3.6 is not supported at")

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from bpy.props import EnumProperty

import core.common
import functions.combine_materials
import functions.join_meshes
import functions.separate_meshes
import ui.main
import ui.quick_access
import ui.optimization
import ui.credits
import ui.settings
import core.translations

importlib.reload(core.common)
importlib.reload(functions.combine_materials)
importlib.reload(functions.join_meshes)
importlib.reload(functions.separate_meshes)
importlib.reload(ui.main)
importlib.reload(ui.quick_access)
importlib.reload(ui.optimization)
importlib.reload(ui.credits)
importlib.reload(ui.settings)
importlib.reload(core.translations)

def update_language(self, context):
    core.translations.set_language(context.scene.plugin_language)
    
def register():
    bpy.utils.register_class(ui.main.RinasBlenderToolsPanel)
    bpy.utils.register_class(ui.quick_access.QuickAccessSubMenu)
    bpy.utils.register_class(ui.optimization.OptimizationSubMenu)
    bpy.utils.register_class(ui.credits.CreditsSubMenu)
    bpy.utils.register_class(ui.settings.SettingsSubMenu)
    bpy.types.Scene.show_credits = bpy.props.BoolProperty(name="Show Credits", default=False)
    bpy.types.Scene.show_optimization = bpy.props.BoolProperty(name="Show Optimization", default=False)
    bpy.types.Scene.show_quick_access = bpy.props.BoolProperty(name="Show Quick Access", default=True)
    bpy.types.Scene.show_settings = bpy.props.BoolProperty(name="Show Settings", default=True)
    bpy.utils.register_class(functions.combine_materials.CombineMaterials)
    bpy.utils.register_class(functions.join_meshes.JoinAllMeshes)
    bpy.utils.register_class(functions.join_meshes.JoinSelectedMeshes)
    bpy.utils.register_class(functions.separate_meshes.SeparateByMesh)
    core.translations.load_translations()

    #Define a list of supported languages
    language_items = [
        ("en", "English", "English"),
        ("ja", "Japanese", "Japanese"),
        ("ko", "Korean", "Korean"),
    ]

    bpy.types.Scene.plugin_language = bpy.props.EnumProperty(
        name="Plugin Language",
        items=language_items,
        default="en",
        update=update_language
    )

def unregister():
    bpy.utils.unregister_class(functions.combine_materials.CombineMaterials)
    bpy.utils.unregister_class(functions.join_meshes.JoinAllMeshes)
    bpy.utils.unregister_class(functions.join_meshes.JoinSelectedMeshes)
    bpy.utils.unregister_class(functions.separate_meshes.SeparateByMesh)
    bpy.utils.unregister_class(ui.main.RinasBlenderToolsPanel)
    bpy.utils.unregister_class(ui.quick_access.QuickAccessSubMenu)
    bpy.utils.unregister_class(ui.optimization.OptimizationSubMenu)
    bpy.utils.unregister_class(ui.credits.CreditsSubMenu)
    del bpy.types.Scene.show_credits
    del bpy.types.Scene.show_optimization
    del bpy.types.Scene.show_quick_access
    del bpy.types.Scene.show_settings
    core.translations.load_translations()
    bpy.utils.unregister_class(ui.settings.SettingsSubMenu)
    del bpy.types.Scene.plugin_language

if __name__ == '__main__':
    register()
