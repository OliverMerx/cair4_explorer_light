# ===============================================
# 🧠 CAIR4 Embedding Visualizer – Textkarte (PCA)
# ===============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from utils.core.CAIR4_debug_utils import DebugUtils

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def render_embedding_map_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
 
    # Hauptansicht
    st.subheader(title)
    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)
    
    user_input = st.text_area("Mehrere Zeilen, z. B. verschiedene Fachbegriffe oder Aussagen", height=200)

    if user_input or st.button("Textkarte erstellen"):
        sentences = [line.strip() for line in user_input.splitlines() if line.strip()]
        if len(sentences) < 2:
            st.warning("Bitte gib mindestens zwei verschiedene Begriffe oder Sätze ein.")
            return

        model = load_embedding_model()

        # === Embeddings erzeugen
        with st.spinner("🔢 Erzeuge Embeddings..."):
            embeddings = model.encode(sentences)

        # === PCA auf 2D reduzieren
        pca = PCA(n_components=2)
        points_2d = pca.fit_transform(embeddings)

        # === Visualisierung
        st.markdown("### 🗺️ Embedding-Visualisierung (PCA)")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(points_2d[:, 0], points_2d[:, 1], s=100, c="cornflowerblue")

        for i, sentence in enumerate(sentences):
            ax.text(points_2d[i, 0], points_2d[i, 1], sentence, fontsize=9, ha='right', va='bottom')

        ax.set_title("📌 Textkarte basierend auf semantischer Ähnlichkeit")
        ax.set_xlabel("PCA Komponente 1")
        ax.set_ylabel("PCA Komponente 2")
        ax.grid(True)
        st.pyplot(fig)

        # Debugging / Transparenz
        DebugUtils.debug_print(f"Embedding-Visualisierung für {len(sentences)} Einträge abgeschlossen.")