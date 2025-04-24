"""
========================
📊 CAIR4 Token Analyzer
========================

Ein Token ist keine Silbe, kein Wort und kein Buchstabe – aber irgendwie *alles davon gleichzeitig*.  
KI-Systeme wie GPT denken nicht in Wörtern, sondern in **Token** – und jedes Token verbraucht Speicherplatz im Gespräch.  

📌 **Beispiel:**  
Das Wort `Internationalisierung` ist **ein** Wort, aber oft **mehrere** Tokens.  
Das Wort `AI` ist sehr kurz – und trotzdem **ein Token**.  
Ein Emoji `🙂`? Auch das ist **ein Token**!

---
### ✅ In diesem View:
- Zerlege deinen Text in Tokens und erkenne, was wie gezählt wird.
- Sieh, wie viele Tokens **Input** und **Output** du verbrauchst.
- Verstehe die **Grenzen deines Modells** (z. B. max. 4096 oder 8192 Tokens).
- Schätze ab, wann eine Eingabe zu groß wird.
"""

# === 📦 Import externer Bibliotheken ===
from pylibs.numpy_lib import numpy as np
from pylibs.pandas_lib import pandas as pd
from pylibs.re_lib import re
from pylibs.streamlit_lib import streamlit as st

import tiktoken
import pandas as pd
import streamlit as st

# === Hilfsfunktion zur Tokenanalyse ===
def analyze_tokens(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    token_values = [encoding.decode([t]) for t in tokens]
    return tokens, token_values

# === Heuristik zur semantischen Bewertung von Tokens ===
def semantic_analysis(token_values):
    result = []
    for token in token_values:
        if len(token) <= 2:
            meaning = "❌ Unwahrscheinlich sinnvoll"
        elif token.lower() in ["der", "die", "und", "ist", "ein"]:
            meaning = "✅ Eigenständiges Wort"
        elif token[0].isupper() and len(token) > 5:
            meaning = "⚠️ Möglicherweise Teil eines Eigennamens"
        else:
            meaning = "⚠️ Eventuell Teilwort"
        result.append(meaning)
    return result

# === Haupt-Renderfunktion ===
def render_token_visualizer_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    # 📥 Texteingabe
    prompt = st.text_area("Gib einen beliebigen Text ein:", height=150)

    # Modellwahl (Optional)
    model_choice = st.selectbox("🔧 Modell wählen (für Tokenizer)", ["gpt-3.5-turbo", "gpt-4"])

    if st.button("Eingabe analysieren"):
        tokens, token_values = analyze_tokens(prompt, model=model_choice)
        semantics = semantic_analysis(token_values)

        # Fortschrittsbalken zur Tokenanzahl
        max_tokens = 4096 if model_choice == "gpt-3.5-turbo" else 8192
        st.progress(min(len(tokens) / max_tokens, 1.0))
        st.info(f"Dein Text besteht aus **{len(tokens)} Token** (max. {max_tokens} für dieses Modell)")

        # Auswahl der Darstellung
        view_mode = st.selectbox("🧪 Darstellungsvariante wählen:", [
            "🧾 Tabellenansicht mit Bewertung",
            "🔤 Tokenfolge mit Hervorhebung",
            "📉 Tokenverbrauchs-Simulation"
        ])

        if view_mode == "🧾 Tabellenansicht mit Bewertung":
            df = pd.DataFrame({
                "Token-Nr": list(range(1, len(tokens)+1)),
                "Token": token_values,
                "Semantische Bewertung": semantics
            })
            st.dataframe(df, use_container_width=True)

        elif view_mode == "🔤 Tokenfolge mit Hervorhebung":
            st.markdown("### 🔍 Token-Darstellung")
            for i, token in enumerate(token_values):
                badge = semantics[i].split()[0]
                st.markdown(f"{badge} `{token}`", unsafe_allow_html=True)

        elif view_mode == "📉 Tokenverbrauchs-Simulation":
            input_len = len(tokens)
            output_len = st.slider("📤 Erwartete Antwortlänge (geschätzt in Tokens):", 10, 2048, 200, step=10)
            total = input_len + output_len
            st.markdown(f"🧮 Gesamttokenzahl (Input + Output): **{total}**")
            st.progress(min(total / max_tokens, 1.0))

            if total > max_tokens:
                st.error("🚫 Dein Gesamttokenverbrauch überschreitet das Limit dieses Modells!")
            else:
                st.success("✅ Dein Input + erwarteter Output liegen im Rahmen.")
