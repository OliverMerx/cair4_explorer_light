"""
===========================================================
Gemini API Client (query_gemini.py)
===========================================================

Dieses Modul stellt eine Schnittstelle zur **Gemini API** bereit und ermöglicht 
die Verarbeitung von Benutzeranfragen mit kontextabhängigen Prompts.

📌 Funktionen:
- **query_gemini()** → Sendet eine Anfrage an Gemini mit Kontext.
- **Automatische Fehlerbehandlung** → Fängt API-Fehler ab und gibt sinnvolle Rückgaben.

✅ Warum ist das wichtig?
- Ermöglicht eine direkte Kommunikation mit **Gemini 1.5 Flash** (oder anderen Modellen).
- Unterstützt kontextbasierte Konversationen.
- Vereinfacht die API-Integration mit Fehlerbehandlung.
"""

from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.load_dotenv_lib import initialize_load_dotenv

from dotenv import find_dotenv

load_dotenv = initialize_load_dotenv()
load_dotenv(find_dotenv())


# **Definiere ALLE API-Keys für verschiedene Modelle**
API_KEYS = {
    "Mistral": os.getenv("MISTRAL_API_KEY", ""),
    "Gemini": os.getenv("GEMINI_API_KEY", ""),
    "Deepseek": os.getenv("DEEPSEEK_API_KEY", ""),
    "Anthropic": os.getenv("CLAUDE_API_KEY", ""),
    "OpenAI": os.getenv("OPENAI_API_KEY",""),
    "QWEN": os.getenv("QWEN_API_KEY",""),
    "GROQ": os.getenv("GROQ_API_KEY",""),
    "CAIR4": os.getenv("CAIR4_ENCRYPTION_KEY","")
}

# **Falls Nutzer eigene Keys gespeichert hat, überschreibe die Default-Werte**
if "api_keys" in st.session_state:
    for key_name in API_KEYS.keys():
        user_key = st.session_state["api_keys"].get(key_name) or st.session_state["api_keys"].get(key_name.capitalize()) or st.session_state["api_keys"].get(key_name.lower()) or ""
        if user_key:
            API_KEYS[key_name] = user_key

# **Raise Fehler, falls ein API-Key fehlt**
for key, value in API_KEYS.items():
    if not value:
        print(f"⚠️ Warnung: Kein API-Key für {key} gesetzt!")

# **Getter-Funktion für API-Keys**
def get_api_key(model_name):
    if "gemini" in model_name.lower():
        return API_KEYS["Gemini"]
    elif "deepseek" in model_name.lower():
        return API_KEYS["Deepseek"]
    elif "mistral" in model_name.lower():
        return API_KEYS["Mistral"]
    elif "anthropic" in model_name.lower():
        return API_KEYS["Anthropic"]
    elif "openai" in model_name.lower():
        return API_KEYS["OpenAI"]
    elif "qwen" in model_name.lower():
        return API_KEYS["QWEN"]
    elif "deepl" in model_name.lower():
        return API_KEYS["DEEPL"]
    elif "hugging" in model_name.lower():
        return API_KEYS["HUGGINGFACE"]
    elif "groq" in model_name.lower():
        return API_KEYS["GROQ"]
    elif "cair4" in model_name.lower():
        return API_KEYS["CAIR4"]
    return None  # GPT-Modelle brauchen keinen API-Key