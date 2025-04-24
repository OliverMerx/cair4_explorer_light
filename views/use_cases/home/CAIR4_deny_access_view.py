import streamlit as st

def render_deny_access_view(*args, **kwargs):
    st.title("🚫 Kein Zugriff")
    st.warning("Du hast aktuell keine Berechtigung, diese Inhalte anzuzeigen.\n\n"
               "Bitte wende dich an den Administrator oder wähle ein anderes Profil.")