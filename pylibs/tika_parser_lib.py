DESCRIPTION = "Bibliothek für Tokenisieren von Texten v. OpenAi."

# py_lib/tika_parser_lib.py
from tika import parser

def initialize_parser():
    """
    Initialisiert und gibt die tika-parser-Instanz zurück.
    
    Returns:
        parser: Die tika-parser-Instanz für den weiteren Gebrauch.
    """
    return parser