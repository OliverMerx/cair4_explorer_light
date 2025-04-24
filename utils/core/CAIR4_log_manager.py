"""
=================================================
📜 CAIR4 Log Manager (CAIR4_log_manager.py)
=================================================

📌 **Beschreibung:**
Dieses Modul verwaltet Logs für das System. Es ermöglicht:
- **Laden & Speichern von Logs**
- **Erfassen von Session-Aktionen**
- **Detaillierte Fehler- und Crash-Protokollierung**
- **Regulatorische Transparenz durch vollständige Protokollierung**

✅ **Hauptfunktionen:**
- `load_logs(log_file)`: Lädt Logs aus einer Datei.
- `save_logs(log_file, logs)`: Speichert Logs in einer Datei.
- `ensure_log_file_exists(log_file)`: Stellt sicher, dass die Log-Datei existiert.
- `add_log_entry(log_file, entry)`: Fügt einen neuen Log-Eintrag hinzu.
- `handle_session_action(action, details, use_case, session_id)`: Erstellt einen Log-Eintrag für eine Session-Aktion.
- `log_crash(use_case, session_id, error_message)`: Speichert einen Crash in den Logs.
"""

# === 1️⃣ 📦 Import externer Bibliotheken ===
from pylibs.streamlit_lib import streamlit as st
from pylibs.os_lib import os
from pylibs.json_lib import json
from pylibs.datetime_lib import initialize_datetime

# Initialisiere `datetime`
datetime = initialize_datetime()

# Standard-Logdatei
LOG_FILE = "CAIR4_data/logs/logs.json"

# === 2️⃣ 📂 Log-Management Funktionen ===

def load_logs(log_file):
    """Lädt Logs aus einer Datei oder erstellt ein leeres Dictionary."""
    if not os.path.exists(log_file):
        return {"entries": [], "steps": []}
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)
            return logs if isinstance(logs, dict) else {"entries": [], "steps": []}
    except json.JSONDecodeError:
        return {"entries": [], "steps": []}


def save_logs(log_file, logs):
    """Speichert Logs in eine Datei."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)


def ensure_log_file_exists(log_file, session_id):
    """Stellt sicher, dass die Log-Datei existiert."""
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump({"entries": [], "steps": []}, f)


# === 3️⃣ 📝 Einheitliche Log-Funktionen ===

def add_log_entry(log_file, entry):
    """Fügt einen neuen Log-Eintrag hinzu und speichert ihn."""
    logs = load_logs(log_file)
    logs.setdefault("entries", []).append(entry)
    save_logs(log_file, logs)


def handle_session_action(action, details=None, use_case="Unknown", session_id=None):
    """
    Erstellt einen Log-Eintrag für eine Session-Aktion.

    ✅ Änderungen:
    - `session_id` wird immer sicher aus `st.session_state` geholt, falls nicht übergeben.
    - `use_case` und `session_id` sind jetzt klar getrennt.
    - Falls `current_session` nicht existiert, wird ein Platzhalter verwendet.

    Args:
        action (str): Die durchgeführte Aktion.
        details (dict, optional): Weitere Details zur Aktion.
        use_case (str, optional): Der Anwendungsfall (Use Case).
        session_id (str, optional): Die Session-ID.
    """
    
    # **Session-ID sicherstellen**
    if session_id is None:
        session_id = (
            st.session_state["current_session"]["session_id"]
            if "current_session" in st.session_state and "session_id" in st.session_state["current_session"]
            else "N/A"
        )

    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "use_case": use_case,
        "session_id": session_id,
        "action": action,
        "details": details if details else {"info": "No details provided"}
    }
    
    # **Log-Eintrag speichern**
    if(use_case is not "unknown"):
        add_log_entry(LOG_FILE, log_entry)


# === 4️⃣ ❌ Crash-Protokollierung ===

def log_crash(use_case, session_id, error_message):
    """
    Speichert einen Crash in die Logs.

    ✅ Änderungen:
    - `session_id` wird sicher übergeben oder aus `st.session_state` geholt.
    - Fehlerdetails werden vollständig protokolliert.

    Args:
        use_case (str): Der aktuelle Anwendungsfall.
        session_id (str): Die Session-ID.
        error_message (Exception | str): Die Fehlermeldung.
    """

    if session_id is None:
        session_id = (
            st.session_state["current_session"]["session_id"]
            if "current_session" in st.session_state and "session_id" in st.session_state["current_session"]
            else "N/A"
        )

    crash_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "use_case": use_case,
        "session_id": session_id,
        "action": "Crash",
        "details": {
            "error_type": type(error_message).__name__,
            "full_trace": repr(error_message)
        },
    }
    
    # **Log-Eintrag speichern**
    add_log_entry(LOG_FILE, crash_entry)

def add_detailed_log(log_file, step):
    """
    Fügt einen detaillierten Schritt zu den Logs hinzu.

    Args:
        log_file (str): Pfad zur Logdatei.
        step (dict): Detaillierter Schritt.
    """
    logs = load_logs(log_file)
    logs.setdefault("steps", []).append(step)
    save_logs(log_file, logs)
    print(f"[DEBUG] Added detailed log step: {step}")

def inventory_libraries(py_lib_path):
    """
    Inventarisiert Libraries im angegebenen Verzeichnis.

    Args:
        py_lib_path (str): Pfad zum Verzeichnis der Libraries.

    Returns:
        dict: Ein Dictionary mit Informationen zu den Libraries.
    """
    inventory = {}
    if not os.path.exists(py_lib_path):
        print(f"[WARNING] Library path not found: {py_lib_path}")
        return inventory

    for file in os.listdir(py_lib_path):
        if file.endswith("_lib.py"):
            try:
                module_name = file[:-3]
                inventory[module_name] = {"version": "1.0.0", "license": "MIT"}
            except Exception as e:
                print(f"[ERROR] Failed to process library {file}: {e}")
                inventory[file] = {"error": str(e)}
    print(f"[INFO] Library inventory completed: {inventory}")
    return inventory