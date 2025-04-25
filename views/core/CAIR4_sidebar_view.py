"""
=================================================
CAIR4 Sidebar View (CAIR4_sidebar_view.py)
=================================================

Dieses Modul verwaltet die Sidebar für die Anwendung. Es stellt sicher, 
dass alle relevanten Konfigurationen für Use Cases geladen und gesteuert werden.

Funktionen:
- render_sidebar_view(collections, model_options): Erstellt die Sidebar und verwaltet die UI-Elemente.
- initialize_sidebar_session_state(): Initialisiert benötigte Session-State-Werte.

Verwendung:
    from views.core.CAIR4_sidebar_view import render_sidebar_view
    selected_use_case = render_sidebar_view(COLLECTIONS, MODEL_OPTIONS)
"""

# === 1️⃣ Importiere erforderliche Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.time_lib import time
from pylibs.re_lib import re

from core.CAIR4_login_manager import handle_login_dialog
from views.core.CAIR4_settings_view import render_settings_view
from views.core.CAIR4_metrics_view import render_metrics_view
from views.core.CAIR4_modal_search_view import render_search_modal
from views.core.CAIR4_training_view import render_training_view
from views.core.CAIR4_cair4_view import render_cair4_view

from streamlit_option_menu import option_menu  # Wichtig: muss installiert sein
from streamlit_float import float_init, float_css_helper

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
GLOBAL_SETTINGS = st.session_state.get("global_settings", {})

