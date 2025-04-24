"""
==========================
💡 CAIR4 Session Manager
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

# 🛠 3rd Party Libraries
from pylibs.os_lib import os
from pylibs.json_lib import json
from pylibs.uuid_lib import uuid
from pylibs.streamlit_lib import streamlit as st

# 📌 CAIR4 Utilities
from utils.core.CAIR4_log_manager import handle_session_action
from utils.core.CAIR4_metrics_manager import initialize_metrics  # Importiere die Metrik-Initialisierung

def load_sessions(session_file):
    """
    Lädt die gespeicherten Sitzungen aus der Datei und ergänzt fehlende UUIDs und Metriken.

    ✅ Ablauf:
    - Falls die Datei fehlt, wird eine **neue leere Datei** erstellt.
    - Falls Sessions geladen werden, prüft das System auf fehlende **UUIDs & Metriken**.
    - Falls das Dateiformat fehlerhaft ist, wird es **automatisch zurückgesetzt**.

    Args:
        session_file (str): Pfad zur Datei mit gespeicherten Sitzungen.

    Returns:
        list: Eine Liste der geladenen Sitzungen.
    """

    try:
        use_case=st.session_state.active_view
    except:
        use_case="N/A"

    try:
        session_id=st.session_state.session_id
    except:
        session_id=0

    if not os.path.exists(session_file):
        print(f"[WARNING] Session-Datei nicht gefunden: {session_file}. Erstelle neue Datei.")
        os.makedirs(os.path.dirname(session_file), exist_ok=True)
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump([], f)  # Leere Datei initialisieren
        handle_session_action("Session File Created", {"file": session_file}, use_case, session_id)
        return []  # Keine vorhandenen Sitzungen

    # Datei existiert – Versuche, sie zu laden

    try:
        with open(session_file, "r", encoding="utf-8") as f:
            sessions = json.load(f)

        # Ergänze fehlende UUIDs und Metriken
        for session in sessions:
            if "session_id" not in session:
                st.session_state.session_id=str(uuid.uuid4())
                session["session_id"] = st.session_state.session_id
                print(f"[WARNING] Fehlende Session-ID hinzugefügt: {session['session_id']}")
            if "metrics" not in session:
                session["metrics"] = initialize_metrics()  # Initialisiere Metriken
                print(f"[WARNING] Fehlende Metriken für Session {session['session_id']} hinzugefügt.")

        handle_session_action("Loaded Sessions", {"file": session_file, "count": len(sessions)}, use_case, session_id)
        return sessions

    except json.JSONDecodeError:
        print(f"[WARNING] Ungültiges Format der Session-Datei: {session_file}. Setze Datei zurück...")
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump([], f)  # Leere Datei initialisieren
        handle_session_action("Session File Invalid", {"file": session_file}, use_case, session_id)
        return []

def save_sessions(session_file, sessions):
    """
    Speichert die aktuelle Liste der Sitzungen in die Datei und erstellt relevante Log-Einträge.

    ✅ Ablauf:
    - Falls das Speicherverzeichnis fehlt, wird es **automatisch erstellt**.
    - Falls das Speichern erfolgreich ist, wird eine **Bestätigung** ausgegeben.
    - Falls ein Fehler auftritt, wird eine **Fehlermeldung** generiert.

    Args:
        session_file (str): Pfad zur Datei mit gespeicherten Sitzungen.
        sessions (list): Liste der zu speichernden Sitzungen.
    """

    try:
        use_case=st.session_state.active_view
    except:
        use_case="N/A"

    try:
        session_id=st.session_state.session_id
    except:
        session_id=0

    try:
        directory = os.path.dirname(session_file)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"[INFO] Verzeichnis erstellt: {directory}")
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(sessions, f, indent=4)
        print(f"[INFO] {len(sessions)} Sitzungen erfolgreich gespeichert in {session_file}.")
        handle_session_action("Saved Sessions", {"file": session_file, "count": len(sessions)}, use_case, session_id)
    except Exception as e:
        print(f"[ERROR] Fehler beim Speichern der Sitzungen: {e}")
        handle_session_action("Save Sessions Failed", {"file": session_file, "error": str(e)}, use_case, session_id)

def append_session(session, role, content):
    """
    Fügt eine neue Nachricht zur aktuellen Session hinzu.

    ✅ Ablauf:
    - Falls das Nachrichten-Feld fehlt, wird es **erstellt**.
    - Speichert die Nachricht mit **Rolle und Inhalt**.

    Args:
        session (dict): Die aktuelle Session mit Nachrichten.
        role (str): Rolle der Nachricht (z.B. "user" oder "assistant").
        content (str): Inhalt der Nachricht.
    """
    if "messages" not in session:
        session["messages"] = []

    session["messages"].append({"role": role, "content": content})