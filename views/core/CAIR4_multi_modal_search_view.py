"""
===========================
🔍 CAIR4 Kombi-Suchansicht
===========================
Suchfunktion für Use Cases UND PDFs
Dynamisches Nachladen der PDF-Komponente (FAISS) erst bei Bedarf.

Verwendung:
from views.core.CAIR4_search_modal import render_search_modal
render_search_modal(COLLECTIONS)
===========================================
"""
from pylibs.streamlit_lib import streamlit as st  
from streamlit_extras.stylable_container import stylable_container
from collections import defaultdict
from pylibs.importlib_lib import importlib
import pandas as pd
from collections import defaultdict
import unicodedata

def extract_snippet(text, keyword, window=30):
    if not text:
        return ""
    keyword_lower = keyword.lower()
    idx = text.lower().find(keyword_lower)
    if idx == -1:
        return text[:window] + "..."
    start = max(0, idx - window)
    end = min(len(text), idx + len(keyword) + window)
    return "..." + text[start:end] + "..."

def render_use_case_results(query, collections):
    seen_titles = set()
    matches = {}

    for name, data in collections.items():
        if (
            query.lower() in name.lower()
            or query.lower() in data.get("title", "").lower()
            or query.lower() in data.get("description", "").lower()
            or query.lower() in data.get("tags", "").lower()
        ):
            matches[name] = data

    if matches:
        st.markdown("### 📋 Use Case Treffer")
        for name, data in matches.items():
            title = data.get("title", name)
            if title in seen_titles:
                continue
            seen_titles.add(title)
            chapter = data.get("chapter", "–")
            url = f"?view={name}"
            snippet = extract_snippet(data.get("description", ""), query)

            st.markdown(f"""
            <div style='padding:8px 0'>
                <b>Kapitel:</b> {chapter}<br>
                <b>Use Case:</b> <a href="{url}">{title}</a><br>
                <b>Treffer:</b> <i>{snippet}</i>
            </div>
            <hr style='margin:5px 0 10px 0;'>
            """, unsafe_allow_html=True)
    else:
        st.info("Keine passenden Use Cases gefunden.")

def render_use_cases_with_laws(collections):
    import unicodedata
    from collections import defaultdict

    def normalize_key(s):
        norm = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
        return norm.upper()

    # Schritt 1: Auswahl Gesetz + Kategorie
    law_options = {
        "EU AI Act (AIA)": "aia",
        "DSGVO (GDPR)": "gdpr"
    }
    law_display = st.selectbox("📘 Wähle Gesetz", list(law_options.keys()))
    law_key = law_options[law_display]

    category_display = st.radio("📂 Kategorie wählen", ["Artikel", "Erwägungsgründe"], horizontal=True)
    category_key = "articles" if category_display == "Artikel" else "recitals"

    # Schritt 2: Daten sammeln
    entry_map = defaultdict(list)  # z. B. {"2": [(name, title, "Innovation+Umwelt")]}

    for name, data in collections.items():
        title = data.get("title", name)
        section = data.get(law_key, {}).get(category_key, {})

        for art_num, reason in section.items():
            if not reason or reason.lower() == "none":
                continue
            entry_map[art_num].append((name, title, reason))

    if not entry_map:
        st.info("Keine Einträge für diese Auswahl gefunden.")
        return

    # Schritt 3: Alphabetfilter auf Grundlage von 'reason' (optional)
    # → oder direkt sortierte Artikelnummern (einfacher!)
    sorted_entries = sorted(entry_map.items(), key=lambda x: int(x[0]) if x[0].isdigit() else x[0])

    # Schritt 4: Anzeige
    col1, col2 = st.columns(2)
    split_index = len(sorted_entries) // 2 + len(sorted_entries) % 2

    for col, entries in zip([col1, col2], [sorted_entries[:split_index], sorted_entries[split_index:]]):
        with col:
            for art_num, use_cases in entries:
                reasons = {r for _, _, r in use_cases if r and r.lower() != "none"}
                reason_str = " / ".join(reasons)
                st.markdown(f"### <span style='color:#002060;'>🧾 {category_display} {art_num}</span>", unsafe_allow_html=True)
                if reason_str:
                    st.markdown(f"<i>{reason_str}</i>", unsafe_allow_html=True)
                for uc_name, uc_title, _ in use_cases:
                    st.markdown(f"- [{uc_title}](?view={uc_name})")

def render_link_results(query, collections):
    link_matches = []

    for name, data in collections.items():
        legal_links = (
            data.get("training_sections", {})
            .get("legal_info", {})
            .get("links", [])
        )
        for link_obj in legal_links:
            title = link_obj.get("title", "")
            url = link_obj.get("link", "")
            if isinstance(title, str) and query.lower() in title.lower():
                link_matches.append({
                    "source": name,
                    "title": title,
                    "url": url
                })

    if link_matches:
        st.markdown("### 🔗 Links zu Fachartikeln")
        for match in link_matches:
            use_case_title = collections.get(match["source"], {}).get("title", match["source"])
            url = f"?view={match['source']}"
            st.markdown(f"""
            <div style='padding:4px 0'>
                <b>Use Case:</b> <a href="{url}">{use_case_title}</a><br>
                <b>Link:</b> <a href="{match['url']}" target="_blank">{match['title']}</a>
            </div>
            <hr style='margin:4px 0 8px 0;'>
        """, unsafe_allow_html=True)
    else:
        st.info("Keine passenden Links gefunden.")

