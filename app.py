import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titel van de app
st.title("Brand Lift & Cross-Channel Optimization - Fase 1")
st.subheader("Simuleer en analyseer je media-allocatie voor maximale impact")

# Initialiseer session state met standaardwaarden indien niet aanwezig
default_values = {
    "budget": 10000,
    "campaign_duration": 30,
    "frequency_cap": 10,
    "creative_effectiveness": 0.7,
    "context_fit": 0.5,
    "reach": 1000000,
    "attention": 0.6,
    "cpm": 10,
    "selected_channels": {"CTV": True, "Social": True, "Video": True, "Display": True, "DOOH": True},
    "brand_lift_per_channel": {},
    "total_brand_lift": 0
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Berekening van Brand Lift
def bereken_brand_lift():
    base_lift = (st.session_state["reach"] / 1_000_000) * 0.4
    frequency_factor = st.session_state["frequency_cap"] * 0.3
    attention_factor = st.session_state["attention"] * 0.6
    creative_factor = st.session_state["creative_effectiveness"] * 0.4
    context_factor = st.session_state["context_fit"] * 0.3
    
    total_lift = base_lift + frequency_factor + attention_factor + creative_factor + context_factor
    st.session_state["total_brand_lift"] = total_lift

# Invoer Tab
st.header("📊 Campagne-instellingen")
st.session_state["budget"] = st.number_input("Totaal Budget (in €)", min_value=100, max_value=1000000, value=st.session_state["budget"], step=100)
st.session_state["campaign_duration"] = st.slider("Campagne Duur (dagen)", 1, 90, st.session_state["campaign_duration"])
st.session_state["frequency_cap"] = st.slider("Frequency Cap (max. aantal vertoningen per gebruiker)", 1, 20, st.session_state["frequency_cap"])
st.session_state["cpm"] = st.number_input("CPM (Kosten per 1000 impressies in €)", min_value=1, max_value=1000, value=st.session_state["cpm"], step=1)
st.session_state["reach"] = st.number_input("Geschatte Reach", min_value=1000, max_value=100000000, value=st.session_state["reach"], step=1000)
st.session_state["attention"] = st.slider("Attention Score (0 - 1)", 0.0, 1.0, st.session_state["attention"], step=0.01)
st.session_state["creative_effectiveness"] = st.slider("Creative Effectiveness (0 - 1)", 0.0, 1.0, st.session_state["creative_effectiveness"], step=0.01)
st.session_state["context_fit"] = st.slider("Context Fit (0 - 1)", 0.0, 1.0, st.session_state["context_fit"], step=0.01)

st.header("📡 Media Kanalen")
for channel in st.session_state["selected_channels"]:
    st.session_state["selected_channels"][channel] = st.checkbox(f"{channel}", st.session_state["selected_channels"][channel])

if st.button("Bereken Brand Lift"):
    bereken_brand_lift()

# Resultaten Weergave
st.header("🚀 Resultaten en Analyse")
st.metric(label="Totale Brand Lift", value=round(st.session_state["total_brand_lift"], 2))

fig, ax = plt.subplots()
ax.barh(["Brand Lift"], [st.session_state["total_brand_lift"]], color='skyblue')
ax.set_xlabel("Brand Lift Score")
ax.set_title("Brand Lift Overzicht")
st.pyplot(fig)

st.write("\n**Eerste versie van het model. Toekomstige iteraties zullen validatie en optimalisatie bevatten.**")