# === 3️⃣ Sicherstellen, dass Session-State korrekt initialisiert ist ===
def initialize_sidebar_session_state():
    default_values = {
        "previous_use_case": None,
        "show_window": False,
        "selected_training": "",
        "selected_chapter": "",
        "selected_model": None,
        "use_local_llm": False,  # 🆕 Standardmäßig API-Modelle nutzen
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_model_selection():
    initialize_sidebar_session_state()

    st.markdown("""
        <style>
        div[role="tooltip"] {
            z-index: 1 !important;
            margin-bottom: 3rem !important;
            margin-left: 2rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
         with st.expander("### ⚙️ Model Setup", expanded=False):

            if "use_local_llm" not in st.session_state:
                st.session_state["use_local_llm"] = False

            st.checkbox("Lokales LLM nutzen", key="use_local_llm", disabled=len(st.session_state.get("local_model_options", {})) < 1)

            available_models = st.session_state.get("local_model_options", {}) if st.session_state["use_local_llm"] else st.session_state.get("api_model_options", {})

            selected_model_display = st.selectbox(
                "Wähle ein KI-Model:",
                list(available_models.keys()),
                key="model_selector",
            )

            if selected_model_display in available_models:
                st.session_state["selected_model"] = available_models[selected_model_display]

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("⚙️ Settings", key="settings_button"):
                    settings_modal()
            with col2:
                if st.button("📊 Metrics", key="metrics_button"):
                    metrics_modal()

# === 🆕 Dialoge mit dynamischer Größe ===
@st.dialog("⚙️ Settings", width="large")
def settings_modal():
    with st.container():
        st.markdown("""
            <style>
            div[data-testid="stDialog"] div[role="dialog"]:has(.settings-dialog) {
                width: 60vw;
                height: 85vh;
            }
            div[data-testid="stDialog"] div[role="dialog"]::-webkit-scrollbar-track {
                margin-left: 10px;  /* 👈 verschiebt die Scrollbar nach innen */
                }
            div[data-testid="stDialog"] div[role="dialog"]::-webkit-scrollbar-thumb {
            }
            </style>
            <span class='settings-dialog'></span>
        """, unsafe_allow_html=True)
        render_settings_view(global_settings=st.session_state.global_settings)

@st.dialog("📊 Metrics", width="large")
def metrics_modal():
    st.markdown("""
        <style>
        div[data-testid="stDialog"] div[role="dialog"]:has(.metrix-dialog) {
            width: 60vw;
            height: 85vh;
            overflow-y: hidden!important;
        }
        div[data-testid="stDialog"] div[role="dialog"]::-webkit-scrollbar-track {
            margin-left:-10px!important;  /* 👈 verschiebt die Scrollbar nach innen */
        }
            div[data-testid="stDialog"] div[role="dialog"]::-webkit-scrollbar-thumb {
        }
        </style>
        <span class='metrix-dialog'></span>
    """, unsafe_allow_html=True)
    render_metrics_view()

def open_training_modal():
    use_case = st.session_state.get("selected_use_case", "Kein Use Case gewählt")
    title = f"💡 CAIR4 Use Case Deep Dive: {use_case}"

    @st.dialog(title, width="large")
    def training_modal():
        st.markdown("""
            <style>
            div[data-testid="stDialog"] div[role="dialog"]:has(.use-case) {
                width: 90vw;
                height: 90vh;
                overflow-y: hidden!important;
            }
            div[data-testid="stDialog"] div[role="dialog"]::-webkit-scrollbar-track {
                margin-left:-10px!important;
                left:-10px!important;
            }
            div[data-testid="stDialog"] div[role="dialog"]::-webkit-scrollbar-thumb {
            }
            </style>
            <span class='use-case'></span>
        """, unsafe_allow_html=True)

        render_training_view()

    training_modal()

@st.dialog(f"🧭 CAIR4 Suche", width="large")
def search_modal():
    st.markdown("""
        <style>
        div[data-testid="stDialog"] div[role="dialog"]:has(.use-case) {
            width: 80vw;
            height: 85vh;
            overflow-y: hidden!important;
        }
        div[data-testid="stDialog"] div[role="dialog"]::-webkit-scrollbar-track {
            margin-left: -10px!important;  /* 👈 verschiebt die Scrollbar nach innen */;
            left:-10px!important;
        }
        div[data-testid="stDialog"] div[role="dialog"]::-webkit-scrollbar-thumb {
        }
        </style>
        <span class='use-case'></span>
    """, unsafe_allow_html=True)
    #render_search_view(COLLECTIONS)
    render_search_modal(st.session_state.get("collections", {}))
    #render_pdf_vectorizer_view()

@st.dialog(f"Login:", width="large")
def login_modal():
    st.markdown("""
        <style>
        div[data-testid="stDialog"] div[role="dialog"]:has(.chat-dialog) {
            width: 50vw;
            height: 65vh;
            vertical_align:center;
            overflow-y: hidden!important;
        }
        div[data-testid="stDialog"] div[role="dialog"]::-webkit-scrollbar-track {
            margin-left: -10px!important;  /* 👈 verschiebt die Scrollbar nach innen */;
            left:-10px!important;
        }
        div[data-testid="stDialog"] div[role="dialog"]::-webkit-scrollbar-thumb {
        }
        </style>
        <span class='chat-dialog'></span>
    """, unsafe_allow_html=True)
    handle_login_dialog()

@st.dialog("🌍 Mehrsprachige Navigation", width="large")
def multilingual_nav():
    st.markdown("## 🌍 Multilingual Navigation")

    st.markdown("""
    <div style='margin-bottom: 1rem; font-size: 0.9rem; color: #444;'>
    This navigation is designed for use with browser-based translation tools (e.g. Google Translate). 
    Use the chapter menu on the left to browse use cases in your preferred language.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        div[data-testid="stDialog"] div[role="dialog"]:has(.multi-nav-dialog) {
            width: 85vw;
            height: 88vh;
            overflow-y: hidden!important;
        }
        .scroll-area {
            max-height: 68vh;
            overflow-y: auto;
            padding-right: 10px;
        }
        .fixed-height {
            max-height: 68vh;
            overflow-y: auto;
        }
        button.chapter-btn {
            width: 100%;
            margin-bottom: 6px;
            background-color: #f1f1f1;
            border-radius: 5px;
            padding: 0.4rem;
            border: 1px solid #ddd;
            font-size: 0.9rem;
            text-align: left;
        }
        </style>
        <span class='multi-nav-dialog'></span>
    """, unsafe_allow_html=True)

    collections = st.session_state.get("collections", {})

    # Kapitel vorbereiten
    chapters = {}
    for name, data in collections.items():
        chapter = data.get("chapter", "Misc")
        chapters.setdefault(chapter, []).append((name, data.get("title", name)))

    chapter_names = sorted(chapters.keys())
    if "ml_nav_selected_chapter" not in st.session_state:
        st.session_state.ml_nav_selected_chapter = chapter_names[0]

    col1, col2 = st.columns([1, 3])

    with col1:
        with st.expander("📚 Kapitel wählen", expanded=True):
            for chapter in chapter_names:
                if st.button(f"{chapter}", key=f"btn_{chapter}"):
                    st.session_state.ml_nav_selected_chapter = chapter

    with col2:
        selected_chapter = st.session_state.ml_nav_selected_chapter
        with st.container(height=400):
            st.markdown('<div class="scroll-area">', unsafe_allow_html=True)
            for uc_name, uc_title in chapters.get(selected_chapter, []):
                st.markdown(f"""<a href="?view={uc_name}" target="_self">{uc_title}</a>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def initialize_float_training_manager():

    float_init()

    # Globale Button-Styles
    st.markdown("""
        <style>
        .floating-btn button {
            height: 40px;
            width: 45px !important;
            font-size: 18px;
            font-weight: bold;
            border-radius: 100px;
            background-color: white !important;
            color: black;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    # Positions-Offset
    start_top = "1rem"
    step = 3       # rem Abstand
    right_offset = 2
    width = "2.5rem"

    buttons = [    
        ("🔐", "login_button", "Login", lambda: login_modal(),0),
        #("🌍", "navi_button", "Language", lambda: multilingual_nav(),0),
        ("🔍", "search_button", "Suche", lambda: search_modal(),0.5),
        ("💡", "help_button", "Deep Dive", lambda: open_training_modal(),1),
    ]

    for i, (emoji, key, tooltip, callback, distance) in enumerate(buttons):
        css = float_css_helper(
            width=width,
            top=start_top,
            right=f"{right_offset + i * step+distance}rem",
            z_index="99999"
        )

        container = st.container()
        with container:
            if st.button(emoji, key=key, help=tooltip):
                callback()
        container.float(css)

def render_sidebar_view(collections, model_options, direct=False, initial_chapter=None, initial_use_case=None):
    import time
    import re
    from streamlit_option_menu import option_menu

    styles = {
        "container": {"max-height": "250px", "overflow-y": "auto", "padding": "0!important", "background-color": "#fafafa"},
        "menu-title": {"padding-top": "8px!important", "font-family": "Arial", "font-size": "14px", "font-weight": "600", "text-align": "left"},
        "menu-icon": {"font-size": "18px!important"},
        "nav-link": {
            "font-family": "Arial",
            "font-size": "14px",
            "text-align": "left",
            "border-radius":"8px",
            "padding-left": "12px!important",
            "padding-right": "12px!important",
            "--hover-color": "#eee"
            },
        "nav-link-selected": {"background-color": st.session_state.get("button_bg_color", "#e0e0e0")}
    }

    # === Kapitel und Use Cases vorbereiten ===
    raw_chapters = set(data["chapter"] for data in collections.values())
    home_chapters = [ch for ch in raw_chapters if ch.strip().lower() in ("home", "homepage")]
    other_chapters = [ch for ch in raw_chapters if ch not in home_chapters]

    def chapter_sort_key(ch):
        match = re.match(r"(\d+)", ch)
        return int(match.group(1)) if match else 9999

    sorted_other_chapters = sorted(other_chapters, key=chapter_sort_key)
    chapters = home_chapters + sorted_other_chapters

    grouped_usecases = {chapter: [] for chapter in chapters}
    for name, data in collections.items():
        grouped_usecases[data["chapter"]].append(name)

    # === Initialisierung Session State ===
    if "selected_chapter" not in st.session_state or not st.session_state.selected_chapter:
        st.session_state.selected_chapter = chapters[0]

    if "selected_use_case" not in st.session_state:
        st.session_state.selected_use_case = grouped_usecases[st.session_state.selected_chapter][0]

    # === Direktparameter überschreiben ===
    if initial_chapter and initial_chapter in chapters:
        st.session_state.selected_chapter = initial_chapter

    if initial_use_case and initial_use_case in grouped_usecases.get(st.session_state.selected_chapter, []):
        st.session_state.selected_use_case = initial_use_case

    current_chapter = st.session_state.selected_chapter
    current_use_case = st.session_state.selected_use_case
    current_use_cases = grouped_usecases[st.session_state.selected_chapter]
    if st.session_state.selected_use_case not in current_use_cases:
        st.session_state.selected_use_case = current_use_cases[0]

    with st.sidebar:
        with st.expander("Inhalte wählen", expanded=True):
            # === Kapitel-Menü ===
            chapter_index = chapters.index(current_chapter)
            selected_chapter = option_menu(
                menu_title="Kapitel:",
                options=chapters,
                menu_icon="folder",
                default_index=chapter_index,
                orientation="vertical",
                styles=styles,
                key="kapitel_menu",
                icons=['house'] + ["list-task"] * (len(chapters) - 1)
            )

            # === Kapitelwechsel erkannt ===
            if selected_chapter != current_chapter:
                st.session_state.selected_chapter = selected_chapter
                st.session_state.selected_use_case = grouped_usecases[selected_chapter][0]
                current_use_case = st.session_state.selected_use_case  # <-- wichtig
            else:
                current_use_case = st.session_state.selected_use_case

            # === Use Case-Menü ===
            current_use_cases = grouped_usecases[st.session_state.selected_chapter]
            try:
                use_case_index = current_use_cases.index(current_use_case)
            except ValueError:
                use_case_index = 0

            selected_use_case = option_menu(
                menu_title="Use Cases:",
                options=current_use_cases,
                default_index=use_case_index,
                menu_icon="list-task",
                orientation="vertical",
                styles=styles,
                key=f"use_case_menu_{selected_chapter}",
                icons=["code"] * len(current_use_cases),
            )

            if st.session_state.get("sidebar_use_case_selection") != selected_use_case:
                st.session_state["selected_use_case"] = selected_use_case
                st.session_state["active_view"] = selected_use_case
                st.session_state["sidebar_use_case_selection"] = selected_use_case # Verhindert endlos-Reruns
                if direct:  # Nur nach einem Direktaufruf explizit neu rendern
                    st.rerun()

            if st.session_state.previous_use_case != selected_use_case:
                st.session_state.selected_training = selected_use_case
                st.session_state.previous_use_case = selected_use_case

            if selected_use_case != current_use_case and not direct:
                st.session_state.selected_use_case = selected_use_case

    # === Model-UI + Floating Buttons ===
    render_model_selection()
    time.sleep(0.3)
    initialize_float_training_manager()

    if st.session_state.get("logged_in"):
        with st.sidebar:
            st.success(f"✅ Eingeloggt als: {st.session_state.get('current_user')} ({st.session_state.get('user_role')})")

    return st.session_state.selected_use_case
