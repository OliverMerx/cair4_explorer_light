DESCRIPTION = "Bibliothek für Tokenisieren von Texten v. OpenAi."

# py_lib/tiktoken_lib.py
import tiktoken

def initialize_tiktoken():
    """
    Initialisiert und gibt die tiktoken-Instanz zurück.
    
    Returns:
        tiktoken: Die tiktoken-Instanz für den weiteren Gebrauch.
    """
    return tiktoken