from pylibs.streamlit_lib import streamlit as st
from pylibs.base64_lib import base64
from pylibs.random_lib import random
from utils.core.CAIR4_background_image_util import set_new_background
from utils.core.CAIR4_encrypt_manager import encrypt_data
import importlib.util

def number_to_word_de(n):
    number_map = {
        0: "null", 1: "eins", 2: "zwei", 3: "drei", 4: "vier",
        5: "fünf", 6: "sechs", 7: "sieben", 8: "acht", 9: "neun"
    }
    return number_map.get(n, str(n))

def is_view_available(view_path: str) -> bool:
    try:
        module_name, _ = view_path.rsplit(".", 1)
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except:
        return False

def render_chapter_overview(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    chapter_name = context
    collections = collection

    set_new_background(False)

    st.markdown(f"""
        <style>
            .chapter-title {{
                font-size: 40px!important;
                font-weight: bold;
                width: fit-content;
                color: {st.session_state.header_color};
                margin-bottom: 30px;
                padding-left: 20px!important;
                padding-right: 20px;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
                background-color: {st.session_state.bg_color};
                margin-top:-88px;
            }}
            .chapter-description, .light_info {{
                font-size: 18px!important;
                font-weight: bold;
                width: fit-content;
                max-width:90%;
                color: {st.session_state.header_color};
                margin-bottom: 30px;
                padding-left: 20px!important;
                padding-right: 20px;
                padding-top:10px;
                padding-bottom:10px;
                background-color: {st.session_state.bg_color};
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
                margin-top: 10px;
                border-radius:8px;
            }}
        </style>
    """, unsafe_allow_html=True)
    
    light_info = "✅ In Light-Version enthalten – 🚫 Nur Beschreibung in Light-Version verfügbar."

    st.markdown(f"<div class='chapter-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chapter-description'>{description}<br/><br/>{light_info}</div>", unsafe_allow_html=True)

    # === Nur echte Use Cases (mit order > 0)
    use_cases_all = [d for d in collections.values() if d['chapter'] == chapter_name]
    real_use_cases = [d for d in use_cases_all if d.get("order", 0) > 0]
    shuffle_use_cases = real_use_cases[1:]
    random.shuffle(shuffle_use_cases)
    columns = st.columns(2)

    for idx, use_case in enumerate(shuffle_use_cases):
        view_path = use_case.get("view", "")
        is_real = is_view_available(view_path)

        icon = "✅" if is_real else "🚫"
        uc_key = next((k for k, v in collections.items() if v == use_case), None)
        pre_key = f"?role={encrypt_data(st.session_state.user_role)}&view="
        use_case_key = pre_key + uc_key if uc_key else "#"

        link_text = "🔍 Use Case öffnen" if is_real else "Use Case Beschreibung öffnen"

        with columns[idx % 2]:
            with st.container():
                st.markdown(f"""
                    <div style="
                        background-color: white;
                        border-radius: 8px;
                        padding: 20px;
                        margin-bottom: 20px;
                        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
                    ">
                        <h3 style="color: {st.session_state.header_color}; margin-bottom: 10px;">{icon} {use_case['title']}</h3>
                        <p style="color: {st.session_state.text_color};">{use_case['description'][:150]}...</p>
                        <a href="{use_case_key}" target="_self" style="color: blue; font-weight: bold; text-decoration: none;">{link_text}</a>
                    </div>
                """, unsafe_allow_html=True)