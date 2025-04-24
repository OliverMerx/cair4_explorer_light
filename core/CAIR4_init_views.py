from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st    
from pylibs.importlib_lib import importlib

import time

# ✅ Neu: Prüfung auf ersten Start

def stage_container():
    parent = st.empty()  # Eltern-Container existiert in allen Phasen
    parent.empty()  # Temporärer leerer Container zum Löschen des Bildschirms
    time.sleep(0.01)  # Kleine Pause, damit das Frontend mithalten kann
    return parent.container()  # Tatsächlicher Container ersetzt den temporären
    # === core/CAIR4_init_views.py ===

def render_active_view(selected_use_case, use_case_config):

    collections = st.session_state.get("collections",{})
    global_settings = st.session_state.get("global_settings",{})

    stage_container()

    try:
        view_function_path = use_case_config.get("view")
        module_name, function_name = view_function_path.rsplit(".", 1)
        view_module = importlib.import_module(module_name)
        view_function = getattr(view_module, function_name)

        session_file_path = f"CAIR4_data/data/{use_case_config['name']}_sessions.json"
        context = use_case_config.get("context", None)
        title = use_case_config.get("title", "Untitled Use Case")
        description = str(use_case_config["description"])
        sidebar = use_case_config.get("sidebar", False)
        system_message = use_case_config.get("system_message", None)

        view_function(
            use_case=selected_use_case,
            context=context,
            system_message=system_message or st.session_state.global_settings.get("system_message", ""),
            session_file=session_file_path,
            model_name=st.session_state.selected_model,
            settings=global_settings,
            title=title,
            description=description,
            collection=collections, # Verwende die rollenspezifischen collections
            sidebar=sidebar,
        )

        view_path = str(use_case_config["view"]).replace(".", "/")
        full_path = os.path.join(st.session_state.base_path, view_path.split("/render")[0] + ".py")
        st.session_state.view_path = full_path

    except Exception as e:
        #st.info("⚠️ Dieser Use Case ist in der Light-Version nicht enthalten oder konnte nicht geladen werden.")
        
        title = use_case_config.get("title", "Unbekannter Use Case")
        description = str(use_case_config.get("description", "Keine Beschreibung verfügbar."))
        
        with st.container():
            st.markdown(f"### {title}")
            st.markdown(description)
            st.info("""
            ❌ **Dieser Use Case ist in der Light-Version des CAIR4 Explorers nicht verfügbar.**

            Lies Dir die Use-Case-Beschreibung und die dazugehörige Aufgabe durch, um Dich über die Inhalte des Use Cases zu Informieren.

            👉 Vollständige Use-Case-Inhalte befinden sich vornehmlich im ersten Kapitel: "KI-Basics"!
            """)
