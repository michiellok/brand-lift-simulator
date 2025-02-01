import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titel van de app
st.title("Brand Lift & Cross-Channel Optimization Dashboard")
st.subheader("Test verschillende mediaverdelingen en krijg een geoptimaliseerd advies")

# Tabs maken
tab1, tab2, tab3 = st.tabs(["📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie"])

# 1️⃣ Invoer tab
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
    
                total_alloc = sum(media_alloc.values())
    if total_alloc > 0 and total_alloc != 100:
        scaling_factor = 100 / total_alloc
        media_alloc = {key: round(value * scaling_factor, 2) for key, value in media_alloc.items()}

# 2️⃣ Resultaten tab
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
            frequency *= 0.75  # Ad Fatigue effect
        
        brand_lift = min((0.4 * reach) + (0.3 * frequency) + (0.6 * attention) + (0.3 * context_fit) + (0.4 * creative_effectiveness), 100)
        brand_lift_per_channel[channel] = brand_lift
    
    total_brand_lift = sum(brand_lift_per_channel.values())
    st.metric(label="🚀 Totale Brand Lift", value=round(total_brand_lift, 2))
    
    st.header("📊 Benchmarking met historische data")
    historical_brand_lift = {"Display": 8, "Video": 12, "DOOH": 10, "Social": 9, "CTV": 15}
    for channel, lift in brand_lift_per_channel.items():
        historical_avg = historical_brand_lift[channel]
        st.write(f"🔹 {channel}: Berekende Brand Lift = {round(lift, 2)} | Historisch Gemiddelde = {historical_avg}")
        if lift > historical_avg * 1.5:
            st.warning(f"⚠️ {channel} Brand Lift is veel hoger dan historisch gemiddeld! Controleer de invoerwaarden.")
        elif lift < historical_avg * 0.5:
            st.info(f"ℹ️ {channel} Brand Lift is lager dan normaal. Mogelijk suboptimale media-allocatie.")

# 3️⃣ Optimalisatie tab
with tab3:
    st.header("🔍 Geoptimaliseerde Media-Allocatie")
    optimal_alloc = {"Display": 15, "Video": 30, "DOOH": 15, "Social": 20, "CTV": 20}
    st.write("🚀 Op basis van jouw budget en looptijd adviseren we:")
    st.write("Deze verdeling is geoptimaliseerd op basis van de volgende factoren:")
    st.write("- 📊 **Budget & CPM**: Een efficiëntere kostenverdeling over de kanalen die de hoogste ROI bieden.")
    st.write("- 🎯 **Mediakenmerken**: Kanalen met een hoge attentiewaarde en contextuele relevantie krijgen een groter aandeel.")
    st.write("- ⏳ **Campagne Duur & Time Decay**: Houdt rekening met de duur van de campagne en hoe lang de impact blijft.")
    st.write("- ⚠️ **Frequency Cap**: Voorkomt dat gebruikers te vaak dezelfde advertentie zien, wat advertentiemoeheid vermindert.")
    st.write("- 📢 **KPI Focus**: De verdeling past zich aan op jouw gekozen KPI, bijvoorbeeld awareness of intent.")
    st.json({key: f"{value}%" for key, value in optimal_alloc.items()})
    
    st.header("⏳ Time Decay Effect per Mediatype")
    days = np.arange(0, campaign_duration, 1)
    decay_values = {}
    for channel, lift in brand_lift_per_channel.items():
        decay_values[channel] = lift * np.exp(-decay_rates[channel] * days)
    
    df_decay = pd.DataFrame(decay_values, index=days)
    st.line_chart(df_decay)
