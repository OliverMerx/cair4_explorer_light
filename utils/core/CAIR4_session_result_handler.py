
"""
==========================
💡 CAIR4 Session Result Manager
==========================
Dieses Modul verwaltet die Speicherung und das Laden von Benutzersitzungen innerhalb der CAIR4-Plattform. 
Es stellt sicher, dass Sitzungen mit einer eindeutigen UUID gespeichert werden und dass Metriken korrekt 
initialisiert sind. Falls eine Session-Datei fehlt oder fehlerhaft ist, wird sie automatisch neu erstellt.

📌 Funktionen:
- **load_sessions()** → Lädt gespeicherte Sitzungen aus der Datei, ergänzt fehlende UUIDs und Metriken.
- **save_sessions()** → Speichert aktuelle Sitzungen und erstellt Log-Einträge für die Nachverfolgbarkeit.
- **append_message()** → Fügt einer Session eine Nachricht hinzu, um Konversationen zu speichern.

✅ Warum ist das wichtig?
- Verhindert **Datenverlust** durch fehlerhafte oder fehlende Session-Dateien.
- Stellt sicher, dass jede Session eine **eindeutige Identifikation (UUID)** besitzt.
- Ermöglicht eine **metrische Analyse** jeder Sitzung durch die Initialisierung von Kennzahlen.
"""

# === 1️⃣ Importiere erforderliche Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json
from pylibs.uuid_lib import uuid
from pylibs.datetime_lib import initialize_datetime

datetime = initialize_datetime()

from utils.core.CAIR4_session_manager import load_sessions, save_sessions

# === 2️⃣ Importiere interne Module ===
#from utils.core.CAIR4_session_manager import load_sessions, save_sessions

# === 3️⃣ Generische Session-Manager-Funktion ===
def manage_session(use_case, session_file):
    """
    📌 Generische Session-Manager-Funktion, die Sitzungen initialisiert,
    speichert und verwaltet – unabhängig von der Business-Logik.

    Args:
        use_case (str): Der Name des aktuellen Anwendungsfalls.
        session_file (str): Der Dateipfad für gespeicherte Sessions.

    Returns:
        dict: Die aktuelle Session aus `st.session_state`
    """

    # **📂 Sitzungen laden**
    sessions = load_sessions(session_file)
    if not isinstance(sessions, list):
        sessions = []

    st.session_state.setdefault("use_case_sessions", sessions)

    # **🔄 Falls keine aktive Session existiert oder `session_id` fehlt, initialisieren**
    if "current_session" not in st.session_state or "session_id" not in st.session_state["current_session"]:
        new_session_id = str(uuid.uuid4())
        st.session_state["current_session"] = {
            "session_id": new_session_id,  
            "messages": [],  
        }

    return st.session_state["current_session"]

# === 4️⃣ Generische Speichermethode für Berechnungen ===
def store_calculation_result(parameters, session_file):
    """
    📌 Speichert eine beliebige Berechnung als `calculation` in die aktuelle Session.

    Args:
        parameters (dict): Die Berechnungsparameter (z. B. Kreditwerte, Gesundheitsdaten).
        session_file (str): Der Dateipfad für gespeicherte Sessions.
    """

    # **📌 1️⃣ Erstelle die Nachricht für die Berechnung**
    message = {
        "role": "calculation",
        "content": {
            "parameters": parameters,
            "timestamp": datetime.datetime.now().isoformat()
        }
    }

    # **📌 2️⃣ Sicherstellen, dass `messages` existiert**
    if "messages" not in st.session_state["current_session"]:
        st.session_state["current_session"]["messages"] = []

    # **📌 3️⃣ Berechnung zur Session hinzufügen**
    st.session_state["current_session"]["messages"].append(message)

    # **📌 4️⃣ EXISTIERENDE SESSION AKTUALISIEREN**
    session_id = st.session_state["current_session"]["session_id"]
    updated = False

    for i, session in enumerate(st.session_state["use_case_sessions"]):
        if "session_id" in session and session["session_id"] == session_id:
            st.session_state["use_case_sessions"][i] = st.session_state["current_session"]
            updated = True
            break

    # Falls die Session nicht existiert, füge sie neu hinzu
    if not updated:
        st.session_state["use_case_sessions"].append(st.session_state["current_session"])

    # **📌 5️⃣ Session speichern**
    save_sessions(session_file, st.session_state["use_case_sessions"])
