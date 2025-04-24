"""
<description>
=================================================
🧠 CAIR4 Kontext-Chat: Bedeutung und Relevanz
=================================================

Dieses Modul bietet eine **kontextgesteuerte KI-Interaktion**, die es ermöglicht, KI-Systeme gezielt für verschiedene **Anwendungsfälle (Use Cases)** auszurichten.  
Im Gegensatz zu generischen KI-Modellen, die unabhängig vom Nutzerkontext agieren, erlaubt Anbietern eines KI-Systems eine **dynamische Steuerung der KI-Antworten** durch einen festgelegten oder ausgewählten **Kontext**.

🔹 **Warum ist der Kontext wichtig?**
- **Steuerung der KI-Ausgabe:** Das Verhalten der KI kann je nach gewähltem Kontext **gezielt beeinflusst werden**.
- **Personalisierung:** Nutzer können spezifische Kontexte auswählen, um präzisere und relevantere Antworten zu erhalten.
- **Regulatorische Anpassung:** In hochsensiblen Bereichen (z. B. Medizin, Recht, Compliance) kann der Kontext als **Steuerungsmechanismus** genutzt werden.
- **Optimierte Nutzerführung:** Durch die **Vorauswahl von Systemnachrichten** wird sichergestellt, dass die KI nur innerhalb festgelegter Rahmen agiert.

🔧 **Wie beeinflusst der Kontext die Nutzung?**
Der Kontext beeinflusst die KI **auf mehreren Ebenen**:
1️⃣ **Systemnachricht:** Jeder Kontext enthält eine **vordefinierte Systemanweisung**, die das Verhalten der KI lenkt.  
2️⃣ **Dynamische Parameter:** Temperatur, Top-p-Werte und andere Einstellungen können je nach Kontext angepasst werden.  
3️⃣ **Speicher & Sitzungen:** Der Kontext bestimmt, welche Daten in **früheren Sitzungen gespeichert oder erneut verwendet** werden.

🔍 **Beispielhafte Anwendungsfälle für Kontext-Steuerung**
| **Use Case**       | **Möglicher Kontext** |
|-------------------|---------------------|
| 📜 **Juristische KI** | "Antworte auf Basis deutscher Gesetzgebung." |
| 🏥 **Medizinischer Chatbot** | "Berücksichtige medizinische Leitlinien, keine Diagnosen!" |
| 🔎 **Dokumenten-Analyse** | "Fasse den Kerninhalt wissenschaftlicher Paper zusammen." |
| 🎯 **Marketing-Assistent** | "Erstelle kreative Kampagnentexte im informellen Stil." |

🚀 **Relevanz für die KI-Interaktion**
- Nutzer haben **volle Kontrolle über das Verhalten der KI**.
- Unterschiedliche **Use Cases können innerhalb einer Plattform** genutzt werden.
- Durch **gespeicherte Kontexte** wird die Nutzung über mehrere Sitzungen hinweg kohärent.

**📌 Fazit:**  
Die Kontextintegration ist ein **zentraler Mechanismus**, um eine KI zielgerichtet und **regelkonform zu steuern**.  
CAIR4 nutzt diesen Ansatz, um eine **modulare, flexible und regulierbare KI-Interaktion** zu ermöglichen.

=================================================
</description>
"""

# Importiere Streamlit aus der eigenen Bibliothek `pylibs.streamlit_lib`
from pylibs.streamlit_lib import streamlit as st

# Importiere verschiedene Utility-Manager für Sessions, Metriken und Nachrichten
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_metrics_manager import update_metrics
from utils.core.CAIR4_message_manager import append_message

# Importiere den Haupt-Controller für die Verarbeitung von Nutzeranfragen
from controllers.CAIR4_controller import handle_query

