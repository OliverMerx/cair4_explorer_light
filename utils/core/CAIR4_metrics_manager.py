"""
=================================================
CAIR4 Metrics Manager (CAIR4_metrics_manager.py)
=================================================

Dieses Modul verwaltet die Metriken für die Nutzung von AI-Modellen innerhalb einer Session.
Voraussetzung ist, dass beim jeweiligen View auch Metriken bzw. Modell erfaßt werden können (nicht immer möglich). 

Funktionen:
- `initialize_metrics()`: Erstellt ein Metrik-Objekt mit Standardwerten.
- `update_metrics(metrics, tokens_used, costs)`: Aktualisiert die Metriken mit neuen Token- & Kostenwerten.

Verwendung:
    from utils.core.CAIR4_metrics_manager import initialize_metrics, update_metrics

    metrics = initialize_metrics()
    update_metrics(metrics, tokens_used=100, costs=0.05)
"""
from pylibs.streamlit_lib import streamlit as st
from utils.core.CAIR4_debug_utils import DebugUtils  # Import der Debug-Klasse

# === 1️⃣ Metriken-Initialisierung ===
def initialize_metrics():
    """Initialisiert die Metriken für eine neue Session.

    Returns:
        dict: Ein Dictionary mit den Metriken für Token-Verbrauch & Kosten.
    """

    DebugUtils.debug_print(f"Metrics werden initialisiert.")

    metrix = {
        "total_tokens": 0,  # Gesamtanzahl der genutzten Token
        "total_costs": 0.0,  # Gesamtkosten für die API-Anfragen
        "tokens_used_per_request": [],  # Liste der genutzten Token pro Anfrage
        "costs_per_request": [],  # Liste der Kosten pro Anfrage
        "request_names": []  # Namen der API-Requests für Debugging/Tracking
    }
    if ["metrics"] not in st.session_state:
        st.session_state["metrics"]=metrix
    else:
        st.session_state["metrics"]=metrix

    return metrix


# === 2️⃣ Metriken-Aktualisierung ===
def update_metrics(metrics, tokens_used=0, costs=0.0, request_name=None):
    """Aktualisiert die Metriken sicher und verhindert Fehler durch fehlende Felder."""

    # Falls Metriken nicht existieren, initialisieren
    if "total_tokens" not in metrics:
        metrics["total_tokens"] = 0
    if "total_costs" not in metrics:
        metrics["total_costs"] = 0.0
    if "tokens_used_per_request" not in metrics:
        metrics["tokens_used_per_request"] = []
    if "costs_per_request" not in metrics:
        metrics["costs_per_request"] = []
    if "request_names" not in metrics:
        metrics["request_names"] = []

    # Werte hinzufügen
    metrics["total_tokens"] += tokens_used
    metrics["total_costs"] += costs
    metrics["tokens_used_per_request"].append(tokens_used)
    metrics["costs_per_request"].append(costs)
    
    if request_name:
        metrics["request_names"].append(request_name)