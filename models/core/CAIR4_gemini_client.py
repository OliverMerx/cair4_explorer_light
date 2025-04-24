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

# === 1️⃣  Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json
from pylibs.requests_lib import requests

from models.core.CAIR4_dynaminc_api_keys import get_api_key

GEMINI_API_KEY = get_api_key("gemini")

# === 3️⃣  Hauptfunktion zur Kommunikation mit Gemini (erweitert) ===
def query_gemini(
    context, 
    query, 
    system_message="You are a helpful assistant.", 
    response_format="Continuous Text", 
    model_name="gemini-1.5-flash"
):
    """
    Sendet eine Anfrage an Gemini mit System-Message, Kontext und erwartetem Antwortformat.

    Args:
        context (str): Der bisherige Verlauf der Konversation.
        query (str): Die neue Benutzeranfrage.
        system_message (str): Die System-Message zur Steuerung des Assistentenverhaltens.
        response_format (str): Das gewünschte Antwortformat (z. B. "Bullet Points", "JSON", "Continuous Text").
        model_name (str): Das zu verwendende Modell (Standard: "gemini-1.5-flash").

    Returns:
        tuple: (Antworttext, Tokenanzahl, Berechnete Kosten)
    """

    # **API-URL zusammenstellen**
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"

    # ✅ **Response-Format in System-Message integrieren**
    if response_format == "Bullet Points":
        system_message += " Respond in bullet points."
    elif response_format == "JSON":
        system_message += " Respond in JSON format."
    elif response_format == "Continuous Text":
        system_message += " Provide a detailed and continuous explanation."

    # ✅ **Prompt mit System-Message und Kontext erstellen**
    full_prompt = f"{system_message}\nContext: {context}\nUser: {query}\nAssistant:"

    # **JSON-Payload für API-Anfrage**
    payload = {
        "contents": [
            {
                "parts": [{"text": full_prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"[DEBUG] Sending payload to Gemini: {json.dumps(payload, indent=2)}")

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()

        # **Fehlermeldungen abfangen**
        if response.status_code != 200:
            error_message = response_data.get("error", {}).get("message", "Unknown error")
            return f"❌ API Error {response.status_code}: {error_message}", 0, 0.0

        # **Antwort verarbeiten**
        candidates = response_data.get("candidates", [])
        if not candidates:
            return "⚠️ No valid response received from Gemini.", 0, 0.0

        # ✅ **Extrahiere generierten Text**
        generated_content = candidates[0]["content"]["parts"][0]["text"]

        # **Token & Kostenberechnung (sofern verfügbar)**
        usage = response_data.get("usageMetadata", {})
        tokens_used = usage.get("totalTokens", 0)
        estimated_cost = tokens_used * 0.00001  # Beispielrechnung, ggf. anpassen

        print(f"[DEBUG] Gemini Response: {generated_content[:200]}...")

        return generated_content, tokens_used, estimated_cost

    except requests.exceptions.RequestException as e:
        return f"❌ Netzwerkfehler: {e}", 0, 0.0
    except Exception as e:
        return f"❌ Fehler bei der Verarbeitung: {e}", 0, 0.0