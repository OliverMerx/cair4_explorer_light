from pylibs.streamlit_lib import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from utils.core.CAIR4_encrypt_manager import encrypt_data  
import random
import re
import html

# === Hilfsfunktion: HTML-sichere Titel erzeugen
def clean_title_for_html(text):
    text = html.escape(text)  # z. B. & → &amp;
    text = text.replace("–", "-")  # Gedankenstrich zu Bindestrich
    text = re.sub(r"[“”„‟’‘‹›]", '"', text)  # typografische Anführungszeichen
    text = re.sub(r"[•→🔹➡️▶️➤🎯🧠📊🔍📂📁📝]", "", text)  # Emojis & Sonderzeichen entfernen
    return text.strip()

# === Stilcontainer für Pills
def styled_container(bg_color, text_color, key, width, height, shadow=True):
    with stylable_container(
        key=f"style_container_{key}",
        css_styles=f"""
            div[data-testid="stVerticalBlock"] {{
                background-color: {bg_color}!important;
                color: {text_color};
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 10px;
                width: {width}!important;
                height: {height}!important;
                box-shadow: {"5px 5px 10px rgba(0, 0, 0, 0.1)" if shadow else "none"};
                overflow-y:auto;
            }}
        """
    ):
        return st.container()

def render_use_case_pills(COLLECTIONS):
    max_pills=10
    available_keys = list(COLLECTIONS.keys())
    max_pills = min(max_pills, len(available_keys))  # Begrenzen auf vorhandene

    # Zufällige Auswahl aus allen Use Cases
    random_keys = random.sample(available_keys, max_pills)
    use_case_titles = [COLLECTIONS[key].get("title", "Unbenannt") for key in random_keys]

    with styled_container("#f8f9fa", "#000", "use_case_container", "fit-content", "100%"):
        st.markdown("<p style='font-weight: bold; font-size: 18px; color: black;'>✈️ Direct Flight:</p>",
                    unsafe_allow_html=True)
        st.markdown("<p style='font-size: 14px; color: black;'>"
                    "Eine zufällige Auswahl von spannenden KI-Use Cases. "
                    "Bei jedem Reload ändert sich die Zusammenstellung!"
                    "</p>", unsafe_allow_html=True)

        pill_html = '<div class="pill-container">'
        for title, key in zip(use_case_titles, random_keys):
            safe_title = clean_title_for_html(title)
            target_url = f"?role={encrypt_data(st.session_state.user_role)}&view={key}"
            pill_html += f"""
                <a href="{target_url}" target="_self" class="pill"
                   style="background-color: {st.session_state.button_bg_color}; 
                          color: {st.session_state.bg_color}; 
                          text-decoration: none;">
                   🔍 {safe_title}
                </a>"""
        pill_html += '</div>'
        st.markdown(pill_html, unsafe_allow_html=True)

        # ✅ CSS für Pills einfügen
        st.markdown("""
            <style>
                .pill-container {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    padding: 10px 5px;
                    justify-content: center;
                }
                .pill {
                    padding: 10px 18px;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: bold;
                    cursor: pointer;
                    text-align: center;
                    white-space: nowrap;
                    transition: all 0.2s ease-in-out;
                }
                .pill:hover {
                    transform: scale(1.05);
                    opacity: 0.9;
                }
            </style>
        """, unsafe_allow_html=True)