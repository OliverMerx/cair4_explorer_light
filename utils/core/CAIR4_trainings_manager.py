"""
===============================================
CAIR4 Data Manager (CAIR4_data_manager.py)
===============================================

Dieses Modul verwaltet die Speicherung und Verarbeitung von Use-Case-Daten 
und zugehörigen Trainingsinformationen für die CAIR4-Plattform.

📌 Funktionen:
- **ensure_file_exists()** → Stellt sicher, dass JSON-Dateien existieren.
- **load_data()** → Lädt Daten aus JSON-Dateien mit Fehlerhandling.
- **save_data()** → Speichert Use-Case- oder Trainingsdaten.
- **get_training_for_use_case()** → Ruft Training für einen bestimmten Use Case ab.
- **update_training_for_use_case()** → Aktualisiert Trainingsinhalte für einen Use Case.

✅ Warum ist das wichtig?
- Ermöglicht eine strukturierte Verwaltung von Use Cases & Trainingsdaten.
- Stellt sicher, dass inkorrekte JSON-Daten automatisch korrigiert werden.
- Vereinfacht das Speichern & Abrufen von Informationen für das System.
"""

# === 1️⃣  Import externer Bibliotheken ===
from pylibs.os_lib import os
from pylibs.json_lib import json

# === 2️⃣  Dateipfade & Konstanten ===
USE_CASE_FILE = "CAIR4_data/data/use_case_data.json"
TRAINING_FILE = "CAIR4_data/data/training_config.json"

# === 3️⃣  Datei-Management ===
def ensure_file_exists(file):
    """
    Stellt sicher, dass die Datei existiert. Falls nicht, wird sie mit einem Standardwert erstellt.

    Args:
        file (str): Der Dateipfad zur JSON-Datei.
    """
    if not os.path.exists(file):
        os.makedirs(os.path.dirname(file), exist_ok=True)

        default_content = [] if "use_case" in file else {}
        with open(file, "w", encoding="utf-8") as f:
            json.dump(default_content, f, indent=4, ensure_ascii=False)
        print(f"[INFO] Created new file: {file}")


# === 4️⃣  Daten-Handling ===
def load_data(file, data_type):
    """
    Lädt Daten aus einer JSON-Datei und stellt sicher, dass die Struktur korrekt ist.

    Args:
        file (str): Pfad zur JSON-Datei.
        data_type (str): "use_case" für Use Cases oder "training" für Trainingsdaten.

    Returns:
        list oder dict: Geladene Daten in korrektem Format.
    """
    ensure_file_exists(file)
    with open(file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)

            if data_type == "use_case":
                # 🔹 Falls fälschlicherweise als Dict gespeichert, in Liste umwandeln
                if isinstance(data, dict):
                    print("[WARNING] Use Case data was a dict, converting to list!")
                    data = list(data.values())
                    save_data(data, file, data_type)

            elif data_type == "training":
                # 🔹 Falls fälschlicherweise als Liste gespeichert, umwandeln
                if isinstance(data, list):
                    print("[WARNING] Training data was a list, converting to dictionary!")
                    data = {entry.get("Use Case", f"unknown_{i}"): entry for i, entry in enumerate(data)}
                    save_data(data, file, data_type)

            return data

        except json.JSONDecodeError:
            print(f"[ERROR] JSON format error in {file}, resetting to default values!")
            return [] if data_type == "use_case" else {}


def save_data(data, file, data_type):
    """
    Speichert die übergebenen Daten in die JSON-Datei.

    Args:
        data (list|dict): Die zu speichernden Daten.
        file (str): Der Dateipfad zur JSON-Datei.
        data_type (str): "use_case" oder "training" für Logging-Zwecke.
    """
    ensure_file_exists(file)
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[INFO] {data_type.capitalize()} data saved to {file}.")


# === 5️⃣  Trainingsverwaltung ===
def get_training_for_use_case(use_case, file=TRAINING_FILE):
    """
    Gibt die Trainingsinhalte für einen spezifischen Use Case zurück.

    Args:
        use_case (str): Der Name des Use Cases.
        file (str, optional): Der Dateipfad zur Trainingsdatei.

    Returns:
        dict: Trainingsdaten (Beschreibung, Rechtliches, Video-URL).
    """
    training_data = load_data(file, "training")
    return training_data.get(use_case, {
        "description": "Kein Trainingstext vorhanden.",
        "legal": "Keine rechtlichen Hinweise verfügbar.",
        "video_url": "",
    })


def update_training_for_use_case(use_case, description, legal, video_url, file=TRAINING_FILE):
    """
    Aktualisiert oder fügt Trainingsinhalte für einen Use Case hinzu.

    Args:
        use_case (str): Der Name des Use Cases.
        description (str): Beschreibung des Trainings.
        legal (str): Rechtliche Hinweise.
        video_url (str): URL zum Trainingsvideo.
        file (str, optional): Der Dateipfad zur Trainingsdatei.
    """
    training_data = load_data(file, "training")
    training_data[use_case] = {
        "description": description,
        "legal": legal,
        "video_url": video_url,
    }
    save_data(training_data, file, "training")
    print(f"[INFO] Training data for '{use_case}' updated.")