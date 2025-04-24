"""
===========================================================
Mistral API Client (query_mistral.py)
===========================================================

Dieses Modul stellt eine Schnittstelle zur **Mistral API** bereit und ermöglicht 
die Verarbeitung von Benutzeranfragen mit kontextabhängigen Prompts.

📌 Funktionen:
- **query_mistral()** → Sendet eine Anfrage an Mistral mit Kontext.
- **Automatische Fehlerbehandlung** → Fängt API-Fehler ab und gibt sinnvolle Rückgaben.

✅ Warum ist das wichtig?
- Ermöglicht eine direkte Kommunikation mit **Gemini 1.5 Flash** (oder anderen Modellen).
- Unterstützt kontextbasierte Konversationen.
- Vereinfacht die API-Integration mit Fehlerbehandlung.
"""

# === 1️⃣  Import externer Bibliotheken ===
from pylibs.os_lib import os
from mistralai import Mistral

from models.core.CAIR4_dynaminc_api_keys import get_api_key

#Mistral = mistralai.Mistral()

# Mistral API-Schlüssel abrufen
MISTRAL_API_KEY = get_api_key("mistral")

# === 3️⃣  Hauptfunktion zur Kommunikation mit Mistral (erweitert) ===
def query_mistral(
    query,
    context=None,
    system_message="You are a helpful assistant.", 
    response_format="Continuous Text", 
    model_name="mistral-large-latest"
):
    """
    Sendet eine Anfrage an Mistral mit System-Message, Kontext und erwartetem Antwortformat.

    Args:
        query (str): Die neue Benutzeranfrage.
        context (str, optional): Optionaler Kontext für die Konversation.
        system_message (str): Die System-Message zur Steuerung des Assistentenverhaltens.
        response_format (str): Das gewünschte Antwortformat (z. B. "Bullet Points", "JSON", "Continuous Text").
        model_name (str): Das zu verwendende Modell (Standard: "mistral-large-latest").

    Returns:
        tuple: (Antworttext, Tokenanzahl, Berechnete Kosten)
    """

    client = Mistral(api_key=MISTRAL_API_KEY)

    # ✅ **Response-Format in System-Message integrieren**
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

    try:
        print(f"[DEBUG] Sending messages to Mistral: {messages}")

        chat_response = client.chat.complete(
            model=model_name,
            messages=messages
        )
        
        # ✅ **Sicherstellen, dass die Antwort existiert**
        if not chat_response.choices:
            print("❌ [ERROR] Keine Antwort von Mistral erhalten!")
            return "❌ Keine Antwort von Mistral erhalten.", 0, 0.0

        # ✅ **Antwortinhalt extrahieren**
        response_content = getattr(chat_response.choices[0].message, "content", None)

        if response_content:
            # Beispielhafte Token- und Kostenberechnung (falls die API keine Infos liefert)
            estimated_tokens = len(response_content.split())  # Einfache Wortzählung
            estimated_cost = estimated_tokens * 0.00001  # Beispiel-Kostenberechnung

            return response_content, estimated_tokens, estimated_cost
        else:
            print("❌ [ERROR] Antwort von Mistral ist leer oder ungültig!")
            return "❌ Antwort von Mistral ist leer oder ungültig.", 0, 0.0

    except Exception as e:
        print(f"❌ Fehler bei der Verarbeitung: {e}")
        return f"❌ Fehler bei der Verarbeitung: {e}", 0, 0.0