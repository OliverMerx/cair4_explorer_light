# core.CAIR4_login_manager.py
import streamlit as st
import sqlite3
import time

DB_PATH = "user_access.sqlite"

def authenticate_user(username, password):
    """Prüft Login-Daten gegen die SQLite-Datenbank"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        return True, result[0]
    return False, None

def handle_login():
    """Standard-Login mit st.stop() → für Apps mit vollständiger Sperre"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.user_role = None

    if not st.session_state.logged_in:
        with st.form("login_form"):
            st.header("🔐 Login erforderlich")
            username = st.text_input("Benutzername")
            password = st.text_input("Passwort", type="password")
            login_btn = st.form_submit_button("Login")

            if login_btn:
                success, role = authenticate_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.user_role = role
                    st.rerun()
                else:
                    st.error("❌ Benutzername oder Passwort falsch")
        st.stop()

def handle_login_dialog():
    """Nur das Formular für Dialog-Nutzung"""
    st.markdown("Gib deine Login-Daten ein:")
    username = st.text_input("Benutzername", key="dialog_username")
    password = st.text_input("Passwort", type="password", key="dialog_password")

    if st.button("Anmelden", key="dialog_login_btn"):
        success, role = authenticate_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.session_state.user_role = role
            st.query_params.clear()
            st.write("Dein Profil wird geladen. Bitte einen Moment Geduld ...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Benutzername oder Passwort falsch")

def handle_logout():
    with st.sidebar:
        st.success(f"✅ Eingeloggt als: {st.session_state.current_user} ({st.session_state.user_role})")
        if st.button("🔓 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()