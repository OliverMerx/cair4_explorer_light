# === 1️⃣  Import externer Bibliotheken (3rd Party Libraries) ===
from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st  

# === 2️⃣  CAIR4 Core Imports ===
from core.CAIR4_app_base import initialize_chroma_db, initialize_collections, ensure_directories
from core.CAIR4_init_states import init_states
from core.CAIR4_init_views import render_active_view

from utils.core.CAIR4_direct_url_manager import handle_direct_view_from_url
from utils.core.CAIR4_encrypt_manager import decrypt_data  

# === 3️⃣  Hilfs-Utilities ===
from utils.core.CAIR4_log_manager import handle_session_action, ensure_log_file_exists
from utils.core.CAIR4_styles_manager import apply_custom_styles
from utils.core.CAIR4_session_initializer import initialize_session_state

from views.core.CAIR4_pdf_seach_result_view import render_pdf_search_result_view
from views.core.CAIR4_sidebar_view import render_sidebar_view

# === 4️⃣  Logging-Konstante ===
LOG_FILE = "CAIR4_data/data/logs.json"


# === ✅ Main Entry Point
def main():
    COLLECTIONS = st.session_state.get("collections", {})
    GLOBAL_SETTINGS = st.session_state.get("global_settings", {})
    MODEL_OPTIONS = st.session_state.get("api_model_options", {})

    # === 🔐 Rolle aus Query-Params entschlüsseln
    encrypted_role = st.query_params.get("r", None)
    debug_role = st.query_params.get("role", None)
    debug_mode = st.query_params.get("debug", None) == "true"

    if "user_role" not in st.session_state:
        if debug_role and debug_mode:
            role = debug_role
        elif encrypted_role:
            role = decrypt_data(encrypted_role) or "guest"
        else:
            role = "guest"
        st.session_state.user_role = role
        st.session_state.current_user = role

    # === 🌀 First Run
    st.session_state["first_run"] = "first_run" not in st.session_state

    # === Initial Setup
    init_states(COLLECTIONS)
    apply_custom_styles()
    initialize_chroma_db()
    initialize_collections()
    ensure_directories()
    ensure_log_file_exists(LOG_FILE, st.session_state.session_id)
    initialize_session_state(global_settings=GLOBAL_SETTINGS)
    handle_session_action("App gestartet", {"status": "Session init"})

    role=decrypt_data(st.query_params.get("role", None))

    # === 📌 Spezialfall: PDF-Ergebnis-Ansicht
    requested_view = st.query_params.get("view", None)

    if requested_view and "PDF-Results" in requested_view:
        render_pdf_search_result_view(
            use_case="PDF-Results",
            context=st.query_params.get("doc", ""),
            system_message="",
            session_file="",
            model_name="",
            settings={},
            title="PDF-Ergebnisanzeige",
            description="Direkter Aufruf über Suchergebnis.",
            collection=None,
            sidebar=False
        )
        st.stop()

    # === 🚀 Normaler View
    if handle_direct_view_from_url(COLLECTIONS, MODEL_OPTIONS):
        pass
    else:
        try:
            selected_use_case = render_sidebar_view(COLLECTIONS, MODEL_OPTIONS, direct=False)
        except Exception:
            selected_use_case = st.session_state.get("selected_use_case")

        if selected_use_case is None:
            st.warning("⚠️ Fehler im Session State. Bitte Browser neu laden.")
        else:
            config = COLLECTIONS[selected_use_case]
            render_active_view(selected_use_case, config)
            st.session_state["active_view"] = selected_use_case