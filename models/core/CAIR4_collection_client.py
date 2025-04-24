"""
=================================================
📂 CAIR4 ChromaDB Collection Client
=================================================

Dieses Modul verwaltet die Interaktion mit ChromaDB auf Collection-Ebene. Es ermöglicht die Erstellung, Verwaltung und Abfrage von Collections, die für Retrieval-Augmented Generation (RAG) genutzt werden.
ChromaDB ist eine Vektor-Datenbank, die es ermöglicht, semantische Suchanfragen auszuführen. Die Daten werden als numerische Vektoren gespeichert, was eine inhaltliche (nicht nur wörtliche) Suche erlaubt.

🔹 **Aufgrund der unterschiedlichen Modellarchitekturen wird ChromaDB bei CAIR4 primär mit OpenAI genutzt, da OpenAI eine direkte API für Embeddings bietet.**  
Andere Modelle wie LLaMA oder DeepSeek können ebenfalls eingebunden werden, erfordern jedoch eine separate Embedding-Generierung durch externe Modelle wie SentenceTransformers.

🔧 **Funktionalitäten:**
- **get_or_create_collection(collection_name)**  
  ➝ Erstellt oder lädt eine ChromaDB-Collection.
- **list_collection_contents(collection_name, query_text, n_results, embedding_model)**  
  ➝ Führt eine semantische Suche in einer Collection aus.

🚀 **Anwendungsfälle:**
- KI-gestützte Chatbots mit Langzeitgedächtnis (RAG)
- Automatische Dokumentensuche und Kategorisierung
- KI-gestützte Wissensdatenbanken

✅ **Wichtig:**  
Dieses Modul arbeitet mit `chroma_db_client.py` zusammen, das die eigentliche ChromaDB-Verbindung verwaltet.

=================================================
"""

try:
    from pylibs.chromadb_lib import CHROMA_AVAILABLE, initialize_chroma_db
    chroma_client = initialize_chroma_db() if CHROMA_AVAILABLE else None
except Exception as e:
    print(f"❌ ChromaDB konnte nicht geladen werden: {e}")
    chroma_client = None
    CHROMA_AVAILABLE = False

def get_or_create_collection(collection_name):
    if not CHROMA_AVAILABLE or chroma_client is None:
        print("⚠️ ChromaDB nicht verfügbar – Collection kann nicht erstellt werden.")
        return None

    try:
        collections = [col.name for col in chroma_client.list_collections()]
        if collection_name in collections:
            return chroma_client.get_collection(collection_name)
        return chroma_client.create_collection(name=collection_name)
    except Exception as e:
        print(f"❌ Fehler bei ChromaDB-Zugriff: {e}")
        return None