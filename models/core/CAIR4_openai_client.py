"""
===========================================================
OpenAI API Client (generate_answer.py)
===========================================================

Dieses Modul stellt eine Schnittstelle zur **OpenAI API** bereit und ermöglicht
die Generierung von Antworten für Benutzeranfragen mit optionalem Kontext.

📌 Funktionen:
- **generate_answer()** → Sendet eine Anfrage an OpenAI mit einstellbaren Parametern.
- **calculate_tokens()** → Berechnet die Tokenanzahl einer Eingabe für verschiedene Modelle.

✅ Warum ist das wichtig?
- Ermöglicht eine **kontextbewusste Antwortgenerierung** mit OpenAI-Modellen.
- **Flexibel einstellbar** durch Temperatur, Top-P, Token-Limit und Formatierung.
- **Berechnung der Tokenkosten** für transparente API-Nutzung.
"""

# === 1️⃣ Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.openai_lib import openai
from pylibs.tiktoken_lib import tiktoken

from models.core.CAIR4_dynaminc_api_keys import get_api_key

OPENAI_API_KEY = get_api_key("openai")

# === 3️⃣ OpenAI-Client initialisieren ===
openai.api_key = OPENAI_API_KEY
client = openai

# === 4️⃣ Sichere Tokenberechnung für OpenAI-Modelle ===
def calculate_tokens(prompt, model="gpt-4"):
    """ Berechnet die Tokenanzahl basierend auf dem Modell. """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"⚠️ Warnung: `{model}` nicht in `tiktoken` verfügbar. Nutze `cl100k_base` als Fallback.")
        encoding = tiktoken.get_encoding("cl100k_base")  # Fallback für nicht erkannte Modelle

    return len(encoding.encode(prompt))

# === 5️⃣ Hauptfunktion zur Generierung von Antworten ===
def query_openai(
    query,
    context=None,
    system_message="You are a helpful AI assistant.",
    use_context=False,
    temperature=0.7,
    top_p=1.0,
    response_length="Medium",  # 🔥 Wieder hinzugefügt!
    response_format="Continuous Text",
    max_tokens=None,
    model=None,  # ✅ Nimm den model_name als Parameter entgegen
):
    """
    Erstellt eine Anfrage an die OpenAI API und verarbeitet die Antwort.

    Args:
        query (str): Die Benutzeranfrage.
        context (str, optional): Kontext der Konversation.
        system_message (str): System-Nachricht zur Steuerung der KI.
        use_context (bool): Falls True, wird der Kontext der Anfrage hinzugefügt.
        temperature (float): Steuert die Zufälligkeit der Antwort.
        top_p (float): Alternativer Temperatur-Parameter für Wahrscheinlichkeitssteuerung.
        response_length (str): Länge der Antwort ("Short", "Medium", "Long").
        response_format (str): Format der Antwort ("Bullet Points", "JSON", "Continuous Text").
        max_tokens (int, optional): Maximale Anzahl der Tokens für die Antwort.
        model (str, optional): Das zu verwendende OpenAI-Modell. ✅ Hinzugefügt!

    Returns:
        str, int, float: Generierte Antwort, Anzahl der verwendeten Tokens, berechnete Kosten.
    """

    max_model_tokens = 8192 if "gpt-4" in model else 4096

    # ✅ Berechne die bereits verwendeten Tokens & vermeide `NoneType`-Fehler
    input_tokens = calculate_tokens(system_message + query, model=model) or 0
    available_tokens = max_model_tokens - input_tokens

    # ✅ Setze `max_tokens` sicher (kein `NoneType`-Fehler mehr)
    if max_tokens is None:
        if response_length == "Short":
            max_tokens = 500
        elif response_length == "Long":
            max_tokens = 4000
        else:  # Standard "Medium"
            max_tokens = 2000

    max_tokens = min(available_tokens, max_tokens)

    # ✅ Passe die System Message basierend auf dem gewünschten Format an
    if response_format == "Bullet Points":
        system_message += " Respond in bullet points."
    elif response_format == "JSON":
        system_message += " Respond in JSON format."
    elif response_format == "Continuous Text":
        system_message += " Provide a detailed but concise explanation."

    if use_context and context:
        system_message += f" Context: {context}"

    # ✅ Nachrichtenstruktur für OpenAI
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query.strip()}
    ]

    try:
        completion_params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens  # Sicher gesetzt, kein `NoneType`
        }

        # ✅ API-Aufruf
        completion = client.chat.completions.create(**completion_params)
        response = completion.choices[0].message.content.strip()

        # ✅ Berechne die tatsächlichen Token der Antwort & vermeide `NoneType`
        response_tokens = calculate_tokens(response, model=model) or 0
        total_tokens = input_tokens + response_tokens

        print(f"📊 Antwort-Token: {response_tokens}, Gesamt-Token: {total_tokens}")

        # ✅ Kostenberechnung
        cost_per_1k_tokens = 0.03 if "gpt-4" in model else 0.002
        session_cost = (total_tokens / 1000) * cost_per_1k_tokens

        return response, total_tokens, session_cost

    except Exception as e:
        return f"❌ Fehler bei der Antwortgenerierung: {e}", 0, 0.0