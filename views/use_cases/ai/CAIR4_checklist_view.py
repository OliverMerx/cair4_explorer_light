"""
=================================================
📋 CAIR4 Checklisten-Generator View (Finale Version)
=================================================

📌 **Beschreibung:**
Dieser View ermöglicht das **Generieren von interaktiven Checklisten** aus hochgeladenen Dokumenten.
- **Upload direkt im Haupt-View** und **Text-Anzeige nach Upload**.
- **Checklisten mit interaktiven Checkboxen und To-Do-Listen**.
- **Struktur und UI beibehalten**, aber nach **neuem CAIR4-Standard** umgesetzt.

🎯 **Funktionen:**
- **UploadView direkt im Hauptbereich.**
- **Text-Anzeige und interaktive Checklisten** mit Checkboxen.
- **Sauberes Prompt-Handling** mit konsistentem **CAIR4-Standard**.
- **pylibs und DebugUtils** für Digital Twin-Kompatibilität.

=================================================
"""

## === 📚 Importe ===
from pylibs.os_lib import os as os
from pylibs.json_lib import json as json
from pylibs.streamlit_lib import streamlit as st
from pylibs.pandas_lib import pandas as pd
from pylibs.re_lib import re as re
from pylibs.bleach_lib import bleach
from pylibs.tika_lib import tika
from pylibs.tika_parser_lib import parser
from pylibs.datetime_lib import datetime as datetime

# utils
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_metrics_manager import initialize_metrics, update_metrics
from utils.core.CAIR4_log_manager import add_detailed_log

# controllers
from controllers.CAIR4_controller import handle_query

import pymupdf as fitz


tika.initVM()  # Initialize the Tika JVM (do this only once)

def extract_text_from_pdf(pdf_file):
    try:
        # First, try PyMuPDF (fitz)
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = "\n".join(page.get_text("text") for page in doc)
        if text.strip():  # Check for empty or whitespace-only text
            return text

        # If PyMuPDF fails, try Tika as a fallback
        pdf_file.seek(0)  # Reset file pointer for Tika
        parsed = parser.from_file(pdf_file)
        text = parsed['content']
        if text and text.strip():
            return text
        
        return None # Return None if both fail
    except Exception as e:
        st.error(f"Error during PDF text extraction: {e}")  # Handle errors
        return None

def validate_json_structure(response): 
    try: 
        parsed_response = json.loads(response) 
        if ( isinstance(parsed_response, list) and all("Step" in item and "Category" in item for item in parsed_response) ): 
            return parsed_response, None 
        else: return None, "❌ JSON hat nicht die erwartete Struktur." 
    except json.JSONDecodeError as e: 
        return None, f"❌ JSON-Parsing-Fehler: {e}"

def clean_json_response(response): 
    if not response or response.strip() == "": 
        return None, "❌ Fehler: Die KI hat eine leere Antwort zurückgegeben." 
    parsed_response, error_message = validate_json_structure(response) 
    if parsed_response: 
        return parsed_response, None 
    try: 
        json_part = re.search(r"[.*]", response, re.DOTALL) 
        if json_part: 
            response = json_part.group(0) 
            response = response.replace("'", "\"") 
        parsed_response, error_message = validate_json_structure(response) 
        if parsed_response: 
            return parsed_response, None 
        return None, error_message 
    except Exception as e: 
        return None, f"❌ Fehler beim Bereinigen der JSON-Antwort: {e}"


# === 5️⃣ Checkliste rendern ===
def render_checklist_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):

    # === UI-Header ===
    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    # === Session-Management ===
    sessions = load_sessions(session_file)
    st.session_state.setdefault("universal_sessions", {})
    st.session_state.universal_sessions[use_case] = sessions

    extracted_text=""

    # === PDF-Upload und Text-Extraktion ===
    uploaded_file = st.file_uploader("Lade eine PDF hoch", type=["pdf"])

    if uploaded_file is not None:
        extracted_text = extract_text_from_pdf(uploaded_file)
        if extracted_text:
            st.text_area("Extracted Text (Debug)", extracted_text, height=200)
            print("Extracted Text (Console):", extracted_text)  # VERY IMPORTANT!
            # ... (rest of your processing)
        else:
            st.warning("No usable text could be extracted from the PDF.")

    # === Anzeige des extrahierten Textes ===
    with st.expander("**Inhalt von Upload**"):
        if extracted_text:
            st.markdown("### 📜 Inhalt der hochgeladenen PDF:")
            st.write(extracted_text)

    # === Checklisten-Optionen und Generierung ===
    checklist_format = st.selectbox(
        "Checklisten-Format wählen:",
        options=["Action Items", "Compliance Steps", "Audit Tasks"],
        index=0
    )

    generate_checklist = st.button("🚀 Checkliste generieren")

    if generate_checklist:
        st.info("Generating checklist. Please wait...")
        try:
            # EXAKT GLEICHER PROMPT WIE IM 1. VIEW
            prompt = f"""
            Convert the following document into a checklist format. Each entry should include:
            - Step: A concise description of the task.
            - Category: The category of the task.
            - Responsible: Placeholder for the responsible person/group.
            - Deadline: Placeholder for deadlines.

            Format: {checklist_format}

            Document Content:
            {extracted_text}
            """

            # EXAKT GLEICHER handle_query() AUFRUF
            checklist_raw, tokens_used, costs, references = handle_query(
                query=prompt,
                use_case=use_case,
                context=context,
                override_response_format="MARKDOWN",
                model_name=model_name,
            )

            final_checklist = str(checklist_raw)
            final_checklist = bleach.clean(final_checklist, tags=[], strip=True)  # Entfernt alle HTML-Tags

            st.markdown(f"```\n{final_checklist}\n```")

        except Exception as e:
            st.error(f"Error generating checklist: {e}")

    # === Session speichern ===
    st.session_state.universal_sessions[use_case].append(st.session_state["current_session"])
    save_sessions(session_file, st.session_state.universal_sessions[use_case])