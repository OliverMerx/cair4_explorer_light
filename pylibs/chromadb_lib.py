DESCRIPTION = "Embedding und vektorisierung von Inputs."

# py_lib/chromadb_lib.py
import chromadb

def initialize_chromadb():
    """
    Initialisiert und gibt die chromadb-Instanz zurück.
  

    Returns:
        chromadb: Die chromadb-Instanz für den weiteren Gebrauch.
    """
    return chromadb