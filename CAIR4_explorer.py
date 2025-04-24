"""
===============================================
CAIR4 Use Case Explorer - (CAIR4_explorer.py)
===============================================

GitHub-Version (light ohne Login u. Role based
Access)

"""
# === 1. Imports ===
from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st
from utils.core.CAIR4_encrypt_manager import decrypt_data
from utils.core.CAIR4_save_import import safe_import, show_centered_spinner
from utils.core.CAIR4_log_manager import handle_session_action

# === 2. Reset-Funktionen ===
def reset_contents():
    st.session_state["collections"] = {}
    st.session_state["model_options"] = {}
    st.session_state["training"] = {}
    st.session_state["api_model_options"] = {}
    st.session_state["local_models"] = {}
    st.session_state["global_settings"] = {}

def reset_login_state(default_role="guest_light"):
    st.session_state.logged_in = False
    st.session_state.current_user = default_role
    st.session_state.user_role = default_role

# === 3. Initialisieren bei erstem Start ===
if "initialized" not in st.session_state:
    reset_login_state()  # Light-Default: "guest_light"
    reset_contents()
    st.session_state.initialized = True

# === 4. Optionale Rollen-Überschreibung per URL-Param ===
role_param = st.query_params.get("role", None)
if role_param:
    try:
        decrypted_role = decrypt_data(role_param)
        st.session_state.logged_in = True
        st.session_state.current_user = decrypted_role
        st.session_state.user_role = decrypted_role
    except Exception as e:
        st.warning("⚠️ Ungültiger Rollen-Token – Standardrolle wird verwendet.")

# === 5. Konfiguration für Rolle laden ===
from core.CAIR4_explorer_config import user_collection, GLOBAL_SETTINGS
collections, api_model_options, model_options, local_models, training = user_collection(st.session_state.user_role)

st.session_state["collections"] = collections
st.session_state["model_options"] = model_options
st.session_state["training"] = training
st.session_state["api_model_options"] = api_model_options
st.session_state["local_models"] = local_models
st.session_state["global_settings"] = GLOBAL_SETTINGS

# === 6. App-Konfiguration ===
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
if st.session_state.get("standalone", True):
    st.set_page_config(
        page_title="CAIR4 Explorer – Light",
        page_icon=BASE_PATH + "/assets/icons/CAIR4_compass.svg",
        layout="wide",
    )

# === 7. Main starten ===
spinner = show_centered_spinner("initialisiere CAIR4 Explorer...")
main = safe_import("core.CAIR4_init_main_encr", "main")
spinner.empty()

# === 8. Run-Handler ===
if __name__ == "__main__":
    main()
    try:
        handle_session_action("App Closed", None, st.session_state.get("active_view"))
    except Exception as e:
        handle_session_action("App Crashed", {"error": str(e)}, st.session_state.get("active_view"))

def run():
    try:
        main()
        handle_session_action("App Closed")
    except Exception as e:
        print(f"[ERROR] Crash: {e}")
        handle_session_action("App Crashed", {"error": str(e)})