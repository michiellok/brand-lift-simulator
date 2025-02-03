import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Titel
st.title("📊 Campagne Optimalisatie Adviseur")

# Invoerparameters van de gebruiker
st.sidebar.header("📌 Campagne-instellingen")

# Stap 1: Kies het campagnedoel
st.sidebar.subheader("Stap 1: Kies het campagnedoel")
campagne_doel = st.sidebar.selectbox("Wat is het primaire doel van je campagne?", [
    "Merkbekendheid verhogen",
    "Overweging stimuleren",
    "Voorkeur opbouwen",
    "Koopintentie versterken"
])

# Stap 2: Selecteer de kanalen
st.sidebar.subheader("Stap 2: Selecteer kanalen")
channels = ["CTV", "Video", "Display", "DOOH", "Social"]
geselecteerde_kanalen = st.sidebar.multiselect("Selecteer de advertentiekanalen", options=channels, default=channels)

# Stap 3: Looptijd en budget
st.sidebar.subheader("Stap 3: Looptijd en budget")
looptijd = st.sidebar.slider("Hoeveel weken loopt de campagne?", min_value=1, max_value=52, value=4)
budget = st.sidebar.number_input("💰 Wat is het totale budget (in €)?", min_value=1000, max_value=1000000, value=50000)

# Simulatie van een adviesmodel op basis van de input
np.random.seed(42)
data = {
    "Kanaal": np.random.choice(geselecteerde_kanalen, 100),
    "Effectiviteit": np.random.uniform(0.5, 1.0, 100),
    "Bereik": np.random.randint(100000, 5000000, 100),
    "Kosten per 1000 bereikte personen": np.random.uniform(2, 15, 100)
}
df = pd.DataFrame(data)
df["Geschatte Impact Score"] = df["Effectiviteit"] * (budget / df["Kosten per 1000 bereikte personen"])

def genereer_advies():
    advies = ""
    if campagne_doel == "Merkbekendheid verhogen":
        advies += "Focus op kanalen met een breed bereik zoals **CTV en DOOH**. Deze zorgen voor hoge zichtbaarheid."
    elif campagne_doel == "Overweging stimuleren":
        advies += "Gebruik **Video en Social** om interactie en engagement met de doelgroep te vergroten."
    elif campagne_doel == "Voorkeur opbouwen":
        advies += "Zorg voor een consistente boodschap via **Display en Video**, gecombineerd met herhaalde exposure."
    elif campagne_doel == "Koopintentie versterken":
        advies += "Optimaliseer targeting op basis van **retargeting en high-attention formats** zoals DOOH en Social."
    return advies

# Advies tonen
st.subheader("📢 Advies voor jouw campagne")
st.write(genereer_advies())

# Grafiek: Budgetverdeling per kanaal
st.subheader("💰 Budgetverdeling per kanaal")
budget_per_kanaal = df.groupby("Kanaal")["Geschatte Impact Score"].sum().reset_index()
fig = px.bar(budget_per_kanaal, x="Kanaal", y="Geschatte Impact Score", color="Kanaal", title="Aanbevolen budgetverdeling per kanaal")
st.plotly_chart(fig)

# Extra uitleg over de optimalisatie
st.subheader("🔍 Hoe is dit advies tot stand gekomen?")
st.write(
    "Het model kijkt naar de effectiviteit van elk kanaal in relatie tot je campagnedoel. "
    "Op basis van het budget en de looptijd wordt berekend welke kanalen de hoogste impact zullen hebben. "
    "De berekening houdt rekening met bereik, effectiviteit en geschatte kosten per 1000 vertoningen."
)

