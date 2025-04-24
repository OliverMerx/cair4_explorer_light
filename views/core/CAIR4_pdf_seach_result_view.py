"""
===========================
🔍 CAIR4 Search Window
===========================

Suchfunktion für Use Cases – klickbare Ergebnisse mit direkter URL (ohne session_state-Konflikte)
  
Verwendung:
from views.core.CAIR4_search_modal import render_search_modal
render_search_modal(COLLECTIONS)
===========================================
"""
from pylibs.streamlit_lib import streamlit as st  
from urllib.parse import quote
from pylibs.streamlit_lib import streamlit as st
from utils.core.CAIR4_pdf_viewer import render_pdf_viewer

def render_pdf_search_result_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    st.subheader("📄 PDF-Ergebnisanzeige")
    
    pdf_path = st.session_state.base_path+"/"+context  # <- kommt direkt aus URL param ?doc=...

    if not pdf_path:
        st.warning("❌ Kein PDF-Pfad übergeben.")
        return

    st.markdown(f"🔗 Angeforderte Datei: `{pdf_path}`")
    try:
        render_pdf_viewer(pdf_path)
    except Exception as e:
        st.error(f"Fehler beim Laden der PDF-Datei: {e}")