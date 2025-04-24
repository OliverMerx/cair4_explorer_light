"""
<description>
=================================================
💬 CAIR4 FAQ_Chat View
=================================================

📌 **Beschreibung:**
Dieses Beispiel implementiert die **FAQ_Chat-Funktionalität** eines einfachen Feed-Forward-Chats und integriert alle erforderlichen Framework-Komponenten.
Der Unterschied zum Feed-Forward-Chat ist, dass dieser Code mit dem **CAIR4 Code Creator** automatisch von einer generativen KI erstellt wurde.

Der Prompt für den **CAIR4 Code Creator** lautete:

<ANFANG>

🔍 **Erstelle einen CAIR4-View für einen KI-gestützten FAQ-Assistenten.** 
 
✅ **Vorgaben:**
- **Chat-Modul aktivieren** – Nutzer kann Fragen stellen, Antworten kommen von der KI.
- **Session-Handling:** Chat-Nachrichten müssen in einer Session gespeichert werden.
- **Logging:** Jede Nachricht wird als JSON gespeichert (`role`, `content`, `timestamp`).
- **Debugging:** `DebugUtils.debug_print(f"User: {prompt}")` & `DebugUtils.debug_print(f"Assistant: {response}")`
- **Pflicht-Imports:** `from pylibs.streamlit_lib import streamlit as st` und `from pylibs.datetime_lib import initialize_datetime`
- **KEIN Kreditrisiko, KEINE Berechnungen** – Nur ein KI-Chat!
 
🎯 **Erwartete Verarbeitung:**
- Der Nutzer stellt eine Frage.
- Die KI antwortet und speichert die Konversation in der Session.
- Die Session wird nur aktualisiert, wenn eine neue Nachricht hinzukommt.
- `config.json` definiert den `session_file` als `"CAIR4_data/data/faq_chat_sessions.json"`.
 
⚠️ **KEINE Berechnungen oder Zahleneingaben! Nur Chat!**

<ENDE>

✅ **CAIR4-Standard:**
- Integration von pylibs statt direktem Import von 3rd-Party Modulen, um diese im CAIR4-Twin observieren zu können.
- **Session-Verwaltung:** Lädt und speichert inhalte von Sitzungen.
- **Logging & Debugging:** Nutzt DebugUtils für eine detaillierte Fehleranalyse.
- **Query-Handling:** Übergibt Nutzeranfragen an das CAIR4-KI-System.
- Verwendung diverser KI-Modelle möglich.

<description>
"""

# === 1️⃣ Import externer Bibliotheken (3rd Party Libraries) ===
# pylibs
from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json as json
from pylibs.importlib_lib import importlib
from pylibs.datetime_lib import initialize_datetime

datetime = initialize_datetime()

# utils
from utils.core.CAIR4_update_sidebar import update_sidebar

# controller
from controllers.CAIR4_controller import handle_query

# utils
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics
from utils.core.CAIR4_debug_utils import DebugUtils  # Import der Debug-Klasse


def render_faq_chat_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    """
    Rendert die Universal-Ansicht für den gegebenen Use Case.
    """
    # Debug: Aufruf der Funktion
    DebugUtils.debug_print(f"render_faq_chat_view gestartet für Use Case: {use_case}")

    # Sessions laden
    sessions = load_sessions(session_file)
    st.session_state.setdefault("universal_sessions", {})
    st.session_state.universal_sessions[use_case] = sessions
    DebugUtils.debug_print(f"{len(sessions)} Sessions geladen für Use Case: {use_case}")

    # Initialisiere aktuelle Session
    if "active_use_case" not in st.session_state or st.session_state["active_use_case"] != use_case:
        st.session_state["active_use_case"] = use_case
        st.session_state["current_session"] = {
            "messages": [],
            "metrics": {
                "total_tokens": 0,
                "total_costs": 0.0,
                "tokens_used_per_request": [],
                "costs_per_request": [],
                "request_names": [],
            },
        }
        DebugUtils.debug_print(f"Neue Session initialisiert für {use_case}")

    # Sidebar aktualisieren
    with st.sidebar:
        update_sidebar(use_case, session_file)

    # Hauptansicht
    st.subheader(title)
    
    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)


    # Chatnachrichten anzeigen
    for msg in st.session_state["current_session"]["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Eingabefeld für den Chat
    if prompt := st.chat_input(f"Frage zu {use_case} stellen:"):
        DebugUtils.debug_print(f"User: {prompt}")
        with st.chat_message("user"):
            st.markdown(prompt)
        append_message(st.session_state["current_session"], "user", prompt)

        try:
            with st.chat_message("assistant"):
                with st.spinner("Anfrage wird verarbeitet..."):
                    response, tokens_used, costs, references = handle_query(
                        query=prompt,
                        use_case=use_case,
                        context=context,
                        model_name=model_name,
                    )
                    DebugUtils.debug_print(f"Assistant: {response}")
                    st.markdown(response)
                    append_message(st.session_state["current_session"], "assistant", response)

                    # Metriken aktualisieren
                    update_metrics(
                        st.session_state["current_session"]["metrics"],
                        tokens_used=tokens_used,
                        costs=costs,
                    )
                    DebugUtils.debug_print(f"Metriken aktualisiert: {tokens_used} Tokens, {costs} Kosten")

                    # Session speichern
                    st.session_state.universal_sessions[use_case].append(st.session_state["current_session"])
                    save_sessions(session_file, st.session_state.universal_sessions[use_case])
                    DebugUtils.debug_print("Session erfolgreich gespeichert")

        except Exception as e:
            st.error(f"Fehler: {e}")
            DebugUtils.debug_print(f"Fehler aufgetreten: {str(e)}")

st.markdown("""
    <style> 
    [data-testid="stBottomBlockContainer"] {
    background-color: #ccc !important;
    background:transparent!important;
    }
    </style>
    """, unsafe_allow_html=True
    )