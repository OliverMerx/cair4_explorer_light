"""
=================================================
🧾 CAIR4 Halluzination
=================================================

"""

import streamlit as st
from PIL import Image
from pathlib import Path

# === CAIR4 Setup-Header (für UI-Kompatibilität) ===
def render_muenchhausen_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)

    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    hal1_path = Path("assets/images/muenchhausen1.png")
    hal2_path = Path("assets/images/muenchhausen2.png")

    # === Prüfen, ob beide Dateien vorhanden sind
    if not hal1_path.exists() or not hal2_path.exists():
        st.error("❌ Beide Bilddateien müssen vorhanden sein: `muenchhausen1.png` und `muenchhausen.png`.")

    # === Bilder laden
    hal1_img = Image.open(hal1_path)
    hal2_img = Image.open(hal2_path)

    # === Darstellung
    st.write("Die folgende Ansicht zeigt zwei Varianten des Muenchhausen-Phänomens. Oben mehrfache falsche Verwenden eines Codes. Darunter die Fortsetzung, die auch nach dem 5. Versuch immer noch falsch war, aber als richtig dargestellt wurde.")

    with st.expander("Falsche Überarbeitung  von Code mit behaupteter Richtigkeit - Teil 1", expanded=True):
        st.image(hal1_img)

    with st.expander("Falsche Überarbeitung von Code mit behaupteter Richtigkeit - Teil 2", expanded=True):
        st.image(hal2_img)


