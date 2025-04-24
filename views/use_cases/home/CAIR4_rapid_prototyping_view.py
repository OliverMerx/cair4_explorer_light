"""
=================================================
🎉 CAIR4 Info zur Hinterlegung eigener APIs
=================================================

Dieser View dient Hinweis, dass eigene API-Keys hinterlegt werden müssen, um die verschiedenen KI-Modelle nutzen zu können.
"""
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.importlib_lib  import importlib
from pylibs.pandas_lib import pandas as pd

# === 📂 Pfad zur Config-Datei ===
CONFIG_FILE = "/core/CAIR4_explorer_config.py"

# ✅ **Lädt die verfügbaren Modelle aus der Konfiguration**
def load_config():
    path = st.session_state.base_path + CONFIG_FILE
    spec = importlib.util.spec_from_file_location("config_module", path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    
    return config_module.MODEL_OPTIONS  # Muss in der Config definiert sein

# ✅ **API-Key Speicherstruktur nach Anbieter gruppiert**
API_PROVIDERS = {
    "OpenAI": ["GPT-4.1", "GPT-4o", "GPT-3.5"],
    "Gemini": ["Gemini 1.5 Flash", "Gemini 1.5 Pro"],
    "Mistral": ["Mistral Large", "Mistral Next"],
    "Anthropic": ["Claude 3.5", "Claude Haiku"],
    "Deepseek": ["Deepseek Chat", "Deepseek Stream"],
    "groq": ["llama", "Qwen"]
}

# ✅ Falls Nutzer bereits Keys hinterlegt hat, überschreiben
if "api_keys" not in st.session_state:
    st.session_state["api_keys"] = {
        "OpenAI": os.getenv("OPENAI_API_KEY", ""),
        "Gemini": os.getenv("GEMINI_API_KEY", ""),
        "Mistral": os.getenv("MISTRAL_API_KEY", ""),
        "Anthropic": os.getenv("CLAUDE_API_KEY", ""),
        "Deepseek": os.getenv("DEEPSEEK_API_KEY", ""),
        "Groq": os.getenv("GROQ_API_KEY", "")
    }

# ✅ **Willkommens-View mit API-Key-Übersicht**
def render_api_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):

    # 🔄 **Modelle aus der Config laden**
    #model_options = load_config()

    st.subheader(title)
    st.write(description)

    # 🔄 **Erstelle API-Key Status-Tabelle mit Gruppierung**
    key_status = []
    for provider, models in API_PROVIDERS.items():
        key_status.append({
            "Anbieter": provider,
            "Genutzte Modelle": ", ".join(models),
            "API-Key": "✅ Vorhanden" if st.session_state["api_keys"].get(provider, "") else "❌ Nicht vorhanden"
        })

    df_keys = pd.DataFrame(key_status)

    # 📌 **Zeige API-Key Tabelle**
    st.write("### 🔍 Status der API-Keys")
    st.dataframe(df_keys, use_container_width=True)

    # 📌 **Key hinzufügen (falls nicht vorhanden)**
    st.write("### ➕ API-Keys hinzufügen")
    for provider in API_PROVIDERS.keys():
        if not st.session_state["api_keys"].get(provider, ""):
            new_key = st.text_input(f"🔑 {provider} API-Key eingeben:", type="password")
            if new_key:
                st.session_state["api_keys"][provider] = new_key
                st.success(f"✅ API-Key für {provider} gespeichert!")

    # 📌 **Hinweis für Nutzer**
    st.info("ℹ️ API-Keys werden nur temporär gespeichert. Nach einem Neustart müssen sie erneut eingegeben werden.")
