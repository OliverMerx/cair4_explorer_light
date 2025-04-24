DESCRIPTION = "Visualisierung komplexen Matrizen, BarCharts etc."

import plotly.express as px

def initialize_plotly_express():
    """
    Gibt die plotly.express-Instanz zurück.
    
    Returns:
        px: Die plotly.express-Instanz.

        ACHTUNG: MUSS bei Start initialisiert werden -> px = initialize_plotly_express()
 
    """
    
    return px