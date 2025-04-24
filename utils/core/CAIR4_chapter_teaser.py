import streamlit as st
from pylibs.base64_lib import base64

import re

# === Zahl in deutsches Wort ===
def number_to_word_de(n):
    number_map = {
        0: "null", 1: "eins", 2: "zwei", 3: "drei", 4: "vier",
        5: "fünf", 6: "sechs", 7: "sieben", 8: "acht", 9: "neun",
        10: "zehn", 11: "elf", 12: "zwölf"
    }
    return number_map.get(n, str(n))

# === Kapitelnummer extrahieren ===
def extract_chapter_number(label):
    match = re.match(r"(\d+)", label)
    return int(match.group(1)) if match else 999

# === Kapitel-Kacheln anzeigen ===
def render_chapter_teaser(collections):
    st.markdown("""
        <style>
        .chapter-box {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
        }
        .chapter-title {
            font-size: 26px;
            font-weight: bold;
            color: #003366;
            margin-bottom: 10px;
        }
        .chapter-desc {
            font-size: 16px;
            color: #333333;
        }
        .chapter-link {
            color: #004488;
            font-weight: bold;
            text-decoration: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # Kapitel nach Nummer sortieren
    sorted_chapters = sorted(collections.items(), key=lambda x: extract_chapter_number(x[0]))
    cols = st.columns(2)
    col_index = 0

    for chapter_name, chapter_data in sorted_chapters:
        use_cases = chapter_data.get("use_cases", {})
        use_case_list = list(use_cases.values())
        if not use_case_list:
            continue

        intro_uc = use_case_list[0]  # Annahme: erstes Element = Kapitelintro
        title = intro_uc.get("title", chapter_name)
        description = intro_uc.get("description", "")

        # Anzahl Use Cases (abzgl. Intro)
        total_ucs = len([uc for uc in use_case_list if uc.get("order", 1) > 0]) - 1
        total_text = f"Anzahl der Use Cases: {number_to_word_de(total_ucs)}"

        # Kapitel-URL (Basierend auf View-Key)
        view_key = None
        for k, v in use_cases.items():
            if v.get("view", "").endswith("render_chapter_overview"):
                view_key = v.get("name", None)
                break

        if not view_key:
            continue
        link = f"?view={view_key}"

        with cols[col_index]:
            st.markdown(f"""
                <div class='chapter-box'>
                    <div class='chapter-title'>{title}</div>
                    <div class='chapter-desc'>{description}</div>
                    <div style='margin-top:8px; font-size:14px;'>{total_text}</div>
                    <a class='chapter-link' href="{link}">Kapitel öffnen →</a>
                </div>
            """, unsafe_allow_html=True)
        col_index = (col_index + 1) % 2