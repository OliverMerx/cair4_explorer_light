# =============================================
# 📊 CAIR4 EHR_Diagnosis_Analytics View (Standalone + Stitcher)
# =============================================

"""
📌 Beschreibung:
Analysiert medizinische PDFs automatisch mithilfe von GPT-4 und extrahiert relevante Diagnosen zur grafischen Auswertung.

✅ Funktionen:
- PDF-Upload & Textextraktion
- GPT-gestützte Diagnosenanalyse
- Heatmap: Dokument vs. Diagnose
- Wortwolke & Balkendiagramm
- Diagnosen-Tabelle

✅ Unterstützt Explorer UND Stitcher
"""

# === 📦 Imports ===
try:
    import pylibs.streamlit_lib.streamlit as st
except ImportError:
    import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymupdf as fitz
from wordcloud import WordCloud

from controllers.CAIR4_controller import handle_query
from utils.core.CAIR4_debug_utils import DebugUtils

# === Diagnoseanalyse via GPT ===
def analyze_diagnoses(text, model_name, use_case, context):
    prompt = f"""
Extrahiere alle medizinisch relevanten Diagnosen aus folgendem Text.
Gib nur die wichtigsten Krankheitsnamen als Liste mit Komma getrennt zurück.

Text:
{text}
"""
    try:
        response, *_ = handle_query(
            query=prompt,
            model_name=model_name,
            use_case=use_case,
            context=context,
        )
        return [diag.strip() for diag in response.replace("\n", ",").split(",") if len(diag.strip()) > 2]
    except Exception as e:
        st.error(f"❌ Fehler bei Diagnoseanalyse: {e}")
        return []

# === PDF-Text extrahieren ===
def extract_text_from_pdf(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        DebugUtils.debug_print(f"PDF-Fehler: {e}")
        return ""

# === Visualisierung ===
def display_diagnosis_visuals(doc_diagnoses, all_diagnoses):
    if not all_diagnoses:
        st.warning("Keine Diagnosen erkannt.")
        return

    st.markdown("## 🧠 Dokument-Diagnose-Heatmap")
    df = pd.DataFrame(0, index=doc_diagnoses.keys(), columns=list(set(all_diagnoses)))
    for doc, diags in doc_diagnoses.items():
        for d in diags:
            df.loc[doc, d] += 1

    fig, ax = plt.subplots(figsize=(10, len(df)*0.6 + 2))
    sns.heatmap(df, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
    st.pyplot(fig)

    st.markdown("## ☁️ Häufigste Diagnosen")
    wc_text = " ".join(all_diagnoses)
    wc = WordCloud(width=800, height=300, background_color='white').generate(wc_text)
    st.image(wc.to_array())

    st.markdown("## 📄 Diagnoseliste je Dokument")
    table_df = pd.DataFrame.from_dict(doc_diagnoses, orient="index").transpose()
    st.dataframe(table_df.fillna(""))

    st.markdown("## 📊 Häufigkeit der Diagnosen")
    diag_series = pd.Series(all_diagnoses).value_counts()
    st.bar_chart(diag_series)

# === 1️⃣ Standalone View ===
def render_ehr_document_search_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):

    st.subheader(title)
 
    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    uploaded_files = st.file_uploader("📄 Lade medizinische PDFs hoch", type=["pdf"], accept_multiple_files=True)
    if not uploaded_files:
        st.info("Bitte mindestens ein PDF hochladen.")
        return

    docs = []
    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        docs.append({"filename": file.name, "anonymized_text": text})

    doc_diagnoses = {}
    all_diagnoses = []
    for doc in docs:
        with st.spinner(f"Analysiere {doc['filename']}..."):
            diags = analyze_diagnoses(doc["anonymized_text"], model_name, use_case, context)
            doc_diagnoses[doc["filename"]] = diags
            all_diagnoses.extend(diags)

    display_diagnosis_visuals(doc_diagnoses, all_diagnoses)

# === 2️⃣ Stitcher-Kompatibilität ===
def run_step(context):

    if not hasattr(context, "original_files") or not hasattr(context, "anonymized_data"):
        st.warning("❌ Kontext unvollständig.")
        return context

    if not context.anonymized_data:
        st.warning("⚠️ Bitte zuerst die Anonymisierung durchführen.")
        return context

    doc_diagnoses = {}
    all_diagnoses = []

    for file, text in zip(context.original_files, context.anonymized_data):
        name = getattr(file, "name", "Unbekannt")
        with st.spinner(f"Analysiere {name}..."):
            diags = analyze_diagnoses(text, model_name="gpt-4", use_case="ehr_diagnosis_analytics", context={})
            doc_diagnoses[name] = diags
            all_diagnoses.extend(diags)

    context.analysis_result = doc_diagnoses
    display_diagnosis_visuals(doc_diagnoses, all_diagnoses)
    return context
