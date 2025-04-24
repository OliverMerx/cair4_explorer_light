"""
=================================================
CAIR4 Deepseek API Wrapper
=================================================

Dieses Modul verwaltet die Kommunikation mit der **Deepseek-API**, 
um KI-generierte Antworten auf Benutzeranfragen zu erhalten.

📌 Funktionen:
- **query_deepseek(query, context, model_name, stream)**  
  ➝ Sendet eine Anfrage an die Deepseek-API mit optionalem Kontext.

✅ Warum ist das wichtig?
- **Automatisierte API-Interaktion**: Erleichtert die Kommunikation mit Deepseek.
- **Kontextsteuerung**: Ermöglicht präzisere Antworten durch Kontextübermittlung.
- **Fehlertolerant**: Bietet robuste Fehlerbehandlung für API-Anfragen.

Verwendung:
    from utils.core.CAIR4_deepseek_manager import query_deepseek
    response = query_deepseek("Was ist Künstliche Intelligenz?", model_name="deepseek-chat")
    print(response)
"""
# === 1️⃣ Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.requests_lib import requests
from pylibs.json_lib import json 

from models.core.CAIR4_dynaminc_api_keys import get_api_key

# Deepseek API-Schlüssel abrufen
DEEPSEEK_API_KEY = get_api_key("deepseek")

# === 3️⃣ Deepseek API-Anfrage-Funktion (erweitert) ===
def query_deepseek(
    query, 
    context=None, 
    system_message="You are a helpful assistant.", 
    response_format="Continuous Text", 
    model_name="deepseek-chat", 
    stream=False
):
    """
    Sendet eine Anfrage an die Deepseek-API und verarbeitet System-Message, Kontext und Response-Format.

    Args:
        query (str): Die Benutzeranfrage.
        context (str, optional): Kontextinformationen für die Konversation.
        system_message (str): Die System-Message, die das Verhalten der KI steuert.
        response_format (str): Das gewünschte Antwortformat (z. B. "Bullet Points", "JSON", "Continuous Text").
        model_name (str): Das zu verwendende Modell (Standard: "deepseek-chat").
        stream (bool): Ob die Antwort gestreamt werden soll (Standard: False).

    Returns:
        str: Die generierte Antwort von Deepseek oder eine Fehlermeldung.
    """
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    # ✅ **System-Message mit Response-Format kombinieren**
    if response_format == "Bullet Points":
        system_message += " Respond in bullet points."
    elif response_format == "JSON":
        system_message += " Respond in JSON format."
    elif response_format == "Continuous Text":
        system_message += " Provide a detailed and continuous explanation."

    # ✅ **Nachrichtenstruktur erstellen**
    messages = [{"role": "system", "content": system_message}]

    if context:
        messages.append({"role": "system", "content": f"Context: {context}"})
    
    messages.append({"role": "user", "content": query})

    payload = {
        "model": model_name,
        "messages": messages,
        "stream": stream,
    }

    try:
        print(f"[DEBUG] Sending payload to DeepSeek: {json.dumps(payload, indent=2)}")

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Prüft auf HTTP-Fehler

        response_data = response.json()
        result = response_data.get("choices", [{}])[0].get("message", {}).get("content", "⚠️ No content returned.")
        
        print(f"[DEBUG] DeepSeek Response: {result[:200]}...")  # Nur den Anfang der Antwort anzeigen
        return result

    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTP-Fehler: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"❌ Netzwerkfehler: {req_err}"
    except Exception as e:
        return f"❌ Ein Fehler ist aufgetreten: {e}"