"""
=======================================
💡 CAIR4 Persistent Memory Chat View
=======================================
Dieses Modul verwaltet die Speicherung und Darstellung von Erinnerungen ("Memories") 
und Sitzungshistorien für verschiedene Anwendungsfälle in der CAIR4-Plattform.
Eine neue Chat-Session kann sich an Inhalte einer älteren Chat-Session erinnern.
Dabei wird unterschieden zwischen Erinnerungen aus persönlcihen Memories, die der User selbst einträgt, 
und Erinnerungen aus den gespeicherten Inhalten von älteren Sessions.
User können auswählen, ob beides kumulativ berücksichtigt werden soll oder nur alternativ.

Im modernen digitalen Umfeld ist die Fähigkeit, Erinnerungen und Nutzerdaten über mehrere Sessions hinweg zu speichern, ein entscheidender Erfolgsfaktor. 
Der CAIR4-Use Case „Speichern von Erinnerungen über Sessions hinweg“ bietet genau diese Möglichkeit. Er eignet sich ideal für personalisierte Anwendungen, bei denen die Benutzererfahrung durch kontextbasiertes Wissen und fortlaufende Interaktionen optimiert wird.

🎯 Anwendungsfälle:
	•	Personalisierte Assistenten: Systeme können sich an frühere Interaktionen erinnern und nahtlos an Gespräche anknüpfen.
	•	Langfristige Nutzerprofile: Informationen werden nicht nur temporär, sondern dauerhaft gespeichert, um personalisierte Empfehlungen zu ermöglichen.
	•	Unterbrechungsfreie Workflows: Selbst nach einer Abmeldung oder einer längeren Pause bleibt der Kontext erhalten.

🚀 Funktionen im Überblick:
	1.	Kombinierte Speicherung: Nutzt sowohl Memories als auch Sessions, um den größtmöglichen Kontext zu gewährleisten.
	2.	Nur Memories: Speichert ausschließlich dauerhafte Erinnerungen und verzichtet auf temporäre Sitzungsdaten.
	3.	Nur Sessions: Beschränkt sich auf temporäre Daten, die beim Schließen der Anwendung zurückgesetzt werden.

💡 Vorteile:
	•	Optimierte Benutzerführung: Nutzer müssen sich nicht wiederholen – das System merkt sich wichtige Informationen.
	•	Effizienzsteigerung: Reduziert Redundanzen und fördert eine intelligente Interaktion.
	•	Flexibilität: Wähle die passende Speicherstrategie je nach Anwendungsfall.


📌 Funktionen:
- **generate_combined_memory()** → Kombiniert persistente Memories und Session-Daten.
- **render_persistent_memory_chat_view()** → Stellt die Memory-Ansicht bereit, inkl. Steueroptionen.
- **render_memory_list()** → Zeigt gespeicherte Memories mit Bearbeitungs- und Löschoptionen.

✅ Warum ist das wichtig?
- Erlaubt eine gezielte Kombination aus Memories und Sitzungshistorien.
- Erleichtert dem Nutzer die Kontrolle über den Konversationskontext.
- Unterstützt eine verbesserte Antwortqualität durch optimierte Kontextsteuerung.
"""

# Required Libraries
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json
from pylibs.uuid_lib import uuid

# Manager
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_update_sidebar import update_sidebar
from utils.core.CAIR4_memory_manager import load_memories, save_memories

# Controller
from controllers.CAIR4_controller import handle_query

# Memory File Path
PERSISTENT_MEMORY_FILE = "CAIR4_data/data/persistent_memories.json"

def generate_combined_memory(use_case, memory_mode):
    """
    Generiert die Memory-Zusammenfassung basierend auf der Auswahl der Memory-Quelle.
    """
    combined_memory = {"user": "", "assistant": ""}
    
    # **Persistente Memories (falls gewählt)**
    if memory_mode in ["Kombiniert", "Nur Memories"]:
        persistent_memories = load_memories(PERSISTENT_MEMORY_FILE)
        for memory in persistent_memories:
            content = memory.get("memory", "").strip()
            if content and content not in combined_memory["user"]:
                combined_memory["user"] += f" {content}"

    # **Session-Daten (falls gewählt)**
    if memory_mode in ["Kombiniert", "Nur Sessions"]:
        all_sessions = st.session_state.memory_sessions.get(use_case, [])
        for session in all_sessions:
            for message in session.get("messages", []):
                role = message.get("role")
                content = message.get("content", "").strip()
                if role and content and content not in combined_memory[role]:
                    combined_memory[role] += f" {content}"

    return {key: value.strip() for key, value in combined_memory.items()}

