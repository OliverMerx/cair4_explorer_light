"""
====================================
🎉 Willkommen im CAIR4 Use Cases App
====================================

Dieser View dient als Willkommensseite und zeigt die Anzahl aller Kapitel 
und Views an. Die Views können über die Seitenleiste ausgewählt werden.
"""

# === 📦 Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.importlib_lib import importlib
from utils.core.CAIR4_background_image_util import set_background

# === 📂 Pfad zur Config-Datei ===
CONFIG_FILE = "/core/CAIR4_explorer_config.py"

# === 🔄 Utility-Funktion zum Laden der Config ===
def load_config():
    """
    Lädt die Konfiguration aus der CAIR4_main_config.py Datei.
    """
    path = st.session_state.base_path + CONFIG_FILE
    spec = importlib.util.spec_from_file_location("config_module", path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    
    return config_module.COLLECTIONS, config_module.MODEL_OPTIONS


# === 2️⃣ Willkommens-View ===
def render_about_video_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    """
    Standard-Willkommensscreen für die CAIR4-App mit Overlay-Design, Video und weiterführendem Button.
    """
    
    if st.session_state.selected_use_case is not use_case:
        st.session_state["selected_content_index"] = 1
        st.session_state.selected_use_case = use_case


    # 🔄 Alle Kapitel und Use Cases laden
    collections, model_options = load_config()

    chapters = {}
    for entry in collections.values():
        chapter_name = entry.get("chapter", "Unbekannt")
        if chapter_name not in chapters:
            chapters[chapter_name] = []
        chapters[chapter_name].append({
            "title": entry.get("title", "Untitled"),
            "description": entry.get("description", "Keine Beschreibung verfügbar.")
        })
        
    models = len(model_options)

    total_chapters = len(chapters) - 1
    total_views = sum(len(views) for views in chapters.values()) - 4
    total_models = models
    video_url = context

    # 🎨 **Theme-Farben aus Session-Variablen**
    bg_color = st.session_state.bg_color
    header_color = st.session_state.header_color
    text_color = st.session_state.text_color

    # 📌 **CSS für das Overlay**
    st.markdown(f"""
        <style>
            .overlay-box {{
                background-color: {bg_color}!important;
                padding-left: 15px;
                padding-right: 15px;
                margin-bottom: 35px;
                margin-top: -50px;
                width: fit-content;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
            }}
            .overlay-title {{
                font-size: 40px;
                font-weight: bold;
                color: {header_color};
            }}
            .overlay-description {{
                font-size: 20px;
                color: {text_color};
                max-width: 1000px;
                padding-top: 10px;
                padding-bottom: 10px;
            }}
            .video-container {{
                display: flex;
                justify-content: center;
                margin-top: 20px;
            }}
        </style>
    """, unsafe_allow_html=True)

    # 🎬 **Video & Beschreibung im Overlay**
    st.markdown(f"""
        <div class="overlay-box">
            <div class="overlay-title">{title}</div>
        </div>
        <div class="overlay-box">
            <div class="overlay-description">
                {description}
                <br><br>
                <div class="video-container">
                    <iframe width="700" height="420" src="{video_url}" frameborder="0" allowfullscreen></iframe>
                </div>
                <br>
                <b>Dieser CAIR4 Use Case Explorer enthält {total_chapters} KI-Kapitel mit {total_views} KI-Use Cases und {total_models} verschiedenen LLM-Varianten.</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 🖼 **Hintergrund setzen**
    file = st.session_state.background_image  
    image_path = st.session_state.base_path + file  
    set_background(image_path)
    
    # 🟢 **Weiterführender Button**
    view_name = "API-Keys"
    st.markdown(f"""
        <a href="?view={view_name}" target="_self">
            <button style="
                color: {st.session_state.bg_color};
                background-color: {st.session_state.header_color};
                font-size:24px;
                padding-top: 5px;
                padding-bottom: 5px;
                padding-left: 20px;
                padding-right: 20px;
                border-radius: 8px;
                border: 2px solid {st.session_state.bg_color};
                cursor: pointer;">
                weiter zum Intro-Video
            </button>
        </a>
    """, unsafe_allow_html=True)