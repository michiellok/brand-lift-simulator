import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titel van de app
st.title("Brand Lift & Cross-Channel Optimization - Fase 1")
st.subheader("Simuleer en analyseer je media-allocatie voor maximale impact")

# Tabs maken
tab1, tab2, tab3 = st.tabs(["📊 Campagne-instellingen", "🚀 Resultaten en Analyse", "📖 Hoe werkt dit model?"])

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
    "attention": 0.6
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Berekening van Reach op basis van budget en CPM met decay factor
def bereken_reach():
    total_active_channels = sum(1 for active in st.session_state["selected_channels"].values() if active)
    if total_active_channels > 0:
        reach_per_channel = {}
        for channel, is_active in st.session_state["selected_channels"].items():
            if is_active:
                budget_for_channel = (st.session_state["media_alloc"].get(channel, 0) / 100) * st.session_state["budget"]
                reach_per_channel[channel] = (budget_for_channel / st.session_state["cpm"]) * 1000  # CPM is per 1000 impressies
        total_reach = sum(reach_per_channel.values())
        decay_factor = 1 - (st.session_state["campaign_duration"] / 100)  # Simpele decay factor
        st.session_state["reach"] = total_reach * max(decay_factor, 0.5)  # Zorg dat decay niet negatief wordt
    else:
        st.session_state["reach"] = 0

# Berekening van Brand Lift
def bereken_brand_lift():
    bereken_reach()
    base_lift = (st.session_state["reach"] / 1_000_000) * 0.4
    frequency_factor = st.session_state["frequency_cap"] * 0.3
    attention_factor = st.session_state["attention"] * 0.6
    creative_factor = st.session_state["creative_effectiveness"] * 0.4
    context_factor = st.session_state["context_fit"] * 0.3
    
    total_lift = base_lift + frequency_factor + attention_factor + creative_factor + context_factor
    st.session_state["total_brand_lift"] = total_lift

# 📊 Campagne-instellingen Tab
with tab1:
    st.header("📊 Campagne-instellingen")
    st.write("Hier stel je de kernparameters van je campagne in.")
    st.session_state["budget"] = st.number_input("Totaal Budget (in €)", min_value=100, max_value=1000000, value=st.session_state["budget"], step=100)
    st.session_state["campaign_duration"] = st.slider("Campagne Duur (dagen)", 1, 90, st.session_state["campaign_duration"])
    st.session_state["frequency_cap"] = st.slider("Frequency Cap (max. aantal vertoningen per gebruiker)", 1, 20, st.session_state["frequency_cap"])
    st.session_state["cpm"] = st.number_input("CPM (Kosten per 1000 impressies in €)", min_value=1, max_value=1000, value=st.session_state["cpm"], step=1)
    if st.button("Bereken Brand Lift"):
        bereken_brand_lift()

# 🚀 Resultaten en Analyse Tab
with tab2:
    st.header("🚀 Resultaten en Analyse")
    st.metric(label="Geschatte Reach", value=int(st.session_state["reach"]))
    st.metric(label="Totale Brand Lift", value=round(st.session_state["total_brand_lift"], 2))
    fig, ax = plt.subplots()
    ax.barh(["Brand Lift"], [st.session_state["total_brand_lift"]], color='skyblue')
    ax.set_xlabel("Brand Lift Score")
    ax.set_title("Brand Lift Overzicht")
    st.pyplot(fig)

# 📖 Hoe werkt dit model? Tab
with tab3:
    st.header("📖 Hoe werkt dit model?")
    st.write("Dit model voorspelt de Brand Lift van een campagne door middel van een aantal kernfactoren, waaronder:")
    st.markdown("""
    - **Budget**: Het totale bedrag dat aan de campagne wordt besteed.
    - **Campagne Duur**: Hoe lang de campagne loopt.
    - **CPM (Cost per Mille)**: Kosten per 1000 impressies.
    - **Frequency Cap**: Het maximum aantal keer dat een gebruiker een advertentie kan zien.
    - **Attention Score**: Hoeveel aandacht een advertentie gemiddeld krijgt.
    - **Creative Effectiveness & Context Fit**: De kwaliteit en relevantie van de advertentie in de context waarin deze wordt weergegeven.
    
    De Brand Lift wordt berekend met de volgende formule:
    ```
    Brand Lift = (0.4 × Reach / 1.000.000) + (0.3 × Frequency) + (0.6 × Attention) + (0.4 × Creative Quality) + (0.3 × Context Fit)
    ```
    """)
    st.subheader("🔍 Voorbeeldcampagne")
    st.write("Bij een budget van €50.000, een CPM van €10 en een frequentiecap van 5 zou de berekening als volgt gaan:")
    st.markdown("""
    - Geschatte reach: (50.000 / 10) * 1000 = 5.000.000 impressies
    - Brand Lift = (0.4 × 5) + (0.3 × 5) + (0.6 × 0.8) + (0.4 × 0.7) + (0.3 × 0.6) = 3.55
    
    Dit betekent dat de campagne naar verwachting een gemiddelde Brand Lift van 3.55 zal genereren.
    """)
    st.write("Gebruik de andere tabs om je eigen campagne te simuleren!")

st.write("\n**Eerste versie van het model. Toekomstige iteraties zullen validatie en optimalisatie bevatten.**")

