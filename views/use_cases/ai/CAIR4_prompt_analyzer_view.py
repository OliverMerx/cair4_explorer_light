"""
=================================================
📊 CAIR4 Prompt-Analyse & Verarbeitung
=================================================

📌 **Beschreibung:**
Damit ein KI-Modell die Texteingabe versteht, muss der Inputtext numerisch umgewandelt werden. 
Dies geschieht mithilfe von **Vektoren**, die es ermöglichen, das Verhältnis von Wörtern zueinander zu bestimmen.  
Das KI-System sendet keine Texte an das Modell, sondern **Vektor-Repräsentationen** der Eingabe.  
Gleiches gilt für die Antwort: Sie erfolgt als Vektor und wird vom KI-System zurück in Text umgewandelt.  

💡 **Erkunde, wie sich dein Text in Zahlen verwandelt!**  
Gib eine Nachricht ein und analysiere die Verarbeitungsschritte in verschiedenen Visualisierungsformen.

✅ **Hauptfunktionen:**
- **Schritt-für-Schritt-Analyse der Tokenisierung & Umwandlung in Vektoren**
- **Farbcodierung der Token für bessere Verständlichkeit**
- **Übersetzungsvergleich mit anderen Sprachen**
- **Interaktive Manipulation einzelner Wörter und deren Auswirkungen**
- **Speicherung und Nachverfolgung der Transformationen in der Session**
"""

# === 📦 Import externer Bibliotheken ===
from pylibs.numpy_lib import numpy as np
from pylibs.pandas_lib import pandas as pd
from pylibs.re_lib import re
from pylibs.random_lib import random
from pylibs.streamlit_lib import streamlit as st
from deep_translator import GoogleTranslator

# === 🛠 Import interner Module ===
from utils.core.CAIR4_debug_utils import DebugUtils
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics
from controllers.CAIR4_controller import handle_query


