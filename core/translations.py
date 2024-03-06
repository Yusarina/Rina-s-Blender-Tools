import bpy
import os
import csv
import json

# Retrieve the package name using a direct import
from . import __package__

language_items = [
    ("en", "English", "English"),
    ("fr", "French", "French"),
    ("sp", "Spanish", "Spanish"),
    ("ja", "Japanese", "Japanese"),
    ("ko", "Korean", "Korean")
]

current_language = "en"
translations = {}

def update_language(self, context):
    set_language(context.scene.plugin_language)
    bpy.ops.script.reload()

def load_translations():
    global translations

    # Construct full path to CSV file
    dirname = os.path.dirname(__file__)
    csv_path = os.path.join(dirname, "RinasBlenderToolsTranslations.csv")

    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            text_id = row["name"]

            translations[text_id] = {
                "en": row["en"],
                "ja": row["ja"],
                "ko": row["ko"],
                "fr": row["fr"],
                "sp": row["sp"]
            }

def t(text_id):
    if text_id in translations and current_language in translations[text_id]:
        return translations[text_id][current_language]

def set_language(language):
    global current_language
    current_language = language

    # Save the language in user preferences
    addon_prefs = bpy.context.preferences.addons.get(__package__)
    if addon_prefs:
        addon_prefs = addon_prefs.preferences
        addon_prefs.plugin_language = language

    # Save the language in JSON file in the core folder
    save_language_to_json(language)

def save_language_to_json(language):
    json_filepath = os.path.join(os.path.dirname(__file__), 'settings.json')  # Update the path to the core folder
    preferences = {"plugin_language": language}
    with open(json_filepath, 'w') as file:
        json.dump(preferences, file)

# Load language from JSON file
def load_language_from_json():
    json_filepath = os.path.join(os.path.dirname(__file__), 'settings.json')  # Update the path to the core folder
    try:
        with open(json_filepath, 'r') as file:
            preferences = json.load(file)
            set_language(preferences.get("plugin_language", "en"))
    except FileNotFoundError:
        pass

# Load translations and language when Blender starts
load_translations()
load_language_from_json()