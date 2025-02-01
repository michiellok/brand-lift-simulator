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

# Tabs maken
selected_tab = st.session_state["active_tab"]
tab1, tab2, tab3 = st.tabs(["📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie"])

# 1️⃣ Invoer tab
if selected_tab == "📊 Invoer":
    with tab1:
        st.header("📊 Campagne-instellingen")
        budget = st.number_input("Totaal Budget (in €)", min_value=0, max_value=1000000, value=100, step=100)
        campaign_start = st.date_input("📅 Startdatum Campagne")
        campaign_end = st.date_input("📅 Einddatum Campagne")
        campaign_duration = (campaign_end - campaign_start).days if campaign_end > campaign_start else 1
        
        st.header("🔧 Extra variabelen")
        cpm = st.slider("Cost per Mille (CPM in €)", 1, 50, 10)
        frequency_cap = st.slider("Frequency Cap (max. frequentie per gebruiker)", 1, 20, 10)
        creative_effectiveness = st.slider("Creative Effectiveness Score (0-1)", 0.1, 1.0, 0.7)
        kpi_goal = st.selectbox("KPI Focus", ["Awareness", "Consideration", "Preference", "Intent"])
        
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
            total_budget_alloc = sum(media_alloc.values())
            if total_budget_alloc > budget:
                st.warning("⚠️ Het totaal toegewezen budget overschrijdt het campagnebudget!")
        
        # Next button to navigate to results
        if st.button("Next →"):
            st.session_state["active_tab"] = "🚀 Resultaten"
            st.rerun()

# 2️⃣ Resultaten tab
if selected_tab == "🚀 Resultaten":
    with tab2:
        st.header("🚀 Berekening van Brand Lift per Kanaal")
        media_characteristics = {
            "Display": {"attention": 0.6, "frequency": 3, "context_fit": 0.5},
            "Video": {"attention": 0.8, "frequency": 5, "context_fit": 0.7},
            "DOOH": {"attention": 0.7, "frequency": 2, "context_fit": 0.6},
            "Social": {"attention": 0.75, "frequency": 4, "context_fit": 0.65},
            "CTV": {"attention": 0.85, "frequency": 6, "context_fit": 0.8},
        }
        decay_rates = {"Display": 0.20, "Video": 0.10, "DOOH": 0.05, "Social": 0.15, "CTV": 0.08}
        
        brand_lift_per_channel = {}
        for channel, alloc in media_alloc.items():
            reach = (alloc / 100) * (budget / cpm) * min(campaign_duration / 30, 1)
            frequency = media_characteristics[channel]["frequency"]
            attention = media_characteristics[channel]["attention"]
            context_fit = media_characteristics[channel]["context_fit"]
            
            if frequency > frequency_cap:
                frequency *= 0.75  # Frequency Cap effect
            
            brand_lift = min((0.4 * reach) + (0.3 * frequency) + (0.6 * attention) + (0.3 * context_fit) + (0.4 * creative_effectiveness), 100)
            brand_lift_per_channel[channel] = brand_lift
        
        total_brand_lift = sum(brand_lift_per_channel.values())
        st.metric(label="🚀 Totale Brand Lift", value=round(total_brand_lift, 2))

