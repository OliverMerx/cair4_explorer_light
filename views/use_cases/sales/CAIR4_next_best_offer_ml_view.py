"""
################
#
################
⸻

📊 Wann sind Trainingsdaten valide oder belastbar?

Das hängt von vielen Faktoren ab – aber hier eine einfache Faustregel für kleine ML-Demos:

Trainingsgröße	Eignung
unter 100	🟥 Nur für Debugging oder Prototypen
100–1000	🟧 OK für einfache Logiken, aber nicht stabil
1000–10.000	🟨 Akzeptabel für strukturierte Regeln oder einfache Klassifikation
10.000+	🟩 Kann belastbare Signale enthalten, v. a. bei gutem Feature-Engineering

⸻"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ==== Produktdatenbank erweitern ====
PRODUCT_DATABASE = [
    {"product": "Wanderstiefel", "category": "Outdoor", "season": "Sommer"},
    {"product": "Skihelm", "category": "Wintersport", "season": "Winter"},
    {"product": "Laufschuhe", "category": "Fitness", "season": "Frühling"},
    {"product": "Yogamatte", "category": "Fitness", "season": "Ganzjährig"},
    {"product": "Heizkissen", "category": "Wohnen", "season": "Winter"},
    {"product": "Grillzange", "category": "Outdoor", "season": "Sommer"},
    {"product": "Snowboard", "category": "Wintersport", "season": "Winter"},
    {"product": "Ventilator", "category": "Wohnen", "season": "Sommer"},
]

# ==== Zufällige Trainingsdaten generieren ====
def generate_training_data(n=100):
    data = []
    for _ in range(n):
        age = random.randint(18, 70)
        gender = random.choice(["Male", "Female"])
        season = random.choice(["Sommer", "Winter", "Frühling", "Ganzjährig"])
        category = random.choice(["Outdoor", "Fitness", "Wohnen", "Wintersport"])
        product = next((p["product"] for p in PRODUCT_DATABASE if p["category"] == category and (p["season"] == season or p["season"] == "Ganzjährig")), "")
        data.append({"age": age, "gender": gender, "season": season, "category": category, "product": product})
    return pd.DataFrame(data)

# ==== Training starten ====
def train_model(df):
    df = df[df["product"] != ""]
    le_gender = LabelEncoder()
    le_season = LabelEncoder()
    le_category = LabelEncoder()
    le_product = LabelEncoder()

    df["gender"] = le_gender.fit_transform(df["gender"])
    df["season"] = le_season.fit_transform(df["season"])
    df["category"] = le_category.fit_transform(df["category"])
    df["product"] = le_product.fit_transform(df["product"])

    X = df[["age", "gender", "season", "category"]]
    y = df["product"]

    model = RandomForestClassifier()
    with st.spinner("Modelltraining läuft..."):
        for i in range(0, 101, 10):
            time.sleep(0.1)
            st.progress(i)
        model.fit(X, y)

    return model, (le_gender, le_season, le_category, le_product), df

# ==== Vorhersage machen ====
def predict_offer(model, encoders, input_data):
    gender_enc, season_enc, category_enc, product_enc = encoders
    input_df = pd.DataFrame([input_data])
    input_df["gender"] = gender_enc.transform([input_data["gender"]])
    input_df["season"] = season_enc.transform([input_data["season"]])
    input_df["category"] = category_enc.transform([input_data["category"]])
    pred = model.predict(input_df[["age", "gender", "season", "category"]])[0]
    return product_enc.inverse_transform([pred])[0]

# ==== Streamlit UI ====
def render_nbo_ml_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)

    # 🔹 Expander für die gewählte Beschreibung
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    st.divider()

    with st.expander("1. Auszug von Trainingsdaten anzeigen"):
        training_data = generate_training_data(200)
        st.dataframe(training_data.head(20))

    with st.expander("2. Modell trainieren"):
        if st.button("Trainieren starten"):
            model, encoders, df = train_model(training_data)
            st.session_state["trained_model"] = model
            st.session_state["encoders"] = encoders
            st.success(f"Modell mit {len(df)} Trainingsdaten trainiert")

    st.divider()
    st.markdown("### Nutzerprofil wählen")

    age = st.slider("Alter", 18, 70, 30)
    gender = st.selectbox("Geschlecht", ["Male", "Female"])
    season = st.selectbox("Aktuelle Saison", ["Sommer", "Winter", "Frühling", "Ganzjährig"])
    category = st.selectbox("Interessen-Kategorie", ["Outdoor", "Fitness", "Wohnen", "Wintersport"])

    if st.button("Empfehlung anzeigen"):
        if "trained_model" not in st.session_state:
            st.warning("Bitte zuerst ein Modell trainieren!")
        else:
            input_data = {"age": age, "gender": gender, "season": season, "category": category}
            offer = predict_offer(st.session_state["trained_model"], st.session_state["encoders"], input_data)
            st.success(f"Empfohlene Produkt: **{offer}**")
