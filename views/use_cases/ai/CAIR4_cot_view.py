# pylibs
from pylibs.streamlit_lib import streamlit as st

# utils
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_metrics_manager import update_metrics
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_debug_utils import DebugUtils  # Import der Debug-Klasse

# models
from models.core.CAIR4_chromadb_client import get_or_create_collection
from models.core.CAIR4_collection_client import list_collection_contents

# controller
from controllers.CAIR4_controller import handle_query


def render_cot_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    """
    Rendert den 'Chain of Thought' (CoT) View mit schrittweisem logischen Denken.
    """

    # Hauptansicht
    st.subheader(title)
    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    # **Session-Daten initialisieren**
    sessions = load_sessions(session_file)
    st.session_state.setdefault("cot_sessions", {})
    st.session_state.cot_sessions[use_case] = sessions

    # **Aktuelle CoT-Session initialisieren**
    if "active_use_case" not in st.session_state or st.session_state["active_use_case"] != use_case:
        st.session_state["active_use_case"] = use_case
        st.session_state["current_cot_session"] = {
            "cot_steps": [],  # Speichert die einzelnen Gedankenketten
            "metrics": {
                "total_tokens": 0,
                "total_costs": 0.0,
                "tokens_used_per_request": [],
                "costs_per_request": [],
                "request_names": [],
            },
        }


    # **Collection für den Use Case abrufen**
    DebugUtils.debug_print(f"(📌 DEBUG - COT Collection Type: {type(collection)}")
    try:
        collection = get_or_create_collection(use_case)        
        collection_contents = list_collection_contents(use_case)  
    except Exception as e:
        st.error(f"Fehler beim Laden der Collection für '{use_case}': {e}")
        collection_contents = []

    # **Vorherige Schritte der Argumentation anzeigen**
    for step_num, step in enumerate(st.session_state["current_cot_session"]["cot_steps"], start=1):
        with st.expander(f"Schritt {step_num}: {step['question']}"):
            st.markdown(f"**Antwort:** {step['answer']}")
    
    # **Nutzerinput für die nächste Denkstufe**
    if prompt := st.text_input(f"Stelle eine neue Frage für {use_case}:"):
        # ❗ Vorherige Denk-Schritte zurücksetzen
        st.session_state["current_cot_session"]["cot_steps"] = []
        with st.spinner("Denke in mehreren Schritten..."):
            try:
                 
                # **CoT-Aufforderung an das Modell**  
                cot_prompt = f"""
                Denke Schritt für Schritt. 
                Neue Frage: {prompt}
                Antworte in mehreren logischen Schritten.
                """
                
                response_steps = ""
                structured_steps = []
                response, tokens_used, costs, _ = handle_query(
                    query=cot_prompt,
                    use_case=use_case,
                    context=context,
                    model_name=model_name,
                )

                # **Antwort in Schritte zerlegen**
                response_steps = response.split("\n")  # Modell gibt oft Schritte als Zeilen zurück
                structured_steps = [{"question": prompt, "answer": step.strip()} for step in response_steps if step.strip()]

                # **Jeder Schritt wird als Expander direkt unter der Antwort angezeigt**
                for i, step in enumerate(structured_steps):
                    if step is not "":
                        with st.expander("Chain of thoughts:", expanded=True):
                            st.markdown(step["answer"])

                # **Neue Schritte speichern**
                #st.session_state["current_cot_session"]["cot_steps"].extend(response_steps)

                # **Metriken aktualisieren**
                update_metrics(
                    st.session_state["current_cot_session"]["metrics"],
                    tokens_used=tokens_used,
                    costs=costs,
                )

                # **Session speichern**
                st.session_state.cot_sessions[use_case].append(st.session_state["current_cot_session"])
                save_sessions(session_file, st.session_state.cot_sessions[use_case])

            except Exception as e:
                st.error(f"Fehler: {e}")

