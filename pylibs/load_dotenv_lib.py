DESCRIPTION = "Laden von Variablen aus einer .env-Datei"

from dotenv import load_dotenv as original_load_dotenv

def initialize_load_dotenv():
    """
    Gibt die Funktion `load_dotenv` aus dem Paket `dotenv` zurück.

    Returns:
        function: Die `load_dotenv`-Funktion, um Umgebungsvariablen zu laden.

        ACHTUNG: MUSS bei Start initialisiert werden -> px = initialize_plotly_express()
    """
    return original_load_dotenv