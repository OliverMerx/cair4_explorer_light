from pylibs.streamlit_lib import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def next_video(videos):
    st.session_state.home_video_index = (st.session_state.home_video_index + 1) % len(videos)

def prev_video(videos):
    st.session_state.home_video_index = (st.session_state.home_video_index - 1) % len(videos)

def styled_container(bg_color, text_color, key, width, height, margin_top=0, shadow=True):
    with stylable_container(
        key=f"style_container_{key}",
        css_styles=f"""{{
                background-color: {bg_color}!important;
                color: {text_color};
                padding: 20px;
                border-radius: 15px;
                margin-bottom: -10px;
                width: {width}!important;
                margin-top:{margin_top};
                height:100%;
                max-height: {height}!important;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
                overflow-y:auto;
            }}
        """
    ):
        return st.container()
def update_home_video_teaser(videos, col1):
    with col1:
        st.video(list(videos.values())[st.session_state.home_video_index])

def render_video_teaser(videos):
    # Initialisiere State nur einmalig
    if "home_video_index" not in st.session_state:
        st.session_state.home_video_index = 0
    if "home_video_label" not in st.session_state:
        st.session_state.home_video_label = list(videos)[0]
    if "home_video_initialized" not in st.session_state:
        st.session_state.home_video_initialized = False

    with styled_container("#fff", "#000", "home_video_teaser", "100%", "100%"):
        st.markdown(f"""<p 
                    style="text-align:left; 
                    font-weight: bold; 
                    font-size: 18px; 
                    color: black;">Empfohlene Videos:
                    </p>""", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])

        with col2:
            video_scrollcontainer = st.container(height=370)
            with video_scrollcontainer:
                for index, (title, url) in enumerate(videos.items()):
                    if st.button(title, key=f"home_video_{index}", use_container_width=False):
                        st.session_state.home_video_index = index
                        st.session_state.home_video_label = title
                        st.session_state.home_video_initialized = True
                        update_home_video_teaser(videos, col1)

            st.markdown("""
                <style>
                    .st-emotion-cache-1qke9ij {
                        margin-top:-5px;
                        padding: 5px !important;
                        border-width:0px;
                     }
                </style>
            """, unsafe_allow_html=True)

        # Nur erstes Video anzeigen, wenn noch keine Auswahl erfolgt ist
        if not st.session_state.home_video_initialized:
            update_home_video_teaser(videos, col1)

def update_use_case_video_teaser(videos, col1):
    with col1:
        st.video(list(videos.values())[st.session_state.use_case_video_index])

def render_use_case_video_teaser(videos):

    st.session_state.use_case_video_initialized = False

    st.session_state.use_case_video_index = 0
    st.session_state.use_case_video_label = list(videos)[0]


    with st.container():
        col1, col2 = st.columns([3, 1])

        with col2:
            video_scrollcontainer = st.container(height=370, border=True)

            with video_scrollcontainer:
                for index, (title, url) in enumerate(videos.items()):
                    if st.button(title, key=f"video_{index}", use_container_width=False):
                        st.session_state.use_case_video_index = index
                        st.session_state.use_case_video_label = title
                        st.session_state.use_case_video_initialized = True  # ✅ Ab jetzt ist Initialvideo überschrieben
                        update_use_case_video_teaser(videos, col1)

            # 🛠 CSS-Overflow-Fix
            st.markdown("""
                <style>
                    .st-emotion-cache-1qke9ij {
                        padding: 5px !important;
                     }
                </style>
            """, unsafe_allow_html=True)

        # ✅ Zeige nur dann das erste Video automatisch, wenn noch nicht initialisiert
        if not st.session_state.use_case_video_initialized:
            update_use_case_video_teaser(videos, col1)