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
    
    **Wat wordt berekend?**
    - De totale **Brand Lift** (op basis van media-allocatie en instellingen).
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



