"""
=================================================
🧾 CAIR4 Halluzination
=================================================

"""

import streamlit as st
from PIL import Image
from pathlib import Path

# === CAIR4 Setup-Header (für UI-Kompatibilität) ===
def render_hallucination_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)

    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    hal1_path = Path("assets/images/halluzination_hochzeit.png")
    hal2_path = Path("assets/images/halluzination_recht.png")

    # === Prüfen, ob beide Dateien vorhanden sind
    if not hal1_path.exists() or not hal2_path.exists():
        st.error("❌ Beide Bilddateien müssen vorhanden sein: `hallunzination_hochzeit.png` und `halluzination_recht.png`.")

    # === Bilder laden
    hal1_img = Image.open(hal1_path)
    hal2_img = Image.open(hal2_path)

    # === Darstellung
    st.write("Die folgende Ansicht zeigt zwei Varianten von Halluzinationen. Oben das falsche Datum einer historischen Hochzeit. Darunter die Zuordnung von Artikeln des EU AI Acts zu einem falschen Kontext. Beides Halluziinationen, die so definitiv nicht zutreffen, aber auch schwer erkennbar sind.")

    with st.expander("Falsches Hochzeitsdatum der Hochzeit von Maria Theresia", expanded=True):
        st.image(hal1_img)

    with st.expander("Falsche Zurordnung von Artikeln des EU AI Acts", expanded=True):
        st.image(hal2_img)


