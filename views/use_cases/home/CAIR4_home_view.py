from pylibs.streamlit_lib import streamlit as st
from pylibs.base64_lib import base64
from utils.core.CAIR4_background_image_util import set_new_background
from utils.core.CAIR4_video_teaser import render_video_teaser
from utils.core.CAIR4_pills_teaser import render_use_case_pills
from utils.core.CAIR4_home_chat_teaser_combined import render_home_chat_teaser
from utils.core.CAIR4_home_journey_teaser import render_home_journey_teaser

import time

# 📌 **Hauptfunktion für die Home-Page**
def render_home_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    #file = "/assets/images/"+system_message
    #image_path = st.session_state.base_path+file  
    set_new_background(False)
    
    st.markdown("<div class='title-box'>CAIR4 Explorer</div>", unsafe_allow_html=True)

    COLLECTIONS=st.session_state.collections

    st.markdown(f"""
        <style>
        .title-box {{
            font-size: 40px!important;
            font-weight: bold;
            width: fit-content;
            color: {st.session_state.header_color};
            margin-bottom: 30px;
            padding-left: 20px!important;
            padding-right: 20px;
            background-color: {st.session_state.bg_color};
            box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
            margin-top:-88px;
        }}
            </style>
    """, unsafe_allow_html=True)
    
    videos = {
        "Feed Forward Chat": "https://youtu.be/Ee4RwwGuG1E?feature=shared",
        "Deep Learning Basics": "https://www.youtube.com/embed/O5xeyoRL95U?si=32S-53-xgCWv32h4",
        "Python für Einsteiger": "https://www.youtube.com/embed/9mmVa6O-hzQ?si=a7z7LEgtOj1j08r4",
        "Übersicht EU AI Act": "https://www.youtube.com/embed/5SVEBQyOr7U?si=NTeg9tXg0vYaGmcJ",
    }

    use_cases = ["Sprachmodell-Optimierung", "Automatisierte Prozesssteuerung", "Datenanalyse mit KI"]
    chapters = ["Kapitel 1: Einführung", "Kapitel 2: Grundlagen", "Kapitel 3: Fortgeschrittene Techniken"]

    role = st.session_state.get("user_role")

    #if role.startswith("guest_home"):
    #    render_slider_teaser()
    #else:
    render_home_chat_teaser()
        
    render_video_teaser(videos)
    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True)
  
    render_use_case_pills(COLLECTIONS)
    """
    col1,col2 = st.columns([1, 1])
    with col1:
        st.write("Hello")
        #render_chapter_teaser(COLLECTIONS)

    with col2:
              # 📌 Unabhängige Zufallsauswahlen
        render_api_item()
        render_creator_item()
        render_twin_item()
        render_random_item("use_case_index", use_cases, "📌 Zufälliger Use Case")
        render_random_item("chapter_index", chapters, "📌 Zufälliges Kapitel")"
        """
    
    if role.startswith("guest_home"):
        pass
    else:
        render_home_journey_teaser()
    
    #render_chapter_teaser(COLLECTIONS)
    #st.markdown(
    #    """
    #   </div>
    #   """,
    #   unsafe_allow_html=True)
      