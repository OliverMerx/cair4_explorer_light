"""
=================================================
💬 CAIR4 Arbeitszeugnis View
=================================================

📌 **Beschreibung:**
Diese View implementiert die **Arbeitszeugnis-Funktionalität** und integriert alle erforderlichen Framework-Komponenten.

✅ **Hauptfunktionen:**
- **Session-Verwaltung:** Lädt und speichert Sitzungen für langfristige Interaktionen.
- **Logging & Debugging:** Nutzt DebugUtils für eine detaillierte Fehleranalyse.
- **Query-Handling:** Übergibt Nutzeranfragen an das CAIR4-KI-System.

🔍 **Automatische Generierung:**  
Diese View wurde vom **CAIR4 Code Creator** erzeugt und kann direkt in das Framework eingebunden werden.
"""

# === 1️⃣ Import externer Bibliotheken (3rd Party Libraries) ===
from pylibs.os_lib import os
from pylibs.streamlit_lib import streamlit as st
from pylibs.importlib_lib import importlib
from pylibs.datetime_lib import initialize_datetime

# Initialisiere `datetime`
datetime = initialize_datetime()

# === 2️⃣ Framework-Module laden ===
from utils.core.CAIR4_session_manager_hybrid import load_sessions, save_sessions
from utils.core.CAIR4_debug_utils import DebugUtils
from utils.core.CAIR4_update_sidebar import update_sidebar
from controllers.CAIR4_controller import handle_query
from utils.core.CAIR4_message_manager import append_message

# === 3️⃣ Haupt-Render-Funktion für den View ===
def render_reference_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    """
    🛠 Rendert den Arbeitszeugnis-View im CAIR4-Framework.

    🔹 **Parameter:**
    - `use_case`: Name des Anwendungsfalls.
    - `context`: Kontext für die KI (falls genutzt).
    - `title`: Titel des Views.
    - `description`: Beschreibung des Views.
    - `system_message`: Systemkonfiguration für das KI-Modell.
    - `session_file`: Pfad zur gespeicherten Session.
    - `model_name`: Name des verwendeten KI-Modells.
    - `settings`: Konfigurationsoptionen für die KI.
    - `collection`: Weitere Metadaten für die View.
    """

    # **Session-Handling**
    if "active_use_case" not in st.session_state or st.session_state["active_use_case"] != use_case:
        st.session_state["active_use_case"] = use_case
        st.session_state["current_session"] = {"messages": [], "calculations": []}
        DebugUtils.debug_print(f"Neue Session für {use_case} erstellt.")

    # Hauptansicht
    st.subheader(title)
    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)
        
    # **Formularfelder für die Eingabe**
    name = st.text_input("Name des Mitarbeiters")
    position = st.text_input("Position des Mitarbeiters")
    eintrittsdatum = st.date_input("Eintrittsdatum")
    austrittsdatum = st.date_input("Austrittsdatum")
    leistungsbewertung = st.selectbox("Leistungsbewertung", ["Sehr gut", "Gut", "Befriedigend", "Ausreichend", "Mangelhaft"])
    soziale_kompetenzen = st.text_area("Soziale Kompetenzen (optional)")
    arbeitsweise = st.multiselect("Arbeitsweise", ["Strukturiert", "Innovativ", "Teamorientiert", "Selbstständig"])
    besondere_erfolge = st.text_area("Besondere Erfolge (optional)")
    zeugnissprache = st.selectbox("Zeugnissprache", ["Standard", "Individuell"])
    
    if st.button("Zeugnis erstellen"):
        # Zusammenführen der Eingabedaten für die KI
        input_data = {
            "name": name,
            "position": position,
            "eintrittsdatum": eintrittsdatum.isoformat(),
            "austrittsdatum": austrittsdatum.isoformat(),
            "leistungsbewertung": leistungsbewertung,
            "soziale_kompetenzen": soziale_kompetenzen,
            "arbeitsweise": arbeitsweise,
            "besondere_erfolge": besondere_erfolge,
            "zeugnissprache": zeugnissprache
        }
        
        DebugUtils.debug_print(f"Eingabedaten: {input_data}")

        # Abfrage an die KI senden
        try:
            with st.spinner("Zeugnis wird generiert..."):
                query = f"Erstelle ein Arbeitszeugnis für {name} mit den folgenden Daten: {input_data}"
                response, tokens_used, costs, references = handle_query(
                    query=query,
                    use_case=use_case,
                    context=context,
                    model_name=model_name,
                )
                st.markdown(response)
                
                # Zeugnis in der Session speichern
                zeugnis_data = {
                    "input_data": input_data,
                    "zeugnis_text": response,
                    "timestamp": datetime.datetime.now().isoformat(),
                }
                st.session_state["current_session"]["calculations"].append(zeugnis_data)
                DebugUtils.debug_print("Zeugnis gespeichert")

                # **Session speichern**
                save_sessions(session_file, st.session_state["current_session"])
                DebugUtils.debug_print("Session gespeichert")

        except Exception as e:
            st.error(f"Fehler: {e}")
            DebugUtils.debug_print(e)


    # Anzeige der gespeicherten Zeugnisse
    if st.session_state["current_session"]["calculations"]:
        st.subheader("Gespeicherte Zeugnisse")
        for i, zeugnis in enumerate(st.session_state["current_session"]["calculations"]):
            st.write(f"Zeugnis {i+1} (erstellt am {zeugnis['timestamp']})")
            st.write(zeugnis["zeugnis_text"])

    

# === 4️⃣ Styling für Streamlit ===
st.markdown("""
<style> 
[data-testid="stBottomBlockContainer"] {
background-color: #ccc !important;
background:transparent!important;
}
</style>
""", unsafe_allow_html=True)