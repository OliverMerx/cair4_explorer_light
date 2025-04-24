import streamlit as st
import sqlite3
from pathlib import Path
from duckduckgo_search import DDGS
from controllers.CAIR4_controller import handle_query

CHECKUP_ASCII_DIR = Path("./assets/ascii/check_ups/")
DB_PATH = Path("CAIR4_data/db/ascii_checkups.db")

def save_ascii_files_to_db(files):
    if not DB_PATH.parent.exists():
        DB_PATH.parent.mkdir(parents=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DROP TABLE IF EXISTS checklists")
        conn.execute("""
            CREATE TABLE checklists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                content TEXT
            )
        """)
        for file in files:
            conn.execute(
                "INSERT INTO checklists (filename, content) VALUES (?, ?)",
                (file["filename"], file["content"])
            )
        conn.commit()


def render_checklist_comparison_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):

    if not CHECKUP_ASCII_DIR.exists():
        st.warning("❗️Checklisten-Ordner fehlt.")
        return

    checkup_files = [f for f in CHECKUP_ASCII_DIR.iterdir() if f.suffix in [".txt", ".asc"]]

    checkup_names = [f.name for f in checkup_files]

    col1, col2, col3 = st.columns(3)
    with col1:
        sel1 = st.selectbox("Checkliste A", checkup_names, index=0, key="check1")
    with col2:
        sel2 = st.selectbox("Checkliste B", checkup_names, index=1, key="check2")
    with col3:
        sel3 = st.selectbox("Checkliste C (optional)", ["- keine -"] + checkup_names, index=0, key="check3")

    if st.button("🔍 Vergleichen mit Dr. Know"):
        selected_files = [sel1, sel2]
        if sel3 != "- keine -":
            selected_files.append(sel3)

        contents = []
        for filename in selected_files:
            file_path = CHECKUP_ASCII_DIR / filename
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    contents.append(f.read())
            except Exception as e:
                st.error(f"Fehler beim Laden von {filename}: {e}")
                return

        combined_query = f"""
Bitte vergleiche und erkläre das Zusammenspiel folgender Checklisten:

1. {sel1}
2. {sel2}
""" + (f"3. {sel3}\n" if sel3 != "- keine -" else "") + """

Hier sind die Inhalte der Checklisten:
""" + "\n\n---\n\n".join(contents) + """

Ziel: Erkläre, wie sich die Inhalte überschneiden, ergänzen oder widersprechen.
Gib auch Hinweise, in welchen regulatorischen Szenarien ein kombinierter Einsatz sinnvoll wäre.

Zusatzfrage:
Erstelle am Ende eine übergeordnete ASCII-Gesamt-Checkliste, die das potenzielle Zusammenspiel der zu prüfenden Checklisten plakativ darstellt.

Bitte gib eine strukturierte Einschätzung.
"""

        with st.spinner("Dr. Know analysiert die Überschneidungen..."):
            response, *_ = handle_query(query=combined_query, model_name=model_name, context={})
            with st.expander("### 🧠 Dr. Knows Antwort zum Vergleich & Zusammenspiel", expanded=True):
                st.markdown(response)

