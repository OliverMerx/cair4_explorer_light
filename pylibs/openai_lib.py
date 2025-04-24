DESCRIPTION = "Zugriff auf openai."

# py_lib/openai_lib.py
import openai

def initialize_openai():
    """
    Initialisiert und gibt die openai-Instanz zurück.
    
    Returns:
        oopenai: Die openai-Instanz für den weiteren Gebrauch.
    """
    return openai