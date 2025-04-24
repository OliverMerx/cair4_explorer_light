"""
=========================================
CAIR4 Logo Manager
=========================================

Dieses Skript ist erforderlich, da die von Streamlit verwendete Funktion st.logo() immer ein sepates Browser-Tab
öffnet, wenn das Logo angeklickt wird. Um dieses Verhalten zu umgehen, wird ein benutzerdefiniertes Logo-Element
erstellt, das in Streamlit eingebettet wird und die Logo-URL im Sinne eines Home-Buttonsmit "_self" statt "_blank" öffnet. 

"""

# === 1️⃣ Importiere erforderliche Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.base64_lib import base64

# === 🔧 Funktion zum Codieren eines Bildes als Base64 ===
def encode_image(image_path):
    """Codiert ein Bild zu Base64 für die Anzeige in Streamlit."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# === 🎨 Setzt das Logo mit Link als Streamlit-Komponente ===
def set_logo(image_path, target_url="/", width="91", top="-38", left="0"):
    """
    Erstellt ein klickbares Logo in Streamlit mit einer anpassbaren URL.

    Args:
        image_path (str): Pfad zum Logo-Bild.
        target_url (str): Home als Ziel-URL für den Klick.
        width (int): Breite des Logos in Pixel.
    """
    encoded_logo = encode_image(image_path)
    st.markdown(f"""
        <style>
            .custom-logo-container {{
                width:{width}px;
                text-align: left; 
                margin-bottom: 20px;
                margin-top:{top}px;
                margin-left:{left}px;
            }}
            .custom-logo-container img {{
                cursor: pointer;
                margin-top:{top}px;
                margin-left:{left}px;
            }}
            .custom-logo-container img:hover {{
                transform: scale(1.05);
                margin-top:{top}px;
                margin-left:{left}px;
            }}
        </style>

        <div class="custom-logo-container">
            <a href="{target_url}" target="_self">
                <img src="data:image/png;base64,{encoded_logo}"  alt="Custom Logo">
            </a>
        </div>
    """, unsafe_allow_html=True)