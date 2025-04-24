from core.CAIR4_init_views import render_active_view
from views.core.CAIR4_sidebar_view import render_sidebar_view
import streamlit as st

def handle_direct_view_from_url(collections: dict, model_options) -> bool:
    """
    Verarbeitet direkte Aufrufe per URL (z. B. ?view=OCR-Texterkennung).

    - Unterstützt nun auch Kleinschreibung per Browser (?view=gpai-modelle)
    - Setzt Session-State korrekt und rendert die Sidebar + View.
    - Löscht Query-Params nach erfolgreichem Direktaufruf.

    Rückgabewert:
    - True: Direkter View wurde erfolgreich gerendert.
    - False: Kein passender View vorhanden oder kein direkter Aufruf.
    """

    requested_view = st.query_params.get("view", None)
    if not requested_view:
        return False

    # 🔍 Case-insensitive Lookup für Use Case Namen
    view_map = {k.lower(): k for k in collections}
    requested_view_lower = requested_view.lower()

    if requested_view_lower not in view_map:
        st.warning(f"Unbekannter View: '{requested_view}' – kein Rendering durchgeführt.")
        return False

    # ✅ Originalname rekonstruieren
    actual_view = view_map[requested_view_lower]
    use_case_config = collections[actual_view]
    chapter = use_case_config["chapter"]

    # 🧠 Session-Werte setzen
    st.session_state["selected_use_case"] = actual_view
    st.session_state["selected_training"] = actual_view
    st.session_state["previous_use_case"] = actual_view
    st.session_state["selected_chapter"] = chapter
    st.session_state["active_view"] = actual_view

    # 🧭 Sidebar & View rendern
    render_sidebar_view(
        collections,
        model_options,
        direct=True,
        initial_chapter=chapter,
        initial_use_case=actual_view
    )

    render_active_view(actual_view, use_case_config)

    # 🧼 Query-Parameter löschen, um Loop zu vermeiden
    st.query_params.clear()
    st.session_state.direct_url = False

    # Optionales Debug-Log
    # st.info(f"✅ Direktlink erkannt: '{requested_view}' → '{actual_view}'")

    return True