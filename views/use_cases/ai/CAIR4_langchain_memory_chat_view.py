"""
=================================================
🧠 CAIR4 Langchain Memory Chat View
=================================================

📌 **Unterschiede zu `Session Memory Chat View`**
Dieses Modul kombiniert **Langchains `ConversationBufferMemory`** mit **CAIR4-Session-Speicherung**.
Dadurch wird sichergestellt, dass:
1️⃣ **Langchain Memory** den Chatverlauf für die aktuelle Sitzung speichert.  
2️⃣ **CAIR4 Sessions** das gesamte Gespräch persistent abspeichert, sodass es auch nach einem Neustart der Anwendung erhalten bleibt.

✅ **Warum kombinieren?**
- **Langchain `ConversationBufferMemory`** speichert den Verlauf im RAM. Wenn der Server abstürzt, ist alles weg.
- **CAIR4 `Session State + JSON-Speicherung`** sichert die Daten in Dateien.
- Diese Kombination erlaubt **eine effiziente, speicherfreundliche Nutzung des Langchain Memory** ohne Token-Overhead.
"""

# === 1️⃣ Importiere erforderliche Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

# === 2️⃣ Importiere interne CAIR4-Module ===
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics

# === 3️⃣ KI-Model initialisieren ===
MODEL_NAME = "gpt-4o"  # Falls du ein anderes Modell möchtest, hier ändern
llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

# === 4️⃣ Conversation Memory & Kettenaufbau ===
def setup_memory_chain():
    """ Erstellt eine Langchain `ConversationBufferMemory` mit dem erwarteten `history` Schlüssel. """
    if "chat_memory" not in st.session_state:
        st.session_state.chat_memory = ConversationBufferMemory(memory_key="history")  # 🔥 **Fix: Jetzt bleibt Memory erhalten**
    
    chain = ConversationChain(llm=llm, memory=st.session_state.chat_memory, verbose=False)
    return chain

# === 5️⃣ Hauptansicht für den Chat mit Memory & Session-Persistenz ===
def render_langchain_memory_chat_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    """
    Kombiniert Langchains `ConversationBufferMemory` mit CAIR4-Session-Management,
    um sowohl **kurzfristige** als auch **langfristige** Chatverläufe zu ermöglichen.
    """

    # **📂 Sitzungsladen aus JSON**
    sessions = load_sessions(session_file)
    st.session_state.setdefault("memory_sessions", {})
    st.session_state.memory_sessions[use_case] = sessions

    # **🧠 Langchain Memory initialisieren**
    chain = setup_memory_chain()

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

    # **🔄 Nachrichtenverlauf anzeigen (Letzte 5)**
    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    for msg in st.session_state["current_session"]["messages"][-5:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # **📝 Benutzer-Input**
    prompt = st.chat_input(f"💡 Frage zu {use_case} stellen:")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        append_message(st.session_state["current_session"], "user", prompt)

        try:
            with st.chat_message("assistant"):
                with st.spinner("🔄 Denke nach..."):

                    # **🚀 Langchain Memory verwenden**
                    response = chain.invoke({"input": prompt})

                    # 🔍 **Key absichern, falls `response` nicht existiert**
                    answer = response.get("response", "❌ Fehler beim Abrufen der Antwort")

                    st.markdown(answer)
                    append_message(st.session_state["current_session"], "assistant", answer)

                    # **📊 Metriken aktualisieren**
                    update_metrics(
                        st.session_state["current_session"]["metrics"],
                        tokens_used=0,  # Langchain speichert keine Token-Daten
                        costs=0.0,  # Kostenberechnung optional
                    )

                    # **💾 Sitzung speichern**
                    st.session_state.memory_sessions[use_case].append(st.session_state["current_session"])
                    save_sessions(session_file, st.session_state.memory_sessions[use_case])

        except Exception as e:
            st.error(f"⚠️ Fehler: {e}")