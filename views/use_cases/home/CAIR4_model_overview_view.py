import streamlit as st
from core.CAIR4_explorer_config_raw import API_MODEL_OPTIONS, LOCAL_MODEL_OPTIONS 

def render_model_overview_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):

    st.subheader(title)
    # API-Modelle
    api_models = API_MODEL_OPTIONS
    local_models = LOCAL_MODEL_OPTIONS
    
    total_models = len(api_models) + len(local_models)
    st.write(description)
    st.write(f"Aktuell können **{total_models-1} KI-Modelle** mit allgemeinem Verwendungszweck angebunden werden.")


    # === API-Modelle ===
    with st.expander("🌐 Externe API-Modelle (z. B. OpenAI, Google, Anthropic)", expanded=True):
        first = True
        for key, model in api_models.items():
            if first:
                first = False
                continue  # Überspringt die erste Iteration
            if not model.get("enabled", True):
                continue
            st.markdown(f"#### 🔸 {model['label']}")
            st.markdown(f"- Anbieter: **{model['provider']}**")
            if model.get("description"):
                st.markdown(model["description"])
            if model.get("tags"):
                st.markdown("  " + " ".join([f"`{tag}`" for tag in model["tags"]]))
            if model.get("link"):
                st.markdown(f"[🌐 Mehr erfahren]({model['link']})", unsafe_allow_html=True)
            st.divider()

    # === Lokale Modelle ===
    with st.expander("💻 Lokale Modelle (laufen auf deinem System)", expanded=True):
        for key, model in local_models.items():
            if not model.get("enabled", True):
                continue
            st.markdown(f"#### 🟢 {model['label']}")
            st.markdown(f"- Anbieter: **{model['provider']}**")
            if model.get("tags"):
                st.markdown("  " + " ".join([f"`{tag}`" for tag in model["tags"]]))
            if model.get("link"):
                st.markdown(f"[🌐 Mehr erfahren]({model['link']})", unsafe_allow_html=True)
            st.divider()