def render_memory_list(file):
    """
    Zeigt eine Liste der persistierenden Memories mit Bearbeitungs- und Lösch-Option.
    """
    persistent_memories = load_memories(file)
    
    st.write("####🛠 Memory Bearbeitung")
    if not persistent_memories:
        st.info("⚠️ Keine gespeicherten Memories vorhanden.")

    for i, memory in enumerate(persistent_memories):
        col1, col2 = st.columns([4, 1])
        with col1:
            updated_memory = st.text_area(f"Memory {i+1}", value=memory["memory"], key=f"edit_memory_{i}")
            persistent_memories[i]["memory"] = updated_memory

        with col2:
            if st.button("❌", key=f"delete_memory_{i}", help="Memory löschen"):
                del persistent_memories[i]
                save_memories(persistent_memories, file)
                st.rerun()

def render_persistent_memory_chat_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    """
    Rendert die Memory-Ansicht mit Steuerungsoptionen für Memory-Quellen.
    """
    
    # Hauptansicht
    st.subheader(title)
    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    # **Session State initialisieren**
    st.session_state.setdefault("memory_sessions", {})
    st.session_state.setdefault("global_memory", [])
    st.session_state.setdefault("memory_mode", "Kombiniert")  # Standardmäßig „Kombiniert“
    st.session_state.setdefault("edit_mode", False)  # Steuert die Sichtbarkeit der Edit-Funktion
    st.session_state.setdefault("add_memory", False)  # Verhindert ungewolltes Triggern
    st.session_state.setdefault("new_memory_input", "")  # Sicherstellen, dass es initialisiert ist

    # **Sessions laden**
    sessions = load_sessions(session_file)
    st.session_state.memory_sessions[use_case] = sessions

    # **Falls keine aktive Session existiert, initialisieren**
    if "active_use_case" not in st.session_state or st.session_state["active_use_case"] != use_case:
        st.session_state["active_use_case"] = use_case
        st.session_state["current_session"] = {
            "session_id": str(uuid.uuid4()),
            "messages": [],
            "metrics": {"total_tokens": 0, "total_costs": 0.0, "tokens_used_per_request": [], "costs_per_request": [], "request_names": []},
        }

    # Sidebar aktualisieren // nur für Testzwecke
    # with st.sidebar:
    #    update_sidebar(use_case, session_file)

    # **🟢 UI: Steueroptionen für Memory-Quellen mit Radio-Buttons**

    st.session_state["memory_mode"] = st.radio(
        "Wähle die gewünschte Memory-Quelle:",
        ["Kombiniert", "Nur Memories", "Nur Sessions"],
        horizontal=True,
        index=["Kombiniert", "Nur Memories", "Nur Sessions"].index(st.session_state["memory_mode"])
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        # **🔄 Edit-Modus Button**
        if st.button("✏️ Edit Memories"):
            st.session_state["edit_mode"] = not st.session_state["edit_mode"]  # Umschalten

    with col2:
        # **💾 Memory hinzufügen Button**
        if st.button("➕ Neue Memory hinzufügen"):
            st.session_state["add_memory"] = True  # Öffnet das Eingabefeld

    # **Memory-Eingabe nur anzeigen, wenn "add_memory" aktiv ist**
    if st.session_state["add_memory"]:
        new_memory_value = st.text_input("📌 Neue Erinnerung eingeben", key="memory_input_key")

        if st.button("💾 Speichern"):
            if new_memory_value.strip():
                persistent_memories = load_memories(PERSISTENT_MEMORY_FILE)
                persistent_memories.append({"session": "sessionID", "memory": new_memory_value.strip()})
                save_memories(persistent_memories, PERSISTENT_MEMORY_FILE)
                st.success("✅ Neue Memory gespeichert!")
                
                # **Nach dem Speichern zurücksetzen, aber erst nach dem Rendern**
                st.session_state["add_memory"] = False
                st.rerun()

    # **Chat & User Interaction**
    for msg in st.session_state["current_session"]["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # **Benutzer-Input (Prompt-Feld bleibt sichtbar)**
    prompt = st.chat_input(f"💡 Frage zu {use_case} stellen:")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state["current_session"]["messages"].append({"role": "user", "content": prompt})

        try:
            with st.chat_message("assistant"):
                with st.spinner("🔄 Verarbeite Anfrage..."):
                    combined_memory = generate_combined_memory(use_case, st.session_state["memory_mode"])
                    serialized_context = json.dumps({
                        "memory": combined_memory,
                        "conversation": [msg["content"] for msg in st.session_state["current_session"]["messages"]],
                    })
                    
                    response, tokens_used, costs, _ = handle_query(
                        query=prompt,
                        use_case=use_case,
                        context=serialized_context,
                        model_name=model_name,
                    )

                    st.markdown(response)
                    st.session_state["current_session"]["messages"].append({"role": "assistant", "content": response})

                    # **Session speichern**
                    sessions.append(st.session_state["current_session"].copy())
                    save_sessions(session_file, sessions)
                    st.session_state.memory_sessions[use_case] = sessions  # Aktualisiere globalen Zustand

        except Exception as e:
            st.error(f"⚠️ Fehler: {e}")

    # **Persistente Memories bearbeiten (nur wenn Edit-Mode aktiv ist)**
    if st.session_state["edit_mode"]:
        render_memory_list(PERSISTENT_MEMORY_FILE)