# === 🔍 Funktion zur Vorverarbeitung von Prompts ===
def preprocess_prompt(prompt):
    """
    Simuliert die Transformation eines Prompts in eine KI-kompatible Form.

    **Schritte der Vorverarbeitung:**
    1️⃣ Tokenisierung → Zerlegt den Text in einzelne Wörter.  
    2️⃣ Indizierung → Weist jedem Wort eine ID zu.  
    3️⃣ Vektorisierung → Erzeugt für jedes Wort eine numerische Darstellung.  
    4️⃣ Positionskodierung → Setzt Wörter in einen mathematischen Kontext.  
    5️⃣ Übersetzung → Vergleicht den deutschen mit dem englischen Text.  
    6️⃣ Farbcodierung → Weist Token bestimmte Farben zur Visualisierung zu.  

    Args:
        prompt (str): Vom Benutzer eingegebener Text.

    Returns:
        pandas.DataFrame: Eine Tabelle mit allen Verarbeitungsschritten.
    """
    DebugUtils.debug_print(f"🔄 Vorverarbeitung gestartet für: {prompt}")

    # 1️⃣ Tokenisierung
    tokens = re.findall(r'\b\w+\b', prompt)
    DebugUtils.debug_print(f"✅ Tokenisierung abgeschlossen: {tokens}")

    # 2️⃣ Indizierung
    token_indices = {token: idx for idx, token in enumerate(tokens)}
    DebugUtils.debug_print(f"📊 Indizierung: {token_indices}")

    # 3️⃣ Dummy-Vektorisierung (One-Hot-Encoding)
    vector_size = len(tokens)
    word_vectors = np.eye(vector_size)

    # 4️⃣ Positionskodierung (vereinfachtes Modell)
    position_encoding = {token: idx / vector_size for token, idx in token_indices.items()}
    DebugUtils.debug_print(f"📍 Positionskodierung: {position_encoding}")

    # 5️⃣ Englische Übersetzung
    translated_prompt = GoogleTranslator(source='de', target='en').translate(prompt)
    translated_tokens = re.findall(r'\b\w+\b', translated_prompt)

    # ✂ Anpassung der Token-Länge (Padding oder Abschneiden)
    if len(translated_tokens) < len(tokens):
        translated_tokens += ["N/A"] * (len(tokens) - len(translated_tokens))
    elif len(translated_tokens) > len(tokens):
        translated_tokens = translated_tokens[:len(tokens)]

    # 6️⃣ Farbcodierung (zur besseren Darstellung)
    emoji_palette = [
        # 🟦 Quadrate (farbige Blöcke)
        "🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "⬛", "⬜", "🟫",

        # ❤️ Emotionen
        "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎",

        # ✨ Licht & Energie
        "🌕", "🌑", "🌗", "🌈", "⭐", "✨", "🔥", "⚡", "💥",

        # 🔠 Symbole
        "🔍", "📌", "🧠", "📎",

        # ➕ Bonus-Runde: Stil + Technik
        "🧬", "🪐", "💡", "🛰️", "🖥️", "🧮", "🗂️", "📊", "📚"
    ]

    # 🔀 Mischen & beschneiden auf Anzahl Tokens
    def assign_unique_emojis(tokens):
        unique_count = len(tokens)
        used_palette = emoji_palette.copy()
        random.shuffle(used_palette)
        if unique_count <= len(used_palette):
            return used_palette[:unique_count]
        else:
            # Wenn mehr Tokens als Symbole → auffüllen mit ⬜
            return used_palette + ["⬜"] * (unique_count - len(used_palette))

    # Ergebnis:
    colors = assign_unique_emojis(tokens)
    # DataFrame für die Analyse erstellen
    df_processing = pd.DataFrame({
        'Token': tokens,
        'Index': [token_indices[token] for token in tokens],
        'Vektor': [list(word_vectors[token_indices[token]]) for token in tokens],
        'Positionskodierung': [position_encoding[token] for token in tokens],
        'Englische Übersetzung': translated_tokens,
        'Symbol': colors
    })

    return df_processing


# === 🏗 Haupt-Render-Funktion ===
def render_prompt_analyze_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    """
    Rendert die Hauptansicht zur **Analyse von Prompts und ihrer Umwandlung in KI-kompatible Daten**.

    Args:
        use_case (str): Der Name des aktuellen Anwendungsfalls.
        context (str): Kontextuelle Informationen.
        title (str): Titel des Views.
        description (str): Beschreibung des Anwendungsfalls.
        session_file (str): Dateipfad zur Speicherung der Sessions.
    """
    DebugUtils.debug_print(f"📌 View gestartet für Use Case: {use_case}")

    # ✅ Sitzungen laden & Initialisieren
    sessions = load_sessions(session_file)
    st.session_state.setdefault("universal_sessions", {})
    st.session_state.universal_sessions[use_case] = sessions

    if "active_use_case" not in st.session_state or st.session_state["active_use_case"] != use_case:
        st.session_state["active_use_case"] = use_case
        st.session_state["current_session"] = {
            "messages": [],
            "metrics": {"total_tokens": 0, "total_costs": 0.0}
        }

    # Hauptansicht
    st.subheader(title)
 
    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    # 💬 **Eingabefeld für Prompts**
    if prompt := st.chat_input("💡 Gib einen Text ein zur Analyse:"):
        DebugUtils.debug_print(f"📥 Eingabe erhalten: {prompt}")
        df = preprocess_prompt(prompt)

        st.dataframe(df)
        st.info("📌 Jeder Schritt zeigt, wie der Text verarbeitet wird, bevor er an das KI-Modell gesendet wird.")

        # 📜 **Chat speichern**
        append_message(st.session_state["current_session"], "user", prompt)
        append_message(st.session_state["current_session"], "assistant", "Ergebnis wurde generiert.")
        save_sessions(session_file, st.session_state.universal_sessions[use_case])