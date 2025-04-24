"""
==========================================================
CAIR4 Global Settings Manager (CAIR4_settings_manager.py)
==========================================================

Dieses Modul verwaltet die globalen Einstellungen für die CAIR4-Plattform. 
Es stellt Funktionen bereit, um Konfigurationen im `st.session_state` zu initialisieren, 
zu speichern und aus einer JSON-Datei zu laden.

📌 Funktionen:
- **initialize_global_settings()** → Initialisiert Standardwerte im Session-State.
- **save_global_settings()** → Speichert die aktuellen Einstellungen in eine Datei.
- **load_global_settings()** → Lädt gespeicherte Einstellungen oder setzt Defaults.

✅ Warum ist das wichtig?
- Ermöglicht ein persistentes Speichern von Benutzereinstellungen.
- Erlaubt eine flexible Anpassung von Systemparametern zur Laufzeit.
- Reduziert Fehler durch zentrale Verwaltung der Konfigurationswerte.
"""

# === 1️⃣  Import externer Bibliotheken ===
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json
from pylibs.os_lib import os


def initialize_global_settings(default_settings):
    """
    Initialisiert die globalen Einstellungen im Session State, falls nicht vorhanden.

    Args:
        default_settings (dict): Standardwerte für globale Einstellungen.
    
    Beispiel:
        ```python
        DEFAULT_SETTINGS = {
            "temperature": 0.7,
            "top_p": 0.9,
            "response_length": "Medium",
            "response_format": "Continuous Text"
        }
        initialize_global_settings(DEFAULT_SETTINGS)
        ```
    """
    if "global_settings" not in st.session_state:
        st.session_state.global_settings = default_settings
        print("[INFO] Global settings initialized with default values.")


def save_global_settings(settings_file):
    """
    Speichert die aktuellen globalen Einstellungen in eine JSON-Datei.

    Args:
        settings_file (str): Pfad zur Einstellungsdatei.

    Beispiel:
        ```python
        save_global_settings("config/global_settings.json")
        ```
    """
    try:
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(st.session_state.global_settings, f, indent=4)
        print(f"[INFO] Global settings saved to {settings_file}")

    except Exception as e:
        print(f"[ERROR] Failed to save global settings: {e}")


def load_global_settings(settings_file, default_settings):
    """
    Lädt globale Einstellungen aus einer JSON-Datei oder initialisiert sie mit Standardwerten.

    Args:
        settings_file (str): Pfad zur JSON-Konfigurationsdatei.
        default_settings (dict): Standardwerte für Einstellungen, falls keine Datei existiert.

    Beispiel:
        ```python
        load_global_settings("config/global_settings.json", DEFAULT_SETTINGS)
        ```
    """
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                st.session_state.global_settings = json.load(f)
            print(f"[INFO] Global settings loaded from {settings_file}")

        except json.JSONDecodeError:
            print(f"[WARNING] Invalid JSON format in {settings_file}. Resetting to default settings.")
            initialize_global_settings(default_settings)
            save_global_settings(settings_file)  # Speichert die Standardwerte in die Datei

    else:
        print(f"[INFO] No settings file found. Initializing with default settings.")
        initialize_global_settings(default_settings)
        save_global_settings(settings_file)  # Speichert die Standardwerte direkt in die Datei