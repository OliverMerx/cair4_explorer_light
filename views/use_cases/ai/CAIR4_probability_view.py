"""
==============================================
💡 CAIR4 Wahrscheinlichkeiten berechnen
==============================================

KI leitet Antworten auf Basis probabilistischer Entscheidungslogiken vor. 
Durch die Verarbeitung der Nutzereingabe und die dynamische Reaktion auf erkannte Muster können verschiedene plausible Antworten vergleichen werden.
Die Antwort bzgl. der Hauptstädte von vier Ländern wird dabei stets mit anderen relevanten Städten verglichen.

Um entsprechende Wahrscheinlichkeiten und Relationen berechnen zu können, müssen die Worte des Promptszuvor numerisch umgewandelt sein (Vektorisierung).

"""

import numpy as np
import pandas as pd
import re
import streamlit as st
import graphviz
from utils.core.CAIR4_debug_utils import DebugUtils  # Import der Debug-Klasse
from controllers.CAIR4_controller import handle_query
from models.core.CAIR4_collection_client import list_collection_contents

def process_query_steps(query):
    DebugUtils.debug_print(f"Analyse der Anfrage: {query}")
   
    # Schritt 1: Tokenisierung
    tokens = re.findall(r'\b\w+\b', query)
    
    # Schritt 2: Wahrscheinlichkeiten für Länder
    country_probabilities = {"Italien": 0.7, "Frankreich": 0.1, "Deutschland": 0.1, "England": 0.1}
    
    # Schritt 3: Land bestimmen
    collection_name = "answer_finding_collection"
    try:
        documents = list_collection_contents(collection_name)
        for doc in documents:
            for country in country_probabilities:
                if country in doc["content"]:
                    country_probabilities[country] = min(country_probabilities[country] + 0.1, 1.0)
    except Exception as e:
        st.warning(f"Fehler beim Laden der Collection: {e}")
    
    best_country = max(country_probabilities, key=country_probabilities.get)
    
    # Schritt 4: Wahrscheinlichkeiten für Hauptstädte basierend auf Land
    city_probabilities = {
        "Italien": {"Rom": 0.8, "Mailand": 0.1, "Neapel": 0.05, "Florenz": 0.05},
        "Frankreich": {"Paris": 0.9, "Lyon": 0.05, "Marseille": 0.05},
        "Deutschland": {"Berlin": 0.9, "München": 0.05, "Hamburg": 0.05},
        "England": {"London": 0.9, "Manchester": 0.05, "Birmingham": 0.05}
    }
    
    city_probs = city_probabilities.get(best_country, {})
    
    return best_country, country_probabilities, city_probs

def render_probability_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):

    """
    Mehrstufige Visualisierung der Antwortfindung mit vollständigem Entscheidungsfluss.
    """
    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)
    
 # Session State initialisieren, wenn nicht vorhanden
    if "user_input" not in st.session_state:
        st.session_state.user_input = "Was ist die Hauptstadt von Italien"

    # Eingabefeld mit Sessionbindung
    user_input = st.text_input(
        "",
        key="user_input"
    )
    
    # Szenarien-Daten
    ki_szenarien = {
        "Italien": {"Rom": 0.8, "Mailand": 0.1, "Neapel": 0.05, "Florenz": 0.05},
        "Frankreich": {"Paris": 0.9, "Lyon": 0.05, "Marseille": 0.05},
        "Deutschland": {"Berlin": 0.9, "München": 0.05, "Hamburg": 0.05},
        "England": {"London": 0.9, "Manchester": 0.05, "Birmingham": 0.05}
    }

    # Dynamische Ländererkennung aus Eingabe
    matched_country = None
    for country in ki_szenarien:
        if country.lower() in st.session_state.user_input.lower():
            matched_country = country
            break

    # Dynamische KI-Visualisierung
    ai_graph = graphviz.Digraph()

    if matched_country:
        st.info(f"📊 Szenario erkannt: {matched_country}")

        ai_graph.node("Eingabe", f"Frage: {st.session_state.user_input}")
        ai_graph.node("Suche", "Vergleich mit Trainingsdaten")
        ai_graph.node("Bewertung", "Wahrscheinlichkeitsverteilung")
        ai_graph.node("Ausgabe", "Antwort")

        ai_graph.edge("Eingabe", "Suche")
        ai_graph.edge("Suche", "Bewertung")

        for city, prob in ki_szenarien[matched_country].items():
            city_node = f"{city}\n{int(prob * 100)}%"
            ai_graph.node(city_node, city_node)
            ai_graph.edge("Bewertung", city_node)
            ai_graph.edge(city_node, "Ausgabe")

        st.graphviz_chart(ai_graph)

    elif st.session_state.user_input:
        st.warning("🚫 Dieses System kennt nur die Länder Italien, Frankreich, Deutschland und England.")