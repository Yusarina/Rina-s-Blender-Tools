bl_info = {
    "name": "Rina's Blender Tools",
    "author": "Yusarina",
    "description": "A collection of tools to help make models easier to work with in VRChat or other Games.",
    "version": (4, 1, 0, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Sidebar",
    "description": "An set of tools to help shorten steps needed to optimize models into VRChat or other Games. Currently only does a few things but I planning to build even more features into these tools.",
	"warning": "",
	"wiki_url": "https://github.com/Yusarina/Rina-s-Blender-Tools/wiki",
	"tracker_url": "https://github.com/Yusarina/Rina-s-Blender-Tools/issues",
	"category": ""
}

import bpy
import sys
import os
import importlib

# Check if Blender version is supported
if bpy.app.version < (4, 1, 0) or bpy.app.version > (4, 1, 99):
    raise Exception("This addon requires Blender 4.1. Versions below 4.1 and above 4.1 are not supported.")

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from bpy.props import EnumProperty
from . import addon_updater_ops
from ui.settings import SettingsSubMenu
from addon_updater_ops import updater
from core.registry import registered_classes

import core.addonpreferences
import core.translations
import core.common
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

importlib.reload(core.addonpreferences)
importlib.reload(core.translations)
importlib.reload(core.common)
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

@addon_updater_ops.make_annotations
class UpdaterPreferences(bpy.types.AddonPreferences):
	"""Demo bare-bones preferences"""
	bl_idname = __package__

	# Addon updater preferences.

	auto_check_update = bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False)

	updater_interval_months = bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)

	updater_interval_days = bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)

	updater_interval_hours = bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)

	updater_interval_minutes = bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59) 

	def draw(self, context):
		layout = self.layout

		# Works best if a column, or even just self.layout.
		mainrow = layout.row()
		col = mainrow.column()

		# Updater draw function, could also pass in col as third arg.
		addon_updater_ops.update_settings_ui(self, context)
        
classes = (
    SettingsSubMenu,
    UpdaterPreferences
) 

def register():
    core.translations.load_translations()
    addon_updater_ops.register(bl_info)
    bpy.app.handlers.save_post.append(lambda dummy: core.addonpreferences.addon_prefs.save_preferences(core.addonpreferences.addon_prefs.addon_prefs_filepath))
    bpy.app.handlers.load_post.append(lambda dummy: core.addonpreferences.addon_prefs.load_preferences(core.addonpreferences.addon_prefs.addon_prefs_filepath))
    bpy.types.Scene.merge_base_bone = bpy.props.StringProperty()
    bpy.types.Scene.merge_ratio = bpy.props.FloatProperty(min=0.0, max=100.0, default=50.0)
    bpy.types.Scene.show_quick_access = bpy.props.BoolProperty(name="Show Quick Access", default=True)
    bpy.types.Scene.show_other_options = bpy.props.BoolProperty(name="Show Other Options", default=False)
    bpy.types.Scene.show_optimization = bpy.props.BoolProperty(name="Show Optimization", default=False)
    bpy.types.Scene.show_settings = bpy.props.BoolProperty(name="Show Settings", default=False)
    bpy.types.Scene.show_credits = bpy.props.BoolProperty(name="Show Credits", default=False)
    bpy.types.Scene.keep_merged_bones = bpy.props.BoolProperty(name="Keep Merged Bones", default=False)
    bpy.types.Scene.show_mesh_options = bpy.props.BoolProperty(name="Show Mesh Options", default=False)
    bpy.types.Scene.show_bones_options = bpy.props.BoolProperty(name="Show Bone Options", default=False)

    for cls in classes:
            addon_updater_ops.make_annotations(cls)

    for cls in registered_classes:
        print(f"Registering class: {cls.__name__}") 
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.plugin_language = bpy.props.EnumProperty(
        name="Plugin Language",
        items=core.translations.language_items,
        default="en",
        update=core.translations.update_language  
    )

    updater.check_for_update_now()
    
def unregister():
    del bpy.types.Scene.merge_base_bone
    del bpy.types.Scene.merge_ratio
    del bpy.types.Scene.show_credits
    del bpy.types.Scene.show_optimization
    del bpy.types.Scene.show_quick_access
    del bpy.types.Scene.show_settings
    del bpy.types.Scene.plugin_language
    del bpy.types.Scene.keep_merged_bones
    del bpy.types.Scene.show_mesh_options
    del bpy.types.Scene.show_bones_options
    core.translations.load_translations()
    addon_updater_ops.unregister()   

    for cls in reversed(registered_classes):
        bpy.utils.unregister_class(cls) 

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
