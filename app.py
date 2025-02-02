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
    "attention": 0.6,
    "reach": 0
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Functie om Reach te berekenen op basis van budget en CPM
def bereken_reach():
    total_active_channels = sum(1 for active in st.session_state["selected_channels"].values() if active)
    if total_active_channels > 0:
        reach_per_channel = {}
        for channel, is_active in st.session_state["selected_channels"].items():
            if is_active:
                budget_for_channel = (st.session_state["media_alloc"].get(channel, 0) / 100) * st.session_state["budget"]
                reach_per_channel[channel] = (budget_for_channel / st.session_state["cpm"]) * 1000  # CPM is per 1000 impressies
        st.session_state["reach"] = sum(reach_per_channel.values())
    else:
        st.session_state["reach"] = 0

# Functie om Brand Lift te berekenen
def bereken_brand_lift():
    bereken_reach()
    base_lift = (st.session_state["reach"] / 1_000_000) * 0.4
    frequency_factor = st.session_state["frequency_cap"] * 0.3
    attention_factor = st.session_state["attention"] * 0.6
    creative_factor = st.session_state["creative_effectiveness"] * 0.4
    context_factor = st.session_state["context_fit"] * 0.3
    
    total_lift = base_lift + frequency_factor + attention_factor + creative_factor + context_factor
    st.session_state["total_brand_lift"] = total_lift

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
    - **Geschatte reach**: (50.000 / 10) * 1000 = **5.000.000 impressies**  
    - **Brand Lift-berekening**:
        - (0.4 × 5) → Bereikfactor (0.4 weegt Reach, 5M impressies omgerekend naar schaal)
        - (0.3 × 5) → Frequentiefactor (0.3 weegt Frequency Cap van 5 vertoningen per gebruiker)
        - (0.6 × 0.8) → Attention Score-factor (0.6 weegt hoe goed de advertentie wordt bekeken, 0.8 is de attention score)
        - (0.4 × 0.7) → Creatieve kwaliteit (0.4 weegt de effectiviteit van de advertentie zelf, 0.7 is de kwaliteitsscore)
        - (0.3 × 0.6) → Contextuele fit (0.3 weegt hoe goed de advertentie bij de omgeving past, 0.6 is de context fit score)
    - **Totaal**: 2.0 + 1.5 + 0.48 + 0.28 + 0.18 = **3.55**
    
    Dit betekent dat de campagne naar verwachting een gemiddelde Brand Lift van **3.55** zal genereren.
    """)
    st.write("Gebruik de andere tabs om je eigen campagne te simuleren!")

st.write("\n**Eerste versie van het model. Toekomstige iteraties zullen validatie en optimalisatie bevatten.**")
