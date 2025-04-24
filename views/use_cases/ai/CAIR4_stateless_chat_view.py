"""
================================
💡 CAIR4 Stateless Chat View
================================
Dieser CAIR4 Use Case rendert einen so genannten Stateless-Chat als einfaches Beispiel eines KI-Systems i.S.v. Artikel 3 Nr. 1 EU AI Acts.
Jeder Prompt ist individuell. Innerhalb einer Session gibt es keine Erinnerungen an vorherige Prompts.
Häufig werden Stateless-Chats für FAQs und einfache kurze Dialoge genutzt.
Da die Antworten nicht regelbasiert, sondern datengeneriert sind, handelt es sich um KI im regulatorischen Sinne. 
Der View ermöglicht das Laden, Anzeigen und Verwalten von Sitzungen.
Über Metrics (Sidebar) sind die Kosten der Abfrage abrufbar (nicht bei jedem Modell möglich).

+++++++++++++++++++++++++++++++++++++++++++++++++++++
+ Beispiel für einfaches KI-System i.S.d. EU AI Acts:
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Da in diesem Use Case eine Interaktionsschnittstelle für Anwender integriert ist, handelt es sich um ein KI-System.
Dieser Chat kann als Anbieter, aber auch als Betreiber i.S.v. Art. 3 Nr. 3, 4 EU AI Acts in Verkehr gebracht bzw. betrieben werden.
Als Anbieter besteht insbesondere die Möglichkeit der Individualisierung bzw. funktionellen Erweiterung.

###################################

Der Use Case „Stateless-Chat ohne Erinnerungen“ ermöglicht schnelle und effiziente Interaktionen, bei denen jede Konversation eigenständig betrachtet wird. Dieses Modell eignet sich ideal für Anwendungsfälle, bei denen kein Langzeitgedächtnis erforderlich ist und jede Anfrage unabhängig vom bisherigen Kontext verarbeitet werden soll.

🎯 Anwendungsfälle:
    •    Support-Chats: Bieten schnelle Antworten auf spezifische Anfragen, ohne vergangene Konversationen zu berücksichtigen.
    •    Formulareingaben: Ermöglichen die strukturierte Aufnahme von Daten, ohne Vorwissen aus vorherigen Sessions.
    •    Einfache Chatbots: Unterstützen gezielte Interaktionen, z. B. für FAQs oder einfache Prozessabfragen.

🚀 Funktionen im Überblick:
    1.    Jede Session ist unabhängig: Es gibt keine Speicherung von Nutzereingaben über Sessions hinweg.
    2.    Schnelle Reaktionszeiten: Da kein Kontext geladen oder analysiert werden muss, bleibt das System schlank und reaktionsfreudig.
    3.    Datenschutzfreundlich: Da keine langfristigen Daten gespeichert werden, eignet sich dieser Ansatz besonders für sensible Anwendungsfälle.

💡 Vorteile:
    •    Schnelle Initialisierung: Kein Laden von Erinnerungen oder Kontextdaten notwendig.
    •    Eindeutige Interaktionen: Jede Anfrage wird nur auf Basis der aktuellen Eingabe beantwortet.
    •    Minimaler Speicherbedarf: Ideal für Systeme mit begrenzten Ressourcen oder strengen Datenschutzanforderungen.

Funktionen im Überblick:
- **render_stateless_chat_view**: Hauptfunktion, die die View rendert und die Logik der Eingaben steuert.
- **update_sidebar**: Hilfsfunktion, um die Sidebar dynamisch mit Sitzungsinformationen zu aktualisieren.
- **Debug-Modus**: Aktivierbare Debug-Ausgaben für die Analyse von Prozessen und Fehlern.

Wichtige Module:
- **session_manager**: Lädt und speichert Sitzungsdaten.
- **message_manager**: Verarbeitet und speichert Nachrichten in der aktuellen Sitzung.
- **metrics_manager**: Aktualisiert Metriken wie Token- und Kostennutzung.
"""

#pylibs
from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json as json

#utils
from utils.core.CAIR4_update_sidebar import update_sidebar

#controller
from controllers.CAIR4_controller import handle_query

# utils
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics
from utils.core.CAIR4_debug_utils import DebugUtils


def render_stateless_chat_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    
    DebugUtils.debug_print(f"render_universal_view gestartet für Use Case: {use_case}")

    sessions = load_sessions(session_file)
    st.session_state.setdefault("universal_sessions", {})
    st.session_state.universal_sessions[use_case] = sessions

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

    with st.sidebar:
        update_sidebar(use_case, session_file)

    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    for msg in st.session_state["current_session"]["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input(f"Frage zu {use_case} stellen:"):
        DebugUtils.debug_print(f"Eingabe erhalten: {prompt}")
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

                    DebugUtils.debug_print(f"Antwort generiert: {response[:50]}...")

                    st.markdown(response)
                    append_message(st.session_state["current_session"], "assistant", response)

                    if "metrics" not in st.session_state["current_session"]:
                        st.session_state["current_session"]["metrics"] = {
                            "total_tokens": 0,
                            "total_costs": 0.0,
                            "tokens_used_per_request": [],
                            "costs_per_request": [],
                            "request_names": []
                        }

                    update_metrics(
                        st.session_state["current_session"]["metrics"],
                        tokens_used=tokens_used,
                        costs=costs,
                    )

                    DebugUtils.debug_print(f"Metriken aktualisiert: {tokens_used} Tokens, {costs} Kosten")

                    st.session_state.universal_sessions[use_case].append(st.session_state["current_session"])
                    save_sessions(session_file, st.session_state.universal_sessions[use_case])

                    DebugUtils.debug_print("Session erfolgreich gespeichert")

        except Exception as e:
            st.error(f"Fehler: {e}")
            DebugUtils.debug_print(f"Fehler aufgetreten: {str(e)}")

st.markdown(
    """
    <style> 
    [data-testid="stBottomBlockContainer"] {
    background-color: #ccc !important;
    background:transparent!important;
    }
    </style>
    """, unsafe_allow_html=True
)
