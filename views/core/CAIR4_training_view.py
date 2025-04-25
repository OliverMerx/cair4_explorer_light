from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.random_lib import random

from streamlit_extras.stylable_container import stylable_container
from streamlit_option_menu import option_menu

from utils.core.CAIR4_pdf_viewer import render_pdf_viewer
from utils.core.CAIR4_legal_manager import render_legal_pills
from utils.core.CAIR4_video_teaser_btn import  render_use_case_video_teaser
from views.core.CAIR4_multi_chat_view_experiment import render_multi_chat_view

PDF_FOLDER = "CAIR4_data/pdf"
COLLECTIONS = st.session_state.get("collections", {})
TRAINING = st.session_state.get("training", {})


FAQs = [
    "Was macht dieser Code genau?",
    "Was ist die regulatorische Relevanz dieses Use Cases?",
    "Welche Risiken können sich aus der Nutzung ergeben?",
    "Wie unterscheidet sich das von klassischer Software?",
    "Gibt es Einschränkungen bei diesem Szenario?"
]

def load_ascii_content():
    ascii_diagram = ""
    ascii_filename = st.session_state.get("ascii_filename", None)
    if ascii_filename:
        ascii_path = os.path.join(st.session_state.get("base_path", ""), ascii_filename)
        try:
            with open(ascii_path, "r", encoding="utf-8") as f:
                ascii_diagram = f.read()
        except Exception as e:
            st.warning(f"⚠️ Fehler beim Laden des ASCII-Diagramms: {e}")
    return ascii_diagram

def render_ascii_tab():
    ascii_content = load_ascii_content()
    if ascii_content:
        st.code(ascii_content, language="text")
    elif st.session_state.get("ascii_filename"):
        st.info("ℹ️ ASCII-Diagramm ist leer oder konnte nicht geladen werden.")

def load_source_code():
    code = ""
    if "view_path" in st.session_state:
        try:
            file_path = st.session_state.view_path
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
        except Exception as e:
            st.warning(f"⚠️ Fehler beim Laden der Datei: {e}")
    else:
        st.warning("⚠️ Kein 'view_path' im Session State gefunden.")
    return code

def render_source_code_tab():
    code_content = load_source_code()
    if code_content:
        st.code(code_content, language="python")
    elif "view_path" in st.session_state:
        st.info("ℹ️ Quellcode ist leer oder konnte nicht geladen werden.")
    else:
        st.info("ℹ️ Kein Quellcode verfügbar.")

def render_legal_info_tab(legal_info):
    col_left, col_mid, col_right = st.columns([2, 1, 2])
    with col_left:
        st.write("Weiterführende Links:")
        st.write(legal_info.get("description", ""))
        links = legal_info.get("links", [])
        if links:
            for link in links:
                title = link.get("title", "Unbekannter Titel")
                url = link.get("link", "#")
                st.markdown(f'🔗 [{title}]({url})', unsafe_allow_html=True)
        else:
            st.info("📭 Keine weiterführenden Links verfügbar.")
    with col_mid:
        pass
    with col_right:
        st.write("Artikel & Erwägungsgründe")
        for regime in ["aia", "gdpr"]:
            if regime in legal_info and isinstance(legal_info[regime], dict):
                render_legal_pills({regime: legal_info[regime]})

def render_multi_chat_tab():
    code = load_source_code()
    ascii_content = load_ascii_content()
    title = st.session_state.get("selected_use_case", "Unbekannter Use Case")
    description = COLLECTIONS.get(title, {}).get("description", "Keine Beschreibung verfügbar.")
    st.session_state.setdefault("selected_faq",)
    st.session_state.setdefault("messages",[])

    render_multi_chat_view(title, description, ascii_content, code, False)

def render_training_view():
    selected_use_case = st.session_state.get("previous_use_case", None)

    if not selected_use_case or selected_use_case not in COLLECTIONS:
        st.warning("⚠️ Kein gültiger Use Case ausgewählt.")
        
    training_content = st.session_state.selected_training
    st.session_state["selected_use_case"] = selected_use_case
    selected_training_key = COLLECTIONS[selected_use_case]["name"]
    training_content = TRAINING.get(selected_training_key, {})

    # === Menüstruktur vorbereiten ===
    menu_items = []
    callbacks = []

    sections = training_content.get("sections", {})

    # 🎬 Intro Video
    intro_videos = sections.get("intro_video", [])
    valid_videos = [v for v in intro_videos if v.get("link")]

    if valid_videos:
        menu_items.append("Intro Video")
        def render_video_tab():
            try:
                videos = {entry.get("title", f"Video {i+1}"): entry.get("link", "") for i, entry in enumerate(valid_videos)}
                render_use_case_video_teaser(videos)
            except Exception as e:
                st.info(f"⚠️ Fehler beim Laden des Videos: {e}")
        callbacks.append(render_video_tab)

    # 🧱 ASCII-Grafik
    ascii_filename = sections.get("ascii", "")
    st.session_state["ascii_filename"] = ascii_filename
    if ascii_filename:
        menu_items.append("ASCII-Diagramm")
        callbacks.append(render_ascii_tab)

    # 💬 Steckbrief PDF
    info = sections.get("use_case_info", {})
    pdf_filename = info.get("description", "")
    pdf_path = os.path.join(st.session_state.get("base_path", ""), "assets/docs/use_cases/", pdf_filename)
    if pdf_filename and ".pdf" in pdf_filename and os.path.exists(pdf_path):
        menu_items.append("Use Case Steckbrief")
        def render_pdf_tab():
            try:
                render_pdf_viewer(pdf_path)
            except:
                st.info("⚠️ Fehler beim Laden der PDF.")
        callbacks.append(render_pdf_tab)

    legal_info = sections.get("legal_info", {})
    has_links = bool(legal_info.get("links"))
    has_articles = any(k in legal_info for k in ["aia", "gdpr"])

    if has_links or has_articles:
        menu_items.append("Links & more")
        def render_legal_tab():
            try:
                render_legal_info_tab(legal_info)
            except Exception as e:
                st.info(f"⚠️ Fehler beim Laden rechtlicher Inhalte: {e}")
        callbacks.append(render_legal_tab)

    # 💻 Beschreibung & Code (immer anzeigen, oder wenn 'view_path' vorhanden)
    if "view_path" in st.session_state:
        menu_items.append("Python-Code")
        callbacks.append(render_source_code_tab)

    menu_items.append("🧠 Dr. Know fragen")
    callbacks.append(render_multi_chat_tab)

    # === Layout mit Option Menu ===
    col1, col2 = st.columns([1, 3], gap="medium")
    with col1:
        with st.expander(f"🧠 Inhalte zu {st.session_state.selected_use_case}", expanded=True):
            selected_tab = option_menu(
                menu_title="",
                options=menu_items,
                default_index=0,
                orientation="vertical",
                styles=st.session_state.get("dialog_colors", {}),
            )

    with col2:
        container_key = f"training_content_{random.randint(1,999999)}"
        with stylable_container(
            key=container_key,
            css_styles=f"""{{
                padding: 10px;
                border-radius: 15px;
                margin-bottom: -10px;
                border-style:solid;
                border-width:1px;
                border-color:#ccc!important;
                width: 100%;
                min-height:65vh!important;
                height:auto;
                max-height:55vh!important;
                overflow-y:auto;
            }}"""
        ):
            for i, label in enumerate(menu_items):
                if selected_tab == label:
                    callbacks[i]()
                    break
