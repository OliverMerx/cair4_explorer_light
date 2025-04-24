"""
==========================
💡 CAIR4 Log Viewer
==========================
Dieses Modul ermöglicht das Laden, Filtern und Visualisieren von Log-Daten innerhalb der CAIR4-Plattform. 
Es bietet eine Benutzeroberfläche zur Auswahl eines spezifischen Datums sowie Visualisierungen der erfassten Logs.

📌 Funktionen:
- **render_logs_view()** → Hauptfunktion zum Anzeigen des Log Viewers mit Datumsauswahl.
- **group_logs_by_date()** → Gruppiert die Log-Einträge nach Datum für eine einfachere Auswahl.
- **render_filtered_logs()** → Zeigt gefilterte Logs für das ausgewählte Datum in einer Tabelle.
- **render_statistics_and_visuals()** → Erstellt Statistiken und Visualisierungen auf Basis der Logs.

✅ Warum ist das wichtig?
- Ermöglicht eine **strukturierte Analyse** vergangener Aktivitäten in der Anwendung.
- Identifiziert schnell **Abstürze und Sitzungsaktivitäten**.
- Visualisiert die **Verteilung der genutzten Use Cases**.
"""

# 🛠 3rd Party Libraries
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.pandas_lib import pandas as pd
from pylibs.datetime_lib import initialize_datetime
from pylibs.matplotlib_pyplot_lib import initialize_matplotlib_pyplot

# 📌 CAIR4 Utilities
from utils.core.CAIR4_log_manager import load_logs

# 📊 Initialisierung externer Bibliotheken
plt = initialize_matplotlib_pyplot()
datetime = initialize_datetime()

def group_logs_by_date(log_entries):
    """
    Gruppiert Log-Einträge nach Datum basierend auf dem Timestamp.

    ✅ Ablauf:
    - Extrahiert das **Datum** aus dem Timestamp der Logs.
    - Gruppiert die Einträge nach **jeweiligem Datum**.

    Args:
        log_entries (list): Liste der Log-Einträge.

    Returns:
        dict: Ein Dictionary, das die Log-Einträge nach Datum gruppiert.
    """
    grouped_logs = {}
    for entry in log_entries:
        timestamp = entry.get("timestamp", "Unknown")
        try:
            date = datetime.datetime.fromisoformat(timestamp).strftime("%Y-%m-%d")  # Datum extrahieren
        except ValueError:
            date = "Unknown"

        if date not in grouped_logs:
            grouped_logs[date] = []
        grouped_logs[date].append(entry)

    return grouped_logs

def render_logs_view(log_file):
    """
    Zeigt die Log-Übersicht mit einer Auswahl für das gewünschte Datum an.

    ✅ Ablauf:
    - Lädt die Logs aus der Datei.
    - Bietet eine **Dropdown-Auswahl** für verschiedene Datumswerte.
    - Zeigt eine **Tabelle** mit den gefilterten Logs.
    - Erstellt **Statistiken und Visualisierungen**.

    Args:
        log_file (str): Pfad zur Logdatei.
    """
    st.title("📜 Session Logs Viewer")

    try:
        logs = load_logs(log_file)  # Logs laden
        log_entries = logs.get("entries", [])
        grouped_logs = group_logs_by_date(log_entries)
    except FileNotFoundError:
        st.error("❌ Log-Datei nicht gefunden.")
        return
    except Exception as e:
        st.error(f"⚠️ Fehler beim Laden der Logs: {e}")
        return

    # 🗓 Dropdown für Datumsauswahl
    available_dates = sorted(grouped_logs.keys(), reverse=True)
    if "Unknown" in available_dates:
        available_dates.remove("Unknown")

    if not available_dates:
        st.warning("⚠️ Keine gültigen Log-Einträge gefunden.")
        return

    selected_date = st.selectbox("📅 Wähle ein Datum", options=available_dates, index=0)

    if selected_date:
        st.subheader(f"📑 Logs für {selected_date}")
        filtered_logs = grouped_logs.get(selected_date, [])
        render_filtered_logs(filtered_logs)

        # 📊 Visualisierungen für das gewählte Datum
        st.subheader("📊 Visual Insights: Gewähltes Datum")
        render_statistics_and_visuals(filtered_logs)

        # 📈 Visualisierungen für alle Logs
        st.subheader("📈 Visual Insights: Alle Logs")
        render_statistics_and_visuals(log_entries)
    else:
        st.info("ℹ️ Kein Datum ausgewählt. Bitte wähle ein Datum.")

def render_filtered_logs(filtered_logs):
    """
    Zeigt die gefilterten Logs als Tabelle an.

    ✅ Ablauf:
    - Falls Einträge vorhanden sind → **Tabelle anzeigen**.
    - Falls keine Einträge vorhanden sind → **Warnung ausgeben**.

    Args:
        filtered_logs (list): Gefilterte Log-Einträge.
    """
    st.subheader("📄 Gefilterte Logs")
    if filtered_logs:
        df = pd.DataFrame(filtered_logs)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Keine Logs für das gewählte Datum gefunden.")

def render_statistics_and_visuals(log_entries):
    """
    Erstellt Statistiken und Visualisierungen auf Basis der Logs.

    ✅ Ablauf:
    - Berechnet **Anzahl der Sitzungen & Abstürze**.
    - Ermittelt die **Verteilung der Use Cases**.
    - Erstellt **Balkendiagramme & Kreisdiagramme** zur Visualisierung.

    Args:
        log_entries (list): Liste der Log-Einträge.
    """
    if not log_entries:
        st.warning("⚠️ Keine Logs für Visualisierungen verfügbar.")
        return

    # 📊 Berechnung der Log-Statistiken
    total_logs = len(log_entries)
    total_sessions = sum(1 for entry in log_entries if entry["action"] == "Loaded Sessions")
    total_crashes = sum(1 for entry in log_entries if entry["action"] == "Application Crashed")

    # 📌 Verteilung der Use Cases analysieren
    use_case_counts = {}
    for entry in log_entries:
        use_case = entry.get("details", {}).get("use_case", "Unknown")
        if use_case in use_case_counts:
            use_case_counts[use_case] += 1
        else:
            use_case_counts[use_case] = 1

    # 📊 Erstellung der Diagramme
    fig_bar, ax_bar = plt.subplots()
    ax_bar.bar(["Total Logs", "Loaded Sessions", "Application Crashes"], 
               [total_logs, total_sessions, total_crashes], 
               color=["#1976D2", "#4CAF50", "#FF5722"])
    ax_bar.set_ylabel("Count")
    ax_bar.set_title("🔍 Log-Statistiken")

    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(use_case_counts.values(), labels=use_case_counts.keys(), autopct="%1.1f%%", startangle=90)
    ax_pie.set_title("📊 Use Case Verteilung")

    # 📌 Grafiken nebeneinander anzeigen
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig_bar)
    with col2:
        st.pyplot(fig_pie)