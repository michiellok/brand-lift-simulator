import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titel van de app
st.title("Brand Lift & Cross-Channel Optimization - Fase 1")
st.subheader("Simuleer en analyseer je media-allocatie voor maximale impact")

# Tabs maken
tab1, tab2, tab3 = st.tabs([" Campagne-instellingen", " Resultaten en Analyse", " Hoe werkt dit model?"])

# Initialiseer session state met standaardwaarden indien niet aanwezig
default_values = {
    "budget": 10000,
    "campaign_duration": 30,
    "frequency_cap": 10,
    "creative_effectiveness": 0.7,
    "context_fit": 0.5,
    "cpm": 10,
    "selected_channels": {"CTV": True, "Social": True, "Video": True, "Display": True, "DOOH": True},
    "media_alloc": {"CTV": 20, "Social": 20, "Video": 20, "Display": 20, "DOOH": 20},
    "brand_lift_per_channel": {},
    "total_brand_lift": 0,
    "attention": 0.6,
    "reach": 0
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Functies voor berekeningen
def bereken_reach(budget, cpm, alloc_percentage):
    if cpm == 0:  # Check for division by zero
        return 0
    return (budget * alloc_percentage / 100) / cpm

def bereken_brand_lift():
    total_brand_lift = 0
    for channel, active in st.session_state["selected_channels"].items():
        if active:
            reach = bereken_reach(st.session_state["budget"], st.session_state["cpm"], st.session_state["media_alloc"][channel])
            st.session_state["reach"] += reach # Total reach calculation
            brand_lift = (0.4 * (reach / 1000000)) + (0.3 * st.session_state["frequency_cap"]) + (0.6 * st.session_state["attention"]) + (0.4 * st.session_state["creative_effectiveness"]) + (0.3 * st.session_state["context_fit"])
            st.session_state["brand_lift_per_channel"][channel] = brand_lift
            total_brand_lift += brand_lift
    st.session_state["total_brand_lift"] = total_brand_lift

#  Campagne-instellingen Tab
with tab1:
    st.header(" Campagne-instellingen")
    st.write("Hier stel je de kernparameters van je campagne in.")
    st.session_state["budget"] = st.number_input("Totaal Budget (in €)", min_value=100, max_value=1000000, value=st.session_state["budget"], step=100)
    st.session_state["campaign_duration"] = st.slider("Campagne Duur (dagen)", min_value=1, max_value=365, value=st.session_state["campaign_duration"])
    st.session_state["frequency_cap"] = st.slider("Frequency Cap (max. aantal keer per persoon)", min_value=1, max_value=20, value=st.session_state["frequency_cap"])
    st.session_state["attention"] = st.slider("Attention Score (0-1)", min_value=0.0, max_value=1.0, value=st.session_state["attention"], step=0.1)
    st.session_state["creative_effectiveness"] = st.slider("Creatieve Effectiviteit (0-1)", min_value=0.0, max_value=1.0, value=st.session_state["creative_effectiveness"], step=0.1)
    st.session_state["context_fit"] = st.slider("Context Fit (0-1)", min_value=0.0, max_value=1.0, value=st.session_state["context_fit"], step=0.1)
    st.session_state["cpm"] = st.number_input("Gemiddelde CPM (€ per 1000 impressies)", min_value=1, value=st.session_state["cpm"], step=1)

    st.subheader("Selecteer Mediakanalen en Verdeel Budget")
    for channel in st.session_state["selected_channels"]:
        col1, col2 = st.columns(2)
        with col1:
            st.session_state["selected_channels"][channel] = st.checkbox(f"{channel}", st.session_state["selected_channels"][channel])
        with col2:
            st.session_state["media_alloc"][channel] = st.slider(f"Allocatie % voor {channel}", min_value=0, max_value=100, value=st.session_state["media_alloc"][channel], step=1)

    if st.button("Bereken Brand Lift"):
        bereken_brand_lift()

#  Resultaten en Analyse Tab
with tab2:
    st.header(" Resultaten en Analyse")
    st.write("Bekijk hier de berekende Brand Lift per kanaal en de totale Brand Lift.")

    if st.session_state["total_brand_lift"] > 0: # Only show results if calculation has been done
        st.metric(label="Totale Brand Lift", value=round(st.session_state["total_brand_lift"], 2), help="De som van de Brand Lift over alle geselecteerde kanalen.")
        st.metric(label="Geschatte Reach", value=int(st.session_state["reach"]), help="Het geschatte aantal unieke gebruikers dat je campagne bereikt.")
        st.write("Brand Lift per kanaal:")
        for channel, brand_lift in st.session_state["brand_lift_per_channel"].items():
            st.write(f"- {channel}: {round(brand_lift, 2)}")

        # Visualisatie
        channels = list(st.session_state["brand_lift_per_channel"].keys())
        brand_lifts = list(st.session_state["brand_lift_per_channel"].values())

        fig, ax = plt.subplots()
        ax.bar(channels, brand_lifts)
        ax.set_xlabel("Mediakanalen")
        ax.set_ylabel("Brand Lift")
        ax.set_title("Brand Lift per Kanaal")
        st.pyplot(fig)
    else:
        st.write("Druk op 'Bereken Brand Lift' om de resultaten te bekijken.")


#  Hoe werkt dit model? Tab
with tab3:
    st.header(" Hoe werkt dit model?")
    st.write("Dit model simuleert de Brand Lift van een marketingcampagne op basis van de ingevoerde parameters. Hieronder vind je een uitleg van de belangrijkste concepten en berekeningen:")

    st.subheader("Kernfactoren")
    st.write("- **Budget:** Het totale budget dat beschikbaar is voor de campagne.")
    st.write("- **Campagne Duur:** De duur van de campagne in dagen.")
    st.write("- **Frequency Cap:** Het maximale aantal keer dat een advertentie aan dezelfde persoon wordt getoond.")
    st.write("- **Attention Score:** Een score die aangeeft hoeveel aandacht de advertentie krijgt (0-1).")
    st.write("- **Creatieve Effectiviteit:** Een score die aangeeft hoe effectief de advertentie is (0-1).")
    st.write("- **Context Fit:** Een score die aangeeft hoe goed de advertentie bij de context past (0-1).")
    st.write("- **CPM:** Kosten per 1000 impressies.")
    st.write("- **Media Allocatie:** Percentage van het budget dat aan elk kanaal wordt toegewezen.")

    st.subheader("Berekeningen")
    st.write("1. **Reach per kanaal:** `Reach = (Budget * Allocatie %) / CPM`")
    st.write("2. **Brand Lift per kanaal:** `Brand Lift = (0.4 * (Reach / 1.000.000)) + (0.3 * Frequency Cap) + (0.6 * Attention Score) + (0.4 * Creatieve Effectiviteit) + (0.3 * Context Fit)`")
    st.write("3. **Totale Brand Lift:** De som van de Brand Lift over alle kanalen.")

    st.

