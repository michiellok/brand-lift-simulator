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

# Stap 2: Voer campagnedetails in
st.sidebar.subheader("Stap 2: Voer campagnedetails in")
totaal_budget = st.sidebar.number_input("💰 Wat is het totale budget (in €)?", min_value=1000, max_value=1000000, value=50000)
cpm = st.sidebar.number_input("📉 Gemiddelde CPM (kosten per 1000 impressies in €)", min_value=1.0, max_value=50.0, value=5.0, step=0.5)
start_datum = st.sidebar.date_input("📅 Startdatum")
eind_datum = st.sidebar.date_input("📅 Einddatum")
freq_cap = st.sidebar.slider("🔄 Max. frequentie per gebruiker", min_value=1, max_value=20, value=5, step=1)
time_decay_factor = st.sidebar.slider("⏳ Impact decay factor", min_value=0.01, max_value=1.0, value=0.5, step=0.01)

# Kanaaldata en optimalisatie
channels = ["CTV", "Video", "Display", "DOOH", "Social"]
kanaal_effectiviteit = {
    "Merkbekendheid verhogen": {"CTV": 0.9, "Video": 0.8, "Display": 0.7, "DOOH": 0.9, "Social": 0.6},
    "Overweging stimuleren": {"CTV": 0.6, "Video": 0.9, "Display": 0.7, "DOOH": 0.7, "Social": 0.8},
    "Voorkeur opbouwen": {"CTV": 0.5, "Video": 0.8, "Display": 0.9, "DOOH": 0.6, "Social": 0.7},
    "Koopintentie versterken": {"CTV": 0.4, "Video": 0.7, "Display": 0.8, "DOOH": 0.5, "Social": 0.9}
}

# Optimalisatie: automatische budgetverdeling
if st.sidebar.button("🔍 Bereken optimale mediaselectie"):
    optimalisatie_data = []
    for kanaal in channels:
        effectiviteit = kanaal_effectiviteit[campagne_doel][kanaal]
        bereik = (totaal_budget / cpm) * 1000  # Bereik berekenen
        impact = effectiviteit * bereik * np.exp(-time_decay_factor)  # Berekening van impact met decay
        optimalisatie_data.append([kanaal, effectiviteit, bereik, impact])
    
    optimalisatie_df = pd.DataFrame(optimalisatie_data, columns=["Kanaal", "Effectiviteit", "Bereik", "Impact"])
    optimalisatie_df = optimalisatie_df.sort_values(by="Impact", ascending=False)
    
    # Optimale verdeling bepalen
    totaal_impact = optimalisatie_df["Impact"].sum()
    optimalisatie_df["Budget Allocatie (€)"] = (optimalisatie_df["Impact"] / totaal_impact) * totaal_budget
    
    # Advies tonen
    st.subheader("📢 Aanbevolen Mediaselectie en Budgetverdeling")
    st.write("Op basis van het campagnedoel, budget en effectiviteit per kanaal is dit de optimale verdeling:")
    st.dataframe(optimalisatie_df[["Kanaal", "Budget Allocatie (€)", "Bereik", "Effectiviteit"]])
    
    # Grafiek: Optimale budgetallocatie
    fig = px.bar(optimalisatie_df, x="Kanaal", y="Budget Allocatie (€)", color="Kanaal", title="Optimale Budgetverdeling per Kanaal")
    st.plotly_chart(fig)
    
    # Scenario-analyse: impact over tijd
    st.subheader("⏳ Scenario-analyse: Impact verloop over tijd")
    impact_df = optimalisatie_df.copy()
    impact_df["Impact Over Tijd"] = impact_df["Impact"] * np.exp(-time_decay_factor * np.arange(len(impact_df)))
    fig2 = px.line(impact_df, x="Kanaal", y="Impact Over Tijd", title="Impact verloop per kanaal over tijd")
    st.plotly_chart(fig2)
    
    # Extra uitleg over de optimalisatie
    st.subheader("🔍 Hoe is dit advies tot stand gekomen?")
    st.write(
        "Deze verdeling is gebaseerd op de geschatte impact per kanaal, rekening houdend met budget, bereik, effectiviteit en een afname van impact over tijd."
    )
    
    # Uitleg over effectiviteit en impact decay factor
    st.subheader("📘 Wat betekenen Effectiviteit en Impact Decay Factor?")
    st.write(
        "**Effectiviteit:** Dit is een gewogen factor die aangeeft hoe goed een kanaal presteert voor het gekozen campagnedoel. "
        "Een hogere waarde betekent een groter effect op het campagnedoel. "
        "Deze waarden zijn gebaseerd op historische data en expertbeoordelingen."
    )
    st.write(
        "**Impact Decay Factor:** Dit modelleert hoe de impact van advertenties over tijd afneemt. "
        "Hogere waarden betekenen een snellere afname van effectiviteit (bijvoorbeeld bij campagnes met korte levensduur of hoge advertentie-verzadiging)."
    )
