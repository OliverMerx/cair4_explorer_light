import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from utils.core.CAIR4_encrypt_manager import encrypt_data
from controllers.CAIR4_controller import handle_query
from sentence_transformers import SentenceTransformer, util
import sqlite3
from pathlib import Path
import torch

DB_PATH = Path("CAIR4_data/db/CAIR4_usecases.db")
  # === FAQ-Auswahl
FAQ_PROMPTS = {
    "KI-Einsteiger": "Einsteiger, Grundlagen der KI, einfache Use Cases, plakative Beispiele, Erklärbarkeit, Einstieg",
    "KI-Fortgeschrittene": "KI-Anwendungen für Fortgeschrittene, NLP, Bildverarbeitung, Klassifikation, LLM-Integration",
    "KI-Experten": "komplexe KI-Systeme, High-Risk-AI, regulatorische Aspekte, modellübergreifende Evaluation, Training und Fine-Tuning",
    "EU AI Act": "KI-Verordnung, EU AI Act, Hochrisiko-KI, KI-Gesetz, KI-Governance, Compliance, Regulierung, Anhang III",
    "DSGVO": "DSGVO, Datenschutz, Einwilligung, personenbezogene Daten, Verarbeitung, Recht auf Löschung, Transparenz",
    "Retail": "Einzelhandel, Preise, Kundenverhalten, Produktempfehlung, Rabattstrategie, Point-of-Sale, Einkauf",
    "Finance": "Finanzen, Kreditvergabe, Bankwesen, Zahlungssysteme, Risikoanalyse, Finanztransparenz, Geldwäscheprävention",
    "Health": "Gesundheit, Medizin, Diagnosen, Patientendaten, Krankenhaus, E-Health, Medikation",
    "Public": "öffentliche Verwaltung, Verwaltungsvorgänge, Behörden, Bürgerdienste, Transparenz, E-Government",
    "RAG": "Retrieval-Augmented Generation, Vektorsuche, Dokumentenabfrage, Kontextintegration, Frage-Antwort-Systeme",
    "SQL": "SQL, Datenbankabfrage, Tabellenstruktur, SELECT, Datenbankzugriff, relationales Modell, SQLite",
    "RBAC": "RBAC, Role-Based Access Control, Zugriffsrechte, Rollenverwaltung, Zugriffsschutz, Benutzerverwaltung",
    "ATCF": "ATCF, Adaptive Trust Control Framework, Vertrauenswürdigkeit, KI-Transparenz, modulare Risikobewertung"
}
OPTIONS = ["Quick-Search:"] + list(FAQ_PROMPTS.keys())

# === Embedding-Modell laden
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-mpnet-base-v2")

# === Use Cases aus SQLite-DB laden
@st.cache_data
def load_use_cases_from_db():
    if not DB_PATH.exists():
        return []
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT id, name, title, description, tags, view_path, key, ascii FROM usecases").fetchall()
        return [
            {
                "id": r[0],
                "name": r[1],
                "title": r[2],
                "description": r[3],
                "tags": r[4],
                "view_path": r[5],
                "key": r[6],
                "ascii": r[7] or ""
            }
            for r in rows
        ]
    return [
        {"id": r[0], "name": r[1], "title": r[2], "description": r[3], "tags": r[4], "view_path": r[5], "key": r[6]}
        for r in rows
    ]

# === Semantische Suche
def combined_semantic_search(query, use_cases, top_k=3):
    model = load_embedding_model()

    texts = [f"{uc['title']} {uc['description']} {uc['tags']} {uc.get('ascii', '')}" for uc in use_cases]
    query_embedding = model.encode(query, convert_to_tensor=True)
    case_embeddings = model.encode(texts, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, case_embeddings)[0]
    top_indices = similarities.topk(top_k).indices.tolist()
    return [use_cases[i] for i in top_indices]

def set_faq_to_default():
    st.session_state["teaser_faq_select"] = OPTIONS[0]

def clear_text_input():
    st.session_state["teaser_question_input"] = ""

# === UI-Komponente
def styled_container(bg_color, text_color, key, width, height, margin_top=0):
    st.session_state.setdefault("teaser_faq_index",0)
    with stylable_container(
        key=f"style_container_{key}",
        css_styles=f"""
        {{
            background-color: {bg_color}!important;
            color: {text_color};
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 10px;
            width: {width}!important;
            margin-top:{margin_top};
            height:100%;
            max-height: {height}!important;
            box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
            overflow-y:auto;
        }}"""
    ):
        return st.container()
    
