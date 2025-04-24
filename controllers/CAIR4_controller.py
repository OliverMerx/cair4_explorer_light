"""
=================================================
CAIR4 Query Handler/Controller (CAIR4_controller.py)
=================================================

Dieses Modul verwaltet Benutzeranfragen für die Main-Applikation und leitet sie an das passende 
KI-Modell weiter (z. B. OpenAI, Gemini, DeepSeek). Zudem kann es kontextbezogene 
Referenzen aus ChromaDB abrufen.

Funktionen:
- `handle_query`: Verarbeitet eine Benutzeranfrage und ruft das passende Modell auf.
- Unterstützt OpenAI, Gemini, DeepSeek, llama und ChromaDB.
"""
# ============================================================
# 🧠 CAIR4 Handle Query Controller (Unified)
# ============================================================
"""
Dieses Modul verwaltet Benutzeranfragen für die Main-Applikation und leitet sie an das passende
KI-Modell weiter (z. B. OpenAI, Gemini, DeepSeek, Groq). Zudem können kontextbezogene
Referenzen aus ChromaDB abgerufen werden.
"""

from pylibs.streamlit_lib import streamlit as st
from pylibs.os_lib import os

from models.core.CAIR4_openai_client import query_openai
from models.core.CAIR4_gemini_client import query_gemini
from models.core.CAIR4_llama2_local_client import query_llama2
from models.core.CAIR4_deepseek_client import query_deepseek
from models.core.CAIR4_deepseek_stream import query_deepseek_stream
from models.core.CAIR4_claude_client import query_claude
from models.core.CAIR4_mistral_client import query_mistral
from models.core.CAIR4_qwen_client import query_qwen
from models.core.CAIR4_groq_client import query_groq
from models.core.CAIR4_collection_client import get_or_create_collection

# === .env laden und prüfen ===
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

API_KEYS = {
    "mistral": os.getenv("MISTRAL_API_KEY", ""),
    "gemini": os.getenv("GEMINI_API_KEY", ""),
    "deepseek": os.getenv("DEEPSEEK_API_KEY", ""),
    "claude": os.getenv("CLAUDE_API_KEY", ""),
    "openai": os.getenv("OPENAI_API_KEY", ""),
    "qwen": os.getenv("QWEN_API_KEY", ""),
    "groq": os.getenv("GROQ_API_KEY", ""),
}

st.code(API_KEYS)

def check_model_api_key(model_name: str) -> str | None:
    model_name = model_name.lower()
    for key_fragment, key_value in API_KEYS.items():
        if key_fragment in model_name and not key_value:
            return f"⚠️ Fehlender API-Key für **{key_fragment.upper()}** – bitte `.env` prüfen oder Key in `st.session_state['api_keys']` setzen."
    return None


def parse_think_block(response_text):
    if "<think>" in response_text and "</think>" in response_text:
        try:
            think_content = response_text.split("<think>")[1].split("</think>")[0].strip()
            explanation_block = f"\n\n---\n🧠 **Chain of Thought**:\n```text\n{think_content}\n```\n---\n"
            return response_text.replace(f"<think>{think_content}</think>", explanation_block)
        except Exception as e:
            print(f"[WARNING] Fehler beim Parsen von <think>: {e}")
    return response_text


def handle_query(
    query,
    use_case=None,
    context=None,
    model_name=None,
    override_response_format=None,
    new_system_message=None,
    new_temperature=None,
    new_top_p=None,
    new_response_length=None,
    new_response_format=None,
    new_max_tokens=None
):
    model_name = model_name.strip()
    
    # === Key-Prüfung ===
    key_warning = check_model_api_key(model_name)
    if key_warning:
        st.warning(key_warning)
        return "", 0, 0, None

    COLLECTIONS = st.session_state.get("collections", {})
    context = context or "No context provided."
    settings = st.session_state.get("global_settings", {})

    system_message = new_system_message or settings.get("system_message", "You are an AI assistant.")
    temperature = new_temperature if new_temperature is not None else settings.get("temperature", 0.7)
    top_p = new_top_p if new_top_p is not None else settings.get("top_p", 0.9)
    response_length = new_response_length or settings.get("response_length", "Medium")
    response_format = new_response_format or settings.get("response_format", "Continuous Text")
    max_tokens = new_max_tokens or 500

    if use_case and use_case in COLLECTIONS:
        use_case_config = COLLECTIONS[use_case]
        system_message = use_case_config.get("system_message", system_message)
        response_format = override_response_format or response_format

    tokens_used = 0
    costs = 0
    response = None

    try:
        if model_name.startswith("groq_"):
            true_model = model_name.replace("groq_", "")
            response = query_groq(query, context, system_message, true_model)

        elif model_name == "Qwen/QwQ-32B":
            response = query_qwen(query, context, system_message, response_format)

        elif model_name.startswith("gpt"):
            response, tokens_used, costs = query_openai(
                query=query,
                context=context,
                system_message=system_message,
                use_context=True,
                temperature=temperature,
                top_p=top_p,
                response_length=response_length,
                response_format=response_format,
                max_tokens=max_tokens,
                model=model_name
            )

        elif model_name == "deepseek-api":
            response = query_deepseek(query, context, system_message, response_format)

        elif model_name == "deepstream":
            response = query_deepseek_stream(query, context, system_message, response_format)

        elif model_name.startswith("gemini"):
            response, tokens_used, costs = query_gemini(query, context, system_message, response_format, model_name)

        elif model_name.startswith("llama"):
            response = query_llama2(query, context, system_message, response_format, model_name)

        elif model_name.startswith("claude"):
            response = query_claude(query, context, model_name, system_message, response_format)

        elif model_name.startswith("mistral"):
            response, tokens_used, costs = query_mistral(query, context, system_message, response_format, model_name)

        else:
            return f"❌ Nicht unterstütztes Modell: {model_name}", 0, 0, None

        if isinstance(response, str):
            response = parse_think_block(response)

    except Exception as e:
        print(f"[ERROR] Model Error ({model_name}): {e}")
        return f"Error: {e}", 0, 0, None

    # === Referenzen aus ChromaDB laden
    references = {}
    if use_case:
        try:
            collection = get_or_create_collection(use_case)
            results = collection.query(query_texts=[query], n_results=100)

            for docs, metas, scores in zip(results["documents"], results["metadatas"], results["distances"]):
                for doc, meta, score in zip(docs, metas, scores):
                    source = meta.get("source", "Unknown")
                    page = meta.get("page", "Unknown")
                    relevance = round((1 - score) * 100, 2)

                    references.setdefault(source, []).append({
                        "page": page,
                        "text": doc.strip()[:300],
                        "relevance": relevance,
                    })
        except Exception as e:
            print(f"[ERROR] Reference Lookup Error ({use_case}): {e}")

    return response, tokens_used, costs, references