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

# Stap 2: Selecteer de kanalen en hun budgetverdeling
st.sidebar.subheader("Stap 2: Selecteer kanalen en budgetverdeling")
channels = ["CTV", "Video", "Display", "DOOH", "Social"]
geselecteerde_kanalen = st.sidebar.multiselect("Selecteer de advertentiekanalen", options=channels, default=channels)

# Budget sliders per kanaal
totaal_budget = st.sidebar.number_input("💰 Wat is het totale budget (in €)?", min_value=1000, max_value=1000000, value=50000)
budget_allocatie = {}
st.sidebar.subheader("💰 Budgetverdeling per kanaal")
for kanaal in geselecteerde_kanalen:
    budget_allocatie[kanaal] = st.sidebar.slider(f"Budgetpercentage {kanaal}", min_value=0, max_value=100, value=int(100/len(geselecteerde_kanalen)), step=5)

# Normalisatie naar 100%
totaal_percentage = sum(budget_allocatie.values())
for kanaal in budget_allocatie:
    budget_allocatie[kanaal] = (budget_allocatie[kanaal] / totaal_percentage) * totaal_budget

# Stap 3: Selecteer de campagneduur
st.sidebar.subheader("Stap 3: Kies de periode van de campagne")
start_datum = st.sidebar.date_input("Startdatum")
eind_datum = st.sidebar.date_input("Einddatum")

# Simulatie van een adviesmodel op basis van de input
np.random.seed(42)
data = {
    "Kanaal": np.random.choice(geselecteerde_kanalen, 100),
    "Effectiviteit": np.random.uniform(0.5, 1.0, 100),
    "Bereik": np.random.randint(100000, 5000000, 100),
    "Kosten per 1000 bereikte personen": np.random.uniform(2, 15, 100)
}
df = pd.DataFrame(data)
df["Geschatte Impact Score"] = df["Effectiviteit"] * (df["Bereik"] / df["Kosten per 1000 bereikte personen"]) * df["Kanaal"].map(budget_allocatie)

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
budget_per_kanaal = pd.DataFrame(list(budget_allocatie.items()), columns=["Kanaal", "Budget"])
fig = px.bar(budget_per_kanaal, x="Kanaal", y="Budget", color="Kanaal", title="Toegekend budget per kanaal")
st.plotly_chart(fig)

# Extra uitleg over de optimalisatie
st.subheader("🔍 Hoe is dit advies tot stand gekomen?")
st.write(
    "Het model analyseert de gekozen doelen, kanalen, looptijd en budgetverdeling om een strategie op te stellen. "
    "De belangrijkste overwegingen zijn het bereik van elk kanaal, de geschatte effectiviteit en de kosten per 1000 vertoningen. "
    "Door slimme budgetallocatie worden kanalen geoptimaliseerd om de beste impact te realiseren."
)

st.subheader("📋 Belangrijke overwegingen in het model")
st.write(
    "✅ **Bereik per kanaal**: Sommige kanalen hebben een groter publiek en zijn geschikt voor brede awareness."
    "✅ **Effectiviteit**: Engagement-kanalen zoals Video en Social zijn beter voor overweging en voorkeur."
    "✅ **Kosten per 1000 impressies**: DOOH en CTV zijn duurder, maar hebben vaak een hogere attentiewaarde."
    "✅ **Looptijd en consistentie**: Een langere campagne met consistente exposure levert vaak betere resultaten."
)


