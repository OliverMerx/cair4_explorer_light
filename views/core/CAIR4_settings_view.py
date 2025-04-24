"""
=================================================
CAIR4 Einstellungen (CAIR4_settings_view.py)
=================================================

Dieses Modul verwaltet die globale Konfigurationsansicht und stellt sicher, 
dass alle relevanten Einstellungen gespeichert und geladen werden.

📌 Funktionen:
- `render_settings_view(global_settings)`: Zeigt die Einstellungsansicht mit UI-Elementen an.
- `initialize_global_settings()`: Stellt sicher, dass `global_settings` im Session-State existiert.
- `load_memories() / save_memories() / show_memories()`: Verwalten der Memory-Datenbank.

✅ Warum ist das wichtig?
- Ermöglicht eine einheitliche Anpassung der Konfigurationswerte.
- Stellt sicher, dass gespeicherte Erinnerungen (Memories) erhalten bleiben.
- Verhindert Fehler durch fehlende Session-State-Variablen.

🔧 Verwendung:
    from views.core.CAIR4_settings_view import render_settings_view
    render_settings_view(st.session_state.global_settings)
"""

# === 1️⃣ Importiere erforderliche Bibliotheken ===
from pylibs.streamlit_lib import streamlit as st
from pylibs.random_lib import random

from utils.core.CAIR4_settings_manager import save_global_settings
from utils.core.CAIR4_memory_manager import load_memories, save_memories, show_memories

from streamlit_extras.stylable_container import stylable_container

# === 2️⃣ Speicherpfad für Erinnerungen (Memories) ===
MEMORY_FILE = "CAIR4_data/data/persistent_memories.json"

# === 3️⃣ Sicherstellen, dass `global_settings` existiert ===
def initialize_global_settings():
    """Initialisiert die globalen Einstellungen im Session-State, falls sie nicht existieren."""
    if "global_settings" not in st.session_state:
        st.session_state.global_settings = {
            "temperature": 0.7,
            "top_p": 0.9,
            "response_length": "Mittel",
            "response_format": "Fließtext",
            "system_message": ""  # Standard-Systemnachricht (leer)
        }
        print("[INFO] `global_settings` wurde in st.session_state initialisiert.")

# === 4️⃣ Ansicht für die Einstellungen rendern ===
def render_settings_view(global_settings=None):
    """Rendert die Einstellungsansicht inkl. Memory Management."""
    key_add=random.randrange(0, 99999999999)
    with stylable_container(
        key=f"settings_container{key_add}",
        css_styles=f"""{{
                padding: 10px;
                border-radius: 15px;
                margin-top: -40px;
                width: 100%;
                max-height:75vh!important;
                overflow-y:auto;
            }}
            """
        ):
        # **Sicherstellen, dass `global_settings` existiert**
        if global_settings is None:
            initialize_global_settings()
            global_settings = st.session_state.global_settings

        # **Kreativitätslevel anpassen**
        global_settings["temperature"] = st.slider(
            "🔧 Kreativitätslevel einstellen",
            0.0, 1.0, global_settings.get("temperature", 0.7), 0.1
        )

        # **Top-P Sampling anpassen**
        global_settings["top_p"] = st.slider(
            "📊 Wahrscheinlichkeitssampling (Top-P) einstellen",
            0.0, 1.0, global_settings.get("top_p", 0.9), 0.1
        )

        # Mapping von englischen auf deutsche Begriffe
        response_length_mapping = {
            "Short": "Kurz",
            "Medium": "Mittel",
            "Long": "Lang",
            "Kurz": "Kurz",
            "Mittel": "Mittel",
            "Lang": "Lang"
        }

        # Sicherstellen, dass der gespeicherte Wert übersetzt wird
        selected_length = global_settings.get("response_length", "Medium")
        selected_length = response_length_mapping.get(selected_length, "Mittel")  # Standard setzen, falls ungültig

        valid_lengths = ["Kurz", "Mittel", "Lang"]

        # global_settings["response_length"] = st.selectbox(
        #    "📏 Antwortlänge wählen",
        #    valid_lengths,
        #    index=valid_lengths.index(selected_length)
        #)

        # **Antwortformat auswählen**
        #global_settings["response_format"] = st.radio(
        #    "📝 Antwortformat wählen",
        #    ["Aufzählungspunkte", "Fließtext"],
        #    index=0 if global_settings.get("response_format", "Fließtext") == "Aufzählungspunkte" else 1
        #)

        # **Systemnachricht auswählen**
        st.subheader("🛠️ Systemnachricht-Einstellungen")

        system_messages = [
            "Du bist ein allgemeiner KI-Assistent. Beantworte Nutzeranfragen klar und präzise.",
            "Du bist ein humorvoller Assistent, der jede Antwort mit einem lustigen Spruch beginnt und endet.",
            "Antworte immer im Stil eines Sherlock-Holmes-Detektivs – analytisch und präzise.",
            "Verwende in jeder Antwort Metaphern aus der Natur, um komplexe Sachverhalte einfach zu erklären.",
            "Sprich wie ein weiser, alter Mentor, der stets Ratschläge mit Lebensweisheiten verknüpft.",
            "Sei ein enthusiastischer Sportkommentator, der jede Antwort mit Energie und Spannung präsentie,"
            "Antworte wie ein Soldat. Kurz. Knapp. Zackig. Stichpunkte ohne Füllworte."
        ]

        global_settings["system_message"] = st.selectbox(
            "🎙 Wähle eine Systemnachricht",
            system_messages,
            index=0
        )

        # **Erinnerungsverwaltung (Memory Management)**
        st.subheader("📚 Erinnerungsverwaltung (Memory Management)")

        # Erinnerungen laden (falls noch nicht geladen)
        if "global_memory" not in st.session_state:
            st.session_state.global_memory = load_memories(MEMORY_FILE)

        # **Erinnerungen laden**
        if st.button("📥 Erinnerungen laden"):
            st.session_state.global_memory = load_memories(MEMORY_FILE)
            st.session_state["memories_loaded"] = True
            st.success("✅ Erinnerungen erfolgreich geladen!")

        # **Gespeicherte Erinnerungen anzeigen**
        if st.session_state.get("memories_loaded", False):
            show_memories(MEMORY_FILE)

        # **Neue Erinnerung hinzufügen**
        st.subheader("➕ Neue Erinnerung hinzufügen")
        new_memory_value = st.text_input("📌 Neue Erinnerung eingeben", key="new_memory_input")
        
        if st.button("💾 Neue Erinnerung speichern"):
            if new_memory_value.strip():
                st.session_state["global_memory"].append({"session": "sessionID", "memory": new_memory_value.strip()})
                save_memories(st.session_state["global_memory"], MEMORY_FILE)
                st.success("✅ Neue Erinnerung erfolgreich gespeichert!")
                st.rerun()

        # **Alle Erinnerungen löschen**
        if st.button("🗑️ Alle Erinnerungen löschen"):
            st.session_state["global_memory"] = []
            save_memories([], MEMORY_FILE)
            st.success("🗑️ Alle Erinnerungen wurden gelöscht.")
            st.rerun()

        # **Einstellungen speichern**
        if st.button("💾 Globale Einstellungen speichern"):
            save_global_settings(global_settings)
            st.success("✅ Globale Einstellungen erfolgreich gespeichert!")
            print("[INFO] Globale Einstellungen gespeichert.")