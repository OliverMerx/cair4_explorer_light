"""
=================================================
💾 CAIR4 ChromaDB Utility (Modellagnostisch)
=================================================

Dieses Modul stellt die ChromaDB-Verbindung bereit und bietet eine einheitliche Schnittstelle für Embeddings. 

🔹 **Aufgrund der unterschiedlichen Modellarchitekturen wird ChromaDB bei CAIR4 primär mit OpenAI genutzt, da OpenAI eine direkte API für Embeddings bietet.**  
Andere Modelle wie LLaMA oder DeepSeek können ebenfalls eingebunden werden, erfordern jedoch eine separate Embedding-Generierung durch externe Modelle wie SentenceTransformers.


📌 **Warum ist das Modul wichtig?**  
- **Persistente Speicherung:** Speichert und verwaltet Vektoren in ChromaDB.  
- **Modellagnostisch:** Unterstützt **OpenAI** und **SentenceTransformers** für Embeddings.  
- **Optimiert für RAG:** Ermöglicht schnelle semantische Suchanfragen in KI-Systemen.

🔧 **Wichtige Funktionen:**
- **initialize_chroma_client()**  
  ➝ Initialisiert ChromaDB mit Persistenz.  
- **generate_embedding(texts, embedding_model)**  
  ➝ Erstellt Embeddings für OpenAI oder lokale Modelle. 
- **get_or_create_collection(collection_name)**  
  ➝ Erstellt oder lädt eine ChromaDB-Collection. 

🚀 **Verwendung:**  
Dieses Modul wird insbesondere vom `CAIR4_collection_client.py` aber auch von andern CAIR4-Files genutzt (z.B. CAIR4_upload_view).

=================================================
"""
# === 1️⃣ Initialisierung nur, wenn chromadb verfügbar ist
try:
    import chromadb
    Client = chromadb.PersistentClient
    Settings = chromadb.Settings
    chroma_client = None
    CHROMA_AVAILABLE = True
except (ImportError, RuntimeError, Exception) as e:
    print("⚠️ chromadb konnte nicht geladen werden:", e)
    chroma_client = None
    Client = None
    Settings = None
    CHROMA_AVAILABLE = False

DEFAULT_CHROMA_PATH = "./chroma_db"
PYLIBS_DIR = "pylibs"
COLLECTIONS = {}

def initialize_chroma_db():
    global chroma_client
    if not CHROMA_AVAILABLE:
        print("⚠️ ChromaDB nicht verfügbar – Initialisierung wird übersprungen.")
        return None

    import os  # nachziehen, falls nötig
    from pylibs.streamlit_lib import streamlit as st

    if "chroma_name" not in st.session_state:
        st.session_state["chroma_name"] = DEFAULT_CHROMA_PATH

    db_path = st.session_state["chroma_name"]

    if not os.path.exists(db_path):
        os.makedirs(db_path)
        print(f"📁 ChromaDB-Verzeichnis erstellt: {db_path}")
    else:
        print(f"✅ ChromaDB-Verzeichnis gefunden: {db_path}")

    try:
        chroma_client = Client(path=db_path, settings=Settings(anonymized_telemetry=False))
        print("✅ ChromaDB erfolgreich initialisiert.")
    except Exception as e:
        print(f"❌ Fehler beim Initialisieren von ChromaDB: {e}")
        chroma_client = None

    return chroma_client

