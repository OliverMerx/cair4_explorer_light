"""
=================================================
CAIR4 PDF Vector Search (CAIR4_pdf_vectorizer_view.py)
=================================================

Dieses Modul implementiert eine **lokale semantische Suche in PDFs** mithilfe von **FAISS** und **SentenceTransformers**.

💡 Besonderheiten:
-------------------------------------------------
🔹 **On-Demand-Indexierung**:
    - FAISS-Index und Metadaten werden **nur bei Bedarf erstellt** (wenn kein Cache existiert).
    - Speicherung in `CAIR4_data/cache`, um wiederholte Indexierung zu vermeiden.

🔹 **Chunking & Kontextfenster**:
    - Texte werden in überlappende Chunks zerlegt (`split_text()`), um granularere Treffer zu ermöglichen.
    - Suchergebnisse zeigen einen **kontextualen Ausschnitt** mit einstellbarem Fenster (`CONTEXT_WINDOW`) und maximaler Anzeige (`MAX_DISPLAY_LENGTH`).

🔹 **Query Expansion**:
    - Bei Begriffen wie `"KI-System"` wird automatisch eine semantische **Erweiterung der Suchanfrage** durchgeführt:
      `"KI-System"`, `"KI System"`, `"KISystem"` und `"KI"` + `"System"` werden gewichtet gemittelt.
    - Dies erhöht die Trefferquote bei zusammengesetzten Begriffen und Schreibvarianten.

🔹 **Treffergruppierung**:
    - Mehrere Treffer pro PDF werden gruppiert dargestellt, inkl. Kapitel und Seitenzahl.
    - Nur **ein PDF-Link pro Datei** – nicht pro Treffer.

🔹 **Öffnen im Viewer (Streamlit)**:
    - Öffnen der Treffer über URL-Parameter (`?view=PDF-Results&doc=...`) im CAIR4 PDF-Viewer.
    - 🔒 **Einschränkung:** Streamlit unterstützt **keine direkte Seitensteuerung** (`#page=3`) im iframe-Viewer.
    - Alternative Lösung: Anzeige als Link zur statischen Kopie (`/static/pdf_results/xyz.pdf`) – funktioniert in den meisten Browsern außer Safari inkonsistent.

📦 Externe Abhängigkeiten:
-------------------------------------------------
- `fitz` (PyMuPDF): PDF-Text-Extraktion
- `faiss`: Vektorsuche
- `sentence_transformers`: Embedding-Modell
- `streamlit`, `re`, `shutil`, `urllib`

🚀 Hauptfunktionen:
-------------------------------------------------
- `create_faiss_index()`: Erstellt Embeddings + FAISS-Index und speichert sie.
- `render_pdf_search_results(query)`: Führt die Suche aus und zeigt Ergebnisse gruppiert an.
- `render_pdf_vectorizer_view()`: Haupt-Entry-Point inkl. Indexierungskontrolle und Sucheingabe.

"""
# ============================================================
# 📄 CAIR4 Semantische PDF-Suche mit FAISS (komplett robust)
# ============================================================

import os
import pymupdf
import faiss
import numpy as np
import streamlit as st
import re
from pathlib import Path
from urllib.parse import quote
from collections import defaultdict
from sentence_transformers import SentenceTransformer

# === 🔧 Konfiguration ===
PDF_DIR = "assets/docs/use_cases"
CACHE_DIR = "CAIR4_data/cache"
INDEX_CACHE = f"{CACHE_DIR}/faiss_index.npy"
METADATA_CACHE = f"{CACHE_DIR}/faiss_meta.npy"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
CONTEXT_WINDOW = 250
MAX_DISPLAY_LENGTH = 400
TOP_K = 15

# === 🔍 Modell laden ===
@st.cache_resource(show_spinner="📦 Lade Sprachmodell...")
def load_model():
    return SentenceTransformer(MODEL_NAME)

