"""
=================================================
CAIR4 Styles Manager
=================================================

Der Styles Manager beinhaltet diverse CSS und dynamische Styleelemente.
Darunter Fullscreen, Logos, Bilder für den Hintergrund und Farben.

Externe Quellen der Anpassung sind das CAIR4_css.json
/assets/css/CAIR4_css.json

Das Base-Theme von Streamlit kann in der "config.toml" angepaßt werden
/Dein Benutzerordner/.streamlit/config.toml 

-> Öffnen über Visual Studio oder anderen Editor, da oft versteckt

###########
# Beispiel:
###########

[theme] wird nicht mehr abgefragt, da Neuladen von Theme stets Verzögerung bewirkt

# Primary accent for interactive elements
primaryColor = '#C03F3B'

# Background color for the main content area
backgroundColor = '#FFF'

# Background color for sidebar and most interactive widgets
secondaryBackgroundColor = '#FFF'

# Color used for almost all text
textColor = '#000'

# Font family for all text in the app, except code blocks
# Accepted values (serif | sans serif | monospace) 
# Default: "sans serif"
font = "sans serif"
##############

"""

from pylibs.streamlit_lib import streamlit as st  
from pylibs.json_lib import json  
from utils.core.CAIR4_logo_manager import set_logo
from utils.core.CAIR4_encrypt_manager import encrypt_data

CSS_COLLECTION={
    "placeholder_logo":"CAIR4_placeholder_logo.png",
    "light_theme":{
        "sidebar_logo":"CAIR4_logo.png",
        "stage_logo":"CAIR4_logo_light_grey.png",
        "text_color": "#000",     
        "background_color": "#fff",
        "header_color":"#203864",
        "field_color":"#f0f0f0",
        "border_color":"#f9f9f9"
    },
    "dark_theme":{
        "sidebar_logo":"CAIR4_logo_white.png",
        "stage_logo":"CAIR4_logo.png",
        "text_color": "#fff",     
        "background_color": "#000",
        "header_color":"#203864",
        "field_color":"#f0f0f0",
        "border_color":"#f9f9f9"
    },
    "button_bg_color":"#8497B0",
    "button_txt_color":"#fff",
    "button_hover_color":"#fff000",
    "background_image": "/assets/images/sky-34536_1280.webp",
    "width":"130",
    "top":"-43",
    "left":"0"
}


