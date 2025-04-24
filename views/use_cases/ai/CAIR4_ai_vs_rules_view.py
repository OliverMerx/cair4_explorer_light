"""
=================================================
💬 CAIR4 Regelbasierte Systeme vs. KI
=================================================

📌 **Beschreibung:**
Diese View visualisiert die Unterschiede zwischen regelbasierten Systemen und Künstlicher Intelligenz (KI).

✅ **Hauptfunktionen:**
- **Vergleich von Regelbasierten Systemen & KI:** Grafische Darstellung der Entscheidungsprozesse.
- **Dynamische Simulation:** Nutzer können eigene Eingaben testen.
- **Session-Tracking & Logging:** Speichert Ergebnisse zur späteren Analyse.

🔍 **Automatische Generierung:**
Diese View wurde nach dem CAIR4-Standard erstellt und ist direkt ins Framework integrierbar.
"""

# === 1️⃣ Import externer Bibliotheken (3rd Party Libraries) ===
#pylibs
from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json as json
from pylibs.datetime_lib import initialize_datetime
from pylibs.graphviz_lib import graphviz as graphviz

datetime = initialize_datetime()

#utils
from utils.core.CAIR4_update_sidebar import update_sidebar
from utils.core.CAIR4_session_manager_hybrid import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics
from utils.core.CAIR4_debug_utils import DebugUtils  # Import der Debug-Klasse

#controller
from controllers.CAIR4_controller import handle_query

def render_rule_vs_ai_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    """
    Rendert die View zur Visualisierung des Unterschieds zwischen regelbasierten Systemen und KI.
    """
    # Debug: Aufruf der Funktion
    DebugUtils.debug_print(f"render_rule_vs_ai_view gestartet für Use Case: {use_case}")

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

    # Hauptansicht
    st.subheader(title)
    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Regelbasiertes System")
        st.write("Ein regelbasiertes System folgt festen Regeln. Jede Eingabe wird nach vorher definierten Regeln verarbeitet.")
        rule_options = ["Wenn A dann B", "Wenn Temperatur > 30° dann Klimaanlage an", "Wenn Benutzer X dann Zugriff erlaubt"]
        selected_rule = st.selectbox("📜 Wähle eine Regel:", rule_options, key="rule_selection")

        # **Graphviz-Visualisierung für Regeln**
        rule_graph = graphviz.Digraph()
        rule_graph.node("Eingabe", "Eingabe")
        rule_graph.node("Regel", f"Regel: {selected_rule}")
        rule_graph.node("Ausgabe", "Feste Ausgabe")

        rule_graph.edge("Eingabe", "Regel")
        rule_graph.edge("Regel", "Ausgabe")

        st.graphviz_chart(rule_graph)

    with col2:
        st.write("#### Künstliche Intelligenz")
        st.write("Ein KI-System analysiert große Datenmengen und leitet Regeln aus den Daten selbstständig ab.")

        user_input = st.text_input("🔍 Gib eine Anfrage ein (z. B. 'Soll die Klimaanlage aktiviert werden?'):")

        # **Graphviz-Visualisierung für KI**
        ai_graph = graphviz.Digraph()
        ai_graph.node("Eingabe", "Eingabe")
        ai_graph.node("Daten", "Vergleich mit Daten")
        ai_graph.node("Modell", "KI-Modell: Wahrscheinlichkeitsbewertung")
        ai_graph.node("Ausgabe", "Dynamische Ausgabe")

        ai_graph.edge("Eingabe", "Daten")
        ai_graph.edge("Daten", "Modell")
        ai_graph.edge("Modell", "Ausgabe")

        st.graphviz_chart(ai_graph)

    st.markdown("---")

    if user_input:
        with st.spinner("Antwort wird berechnet..."):
            try:
                response, tokens_used, costs, references = handle_query(
                    query=user_input,
                    use_case=use_case,
                    context=context,
                    model_name=model_name,
                )

                st.success(f"💡 KI-Antwort: {response}")

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