def render_ascii_checkup_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar):
    st.subheader(title)
    st.write(description)

    if not CHECKUP_ASCII_DIR.exists():
        st.warning("❗️Der Ordner `./assets/ascii/check_ups/` ist nicht vorhanden.")
        return

    checkup_files = [file for file in CHECKUP_ASCII_DIR.iterdir() if file.is_file() and file.suffix in [".txt", ".asc"]]
    st.info(f"🧾 Im lokalen Ordner befinden sich aktuell **{len(checkup_files)} Check-Ups**.")
    
    selected_file = st.selectbox("📄 Wähle eine Checkliste zur Erklärung:", [f.name for f in checkup_files])
    chat_key = f"chat_checklist_{selected_file}"

    vague_markers = [
        "ohne spezifische Informationen", 
        "nicht direkt beantwortet werden", 
        "müsste geprüft werden", 
        "kann nicht bestimmt werden", 
        "basierend auf den spezifischen Eigenschaften",
        "fehlende Information",
        "keine aktuellen Daten"
    ]

    if selected_file:
        selected_path = CHECKUP_ASCII_DIR / selected_file
        content = ""
        try:
            with st.expander(selected_file):
                with open(selected_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    st.code(content, language="markdown")
        except Exception as e:
            st.error(f"❌ Fehler beim Laden der Datei: {e}")
            return

        st.session_state.setdefault(chat_key, [])

        if st.button("🧠 Checkliste durch Dr. Know erklären lassen"):
            with st.spinner("**Dr. Know analysiert...**"):
                query = f"Bitte erkläre diese Checkliste in einfachen Worten. Erkläre Abkürzungen und Fachbegriffe:\n\n{content}"
                response, *_ = handle_query(query=query, model_name=model_name, context={})

                # Erkennung vager Antworten
                if any(marker in response.lower() for marker in vague_markers):
                    with st.spinner("Antwort unklar – starte automatische Websuche..."):
                        try:
                            with DDGS() as ddgs:
                                web_query = f"{selected_file} EU AI Act"
                                search_results = ddgs.text(web_query, max_results=5)
                                web_context = "\n\n".join(
                                    [f"**{r['title']}**\n{r.get('body', '')}\n🔗 {r['href']}" for r in search_results if r.get("href")]
                                ) if search_results else "Keine relevanten Web-Ergebnisse gefunden."
                        except Exception as e:
                            web_context = f"Fehler bei der Websuche: {e}"

                        final_query = f"""
Ein Nutzer möchte folgende Checkliste erklärt bekommen:
{selected_file}

Die ursprüngliche GPT-Antwort war zu unklar. Bitte analysiere die folgende Checkliste:
{content}

Hier sind 5 relevante Web-Ergebnisse zur Unterstützung:
{web_context}

Erkläre nun die Checkliste klar, verständlich und mit Bezug auf die Web-Infos.
"""
                        response, *_ = handle_query(
                            query=final_query,
                            model_name=model_name,
                            use_case="web_checklist_assistant",
                            context={}
                        )

                st.session_state[chat_key].append({"role": "assistant", "content": response})

        for msg in st.session_state[chat_key]:
            with st.expander("**Antwort Dr. Know:**", expanded=True):
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        user_input = st.chat_input("Stelle eine Rückfrage zu dieser Checkliste...")
        if user_input:
            st.session_state[chat_key].append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            with st.chat_message("assistant"):
                with st.spinner("**Dr. Know denkt nach ...**"):
                    followup_query = f"Die folgende Rückfrage bezieht sich auf eine erklärte Checkliste:\n\nCheckliste:\n{content}\n\nFrage: {user_input}\n\nBitte antworte klar und verständlich."
                    response, *_ = handle_query(query=followup_query, model_name=model_name, context={})

                    # Auch hier ggf. Web-Recherche starten
                    if any(marker in response.lower() for marker in vague_markers):
                        with st.spinner("Antwort unklar – Web wird konsultiert..."):
                            try:
                                with DDGS() as ddgs:
                                    web_query = user_input
                                    search_results = ddgs.text(web_query, max_results=5)
                                    web_context = "\n\n".join(
                                        [f"**{r['title']}**\n{r.get('body', '')}\n🔗 {r['href']}" for r in search_results if r.get("href")]
                                    ) if search_results else "Keine relevanten Web-Ergebnisse gefunden."
                            except Exception as e:
                                web_context = f"Fehler bei der Websuche: {e}"

                            enhanced_prompt = f"""
Ein Nutzer hat diese Rückfrage zu einer Checkliste gestellt:
\"{user_input}\"

Die ursprüngliche Antwort war nicht hilfreich. Hier ist der Kontext aus dem Web:

{web_context}

Bitte beantworte die Frage nun fundiert und klar.
"""
                            response, *_ = handle_query(
                                query=enhanced_prompt,
                                model_name=model_name,
                                use_case="web_checklist_assistant",
                                context={}
                            )
                    with st.expander("**Antwort Dr. Know:**", expanded=True):
                        st.markdown(response)
                        st.session_state[chat_key].append({"role": "assistant", "content": response})

    # === Admin-Funktion
    if st.session_state.user_role == "adm":
        if st.button("💾 Checklisten in Datenbank speichern"):
            ascii_files = []
            loaded, failed = 0, 0
            for file in checkup_files:
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        content = f.read()
                        ascii_files.append({
                            "filename": file.name,
                            "content": content
                        })
                        loaded += 1
                except Exception as e:
                    failed += 1
                    st.error(f"Fehler bei {file.name}: {e}")
            save_ascii_files_to_db(ascii_files)
            st.success(f"✅ {loaded} Checklisten wurden gespeichert.")
            if failed:
                st.warning(f"⚠️ {failed} Dateien konnten nicht gelesen werden.")

    render_checklist_comparison_view(use_case, context, title, description, session_file, system_message, model_name, settings, collection, sidebar)
