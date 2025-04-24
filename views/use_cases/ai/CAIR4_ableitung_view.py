"""
=================================================
🔍 CAIR4 Ableitungs-View: Wie KI Entscheidungen trifft
=================================================

📌 **Beschreibung:**  
Dieser View zeigt, **wie eine KI Ableitungen trifft** und damit zu Entscheidungen kommt.  
Anders als **regelbasierte Systeme**, die auf **vordefinierten Regeln** basieren, **erkennt**  
eine KI **Muster in Daten, extrahiert Merkmale und gewichtet sie**, um eine **datenbasierte Ableitung** zu treffen.

⚖️ **Regulatorischer Kontext:**  
Im Sinne des **EU AI Acts** ist eine Software **nur dann eine KI**, wenn sie:
1️⃣ **Muster erkennt & verarbeitet**,  
2️⃣ **Merkmale (Features) aus Daten extrahiert**,  
3️⃣ **Datenbasiert Ableitungen trifft (ohne feste Regeln)**.  

➡️ ACHTUNG: **Regelbasierte Systeme sind keine KI im regulatorischen Sinne ** 
– ein klassischer **Finanzregel-Algorithmus** würde z. B. eine Kreditentscheidung **direkt nach festen Werten** treffen, 
ohne Merkmale zu extrahieren. Regelbasierte Systeme nutzen keine datenbasierte Ableitung   

🛠 **Technische Umsetzung:**  
- **Nutzereingabe** → KI **extrahiert Merkmale**  
- **Merkmale werden gewichtet** → KI bewertet deren Einfluss  
- **Ergebnis der Ableitung** → KI trifft datenbasierte Entscheidung  

🎯 **Ziel dieses Views:**  
- **Erklären, wie eine KI Ableitungen trifft**  
- **Visualisieren des Prozesses mit einem Entscheidungsgraphen**  
- **Unterscheiden zwischen Regelbasierten Systemen und KI**  

🔍 **Beispiel:**  
💬 **Frage:** "Soll dieser Kredit genehmigt werden?"  
🧠 **KI erkennt & gewichtet:**  
  ✅ **Merkmal:** Sprache positiv → **+20% Wahrscheinlichkeit**  
  ✅ **Merkmal:** Text sehr lang → **-10% Wahrscheinlichkeit**  
  ✅ **Merkmal:** Kreditbetrag sehr hoch → **-30% Wahrscheinlichkeit**  
💡 **Ergebnis:** **Genehmigt oder Abgelehnt** basierend auf der Gesamtbewertung.
"""

# === 1️⃣ 📂 Importiere erforderliche CAIR4-Standardbibliotheken ===
from pylibs.streamlit_lib import streamlit as st  # UI-Komponente für StreamlitE
from pylibs.os_lib import os  # Betriebssystem-Interaktionen
from pylibs.json_lib import json  # JSON-Verarbeitung
from pylibs.graphviz_lib import graphviz  # 📈 Visualisierung von Entscheidungsbäumen
from pylibs.random_lib import random  # Zufallszahlen für Simulation
from pylibs.datetime_lib import initialize_datetime  # 🕒 Zeithandhabung

# **📌 CAIR4-Module für Logging & Debugging**
from utils.core.CAIR4_debug_utils import DebugUtils  # Debugging & Logging

# **📌 Datetime initialisieren**
datetime = initialize_datetime()

