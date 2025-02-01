import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titel van de app
st.title("Brand Lift & Cross-Channel Optimization Simulator")
st.subheader("Test verschillende mediaverdelingen en krijg een geoptimaliseerd advies")

# Inputvelden voor scenario
st.sidebar.header("Campagne-instellingen")

# Budget en media-allocatie sliders
budget = st.sidebar.slider("📊 Totaal Budget (in miljoen €)", 1, 50, 10)
media_alloc = {
    "Display": st.sidebar.slider("Display (%)", 0, 100, 25),
    "Video": st.sidebar.slider("Video (%)", 0, 100, 25),
    "DOOH": st.sidebar.slider("DOOH (%)", 0, 100, 25),
    "Social": st.sidebar.slider("Social (%)", 0, 100, 25),
}

total_alloc = sum(media_alloc.values())
if total_alloc != 100:
    st.sidebar.error("⚠️ De media-allocatie moet samen 100% zijn!")

# Media kenmerken
media_characteristics = {
    "Display": {"attention": 0.6, "frequency": 3, "context_fit": 0.5},
    "Video": {"attention": 0.8, "frequency": 5, "context_fit": 0.7},
    "DOOH": {"attention": 0.7, "frequency": 2, "context_fit": 0.6},
    "Social": {"attention": 0.75, "frequency": 4, "context_fit": 0.65},
}

decay_rates = {"Display": 0.20, "Video": 0.10, "DOOH": 0.05, "Social": 0.15}

# Berekening van Brand Lift per kanaal
brand_lift_per_channel = {}
for channel, alloc in media_alloc.items():
    reach = (alloc / 100) * budget  # Simpel model: Budget bepaalt reach
    frequency = media_characteristics[channel]["frequency"]
    attention = media_characteristics[channel]["attention"]
    context_fit = media_characteristics[channel]["context_fit"]
    
    brand_lift = (0.4 * reach) + (0.3 * frequency) + (0.6 * attention) + (0.3 * context_fit)
    brand_lift_per_channel[channel] = brand_lift

# Totale Brand Lift berekenen
total_brand_lift = sum(brand_lift_per_channel.values())
st.metric(label="🚀 Totale Brand Lift", value=round(total_brand_lift, 2))

# Weergeven van resultaten per kanaal
st.write("### 📈 Brand Lift per Mediatype")
df_lift = pd.DataFrame(list(brand_lift_per_channel.items()), columns=["Mediatype", "Brand Lift"])
st.bar_chart(df_lift.set_index("Mediatype"))

# Optimalisatie Advies
st.write("### 🔍 Geoptimaliseerde Media-Allocatie")
optimal_alloc = {"Display": 20, "Video": 40, "DOOH": 20, "Social": 20}  # Eenvoudige optimalisatie
st.write("🚀 Op basis van jouw budget adviseren we:")
st.json(optimal_alloc)

# Time Decay Simulatie
st.write("### ⏳ Time Decay Effect per Mediatype")
days = np.arange(0, 30, 1)
decay_values = {}
for channel, lift in brand_lift_per_channel.items():
    decay_values[channel] = lift * np.exp(-decay_rates[channel] * days)

df_decay = pd.DataFrame(decay_values, index=days)
st.line_chart(df_decay)

st.write("### 🔹 Hoe werkt dit model?")
st.write("- Pas de waarden in de zijbalk aan om direct de impact op Brand Lift te zien.")
st.write("- Gebruik het geoptimaliseerde advies om je mediabudget beter te verdelen.")
st.write("- De Time Decay-grafiek toont hoe de impact afneemt over 30 dagen.")
