DESCRIPTION = "Bibliothek für Mistral LLM."

# py_lib/mistralai_lib.py
import mistralai 

def initialize_mistralai():
    """
    Initialisiert und gibt die mistralai-Instanz zurück.

    Returns:
        mistral: Die mistralai-Instanz für den weiteren Gebrauch.
    """
    return mistralai