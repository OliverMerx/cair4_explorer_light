from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st

def init_states(collections):
    """Initialisiert alle benötigten Session-State-Werte nur einmal."""

    try:
        default_use_case = list(collections.keys())[0]
    except:
        default_use_case = None

    # Standardwerte setzen
    st.session_state.setdefault("sidebar_initialized", False)
    st.session_state.setdefault("chroma_name", "./CAIR4_data/chroma_db")
    st.session_state.setdefault("base_path", os.path.dirname(os.path.abspath(__file__)).replace("/core", ""))
    st.session_state.setdefault("current_view_index", 0)
    st.session_state.setdefault("debug_modus_model", True)
    st.session_state.setdefault("session_id", "N/A")
    st.session_state.setdefault("active_view", [])
    st.session_state.setdefault("view_path", "")
    st.session_state.setdefault("previous_use_case", "")
    st.session_state.setdefault("selected_use_case", default_use_case)
    st.session_state.setdefault("selected_training", default_use_case)
    st.session_state.setdefault("show_training_modal", False)
    st.session_state.setdefault("selected_chapter", '')
    st.session_state.setdefault("selected_chapter_index", 0)
    st.session_state.setdefault("selected_content_index", 0)
    st.session_state.setdefault("home_video_index", 0)
    st.session_state.setdefault("home_video_label", {})
    st.session_state.setdefault("use_case_video_index", 0)
    st.session_state.setdefault("use_case_video_label", {})
    st.session_state.setdefault("chapter_options", sorted(set(entry["chapter"] for entry in collections.values())))
    st.session_state.setdefault("content_options", [])
    st.session_state.setdefault("selected_model", "gpt-4 (03/2024)")
    st.session_state.setdefault("selected_model_api", "gpt-4")
    st.session_state.setdefault("api_keys", {})
    st.session_state.setdefault("header_color", "")
    st.session_state.setdefault("bg_color", "")
    st.session_state.setdefault("border_color", "")
    st.session_state.setdefault("field_color", "")
    st.session_state.setdefault("background_image", "")
    st.session_state.setdefault("direct_link", None)
    st.session_state.setdefault("direct_chapter", False)
    st.session_state.setdefault("window_width", 1200)
    st.session_state.setdefault("internet_chat_messages", "")
    st.session_state.setdefault("tracker", 0)
    st.session_state.setdefault("generated_images", [])
    st.session_state.setdefault("selected_stitch", "")
    st.session_state.setdefault("previous_stitch", "empty")
    st.session_state.setdefault("step", 0)
    st.session_state.setdefault("pipe_context", [])
    st.session_state.setdefault("model_selection", [])
    st.session_state.setdefault("token_compare_result", {})
    st.session_state.setdefault("access_layer_enabled", False)
    st.session_state.setdefault("user_authenticated", False)
    st.session_state.setdefault("user_role", None)
    st.session_state.setdefault("popover_visible", False)  
    st.session_state.setdefault("atcf_description", "")
    st.session_state.setdefault("atcf_title", "")  