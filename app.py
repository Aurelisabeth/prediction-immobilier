import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Chargement du modèle
model = pickle.load(open("random_forest_model.pkl", "rb"))

st.set_page_config(page_title="Prédiction du prix de l'immobilier en Californie", page_icon="🏡")

# Titre
st.title("🏡 Prédiction du prix de l'immobilier en Californie")

st.markdown("""
Bienvenue dans cette application de prédiction immobilière 🏡

Cette app vous permet d'estimer le **prix médian d'un bien immobilier** en Californie 🇺🇸, à partir de données sociodémographiques locales.  
Entrez les caractéristiques du logement ➤ cliquez sur *Prédire le prix* ➤ obtenez une estimation instantanée 💬

""")

with st.expander("ℹ️ À propos du modèle"):
    st.markdown("""
    - Modèle utilisé : **Random Forest Regressor**
    - Données : `California Housing` dataset (`sklearn.datasets`)
    - Entraîné avec 4 variables explicatives :
        - Revenu médian
        - Nombre de pièces
        - Nombre de chambres
        - Catégorie d’âge du logement
    - R² = **0.60** | MAE ≈ **52 000 $**
    """)

# Sidebar pour les inputs utilisateur
st.sidebar.header("📋 Données du logement")

# Revenu médian
st.sidebar.markdown("**💰 Revenu médian (en dizaines de milliers de $)**")
st.sidebar.caption("Indiquez le revenu moyen des habitants du quartier (1.0 = 1 000 $).")
MedInc = st.sidebar.slider("Revenu médian", min_value=0.0, max_value=15.0, step=0.1)

# Nombre moyen de pièces
st.sidebar.markdown("**🛋️ Nombre moyen de pièces**")
st.sidebar.caption("Pièce principale (salon) + nombre de pièce(s) à vivre (chambre(s), bureau, salle de jeu, etc.).")
AveRooms = st.sidebar.slider("Nombre de pièces", min_value=1.0, max_value=15.0, step=1.0)

# Nombre moyen de chambres
st.sidebar.markdown("**🛏️ Nombre moyen de chambres**")
st.sidebar.caption("Nombre moyen de chambres par logement.")
AveBedrms = st.sidebar.slider("Nombre de chambres", min_value=0.0, max_value=5.0, step=1.0)


# Tranche d'âge de la maison
st.sidebar.markdown("**📊 Catégorie d’âge du logement**")
st.sidebar.caption("0 = Neuve (entre 0 et 5 ans)")
st.sidebar.caption("1 = Récente (entre 6 et 20 ans)")
st.sidebar.caption("2 = Vieille (entre 21 et 75 ans)")
st.sidebar.caption("3 = Très vieille.(plus de 76 ans)")
AgeGroup = st.sidebar.selectbox("Catégorie d'âge", options=[0, 1, 2, 3])

# Créer le DataFrame pour prédire
input_data = pd.DataFrame({
    'MedInc': [MedInc],
    'AveRooms': [AveRooms],
    'AveBedrms': [AveBedrms],
    'AgeGroup': [AgeGroup]
})

# Bouton de prédiction
if st.button("**Prédire le prix**"):
    prediction = model.predict(input_data)
    st.header("💬 Résultat")
    st.success(f"🏠 La valeur médiane du bien est estimé à : **${prediction[0]*100_000:,.0f}**")
