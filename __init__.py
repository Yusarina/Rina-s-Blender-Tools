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

# Check if Blender version is supported
if bpy.app.version < (4, 0, 0):
    raise Exception("This addon requires Blender 4.0 or newer, 3.6 is not supported at")

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from bpy.props import EnumProperty

import core.common
import core.addonpreferences
import core.translations
import core.updater
import functions.otheroptimizations
import functions.combine_materials
import functions.join_meshes
import functions.separate_meshes
import functions.bones
import ui.main
import ui.quick_access
import ui.optimization
import ui.otheroptions
import ui.credits
import ui.settings

importlib.reload(core.common)
importlib.reload(core.addonpreferences)
importlib.reload(core.translations)
importlib.reload(core.updater)
importlib.reload(functions.otheroptimizations)
importlib.reload(functions.combine_materials)
importlib.reload(functions.join_meshes)
importlib.reload(functions.separate_meshes)
importlib.reload(functions.bones)
importlib.reload(ui.main)
importlib.reload(ui.quick_access)
importlib.reload(ui.optimization)
importlib.reload(ui.otheroptions)
importlib.reload(ui.credits)
importlib.reload(ui.settings)    
    
def register():
    core.translations.load_translations()
    bpy.utils.register_class(core.addonpreferences.AddonPreferences)
    bpy.utils.register_class(core.updater.AddonUpdater)
    bpy.app.handlers.save_post.append(lambda dummy: core.addonpreferences.addon_prefs.save_preferences(core.addonpreferences.addon_prefs.addon_prefs_filepath))
    bpy.app.handlers.load_post.append(lambda dummy: core.addonpreferences.addon_prefs.load_preferences(core.addonpreferences.addon_prefs.addon_prefs_filepath))
    bpy.utils.register_class(functions.otheroptimizations.RemoveDoubles)
    bpy.utils.register_class(functions.combine_materials.CombineMaterials)
    bpy.utils.register_class(functions.join_meshes.JoinAllMeshes)
    bpy.utils.register_class(functions.join_meshes.JoinSelectedMeshes)
    bpy.utils.register_class(functions.separate_meshes.SeparateByMaterials)
    bpy.utils.register_class(functions.separate_meshes.SeparateLooseParts)
    bpy.utils.register_class(functions.bones.MergeBones)
    bpy.utils.register_class(functions.bones.RemoveZeroWeightBones)
    bpy.utils.register_class(functions.bones.RemoveConstraints)
    bpy.utils.register_class(ui.main.RinasBlenderToolsPanel)
    bpy.utils.register_class(ui.quick_access.QuickAccessSubMenu)
    bpy.utils.register_class(ui.optimization.OptimizationSubMenu)
    bpy.utils.register_class(ui.otheroptions.OtherOptionsSubMenu)
    bpy.utils.register_class(ui.settings.SettingsSubMenu)
    bpy.utils.register_class(ui.credits.CreditsSubMenu)
    bpy.utils.register_class(ui.optimization.RinasPluginProps)
    bpy.types.Scene.merge_base_bone = bpy.props.StringProperty()
    bpy.types.Scene.rinas_plugin = bpy.props.PointerProperty(type=ui.optimization.RinasPluginProps)
    bpy.types.Scene.merge_ratio = bpy.props.FloatProperty(min=0.0, max=100.0, default=50.0)
    bpy.types.Scene.show_quick_access = bpy.props.BoolProperty(name="Show Quick Access", default=True)
    bpy.types.Scene.show_other_options = bpy.props.BoolProperty(name="Show Other Options", default=True)
    bpy.types.Scene.show_optimization = bpy.props.BoolProperty(name="Show Optimization", default=False)
    bpy.types.Scene.show_settings = bpy.props.BoolProperty(name="Show Settings", default=True)
    bpy.types.Scene.show_credits = bpy.props.BoolProperty(name="Show Credits", default=False)
    
    bpy.types.Scene.plugin_language = bpy.props.EnumProperty(
        name="Plugin Language",
        items=core.translations.language_items,
        default="en",
        update=core.translations.update_language  
    )
    
def unregister():
    bpy.utils.unregister_class(functions.otheroptimizations.RemoveDoubles)
    bpy.utils.unregister_class(functions.combine_materials.CombineMaterials)
    bpy.utils.unregister_class(functions.join_meshes.JoinAllMeshes)
    bpy.utils.unregister_class(functions.join_meshes.JoinSelectedMeshes)
    bpy.utils.unregister_class(functions.separate_meshes.SeparateByMaterials)
    bpy.utils.unregister_class(functions.separate_meshes.SeparateLooseParts)
    bpy.utils.unregister_class(functions.bones.MergeBones)
    bpy.utils.unregister_class(functions.bones.RemoveZeroWeightBones)
    bpy.utils.unregister_class(functions.bones.RemoveConstraints)
    bpy.utils.unregister_class(ui.main.RinasBlenderToolsPanel)
    bpy.utils.unregister_class(ui.quick_access.QuickAccessSubMenu)
    bpy.utils.unregister_class(ui.optimization.OptimizationSubMenu)
    bpy.utils.unregister_class(ui.otheroptions.OtherOptionsSubMenu)
    bpy.utils.unregister_class(ui.credits.CreditsSubMenu)
    bpy.utils.unregister_class(ui.settings.SettingsSubMenu)
    bpy.utils.unregister_class(core.updater.AddonUpdater)
    bpy.utils.unregister_class(core.addonpreferences.AddonPreferences)
    del bpy.types.Scene.merge_base_bone
    del bpy.types.Scene.merge_ratio
    del bpy.types.Scene.show_credits
    del bpy.types.Scene.show_optimization
    del bpy.types.Scene.show_quick_access
    del bpy.types.Scene.show_settings
    del bpy.types.Scene.plugin_language
    del bpy.types.Scene.rinas_plugin
    bpy.utils.unregister_class(ui.optimization.RinasPluginProps)
    core.translations.load_translations()

    # Check if the load_post handler is in the list before removing it
    load_post_handler = core.addonpreferences.AddonPreferences.load_preferences
    if load_post_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_post_handler)

    # Check if the save_post handler is in the list before removing it
    save_post_handler = core.addonpreferences.AddonPreferences.save_preferences
    if save_post_handler in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(save_post_handler)

if __name__ == '__main__':
    register()
