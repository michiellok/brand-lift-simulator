import streamlit as st
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

# Titel van de app
st.title("Brand Lift & Cross-Channel Optimization Dashboard")
st.subheader("Simuleer en optimaliseer jouw media-allocatie voor maximale impact")

# Initialiseer session state
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "📖 Uitleg"
if "media_alloc" not in st.session_state:
    st.session_state["media_alloc"] = {}
if "budget" not in st.session_state:
    st.session_state["budget"] = 10000
if "campaign_duration" not in st.session_state:
    st.session_state["campaign_duration"] = 30
if "cpm" not in st.session_state:
    st.session_state["cpm"] = 10
if "frequency_cap" not in st.session_state:
    st.session_state["frequency_cap"] = 10
if "creative_effectiveness" not in st.session_state:
    st.session_state["creative_effectiveness"] = 0.7
if "context_fit" not in st.session_state:
    st.session_state["context_fit"] = 0.5
if "selected_channels" not in st.session_state:
    st.session_state["selected_channels"] = ["Display", "Video", "DOOH", "Social", "CTV"]
if "brand_lift_per_channel" not in st.session_state:
    st.session_state["brand_lift_per_channel"] = {}
if "brand_lift_index" not in st.session_state:
    st.session_state["brand_lift_index"] = 100
if "ai_recommendations" not in st.session_state:
    st.session_state["ai_recommendations"] = {}
if "total_brand_lift" not in st.session_state:
    st.session_state["total_brand_lift"] = 0

# Tabs maken, altijd zichtbaar
st.sidebar.title("Navigatie")
tab_selection = st.sidebar.radio("Ga naar", ["📖 Uitleg", "📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie", "📂 Export", "📈 Scenario's"])

# Uitleg tab
if tab_selection == "📖 Uitleg":
    st.header("📖 Uitleg van het Model")
    st.markdown("""
    Dit dashboard helpt bij het optimaliseren van Brand Lift door media-allocatie en budgetstrategieën te simuleren.
    
    **Hoe werkt dit model?**
    - Het voorspelt de **Brand Lift** op basis van:
      - **Reach**: Het aantal mensen dat bereikt wordt.
      - **Frequency**: Hoe vaak een advertentie wordt gezien.
      - **Attention**: De mate van aandacht voor een advertentie.
      - **Creative Effectiveness**: Hoe sterk de advertentie visueel en inhoudelijk is.
      - **Context Fit**: Hoe goed de advertentie past binnen de omgeving.
      - **Budget**: Hoeveel er wordt geïnvesteerd in de campagne.
      - **Campagne Looptijd**: De duur van de campagne beïnvloedt de impact.
    
    **Wat wordt berekend?**
    - De totale **Brand Lift** (op basis van media-allocatie, budget en instellingen).
    - Een **Brand Lift Index** (100 = industrienorm).
    - AI-gestuurde aanbevelingen voor optimalisatie.
    
    **Wat ontbreekt nog?**
    - Realtime integratie met DSP's.
    - Geavanceerde AI-modellen voor automatische optimalisatie.
    - Betere koppeling met historische merkmetingen.
    
    **Volgende stappen:**
    - Model valideren met echte data.
    - Meer granulariteit toevoegen per mediumtype.
    - Integratie met externe partners voor nauwkeurigere voorspellingen.
    """)

# Invoer tab
if tab_selection == "📊 Invoer":
    st.header("📊 Campagne-instellingen")
    st.session_state["budget"] = st.number_input("Totaal Budget (in €)", min_value=100, max_value=1000000, value=st.session_state["budget"], step=100)
    st.session_state["campaign_duration"] = st.slider("Campagne Duur (dagen)", 1, 90, st.session_state["campaign_duration"])
    st.session_state["frequency_cap"] = st.slider("Frequency Cap (max. aantal vertoningen per gebruiker)", 1, 20, st.session_state["frequency_cap"])
    
    st.header("📡 Kies Media Kanalen")
    st.session_state["selected_channels"] = st.multiselect("Selecteer kanalen", ["Display", "Video", "DOOH", "Social", "CTV"], default=st.session_state["selected_channels"])
    
    st.header("📡 Media Allocatie")
    media_alloc = {channel: st.slider(f"{channel} (%)", 0, 100, 20) for channel in st.session_state["selected_channels"]}
    st.session_state["media_alloc"] = media_alloc

# Resultaten tab
if tab_selection == "🚀 Resultaten":
    st.header("🚀 Resultaten en Analyse")
    # Berekening van de totale Brand Lift met budget en looptijd als invloed
    st.session_state["total_brand_lift"] = round(
        sum(st.session_state["media_alloc"].values()) *
        (st.session_state["budget"] / 10000) *
        (st.session_state["campaign_duration"] / 30) *
        (st.session_state["frequency_cap"] / 10) *
        st.session_state["creative_effectiveness"] *
        st.session_state["context_fit"], 2
    )
    st.metric(label="Totale Brand Lift", value=st.session_state["total_brand_lift"])
    st.metric(label="📊 Brand Lift Index", value=f"{st.session_state["brand_lift_index"]} (100 = industrienorm)")

    # Grafiek toevoegen
    fig, ax = plt.subplots()
    ax.bar(st.session_state["brand_lift_per_channel"].keys(), st.session_state["brand_lift_per_channel"].values())
    ax.set_title("Brand Lift per Kanaal")
    st.pyplot(fig)









