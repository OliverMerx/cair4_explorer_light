import streamlit as st
from duckduckgo_search import DDGS
from streamlit_extras.stylable_container import stylable_container
from controllers.CAIR4_controller import handle_query
import sqlite3
from sentence_transformers import SentenceTransformer, util
from pathlib import Path

# === Zusatzkomponente für Style-Container ===
def styled_container(bg_color, text_color, key, width, height):
    with stylable_container(
        key=f"style_container_{key}",
        css_styles=f"""{{
            width: {width}!important;
            padding-right:20px;
            margin-top:-45px!important;
        }}"""
    ):
        return st.container()


DB_PATH = Path("CAIR4_data/db/CAIR4_usecases.db")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

CHECKLIST_DB_PATH = Path("CAIR4_data/db/CAIR4_checklists.db")

def load_checklists_from_db():
    if not CHECKLIST_DB_PATH.exists():
        return []

    with sqlite3.connect(CHECKLIST_DB_PATH) as conn:
        rows = conn.execute("SELECT filename, content FROM checklists").fetchall()
        return [{"filename": r[0], "content": r[1]} for r in rows]

def get_relevant_checklists(title, description, code, ascii_diagram, top_k=3):
    checklists = load_checklists_from_db()
    if not checklists:
        return []

    context_text = f"{title}\n{description}\n{code}\n{ascii_diagram}"
    query_embedding = embedding_model.encode(context_text, convert_to_tensor=True)
    checklist_embeddings = embedding_model.encode([c["content"] for c in checklists], convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, checklist_embeddings)[0]
    top_indices = scores.topk(top_k).indices.tolist()

    return [checklists[i] for i in top_indices]

def format_ascii_checklist_evaluation(checklist):
    lines = checklist["content"].strip().splitlines()
    result = [f"\U0001F9BE Bewertung: {checklist['title']}"]
    for line in lines:
        if line.strip().startswith("-"):
            result.append(f"{line}\n→ Einschätzung: [bitte prüfen]")
    return "\n".join(result)

# === HAUPTFUNKTION ===
def render_multi_chat_view(use_case_title="", use_case_description="", ascii_art="", source_code="", initial_faq=None):
    FAQs = [
        "FAQs:",
        f"Was beinhaltet Code des Use Case '{use_case_title}' genau?",
        f"Welche Chancen und Mehrwerte ermöglicht der Use Case '{use_case_title}'?",
        f"Welche regulatorischen Aspekte können beim Use Case '{use_case_title}' eine Rolle spielen?",
        f"Welche Risiken können sich beim Use Case '{use_case_title}' ergeben?",
        f"Wie unterscheidet sich der Use Case '{use_case_title}' von klassischer Software?",
        f"Gibt es Einschränkungen beim Use Case '{use_case_title}'?",
        #"Relevante Checklisten anzeigen und prüfen"
    ]

    st.markdown("""
        <style>
        div[role="tooltip"] {
            z-index: 1 !important;
            margin-bottom: 3rem !important;
            margin-left: 2rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    chat_key = f"chat_messages_{use_case_title}"
    st.session_state.setdefault(chat_key, [])
    st.session_state.setdefault("selected_faq", None)

    col_websearch, col_context, col_faq, col_history = st.columns([2, 2, 2, 2])

    with col_websearch:
        use_websearch = st.checkbox("\U0001F310 Websuche", value=False)

    with col_context:
        use_code_context = st.checkbox("\U0001F9E0 Code- und Use Case", value=True)

    with col_faq:
        with styled_container("#fff", "#000", "faq_multichat_teaser", "", ""):
            st.markdown("<p></p>", unsafe_allow_html=True)
            st.selectbox("", options=FAQs, key="faq_selectbox", on_change=lambda: st.session_state.update({"selected_faq": st.session_state.faq_selectbox}))

    with col_history:
        show_history = st.checkbox("\U0001F4AC Verlauf anzeigen", value=False)

    if show_history:
        for msg in st.session_state[chat_key]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if st.session_state.selected_faq and st.session_state.selected_faq != "FAQs:":
        selected_faq = st.session_state.selected_faq
        st.session_state.selected_faq = None
        process_query(
            query=selected_faq,
            chat_key=chat_key,
            show_history=show_history,
            use_websearch=use_websearch,
            use_code_context=use_code_context,
            use_case_title=use_case_title,
            use_case_description=use_case_description,
            ascii_art=ascii_art,
            source_code=source_code,
        )

    user_query = st.chat_input("Stelle deine Hauptfrage...")
    if user_query:
        process_query(
            query=user_query,
            chat_key=chat_key,
            show_history=show_history,
            use_websearch=use_websearch,
            use_code_context=use_code_context,
            use_case_title=use_case_title,
            use_case_description=use_case_description,
            ascii_art=ascii_art,
            source_code=source_code,
        )

def process_query(query, chat_key, show_history, use_websearch, use_code_context,
                  use_case_title, use_case_description, ascii_art, source_code):

    if not show_history:
        st.session_state[chat_key] = []

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Antwort wird generiert..."):

            # 🌐 Websuche
            web_context = ""
            if use_websearch:
                try:
                    with DDGS() as ddgs:
                        results = ddgs.text(query, max_results=3)
                    web_context = "\n\n".join([
                        f"**{r['title']}**\n{r.get('body', '')}\n🔗 {r['href']}" for r in results if r.get("href")
                    ])
                except Exception as e:
                    web_context = f"Fehler bei der Websuche: {e}"

            # 📘 Use Case Kontext
            code_context = f"""
📌 Use Case: {use_case_title}
📋 Beschreibung: {use_case_description}

💻 Code:
{source_code}

🧾 ASCII:
{ascii_art}
""".strip() if use_code_context else ""

            # ✅ Checklisten-Matching mit Statusanzeige
            checklist_block = ""
            with st.status("🔍 Suche nach passenden Checklisten...", expanded=True) as status:
                matched = get_relevant_checklists(
                    title=use_case_title,
                    description=use_case_description,
                    code=source_code,
                    ascii_diagram=ascii_art
                )
                if not matched:
                    status.update(label="⚠️ Keine passenden Checklisten gefunden.", state="error")
                    checklist_block = "❌ Keine passenden Checklisten verfügbar."
                else:
                    checklist_block = "\n\n".join([format_ascii_checklist_evaluation(chk) for chk in matched])
                    status.update(label=f"✅ {len(matched)} relevante Checklisten gefunden.", state="complete")

            # 🧠 Prompt für LLM
            full_prompt = f"""
Ein Nutzer fragt:
\"{query}\"

{f"🔍 Web-Kontext:\n{web_context}" if web_context else ""}
📘 Kontext aus Use Case:
{code_context}

✅ Passende Checklisten:
{checklist_block}

Bitte beantworte die Nutzerfrage strukturiert. Wenn möglich, bewerte den Use Case entlang der Checklisten.
""".strip()

            # 🧠 Modellantwort
            response, *_ = handle_query(
                query=full_prompt,
                model_name=st.session_state.get("selected_model", "gpt-4o"),
                use_case=st.session_state.get("selected_use_case", "default_use_case"),
                context={}
            )

            st.markdown(response)

            # 💬 Verlauf speichern
            if show_history:
                st.session_state[chat_key].append({"role": "user", "content": query})
                st.session_state[chat_key].append({"role": "assistant", "content": response})
            else:
                st.session_state[chat_key] = [
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": response}
                ]