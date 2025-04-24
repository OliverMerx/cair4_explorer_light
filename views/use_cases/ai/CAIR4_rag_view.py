##pylibs
from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json as json

#utils
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics

#models
from models.core.CAIR4_collection_client import list_collection_contents, get_or_create_collection

#controller
from controllers.CAIR4_controller import handle_query

def render_rag_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):

    """
    Rendert die Universal-Ansicht für den gegebenen Use Case.
    """
    # **Sessions laden**
    sessions = load_sessions(session_file)
    st.session_state.setdefault("universal_sessions", {})
    st.session_state.universal_sessions[use_case] = sessions

    # **Initialisiere aktuelle Session**
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

    # Hauptansicht
    st.subheader(title)
    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    # **Collection Contents laden**
    collection = get_or_create_collection(use_case)
    
    #collection_name = collections[use_case]
    collection_contents = list_collection_contents(use_case)      

    for msg in st.session_state["current_session"]["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # **Checkboxen für Suchoptionen**
    exact_match_enabled = st.checkbox("Exakte Suche aktivieren", value=False)
    semantic_search_enabled = st.checkbox("Semantische Suche aktivieren", value=True)

    # **Eingabefeld**
    if prompt := st.chat_input(f"Frage zu {use_case} stellen:"):
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
                    st.markdown(response)
                    append_message(st.session_state["current_session"], "assistant", response)

                    # **Metriken aktualisieren**
                    update_metrics(
                        st.session_state["current_session"]["metrics"],
                        tokens_used=tokens_used,
                        costs=costs,
                    )

                    # **Referenzen anzeigen**
                    if references:
                        display_references(references, collection_contents, exact_match_enabled ,semantic_search_enabled, prompt )

                    # **Session speichern**
                    st.session_state.universal_sessions[use_case].append(st.session_state["current_session"])
                    save_sessions(session_file, st.session_state.universal_sessions[use_case])

        except Exception as e:
            st.error(f"Fehler: {e}")


def update_sidebar(use_case, session_file):
    """
    Aktualisiert die Sidebar für Sessions eines Use Cases.
    """
    # **Sessions laden**
    sessions = load_sessions(session_file)

    # **Dropdown-Optionen erstellen**
    session_labels = [
        f"Session {i + 1}: {sess['messages'][0]['content'][:30]}"
        for i, sess in enumerate(sessions) if sess["messages"]
    ]
    dropdown_options = ["Keine"] + session_labels

    # **Dropdown anzeigen**
    chosen_session = st.selectbox(
        "Gespeicherte Sessions",
        dropdown_options,
        index=st.session_state.get(f"{use_case}_selected_index", 0),
        key=f"{use_case}_dropdown"
    )

    # **Dropdown-Auswahl verarbeiten**
    if chosen_session != "Keine":
        selected_index = dropdown_options.index(chosen_session) - 1
        st.session_state["current_session"] = sessions[selected_index]
        st.session_state[f"{use_case}_selected_index"] = selected_index + 1

    # Buttons hinzufügen
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📝", help="Neue Session starten", key=f"{use_case}_new_session"):
            if st.session_state["current_session"]["messages"]:
                sessions.append(st.session_state["current_session"])
                save_sessions(session_file, sessions)
               
    with col2:
        if st.button("🔄", help="Session zurücksetzen", key=f"{use_case}_reset_session"):
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
    with col3:
        if st.button("🗑️", help="Alle Sessions löschen", key=f"{use_case}_delete_sessions"):
            if os.path.exists(session_file):
                os.remove(session_file)
            st.session_state.universal_sessions[use_case] = []

def exact_text_search(query, collection_contents):
    """
    Führt eine exakte Textsuche in den Referenzen durch.

    Args:
        query (str): Der Suchbegriff.
        references (dict): Ein Wörterbuch mit Dokumenten und deren Inhalten.

    Returns:
        list: Eine Liste mit Treffern, die den Suchbegriff enthalten.
    """
    print(f"USE CASE NAME: {query}    {collection_contents}")
    results = []
    for entry in collection_contents:
        if query.lower() in entry["content"].lower():
            results.append(entry)
    return results


def perform_semantic_search(query, references):
    """
    Führt eine semantische Suche in den Referenzen durch.

    Args:
        query (str): Der Suchbegriff.
        references (dict): Ein Wörterbuch mit Dokumenten und deren Inhalten.

    Returns:
        list: Eine Liste mit Treffern, sortiert nach Relevanz.
    """
    semantic_results = []
    for doc, refs in references.items():
        for ref in refs:
            relevance = ref.get("relevance", 0)
            semantic_results.append({
                "source": doc,
                "page": ref.get("page", "Unknown"),
                "content": ref["text"],
                "relevance": relevance,
            })

    # Sortiere Ergebnisse basierend auf der Relevanz
    semantic_results.sort(key=lambda x: x["relevance"], reverse=True)
    return semantic_results


def display_references(references, collection_contents, exact_match_enabled=False ,semantic_search_enabled=False, query=None):
    """
    Zeigt die Trefferübersicht an.

    Args:
        references (dict): Ein Wörterbuch mit Dokumenten und deren Inhalten.
        exact_matches_only (bool): Wenn True, werden nur exakte Treffer angezeigt.
    """
    # Debugging: Referenzen ausgeben
    print("[DEBUG] References:", references)

    if exact_match_enabled:
        st.markdown("### Exact Matches:")
        exact_matches = exact_text_search(query, collection_contents)
        if exact_matches:
            for match in exact_matches:
                st.markdown(
                    f"- **Document:** {match['name']} **Page:** {match['pages']} **Content:** {match['content']}"
                )
        results = []
    else:
        st.info("No exact matches found.")

    # **Semantic Matches anzeigen**
    st.markdown("### Semantic Matches:")
    if semantic_search_enabled:
        semantic_results = perform_semantic_search(query=st.session_state.get("query", ""), references=references)
        if semantic_results:
            for result in semantic_results:
                color = "green" if result["relevance"] >= 70 else "orange" if result["relevance"] >= 40 else "red"
                st.markdown(
                    f"- **[{result['relevance']:.2f}% Relevance, Page {result['page']}]** {result['content']}",
                    unsafe_allow_html=True
                )
        else:
            st.info("No semantic matches found.")