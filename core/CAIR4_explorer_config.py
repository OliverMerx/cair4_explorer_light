# ======================================================
# CAIR4_explorer_config.py
# Rollenbasierte Konfiguration von Use Cases & Modellen
# ======================================================

import streamlit as st
import sqlite3
import ast
from collections import defaultdict

# Rolle für Standard-User von Light-Version anstatt DB-Zugang
guest_light = {
    "guest_light": {
    "chapters": {
        "Homepage": "all",
        "1. KI-Basics": "all",
        "2. KI-Advanced": "all",
        "3. HR & Textverarbeitung": "all",
        "4. Sales & CRM": "all",
        "5. Finance": "all",
        "6. Health": "all",
        "7. Research": "all",
        "8. ATCF-Module": "all",
    },
    "models": "all"
    }
}

# === Rohdaten: Use Case Struktur & Modell-Optionen ===
from core.CAIR4_explorer_config_raw import (
    CAIR4_COLLECTIONS as RAW_COLLECTIONS,
    API_MODEL_OPTIONS as RAW_API_MODELS,
    LOCAL_MODEL_OPTIONS as RAW_LOCAL_MODELS
)

# === DB-Pfad ===
#DB_PATH = "user_access.sqlite"

CURRENT_USER = st.session_state.get("current_user", "guest_light")
USER_ROLE = st.session_state.get("user_role", "guest_light")

# === Rollen-Zugriffsrechte dynamisch aus Datenbank laden ===
def load_role_access_from_db():

    role_access = defaultdict(lambda: {"chapters": [], "models": []})
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Kapitel-Zugriff
    cursor.execute("SELECT role, chapter FROM access_chapter")
    for role, chapter in cursor.fetchall():
        role_access[role]["chapters"].append(chapter)

    # Excluded Use Cases
    cursor.execute("SELECT role, chapter, uc_key FROM excluded_use_cases")
    for role, chapter, uc_key in cursor.fetchall():
        role_access[role].setdefault("excluded", set()).add((chapter, uc_key))

    # Modell-Zugriff
    cursor.execute("SELECT role, model_id FROM access_model")
    for role, model in cursor.fetchall():
        role_access[role]["models"].append(model)

    conn.close()

    # Kapitelstruktur anpassen
    for role in role_access:
        if "all" in role_access[role]["chapters"]:
            role_access[role]["chapters"] = "all"
        else:
            role_access[role]["chapters"] = {
                ch: "all" for ch in role_access[role]["chapters"]
            }

        if "all" in role_access[role]["models"]:
            role_access[role]["models"] = "all"

    return dict(role_access)


#ROLE_ACCESS = load_role_access_from_db() #kein Inhalt von Light-Version
ROLE_ACCESS = guest_light

def parse_collection(raw_collections, access):
    parsed = {}
    allowed_chapters = access.get("chapters", {})
    excluded_uc = access.get("excluded", set())  # << Wichtig

    for chapter_name, chapter_data in raw_collections.items():
        use_cases = chapter_data.get("use_cases", {})

        if allowed_chapters == "all":
            filtered_use_cases = {
                k: v for k, v in use_cases.items()
                if v.get("enabled", True) and (chapter_name, k) not in excluded_uc
            }
            if filtered_use_cases:
                parsed[chapter_name] = {"use_cases": filtered_use_cases}
            continue

        allowed_uc = allowed_chapters.get(chapter_name)
        if not allowed_uc:
            continue

        if allowed_uc == "all":
            filtered_uc = {
                k: v for k, v in use_cases.items()
                if v.get("enabled", True) and (chapter_name, k) not in excluded_uc
            }
            if filtered_uc:
                parsed[chapter_name] = {"use_cases": filtered_uc}
        else:
            filtered_uc = {
                k: v for k, v in use_cases.items()
                if k in allowed_uc and v.get("enabled", True) and (chapter_name, k) not in excluded_uc
            }
            if filtered_uc:
                parsed[chapter_name] = {"use_cases": filtered_uc}

    return parsed


# === Trainingsdaten parsern ===
def parse_training_data(collections_data):
    training = {}
    for chapter in collections_data.values():
        for uc in chapter.get("use_cases", {}).values():
            if "training_sections" in uc:
                training[uc["name"]] = {
                    "title": f"Explorer für {uc['title']}",
                    "description": "",
                    "sections": uc["training_sections"]
                }
    return training


# === Modellformate konvertieren ===
def convert_api_model_options(data):
    if isinstance(data, tuple) and len(data) == 1 and isinstance(data[0], dict):
        new_format = data[0]
    elif isinstance(data, dict):
        new_format = data
    else:
        print(f"Warnung: Unerwartetes Datenformat: {type(data)}")
        return {}

    old_format_list = []
    for model_id, metadata in new_format.items():
        label = metadata.get('label')
        if label:
            old_format_list.append(f"'{label}': '{model_id}',")

    if old_format_list:
        old_format_string = "{\n    " + "\n    ".join(old_format_list)[:-1] + "\n}"
    else:
        old_format_string = "{}"

    try:
        old_format_dict = ast.literal_eval(old_format_string)
    except (SyntaxError, ValueError) as e:
        print(f"Fehler beim Parsen der Modelle: {e}")
        old_format_dict = {}

    return old_format_dict


# === Modellfilterung anwenden ===
def parse_model_collection(full_model_dict, allowed_keys):
    return {
        label: key for label, key in full_model_dict.items() if key in allowed_keys
    }


# === Hauptfunktion für Sammlung & Modelle pro Nutzerrolle ===
def user_collection(role):
    user_access = ROLE_ACCESS.get(role, {})
    allowed_models = user_access.get("models", [])

    filtered_raw = parse_collection(RAW_COLLECTIONS, user_access)

    collections = {}
    order = 0
    for chapter, content in filtered_raw.items():
        for uc_name, uc_data in content["use_cases"].items():
            uc_parsed = uc_data.copy()
            uc_parsed["chapter"] = chapter
            uc_parsed["order"] = order
            collections[uc_name] = uc_parsed
            order += 1

    TRAINING = parse_training_data(filtered_raw)

    old_api_models_converted = convert_api_model_options(RAW_API_MODELS)
    old_local_models_converted = convert_api_model_options(RAW_LOCAL_MODELS)

    if allowed_models == "all":
        API_MODELS = old_api_models_converted
        LOCAL_MODELS = old_local_models_converted
    else:
        API_MODELS = parse_model_collection(old_api_models_converted, allowed_models)
        LOCAL_MODELS = parse_model_collection(old_local_models_converted, allowed_models)

    return collections, API_MODELS, API_MODELS, LOCAL_MODELS, TRAINING


# === Globale Modell-Settings ===
GLOBAL_SETTINGS = {
    'temperature': 0.7,
    'top_p': 0.9,
    'response_length': 'Medium',
    'response_format': 'Continuous Text',
    'summary_length': 0.5
}