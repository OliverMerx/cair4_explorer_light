"""
=================================================
💬 CAIR4 Hybrid-Chat für Kreditbewertung
=================================================

📌 **Beschreibung:**
Dieser View kombiniert einen **KI-gestützten Chat** mit einer **regelbasierten Kreditbewertung**.  
- **Chat als zentrale Steuereinheit** → Nutzer fragt & passt Parameter an.
- **Dynamische Kreditbewertung** → Werte ändern sich live.
- **Regulatorische Trennung** → KI liefert Beratung, Berechnung bleibt regelbasiert.

🎯 **Hauptfunktionen:**
- **KI-Chat mit Session-Memory** → Nutzer kann iterativ fragen.
- **Live-Update der Kreditwürdigkeit** → Jede Eingabe löst Neuberechnung aus.
- **Editierbare Kreditparameter** → Werte flexibel anpassbar.
- **Vorschau der Berechnung** → Sofortige Rückmeldung zur Kreditwürdigkeit.

✅ **Warum ist das wichtig?**
- **KI-gestützte Beratung mit klarer Abgrenzung** zur regulierten Berechnung.
- **Erhöhte Transparenz** → Nutzer sieht sofort den Einfluss von Änderungen.
- **Nahtlose Interaktion** zwischen Chat & Finanzbewertung.

"""

# === 1️⃣ Importiere erforderliche Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json
from pylibs.uuid_lib import uuid
import random
import datetime

# === 2️⃣ Importiere interne Module ===
from utils.core.CAIR4_session_manager_hybrid import load_sessions, save_sessions, append_session
from utils.core.CAIR4_update_sidebar import update_sidebar
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics

# === 3️⃣ Haupt-Render-Funktion für den Hybrid-View ===
import random
import datetime
from controllers.CAIR4_controller import handle_query  # ✅ KI-Handler für Anfragen

def render_credit_hybrid_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    """
    📌 **Erweitertes Session-Handling für Hybride Modelle**
    
    ✅ **Unterstützt 3 Szenarien:**
    - **Regelbasierte Berechnungen (`calculation`)** → Scoring-Modelle (z. B. Kreditbewertung)
    - **KI-Abfragen (`query`)** → KI-generierte Antworten (z. B. GPT-4 für Beratung)
    - **Hybride Modelle (`hybrid`)** → Regelbasiert + KI-Optimierung (z. B. Kreditmodell + GPT-Analyse)
    
    🔹 **Parameter:**
    - `use_case`: Name des Anwendungsfalls.
    - `context`: Vorherige Konversation oder Berechnungen.
    - `title`: Titel der View.
    - `description`: Beschreibung des Use Cases.
    - `session_file`: Speicherort der Session.
    """

    # **🗂 Sitzungen laden**
    sessions = load_sessions(session_file)
    st.session_state.setdefault("hybrid_sessions", sessions)

    # **🔄 Falls keine aktive Session existiert, initialisieren**
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

    st.subheader(title)

    with st.expander("**Use Case Beschreibung**"):
        st.write(description)
 
    for msg in st.session_state["current_session"]["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # **📝 Benutzer-Input für Chat**
    prompt = st.chat_input(f"💡 Frage zur Kreditbewertung stellen:")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        append_message(st.session_state["current_session"], "user", prompt)

        try:
            with st.chat_message("assistant"):
                with st.spinner("🔄 Anfrage wird verarbeitet..."):
                    context = generate_optimized_context(st.session_state["current_session"], max_length=2000)
                    response, tokens_used, costs, _ = handle_query(
                        query=prompt,
                        use_case=use_case,
                        context=context,
                        model_name=model_name,
                    )

                    st.markdown(response)
                    append_message(st.session_state["current_session"], "assistant", response)

                    st.session_state.hybrid_sessions.append(st.session_state["current_session"])
                    save_sessions(session_file, st.session_state.hybrid_sessions)
        except Exception as e:
            st.error(f"⚠️ Fehler: {e}")

    # **📊 Kreditbewertung mit Live-Update**
    st.subheader("🏦 Live-Kreditbewertung")
    with st.form("kredit_form"):
        gehalt = st.number_input("💰 Gehalt (€)", min_value=1000, value=3000)
        kreditbetrag = st.number_input("💳 Kreditbetrag (€)", min_value=1000, value=10000)
        laufzeit = st.slider("📆 Laufzeit (Monate)", min_value=6, max_value=120, value=24)
        bonität = st.selectbox("📊 Bonität", ["Exzellent", "Gut", "Mittel", "Schlecht"])
        submitted = st.form_submit_button("📊 Kreditwürdigkeit berechnen")
    
    if submitted:
        score = round((gehalt / kreditbetrag) * 100 - (laufzeit / 12) - (["Schlecht", "Mittel", "Gut", "Exzellent"].index(bonität) * 5), 2)
        result = "Genehmigt" if score > 50 else "Abgelehnt"
        parameters = {"gehalt": gehalt, "kreditbetrag": kreditbetrag, "laufzeit": laufzeit, "bonität": bonität, "score": score, "ergebnis": result}
        append_message(st.session_state["current_session"], "calculation", parameters)
        st.success(f"✅ Kreditprüfung abgeschlossen: {result} (Score: {score})")

def generate_optimized_context(session, max_length=2000):
    """
    Generiert einen optimierten Konversationskontext, indem ältere Nachrichten zusammengefasst
    und nur die letzten relevanten Nachrichten beibehalten werden.

    Args:
        session (dict): Die aktuelle Sitzung mit Nachrichten.
        max_length (int): Maximale Länge des finalen Kontexts für das KI-Modell.

    Returns:
        str: Optimierter Konversationsverlauf für die KI.
    """

    messages = session.get("messages", [])
    if not messages:
        return ""  # Kein Kontext verfügbar

    # 🚀 Letzte 5 Nachrichten direkt beibehalten
    recent_messages = messages[-5:]

    # 📜 Ältere Nachrichten zusammenfassen
    older_messages = messages[:-5]
    summary = summarize_messages(older_messages) if older_messages else ""

    # 🔗 Kombinierte Nachrichten zusammenführen
    combined_context = summary + "\n" + "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in recent_messages]
    )

    # ✂️ Kürzen, falls nötig
    if len(combined_context) > max_length:
        combined_context = combined_context[-max_length:]

    return combined_context


def summarize_messages(messages):
    """
    Erstellt eine kompakte Zusammenfassung älterer Nachrichten.

    Args:
        messages (list): Liste der vorherigen Nachrichten.

    Returns:
        str: Zusammengefasste Nachricht.
    """

    summary = "📜 **Zusammenfassung vorheriger Nachrichten:**\n"
    for msg in messages:
        summary += f"- {msg['role'].capitalize()}: {msg['content'][:50]}...\n"
    return summary

# === 4️⃣ Styling für Streamlit ===
st.markdown("""
<style> 
[data-testid="stBottomBlockContainer"] {
background-color: #ccc !important;
background:transparent!important;
}
</style>
""", unsafe_allow_html=True)
