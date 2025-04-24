import streamlit as st
from utils.core.CAIR4_encrypt_manager import encrypt_data
from streamlit.components.v1 import html as st_html
from streamlit_extras.stylable_container import stylable_container
from PIL import Image
import base64
from io import BytesIO

# === Stilcontainer
def styled_container(bg_color, text_color, key, width, height, shadow=True):
    with stylable_container(
        key=f"journey_style_container_{key}",
        css_styles=f"""
            div[data-testid="stVerticalBlock"] {{
                background-color: {bg_color}!important;
                color: {text_color};
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 50px;
                width: {width}!important;
                height: {height}!important;
                box-shadow: {"5px 5px 10px rgba(0, 0, 0, 0.1)" if shadow else "none"};
                overflow-y:auto;
            }}
        """
    ):
        return st.container()

# === Bild in base64 konvertieren
def get_base64_image(path, size):
    try:
        img = Image.open(path)
        img = img.resize(size)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Fehler beim Laden des Bildes: {e}")
        return ""

# === Journey-Teaser
def render_home_journey_teaser():
    with styled_container("#f8f9fa", "#000", "use_case_container", "100%", "100%"):
        st.markdown("<p style='font-weight: bold; font-size: 18px; color: black;'>🌍 Use Case Journey (Beispiel):</p>",
                    unsafe_allow_html=True)
        st.markdown("<p style='font-size: 14x; color: black;'>" \
        "Auf dieser KI-Reiseroute für KI-Einsteiger lernst und erlebst Du interaktiv wichtige Prinzipen der KI inklusive der dazugehörigen Begriffe!" \
        "Beachte, dass die einzelnen Use Cases bei einem Klick in einem neuen Browserfenster geöffnet werden. So kannst Du alle Steps nach und nach erforschen.</p>",
                    unsafe_allow_html=True)
        # Pfeile laden
        arrow_down = get_base64_image("assets/arrows/arrow_long_down_blue.png", (50, 80))
        arrow_up = get_base64_image("assets/arrows/arrow_medium_up_orange.png", (50, 80))
        arrow_curve_bottom_right = get_base64_image("assets/arrows/arrow_left_up_orange.png", (40, 40))
        arrow_curve_top_left = get_base64_image("assets/arrows/arrow_top_right_orange.png", (60, 80))
        pre_key = encrypt_data(st.session_state.user_role)

        # Use Case Steps
        steps_left = [
            ("🧩 KI-System", "Stateless Chat", "KI-System"),
            ("🧠 GPAI-Modell", "Modellvergleich", "KI-Modell-Vergleich"),
            ("💬 Prompting", "Typen und Techniken", "Prompting-Typen"),
            ("📐 Vektorisierung", "Prompt-Analyse", "Vektorisierung"),
            ("🔤 Tokenisierung", "Token Visualizer", "Token-Verständnis"),
            ("⚖️ Modellvergleich", "Tokenisierung", "Token-Vergleich"),
            ("📈 Ableitung", "Autonome Entscheidung", "Ableitung"),
        ]

        steps_right = [
            ("🔢 Wahrscheinlichkeit", "Antwortwahrscheinlichkeit", "Wahrscheinlichkeiten"),
            ("🤯 Halluzinationen", "Fehlinterpretation", "Halluzinationen"),
            ("⚙️ KI vs. Regeln", "Vergleichs-Engine", "Regelbasiertes-System"),
            ("🎚 Prompt-Einstellungen", "Parameter testen", "Prompt-Einstellungen"),
            ("🧠 Session Memory", "Langzeitgedächtnis", "Chat-mit-Sessiongedächtnis"),
            ("🌐 Kontext", "Kontextvergleich", "Kontext-Chat"),
        ]

        html = f"""
        <style>
        .journey-layout {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 30px;
        }}
        .journey-column {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .step-card {{
            background: linear-gradient(145deg, #ffffff, #f3f3f3);
            border: 1px solid #ccc;
            border-radius: 12px;
            padding: 15px;
            width: 220px;
            text-align: center;
            margin: 5px 0;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.07);
            transition: transform 0.2s ease;
        }}
        .step-card:hover {{
            transform: scale(1.03);
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .step-card a {{
            text-decoration: none;
            color: inherit;
        }}
        .arrow-img {{
            margin: 5px 0;
            width: 50px;
            height: 80px;
        }}
        .arrow-up {{
            margin: 25px 0; /* 👉 Größerer Abstand */
            width: 30px;
            height: 80px;
            margin-bottom:52px;
        }}
        .arrow-top {{
            margin-top: 25px;
            margin-bottom: 35px;
            margin-left:35px;
            width: 60px;
            height: 40px;
        }}
        .arrow-bottom {{
            margin-top: 25px;
            margin-bottom: 35px;
            margin-left:-15px;
            width: 60px;
            height: 40px;
        }}
        .spacer {{
            height: 60px;
            width: 100%;
        }}
        </style>

        <div class="journey-layout">
        """

        # === Column 1 (Links)
        html += '<div class="journey-column">'
        for i, (title, subtitle, view) in enumerate(steps_left):
            html += f"""
            <div class="step-card">
                <a href="?role={pre_key}&view={view}" target="_blank">
                    <div style='font-family:Arial;font-size:1.1em'><strong>{title}</strong></div>
                    <div style='font-family:Arial;font-size:0.85em; color:#666;'>{subtitle}</div>
                </a>
            </div>
            """
            if i < len(steps_left) - 1:
                html += f'<img class="arrow-img" src="data:image/png;base64,{arrow_down}" />'
        html += '</div>'

        # === Column 2 (Mittig) – Pfeile nach oben inkl. Kurven
        html += '<div class="journey-column">'

        # Oben: Kurvenpfeil von links oben nach rechts unten
        html += f'<img class="arrow-top" src="data:image/png;base64,{arrow_curve_top_left}" />'

        # Mittlere Pfeile nach oben mit großem Abstand
        for _ in range(len(steps_left) - 1):
            html += f'<img class="arrow-up" src="data:image/png;base64,{arrow_up}" />'

        # Unten: Kurvenpfeil von links unten nach rechts oben
        html += f'<img class="arrow-bottom" src="data:image/png;base64,{arrow_curve_bottom_right}" />'
        html += '</div>'

        # === Column 3 (Rechts)
        html += '<div class="journey-column">'
        for i, (title, subtitle, view) in enumerate(steps_right):
            html += f"""
            <div class="step-card">
                <a href="?role={pre_key}&view={view}" target="_blank">
                    <div style='font-family:Arial; font-size:1.1em'><strong>{title}</strong></div>
                    <div style='font-family:Arial; font-size:0.85em; color:#666;'>{subtitle}</div>
                </a>
            </div>
            """
            if i < len(steps_right) - 1:
                html += f'<img class="arrow-img" src="data:image/png;base64,{arrow_down}" />'
        html += '</div>'

        # === Layout abschließen
        html += '</div>'
        # === Anzeige in Streamlit
        st_html(html, height=1200)