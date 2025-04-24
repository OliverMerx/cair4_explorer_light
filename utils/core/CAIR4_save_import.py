"""
===============================================
CAIR4 Save Import
===============================================

Beim Start komplexer Streamlit-Anwendungen wie CAIR4 mit mehrfachen oder verschachtelten imports
kann es aufgrund der initialen Ladezeit zu Fehlern kommen. Diese Datei verhindert beim Start, dass wichtige Module fehlerhaft geladen werden
bzw. dass sie erst geladen werden, nachdem das vorherige Modul erfolgreich geladen wurde.

Das Modul führt einen robusten Import eines Moduls + Attributs (Funktion/Klasse) durch.
Beispiel: safe_import("core.CAIR4_init_main", "main")

"""

from pylibs.streamlit_lib import streamlit as st
from pylibs.importlib_lib import importlib, initialize_importlib
from pylibs.time_lib import time
from streamlit_extras.stylable_container import stylable_container

initialize_importlib()

MAX_RETRIES = 3
RETRY_DELAY = 0.2  # Sekunden

def show_centered_spinner(message="Initialisierung ..."):
    spinner_placeholder = st.empty()
    spinner_html = f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 70vh;">
            <div>
                <div class="spinner" style="margin: auto; width: 60px; height: 60px; border: 8px solid #f3f3f3; border-top: 8px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                <p style="text-align: center; margin-top: 20px;">{message}</p>
            </div>
        </div>
        <style>
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
    """
    spinner_placeholder.markdown(spinner_html, unsafe_allow_html=True)
    
    return spinner_placeholder

def safe_import(module_str: str, attribute_str: str):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            module = importlib.import_module(module_str)
            return getattr(module, attribute_str)
        except (ModuleNotFoundError, AttributeError) as e:
            if attempt < MAX_RETRIES:
                print(f"[WARN] Import von {module_str}.{attribute_str} fehlgeschlagen (Versuch {attempt}) – warte {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"[ERROR] Konnte {module_str}.{attribute_str} nicht laden:\n{e}")
                st.error(f"❌ Fehler beim Laden von `{module_str}.{attribute_str}`. Bitte prüfen, ob Modul & Funktion verfügbar sind.")
                st.stop()