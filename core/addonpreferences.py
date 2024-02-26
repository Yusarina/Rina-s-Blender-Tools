import bpy
import json
import os

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    plugin_language: bpy.props.StringProperty(
        name="Plugin Language",
        description="Select the language for the plugin",
        default="en",
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Addon Preferences")
        layout.prop(self, "plugin_language")

    def save_preferences(self, filepath):
        preferences = {"plugin_language": self.plugin_language}
        with open(filepath, 'w') as file:
            json.dump(preferences, file)

    def load_preferences(self, filepath):
        try:
            with open(filepath, 'r') as file:
                preferences = json.load(file)
                self.plugin_language = preferences.get("plugin_language", "en")
        except FileNotFoundError:
            # If the file doesn't exist, create an empty file
            with open(filepath, 'w') as file:
                json.dump({}, file)

# Load preferences when Blender starts
addon_prefs_filepath = os.path.join(os.path.dirname(__file__), 'settings.json')  # Update the path to the core folder
addon_prefs = bpy.context.preferences.addons.get(__package__)
if addon_prefs:
    addon_prefs = addon_prefs.preferences
    addon_prefs.load_preferences(addon_prefs_filepath)

# Register the preference update and load handlers
bpy.app.handlers.save_post.append(lambda dummy: addon_prefs.save_preferences(addon_prefs_filepath))
bpy.app.handlers.load_post.append(lambda dummy: addon_prefs.load_preferences(addon_prefs_filepath))
