"""
=========================================
CAIR4 Metrics View
=========================================

Dieses Modul rendert das Metrics-Dashboard für Chat-Sessions.
Hier können Token-Nutzung und Kosten pro Anfrage analysiert werden.

Funktionen:
- `render_metrics_view()`: Erstellt die Metrik-Übersicht für die aktuelle oder ausgewählte Session.

Verwendung:
    render_metrics_view()
"""

# 🔹 Import notwendiger Bibliotheken
from pylibs.streamlit_lib import streamlit as st
from pylibs.pandas_lib import pandas as pd
from pylibs.plotly_express_lib import initialize_plotly_express

# 🔹 Plotly Express initialisieren
px = initialize_plotly_express()

def render_metrics_view():
    """
    Rendert das Metrics-Dashboard zur Analyse der Token-Nutzung und Kosten pro Anfrage.

    - Zeigt allgemeine Metriken (Tokens & Kosten).
    - Visualisiert die Verteilung über alle Anfragen.
    """
    
    # 🔹 Abrufen der Metrics-Daten
    if "selected_session" in st.session_state and st.session_state.selected_session is not None:
        sess = st.session_state.chat_sessions[st.session_state.selected_session]
        metrics = sess["metrics"]
    else:
        metrics = st.session_state.current_session["metrics"]

    # 🔹 Übersicht der Metriken
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📝 Tokens Used", metrics["total_tokens"])
    with col2:
        st.metric("💰 Costs", f"${metrics['total_costs']:.4f}")

    # 🔹 Daten für die Diagramme
    tokens_list = metrics.get("tokens_used_per_request", [])
    costs_list = metrics.get("costs_per_request", [])
    request_names = metrics.get("request_names", [])

    # 🔹 Debugging der Metrik-Daten
    print("Metrics Debugging:")
    print(f"Tokens per Request: {tokens_list}")
    print(f"Costs per Request: {costs_list}")
    print(f"Request Names: {request_names}")

    # 🔹 Falls keine Namen für Anfragen existieren → Standardwerte setzen
    if not request_names:
        request_names = [f"Request {i + 1}" for i in range(len(tokens_list))]

    # 🔹 Überprüfung der Datenkonsistenz
    if len(tokens_list) != len(costs_list) or len(tokens_list) != len(request_names):
        st.warning("⚠️ Die Listen für Tokens, Kosten und Anfrage-Namen sind nicht synchron.")
        print(f"Lengths -> Tokens: {len(tokens_list)}, Costs: {len(costs_list)}, Request Names: {len(request_names)}")
        return

    # 🔹 DataFrame für die Visualisierung erstellen
    df = pd.DataFrame({
        "Request Name": request_names,
        "Tokens Used": tokens_list,
        "Costs": costs_list
    })

    # 🔹 Token-Nutzung pro Anfrage visualisieren
    st.header("📌 Token Usage per Request")
    fig_tokens = px.bar(
        df,
        x="Request Name",
        y="Tokens Used",
        title="Tokens per Request",
        hover_data={"Request Name": True, "Tokens Used": True},
    )
    st.plotly_chart(fig_tokens)

    # 🔹 Kostenanalyse pro Anfrage visualisieren
    st.header("💲 Cost Analysis per Request")
    fig_costs = px.bar(
        df,
        x="Request Name",
        y="Costs",
        title="Costs per Request",
        hover_data={"Request Name": True, "Costs": True},
    )
    st.plotly_chart(fig_costs)