import streamlit as st
from duckduckgo_search import DDGS
from controllers.CAIR4_controller import handle_query
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_metrics_manager import update_metrics

# === Session-Init
if "webchat_messages" not in st.session_state:
    st.session_state.webchat_messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-4o"

# === CAIR4 Web Agent View ===
def render_web_search_chat_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)

    with st.expander("**Use Case Beschreibung**", expanded=False):
        st.markdown(description)

    # === Verlauf anzeigen
    for msg in st.session_state.webchat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # === Neue Eingabe
    user_input = st.chat_input("🌐 Stelle eine Frage mit Webbezug...")
    if user_input:
        st.session_state.webchat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("🔎 Suche im Web..."):
                try:
                    with DDGS() as ddgs:
                        query = f"CAIR4 {user_input}" if "cair4" not in user_input.lower() else user_input
                        search_results = ddgs.text(query, max_results=5)
                    if not search_results:
                        web_context = "Keine relevanten Web-Ergebnisse gefunden."
                    else:
                        web_context = "\n\n".join(
                            [f"**{r['title']}**\n{r.get('body', '')}\n🔗 {r['href']}" for r in search_results if r.get("href")]
                        )
                except Exception as e:
                    web_context = f"Fehler bei der Websuche: {e}"

            # === GPT-Antwort generieren
            with st.spinner("🧠 Generiere KI-Antwort..."):
                prompt = f"""
Ein Nutzer hat folgende Frage gestellt:
\"{user_input}\"

Hier sind die 5 relevantesten Web-Ergebnisse von DuckDuckGo:

{web_context}

Bitte beantworte die Frage basierend auf den Web-Inhalten. Wenn keine Informationen passen, formuliere eine höfliche Antwort.
"""

                response, *_ = handle_query(
                    query=prompt,
                    model_name=st.session_state.get("selected_model", "gpt-4o"),
                    use_case="web_search_chat",
                    context={}
                )

                st.markdown(response)

                # 🔗 DuckDuckGo-Ergebnisse separat anzeigen
                if search_results:
                    with st.expander("🔗 Web-Ergebnisse (DuckDuckGo)", expanded=False):
                        for r in search_results:
                            title = r.get("title", "Kein Titel")
                            url = r.get("href", "#")
                            body = r.get("body", "")
                            st.markdown(f"**[{title}]({url})**  \n{body[:250]}...")

                st.session_state.webchat_messages.append({"role": "assistant", "content": response})
                st.session_state.webchat_messages.append({"role": "assistant", "content": response})

                # === Metriken & Session speichern
                update_metrics(st.session_state.get("internet_chat_metrics", {}), tokens_used=0, costs=0)
                save_sessions(session_file or "internet_chat_sessions.json", st.session_state.webchat_messages)