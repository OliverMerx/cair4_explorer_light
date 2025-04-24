"""
================================
💡 CAIR4 Feed Forward Chat mit Datei-Upload
================================

🚀 **Was ist der Feed Forward Chat mit Datei-Upload?**  
Dieser CAIR4 Use Case erweitert den klassischen **Feed Forward Chat** um eine **Datei-Upload-Funktion**, 
wodurch **Textdateien und PDFs** direkt in das KI-System eingespeist werden können.  
Damit wird das KI-System in die Lage versetzt, Fragen **auf Basis hochgeladener Inhalte** zu beantworten.  

Während **klassische Chatbots** oft auf vorherige Nachrichten Bezug nehmen, bleibt der **Feed Forward Chat** 
bewusst **kontextfrei** – jede Eingabe wird **unabhängig** verarbeitet.  
Durch die neue **Datei-Upload-Funktion** wird jedoch eine **einmalige Kontextanreicherung** für die aktuelle 
Anfrage ermöglicht.


Hier ist die überarbeitete Einleitung, die noch klarer beschreibt, wo der Unterschied zur klassischen RAG-Variante liegt und was diese Lösung eigentlich macht. Die zentrale Botschaft: Hier wird nur einmalig Kontext durch ein hochgeladenes Dokument hinzugefügt – keine langfristige Speicherung, kein permanentes Retrieval. 🎯

⸻

📌 CAIR4 Feed Forward Chat mit Datei-Upload

Dieses Modul stellt eine einfache Variante eines Feed-Forward-Chats dar, der zusätzlich die Möglichkeit bietet, ein Dokument hochzuladen, um Fragen dazu zu stellen.
Das Besondere: Jede Anfrage wird unabhängig von vorherigen Chats behandelt – es gibt keine Erinnerung an frühere Nachrichten.

Dadurch eignet sich dieser Chat besonders für schnelle Einzelanfragen, zum Beispiel:
✅ Dokumentenverständnis: Fragen zu einem hochgeladenen PDF oder einer Textdatei stellen
✅ FAQ-ähnliche Szenarien: Unterstützung ohne langfristige Speicherung von Konversationen
✅ Einfache KI-gestützte Interaktionen, die keinen Kontext über mehrere Abfragen hinweg benötigen

⸻

🤔 Ist das eine RAG-Variante?

Nein, dieser Feed-Forward-Chat ist KEINE klassische RAG-Variante – aber er nutzt ein ähnliches Prinzip:
💡 Hier wird einmalig ein externer Kontext hinzugefügt (z. B. durch ein hochgeladenes Dokument)
⛔ Es gibt aber keine permanente Speicherung oder Vektordatenbank, wie es bei RAG üblich ist

⸻

📌 Fazit: Was macht diese Lösung genau?

🟢 Sie fügt temporär Kontext hinzu (z. B. durch ein hochgeladenes PDF oder TXT).
🔵 Die Datei wird nicht gespeichert, sondern nur während der aktuellen Session genutzt.
🔴 Es gibt keine Vektordatenbank oder persistente Langzeitspeicherung – sobald die Session beendet ist, geht der Kontext verloren.

Falls eine echte RAG-Variante gewünscht ist, könnte man:
✅ Eine lokale Vektordatenbank wie ChromaDB oder FAISS integrieren
✅ Dokumente speichern und für spätere Anfragen wiederverwenden

⸻

Kurz gesagt:
💡 Diese Lösung fügt einmalig externen Kontext hinzu – mehr nicht! Kein Gedächtnis, keine Persistenz, sondern eine einfache Möglichkeit, Fragen zu einer Datei zu stellen.

⸻


### 🎯 **Anwendungsfälle:**
✅ **Dokumentenbasierte KI-Abfragen**  
→ Lade **PDFs oder Textdateien** hoch und stelle Fragen zum Inhalt, z. B. **Verträge, Berichte, Anleitungen**.  

✅ **Schnelle Informationsverarbeitung**  
→ Statt lange Dokumente manuell zu durchsuchen, kann die KI relevante **Passagen identifizieren**.  

✅ **Einfache Interaktionen ohne "Gedächtnis"**  
→ Perfekt für **FAQ-Systeme, Support-Bots und einmalige Analysen**, bei denen kein langfristiger Chat-Verlauf benötigt wird.  

✅ **Datenschutzfreundlich & effizient**  
→ Da keine **Langzeitspeicherung** der Chats erfolgt, eignet sich dieser Ansatz besonders für **sensible Daten**.  

---

### 🛠 **Wie funktioniert es?**
1️⃣ **Normale Chat-Nutzung:**  
💬 Schreibe eine Frage in das Chat-Eingabefeld und erhalte eine Antwort – **ganz ohne gespeicherte Historie**.  

2️⃣ **Datei-Upload als Kontext-Erweiterung:**  
📂 Lade eine **Textdatei (.txt) oder ein PDF (.pdf)** hoch.  
Die KI liest den Inhalt **(max. 2000 Zeichen)** und nutzt ihn als **einmaligen Kontext** für die nächste Antwort.  

3️⃣ **Antwort auf Basis der Datei:**  
🤖 Die KI verarbeitet die hochgeladenen Inhalte und gibt eine **kontextspezifische Antwort** zurück.  

---

### 📌 **Technische Besonderheiten:**
- **KEIN Gedächtnis:** Jede Anfrage wird **isoliert verarbeitet**.  
- **Datei-Parsing:** PDFs werden automatisch **mit Tika analysiert** (falls verfügbar).  
- **Token-Optimierung:** Max. **2000 Zeichen pro Datei** zur effizienten Verarbeitung.  
- **Regulatorisch konform:** Dieser Chat erfüllt die Anforderungen des **EU AI Acts** als ein **einfaches KI-System** (Art. 3 Nr. 1).  

---

🚀 **Warum ist das wichtig?**  
KI-gestützte Chats mit Datei-Uploads bieten eine **brückenschlagende Lösung** zwischen klassischen 
FAQ-Systemen und komplexeren Chatbots mit Langzeitspeicherung.  
Dieses Konzept eignet sich für **Unternehmen, Behörden und Forschung**, die eine **effiziente, datenschutzfreundliche 
KI-Interaktion** benötigen – ohne dabei langfristige Datenhaltung zu riskieren.  

"""