def render_context_chat_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):

    """
    Rendert den kontextsensitiven Chat-View.
    Dies ermöglicht Nutzern, in einem Chat mit einer KI zu interagieren, 
    die auf einen spezifischen Kontext ausgerichtet ist.
    
    Parameter:
    - use_case (str): Der aktuell ausgewählte Anwendungsfall.
    - context (dict): Enthält verschiedene Kontexte mit Beschreibungen und System-Nachrichten.
    - session_file (str): Der Pfad zur Datei, in der Chat-Sitzungen gespeichert werden.
    - model_name (str): Der Name des verwendeten KI-Modells.
    - settings (dict): Enthält verschiedene Parameter für das Modell, z. B. Temperatur und Antwortlänge.
    """

    # Hauptansicht
    st.subheader(title)

    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)


    # **1️⃣ Initialisierung von Session-Variablen**
    # Diese Variablen bleiben über die gesamte Laufzeit des Chats erhalten.

    if "context_chat_messages" not in st.session_state:
        st.session_state.context_chat_messages = []  # Speichert die Nachrichten im aktuellen Chatverlauf
    
    if "selected_context" not in st.session_state:
        st.session_state.selected_context = "None"  # Standardmäßig kein Kontext gesetzt

    # Lade gespeicherte Sitzungen aus der Session-Datei
    sessions = load_sessions(session_file)

    # Falls `universal_sessions` noch nicht existiert, erstelle es
    st.session_state.setdefault("universal_sessions", {})
    
    # Weise die geladenen Sitzungen dem aktuellen Use Case zu
    st.session_state.universal_sessions[use_case] = sessions

    # **2️⃣ Initialisierung der aktuellen Sitzung**
    # Falls der aktive Use Case gewechselt wurde, wird eine neue Sitzung erstellt.
    if "active_use_case" not in st.session_state or st.session_state["active_use_case"] != use_case:
        st.session_state["active_use_case"] = use_case
        st.session_state["current_session"] = {
            "messages": [],  # Nachrichtenverlauf der aktuellen Sitzung
            "metrics": {  # Metriken zur Nutzung des Modells
                "total_tokens": 0,  # Gesamtzahl der verwendeten Token
                "total_costs": 0.0,  # Gesamtkosten
                "tokens_used_per_request": [],  # Token-Nutzung pro Anfrage
                "costs_per_request": [],  # Kosten pro Anfrage
                "request_names": [],  # Namen der Anfragen
            },
        }

    # Sicherstellen, dass `context_config` eine gültige Konfigurationsdatei ist
    if not isinstance(context, dict):
        st.error("Fehler: Ungültige Kontextkonfiguration.")
        return

    # Alle verfügbaren Kontexte als Liste extrahieren
    context_options = list(context.keys())

    # Kontext-Auswahlbox (Dropdown-Menü)
    selected_context = st.selectbox(
        "Wähle einen Kontext und stelle eine beliebige Frage (z.B. 'Was ist ein Risiko?'):", 
        context_options, 
        index=context_options.index(st.session_state.get("selected_context", "None"))
    )

    # Speichern des ausgewählten Kontexts in der Session-Variable
    st.session_state.selected_context = selected_context

    # Beschreibung des ausgewählten Kontexts anzeigen
    context_details = context.get(
        selected_context, 
        {"description": "Kein Kontext verfügbar.", "system_message": "General-purpose AI."}
    )
    st.info(context_details["description"])

    # **3️⃣ Sidebar für die Auswahl des Kontexts**
    with st.sidebar:
        # **4️⃣ Sitzungen laden und anzeigen**
        sessions = load_sessions(session_file) or []

        # Sicherstellen, dass die geladene Datei tatsächlich eine Liste ist
        if not isinstance(sessions, list):
            st.error("Fehler: Ungültige Sitzungsdaten.")
            sessions = []

    # **6️⃣ Nachrichtenverlauf anzeigen**
    for message in st.session_state.context_chat_messages:
        with st.chat_message(message["role"]):  # Nachricht im Chat-Fenster darstellen
            st.markdown(message["content"])

    # **7️⃣ Eingabefeld für die Nutzerfrage**
    if prompt := st.chat_input("Frage stellen:"):
        with st.chat_message("user"):  # Nachricht als Nutzer-Input speichern
            st.markdown(prompt)

        # Nachricht in den aktuellen Sitzungsverlauf einfügen
        append_message(st.session_state["current_session"], "user", prompt)

        # **8️⃣ Verarbeitung der Anfrage**
        try:
            # Hole die Systemnachricht für den gewählten Kontext
            system_message = context[selected_context]["system_message"]

            with st.chat_message("assistant"):
                with st.spinner("Verarbeite Anfrage..."):
                    response, tokens_used, costs, _ = handle_query(
                        query=prompt,
                        use_case=use_case,
                        context=context_details,
                        model_name=model_name,
                    )

                    # **Antwort der KI anzeigen**
                    st.markdown(response)

                    # Antwort der Sitzung hinzufügen
                    append_message(st.session_state["current_session"], "assistant", response)

                    # **9️⃣ Aktualisierung der Metriken**
                    update_metrics(
                        st.session_state["current_session"]["metrics"],
                        tokens_used=tokens_used,
                        costs=costs,
                    )

                    # **🔟 Sitzung speichern**
                    st.session_state.universal_sessions[use_case].append(st.session_state["current_session"])
                    save_sessions(session_file, st.session_state.universal_sessions[use_case])

        except Exception as e:
            st.error(f"Fehler: {e}")