"""
=================================================
Anthropic API Client (Messages-Endpoint)
=================================================

Dieses Modul stellt eine Verbindung zur Anthropic-API (Claude) 
über /v1/messages her und ermöglicht das Senden von Anfragen 
ohne Streaming.

📌 Funktionen:
- query_claude() → Sendet eine Anfrage an Anthropic (Claude).

✅ Warum ist das wichtig?
- Unterstützt kontextbezogene Anfragen durch ein allgemeines System-Prompt.
- Nutzt die aktuelle /v1/messages-Struktur der Anthropic API.
"""
# === 📦 Imports ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.requests_lib import requests
from pylibs.json_lib import json
from models.core.CAIR4_dynaminc_api_keys import get_api_key

# === 🔐 API-Key ===
ANTHROPIC_API_KEY = get_api_key("anthropic")


# === 🤖 Claude v1/messages API-Call ===
def query_claude(
    *,
    query: str,
    context: str = None,
    model_name: str = "claude-3-7-sonnet-20250219",
    max_tokens: int = 512,
    temperature: float = 1.0,
    response_format: str = "Continuous Text",
    system_message: str = "You are a helpful assistant.",
    stop_sequences: list = None
) -> str:
    """
    Sendet eine Anfrage an Anthropic (Claude) über den /v1/messages Endpunkt.

    Args:
        query (str): Benutzeranfrage (Prompt).
        context (str, optional): Zusätzlicher Kontext.
        model_name (str): Claude-Modellname.
        max_tokens (int): Maximale Tokenanzahl.
        temperature (float): Kreativitätssteuerung.
        response_format (str): Antwortformat (derzeit nicht genutzt).
        system_message (str): Systemnachricht an Claude.
        stop_sequences (list, optional): Stop-Sequenzen.

    Returns:
        str: Antwort von Claude oder Fehlermeldung.
    """

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    # === Nachrichtenformat (Claude benötigt Liste von Rollen)
    messages = [{"role": "user", "content": query}]
    if context:
        messages.append({"role": "user", "content": context})

    # === Payload zusammenbauen
    payload = {
        "model": model_name,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system_message,
    }
    if stop_sequences:
        payload["stop_sequences"] = stop_sequences

    # === Debug: Optional Payload anzeigen
    st.sidebar.markdown("### 📦 Claude Payload:")
    st.sidebar.code(json.dumps(payload, indent=2))

    # === Request senden
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        resp_data = response.json()
        return resp_data['content'][0]['text']

    except requests.exceptions.HTTPError as http_err:
        st.error(f"🚨 HTTP-Fehler: {http_err}")
        st.error(f"❌ Fehlerdetails: {response.text}")
    except Exception as e:
        st.error(f"🚨 Allgemeiner Fehler: {e}")
        return f"❌ Fehler: {e}"