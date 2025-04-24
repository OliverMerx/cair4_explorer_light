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

from pylibs.streamlit_lib import streamlit as st

def render_legal_pills(legal_info):
    def is_empty(thing):
        return not thing or (isinstance(thing, dict) and not any(thing.values()))

    if all([
        is_empty(legal_info.get("description")),
        is_empty(legal_info.get("links")),
        is_empty(legal_info.get("aia")),
        is_empty(legal_info.get("gdpr"))
    ]):
        st.info("📭 Es wurden keine rechtlichen Verweise oder Normen zur Verfügung gestellt.")
        return

    colors = {
        "article_aia": st.session_state.header_color,
        "recital_aia": st.session_state.button_bg_color,
        "article_gdpr": st.session_state.header_color,
        "recital_gdpr": st.session_state.button_bg_color,
    }
    laws = {
        "aia": "EU AI ACT",
        "gdpr": "DSGVO",
    }

    def build_link(regime, kind, id, highlight=None):
        if regime == "aia":
            base = f"https://cair4.eu/eu-ai-act/artikel-{id}-eu-ai-act-aia" if kind == "articles" else f"https://cair4.eu/eu-ai-act-begruendung/begruendung-eu-ai-act-ziffer-{id}"
            return f"{base}?hilite={highlight}" if highlight else base
        elif regime == "gdpr":
            return f"https://dsgvo-gesetz.de/art-{id}-dsgvo" if kind == "articles" else f"https://dsgvo-gesetz.de/erwaegungsgruende/nr-{id}"
        return "#"

    if legal_info.get("description"):
        st.markdown(f"📘 *{legal_info['description']}*")

    if legal_info.get("links"):
        st.markdown("🔗 **Weiterführende Links:**")
        for link in legal_info["links"]:
            st.markdown(f"- [{link['title']}]({link['link']})")

    # === Nur noch gestylte Pills anzeigen ===
    with st.container():
        st.markdown("🧾 **Rechtliche Verweise (EU AI Act & DSGVO):**")
        for regime in ["aia", "gdpr"]:
            if regime not in legal_info:
                continue
            for kind in ["articles", "recitals"]:
                items = legal_info[regime].get(kind, {})
                for id, reason in items.items():
                    label_prefix = "Art." if kind == "articles" else "Begr."
                    label = f"{label_prefix} {id}"
                    link = build_link(regime, kind, id, reason if regime == "aia" else None)
                    color_key = f"{kind[:-1]}_{regime}"  # z. B. article_aia
                    color = colors.get(color_key, "#999999")
                    law = laws.get(regime, "")
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: left;">
                            <a href="{link}" target="_blank" style="text-decoration: none;">
                                <div style="
                                    background-color: {color};
                                    color: white;
                                    padding: 8px 16px;
                                    border-radius: 999px;
                                    margin: 6px 0;
                                    width: 160px;
                                    font-size:12px;
                                    text-align: center;
                                    font-weight: bold;
                                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                                ">
                                    {label} {law}
                                </div>
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )