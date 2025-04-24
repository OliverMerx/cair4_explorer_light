"""
=================================================
🔗 CAIR4 Website Chatbot (ChatbotWeb)
=================================================
Ermöglicht interaktive Abfragen zu Webseiten-Inhalten
mit `ConversationalRetrievalChain` + persistenter Speicherung in `CAIR4_session_manager`.
    
📌 **Funktionen:**
- **Webseiten analysieren & speichern:** Scraped Webseiten in einer Vektordatenbank.
- **Langchain Conversational Retrieval Chain:** Verwendet ein KI-Modell für Webseiten-gestützte Chats.
- **CAIR4-Session-Management:** Speichert den Gesprächsverlauf in `st.session_state` & JSON.

✅ **Warum CAIR4-Standard?**
- **Echtzeit-Streaming** über `StreamHandler`
- **Langchain Memory + Persistenz** → Kombiniert `ConversationBufferMemory` mit CAIR4-Session-Speicherung.
"""


import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
import validators

# 🔄 **CAIR4-Module für Session-Handling**
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics

# 🌍 **Embedding-Modell für die Vektordatenbank**
embedding_model = OpenAIEmbeddings()

def scrape_website(url):
    """Holt sauberen Text von einer Webseite."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all(["p", "h1", "h2", "h3"])
    text = "\n".join([p.get_text() for p in paragraphs])
    return text

def setup_vector_db(content):
    """Erstellt eine Vektor-Datenbank für die Webseite."""
    docs = [Document(page_content=content, metadata={"source": "web"})]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 🛠 **Embedding-Modell übergeben**
    vectordb = DocArrayInMemorySearch.from_documents(splits, embedding_model)
    return vectordb

def setup_qa_chain(vectordb):
    """Erstellt eine RAG-Pipeline mit Memory."""
    retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})
    memory = ConversationBufferMemory(memory_key="chat_history", output_key="answer", return_messages=True)
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-4o"),
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )
    return qa_chain

def render_website_dialog_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.markdown(description)

    # Initiale States
    st.session_state.setdefault("web_scrape_triggered", False)
    st.session_state.setdefault("web_content", "")
    st.session_state.setdefault("qa_chain", None)

   # 🔘 Vorauswahl der Webseite (inkl. Link-Handling)
    st.markdown("### 🌐 Wähle eine Beispiel-Webseite oder gib deine eigene URL ein")

    options = {
        "🌍 Tagesschau (ohne weiterführende Links)": {
            "url": "https://www.tagesschau.de/brasilien-ts-120.html",
            "show_links": False
        },
        "🧠 CAIR4-Artikel (mit weiterführenden Links)": {
            "url": "https://cair4.eu/nachgelagerte-anbieter-1-das-matrjoschka-problem",
            "show_links": True
        },
        "🔗 Eigene URL eingeben": {
            "url": None,
            "show_links": None
        }
    }

    selection = st.radio("Webseiten-Auswahl:", list(options.keys()))
    selected_option = options[selection]

    if selection == "🔗 Eigene URL eingeben":
        custom_url = st.text_input("🔧 Eigene URL eingeben:")
        url = custom_url
        show_links = None
    else:
        url = selected_option["url"]
        show_links = selected_option["show_links"]
        st.session_state["show_links"] = show_links
        st.markdown(f"[🌐 Seite in neuem Tab öffnen]({url})", unsafe_allow_html=True)

    # 🔘 Button zum Starten des Scraping
    if st.button("🔄 Webseite laden und analysieren"):
        if url and validators.url(url):
            with st.spinner("Lade und analysiere die Webseite..."):
                content = scrape_website(url)
                vectordb = setup_vector_db(content)
                qa_chain = setup_qa_chain(vectordb)

                st.session_state["web_scrape_triggered"] = True
                st.session_state["web_content"] = content
                st.session_state["qa_chain"] = qa_chain
        else:
            st.warning("Bitte gib eine gültige URL ein.")

    # 📄 Zeige geladenen Webseiten-Text
    if st.session_state["web_scrape_triggered"]:
        st.markdown("### 📄 Eingelesener Webseiten-Text")
        st.info("Der folgende Text wurde erfolgreich extrahiert:")
        st.caption(st.session_state["web_content"])

        # 🛡️ Session-Setup
        st.session_state.setdefault("web_sessions", {})
        if url not in st.session_state["web_sessions"]:
            st.session_state["web_sessions"][url] = {"messages": []}
        messages = st.session_state["web_sessions"][url]["messages"]

        # 💬 Verlauf anzeigen
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # 💡 User-Eingabe
        user_query = st.chat_input("Frage zur Webseite:")
        if user_query:
            with st.chat_message("user"):
                st.markdown(user_query)
            append_message(st.session_state["web_sessions"][url], "user", user_query)

            with st.chat_message("assistant"):
                with st.spinner("Denke nach..."):
                    response = st.session_state["qa_chain"].invoke({"question": user_query})
                    assistant_reply = response["answer"]

                    st.markdown(assistant_reply)
                    append_message(st.session_state["web_sessions"][url], "assistant", assistant_reply)

                # 📌 Quellen
                for idx, doc in enumerate(response["source_documents"], 1):
                    with st.expander(f":blue[Quelle {idx}]"):
                        st.caption(doc.page_content)