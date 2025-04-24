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

from models.core.CAIR4_chromadb_client import get_or_create_collection  # Verbindung zu ChromaDB-Client

def list_collection_contents(collection_name):
    """
    Listet alle Dokumente einer ChromaDB-Collection auf.
    """
    try:
        collection = get_or_create_collection(collection_name)
        
        results = collection.get(include=["documents", "metadatas"])  # ✅ Holt alle Dokumente + Metadaten

        if not results or "documents" not in results or not results["documents"]:
            print(f"⚠️ Keine Ergebnisse für Collection '{collection_name}'.")
            return []
        
        return [
            {"name": meta.get("source", "Unknown"), "content": doc, "pages": meta.get("page", 1)}
            for doc, meta in zip(results["documents"], results["metadatas"])
        ]

    except Exception as e:
        print(f"❌ Fehler beim Abrufen der Collection-Inhalte: {e}")
        return []