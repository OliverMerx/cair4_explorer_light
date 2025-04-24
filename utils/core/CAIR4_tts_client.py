"""
<description>
=================================================
🗣️ CAIR4 Text-to-Speech (TTS) mit OpenAI
=================================================

📌 **Beschreibung:**
Dieser View integriert OpenAI's **Text-to-Speech (TTS)** in das CAIR4-Framework.
Er ermöglicht das **Vorlesen von Trainingsinhalten** und stellt eine **Kostenberechnung**
für generierte Audiodateien bereit.

🎯 **Hauptfunktionen:**
- **Text-zu-Sprache-Umwandlung mit OpenAI** (TTS-1 Modell)
- **Wahl zwischen verschiedenen Sprecherstimmen**
- **Dynamische Kostenberechnung & Zeichenstatistik**
- **Audio-Wiedergabe & Download-Option für generierte Dateien**
- **Session-Speicherung der Nutzung** (Sprecher, Text, Kosten, Audio-File)

✅ **Warum ist das wichtig?**
- **Barrierefreiheit:** Trainingsinhalte können als Audio wiedergegeben werden.
- **Kostenkontrolle:** OpenAI-TTS ist kostenpflichtig – direkte Anzeige der erwarteten Kosten.
- **Dokumentation & Nachverfolgbarkeit:** Speicherung der generierten Inhalte für spätere Analyse.

⚠️ **Hinweis zur Nutzung:**
Kosten basieren auf OpenAI-Tarifen (Stand: 2024). Änderungen möglich.
<description>
"""

# === 1️⃣ **Importe & Bibliotheken** ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json
from pylibs.uuid_lib import uuid
from pylibs.openai_lib import openai
from pylibs.load_dotenv_lib import initialize_load_dotenv

import tempfile
import base64
import re

# === 2️⃣ **Interne Module** ===
from utils.core.CAIR4_update_sidebar import update_sidebar
from utils.core.CAIR4_session_manager import load_sessions, save_sessions, append_session
from utils.core.CAIR4_debug_utils import DebugUtils  
from utils.core.CAIR4_log_manager import handle_session_action
from controllers.CAIR4_controller import handle_query

# === 2️⃣ **API-Schlüssel laden & Umgebungsvariablen setzen** ===
load_dotenv = initialize_load_dotenv()
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === 3️⃣ **Kostenstruktur für OpenAI TTS (Stand: 2024)** ===
COST_PER_1M_CHARACTERS = 0.015  # 15 USD pro 1 Million Zeichen

# === 4️⃣ **OpenAI TTS-Stimmen** (offizielle Namen, **case-sensitive!**) ===
SPEAKER_OPTIONS = {
    "alloy": "Alloy (neutral, klar)",
    "echo": "Echo (kräftig, resonant)",
    "fable": "Fable (erzählerisch, sanft)",
    "onyx": "Onyx (tief, autoritär)",
    "nova": "Nova (dynamisch, energiegeladen)",
    "shimmer": "Shimmer (weich, schwebend)",
    "ash": "Ash (mysteriös, warm)",
    "sage": "Sage (sanft, weise)",
    "coral": "Coral (leicht, freundlich)"
}

# === 5️⃣ **Kosten berechnen** ===
def calculate_cost(text):
    """Berechnet die **geschätzten Kosten** für die OpenAI-TTS-Abfrage."""
    char_count = len(text)
    cost = (char_count / 1_000_000) * COST_PER_1M_CHARACTERS
    return round(cost, 6), char_count

# === 6️⃣ **Aussprache bestimmter Begriffe optimieren** ===
def preprocess_text_for_tts(text):
    """
    Ersetzt problematische Begriffe durch eine phonetisch bessere Schreibweise für die OpenAI-TTS API.
    """
    replace_dict = {
        "CAIR4": "Care for",  # Damit OpenAI es richtig ausspricht
        "KI": "Künstliche Intelligenz",  # Falls "K I" statt "Ka-i" gesprochen wird
        "EU AI Act": "EU A I Act",  # Verhindert englische Betonung
        "OpenAI": "Open A I",  # Verhindert falsche Betonung auf "Openai"
        "Neural Networks": "Newral Networks",  # Phonetische Anpassung
    }

    for key, value in replace_dict.items():
        text = text.replace(key, value)

    return text

# === 6️⃣ **Sprachausgabe generieren** ===
def generate_speech(text, voice):
    """Generiert Sprache aus Text mit OpenAI API.

    Args:
        text (str): Der umzuwandelnde Text.
        voice (str): Name der gewählten OpenAI-Stimme.

    Returns:
        bytes | str: Audiodatei als Binärdaten oder eine Fehlermeldung.
    """
    try:
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        return response.content  # Binäre Audiodaten zurückgeben
    except Exception as e:
        return f"❌ Fehler: {e}"


# === 7️⃣ **Automatische `<description>`-Erkennung** ===
def extract_description(view_code):
    """Extrahiert die `<description>`-Sektion aus dem View-Code.

    Args:
        view_code (str): Der vollständige Python-Code des Views.

    Returns:
        str: Der extrahierte Beschreibungstext oder eine Standardmeldung.
    """
    match = re.search(r"<description>(.*?)</description>", view_code, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "⚠️ Keine `<description>`-Sektion gefunden."


# === 8️⃣ **TTS-Button in anderen Views integrieren** ===
def render_tts_button(view_code):
    """Erstellt einen **Vorlesen-Button**, um die `<description>` eines Views in Sprache umzuwandeln.

    Args:
        view_code (str): Der Code des aktuellen Views, um die `<description>`-Sektion zu extrahieren.
    """
    description_text = extract_description(view_code)

    with st.expander("🎙️ Text-to-Speech (TTS)"):
        #st.write(f"📜 **Erkannte Einleitung:**\n\n_{description_text}_")
        selected_voice = st.selectbox("🔊 Sprecher wählen:", list(SPEAKER_OPTIONS.keys()), format_func=lambda v: SPEAKER_OPTIONS[v])
        cost, chars = calculate_cost(description_text)
        st.markdown(f"💰 **Geschätzte Kosten:** `{cost} USD` für `{chars}` Zeichen")

        if st.button("🎙️ Text vorlesen"):
            st.info(f"🔄 Generiere Audio mit `{SPEAKER_OPTIONS[selected_voice]}`...")

            #Aussprache bestimmter Worte optimieren
            processed_text = preprocess_text_for_tts(description_text)

            #Versenden des Textes zur Vertonung
            audio_data = generate_speech(processed_text, selected_voice)

            if isinstance(audio_data, str) and "Fehler" in audio_data:
                st.error(audio_data)
            else:
                # 📌 **Temporäre Datei speichern & bereitstellen**
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tmp_file.write(audio_data)
                    audio_path = tmp_file.name

                # 📌 **Audio-Wiedergabe**
                st.audio(audio_path, format="audio/mp3")

                # 📌 **Download-Button**
                with open(audio_path, "rb") as file:
                    st.download_button(
                        label="📥 Audio herunterladen",
                        data=file,
                        file_name="CAIR4_{st.session_state.previous_use_case}.mp3",
                        mime="audio/mp3"
                    )