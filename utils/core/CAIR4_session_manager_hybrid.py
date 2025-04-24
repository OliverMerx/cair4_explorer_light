"""
==========================
💡 CAIR4 Session Manager
==========================
Dieses Modul verwaltet die Speicherung und das Laden von Benutzersitzungen innerhalb der CAIR4-Plattform. 
Es stellt sicher, dass alle Sessions in einem einheitlichen Format gespeichert werden.

📌 Funktionen:
- **load_sessions()** → Lädt gespeicherte Sitzungen aus der Datei.
- **save_sessions()** → Speichert aktuelle Sitzungen und aktualisiert Metriken.
- **append_session()** → Fügt eine neue Nachricht oder Berechnung hinzu.
- **get_current_session()** → Gibt die aktuelle Session zurück.

✅ Vorteile:
- Unterstützt **alle Use Cases (Finance, Medical, HR, Kommunikation, Chat, Berechnungen)**.
- **Modular & resilient** – Kein Datenverlust mehr bei Abstürzen.
- **Metriken werden in Echtzeit aktualisiert**.
"""

# 🛠 3rd Party Libraries
from pylibs.streamlit_lib import streamlit as st
from pylibs.os_lib import os
from pylibs.json_lib import json
from pylibs.uuid_lib import uuid
import datetime

# 📌 CAIR4 Utilities
from utils.core.CAIR4_log_manager import handle_session_action
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_metrics_manager import initialize_metrics  # Importiere die Metrik-Initialisierung
from utils.core.CAIR4_debug_utils import DebugUtils 

# === 3️⃣ ➕ Nachricht oder Berechnung hinzufügen ===
def append_session(session, role, content, tokens_used=0, cost=0.0):
    """
    📌 **Erweitertes Session-Handling für hybride Modelle**
    
    ✅ **Unterstützte Session-Typen:**
    - **Regelbasierte Berechnungen (`calculation`)** → Finanz- oder medizinische Scores.
    - **KI-gestützte Anfragen (`query`)** → GPT-4, BioBERT etc.
    - **Hybride Modelle (`hybrid`)** → Kombination aus Regelbasiertem Modell & KI-Optimierung.

    🔹 **Parameter:**
    - `session (dict)`: **Die aktuelle Session mit Nachrichten.**
    - `role (str)`: `"user"`, `"assistant"`, `"calculation"`, `"query"`, `"hybrid"`.
    - `content (str | dict)`: **Inhalt der Nachricht oder Berechnung.**
    - `tokens_used (int)`: **Genutzte Tokens bei KI-Abfragen.**
    - `cost (float)`: **Kosten der Berechnung in Währung (z.B. USD).**
    """
    
    DebugUtils.debug_print(f"Anhang für Sessions: {session}.")
    
    if "messages" not in session:
        session["messages"] = []

    # **📌 Sicherstellen, dass alle Metriken vorhanden sind**
    if "metrics" not in session or not isinstance(session["metrics"], dict):
        session["metrics"] = initialize_metrics()
       
    # **📌 Nachricht/Berechnung hinzufügen**
    session["messages"].append({
        "role": "ROLE"+role,
        "content": content,
        "tokens": tokens_used,
        "cost": cost,
        "timestamp": datetime.datetime.now().isoformat()
    })

    # **📌 Metriken aktualisieren (nur für KI & hybride Modelle)**
    if role in ["query", "hybrid"]:
        session["metrics"]["total_tokens"] += tokens_used
        session["metrics"]["total_costs"] += cost

        # Falls `tokens_used_per_request` oder `costs_per_request` fehlen, initialisieren
        session["metrics"].setdefault("tokens_used_per_request", []).append(tokens_used)
        session["metrics"].setdefault("costs_per_request", []).append(cost)

    # **📌 Session speichern**
    save_sessions("your_session_file.json", [session])


# === 4️⃣ 📌 Aktuelle Session abrufen ===
def get_current_session(use_case, session_file):
    """
    Gibt die aktuelle Session zurück oder erstellt eine neue.

    ✅ Änderungen:
    - Falls eine Session bereits existiert, wird sie geladen.
    - Falls keine Session existiert, wird eine neue mit `session_id` erstellt.

    Args:
        use_case (str): Der aktuelle Use Case.
        session_file (str): Die Datei, in der Sitzungen gespeichert sind.

    Returns:
        dict: Die aktuelle Session.
    """
    if "current_session" in st.session_state:
        return st.session_state["current_session"]

    sessions = load_sessions(session_file)
    st.session_state.session_id = str(uuid.uuid4())
    new_session = {
        "session_id": st.session_state.session_id,
        "messages": [],
        "metrics": initialize_metrics()
    }
    st.session_state["current_session"] = new_session
    sessions.append(new_session)
    save_sessions(session_file, sessions)
    return new_session

