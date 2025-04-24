"""
================================
💡 CAIR4 Prompting Typen
================================
"""
import streamlit as st
from controllers.CAIR4_controller import handle_query

# Beispiel-Prompts + Erklärungen
PROMPT_TYPES = {
    "Instruktion": {
        "prompt": "Erkläre Paris einem Kind.",
        "description": "Ein klarer Auftrag an das Modell."
    },
    "Formatierter Output": {
        "prompt": "Erstelle eine Tabelle mit 3 KI-Modellen inklusive Beschreibung und Jahr.",
        "description": "Ideal, wenn strukturierte Antworten erwartet werden."
    },
    "Rollenprompting": {
        "prompt": "Handle als Lehrer und erkläre einem Schüler, was ein Neuronales Netz ist.",
        "description": "Simuliert eine Rolle oder Persona."
    },
    "Few-Shot Prompting": {
        "prompt": "Beispiel: Katze → Tier\nBeispiel: Auto → Fahrzeug\nFrage: Apfel → ?",
        "description": "Mit Beispielen lernen lassen, wie die Antwort aussehen soll."
    },
    "Wissensabfrage": {
        "prompt": "Was ist der Unterschied zwischen KI und Machine Learning?",
        "description": "Fachwissen aus dem Modell abrufen."
    }
}

def render_prompting_typen_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    # Session init
    st.session_state.setdefault("prompting_chat", [])
    st.session_state.setdefault("prompting_metrics", {
        "total_tokens": 0,
        "total_costs": 0.0,
        "tokens_used_per_request": [],
        "costs_per_request": [],
    })

    # Typ-Auswahl
    selected_type = st.selectbox("Wähle einen Prompt-Typ", list(PROMPT_TYPES.keys()))
    st.markdown(f"🧠 **Erklärung:** {PROMPT_TYPES[selected_type]['description']}")
    example_prompt = st.text_area("✏️ Beispielprompt (anpassbar)", value=PROMPT_TYPES[selected_type]["prompt"], height=120)

    # Verlauf anzeigen
    for msg in st.session_state.prompting_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Prompt abschicken
    if st.button("✅ Prompt ausführen"):
        prompt = example_prompt.strip()
        if prompt:
            st.session_state.prompting_chat.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                with st.chat_message("assistant"):
                    with st.spinner("Antwort wird generiert..."):
                        response, tokens_used, costs, _ = handle_query(
                            query=prompt,
                            use_case=use_case,
                            context=context,
                            model_name=model_name,
                        )

                        st.markdown(response)
                        st.session_state.prompting_chat.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Fehler: {e}")