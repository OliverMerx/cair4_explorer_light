import streamlit as st
import os
from core.CAIR4_explorer_config_raw import CAIR4_COLLECTIONS

def render_chapter_overview_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    st.subheader(title)

    # 🔁 Erste Schleife: Gesamtzahl der Use Cases berechnen
    total_use_cases = 0
    for chapter_title, chapter_data in CAIR4_COLLECTIONS.items():
        chapter_index = list(CAIR4_COLLECTIONS.keys()).index(chapter_title)
        if chapter_index == 0:
            continue  # Kapitel 1 überspringen

        use_cases = chapter_data.get("use_cases", {})
        count = len(use_cases) - 1 if "Node(0)" in use_cases else len(use_cases)
        if count > 1:
            total_use_cases += count

    final_use_cases = total_use_cases-8
    # Speichern & anzeigen
    st.session_state.atcf_total_use_cases = final_use_cases

    st.write(description)
    st.write(f"Insgesamt befinden sich **{final_use_cases} CAIR4-Use Cases** in **acht Kapiteln**.")

    # 🔁 Zweite Schleife: Kapitel + Details anzeigen
    base_path = st.session_state.get("base_path", "views/use_cases")
    loaded = []
    structured = []

    for chapter_title, chapter_data in CAIR4_COLLECTIONS.items():
        chapter_index = list(CAIR4_COLLECTIONS.keys()).index(chapter_title)
        if chapter_index == 0:
            continue  # Kapitel 1 überspringen
        st.subheader(chapter_title)
        if chapter_index==1:
            expand=True
        else:
            expand=False
        with st.expander(f"📁 {chapter_title}", expanded=expand):
            use_cases = chapter_data.get("use_cases", {})

            for idx, (uc_key, uc_data) in enumerate(use_cases.items()):
                if idx == 0:
                    continue  # Erste Node im Kapitel ignorieren

                title = uc_data.get("title", "Untitled")
                description = uc_data.get("description", "")
                view_path = uc_data.get("view", "")
                tags = uc_data.get("tags", "")
                name = uc_data.get("name", uc_key)
                session_file = uc_data.get("session_file", "")

                if "." in view_path:
                    module_path = view_path.split(".")[0:-1]
                    file_path = os.path.join(base_path, *module_path[0:]) + ".py"
                else:
                    file_path = "(kein Pfad verfügbar)"

                exists = os.path.exists(file_path)

                # === Darstellung
                if not st.session_state.get("global_auto_mode", False):
                    st.markdown(f"### {title}")
                    st.write(description if description.strip() else "_Keine Beschreibung vorhanden._")
                    st.code(file_path, language="python")
                    st.markdown(f"📛 **Name**: `{name}`")
                    st.markdown(f"🏷️ **Tags**: `{tags}`")
                    st.markdown(f"✅ Datei vorhanden: {'Ja' if exists else 'Nein'}")

                loaded.append({
                    "key": uc_key,
                    "chapter": chapter_title,
                    "title": title,
                    "name": name,
                    "description": description,
                    "tags": tags,
                    "view_path": view_path,
                    "file_path": file_path,
                    "file_exists": exists
                })

                structured.append({
                    "key": uc_key,
                    "name": name,
                    "chapter": chapter_title,
                    "view_path": view_path,
                    "module_path": "/".join(view_path.split(".")[:-1]) if "." in view_path else "",
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "session_file": session_file
                })