"""
==========================
💡 CAIR4 Session Initializer
==========================

📌 **Funktion:**  
Stellt sicher, dass alle **wichtigen Variablen** korrekt gesetzt werden, 
bevor die App startet.

✅ **Hauptfunktionen:**
- **initialize_session_state()** → Erstellt oder lädt eine **bestehende Session**.
- **ensure_session_file_exists()** → Stellt sicher, dass die Datei für gespeicherte Sessions existiert.
- **Session bleibt stabil:** `session_id` wird NICHT bei jeder Interaktion überschrieben.
"""

# === 1️⃣ Importiere erforderliche Bibliotheken ===
from pylibs.os_lib import os
from pylibs.uuid_lib import uuid
from pylibs.json_lib import json
from pylibs.streamlit_lib import streamlit as st
from datetime import datetime, timezone

# === 2️⃣ Interne Module ===
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_debug_utils import DebugUtils


def initialize_session_state(global_settings, session_file="CAIR4_data/data/chat_sessions.json"):
    """
    📌 **Initialisiert die Streamlit-Session und sorgt für stabile `session_id`.**

    - Erstellt eine **neue Session**, falls keine existiert.
    - Lädt eine **bestehende Session**, falls verfügbar.
    - Stellt sicher, dass `session_id` stabil bleibt.

    **Args:**
        - `global_settings` (dict): Globale Einstellungen der App.
        - `session_file` (str, optional): Dateipfad für gespeicherte Sessions. Default: `"CAIR4_data/data/chat_sessions.json"`
    """

    # **🛠️ 1. UI Status-Flags initialisieren**
    ui_flags = ["settings_open", "metrics_open", "upload_open", "logs_open"]
    for flag in ui_flags:
        if flag not in st.session_state:
            st.session_state[flag] = False

    # **📌 2. Globale Einstellungen initialisieren**
    if "global_settings" not in st.session_state:
        st.session_state.global_settings = global_settings.copy()
        DebugUtils.debug_print("[INFO] Global settings initialized in session state.")

    # **🗂️ 3. Sicherstellen, dass Session-Datei existiert**
    ensure_session_file_exists(session_file)

    # **🔄 4. Existierende Session laden oder neue erstellen**
    if "current_session" not in st.session_state:
        sessions = load_sessions(session_file)

        if sessions:
            # **📌 Lade letzte gespeicherte Session**
            st.session_state["current_session"] = sessions[-1]
            DebugUtils.debug_print(f"[INFO] Geladene Session: {st.session_state['current_session']['session_id']}")
        else:
            # **📌 Erstelle neue Session**
            st.session_state.session_id = str(uuid.uuid4())
            new_session_id = st.session_state.session_id
            st.session_state["current_session"] = {
                "session_id": new_session_id,
                "start_time": datetime.now(timezone.utc).isoformat(),
                "model": global_settings.get("default_model", "gpt-4"),
                "messages": [],
                "metrics": {
                    "total_tokens": 0,
                    "total_costs": 0.0,
                    "requests": 0,
                    "calculation_steps": 0,
                    "ai_queries": 0
                }
            }

            # **📌 Speichere neue Session**
            save_sessions(session_file, [st.session_state["current_session"]])
            DebugUtils.debug_print(f"[INFO] Neue Session erstellt: {new_session_id}")


def ensure_session_file_exists(session_file):
    """
    📂 **Stellt sicher, dass die Session-Datei existiert und gültig ist.**

    Falls die Datei **nicht existiert** oder ungültig ist, wird sie mit einem **leeren Array** neu erstellt.

    **Args:**
        - `session_file` (str): Pfad zur Session-Datei.
    """

    if not os.path.exists(session_file):
        DebugUtils.debug_print(f"[DEBUG] Session file not found: {session_file}. Creating an empty session file.")
        os.makedirs(os.path.dirname(session_file), exist_ok=True)
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump([], f)
    else:
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("Session file does not contain a valid JSON list.")
        except (json.JSONDecodeError, ValueError):
            DebugUtils.debug_print(f"[WARNING] Session file is invalid or empty. Reinitializing: {session_file}")
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump([], f)