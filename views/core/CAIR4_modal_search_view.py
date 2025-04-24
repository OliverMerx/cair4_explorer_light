"""
===========================
🔍 CAIR4 Kombi-Suchansicht
===========================
Suchfunktion für Use Cases UND PDFs
Dynamisches Nachladen der PDF-Komponente (FAISS) erst bei Bedarf.

Verwendung:
from views.core.CAIR4_search_modal import render_search_modal
render_search_modal(COLLECTIONS)
===========================================
"""
from pylibs.streamlit_lib import streamlit as st  
from streamlit_extras.stylable_container import stylable_container
from collections import defaultdict
from pylibs.importlib_lib import importlib
from utils.core.CAIR4_encrypt_manager import encrypt_data
import pandas as pd
from collections import defaultdict
import unicodedata


def extract_snippet(text, keyword, window=30):
    if not text:
        return ""
    keyword_lower = keyword.lower()
    idx = text.lower().find(keyword_lower)
    if idx == -1:
        return text[:window] + "..."
    start = max(0, idx - window)
    end = min(len(text), idx + len(keyword) + window)
    return "..." + text[start:end] + "..."


# === 📋 Neuer Tag-basierter Filter mit Use Case Anzeige ===
def render_tag_filter_view(collections):

    # 🧠 Hilfsfunktion für Buchstabenvergleich
    def get_first_letter(s):
        first_char = s.strip()[0] if s else ""
        norm = unicodedata.normalize('NFKD', first_char).encode('ASCII', 'ignore').decode('utf-8')
        return norm.upper()

    all_tags = defaultdict(list)

    # 📦 Alle Tags aus Collection extrahieren
    for name, data in collections.items():
        tags = data.get("tags", "")     
        for tag in tags.split(","):
            tag = tag.strip().lstrip("#'\"").rstrip("'\"").strip()
            if tag:
                normalized_tag = tag.lower()
                all_tags[normalized_tag].append((name, data))

    # 🔤 Anfangsbuchstaben dynamisch extrahieren
    available_letters = sorted(set(get_first_letter(tag) for tag in all_tags if tag))
    selected_letter = st.selectbox("🔤 Tags nach Anfangsbuchstabe filtern", ["Alle"] + available_letters)

    # 📍 Filter anwenden
    filtered_tags = {
        tag: entries for tag, entries in sorted(all_tags.items())
        if selected_letter == "Alle" or get_first_letter(tag) == selected_letter
    }

    if not filtered_tags:
        st.info("Keine Tags gefunden für diese Auswahl.")
        return

    # ➗ Tags gleichmäßig auf zwei Spalten verteilen
    tag_items = list(filtered_tags.items())
    mid_point = len(tag_items) // 2 + len(tag_items) % 2
    col1, col2 = st.columns(2)
    pre_key = encrypt_data(st.session_state.user_role)
    for idx, (col, slice_tags) in enumerate(zip([col1, col2], [tag_items[:mid_point], tag_items[mid_point:]])):
        with col:
            for tag, entries in slice_tags:
                st.markdown(f"### <span style='color:#002060;'>#{tag}</span>", unsafe_allow_html=True)
                for name, data in entries:
                    title = data.get("title", name)
                    
                    st.markdown(
                        f"""<p style='margin-left:10px'>
                            <a href="?role={pre_key}&view={name}" target="_self">🔗 {title}</a>
                        </p>""",
                        unsafe_allow_html=True
                    )

                    #st.markdown(f"- [{title}](?role={pre_key}&view={name})")


def render_search_modal(collections):
    # === State Defaults (nur einmal)
    st.session_state.setdefault("activate_pdf_search", False)
    st.session_state.setdefault("active_tag", "")
    st.session_state.setdefault("active_query", "")
    
    # Neuer State für Tag-Button-Klick
    if "tag_button_clicked" not in st.session_state:
        st.session_state.tag_button_clicked = False
    
    # Callback für das Textfeld
    def on_text_change():
        # Speichere den eingegebenen Text
        st.session_state.active_query = st.session_state.search_input
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        with st.expander("", expanded=True):
            # Wenn Tag-Button geklickt wurde, leere das Suchfeld
            if st.session_state.tag_button_clicked:
                # Setze den Wert zurück
                st.session_state.active_query = ""
                st.session_state.tag_button_clicked = False
            
            # Textfeld mit on_change Callback
            input_query = st.text_input("🔍 Stichwort eingeben...", 
                                       value=st.session_state.active_query,
                                       key="search_input",
                                       on_change=on_text_change)
            
            use_case_clicked = st.button("Use Case Suche", key="usecase_btn")
            pdf_clicked = st.button("PDF-Suche", key="pdf_btn", disabled=not st.session_state.activate_pdf_search)
            st.checkbox("PDF-Suche aktivieren", key="activate_pdf_search")
            
            # Callback für Tag-Button
            def on_tag_click():
                st.session_state.tag_button_clicked = True
            
            tag_clicked = st.button("📌 Tags anzeigen", key="tag_btn", on_click=on_tag_click)


    with col2:
        with stylable_container(
            key=f"search_result_container",
            css_styles=f"""{{
                padding: 10px;
                border-radius: 15px;
                margin-bottom: -10px;
                border-style:solid;
                border-width:1px;
                border-color:#ccc!important;
                width: 100%;
                min-height:60vh!important;
                height:auto;
                max-height:55vh!important;
                overflow-y:auto;
            }}"""
        ):

            # === Hauptlogik: Suche oder Tag-Navigation ===

            # Suchbegriff (manuelle Eingabe)
            query = input_query.strip()
            st.session_state.active_query = query  # zum Merken

            # === 1️⃣ Volltextsuche: Use Cases
            if query and pdf_clicked:
                if st.session_state.activate_pdf_search:
                    try:
                        pdf_module = importlib.import_module("utils.core.CAIR4_pdf_vectorize_manager")
                        pdf_module.render_pdf_search_results(query)
                    except Exception as e:
                        st.error(f"Fehler beim Laden des PDF-Suchmoduls: {e}")
                else:
                    st.warning("Bitte aktiviere die PDF-Suche zuerst über die Checkbox.")

            elif query and use_case_clicked:
                render_use_case_results(query, collections)

            elif not query:
                render_tag_filter_view(collections)

            else:
                st.info("Keine passenden Use Cases gefunden.")

def render_use_case_results(query, collections):
    seen_titles = set()
    matches = {
        name: data for name, data in collections.items()
        if query.lower() in name.lower()
        or query.lower() in data.get("title", "").lower()
        or query.lower() in data.get("description", "").lower()
        or query.lower() in data.get("tags", "").lower()
    }

    if matches:
        st.markdown("### 📋 Use Case Treffer")
        for name, data in matches.items():
            title = data.get("title", name)
            if title in seen_titles:
                continue
            seen_titles.add(title)

            chapter = data.get("chapter", "–")
            pre_key = {encrypt_data(st.session_state.user_role)}
            url = f"?role={pre_key}&view={name}"
            snippet = extract_snippet(data.get("description", ""), query)
            
            st.markdown(f"""
            <div style='padding:8px 0'>
                <b>Kapitel:</b> {chapter}<br>
                <b>Use Case:</b> <a href="{url}" target="_self">{title}</a><br>
                <b>Treffer:</b> <i>{snippet}</i>
            </div>
            <hr style='margin:5px 0 10px 0;'>
            """, unsafe_allow_html=True)
    else:
        st.info("Keine passenden Use Cases gefunden.")