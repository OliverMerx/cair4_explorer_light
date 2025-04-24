"""
===========================================================
Qwen API Wrapper (query_qwen.py)
===========================================================

Dieses Modul stellt eine Schnittstelle zur **Qwen API** bereit und ermöglicht 
die Verarbeitung von Benutzeranfragen über die offizielle API.

📌 Funktionen:
- **query_qwen()** → Sendet eine Anfrage an die Qwen-API mit API-Key.
- **Dynamischer API-Key Support** → Falls Nutzer eigene Keys nutzt, wird dieser übernommen.
- **Fehlermanagement & Logging** → Gibt hilfreiche Debugging-Infos aus.

✅ Warum ist das wichtig?
- Spart **lokalen Speicherplatz** (kein riesiger Model-Download!).
- **Schnellere Inferenzzeiten**, da das Modell cloudbasiert läuft.
- **Einfache Nutzung über HTTP** → Kein extra GPU-Support nötig.
"""

# === 📦 1️⃣ Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.requests_lib import requests
from pylibs.json_lib import json

from models.core.CAIR4_dynaminc_api_keys import get_api_key

# ✅ **Hole API-Key aus .env oder Session State**
QWEN_API_KEY = get_api_key("qwen")

# === 2️⃣ Korrekte API-URL für Alibaba DashScope ===
API_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"

# === 3️⃣ Anfrage an Qwen API senden ===
def query_qwen(
    query,
    context="",
    system_message="You are a helpful assistant.",
    model_name="qwen-turbo",
    max_tokens=512,
    response_length="Medium",  # 🔥 Wieder hinzugefügt!
    response_format="Continuous Text",
):
    print(f"🔍 QWEN_API_KEY: {QWEN_API_KEY}")
    max_tokens=None,
    """
    Führt eine Anfrage an die Qwen-API über Alibaba Cloud aus.
    """

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    # **Formatierung der Eingabe für die API**
    payload = {
        "model": model_name,
        "input": {
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": query}
            ]
        },
        "parameters": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": max_tokens
        }
    }

    try:
        print(f"[DEBUG] 🔄 Sende Anfrage an Qwen API: {json.dumps(payload, indent=2)}")

        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # HTTP-Fehler abfangen

        response_data = response.json()

        # **Antwort extrahieren**
        if "output" in response_data:
            response_text = response_data["output"]["text"]
            print(f"✅ Qwen Antwort: {response_text[:200]}...")  # Debugging
            return response_text
        else:
            return "⚠️ Keine gültige Antwort von Qwen erhalten."

    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTP-Fehler: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"❌ Netzwerkfehler: {req_err}"
    except Exception as e:
        return f"❌ Ein Fehler ist aufgetreten: {e}"