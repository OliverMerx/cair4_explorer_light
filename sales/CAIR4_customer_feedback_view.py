import streamlit as st
import plotly.express as px
import pymupdf as fitz

from utils.core.CAIR4_log_manager import add_log_entry
from utils.use_cases.CAIR4_sentiment_analysis import analyze_structured_sentiment
from utils.use_cases.CAIR4_sentiment_viz import render_sentiment_results
from utils.use_cases.CAIR4_sentiment_json_parser import clean_json_response

# === 1️⃣ PDF-Text extrahieren ===
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text("text") for page in doc)
    return text if text.strip() else None

# === 2️⃣ Kundenfeedback View ===
def render_customer_feedback_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)

    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    log_file = f"data/{use_case}_logs.json"
    add_log_entry(log_file, {"action": "view_rendered", "details": {"view": "customer_feedback_analysis"}})

    # PDF-Upload
    uploaded_file = st.file_uploader("📄 Lade eine PDF-Datei hoch", type=["pdf"])

    if uploaded_file is not None:
        extracted_text = extract_text_from_pdf(uploaded_file)
        if extracted_text:
            st.success(f"✅ Datei '{uploaded_file.name}' erfolgreich verarbeitet.")
    else:
        extracted_text = None

    if extracted_text:
        st.markdown("### Gewichtung der Sentimentanalyse")
        with st.expander("Einstellungen:"):
            st.slider("Gewichtung Positiv", 0.5, 2.0, 1.0, 0.1)
            st.slider("Gewichtung Neutral", 0.5, 2.0, 1.0, 0.1)
            st.slider("Gewichtung Negativ", 0.5, 2.0, 1.0, 0.1)

        try:
            with st.expander("**Gesprächsinhalt:**"):
                st.write(extracted_text)
        except:
            pass

        result, error = analyze_structured_sentiment(
            extracted_text,
            model_name=st.session_state.selected_model,
            use_case="sentiment_analysis"
        )

        if result:
            st.json(result)
            render_sentiment_results(result)
        else:
            st.error(f"❌ Analysefehler: {error}")
    else:
        st.info("Bitte lade eine PDF hoch.")
