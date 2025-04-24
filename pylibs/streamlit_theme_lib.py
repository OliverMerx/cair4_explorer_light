DESCRIPTION = "Ermöglicht das Tracking des aktuellen Themes von Streamlit (light/black/custom)."

# py_lib/streamlit_lib.py
from streamlit_theme import st_theme

def initialize_streamlit_theme():
    """
    Gibt die Streamlit-Theme Instanz zurück.
      
    Returns:
        st_theme: Die Streamlit-Theme-Instanz.
    """
    return st_theme