def render_home_chat_teaser():
    # === Layout starten ===
    with styled_container("#fff", "#000", "home_chat_teaser", "100%", "100%"):
        st.markdown("<p style='text-align:left; font-weight: bold; font-size: 18px; color: white;'>🧠 Dr. Know:</p>", unsafe_allow_html=True)
        st.session_state.setdefault("teaser_faq_index",0)
        col1, col2, col3 = st.columns([6, 2, 1])

        # === Textfeld
        with col1:
            user_input = st.text_input(
                "Stelle Dr. Know eine Frage zu CAIR4 oder wähle ein Quick-Search-Thema:",
                key="teaser_question_input",
                placeholder="z.B. Gibt es medizinische Anwendungsfälle?",
                on_change=set_faq_to_default
            )

        with col2:
            options = OPTIONS
            selection = st.selectbox("", 
                    options, 
                    key="teaser_faq_select", 
                    on_change=clear_text_input,
                    ) # Callback bei FAQ-Auswahl

        # === Button
        with col3:
            with stylable_container(
                key="button_style",
                css_styles="""
                    button[kind="secondary"] {
                        margin-top: 29px;
                        width: 100%;
                        height: 37px;
                    }
                """
            ):
                run_query = st.button("➤", key="run_teaser_button")

        # === Anfrage vorbereiten
        query = ""
        if selection != "Quick-Search:":
            query = f"[Ausgewähltes Thema: {selection}]\n{FAQ_PROMPTS[selection]}"
        elif user_input.strip():
            query = user_input.strip()

        if query and run_query:
            st.session_state["last_teaser_query"] = query

            # ... Embedding-Suche und Ausgabe wie gehabt

            with st.spinner("🧠 Dr. Know sucht nach passenden Use Cases..."):
                all_use_cases = load_use_cases_from_db()
                accessible_keys = set(st.session_state.get("collections", {}).keys())
                use_cases = [uc for uc in all_use_cases if uc["key"] in accessible_keys]
                blocked = [uc for uc in all_use_cases if uc["key"] not in accessible_keys]

                # Wenn keine passenden Use Cases verfügbar sind
                if not use_cases:
                    st.warning("🔐 Aufgrund der Dir zugeordneten Nutzerrechte konnten keine passenden Use Cases gefunden werden.")
                    fallback_prompt = f"""
                Du bist Dr. Know, ein KI-basierter Copilot für regulatorische Use Cases im CAIR4 Explorer.

                Ein Nutzer hat diese Frage gestellt:
                \"{query}\"

                Leider stehen diesem Nutzer aktuell keine spezifischen Use Cases zur Verfügung – z. B. aufgrund eingeschränkter Zugriffsrechte oder unpassender Rollen.

                Bitte gib dennoch eine hilfreiche, allgemeine Antwort. Erkläre ggf. typische Einsatzbereiche, beschreibe, welche Themen unter diesem Stichwort typischerweise im CAIR4 Explorer behandelt werden, und lade dazu ein, Zugriff auf weitere Use Cases zu beantragen oder das Kapitel zu wechseln.
                """
                    response, *_ = handle_query(
                        query=fallback_prompt,
                        model_name=st.session_state.get("selected_model"),
                        use_case="home_chat_teaser_fallback",
                        context={}
                    )

                    with st.expander("🧠 **Dr. Know antwortet trotzdem:**", expanded=True):
                        st.markdown(response)

                    return
                
                n_results = st.slider("Anzahl Ergebnisse", 1, 5, 3, key="num_teaser_results")
                top_use_cases = combined_semantic_search(query, use_cases, top_k=n_results)

                context_text = "\n".join([f"- {uc['title']}: {uc['description']}" for uc in top_use_cases])
                prompt = f"""Ein Nutzer fragt: "{query}"\n\nHier die {len(top_use_cases)} ähnlichsten Use Cases:\n{context_text}\n\nBitte formuliere eine strukturierte, hilfreiche Antwort."""
                response, *_ = handle_query(query=prompt, model_name=st.session_state.get("selected_model"), use_case="home_chat_teaser", context={})

                with st.expander("🧠 Dr. Know hat folgende Antwort für Dich:", expanded=True):
                    st.write(response)

                encrypted_role = encrypt_data(st.session_state.get("user_role", "guest"))
                for uc in top_use_cases:
                    if uc["key"] in accessible_keys:
                        st.markdown(f"""<a href="?role={encrypted_role}&view={uc['key']}" target="_self">🔗 {uc['title']}</a> – {uc['description']}""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"❌ **{uc['title']}** – Zugriff verweigert")

                st.success(f"{len(use_cases)} Use Cases berücksichtigt.")
                if blocked:
                    st.info(f"💡 {len(blocked)} Use Cases wurden aus Zugriffsgründen ausgeschlossen.")