def render_tag_filter_view(collections):
    def get_first_letter(s):
        first_char = s.strip()[0] if s else ""
        norm = unicodedata.normalize('NFKD', first_char).encode('ASCII', 'ignore').decode('utf-8')
        return norm.upper()

    all_tags = defaultdict(list)

    for name, data in collections.items():
        tags = data.get("tags", "")
        for tag in tags.split(","):
            tag = tag.strip().lstrip("#'\"").rstrip("'\"").strip()
            if tag:
                normalized_tag = tag.lower()
                all_tags[normalized_tag].append((name, data))

    available_letters = sorted(set(get_first_letter(tag) for tag in all_tags if tag))
    selected_letter = st.selectbox("🔤 Tags nach Anfangsbuchstabe filtern", ["Alle"] + available_letters)

    filtered_tags = {
        tag: entries for tag, entries in sorted(all_tags.items())
        if selected_letter == "Alle" or get_first_letter(tag) == selected_letter
    }

    if not filtered_tags:
        st.info("Keine Tags gefunden für diese Auswahl.")
        return

    tag_items = list(filtered_tags.items())
    mid = len(tag_items) // 2 + len(tag_items) % 2
    col1, col2 = st.columns(2)

    for col, items in zip([col1, col2], [tag_items[:mid], tag_items[mid:]]):
        with col:
            for tag, entries in items:
                st.markdown(f"### <span style='color:#002060;'>#{tag}</span>", unsafe_allow_html=True)
                for name, data in entries:
                    title = data.get("title", name)
                    st.markdown(f"- [{title}](?view={name})")

def get_all_tags(collections):
    tags = set()
    for data in collections.values():
        for tag in data.get("tags", "").split(","):
            cleaned = tag.strip().lower()
            if cleaned:
                tags.add(cleaned)
    return sorted(tags)

def render_filtered_tags(collections, selected_tags):
    results = []
    for name, data in collections.items():
        tags = [t.strip().lower() for t in data.get("tags", "").split(",")]
        if any(tag in tags for tag in selected_tags):
            results.append((name, data.get("title", name)))

    if results:
        st.markdown("### 📌 Treffer zu Tags")
        for name, title in results:
            st.markdown(f"- [{title}](?view={name})")
    else:
        st.info("Keine Treffer zu den ausgewählten Tags.")

def render_search_modal(collections):

    # === Defaults ===
    st.session_state.setdefault("activate_pdf_search", False)

    # === Layout: Zweispaltig – linke Filter, rechte Ergebnisse ===
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown("### 🔎 Search & Filter")

        # 🔤 Suchfeld
        query = st.text_input("Suchbegriff", key="filter_query").strip()

        # 📂 Moduswahl
        mode = st.radio("Suchmodus", [
            "Alle", "Use Cases", "Fachartikel", "PDF", "📘 Normen (AIA/GDPR)", "📌 Tags"
        ])

        # 📘 Norm-Auswahl
        law_key, category_key = None, None
        if mode == "📘 Normen (AIA/GDPR)":
            law_choice = st.selectbox("Gesetz", ["AIA", "GDPR"])
            category_choice = st.radio("Typ", ["Artikel", "Erwägungsgründe"], horizontal=True)
            law_key = law_choice.lower()
            category_key = "articles" if category_choice == "Artikel" else "recitals"

        # 🏷️ Tag-Checkboxen
        selected_tags = []
        if mode in ["📌 Tags", "Alle"]:
            selected_tags = st.multiselect("Tags", get_all_tags(collections))

        # 📄 PDF-Aktivierung
        if mode == "PDF":
            st.checkbox("PDF-Suche aktivieren", key="activate_pdf_search")

    with col2:
        with stylable_container(
            key="search_result_container",
            css_styles="""
            {
                padding: 10px;
                border-radius: 15px;
                margin-bottom: -10px;
                border-style:solid;
                border-width:1px;
                border-color:#ccc!important;
                width: 100%;
                min-height:60vh!important;
                height:auto;
                max-height:55vh!important;
                overflow-y:auto;
            }
            """
        ):
            # === Suchlogik ===
            if mode == "Use Cases" and query:
                render_use_case_results(query, collections)

            elif mode == "Fachartikel" and query:
                render_link_results(query, collections)

            elif mode == "PDF" and query:
                if st.session_state.activate_pdf_search:
                    try:
                        pdf_module = importlib.import_module("utils.core.CAIR4_pdf_vectorize_manager")
                        pdf_module.render_pdf_search_results(query)
                    except Exception as e:
                        st.error(f"Fehler beim PDF-Suchmodul: {e}")
                else:
                    st.warning("Aktiviere zuerst die PDF-Suche.")

            elif mode == "📘 Normen (AIA/GDPR)":
                render_law_filtered_view(collections, law_key, category_key)

            elif mode == "📌 Tags" and selected_tags:
                render_filtered_tags(collections, selected_tags)

            elif mode == "Alle":
                any_result = False
                if query:
                    render_use_case_results(query, collections)
                    render_link_results(query, collections)
                    any_result = True
                if selected_tags:
                    render_filtered_tags(collections, selected_tags)
                    any_result = True
                if not any_result:
                    st.info("Bitte gib einen Suchbegriff ein oder wähle Tags.")

            else:
                st.info("Bitte wähle einen Suchmodus oder gib einen Suchbegriff ein.")