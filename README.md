# CAIR4 Use Case Explorer – Light Edition 

Willkommen zur **Light-Version des CAIR4 Use Case Explorers**.  
Diese Anwendung demonstriert ausgewählte KI-Use-Cases und ihren
regulatorischen Impact in einer modularen Streamlit-Oberfläche 
– ganz ohne Login oder Backend-Abhängigkeiten wie in der Vollversion
(diese hat über 80 Use Cases, Stand April 2025).

Die Light-Version enthält zwar die gesamten Use Case Beschreibungen der Config-Datei
(für Navigation und Übersichten), es sind jedoch nicht alle Python-
Dateien der Use Cases mit integriert. Dies würde aufgrund der Komplexität
das Installieren zusätzlicher Python-Libs und somit ein einfaches 
initiales Setup erheblich erschweren würden. 

Die Light-Version ist gedacht für Demos, Tests und zum Einstieg in die CAIR4-Logik.

Mit ihr können auch eigene CAIR4-Codes entwickelt und verprobt werden. 

---

## Features

- **Use Case Explorer** mit selektierten KI-Beispielen
- **Zugriff ohne Login** (Gastmodus: Vollversion mit Role Based Access)
- **Leichtgewichtig**: Nur essenzielle Module & Views
- **Rechtliche Referenzen, Analysen & Kapitelstruktur**
- **ASCII-Checklisten, ASCII-Use-Case-Descriptions**
- **Dr. Know: Legal Expert Chat** (in Vollversion)
- **How-To-Erklärungsvideos** (in Deutsch)
- **Prompt-basierte KI-Analyse** (OpenAI, Gemini, Mistral etc.)

---

## Projektstruktur

```bash
CAIR4_light/
│
├── core/                    # Konfiguration & Views
├── models/                  # Modell-Schnittstellen
├── pylibs/                  # Hilfsbibliotheken
├── utils/                   # Interne Tools (z. B. Encryption, Backgrounds)
├── assets/                  # Icons, Bilder
├── .env.example             # Vorlage für API-Keys
├── requirements.txt         # Abhängigkeiten
├── CAIR4_explorer.py        # Einstiegspunkt
└── README.md                

## 📜 Lizenz

Dieses Projekt steht unter der MIT-Lizenz – siehe [MIT_LICENSE](./MIT_LICENSE).

## 📬 Kontakt

Für Rückfragen, Feedback oder Interesse an der Vollversion:  
📧 oliver.merx@protonmail.com  
🔗 [LinkedIn-Profil](https://www.linkedin.com/in/oliver-m-merx-83777b/)


# 1. Repository klonen
git clone https://github.com/OliverMerx/cair4_light.git
cd cair4_light

# 2. Virtuelle Umgebung erstellen (optional aber empfohlen)
python3 -m venv venv
source venv/bin/activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt


# Datei .env anlegen auf Basis der Vorlage
cp .env.example .env
# und dort z. B. eintragen:
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...

# Alternativ können auch API-Keys für einzelne KI-Modelle temporär integriert werden (home -> api-keys)
