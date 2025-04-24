"""
===========================
CAIR4 PDF-Viewer (iframe)
===========================

Einfaches Modul zum Laden von PDF als iframe.
Anzeige von Download etc. (bei Safari am Ende des Dokuments)

"""
from pylibs.streamlit_lib import streamlit as st
from pylibs.base64_lib import base64

from utils.core.CAIR4_browser_check import render_browser_check
from PyPDF2 import PdfReader  # Für Seitenanzahl

def load_pdf(file_path):
    with open(file_path, "rb") as f:
        return f.read()

def get_pdf_page_count(pdf_data):
    try:
        reader = PdfReader(pdf_data)
        return len(reader.pages)
    except:
        return 1  # Fallback

def display_pdf(pdf_data, num_pages, width="100%"):
    
    browser=render_browser_check()

    base_page_height=1000

    if browser == "Chrome":
        base_page_height=1130
    elif browser ==  "Safari":
        base_page_height=930
    elif browser == "Firefox":
        base_page_height=1300
    else:
        base_page_height=1130

    

    height = int(num_pages * base_page_height)  # z. B. 1000 px pro Seite
    base64_pdf = base64.b64encode(pdf_data).decode("utf-8")
    pdf_display = f'''
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}#toolbar=1&navpanes=0&scrollbar=0" 
            width="{width}" 
            height="{height}" 
            type="application/pdf"
            style="border:none;">
        </iframe>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)

def render_pdf_viewer(pdf_file_path):
    try:
        pdf_bytes = load_pdf(pdf_file_path)
        num_pages = get_pdf_page_count(pdf_file_path)
        display_pdf(pdf_bytes, num_pages)

    except FileNotFoundError:
        st.error(f"PDF-Datei nicht gefunden unter: {pdf_file_path}")