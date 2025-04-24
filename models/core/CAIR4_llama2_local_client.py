"""
===========================================================
LLaMA 2 API Client (query_llama2.py)
===========================================================

Dieses Modul stellt eine Schnittstelle zur **lokalen LLaMA 2 API** bereit und ermöglicht 
die Verarbeitung von Benutzeranfragen mit kontextabhängigen Prompts über **Ollama**.

📌 Funktionen:
- **query_llama2()** → Sendet eine Anfrage an das lokal installierte LLaMA 2 Modell.
- **Unterstützt Kontext** → Kann zusätzliche Informationen für genauere Antworten nutzen.
- **Automatische Fehlerbehandlung** → Erfasst Fehler und gibt sinnvolle Rückgaben.

✅ Warum ist das wichtig?
- Ermöglicht eine **lokale** Verarbeitung von KI-Anfragen ohne API-Kosten.
- Unterstützt Open-Source-Modelle für Datenschutz und Offline-Verarbeitung.
- Kann in den **Creator, die Main-App und den Digital Twin** integriert werden.
"""

# === 1️⃣  Import externer Bibliotheken ===
from pylibs.streamlit_lib import streamlit as st  # UI-Komponenten für mögliche Erweiterungen
from pylibs.ollama_lib import ollama # Direktanbindung an die Ollama API für lokale KI-Modelle

# === 2️⃣  Hauptfunktion zur Kommunikation mit LLaMA 2 ===
def query_llama2(prompt, context="", model_name="llama2", max_length=200):
    """
    Sendet eine Anfrage an das lokal installierte LLaMA 2 Modell über Ollama.

    Args:
        prompt (str): Die Eingabeaufforderung für das Modell.
        context (str): Optionaler Kontext für genauere Antworten.
        model_name (str): Das zu verwendende Modell (Standard: "llama2").
        max_length (int): Maximale Länge der generierten Antwort.

    Returns:
        str: Die generierte Antwort oder eine Fehlermeldung.
    """

    try:
        # **Erstelle den vollständigen Prompt mit Kontext**
        full_prompt = f"Kontext: {context}\n\nFrage: {prompt}"

        # **Sende Anfrage an Ollama**
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": full_prompt}]
        )

        # **Prüfe die Antwort und extrahiere den generierten Text**
        if "message" in response and "content" in response["message"]:
            return response["message"]["content"]
        else:
            return "❌ Fehler: Keine gültige Antwort erhalten."

    except Exception as e:
        print(f"[ERROR] Fehler beim Aufruf von Ollama: {e}")
        return f"❌ Fehler: {e}"