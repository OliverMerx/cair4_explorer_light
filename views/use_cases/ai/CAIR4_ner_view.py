"""
=================================================
💬 CAIR4 NER View
=================================================

📌 **Beschreibung:**
Diese View implementiert die **NER-Funktionalität** und integriert alle erforderlichen Framework-Komponenten.

✅ **Hauptfunktionen:**
- **Session-Verwaltung:** Lädt und speichert Sitzungen für langfristige Interaktionen.
- **Logging & Debugging:** Nutzt DebugUtils für eine detaillierte Fehleranalyse.
- **Query-Handling:** Übergibt Nutzeranfragen an das CAIR4-KI-System.

🔍 **Automatische Generierung:**  
Diese View wurde vom **CAIR4 Code Creator** erzeugt und kann direkt in das Framework eingebunden werden.
"""

# === 1️⃣ Import externer Bibliotheken (3rd Party Libraries) ===
#pylibs
from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json as json
from pylibs.datetime_lib import initialize_datetime

datetime = initialize_datetime()

#utils
from utils.core.CAIR4_update_sidebar import update_sidebar

#controller
from controllers.CAIR4_controller import handle_query

# utils
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics
from utils.core.CAIR4_debug_utils import DebugUtils  # Import der Debug-Klasse

def render_ner_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    """
    Rendert die NER-Ansicht für den gegebenen Use Case.
    
    Args:
        use_case (str): Der Name des Use Cases.
        context (str): Der Kontext für die Abfrage.
        title (str): Der Titel der Ansicht.
        description (str): Die Beschreibung der Ansicht.
        system_message (str): Die Systemnachricht für das KI-Modell.
        session_file (str): Der Pfad zur Session-Datei.
        model_name (str): Der Name des KI-Modells.
        settings (dict): Die Einstellungen für die Ansicht.
        collection (str): Der Name der Collection.
        sidebar (dict): Konfiguration der Sidebar.
    """

    # Debug: Aufruf der Funktion
    DebugUtils.debug_print(f"render_ner_view gestartet für Use Case: {use_case}")

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
            "calculations": [],
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
    with st.expander("**Use Case Beschreibung**"):
        st.markdown(description, unsafe_allow_html=True)

    # Beispieltexte
    example_texts = {
        "Nachrichtenartikel": "Angela Merkel besuchte gestern die Vereinten Nationen in New York.",
        "Wissenschaftliche Publikation": "Die Studie zeigt einen Zusammenhang zwischen ACE2-Rezeptoren und COVID-19.",
        "Soziale Medien": "Elon Musk twitterte über seine Pläne für Tesla und SpaceX."
    }

    # Auswahl des Beispieltexts
    selected_example = st.selectbox("Beispieltext auswählen:", list(example_texts.keys()))
    user_input = st.text_area("Oder eigenen Text eingeben:", value=example_texts[selected_example], height=150)

    # Analyse starten
    if st.button("Analyse starten"):
        DebugUtils.debug_print(f"Analyse gestartet für Text: {user_input[:50]}...")
        try:
            # Anfrage an den CAIR4-Controller für NER
            with st.spinner("Text wird analysiert..."):
                response, tokens_used, costs, references = handle_query(
                    query=f"Führe NER für folgenden Text durch: {user_input}",
                    use_case=use_case,
                    context=context,
                    model_name=model_name,
                )
                DebugUtils.debug_print(f"Antwort erhalten: {response[:50]}...")
                st.write("Analyseergebnisse:")
                st.markdown(response, unsafe_allow_html=True)

                # Metriken aktualisieren
                update_metrics(
                    st.session_state["current_session"]["metrics"],
                    tokens_used=tokens_used,
                    costs=costs,
                )
                DebugUtils.debug_print(f"Metriken aktualisiert: {tokens_used} Tokens, {costs} Kosten")

                # Session speichern
                # Protokolliere die Analyse als Calculation
                st.session_state["current_session"]["calculations"].append({
                    "event": "NER-Analyse",
                    "parameters": {
                        "input_text": user_input,
                        "analysis_results": response
                    },
                    "timestamp": datetime.datetime.now().isoformat()
                })
                st.session_state.universal_sessions[use_case].append(st.session_state["current_session"])
                save_sessions(session_file, st.session_state.universal_sessions[use_case])
                DebugUtils.debug_print("Session erfolgreich gespeichert")

                 # Logging des Events
                DebugUtils.debug_print({
                    "event": "NER-Analyse",
                    "parameters": {
                        "input_text": user_input,
                        "analysis_results": response
                    },
                    "timestamp": datetime.datetime.now().isoformat()
                })

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