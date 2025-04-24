"""
=================================================
CAIR4 Memory Manager (CAIR4_memory_manager.py)
=================================================

Dieses Modul verwaltet Memories für das CAIR4-System.
Es ist in den Settings verankert, bezieht sich aber auf den Use Case "CAIR4_memory_view"

Funktionen:
- `ensure_file_exists(memory_file)`: Stellt sicher, dass die Speicherdatei existiert.
- `load_memories(memory_file)`: Lädt Memories und wandelt alte Formate automatisch um.
- `save_memories(memories, memory_file)`: Speichert Memories in der JSON-Datei.
- `format_memory_with_linebreak(memory, max_length=140)`: Fügt Zeilenumbrüche in längere Memories ein.
- `show_memories(memory_file)`: Zeigt Memories in der Streamlit-UI an.

Verwendung:
    from utils.core.CAIR4_memory_manager import show_memories

    show_memories("CAIR4_data/data/memory.json")
"""

# === 1️⃣ Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json


# === 2️⃣ Speicherfunktionen (Datei-Handling) ===
def ensure_file_exists(memory_file):
    """Stellt sicher, dass die Datei existiert. Falls nicht, wird eine neue leere Datei erstellt."""
    if not os.path.exists(memory_file):
        with open(memory_file, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)


def load_memories(memory_file):
    """Lädt Memories und wandelt alte Formate um (Liste von Strings → Liste von Dictionaries)."""
    ensure_file_exists(memory_file)  # Datei erstellen, falls sie fehlt
    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            memories = json.load(f)
            # Falls altes Format → Umwandlung in Dictionaries
            if isinstance(memories, list) and all(isinstance(m, str) for m in memories):
                memories = [{"session": "sessionID", "memory": m} for m in memories]
                save_memories(memories, memory_file)
            return memories if isinstance(memories, list) else []
    except (json.JSONDecodeError, IOError):
        return []  # Falls die Datei beschädigt ist


def save_memories(memories, memory_file):
    """Speichert Memories in der JSON-Datei"""
    ensure_file_exists(memory_file)
    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=4, ensure_ascii=False)


# === 3️⃣ UI-Funktionen (Streamlit) ===
def show_memories(memory_file):
    """Zeigt gespeicherte Memories in der UI an."""
    st.subheader("📚 Memory Management")

    # **Memories in den Session-State laden (nur 1x)**
    if "global_memory" not in st.session_state:
        st.session_state["global_memory"] = load_memories(memory_file)

    # **Anzeige der gespeicherten Memories**
    if st.session_state["global_memory"]:
        for i, memory in enumerate(st.session_state["global_memory"]):
            if not isinstance(memory, dict) or "memory" not in memory:
                continue  # Überspringe ungültige Einträge

            col1, col2 = st.columns([4, 1])
            with col1:
                updated_memory = st.text_area(
                    f"Memory {i+1}",
                    value=format_memory_with_linebreak(memory["memory"]),
                    key=f"edit_memory_{i}"
                )
                st.session_state["global_memory"][i]["memory"] = updated_memory

            with col2:
                if st.button("❌", key=f"delete_memory_{i}", help="Delete this memory"):
                    delete_memory(i, memory_file)

    else:
        st.warning("⚠️ No memories found.")

    # **Neue Memory hinzufügen**
    add_new_memory(memory_file)

    # **Alle Memories löschen**
    if st.button("🗑️ Clear All Memories"):
        clear_all_memories(memory_file)


def add_new_memory(memory_file):
    """UI-Funktion: Fügt eine neue Memory hinzu."""
    st.subheader("➕ Add New Memory")

    if "new_memory" not in st.session_state:
        st.session_state["new_memory"] = ""

    new_memory_value = st.text_input("New Memory", value=st.session_state["new_memory"], key="new_memory")

    if st.button("💾 Save New Memory"):
        if new_memory_value.strip():
            st.session_state["global_memory"].append({"session": "sessionID", "memory": new_memory_value.strip()})
            save_memories(st.session_state["global_memory"], memory_file)
            st.success("✅ New memory added successfully!")
            st.session_state["new_memory"] = ""
            st.rerun()


def delete_memory(index, memory_file):
    """Löscht eine einzelne Memory und aktualisiert die UI."""
    del st.session_state["global_memory"][index]
    save_memories(st.session_state["global_memory"], memory_file)
    st.success("✅ Memory deleted successfully!")
    st.rerun()


def clear_all_memories(memory_file):
    """Löscht alle gespeicherten Memories."""
    st.session_state["global_memory"] = []
    save_memories([], memory_file)
    st.success("🗑️ All memories")
    

def format_memory_with_linebreak(memory, max_length=140):
    """Fügt Zeilenumbrüche in längere Memory-Texte ein"""
    if not isinstance(memory, str):
        return ""
    return '\n'.join([memory[i:i + max_length] for i in range(0, len(memory), max_length)])