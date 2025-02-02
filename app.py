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

# Tabs maken met Streamlit tabs
tabs = st.tabs(["📖 Uitleg", "📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie", "📂 Export", "📈 Scenario's"])

# Berekening van Brand Lift
def bereken_brand_lift():
    base_lift = (st.session_state["budget"] / 10000) * 5  # Basis impact per 10k budget
    attention_factor = st.session_state["creative_effectiveness"] * 2
    frequency_factor = st.session_state["frequency_cap"] * 0.1
    lift_per_channel = {}
    
    for channel, alloc in st.session_state["media_alloc"].items():
        channel_lift = base_lift * (alloc / 100) * attention_factor * frequency_factor
        lift_per_channel[channel] = channel_lift
    
    st.session_state["brand_lift_per_channel"] = lift_per_channel
    st.session_state["total_brand_lift"] = sum(lift_per_channel.values())

# Invoer Tab
with tabs[1]:
    st.header("📊 Campagne-instellingen")
    st.session_state["budget"] = st.number_input("Totaal Budget (in €)", min_value=100, max_value=1000000, value=st.session_state["budget"], step=100)
    st.session_state["campaign_duration"] = st.slider("Campagne Duur (dagen)", 1, 90, st.session_state["campaign_duration"])
    st.session_state["frequency_cap"] = st.slider("Frequency Cap (max. aantal vertoningen per gebruiker)", 1, 20, st.session_state["frequency_cap"])
    
    st.header("📡 Kies Media Kanalen")
    st.session_state["selected_channels"] = st.multiselect("Selecteer kanalen", ["Display", "Video", "DOOH", "Social", "CTV"], default=st.session_state["selected_channels"])
    
    st.header("📡 Media Allocatie")
    media_alloc = {channel: st.slider(f"{channel} (%)", 0, 100, 20) for channel in st.session_state["selected_channels"]}
    st.session_state["media_alloc"] = media_alloc
    
    if st.button("Bereken Brand Lift"):
        bereken_brand_lift()

# Resultaten Tab
with tabs[2]:
    st.header("🚀 Resultaten en Analyse")
    if st.session_state["total_brand_lift"] == 0:
        st.write("Geen resultaten beschikbaar. Vul de campagne-instellingen in en genereer de Brand Lift.")
    else:
        st.metric(label="Totale Brand Lift", value=round(st.session_state["total_brand_lift"], 2))
        st.write("De Brand Lift wordt berekend op basis van de gekozen instellingen. Gebruik de optimalisatie-tab om betere resultaten te krijgen.")
        
        fig, ax = plt.subplots()
        channels = list(st.session_state["brand_lift_per_channel"].keys())
        lifts = list(st.session_state["brand_lift_per_channel"].values())
        ax.barh(channels, lifts, color='skyblue')
        ax.set_xlabel("Brand Lift Score")
        ax.set_title("Brand Lift per Kanaal")
        st.pyplot(fig)

# Optimalisatie Tab
with tabs[3]:
    st.header("🔍 AI-gestuurde Optimalisatie Advies")
    st.write("Op basis van de ingevoerde waarden wordt hier een aanbeveling weergegeven.")
    st.json(st.session_state["ai_recommendations"])
    
# Scenario Tab
with tabs[5]:
    st.header("📈 Scenario Analyse")
    st.write("Experimenteer met verschillende budgetten en frequenties om de optimale strategie te vinden.")

