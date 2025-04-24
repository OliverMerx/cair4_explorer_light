"""
=======================================================
CAIR4 Sidebar Update System (CAIR4_update_sidebar.py)
=======================================================

Dieses Modul verwaltet die Sidebar für gespeicherte Sitzungen 
innerhalb der CAIR4-Plattform. Es ermöglicht das Laden, Speichern, Zurücksetzen 
und Löschen von Sitzungen über interaktive Steuerelemente. Zudem werden bestimmte
Funktionen Use Case individuell gestaltet (Sessionstracking hat z.B. nicht jeder Use Case).

📌 Funktionen:
- **update_sidebar()** → Erstellt ein Dropdown-Menü zur Auswahl gespeicherter Sessions.
- **Buttons für Session-Steuerung**:
  - 📝 **Neue Session starten** → Speichert aktuelle, startet eine neue, leert das Eingabefeld.
  - 🔄 **Session zurücksetzen** → Löscht Nachrichten (Bestätigungsdialog), Eingabefeld leer.
  - 🗑️ **Alle Sessions löschen** → Entfernt alle Sessions (Bestätigungsdialog), Eingabefeld leer.

✅ Warum ist das wichtig?
- Erlaubt eine effiziente Navigation zwischen Sessions.
- Unterstützt Nutzer bei der Verwaltung von Sitzungshistorien.
- Ermöglicht Debugging und Wiederherstellung alter Sessions.
"""

# === 1️⃣  Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st

# === 2️⃣  Import interner Module ===
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_debug_utils import DebugUtils  # Debug-Klasse für Log-Ausgaben
from utils.core.CAIR4_stylable_button import stylable_button_light


def update_sidebar(use_case, session_file):
    """
    Aktualisiert die Sidebar für einen spezifischen Use Case, 
    indem gespeicherte Sessions verwaltet und interaktive Buttons bereitgestellt werden.

    Args:
        use_case (str): Der Name des aktuellen Use Cases.
        session_file (str): Dateipfad zur Speicherung der Session-Daten.

    Ablauf:
    - Läd gespeicherte Sessions und zeigt sie in einem Dropdown an.
    - Ermöglicht das Speichern, Zurücksetzen und Löschen von Sessions.
    """

    DebugUtils.debug_print(f"update_sidebar aufgerufen für Use Case: {use_case}")

    # **Sessions laden**
    sessions = load_sessions(session_file)

    # **Dropdown-Optionen erstellen**
    session_labels = [
        f"Session {i + 1}: {sess['messages'][0]['content'][:30]}..."
        for i, sess in enumerate(sessions) if sess["messages"]
    ]

    # **Session-State für Bestätigungsdialoge initialisieren**
    st.session_state.setdefault("confirm_reset", False)
    st.session_state.setdefault("confirm_delete", False)
    
    with st.expander("💬 Sessions", expanded=True):
    # **Buttons zur Steuerung der Sessions**
    
        col1, col2 = st.columns([1, 3])

        # **📝 Neue Session starten (Speichert aktuelle, leert Eingabe)**
        with col1:
            help1="Neue Session starten"
            btn1=stylable_button_light("📝", "#fff", "#fff", "#ccc", f"{use_case}_new_session", False)
            if btn1:
                if st.session_state["current_session"]["messages"]:
                    sessions.append(st.session_state["current_session"].copy())  # 🛠 Fix: Kopie speichern!
                    save_sessions(session_file, sessions)
                    DebugUtils.debug_print("Neue Session gestartet und gespeichert")

                # **Neue leere Session initialisieren**
                st.session_state["current_session"] = {
                    "messages": [],
                    "metrics": {
                        "total_tokens": 0,
                        "total_costs": 0.0,
                        "tokens_used_per_request": [],
                        "costs_per_request": [],
                        "request_names": [],
                    },
                }

                # **Eingabefeld leeren**
                st.session_state["user_input"] = ""
                st.rerun()

        # **🔄 Aktuelle Session zurücksetzen (Bestätigungsdialog)**
        with col2:
            st.write(help1)

        col1, col2 = st.columns([1, 3])
        help2="Session zurücksetzen", 
        # **Session zurücksetzen)**
        with col1:
            help2="Session zurücksetzen"
            btn2=stylable_button_light("🔄", "#fff", "#fff","#ccc", f"{use_case}_reset_session", False)
            if btn2:
                st.session_state["confirm_reset"] = True

            if st.session_state["confirm_reset"]:
                st.warning("⚠️ Wirklich diese Session zurücksetzen?")
                col_confirm1, col_confirm2 = st.columns([1, 1])
                with col_confirm1:
                    if st.button("Ja, zurücksetzen"):
                        st.session_state["current_session"] = {
                            "messages": [],
                            "metrics": {
                                "total_tokens": 0,
                                "total_costs": 0.0,
                                "tokens_used_per_request": [],
                                "costs_per_request": [],
                                "request_names": [],
                            },
                        }
                        st.session_state["user_input"] = ""  # Eingabefeld leeren
                        st.session_state["confirm_reset"] = False
                        st.rerun()
                with col_confirm2:
                    if st.button("Nein, abbrechen"):
                        st.session_state["confirm_reset"] = False
        with col2:
            st.write(help2)
        # **🗑️ Alle Sessions löschen (Bestätigungsdialog)**
        col1, col2 = st.columns([1, 3])
        help3="Alle Sessions löschen"
        # **löscht alle Sessions**
        with col1:
            btn3=stylable_button_light("🗑️", "#fff", "#fff", "ccc", f"{use_case}_delete_session", True)
            if btn3:
                st.session_state["confirm_delete"] = True

        if st.session_state["confirm_delete"]:
            st.warning("⚠️ Wirklich alle gespeicherten Sessions löschen?")
            col_confirm1, col_confirm2 = st.columns([1, 1])
            with col_confirm1:
                if st.button("Ja, alle löschen"):
                    if os.path.exists(session_file):
                        os.remove(session_file)
                    st.session_state["thread_sessions"][use_case] = []  # 🛠 Fix: Schlüssel anpassen!
                    st.session_state["user_input"] = ""  # Eingabefeld leeren
                    st.session_state["confirm_delete"] = False
                    DebugUtils.debug_print("Alle Sessions gelöscht")
                    st.rerun()
            with col_confirm2:
                if st.button("Nein, abbrechen"):
                    st.session_state["confirm_delete"] = False
        with col2:
            st.write(help3)