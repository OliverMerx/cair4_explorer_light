# ============================================================
# 🤖 Groq API Wrapper (query_groq.py)
# ============================================================

"""
Dieses Modul stellt eine Schnittstelle zur **Groq API** bereit und ermöglicht 
die Verarbeitung von Benutzeranfragen über hochperformante LLMs wie LLaMA3, Mixtral oder Gemma.

📌 Funktionen:
- **query_groq()** → Sendet eine Anfrage an die Groq-API mit API-Key.
- **Dynamischer API-Key Support** → Automatisch via Umgebungsvariable oder Session.
- **Fehlermanagement & Debugging** → Ausführliche Fehleranalyse & Logging.

✅ Warum ist das wichtig?
- Nutzt Groq’s **ultraschnelle LLM-Infrastruktur** ohne lokalen Model-Download.
- **Kosteneffiziente Verarbeitung** über Cloud-basierte Transformer.
- **Kompatibel mit CAIR4 Plug-and-Play-Modellen** via Standard-Interface.
"""

# === 📦 1️⃣ Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from groq import Groq
from models.core.CAIR4_dynaminc_api_keys import get_api_key

# === 🔐 2️⃣ API-Key sicher laden ===
GROQ_API_KEY = get_api_key("groq")
client = Groq(api_key=GROQ_API_KEY)

# === 🚀 3️⃣ Anfragefunktion im CAIR4-Stil ===
def query_groq(
    query: str,
    context: str = "",
    system_message: str = "You are a helpful assistant.",
    model_name: str = "groq-llama3-8b-8192",
    max_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 1.0              # Optional, kann erweitert werden
):
    """
    Führt eine Anfrage an die Groq API aus. Unterstützt verschiedene Groq-Modelle.
    """

    try:
        # 📨 Nachrichtenvorbereitung
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        if context:
            messages.append({"role": "user", "content": context})
        messages.append({"role": "user", "content": query})

        # 📡 Anfrage senden
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )

        # ✅ Antwort extrahieren
        result_text = response.choices[0].message.content
        print(f"[Groq ✅] Antwort erhalten ({model_name}): {result_text[:200]}...")
        return result_text

    except Exception as e:
        error_msg = f"❌ Groq-Fehler bei Modell {model_name}: {e} \n\n**Achtung**: Bitte stets die Liste aktuell verfügtbarer groq-Modelle prüfen: https://console.groq.com/docs/deprecations und geänderte Modelle in den API-Model-Options anpassen."
        print(f"[Groq ❌] {error_msg}")
        return error_msg