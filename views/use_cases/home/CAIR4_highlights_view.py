from pylibs.streamlit_lib import streamlit as st
from pylibs.random_lib import random
from streamlit_extras.stylable_container import stylable_container
from utils.core.CAIR4_encrypt_manager import encrypt_data  # falls du's wie bisher nutzt

import time

def styled_container(bg_color, text_color, key, width, height, margin_top=0, shadow=True):
    with stylable_container(
        key=f"style_container_{key}",
        css_styles=f"""{{
                background-color: {bg_color}!important;
                color: {text_color};
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 20px!important;
                width: {width}!important;
                margin-top:{margin_top};
                height: {height}!important;
                overflow-y:auto;
            }}
            """
        ):
        return st.container()

def render_highlights_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
   
    # Hauptansicht
    st.subheader(title)

    # 🔹 Expander für die gewählte Beschreibung
    st.write(description)

    slides = context

    for idx, slide in enumerate(slides):
        with styled_container("#fff", "#000", f"teaser_{idx}", "100%", "auto", margin_top=10):

            col1, col2 = st.columns([2, 3])

            with col1:
                image_key = f"image_teaser_{slide['link']}_{idx}"
                with stylable_container(
                    key=image_key,
                    css_styles="""{ margin-top: 0px; padding-top:10px; }"""
                ):
                    st.image(slide["image"],width=300)

            with col2:
                text_key = f"text_teaser_{slide['link']}_{idx}"
                with stylable_container(
                    key=text_key,
                    css_styles="""{ margin-top: 10px; }"""
                ):
                    st.subheader(slide["title"])
                    st.markdown(slide["description"])

                    role_token = encrypt_data(st.session_state.get("user_role", "guest_home"))
                    target_url = f"?role={role_token}&view={slide['link']}"

                    #st.markdown(
                    #    f"""
                    #    <a href="{target_url}" target="_self"
                    #       style="text-decoration: none;
                    #              font-weight: bold;
                    #              color: #666;">
                    #        ➡️ Mehr erfahren
                    #    </a>
                    #    """,
                    #    unsafe_allow_html=True
                    #)