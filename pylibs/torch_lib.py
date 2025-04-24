DESCRIPTION = "Erstellen von Analysen und neuronalen Netzen."

# py_lib/torch_lib.py
import torch

def initialize_torch():
    """
    Initialisiert und gibt die torch-Instanz zurück.
    
    Returns:
        torch: Die torch-Instanz für den weiteren Gebrauch.
    """
    return torch