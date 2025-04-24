DESCRIPTION = "Importiert Ollama als Plattform für lokale LLM"

# py_lib/ollama_lib.py
import ollama

def initialize_ollama():
    """
    Initialisiert und gibt die ollama-Instanz zurück.
  

    Returns:
        ollama Die ollama-Instanz für den weiteren Gebrauch.
    """
    return ollama