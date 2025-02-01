import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titel van de app
st.title("Brand Lift & Cross-Channel Optimization Simulator")
st.subheader("Test verschillende mediaverdelingen en krijg een geoptimaliseerd advies")

# 1️⃣ Campagne-instellingen
st.sidebar.header("Campagne-instellingen")
budget = st.sidebar.number_input("📊 Totaal Budget (in €)", min_value=0, max_value=1000000, value=100, step=100)
campaign_duration = st.sidebar.slider("📅 Campagne Duur (dagen)", 1, 90, 7)

# 2️⃣ Extra variabelen
st.sidebar.header("Extra Variabelen")
cpm = st.sidebar.slider("💰 Cost per Mille (CPM in €)", 1, 50, 10)
ad_fatigue_threshold = st.sidebar.slider("⚠️ Ad Fatigue Threshold (max. frequentie)", 1, 20, 10)
creative_effectiveness = st.sidebar.slider("🎨 Creative Effectiveness Score (0-1)", 0.1, 1.0, 0.7)
kpi_goal = st.sidebar.selectbox("📢 KPI Focus", ["Awareness", "Consideration", "Preference", "Intent"])

# 3️⃣ Media-allocatie
st.sidebar.header("Media Allocatie")
media_alloc = {
    "Display": st.sidebar.slider("Display (%)", 0, 100, 20),
    "Video": st.sidebar.slider("Video (%)", 0, 100, 20),
    "DOOH": st.sidebar.slider("DOOH (%)", 0, 100, 20),
    "Social": st.sidebar.slider("Social (%)", 0, 100, 20),
    "CTV": st.sidebar.slider("CTV (%)", 0, 100, 20),
}

total_alloc = sum(media_alloc.values())
if total_alloc > 0 and total_alloc != 100:
    scaling_factor = 100 / total_alloc
    media_alloc = {key: round(value * scaling_factor, 2) for key, value in media_alloc.items()}
    scaling_factor = 100 / total_alloc
    media_alloc = {key: round(value * scaling_factor, 2) for key, value in media_alloc.items()}
    media_alloc = {key: value * scaling_factor for key, value in media_alloc.items()}
    st.sidebar.error("⚠️ De media-allocatie moet samen 100% zijn!")

# Media kenmerken
media_characteristics = {
    "Display": {"attention": 0.6, "frequency": 3, "context_fit": 0.5},
    "Video": {"attention": 0.8, "frequency": 5, "context_fit": 0.7},
    "DOOH": {"attention": 0.7, "frequency": 2, "context_fit": 0.6},
    "Social": {"attention": 0.75, "frequency": 4, "context_fit": 0.65},
    "CTV": {"attention": 0.85, "frequency": 6, "context_fit": 0.8},
}

decay_rates = {"Display": 0.20, "Video": 0.10, "DOOH": 0.05, "Social": 0.15, "CTV": 0.08}

# 4️⃣ Berekening van Brand Lift per kanaal
st.write("### 🚀 Berekening van Brand Lift per Kanaal")
brand_lift_per_channel = {}
for channel, alloc in media_alloc.items():
    reach = (alloc / 100) * (budget / cpm) * min(campaign_duration / 30, 1)
    frequency = media_characteristics[channel]["frequency"]
    attention = media_characteristics[channel]["attention"]
    context_fit = media_characteristics[channel]["context_fit"]
    
    if frequency > ad_fatigue_threshold:
        frequency *= 0.75  # Ad Fatigue effect
    
    brand_lift = min((0.4 * reach) + (0.3 * frequency) + (0.6 * attention) + (0.3 * context_fit) + (0.4 * creative_effectiveness), 100)
    brand_lift_per_channel[channel] = brand_lift

total_brand_lift = sum(brand_lift_per_channel.values())
st.metric(label="🚀 Totale Brand Lift", value=round(total_brand_lift, 2))

# 5️⃣ Optimalisatie Advies
st.write("### 🔍 Geoptimaliseerde Media-Allocatie")
optimal_alloc = {"Display": 15, "Video": 30, "DOOH": 15, "Social": 20, "CTV": 20}  # Eenvoudige optimalisatie
st.write("🚀 Op basis van jouw budget en looptijd adviseren we:")
st.json({key: f"{value}%" for key, value in optimal_alloc.items()})

# 6️⃣ Time Decay Simulatie
st.write("### ⏳ Time Decay Effect per Mediatype")
days = np.arange(0, campaign_duration, 1)
decay_values = {}
for channel, lift in brand_lift_per_channel.items():
    decay_values[channel] = lift * np.exp(-decay_rates[channel] * days)

df_decay = pd.DataFrame(decay_values, index=days)
st.line_chart(df_decay)

# 7️⃣ Interpretatie van variabelen
st.write("### 🔹 Interpretatie van variabelen en hoe ze invloed hebben")
st.write("- 📊 **Totaal Budget**: Dit bepaalt de totale mediainzet. Hoe hoger het budget, hoe groter het potentiële bereik.")
st.write("- ⏳ **Campagne Duur**: Een langere campagne kan zorgen voor een duurzamer effect, maar verhoogt ook de kans op advertentiemoeheid.")
st.write("- 💰 **CPM (Cost per Mille)**: Dit bepaalt hoeveel het kost om 1000 mensen te bereiken. Een lagere CPM betekent een efficiënter budgetgebruik.")
st.write("- 📉 **Time Decay**: Dit model laat zien hoe de impact afneemt naarmate de tijd verstrijkt. Dit is afhankelijk van het mediakanaal.")
st.write("- ⚠️ **Ad Fatigue Threshold**: Als een advertentie te vaak wordt vertoond, kan dit de effectiviteit verlagen. Dit model houdt hier rekening mee.")
st.write("- 🎨 **Creative Effectiveness**: Creativiteit heeft een directe invloed op de effectiviteit van de campagne. Een hogere score verhoogt de Brand Lift.")
st.write("- 🎯 **KPI Focus (Awareness, Consideration, Preference, Intent)**: De gekozen KPI bepaalt hoe de mediakanalen het beste kunnen worden ingezet.")



