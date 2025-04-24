import streamlit as st
import ast
import time
from controllers.CAIR4_controller import handle_query
from utils.core.CAIR4_debug_utils import DebugUtils

def generate_token_prompt(text):
    return f'''
Zerlege bitte den folgenden Satz in einzelne Tokens so, wie dein Sprachmodell sie intern verwendet. 
Gib mir ausschließlich eine Liste der Tokens in der Reihenfolge, in der du sie verarbeitet hast.
Antwort bitte nur mit der Tokenliste, ohne Kommentare oder Erklärungen.

Text:
"{text}"
'''.strip()

def get_token_response(model_name, prompt, use_case):
    try:
        response, _, _, _ = handle_query(
            query=prompt,
            use_case=use_case,
            context="",
            model_name=model_name,
        )
        return response.strip()
    except Exception as e:
        return f"Fehler: {e}"

def render_token_compare_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    MODEL_OPTIONS = st.session_state.get("model_options", {})
    MODEL_LABELS = list(MODEL_OPTIONS.keys())
    MODEL_MAP = MODEL_OPTIONS
    REVERSE_MODEL_MAP = {v: k for k, v in MODEL_OPTIONS.items()}

    if "model_selection" not in st.session_state or not isinstance(st.session_state.model_selection, list):
        st.session_state.model_selection = []

    # 🧠 Initialvorgabe sinnvoll setzen
    initial_models = ["deepseek-api", "gemini-1.5-flash", "gpt-4"]
    st.session_state.model_selection = [
        model for model in initial_models if model in MODEL_MAP.values()
    ]
    while len(st.session_state.model_selection) < 3:
        available = [m for m in MODEL_MAP.values() if m not in st.session_state.model_selection]
        if available:
            st.session_state.model_selection.append(available[0])
        else:
            break

    # Eingabefeld für Token-Text
    prompt_text = st.text_area("📬 Eingabetext zur Tokenisierung", "Donaudampfschifffahrtsgesellschaft.")
    token_prompt = generate_token_prompt(prompt_text)

    # 📌 Auswahl der Modelle
    selected_models = []
    cols = st.columns(3)
    for i, col in enumerate(cols):
        with col:
            default_model_id = st.session_state.model_selection[i] if i < len(st.session_state.model_selection) else None
            default_label = REVERSE_MODEL_MAP.get(default_model_id, MODEL_LABELS[0]) if default_model_id else MODEL_LABELS[0]
            selected_label = st.selectbox(
                f"Modell {i+1}",
                options=MODEL_LABELS,
                index=MODEL_LABELS.index(default_label),
                key=f"model_select_{i}"
            )
            selected_models.append(MODEL_MAP[selected_label])

    st.session_state.model_selection = selected_models

    # Nur fortfahren, wenn alle Modelle korrekt gesetzt
    all_valid = all(model in MODEL_MAP.values() for model in selected_models)
    if not all_valid or len(selected_models) < 3:
        st.warning("⚠️ Nicht genügend gültige Modelle ausgewählt.")
        return

    # Anfrage ausführen
    if st.button("🔄 Anfrage absenden und Token vergleichen"):
        result_dict = {}
        with st.spinner("⏳ Tokens werden generiert..."):
            for idx, model_id in enumerate(selected_models):
                response = get_token_response(model_id, token_prompt, use_case)
                result_dict[model_id] = response
            st.session_state["token_compare_result"] = result_dict

    # Ergebnisse anzeigen
    if "token_compare_result" in st.session_state:
        st.divider()
        for idx, model_id in enumerate(selected_models):
            model_label = REVERSE_MODEL_MAP.get(model_id, model_id)
            response = st.session_state["token_compare_result"].get(model_id, "Keine Antwort erhalten.")

            with st.container(border=True):
                st.markdown(f"#### 🧬 Modell: `{model_label}`")
                key_suffix = f"{model_id.replace('/', '_')}_{idx}"

                if response.startswith("["):
                    try:
                        tokens = ast.literal_eval(response)
                        for i, token in enumerate(tokens):
                            st.markdown(f"{i+1}. `{token}`")
                    except Exception as parse_error:
                        st.error(f"Parsing-Fehler: {parse_error}")
                        st.text_area("Raw Response", response, key=f"raw_{key_suffix}")
                else:
                    st.warning("Achtung: Die Tokenliste wurde vermutlich in Textform erhalten.")
                    st.text_area("Antwort:", response, key=f"fallback_{key_suffix}")