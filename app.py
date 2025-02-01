import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titel van de app
st.title("Brand Lift & Cross-Channel Optimization Dashboard")
st.subheader("Test verschillende mediaverdelingen en krijg een geoptimaliseerd advies")

# Initialiseer session state
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "📊 Invoer"
if "media_alloc" not in st.session_state:
    st.session_state["media_alloc"] = {}
if "budget" not in st.session_state:
    st.session_state["budget"] = 100
if "campaign_duration" not in st.session_state:
    st.session_state["campaign_duration"] = 7
if "cpm" not in st.session_state:
    st.session_state["cpm"] = 10
if "frequency_cap" not in st.session_state:
    st.session_state["frequency_cap"] = 10
if "creative_effectiveness" not in st.session_state:
    st.session_state["creative_effectiveness"] = 0.7

# Tabs maken
tabs = ["📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie"]
selected_tab = st.session_state["active_tab"]
tab1, tab2, tab3 = st.tabs(tabs)

# 1️⃣ Invoer tab
with tab1:
    st.header("📊 Campagne-instellingen")
    budget = st.number_input("Totaal Budget (in €)", min_value=0, max_value=1000000, value=st.session_state["budget"], step=100)
    campaign_start = st.date_input("📅 Startdatum Campagne")
    campaign_end = st.date_input("📅 Einddatum Campagne")
    campaign_duration = (campaign_end - campaign_start).days if campaign_end > campaign_start else 1
    
    st.session_state["budget"] = budget
    st.session_state["campaign_duration"] = campaign_duration
    
    st.header("🔧 Extra variabelen")
    cpm = st.slider("Cost per Mille (CPM in €)", 1, 50, st.session_state["cpm"])
    frequency_cap = st.slider("Frequency Cap (max. frequentie per gebruiker)", 1, 20, st.session_state["frequency_cap"])
    creative_effectiveness = st.slider("Creative Effectiveness Score (0-1)", 0.1, 1.0, st.session_state["creative_effectiveness"])
    kpi_goal = st.selectbox("KPI Focus", ["Awareness", "Consideration", "Preference", "Intent"])
    
    st.session_state["cpm"] = cpm
    st.session_state["frequency_cap"] = frequency_cap
    st.session_state["creative_effectiveness"] = creative_effectiveness
    
    st.header("📡 Media Allocatie")
    allocation_type = st.radio("Kies allocatiemethode:", ["Percentage", "Budget (€)"])
    
    if allocation_type == "Percentage":
        media_alloc = {
            "Display": st.slider("Display (%)", 0, 100, 20),
            "Video": st.slider("Video (%)", 0, 100, 20),
            "DOOH": st.slider("DOOH (%)", 0, 100, 20),
            "Social": st.slider("Social (%)", 0, 100, 20),
            "CTV": st.slider("CTV (%)", 0, 100, 20),
        }
        total_alloc = sum(media_alloc.values())
        if total_alloc > 0 and total_alloc != 100:
            scaling_factor = 100 / total_alloc
            media_alloc = {key: round(value * scaling_factor, 2) for key, value in media_alloc.items()}
    else:
        media_alloc = {
            "Display": st.number_input("Display Budget (€)", min_value=0, max_value=budget, value=budget//5, step=100),
            "Video": st.number_input("Video Budget (€)", min_value=0, max_value=budget, value=budget//5, step=100),
            "DOOH": st.number_input("DOOH Budget (€)", min_value=0, max_value=budget, value=budget//5, step=100),
            "Social": st.number_input("Social Budget (€)", min_value=0, max_value=budget, value=budget//5, step=100),
            "CTV": st.number_input("CTV Budget (€)", min_value=0, max_value=budget, value=budget//5, step=100),
        }
    
    st.session_state["media_alloc"] = media_alloc
    
    # Next button to navigate to results
    if st.button("Next →"):
        st.session_state["active_tab"] = "🚀 Resultaten"
        st.rerun()

# 2️⃣ Resultaten tab
with tab2:
    st.header("🚀 Berekening van Brand Lift per Kanaal")
    if "media_alloc" in st.session_state:
        media_characteristics = {
            "Display": {"attention": 0.6, "frequency": 3, "context_fit": 0.5},
            "Video": {"attention": 0.8, "frequency": 5, "context_fit": 0.7},
            "DOOH": {"attention": 0.7, "frequency": 2, "context_fit": 0.6},
            "Social": {"attention": 0.75, "frequency": 4, "context_fit": 0.65},
            "CTV": {"attention": 0.85, "frequency": 6, "context_fit": 0.8},
        }
        
        brand_lift_per_channel = {}
        for channel, alloc in st.session_state["media_alloc"].items():
            reach = (alloc / 100) * (st.session_state["budget"] / st.session_state["cpm"]) * min(st.session_state["campaign_duration"] / 30, 1)
            brand_lift_per_channel[channel] = reach * media_characteristics[channel]["attention"]
        
        st.bar_chart(pd.DataFrame(brand_lift_per_channel, index=["Brand Lift"]).T)

# 3️⃣ Optimalisatie tab
with tab3:
    st.header("🔍 Optimalisatie Advies")
    if "media_alloc" in st.session_state:
        optimal_alloc = {k: v + 5 for k, v in st.session_state["media_alloc"].items()}
        st.json(optimal_alloc)





