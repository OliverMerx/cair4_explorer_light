"""
=================================================
💬 CAIR4 Finetuning View
=================================================

📌 **Beschreibung:**
Diese View implementiert die **Finetuning-Funktionalität** und integriert alle erforderlichen Framework-Komponenten.

✅ **Hauptfunktionen:**
- **Session-Verwaltung:** Lädt und speichert Sitzungen für langfristige Interaktionen.
- **Logging & Debugging:** Nutzt DebugUtils für eine detaillierte Fehleranalyse.
- **Query-Handling:** Übergibt Nutzeranfragen an das CAIR4-KI-System.

🔍 **Automatische Generierung:**  
Diese View wurde vom **CAIR4 Code Creator** erzeugt und kann direkt in das Framework eingebunden werden.
"""

# === 1️⃣ Import externer Bibliotheken (3rd Party Libraries) ===
# pylibs
from pylibs.os_lib import os as os
from pylibs.streamlit_lib import streamlit as st
from pylibs.json_lib import json as json
from pylibs.datetime_lib import initialize_datetime
from pylibs.matplotlib_pyplot_lib import initialize_matplotlib_pyplot
from pylibs.numpy_lib import numpy as np
from pylibs.time_lib import initialize_time, now, sleep

plt = initialize_matplotlib_pyplot()
datetime = initialize_datetime()
time = initialize_time()

# utils
from utils.core.CAIR4_update_sidebar import update_sidebar

# controller
from controllers.CAIR4_controller import handle_query

# utils
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_message_manager import append_message
from utils.core.CAIR4_metrics_manager import update_metrics
from utils.core.CAIR4_debug_utils import DebugUtils  # Import der Debug-Klasse

def render_finetuning_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    DebugUtils.debug_print(f"render_finetuning_view gestartet für Use Case: {use_case}")

    # === Initialisiere Sitzung ===
    sessions = load_sessions(session_file)
    st.session_state.setdefault("finetuning_sessions", {})
    st.session_state.finetuning_sessions[use_case] = sessions

    if "active_use_case" not in st.session_state or st.session_state["active_use_case"] != use_case:
        st.session_state["active_use_case"] = use_case
        st.session_state["current_session"] = {
            "messages": [],
            "metrics": {
                "total_tokens": 0,
                "total_costs": 0.0,
                "tokens_used_per_request": [],
                "costs_per_request": [],
                "request_names": [],
            },
            "calculations": []
        }

    # === Layout ===
    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    st.markdown("### 🔁 Finetuning-Simulation starten")
    if st.button("🚀 Finetuning starten"):
        st.session_state["finetune_start_triggered"] = True

    # === Simuliere Training nur bei Trigger ===
    if st.session_state.get("finetune_start_triggered", False):
        DebugUtils.debug_print("Finetuning gestartet durch Benutzer")

        epochs = list(range(1, 51))
        perfect_fit = []
        too_few_points = [np.exp(-epoch / 10) + np.random.normal(0, 0.05) if epoch % 5 == 0 else None for epoch in epochs]
        overfitting = [np.exp(-epoch / 10) + np.random.normal(0, 0.01) if epoch < 30 else np.exp(-epoch / 30) + np.random.normal(0, 0.02) for epoch in epochs]

        chart_placeholder = st.empty()

        for epoch in epochs:
            loss = np.exp(-epoch / 10) + np.random.normal(0, 0.01)
            perfect_fit.append(loss)

            fig, ax = plt.subplots()
            ax.plot(epochs[:epoch], perfect_fit, label="Perfect Fit", color="blue", linestyle='-')
            ax.plot(epochs, too_few_points, label="Zu Wenig Stützpunkte", color="red", marker='o', linestyle='None')
            ax.plot(epochs, overfitting, label="Overfitting", color="green", linestyle='--')
            ax.set_xlabel("Epoche")
            ax.set_ylabel("Loss")
            ax.set_title("Finetuning: Vergleich von Trainingsszenarien")
            ax.legend()
            chart_placeholder.pyplot(fig)

            time.sleep(0.2)

            calculation_data = {
                "event": "Finetuning-Iteration",
                "parameters": {
                    "epoch": epoch,
                    "loss": loss,
                    "perfect_fit": perfect_fit[-1],
                    "overfitting": overfitting[epoch - 1]
                },
                "timestamp": datetime.datetime.now().isoformat()
            }

            st.session_state["current_session"]["calculations"].append(calculation_data)
            DebugUtils.debug_print(f"Epoch {epoch}: {loss}")

        # Nach Ablauf zurücksetzen & speichern
        st.session_state.finetune_start_triggered = False
        st.session_state.finetuning_sessions[use_case].append(st.session_state["current_session"])
        save_sessions(session_file, st.session_state.finetuning_sessions[use_case])
        DebugUtils.debug_print("Finetuning abgeschlossen und gespeichert")
    
st.markdown("""
    <style> 
    [data-testid="stBottomBlockContainer"] {
    background-color: #ccc !important;
    background:transparent!important;
    }
    </style>
    """, unsafe_allow_html=True
    )