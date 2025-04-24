"""
=================================================
🎉 Willkommen im CAIR4 Use Cases App
=================================================

Dieser View dient als Willkommensseite und zeigt die Anzahl aller Kapitel 
und Views an. Die Views können über die Seitenleiste ausgewählt werden.
"""

# === 📦 Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.importlib_lib  import importlib

# === 📂 Pfad zur Config-Datei ===
CONFIG_FILE = "/core/CAIR4_main_config.py"

# === 🔄 Utility-Funktion zum Laden der Config ===
def load_config():
    """
    Lädt die Konfiguration aus der CAIR4_main_config.py Datei.
    """
    path = st.session_state.base_path+CONFIG_FILE
    spec = importlib.util.spec_from_file_location("config_module", path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    
    return config_module.COLLECTIONS

# === 2️⃣ Willkommens-View ===
def render_use_case_welcome_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    """
    Willkommen-View für die Main-App:
    - Zeigt eine Willkommensnachricht an.
    - Zeigt die Anzahl aller Kapitel und Views an.
    - Zwei Pulldowns: Kapitel und Views.
    - Dynamische Ansicht der Beschreibung des ausgewählten Views.
    """

    # 🔄 Alle Kapitel und Use Cases laden
    collections = load_config()

    chapters = {}
    for entry in collections.values():
        chapter_name = entry.get("chapter", "Unbekannt")
        if chapter_name not in chapters:
            chapters[chapter_name] = []
        chapters[chapter_name].append({
            "title": entry.get("title", "Untitled"),
            "description": entry.get("description", "Keine Beschreibung verfügbar.")
        })
        
    total_chapters = len(chapters)
    total_views = sum(len(views) for views in chapters.values())

    st.title("CAIR4 Use Cases")

    st.markdown(
        f"""
        **Willkommen in der CAIR4 Use Case App**!  
        In dieser Anwendung können in {total_chapters} Kapiteln {total_views} verschiedene KI-Use-Cases erkundet werden. 
        Die Kapitel und ihre Use Cases können links in der Seitenleiste ebenso wie verschiedene KI-Modelle ausgewählt werden. 
        Jeder Use Case kann zudem über den roten Hilfebutton auf der rechten Seite genauer analysiert und regulatorisch eingeordnet werden.
        
        Viel Spaß beim Erkunden! 🚀
        """
    )

