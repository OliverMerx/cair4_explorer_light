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
import os
from pylibs.chromadb_lib import CHROMA_AVAILABLE, initialize_chroma_db

# === 1️⃣ Initialisierung nur, wenn chromadb verfügbar ist
if CHROMA_AVAILABLE:
    chroma_client = initialize_chroma_db()
else:
    chroma_client = None  # oder MockClient, je nach Anwendungsfall

# === 2️⃣ Optional: Embedding-Modell laden (funktioniert unabhängig)
from sentence_transformers import SentenceTransformer
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# === 3️⃣ Collection abrufen oder erstellen ===
def get_or_create_collection(collection_name):
    """Holt oder erstellt eine ChromaDB-Collection."""

    if not CHROMA_AVAILABLE or chroma_client is None:
        print("❌ ChromaDB ist nicht verfügbar. Collection kann nicht geladen werden.")
        return None

    try:
        collections = [col.name for col in chroma_client.list_collections()]
        if collection_name in collections:
            print(f"✅ Collection '{collection_name}' existiert bereits. Wird geladen.")
            return chroma_client.get_collection(collection_name)

        print(f"⚠️ Collection '{collection_name}' nicht gefunden. Erstelle neue...")
        return chroma_client.create_collection(name=collection_name)

    except Exception as e:
        print(f"❌ Fehler beim Zugriff auf ChromaDB: {e}")
        return None