import streamlit as st
import os
from core.CAIR4_explorer_config_raw import CAIR4_COLLECTIONS

def render_ascii_overview_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    st.subheader(title)
    st.write(description)

    total_use_cases = 0
    ascii_loaded = 0
    ascii_failed = 0

    for chapter_title, chapter_data in CAIR4_COLLECTIONS.items():
        chapter_index = list(CAIR4_COLLECTIONS.keys()).index(chapter_title)
        if chapter_index == 0:
            continue  # Kapitel 1 überspringen

        use_cases = chapter_data.get("use_cases", {})
        for uc_key, uc_data in use_cases.items():
            if uc_key == "Node(0)":
                continue

            total_use_cases += 1
            name = uc_data.get("name", uc_key)
            ascii_path = uc_data.get("training_sections", {}).get("ascii")

            if ascii_path and os.path.exists(ascii_path):
                try:
                    with open(ascii_path, "r", encoding="utf-8") as f:
                        ascii_art = f.read()
                        uc_data["ascii_art"] = ascii_art  # Optional: speichern für weitere Nutzung
                        ascii_loaded += 1
                        with st.expander(f"📄 **ASCII für {name}**", expanded=True):
                            st.code(ascii_art)
                except Exception as e:
                    ascii_failed += 1
                    st.error(f"Fehler beim Laden von ASCII für {name}: {e}")
            else:
                ascii_failed += 1
                #st.warning(f"❌ Kein gültiger ASCII-Pfad für {name}: {ascii_path}")

    st.session_state.atcf_total_use_cases = total_use_cases

    st.write(f"Insgesamt befinden sich **{total_use_cases-8} CAIR4-Use Cases** in **acht Kapiteln**.")
    st.success(f"✅ {ascii_loaded} ASCII-Diagramme erfolgreich geladen.")
    if ascii_failed:
        st.warning(f"⚠️ {ascii_failed-8} Diagramme konnten nicht geladen werden.")