def apply_custom_styles():

    """
    #####################################
    # 1. vom Theme abhängige Styleaspekte
    #####################################
    """

    theme = {
        "primaryColor":"#ff4b4b",
        "backgroundColor":"#ffffff",
        "secondaryBackgroundColor":"#f0f2f6",
        "textColor":"#31333F",
        "bodyFont":"'Source Sans Pro', sans-serif",
        "base":"light",
        "fadedText05":"rgba(49, 51, 63, 0.1)",
        "fadedText10":"rgba(49, 51, 63, 0.2)",
        "fadedText20":"rgba(49, 51, 63, 0.3)",
        "fadedText40":"rgba(49, 51, 63, 0.4)",
        "fadedText60":"rgba(49, 51, 63, 0.6)",
        "bgMix":"rgba(248, 249, 251, 1)",
        "darkenedBgMix100":"hsla(220, 27%, 68%, 1)",
        "darkenedBgMix25":"rgba(151, 166, 195, 0.25)",
        "darkenedBgMix15":"rgba(151, 166, 195, 0.15)",
        "lightenedBg05":"hsla(0, 0%, 100%, 1)",
        "font":"'Source Sans Pro', sans-serif",
        }
    
 
    CAIR4_css = CSS_COLLECTION
    
    css_theme="light_theme"

    if "text_color" not in st.session_state:
        st.session_state.text_color = "#FFF"
        st.session_state.header_color = "#FFF"
        st.session_state.bg_color = "#000"
        st.session_state.field_color = "#f9f9f9"
        st.session_state.button_bg_color = "#fff"
        st.session_state.button_txt_color = "#fff"
        st.session_state.button_hover_color = "#fff000"
        st.session_state.popover_visible = True
        st.session_state.popover_x ="130px"
        st.session_state["open_expander"] = False

    st.session_state.text_color = CAIR4_css[css_theme]["text_color"]  # Rote Farbe im Dark Mode
    st.session_state.header_color = CAIR4_css[css_theme]["header_color"]   # Grüne Farbe für Überschriften im Dark Mode
    st.session_state.bg_color = CAIR4_css[css_theme]["background_color"] 
    st.session_state.border_color = CAIR4_css[css_theme]["border_color"] 
    st.session_state.field_color = CAIR4_css[css_theme]["field_color"]
    st.session_state.button_bg_color = CAIR4_css["button_bg_color"]
    st.session_state.button_txt_color = CAIR4_css["button_txt_color"]
    st.session_state.button_hover_color = CAIR4_css["button_hover_color"]

    dialog_styles = {
        "container": {
            "max-height": "350px",
            "overflow-y": "auto",
            "padding": "0!important",
            "background-color": "#fafafa"
        },
        "menu-title":{
            "padding-top":"8px!important",
            "font-family":"Arial",
            "font-size": "14px",
            "font-weight": "600",
            "text-align": "left",
        },
        "menu-icon": {
            "font-size": "18px!important",
            }, 
        "nav-link": {
            "font-family":"Arial",
            "font-size": "14px",
            "text-align": "left",
            "margin-left": "-10px",
            "--hover-color": "#eee"
        },
        "nav-link-selected": {
            "background-color": st.session_state["button_bg_color"]
        }
    }
    
    if "dialog_colors" not in st.session_state:    
        st.session_state["dialog_colors"] = dialog_styles
    
    # Wende die Farbe auf den gesamten Text an
    st.markdown(f"""
        <style>
            /* Standard Textfarbe */
            .stMarkdown p, .stText {{
                color: {st.session_state.text_color} !important;
            }}           
            /* Farbe für Überschriften */
            h1, h2, h3, h4, h5, h6 {{
                color: {st.session_state.header_color} !important;
            }}
        </style>
        """, unsafe_allow_html=True)
    
    # Custom CSS für Top-Navigation
    st.markdown(
        f"""
        <style>
        .st-bw, .st-bv{{
            border-color: {st.session_state.border_color}!important;
            }}
        .st-bu{{
            border-style:solid!important;
            border-width:1px!important;
            border-color:#f0f0f0!important;/*Aktivitätsanzeigen
        }}
        .st-bc {{
            }}
        .stChatInput,.stChatInputFileUp, .stChatInput > input{{
            border-color: {st.session_state.header_color}!important;
            border-width: 1px;
            border-style: solid;
            background-color:{st.session_state.field_color}!important;
            border-radius: 100px;
        }}
        .streamlit-expander{{
            border-color: {st.session_state.border_color}!important;
            background-color:{st.session_state.field_color}!important;;
        }}
        div.stButton button{{
            border-color: {st.session_state.border_color}!important;
            background-color:{st.session_state.field_color}!important;
        }}
        input{{
            background-color: {st.session_state.field_color}!important;
            color: #000 !important;
        }}

        .st-emotion-cache-2dmq9c{{
            color: #000 !important;
        }} 
        textarea {{
            background-color:{st.session_state.field_color}!important;;
            color: #000 !important;
            border-style:solid!important;
            border-width:1px!important;
            border-color:{st.session_state.border_color}!important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    """
    #######################################
    # 2. vom Theme unabhängige Styleaspekte
    #######################################
    """

    st.session_state.background_image = CAIR4_css["background_image"] 
    sidebar_logo=st.session_state.base_path + "/assets/logos/"+CAIR4_css[css_theme]["sidebar_logo"]
    stage_logo=st.session_state.base_path + "/assets/logos/"+CAIR4_css[css_theme]["stage_logo"]
    placeolder_logo=st.session_state.base_path + "/assets/logos/"+CAIR4_css["placeholder_logo"]


    # Header-Visibility und Sidebar
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
            }
            
            section[data-testid="stSidebar"] div.stButton button {
                width:100%!important;
            }
            div[data-testid="stPopover"]>div>button {
                width:100%!important;
                height: 30px;
            }
            /* Hide the Streamlit header and menu / Fullscreen */
            header {visibility: hidden;}  
            /* Optionally, hide the footer */
            .streamlit-footer {display: none;}
            /* Hide your specific div class, replace class name with the one you identified */
            .st-emotion-cache-uf99v8 {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
        <style>
            body, html, .stApp {
                font-family: 'Arial', sans-serif; /* Hier kannst du eine andere Schrift setzen */
                background-color:{st.session_state.bg_color};
                background-image: linear-gradient(45deg, {st.session_state.bg_color},{st.session_state.bg_color});

            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <html>
            <head>
                <style>
                    ::-webkit-scrollbar {
                        width: 10px;
                        }

                        /* Track */
                        ::-webkit-scrollbar-track {
                        background: #f1f1f1;
                        }

                        /* Handle */
                        ::-webkit-scrollbar-thumb {
                        background: #888;
                        }

                        /* Handle on hover */
                        ::-webkit-scrollbar-thumb:hover {
                        background: #555;
                        }
                    </style>
                </head>
            <body>
            </body>
        </html>
    """, unsafe_allow_html=True)
        
    st.markdown("""
        <style>
            div[data-testid="stMainBlockContainer"]{
                margin-bottom: -1rem;
                margin-top: -210px!important;
            }
            div[data-testid="stVerticalBlockBorderWrapper"]:has(div.element-container > div.stHtml > span.st_theme_None) {
                margin-bottom: -1rem;
                margin-top: -170px!important;
            }
            .st-emotion-cache-16tyu1 h3{
               
            }
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <style>
            div[data-testid="stPopover"],.st-emotion-cache-qsto9u {{     
                justify-content:left!important;
            }}
            div[data-testid="stPopoverBody"] {{ 
                transform: translateY(20px) !important;
                bottom: auto !important;
                top: 150px!important;
                visibility: {"visible" if st.session_state.popover_visible else "hidden"} !important; 
                left: {st.session_state.popover_x};
                max-height: 230px!important;
            }}
            /*Buttons in PopOver*/
            .st-emotion-cache-1rcp478, .st-emotion-cache-qsto9u{{
                justify-content: left;
                /*color: {st.session_state.button_txt_color}!important;*/
                /*background-color:{st.session_state.button_bg_color}!important;*/             
                width:100%;
            }}
            /*Link-Button*/
            .st-emotion-cache-consg2 {{ 
                padding: 10px;
            }}
            /*Help-Button*/
            .st-emotion-cache-zaw6nw, .st-emotion-cache-qsto9u {{ 
                min-width:10vh;
                justify-content:center!important;
                background-color:#f9f9f9;            
            }}
            .stButton > button {{ 
                width: 100% !important; /* Maximale Breite in Container setzen */
                min-width: auto !important; /* Verhindert erzwungene Mindestbreite */
                background-color: {st.session_state.button_bg_color}!important;
                color: {st.session_state.button_txt_color}!important;
            }}    
            /* Iconhintergrund für Sidebar */
            .st-emotion-cache-l1ktzw {{ 
            background-color:rgb(240,240,240,0.5)!Important;
            }}
            div[class*="stTabs"] button {{ 
                background-color:rgb(240,240,240,0.5)!Important;
                height:30px!important;
                font-size:15px!important;
            }}
            div[class*="stTabs"] button p{{ 
                font-size:15px!important;
            }}
        </style>
        """,
    unsafe_allow_html=True
    )

    # durchsichtiger Logo-Platzhalter, da kein Home-Button bei st.logo() in Sidebar, aber Logo für Stage

    st.logo(placeolder_logo, size="large", icon_image=stage_logo) 

    # Finales Logo für die Sidebar
    with st.sidebar:
        pre_key = encrypt_data(st.session_state.user_role)
        home_url="?role="+pre_key+"&view="

        set_logo(sidebar_logo, target_url=home_url, width=CAIR4_css["width"], top=CAIR4_css["top"],left=CAIR4_css["left"])

