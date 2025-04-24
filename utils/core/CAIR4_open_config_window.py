"""
=================================================
CAIR4 Open Helpchat Window (CAIR4_open_helpchat_window.py)
=================================================

Dieses Modul verwaltet das modale Fenster für den Helpchat.
Es öffnet ein modales Fenster mit relevanten Fragen basierend auf dem aktuellen Use Case.

Funktionen:
- `open_helpchat_window()`: Erstellt das Helpchat-Modal-Fenster.
"""

# === 1️⃣  Import externer Bibliotheken ===
from pylibs.streamlit_lib import streamlit as st  
from views.core.CAIR4_modal_view import Modal  # Modal-Verwaltung

def open_helpchat_window():
    """
    Öffnet ein modales Helpchat-Fenster unten rechts mit spezifischen Fragen zum aktuellen Use Case.
    """

    # 🏗 **Session State für das Helpchat-Modal initialisieren**
    if "show_helpchat" not in st.session_state:
        st.session_state["show_helpchat"] = False  # Standard: Modal geschlossen

    # ✅ **Modal-Fenster erstellen**
    helpchat_modal = Modal(
        title="💬 KI Helpchat",
        key="helpchat_popup",
        position="bottom-right",  # **Fixierung unten rechts**
        overflow="scroll",
        max_width="80 px", 
        max_height="80 px"
    )

    # 📌 **Falls Modal offen → Inhalte anzeigen**
    if st.session_state["show_helpchat"]:
        helpchat_modal.open()
        with helpchat_modal.container():
            st.subheader("🤖 Fragen zu deinem aktuellen Use Case")

            # **Verfügbare Frage-Kategorien**
            question_categories = ["KI-System", "Ableitung", "KI-Modell", "Medical", "HR", "Finance"]
            selected_category = st.selectbox("📝 Thema wählen", question_categories)

            # **Vordefinierte Fragen**
            if selected_category == "KI-System":
                st.write("🤖 **Wie ist die Architektur dieses KI-Systems aufgebaut?**")
            elif selected_category == "Ableitung":
                st.write("🤖 **Welche Ableitungen wurden für diesen View getroffen?**")
            elif selected_category == "KI-Modell":
                st.write("🤖 **Welche Modellstrategie wird hier verwendet?**")
            elif selected_category == "Medical":
                st.write("🤖 **Gibt es regulatorische Anforderungen im medizinischen Bereich?**")
            elif selected_category == "HR":
                st.write("🤖 **Welche ethischen Überlegungen spielen hier eine Rolle?**")
            elif selected_category == "Finance":
                st.write("🤖 **Welche Compliance-Vorgaben müssen in der Finanzbranche beachtet werden?**")

            # 📩 **Eigene Frage eingeben**
            user_question = st.text_input("🔍 Eigene Frage eingeben")

            # 🚀 **Anfrage absenden**
            if st.button("🚀 Frage an KI senden"):
                st.success(f"📩 Frage gesendet: {user_question}")

    return helpchat_modal













