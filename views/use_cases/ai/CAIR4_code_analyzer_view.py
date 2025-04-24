"""
=================================================
💬 CAIR4 Code Analyser View
=================================================

📌 **Beschreibung:**
Diese View analysiert ein gegebenes Python-Snippet und liefert strukturierte Einblicke.
Sie integriert alle erforderlichen Framework-Komponenten und ermöglicht eine KI-gestützte Code-Analyse.

✅ **Hauptfunktionen:**
- **Session-Verwaltung:** Lädt und speichert Sitzungen für langfristige Interaktionen.
- **Logging & Debugging:** Nutzt DebugUtils für detaillierte Fehleranalysen.
- **Query-Handling:** Übergibt Python-Code an das CAIR4-KI-System zur Analyse.
- **Metriken-Tracking:** Erfasst die Nutzung von Tokens und API-Kosten.
- **Ergebnisvisualisierung:** Stellt die Analyseergebnisse strukturiert dar.

🔍 **Automatische Generierung:**
Diese View wurde nach dem CAIR4-Standard erstellt und kann direkt ins Framework eingebunden werden.
"""

# === 1️⃣ Import externer Bibliotheken (3rd Party Libraries) ===
# pylibs
from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json as json
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

def render_code_analyser_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    """
    Rendert die Framework-Analyse-Ansicht für den gegebenen Use Case.
    """
    # Debug: Aufruf der Funktion
    DebugUtils.debug_print(f"render_framework_analysis_view gestartet für Use Case: {use_case}")

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
    st.title(f"{use_case} - Framework Analysis")
    st.write("Analysiere ein Python-Snippet und erhalte strukturierte Erkenntnisse.")

    # Dummy-Code
    dummy_code = """def example_function(x, y):
    # Diese Funktion addiert zwei Zahlen und gibt das Ergebnis zurück.
    return x + y

class ExampleClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"
    """

    st.subheader("Beispiel-Python-Code")
    st.code(dummy_code, language="python")

    # Query-Einstellungen
    st.subheader("Query-Einstellungen")
    st.write(f"**Temperature:** {settings['temperature']}")
    st.write(f"**Top-p:** {settings['top_p']}")
    st.write(f"**Max Tokens:** {settings['response_length']}")
    st.write(f"**Modell:** {model_name}")
    st.write(f"**Kontext:** {context}")

    # Analyse starten
    if st.button("🔍 Code analysieren"):
        st.info("Der Code wird analysiert. Bitte warten...")
        try:
            query = f"""
            Bitte analysiere den folgenden Python-Code und gib strukturierte Erkenntnisse:
            - Zweck des Codes.
            - Wichtige Funktionen und ihre Rollen.
            - Abhängigkeiten oder genutzte Imports.
            - Verbesserungsvorschläge.

            Code:
            {dummy_code}
            """

            # Anfrage an die KI senden
            response, tokens_used, costs, _ = handle_query(
                query=query,
                use_case=use_case,
                context=context,
                model_name=model_name,
            )

            # Ergebnisse anzeigen
            st.subheader("Analyse-Ergebnis")
            st.text_area("Analyse Output", response or "Keine Antwort vom Modell erhalten.", height=300)

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
            st.error(f"Fehler während der Analyse: {e}")
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