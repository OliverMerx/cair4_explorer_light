DESCRIPTION = "Diese Bibliothek stellt Funktionen für Timer-Operationen bereit und ersetzt direkte `time`-Nutzung."

# py_lib/time_lib.py

import time

def initialize_time():
    """
    Initialisiert und gibt die Timer-Instanz zurück.
    
    Returns:
        module: Das `time`-Modul für den weiteren Gebrauch.
    """
    return time

def now():
    """
    Gibt den aktuellen Timestamp zurück (Ersatz für `time.time()`).
    
    Returns:
        float: Aktueller Zeitstempel.
    """
    return time.time()

def sleep(seconds):
    """
    Wrapper für `time.sleep()` - Verzögert die Ausführung um `seconds` Sekunden.
    
    Args:
        seconds (float): Dauer der Verzögerung in Sekunden.
    """
    time.sleep(seconds)