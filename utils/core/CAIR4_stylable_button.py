"""
=================================================
CAIR4 Stylable Button
=================================================

Erstellt einen Streamlit-Button mit anpassbarem Styling.
Mit der Verwendung/Ausführung können jedoch Konflikte mit anderen Funktionen entstehehn.

    Parameter:
    - label (str): Der Button-Text.
    - bg_color (str): Hintergrundfarbe des Buttons.
    - text_color (str): Schriftfarbe.
    - key (str): Eindeutiger Streamlit-Key.
    - width (str): Breite des Buttons (z. B. "150px", "100%").
    - height (str): Höhe des Buttons (z. B. "50px", "auto").
    - text_align (str): Text-Ausrichtung ("left", "center", "right").
    - font_size (str): Schriftgröße (z. B. "12px", "16px").

if stylable_button(use_case, st.session_state.header_color, "#ffffff", f"btn_{use_case}", "100%", "20px","left", "12"):
    -> Funktion
"""
from pylibs.streamlit_lib import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def stylable_button(label, bg_color, text_color, key, width="100%", height="auto", text_align="center", font_size="14px",disabled=False):

    # 🎯 Fix für Textausrichtung mit `display: flex`
    justify_content = {
        "left": "flex-start",
        "center": "center",
        "right": "flex-end"
    }.get(text_align, "center")  # Falls falscher Wert → Standard: center

    with stylable_container(
        key=f"style_button_{key}",
        css_styles=f"""
            div[data-testid="stButton"] button, div[data-testid="stPopoverBody"] button:first-child {{
                background-color: {bg_color} !important;
                color: {text_color} !important;
                border: none;
                width: {width} !important;
                height: {height} !important;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
                cursor: pointer;
                /* 🎯 Fix für Text-Ausrichtung */
                display: flex !important;
                align-items: center !important;
                justify-content: {justify_content} !important;
            }}
        """
    ):
        return st.button(label, key=key, disabled=disabled)
    
def stylable_button_light(label, color1, color2, color3, key, disabled):
    with stylable_container(
            key=f"style_button_{key}",
            css_styles=f"""
                button {{
                    background-color: {color1}!important;
                    border-color: {color3}important;
                    color: {color2}important;
                    width: fit-content;
                    padding: 10px;
                    border-radius: 10px;
                    font-weight: bold;
                    cursor: pointer;
                 }}
                button:hover:enabled {{
                    filter: brightness(1.2);
                }}
                button:disabled {{
                    opacity: 0.6;
                    cursor: not-allowed !important;
                    filter: none !important;
                }}

            """
        ):
        return st.button(label, key=key, disabled=disabled)  # Dynamischer Key für Konfliktvermeidung

