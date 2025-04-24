"""
=================================================
🧾 CAIR4 Bildvergleichs-View: Kassenbon Original vs. Fake
=================================================

📌 **Beschreibung:**
Dieses Modul visualisiert und vergleicht zwei Kassenbon-Bilder: ein echtes Original und ein manipuliertes Fake-Dokument.

🎯 **Hauptfunktionen:**
- Zeigt beide Belege nebeneinander in Expandern
- Standardmäßig ist das Fake-Dokument geöffnet
- Vorbereitung für weiterführende Bildanalyse (z. B. OCR, Pixelvergleich etc.)
"""

import streamlit as st
from PIL import Image
from pathlib import Path

# === CAIR4 Setup-Header (für UI-Kompatibilität) ===
def render_fake_compare_generator_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)

    with st.expander("**Use Case Beschreibung**"):
        st.write(description)


    original_path = Path("assets/images/kassenbon.jpg")
    fake_path = Path("assets/images/kassenbon_fake.jpg")

    # === Prüfen, ob beide Dateien vorhanden sind
    if not original_path.exists() or not fake_path.exists():
        st.error("❌ Beide Bilddateien müssen vorhanden sein: `kassenbon.jpg` und `kassenbon_fake.jpg`.")

    # === Bilder laden
    original_img = Image.open(original_path)
    fake_img = Image.open(fake_path)

    # === Darstellung
    st.write("Die folgende Ansicht zeigt zwei Versionen eines Kassenbons. Das manipulierte Dokument ist zur Ansicht geöffnet.")

    with st.expander("🧾 Gefälschtes Dokument (Fake)", expanded=True):
        st.image(fake_img, caption="💡 Manipulierte Version (Fake)")

    with st.expander("📄 Originaldokument (Echt)", expanded=False):
        st.image(original_img, caption="✅ Originalbeleg")


