from pylibs.streamlit_lib import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_option_menu import option_menu


# === Beispiel-Videodatenstruktur: Gruppiert + optionaler Use Case
video_data = {
    "CAIR4 Explorer": [
        ("Login", "https://www.youtube.com/embed/Q10zgtOjrqw?si=7xwRmHsy1lJ7mlB-", None),
        ("Sidebar", "https://www.youtube.com/embed/K-dbB5lrNZk?si=9dzSJEr9PncebBnb", None),
        ("Suche", "https://www.youtube.com/embed/RFxpPPir_ks?si=cSSYw6GP5ikpL4bF", None),
        ("Dr. Know", "https://www.youtube.com/embed/fODMR1zNKXk?si=4x2ZQEyU3SCmpCCq", None),
        ("Journeys", "https://www.youtube.com/v/hh-Ix8puf7w&hl=en&fs=1", None),
        ("Use Cases", "https://www.youtube.com/embed/kFJal1ARyB0?si=RhfVnsJ8WdwNxIC-", None),                ("Deep Dive", "https://www.youtube.com/embed/ACLrtV56h3w?si=IAERR1ArmOqGmWL8", None),
        ("ASCII-Checklisten", "https://www.youtube.com/v/OV38uNb8kwQ&hl=en&fs=1", None),
        ("Legal Assessment", "https://www.youtube.com/v/nglSZPnik2o&hl=en&fs=1", None),  
        ("Feed-Forward-Chat", "https://www.youtube.com/embed/Ee4RwwGuG1E?si=Qs0l-u9R-C6oj4xr", None),
     ],
}

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

def render_new_video_teaser(video_data):
    styles = {
            "container": {
                "max-height": "250px",
                "overflow-y": "auto",
                "padding": "0!important",
                "padding-left":"20px",
                "margin-left":"0px",
                "background-color": "#fff"
            },
            "menu-title": {
                "padding-top": "8px!important",
                "font-family": "Arial",
                "font-size": "14px",
                "font-weight": "600",
                "text-align": "left",
            },
            "menu-icon": {
                "font-size": "18px!important",
            },
            "nav-link": {
                "font-family": "Arial",
                "font-size": "14px",
                "text-align": "left",
                "border-radius":"8px",
                "padding-left": "15px!important",
                "padding-right": "12px!important",
                "--hover-color": "#eee"
            },
            "nav-link-selected": {
                "background-color": st.session_state["button_bg_color"]
            }
        }

    # Initialisiere State nur einmalig
    if "home_video_index" not in st.session_state:
        st.session_state.home_video_index = 0
    if "home_video_label" not in st.session_state:
        st.session_state.home_video_label = list(video_data)[0]
    if "home_video_initialized" not in st.session_state:
        st.session_state.home_video_initialized = False
    if "use_case_video_initialized" not in st.session_state:
        st.session_state.use_case_video_initialized=""
    # === Initialisierung
    if "video_group" not in st.session_state:
        st.session_state.video_group = list(video_data.keys())[0]

    # Achtung: Titel erst NACH dem Setzen von group holen
    if "video_title" not in st.session_state:
        st.session_state.video_title = video_data[st.session_state.video_group][0][0]

    with styled_container("#fff", "#000", "home_video_teaser", "100%", "100%"):
        st.markdown(f"""<p 
                    style="text-align:left; 
                    font-weight: bold; 
                    font-size: 18px; 
                    color: black;">🎬 Videos:
                    </p>""", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])

        with col2:
        # === Menü: Kategorieauswahl
            selected_group = option_menu(
                menu_title="",
                styles=styles,
                options=list(video_data.keys()),
                default_index=list(video_data.keys()).index(st.session_state.video_group),
                key="video_group_selector",
                icons=['house']
            )

            # Fix: wenn Gruppe geändert, setze ersten Titel der neuen Gruppe
            if selected_group != st.session_state.video_group:
                st.session_state.video_group = selected_group
                st.session_state.video_title = video_data[selected_group][0][0]

            group_videos = video_data[st.session_state.video_group]
            titles = [vid[0] for vid in group_videos]

            selected_title = option_menu(
                menu_title="",
                styles=styles,
                options=titles,
                default_index=titles.index(st.session_state.video_title),
                key="video_title_selector",
                icons=['house']
            )
            st.session_state.video_title = selected_title
            # 🛠 CSS-Overflow-Fix
            st.markdown("""
                <style>
                    .st-emotion-cache-1qke9ij {
                        padding: 5px !important;
                     }
                </style>
            """, unsafe_allow_html=True)

        # ✅ Zeige nur dann das erste Video automatisch, wenn noch nicht initialisiert
        st.session_state.video_title = selected_title
        with col1:
            # Video anzeigen
            video_entry = next(v for v in video_data[st.session_state.video_group] if v[0] == st.session_state.video_title)
            st.video(video_entry[1])

            # Optionaler Use Case Link
            if video_entry[2]:
                uc = video_entry[2]
                st.markdown(f"""
                    <p style="margin-top:10px">
                        👉 <a href="?view={uc}" target="_self"><b>Zum passenden Use Case</b></a>
                    </p>
                """, unsafe_allow_html=True)

def render_video_teaser(videos):
    render_new_video_teaser(video_data)

