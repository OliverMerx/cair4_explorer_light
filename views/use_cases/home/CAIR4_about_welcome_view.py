
from pylibs.streamlit_lib import streamlit as st
from utils.core.CAIR4_background_image_util import set_background

def render_use_case_welcome_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):

    if st.session_state.selected_use_case is not use_case:
        st.session_state["selected_content_index"] = 0
        st.session_state.selected_use_case = use_case

    # Farbwerte direkt aus der aktuellen Theme abrufen
    bg_color = st.session_state.bg_color 
    header_color = st.session_state.header_color
    text_color = st.session_state.text_color

    # CSS mit korrekter RGBA-Transparenz
    st.markdown(f"""
        <style>
            .overlay-box {{
                background-color: {bg_color}!important; /* CC entspricht ca. 80% Deckkraft */
                padding-left: 15px;
                padding-right: 15px;
                margin-bottom: 35px;
                margin-top: -50px;
                width: fit-content;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
            }}
            .overlay-title {{
                font-size: 40px;
                font-weight: bold;
                color: {header_color};
            }}
            .overlay-description {{
                font-size: 20px;
                color: {text_color};
                max-width: 1000px;
                padding-top: 10px;
                padding-bottom: 10px;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Titel und Beschreibung mit Overlay
    st.markdown(f"""
        <div class="overlay-box">
            <div class="overlay-title">{title}</div>
        </div>
        <div class="overlay-box">
            <div class="overlay-description">{description}</div>
        </div>
    """, unsafe_allow_html=True)


    file = st.session_state.background_image  
    image_path = st.session_state.base_path + file  
    set_background(image_path)
    

    view_name= "Intro-Video"

    # ✅ Custom Style mit CSS für einen schöneren Button
    st.markdown(
        f"""
        <style>
        .custom-button {{
            color: {st.session_state.get("bg_color", "#FFFFFF")};
            background-color: {st.session_state.get("header_color", "#4CAF50")};
            font-size: 24px;
            padding: 10px 20px;
            border-radius: 8px;
            border: 2px solid {st.session_state.get("bg_color", "#FFFFFF")};
            cursor: pointer;
            display: block;
            width: fit-content;
            margin: auto;
            text-align: center;
        }}
        .custom-button:hover {{
            background-color: #45a049;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # ✅ Normaler Streamlit-Button für Funktionalität
    if st.button("weiter zum Intro-Video", key="styled_intro_video_button"):
        st.session_state.selected_use_case = view_name
        if st.session_state.previous_use_case != view_name:
            st.session_state.selected_training = view_name
            st.session_state.previous_use_case = view_name
        st.session_state["selected_content_index"] = 1
        st.rerun()

    # ✅ HTML-Button mit CSS (Funktionalität über Streamlit)
    st.markdown(
        f"""
        <button class="custom-button" onclick="window.location.reload()">weiter zum Intro-Video</button>
        """,
        unsafe_allow_html=True
)

