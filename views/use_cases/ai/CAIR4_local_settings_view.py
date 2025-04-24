"""
==============================================
💡 CAIR4 Einstellungen Settings verändern
==============================================

KI leitet Antworten auf Basis probabilistischer Entscheidungslogiken vor. 
Durch die Verarbeitung der Nutzereingabe und die dynamische Reaktion auf erkannte Muster können verschiedene plausible Antworten vergleichen werden.
Die Antwort bzgl. der Hauptstädte von vier Ländern wird dabei stets mit anderen relevanten Städten verglichen.

Um entsprechende Wahrscheinlichkeiten und Relationen berechnen zu können, müssen die Worte des Promptszuvor numerisch umgewandelt sein (Vektorisierung).

"""
from pylibs.streamlit_lib import streamlit as st
from controllers.CAIR4_controller import handle_query
from utils.core.CAIR4_metrics_manager import update_metrics

def render_local_settings_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    """
    Lokaler Settings-Test-View: Isoliertes Ausprobieren von Temperature, Top-P, Antwortformat & Stil.
    """

    st.subheader(title)
    with st.expander("Beschreibung des Use Case"):
        st.write(description)

    # Lokale Settings initialisieren
    if "local_settings" not in st.session_state:
        st.session_state.local_settings = {
            "temperature": 0.7,
            "top_p": 0.9,
            "response_length": "Mittel",
            "response_format": "Fließtext",
            "system_message": ""
        }

    local_settings = st.session_state.local_settings

    # 🔧 Temperatur
    local_settings["temperature"] = st.slider(
        "🔧 Temperature (Kreativitätslevel)",
        0.0, 1.0, local_settings.get("temperature", 0.7), 0.1
    )

    # 📊 Top-P
    local_settings["top_p"] = st.slider(
        "📊 Top-P Sampling (Wahrscheinlichkeit – Prozent der wahrscheinlichsten Token)",
        0.0, 1.0, local_settings.get("top_p", 0.9), 0.1
    )

    # 📏 Antwortlänge
    #valid_lengths = ["Kurz", "Mittel", "Lang"]
    #selected_length = local_settings.get("response_length", "Mittel")
    local_settings["response_length"] = "Mittel"#st.selectbox(
    #    "📏 Antwortlänge",
    #    valid_lengths,
    #    index=valid_lengths.index(selected_length)
    #)

    # 📝 Antwortformat
    local_settings["response_format"] = "Fließtext" #st.radio(
    #    "📝 Antwortformat",
    #    ["Aufzählungspunkte", "Fließtext"],
    #    index=0 if local_settings.get("response_format") == "Aufzählungspunkte" else 1
    #)

    # 🎙 Systemnachricht
    system_messages = [
        "Du bist ein allgemeiner KI-Assistent. Beantworte Nutzeranfragen klar und präzise.",
        "Du bist ein humorvoller Assistent, der jede Antwort mit einem lustigen Spruch beginnt und endet.",
        "Antworte immer im Stil eines Sherlock-Holmes-Detektivs – analytisch und präzise.",
        "Verwende in jeder Antwort Metaphern aus der Natur, um komplexe Sachverhalte einfach zu erklären.",
        "Sprich wie ein weiser, alter Mentor, der stets Ratschläge mit Lebensweisheiten verknüpft.",
        "Sei ein enthusiastischer Sportkommentator, der jede Antwort mit Energie und Spannung präsentiert.",
        "Antworte wie ein Soldat. Kurz. Knapp. Zackig. Stichpunkte ohne Füllworte"


    ]
    current_message = local_settings.get("system_message", "")
    if current_message not in system_messages:
        current_message = system_messages[0]
    local_settings["system_message"] = st.selectbox(
        "🎙 Systemnachricht",
        system_messages,
        index=system_messages.index(current_message)
    )

    st.markdown("---")

    # 🗣 Eingabefeld
    user_input = st.text_input("💬 Stelle eine Testfrage:")

    if user_input:
        with st.spinner("Antwort wird generiert..."):
            try:
                response, tokens_used, costs, references = handle_query(
                    query=user_input,
                    use_case=use_case,
                    context=context,
                    model_name=model_name,
                    new_system_message=local_settings["system_message"],
                    new_temperature=local_settings["temperature"],
                    new_top_p=local_settings["top_p"],
                    new_response_length=local_settings["response_length"],
                    new_response_format=local_settings["response_format"]
                )

                st.success("💡 KI-Antwort:")
                st.write(response)

                update_metrics(
                    st.session_state["current_session"]["metrics"],
                    tokens_used=tokens_used,
                    costs=costs,
                )

            except Exception as e:
                st.error(f"Fehler bei der Anfrage: {e}")