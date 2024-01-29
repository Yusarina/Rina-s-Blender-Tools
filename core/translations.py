import bpy
import csv
import os

translations = {}
current_language = "en"

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
                "ko": row["ko"]
            }

def set_language(language):
    global current_language
    current_language = language

def t(text_id):

    if text_id in translations and current_language in translations[text_id]:
        return translations[text_id][current_language]

    return text_id
