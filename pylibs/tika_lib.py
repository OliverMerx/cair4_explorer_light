DESCRIPTION = "Bibliothek für Tokenisieren von Texten v. OpenAi."

# py_lib/tika_lib.py
import tika

def initialize_tika():
    """
    Initialisiert und gibt die tika-Instanz zurück.
    
    Returns:
        tika: Die tika-Instanz für den weiteren Gebrauch.
    """
    return tika