# === 2️⃣ 🧠 Simuliere KI-Ableitung ===
def simulate_derived_decision(input_text):
    """
    🧠 Simuliert einen datenbasierten KI-Ableitungsprozess:
    - Erkennt **Merkmale** in der Eingabe
    - Gewichtet **Merkmale** zur Entscheidungsfindung
    - Gibt eine **finale Ableitung** aus
    
    📌 **Warum ist das relevant?**
    - **Regelbasierte Systeme** nutzen **nur feste Vorgaben**.
    - **KI-Systeme** müssen **Muster erkennen** & **dynamische Ableitungen** treffen.
    
    📊 **Beispiel:**
    - **Eingabe:** "Soll dieser Kredit genehmigt werden?"
    - **Extrahierte Merkmale:** 💰 Gehalt, 📅 Laufzeit, 📈 Bonität
    - **Gewichtung der Merkmale:** [Gehalt 40%, Laufzeit 30%, Bonität 30%]
    - **Finale Entscheidung:** Genehmigt oder Abgelehnt
    """
    
    DebugUtils.debug_print(f"📌 KI-Ableitung gestartet mit Eingabe: {input_text}")

    # 1️⃣ **Feature-Extraktion:** Welche Merkmale erkennt die KI?
    extracted_features = {
        "📊 Sentiment": random.choice(["Positiv", "Neutral", "Negativ"]),
        "📄 Länge der Eingabe": len(input_text),
        "🔍 Schlüsselwörter": [word for word in input_text.split() if len(word) > 4]
    }

    # 2️⃣ **Feature-Gewichtung:** Wie wichtig sind die erkannten Merkmale?
    feature_weights = {
        "📊 Sentiment": random.uniform(0.1, 0.9),
        "📄 Länge der Eingabe": random.uniform(0.1, 0.9),
        "🔍 Schlüsselwörter": random.uniform(0.1, 0.9)
    }

    # 3️⃣ **Finale Entscheidung:** KI trifft datenbasierte Ableitung
    score = sum(feature_weights.values()) / len(feature_weights)
    decision = "✅ Entscheidung durch Ableitung" if score > 0.5 else "❌ Abgelehnt"

    return extracted_features, feature_weights, decision

# === 3️⃣ 🎛 Haupt-Render-Funktion ===
def render_derivation_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    """
    📌 Rendert den CAIR4 Ableitungs-View zur KI-Entscheidungsfindung.

    🔹 **Warum wichtig?**
    - Zeigt, wie **KI-Systeme datenbasiert Ableitungen treffen**.
    - Unterscheidet **regelbasierte Algorithmen von echten KI-Systemen**.
    - Unterstützt **Regulatorik nach EU AI Act** zur Klassifizierung von KI.
    """
    
    # Hauptansicht
    st.subheader(title)

    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    # 📝 **Benutzereingabe simulieren**
    input_text = st.text_input("💡 Gib eine Frage oder einen Entscheidungsfall ein:", "Soll dieser Kredit genehmigt werden?")

    if input_text:
        extracted_features, feature_weights, decision = simulate_derived_decision(input_text)

        # 📈 **Graph-Visualisierung der Ableitung**
        graph = graphviz.Digraph()
        graph.node("📥 Eingabe", input_text, shape="ellipse", style="filled", color="lightgrey")
        graph.node("🔍 Feature-Extraktion", "Erkannte Merkmale")
        graph.edge("📥 Eingabe", "🔍 Feature-Extraktion")

        for feature, value in extracted_features.items():
            graph.node(feature, f"{feature}: {value}")
            graph.edge("🔍 Feature-Extraktion", feature)

        graph.node("⚖️ Feature-Gewichtung", "Gewichtung der Merkmale")
        graph.edge("🔍 Feature-Extraktion", "⚖️ Feature-Gewichtung")

        for feature, weight in feature_weights.items():
            graph.node(f"{feature}_W", f"{feature}: {weight:.2f}")
            graph.edge("⚖️ Feature-Gewichtung", f"{feature}_W")

        #graph.node("✅ Ableitung", f"Ergebnis: {decision}", shape="box", style="filled", color="lightblue")
        #graph.edge("⚖️ Feature-Gewichtung", "✅ Ableitung")

        st.graphviz_chart(graph)
        
        st.success(f"**KI-Entscheidung:** {decision}")
        st.info(f"Basierend auf den erkannten Merkmalen und deren Gewichtung wurde die Entscheidung getroffen.")
        
        with st.expander("ℹ️ Details zur Ableitung", expanded=True):
            st.json({
                "🔍 Erkannte Merkmale": extracted_features,
                "⚖️ Merkmalsgewichtung": feature_weights,
                "📌 Entscheidung": decision
            })

    else:
        st.warning("⚠️ Bitte gib eine Eingabe ein, um den Ableitungsprozess zu starten.")