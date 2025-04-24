"""
=============================================
Deepseek API Client - Streaming (deepseek_api.py)
=============================================

Dieses Modul stellt eine Verbindung zur Deepseek-API her und ermöglicht das 
Senden von Anfragen mit optionalem Streaming. Die API nutzt das Modell 
"deepseek-chat" oder andere spezifizierte Varianten.

📌 Funktionen:
- **query_deepseek_stream()** → Sendet eine Anfrage mit Streaming-Unterstützung.

✅ Warum ist das wichtig?
- Erlaubt Echtzeit-Streaming von KI-Antworten.
- Unterstützt kontextbezogene Anfragen durch System-Prompts.
- Stellt sicher, dass die API-Schlüssel sicher aus einer .env-Datei geladen werden.
"""

# === 1️⃣  Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.requests_lib import requests
from pylibs.json_lib import json 

from models.core.CAIR4_dynaminc_api_keys import get_api_key


# API-Schlüssel aus der Umgebungsvariable laden
DEEPSEEK_API_KEY = get_api_key("deepseek")

# === 3️⃣  Deepseek API-Funktion (erweitert) ===
def query_deepseek_stream(
    query, 
    context=None, 
    system_message="You are a helpful assistant.", 
    response_format="Continuous Text", 
    model_name="deepseek-chat", 
    stream=True
):
    """
    Sendet eine Anfrage an die Deepseek-API mit Unterstützung für Streaming-Antworten und 
    berücksichtigt System-Message sowie Response-Format.

    Args:
        query (str): Die Benutzeranfrage.
        context (str, optional): Kontextinformationen für die Anfrage.
        system_message (str): Die System-Message, die das Verhalten der KI steuert.
        response_format (str): Das gewünschte Antwortformat (z. B. "Bullet Points", "JSON", "Continuous Text").
        model_name (str): Das zu verwendende Modell (Standard: "deepseek-chat").
        stream (bool): Ob die Antwort gestreamt werden soll (Standard: True).

    Returns:
        str: Die zusammengefügte Antwort von Deepseek.
    """

    # ✅ **Response-Format in System-Message integrieren**
    if response_format == "Bullet Points":
        system_message += " Respond in bullet points."
    elif response_format == "JSON":
        system_message += " Respond in JSON format."
    elif response_format == "Continuous Text":
        system_message += " Provide a detailed and continuous explanation."

    # Deepseek API-Endpunkt
    url = "https://api.deepseek.com/chat/completions"

    # HTTP-Header für die Anfrage
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    # Nachrichtenstruktur für die API-Anfrage
    messages = [{"role": "system", "content": system_message}]
    if context:
        messages.append({"role": "system", "content": f"Context: {context}"})
    messages.append({"role": "user", "content": query})

    # JSON-Payload für die Anfrage
    payload = {
        "model": model_name,
        "messages": messages,
        "stream": stream,
    }

    try:
        print(f"[DEBUG] Sende Anfrage an DeepSeek: {json.dumps(payload, indent=2)}")

        # API-Anfrage mit Streaming-Unterstützung senden
        response = requests.post(url, headers=headers, data=json.dumps(payload), stream=True)
        response.raise_for_status()  # Überprüfe auf HTTP-Fehler

        full_response = ""  # Variable zum Sammeln der vollständigen Antwort

        # Streaming-Antwort verarbeiten
        for line in response.iter_lines():
            if line:  # Nur nicht-leere Zeilen verarbeiten
                decoded_line = line.decode("utf-8")
                if decoded_line.startswith("data: "):  # JSON-Daten extrahieren
                    data = decoded_line[6:]  # "data: " entfernen
                    
                    if data == "[DONE]":  # Streaming abgeschlossen
                        break

                    try:
                        json_data = json.loads(data)  # JSON parsen
                        delta = json_data["choices"][0]["delta"].get("content", "")
                        full_response += delta  # Antwort zusammensetzen
                    except json.JSONDecodeError as e:
                        print(f"⚠️ JSON-Fehler: {e}, Rohdaten: {data}")
                        continue

        print(f"[DEBUG] DeepSeek Streaming Response: {full_response[:200]}...")  # Gekürzte Antwort anzeigen
        return full_response  # Vollständige Antwort zurückgeben

    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTP-Fehler: {http_err}"
    except Exception as e:
        return f"❌ Ein Fehler ist aufgetreten: {e}"