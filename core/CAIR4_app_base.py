"""
💡 CAIR4 ChromaDB Manager
==========================
Chroma ist eine open-source KI-Datenbank. Dieses Modul verwaltet die 
Initialisierung und Verwaltung der ChromaDB-Instanz für die CAIR4-Plattform. 
Es stellt sicher, dass alle notwendigen Datenbank- und Session-Variablen 
korrekt initialisiert sind, bevor die Anwendung startet.

📌 Funktionen:
- **initialize_chroma_db()** → Startet den ChromaDB-Client und stellt sicher, 
  dass die Datenbank existiert.
- **initialize_collections()** → Lädt oder erstellt benötigte ChromaDB-Collections 
  basierend auf der Konfiguration.
- **ensure_directories()** → Stellt sicher, dass alle notwendigen Verzeichnisse 
  existieren.

✅ Warum ist das wichtig?
- Verhindert Abstürze durch fehlende Datenbankverzeichnisse oder fehlerhafte 
  Initialisierungen.
- Sorgt für eine **stabile und persistente Speicherung** der Vektordaten.
- Gewährleistet, dass die Datenbank mit den benötigten Sammlungen vorab 
  korrekt eingerichtet wird.
"""

# 🛠 3rd Party Libraries
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st

try:
    import chromadb
    Client = chromadb.PersistentClient
    Settings = chromadb.Settings
    chroma_client = None
    CHROMA_AVAILABLE = True
except (ImportError, RuntimeError) as e:
    print("⚠️ chromadb konnte nicht geladen werden:", e)
    chroma_client = None
    Client = None
    Settings = None
    CHROMA_AVAILABLE = False

DEFAULT_CHROMA_PATH = "./chroma_db"
PYLIBS_DIR = "pylibs"
COLLECTIONS = {}

def initialize_chroma_db():
    """
    Initialisiert den ChromaDB-Client und stellt sicher, dass die Datenbank existiert.
    """

    global chroma_client

    if not CHROMA_AVAILABLE:
        print("⚠️ ChromaDB nicht verfügbar – Initialisierung wird übersprungen.")
        return None

    # === ✅ 1. Sicherstellen, dass Session State korrekt initialisiert ist ===
    if "chroma_name" not in st.session_state:
        st.session_state["chroma_name"] = DEFAULT_CHROMA_PATH

    db_path = st.session_state["chroma_name"]

    # Falls das Verzeichnis nicht existiert, erstelle es
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

def initialize_collections():
    """
    Lädt oder erstellt ChromaDB-Collections basierend auf der Konfiguration.

    ✅ Ablauf:
    - Prüft, ob jede konfigurierte Collection existiert.
    - Falls nicht, wird sie neu erstellt.

    ⚠️ Fehlerbehandlung:
    - Falls eine Collection nicht abgerufen oder erstellt werden kann, wird dies protokolliert.
    """
    COLLECTIONS = st.session_state.get("collections", {})
    if chroma_client is None:
        print("⚠️ ChromaDB-Client nicht initialisiert! `initialize_chroma_db()` zuerst aufrufen.")
        return

    for collection_name, collection_config in COLLECTIONS.items():
        try:
            collection = chroma_client.get_collection(name=collection_config["name"])
            #print(f"✅ Collection '{collection_config['name']}' bereits vorhanden.")
        except Exception:
            print(f"⚠️ Collection '{collection_config['name']}' nicht gefunden. Erstelle neue...")
            try:
                chroma_client.create_collection(name=collection_config["name"], embedding_function=None)
                print(f"✅ Collection '{collection_config['name']}' erfolgreich erstellt.")
            except Exception as e:
                print(f"❌ Fehler beim Erstellen der Collection '{collection_config['name']}': {e}")

def ensure_directories():
    """
    Stellt sicher, dass alle benötigten Verzeichnisse existieren.

    📌 Erstellt folgende Verzeichnisse:
    - `CAIR4_data/data/` (für Logs, Sessions etc.)
    - `CAIR4_data/collections/` (ChromaDB Collections)

    """
    directories = ["CAIR4_data/data", PYLIBS_DIR, "CAIR4_data/collections"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"📂 Verzeichnis erstellt: {directory}")
        else:
            print(f"✅ Verzeichnis vorhanden: {directory}")