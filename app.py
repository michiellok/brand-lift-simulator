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

# Functie om Brand Lift te berekenen
def bereken_brand_lift():
    reach = (st.session_state["budget"] / st.session_state["cpm"]) * 1000
    frequency_factor = st.session_state["frequency_cap"] * 0.3
    attention_factor = st.session_state["attention"] * 0.6
    creative_factor = st.session_state["creative_effectiveness"] * 0.4
    context_factor = st.session_state["context_fit"] * 0.3
    
    total_lift = (0.4 * reach / 1_000_000) + frequency_factor + attention_factor + creative_factor + context_factor
    st.session_state["reach"] = reach
    st.session_state["total_brand_lift"] = total_lift

# 📊 Campagne-instellingen Tab
with tab1:
    st.header("📊 Campagne-instellingen")
    st.write("Hier stel je de kernparameters van je campagne in.")
    st.session_state["budget"] = st.number_input("Totaal Budget (in €)", min_value=100, max_value=1000000, value=st.session_state["budget"], step=100)
    st.session_state["campaign_duration"] = st.slider("Campagne Duur (dagen)", 1, 90, st.session_state["campaign_duration"])
    st.session_state["frequency_cap"] = st.slider("Frequency Cap (max. aantal vertoningen per gebruiker)", 1, 20, st.session_state["frequency_cap"])
    st.session_state["cpm"] = st.number_input("CPM (Kosten per 1000 impressies in €)", min_value=1, max_value=1000, value=st.session_state["cpm"], step=1)
    
    st.header("📡 Media Allocatie")
    for channel in st.session_state["selected_channels"]:
        if st.session_state["selected_channels"][channel]:
            st.session_state["media_alloc"][channel] = st.slider(f"{channel} Allocatie (%)", 0, 100, st.session_state["media_alloc"].get(channel, 20))
    
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

st.write("\n**Eerste versie van het model. Toekomstige iteraties zullen validatie en optimalisatie bevatten.**")