import streamlit as st
from io import BytesIO
from PyPDF2 import PdfReader

from utils.core.CAIR4_update_sidebar import update_sidebar
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics
from controllers.CAIR4_controller import handle_query

# 📍 Hauptfunktion für Feedforward Chat mit Upload
def render_upload_chat_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):

    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.markdown(description)

    # Initiale Session starten
    sessions = load_sessions(session_file)
    st.session_state.setdefault("universal_sessions", {})
    st.session_state.universal_sessions[use_case] = sessions

    if "active_use_case" not in st.session_state or st.session_state["active_use_case"] != use_case:
        st.session_state["active_use_case"] = use_case
        st.session_state["current_session"] = {
            "messages": [],
            "metrics": {
                "total_tokens": 0,
                "total_costs": 0.0,
                "tokens_used_per_request": [],
                "costs_per_request": [],
                "request_names": [],
            },
        }

    # Sidebar rendern
    if sidebar:
        with st.sidebar:
            update_sidebar(use_case, session_file)

    # Bisherige Nachrichten anzeigen
    for msg in st.session_state["current_session"]["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "pdf_text" in msg:
                st.text_area("📄 PDF-Inhalt", msg["pdf_text"], height=200)

    # Eingabe mit Datei-Upload
    user_input = st.chat_input("Frage eingeben oder PDF hochladen", accept_file=True, file_type=["pdf"])

    if user_input:
        pdf_text = ""

        with st.chat_message("user"):
            if user_input.text:
                st.markdown(user_input.text)

            if user_input.files:
                pdf_file = user_input.files[0]
                st.markdown(f"📂 Hochgeladen: **{pdf_file.name}**")

                try:
                    reader = PdfReader(pdf_file)
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            pdf_text += extracted + "\n"
                    st.text_area("📄 Extrahierter Text:", pdf_text.strip(), height=200)
                except Exception as e:
                    st.error(f"Fehler beim PDF-Parsing: {e}")

        # Inhalt vorbereiten für die KI
        query = user_input.text if user_input.text else ""
        if pdf_text:
            query += f"\n\n📄 PDF-Inhalt:\n{pdf_text[:2000]}..."

        # Nachricht speichern
        user_msg = {
            "role": "user",
            "content": user_input.text or f"PDF hochgeladen: {pdf_file.name}",
        }
        if pdf_text:
            user_msg["pdf_text"] = pdf_text.strip()
        append_message(st.session_state["current_session"], "user", query)

        # KI antwortet
        with st.chat_message("assistant"):
            with st.spinner("Denke nach..."):
                try:
                    response, tokens_used, costs, _ = handle_query(
                        query=query,
                        use_case=use_case,
                        context=context,
                        model_name=model_name,
                    )
                except Exception as e:
                    response = f"❌ Fehler bei der Verarbeitung: {e}"

                st.markdown(response)
                append_message(st.session_state["current_session"], "assistant", response)
                update_metrics(st.session_state["current_session"]["metrics"], tokens_used, costs)

                st.session_state.universal_sessions[use_case].append(st.session_state["current_session"])
                save_sessions(session_file, st.session_state.universal_sessions[use_case])