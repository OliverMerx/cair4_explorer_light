"""
=================================================
💬 CAIR4 Knowledge-Graph View
=================================================
https://www.nlplanet.org/course-practical-nlp/02-practical-nlp-first-tasks/16-knowledge-graph-from-text.html
"""
import streamlit as st
import graphviz
import spacy
import json
import re
from controllers.CAIR4_controller import handle_query
from utils.core.CAIR4_debug_utils import DebugUtils

# Konstanten
DEFAULT_TEXT = (
    "Angela Merkel wurde 1954 in Hamburg geboren. "
    "Sie war die Bundeskanzlerin von Deutschland und ist Physikerin. "
    "Sie studierte Physik an der Universität Leipzig und arbeitete später am Zentralinstitut für Physikalische Chemie."
)
TRIPLE_PROMPT = (
    "Extrahiere aus folgendem Text semantische Triple im Format "
    "[{'subject': '...', 'predicate': '...', 'object': '...'}, ...]:\n\n"
)

# Lade spaCy-Modell
@st.cache_resource(show_spinner="🔄 Lade spaCy-Modell...")
def load_spacy_model():
    try:
        return spacy.load("de_core_news_lg")
    except OSError:
        st.error("❌ spaCy-Modell 'de_core_news_lg' nicht gefunden.")
        return None

nlp = load_spacy_model()

def parse_json_triples(text):
    """
    Extrahiert JSON-ähnliche Liste von Triple aus einer Modellantwort.
    """
    try:
        match = re.search(r"\[\s*{.*?}\s*]", text, re.DOTALL)
        if match:
            json_block = match.group(0).replace("'", '"')
            try:
                return json.loads(json_block)
            except json.JSONDecodeError as e:
                st.error(f"❌ Fehler beim Dekodieren des JSON: {e}")
                return []
        else:
            st.warning("⚠️ Keine gültige JSON-Liste mit Triples gefunden.")
            return []
    except re.error as e:
        st.error(f"❌ Fehler im regulären Ausdruck: {e}")
        return []

@st.cache_data
def extract_triples(text, model_name="gpt-4"):
    """Extrahiert semantische Triple aus dem Text mithilfe des Sprachmodells."""
    prompt = TRIPLE_PROMPT + text
    with st.spinner("🧠 Extrahiere semantische Triple..."):
        result, *_ = handle_query(
            query=text,
            use_case="knowledge_graph",
            context=prompt,
            model_name=model_name,
        )
    return parse_json_triples(result)

def extract_named_entities(text):
    """Extrahiert Named Entities aus dem Text mit spaCy."""
    if nlp:
        doc = nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
    return []

def render_kg_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    st.session_state.setdefault("kg_text_input", DEFAULT_TEXT)
    text_input = st.text_area("📄 Eingabetext:", height=200, key="kg_text_input")

    if st.button("🔍 Analyse starten"):
        DebugUtils.debug_print("Textanalyse gestartet.")
        triples = extract_triples(text_input, model_name)
        entities = extract_named_entities(text_input)

        if not triples:
            st.warning("❗ Keine gültigen Triple zur Visualisierung gefunden.")
        else:
            st.subheader("📊 Knowledge Graph")
            dot = graphviz.Digraph()
            for triple in triples:
                if all(key in triple for key in ['subject', 'predicate', 'object']):
                    dot.edge(triple['subject'], triple['object'], label=triple['predicate'])
                else:
                    st.error(f"❌ Ungültiges Triple-Format: {triple}")
            st.graphviz_chart(dot)

        if entities:
            st.subheader("🔎 Named Entities")
            for ent, label in entities:
                st.markdown(f"**{ent}** → *{label}*")

        st.success("✅ Analyse abgeschlossen.")

# Dummy-Aufruf der Funktion (im echten Code wird dies durch Streamlit gesteuert)
if __name__ == "__main__":
    # Erstellen Sie eine einfache CAIR4_controller-Imitation für lokale Tests
    def dummy_handle_query(query, use_case, context, model_name):
        # Simuliert eine Antwort mit JSON-ähnlichen Triples
        dummy_response = """
        [
            {'subject': 'Angela Merkel', 'predicate': 'geboren in', 'object': 'Hamburg'},
            {'subject': 'Angela Merkel', 'predicate': 'war', 'object': 'Bundeskanzlerin von Deutschland'},
            {'subject': 'Angela Merkel', 'predicate': 'ist', 'object': 'Physikerin'},
            {'subject': 'Angela Merkel', 'predicate': 'studierte', 'object': 'Physik'},
            {'subject': 'Universität Leipzig', 'predicate': 'Ort von Studium', 'object': 'Angela Merkel'},
            {'subject': 'Angela Merkel', 'predicate': 'arbeitete bei', 'object': 'Zentralinstitut für Physikalische Chemie'}
        ]
        """
        return dummy_response, None  # Simuliere Ergebnis und keine Metadaten

    # Ersetzen Sie den echten handle_query für diesen lokalen Test
    from unittest.mock import patch
    with patch('controllers.CAIR4_controller.handle_query', side_effect=dummy_handle_query):
        render_kg_view(
            use_case="knowledge_graph",
            context="",
            title="CAIR4 Knowledge Graph",
            description="Visualisiert extrahierte Beziehungen als Knowledge Graph.",
            system_message="",
            session_file="",
            model_name="test-model",
            settings={},
            collection=None,
            sidebar=st.sidebar
        )