# === 📚 Text in Chunks teilen ===
def split_text(text, chunk_size=500, overlap=100):
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = tokens[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

# === 🧠 FAISS-Index aufbauen ===
def create_faiss_index():
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    st.info("🔄 Indexierung läuft...")

    model = load_model()
    all_chunks, metadatas = [], []

    for pdf_path in Path(PDF_DIR).rglob("*.pdf"):
        try:
            doc = pymupdf.open(pdf_path)
            for page_num, page in enumerate(doc):
                text = page.get_text()
                if not text:
                    continue
                for chunk in split_text(text):
                    all_chunks.append(chunk)
                    metadatas.append({
                        "pdf": pdf_path.name,
                        "filepath": str(pdf_path),
                        "page": page_num + 1,
                        "chapter": pdf_path.parts[-2] if len(pdf_path.parts) > 1 else "root",
                        "text": chunk
                    })
        except Exception as e:
            st.warning(f"⚠️ Fehler bei {pdf_path.name}: {e}")

    # 🔗 Embeddings & FAISS speichern
    embeddings = model.encode(all_chunks, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    np.save(INDEX_CACHE, embeddings)
    np.save(METADATA_CACHE, metadatas)
    st.success("✅ Index erfolgreich erstellt.")

# === 🔍 PDF-Suche mit Query-Expansion ===
def render_pdf_search_results(query, top_k=TOP_K, min_score=0.0):
    if not os.path.exists(INDEX_CACHE) or not os.path.exists(METADATA_CACHE):
        create_faiss_index()

    try:
        model = load_model()
        embeddings = np.load(INDEX_CACHE)
        metadatas = np.load(METADATA_CACHE, allow_pickle=True)

        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        # 🧠 Query Expansion
        query_variants = [query]
        if "-" in query:
            parts = query.split("-")
            query_variants += parts + [" ".join(parts), "".join(parts)]
        query_variants += [query.lower(), query.upper()]

        query_embeddings = model.encode(query_variants)
        query_embedding = np.mean(query_embeddings, axis=0).reshape(1, -1)

        D, I = index.search(query_embedding, top_k)

        results = []
        seen_keys = set()

        for idx, score in zip(I[0], D[0]):
            if score > min_score:
                meta = metadatas[idx]
                chunk = meta.get("text", "")

                key = f"{meta['pdf']}_{meta['page']}_{chunk[:40]}"
                if key in seen_keys:
                    continue
                seen_keys.add(key)

                keyword_positions = [m.start() for m in re.finditer(re.escape(query), chunk, re.IGNORECASE)]
                if keyword_positions:
                    start = max(0, keyword_positions[0] - CONTEXT_WINDOW)
                    end = min(len(chunk), keyword_positions[-1] + len(query) + CONTEXT_WINDOW)
                    context = chunk[start:end]
                    if len(context) > MAX_DISPLAY_LENGTH:
                        context = context[:MAX_DISPLAY_LENGTH] + "..."
                    highlighted_context = re.sub(re.escape(query), f"<b>{query}</b>", context, flags=re.IGNORECASE)
                else:
                    highlighted_context = chunk[:MAX_DISPLAY_LENGTH] + "..."

                results.append({
                    "pdf": meta["pdf"],
                    "filepath": meta["filepath"],
                    "page": meta["page"],
                    "score": round(1 - score, 3),
                    "chapter": meta.get("chapter", "-"),
                    "context": highlighted_context
                })

        if not results:
            st.info("🚫 Keine Treffer gefunden.")
            return

        # 📂 Gruppierung nach PDF
        grouped = defaultdict(list)
        for r in results:
            grouped[r['pdf']].append(r)

        for pdf_name, entries in grouped.items():
            first_entry = entries[0]
            kapitel = first_entry.get("chapter", "-")
            doc_param = quote(first_entry["filepath"])
            view_url = f"?view=PDF-Results&doc={doc_param}"

            with st.expander(f"📄 {pdf_name} ({kapitel}) – {len(entries)} Treffer"):
                for r in sorted(entries, key=lambda x: x["page"]):
                    st.markdown(f"""
                    <div style='padding: 6px 0 10px;'>
                        <b>📍 Seite:</b> {r['page']}<br>
                        <b>🧠 Kontext:</b>
                        <div style='margin: 6px 0 10px; padding: 6px 12px; background-color: #f9f9f9; border-left: 4px solid #ccc; font-size: 0.9em;'>
                            ... {r['context']} ...
                        </div>
                    </div>
                    <hr style='margin: 10px 0;'>
                    """, unsafe_allow_html=True)

                st.markdown(f'<a href="{view_url}" target="_blank">📂 Öffnen im PDF-Viewer</a>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Fehler bei der PDF-Suche: {e}")

# === 📋 Haupt-Renderfunktion ===
def render_pdf_vectorizer_view():
    st.subheader("🔍 Lokale PDF-Suche mit FAISS")

    if st.button("🛠️ Index jetzt erstellen"):
        create_faiss_index()

    query = st.text_input("Was möchtest du wissen?")
    if query:
        render_pdf_search_results(query, 10,0.7)