"""
=================================================
💬 CAIR4 Session Memory Chat View
=================================================

📌 Beschreibung:
Dieses Modul verwaltet **kontextbewusstes Multi-Prompt-Chatten**, indem es 
Sitzungsverläufe speichert und eine optimierte Konversationshistorie bereitstellt.

🎯 Hauptfunktionen:
- **render_session_memory_chat_view()** → Hauptansicht für den Thread-basierten Chat.
- **generate_optimized_context()** → Erstellt eine gekürzte Version der letzten Nachrichten für besseren Kontext.
- **summarize_messages()** → Fasst ältere Nachrichten zusammen, um den Kontext kompakter zu gestalten.

✅ Warum ist das wichtig?
- **Effiziente Nutzung von Token** → Nicht alle Nachrichten müssen erneut gesendet werden.
- **Optimierter Kontext** → Wichtige Inhalte bleiben erhalten, weniger relevante werden gekürzt.
- **Nahtlose User Experience** → Sitzungsverläufe ermöglichen eine langfristige Interaktion.
"""

# === 1️⃣ Importiere erforderliche Bibliotheken ===
from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json as json

# === 2️⃣ Importiere interne Module ===
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics
from utils.core.CAIR4_update_sidebar import update_sidebar

from controllers.CAIR4_controller import handle_query


# === 3️⃣ Hauptansicht für den Thread-Chat ===
def render_session_memory_chat_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    """
    Rendert den **Thread-basierten Chat**, verwaltet Sitzungsverläufe und optimiert den Kontext.
    """

    # **🗂 Sitzungen laden**
    sessions = load_sessions(session_file)
    st.session_state.setdefault("thread_sessions", {})
    st.session_state.thread_sessions[use_case] = sessions

    # **🔄 Falls kein aktiver Use Case existiert oder sich ändert, zurücksetzen**
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

    # **🔄 Verhindern, dass alte Nachrichten doppelt erscheinen**
    messages = st.session_state["current_session"].get("messages", [])
    displayed_messages = set()  # Set zur Kontrolle, welche Nachrichten bereits gerendert wurden

    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    # **👀 Nur die letzten relevanten Nachrichten anzeigen**
    for msg in messages[-5:]:  # Letzte 5 Nachrichten
        if msg["content"] not in displayed_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
            displayed_messages.add(msg["content"])  # Verhindert doppelte Anzeige

    # **📝 Benutzer-Input**
    prompt = st.chat_input(f"💡 Frage zu {use_case} stellen:")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        append_message(st.session_state["current_session"], "user", prompt)

        try:
            with st.chat_message("assistant"):
                with st.spinner("🔄 Anfrage wird verarbeitet..."):

                    # **🧠 Generiere optimierten Kontext**
                    context = generate_optimized_context(st.session_state["current_session"], max_length=2000)

                    response, tokens_used, costs, references = handle_query(
                        query=prompt,
                        context=context, 
                        use_case=use_case,
                        model_name=model_name,
                    )

                    st.markdown(response)
                    append_message(st.session_state["current_session"], "assistant", response)

                    # **📊 Metriken aktualisieren**
                    update_metrics(
                        st.session_state["current_session"]["metrics"],
                        tokens_used=tokens_used,
                        costs=costs,
                    )

                    # **💾 Sitzung speichern**
                    st.session_state.thread_sessions[use_case].append(st.session_state["current_session"])
                    save_sessions(session_file, st.session_state.thread_sessions[use_case])

        except Exception as e:
            st.error(f"⚠️ Fehler: {e}")

# === 4️⃣ Kontext-Optimierung ===
def generate_optimized_context(thread, max_length):
    """
    Generiert einen **optimierten Konversationskontext**, indem ältere Nachrichten zusammengefasst und nur die letzten behalten werden.

    Args:
        thread (dict): Der aktuelle Konversationsverlauf.
        max_length (int): Maximale Länge des finalen Kontexts.

    Returns:
        str: Optimierter Konversationsverlauf für die KI.
    """

    messages = thread["messages"]
    if not messages:
        return ""  # Kein Kontext verfügbar

    # **🚀 Letzte 5 Nachrichten direkt beibehalten**
    recent_messages = messages[-5:]

    # **📜 Ältere Nachrichten zusammenfassen**
    older_messages = messages[:-5]
    summary = summarize_messages(older_messages) if older_messages else ""

    # **🔗 Kombinierte Nachrichten zusammenführen**
    combined_context = summary + "\n" + "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in recent_messages]
    )

    # **✂️ Kürzen, falls nötig**
    if len(combined_context) > max_length:
        combined_context = combined_context[-max_length:]

    return combined_context


# === 5️⃣ Zusammenfassung älterer Nachrichten ===
def summarize_messages(messages):
    """
    Erstellt eine kompakte **Zusammenfassung** älterer Nachrichten, um den Kontext zu erhalten, aber die Token-Nutzung zu minimieren.

    Args:
        messages (list): Liste der vorherigen Nachrichten.

    Returns:
        str: Zusammengefasste Nachricht.
    """

    summary = "📜 **Zusammenfassung vorheriger Nachrichten:**\n"
    for msg in messages:
        summary += f"- {msg['role'].capitalize()}: {msg['content'][:50]}...\n"
    return summary

