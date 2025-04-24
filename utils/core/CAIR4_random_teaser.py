import streamlit as st

# 📌 **Zufälliger Use Case & KI-Modell-Vergleich**
import streamlit as st

def render_random_item(random_key, items, title="📌 Zufällige Auswahl"):
    """
    Erstellt eine Anzeige mit **einem zufälligen Element** aus `items`.

    Parameter:
    - items (list): Liste mit Elementen, die zufällig angezeigt werden.
    - title (str): Überschrift für die Box.
    """

    # ✅ **Session-State für zufällige Auswahl initialisieren**
    if random_key not in st.session_state:
        st.session_state[random_key] = 0

    def next_random_item():
        st.session_state[random_key] = (st.session_state[random_key] + 1) % len(items)

    # 📌 **Anzeige-Container**
    st.markdown("<div class='teaser-container'>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <style>
            .teaser-box {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-top:20px;
                box-shadow: 3px 3px 15px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            .teaser-box:hover {{
                transform: scale(1.03);
                box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.2);
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='teaser-box'><h4>{title}</h4><p>{items[st.session_state[random_key]]}</p></div>", unsafe_allow_html=True)
    
    st.button("🔄 Neues zufälliges Element", key="RandomButton"+random_key, on_click=next_random_item)

    st.markdown("</div>", unsafe_allow_html=True)
