import streamlit as st
import numpy as np
import pandas as pd

# Titel van de app
st.title("Brand Lift & Cross-Channel Optimization Dashboard")
st.subheader("Simuleer en optimaliseer jouw media-allocatie voor maximale impact")

# Initialiseer session state
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "📊 Invoer"
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

# Berekening Brand Lift
if st.session_state["media_alloc"]:
    st.session_state["brand_lift_per_channel"] = {
        channel: round((st.session_state["media_alloc"][channel] / 1000) *
                       (st.session_state["frequency_cap"] / 10) *
                       st.session_state["creative_effectiveness"] *
                       st.session_state["context_fit"], 2)
        for channel in st.session_state["media_alloc"]
    }

# Tabs maken
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie", "📂 Export", "📈 Scenario's"])

# 1️⃣ Invoer tab
with tab1:
    st.header("📊 Campagne-instellingen")
    st.session_state["budget"] = st.number_input("Totaal Budget (in €)", min_value=100, max_value=1000000, value=st.session_state["budget"], step=100)
    st.session_state["campaign_duration"] = st.slider("Campagne Duur (dagen)", 1, 90, st.session_state["campaign_duration"])
    
    st.header("📡 Kies Media Kanalen")
    st.session_state["selected_channels"] = st.multiselect("Selecteer kanalen", ["Display", "Video", "DOOH", "Social", "CTV"], default=st.session_state["selected_channels"])
    
    st.header("📡 Media Allocatie")
    allocation_type = st.radio("Kies allocatiemethode:", ["Percentage", "Budget (€)"])
    
    if allocation_type == "Percentage":
        media_alloc = {channel: st.slider(f"{channel} (%)", 0, 100, 20) for channel in st.session_state["selected_channels"]}
    else:
        media_alloc = {channel: st.number_input(f"{channel} Budget (€)", min_value=0, max_value=st.session_state["budget"], value=st.session_state["budget"]//5, step=100) for channel in st.session_state["selected_channels"]}
    
    st.session_state["media_alloc"] = media_alloc
    
    if st.button("Next →"):
        st.session_state["active_tab"] = "🚀 Resultaten"
        st.rerun()

# 2️⃣ Resultaten tab
with tab2:
    st.header("🚀 Resultaten en Analyse")
    if st.session_state["media_alloc"]:
        total_brand_lift = sum(st.session_state["brand_lift_per_channel"].values())
        st.metric(label="Totale Brand Lift", value=round(total_brand_lift, 2))
    else:
        st.warning("⚠️ Geen data beschikbaar. Vul eerst de invoervelden in.")

# 3️⃣ Optimalisatie tab
with tab3:
    st.header("🔍 Optimalisatie Advies")
    if st.session_state["media_alloc"]:
        optimal_alloc = {k: round(v * 1.1, 2) for k, v in st.session_state["media_alloc"].items()}
        st.json(optimal_alloc)
        df_comparison = pd.DataFrame({
            "Kanaal": list(st.session_state["media_alloc"].keys()),
            "Huidige Allocatie": list(st.session_state["media_alloc"].values()),
            "Geoptimaliseerde Allocatie": list(optimal_alloc.values())
        })
        st.bar_chart(df_comparison.set_index("Kanaal"))
    else:
        st.warning("⚠️ Geen media-allocatie beschikbaar. Ga naar 'Invoer' en stel een budget in.")


