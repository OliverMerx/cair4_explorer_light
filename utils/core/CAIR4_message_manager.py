"""
=================================================
CAIR4 Session Manager (CAIR4_message_manager.py)
=================================================

Dieses Modul verwaltet die Sitzungen (Sessions) von Querys im CAIR4-System.

Funktionen:
- `initialize_current_session()`: Erstellt eine neue Session mit Nachrichten & Metriken.
- `append_message(session, role, content)`: Fügt eine Nachricht zur Session hinzu.

Verwendung:
    from utils.core.CAIR4_session_manager import initialize_current_session, append_message

    session = initialize_current_session()
    append_message(session, "user", "Hello AI!")
"""

# === 1️⃣ Import externer Module ===
from utils.core.CAIR4_metrics_manager import initialize_metrics
from utils.core.CAIR4_debug_utils import DebugUtils 


# === 2️⃣ Session-Handling ===
def initialize_current_session():
    """Initialisiert eine neue Session mit Nachrichten und Metriken."""
    
    DebugUtils.debug_print(f"Initialisierung von Session erfolgt.")
    
    return {
        "messages": [],  # Liste zur Speicherung der Konversation
        "metrics": initialize_metrics()  # Initialisiere Metriken
    }

def append_message(session, role, content):
    """Fügt eine Nachricht zur aktuellen Session hinzu, ohne bestehende Daten zu überschreiben.

    Args:
        session (dict): Die aktuelle Sitzung.
        role (str): Die Rolle des Absenders (z. B. "user" oder "assistant").
        content (str): Die Nachricht.
    """

    # **📌 Sicherstellen, dass `messages` existiert**
    if "messages" not in session:
        session["messages"] = []

    # **📌 Nachricht hinzufügen**
    session["messages"].append({"role": role, "content": content})

    # **📌 Debugging: Anzeigen der gesamten Session nach jeder Änderung**
    DebugUtils.debug_print(f"📌 Nachricht hinzugefügt: {session}")