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
if "brand_lift_index" not in st.session_state:
    st.session_state["brand_lift_index"] = 100

# Berekening Brand Lift
if st.session_state["media_alloc"]:
    industry_norm = 100  # De gemiddelde industrienorm voor Brand Lift
    st.session_state["brand_lift_per_channel"] = {
        channel: round((st.session_state["media_alloc"][channel] / 1000) *
                       (st.session_state["frequency_cap"] / 10) *
                       st.session_state["creative_effectiveness"] *
                       st.session_state["context_fit"] *
                       (st.session_state["budget"] / 10000), 2)
        for channel in st.session_state["media_alloc"]
    }
    total_brand_lift = sum(st.session_state["brand_lift_per_channel"].values())
    st.session_state["brand_lift_index"] = round((total_brand_lift / industry_norm) * 100, 2)

# Tabs maken
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie", "📂 Export", "📈 Scenario's"])

# 5️⃣ Scenario-analyse tab
with tab5:
    st.header("📈 Scenario Analyse")
    if st.session_state["media_alloc"]:
        scenario_budget = st.slider("Extra Budget (% verhoging)", 0, 100, 10)
        scenario_alloc = {k: round(v * (1 + scenario_budget / 100), 2) for k, v in st.session_state["media_alloc"].items()}
        st.json(scenario_alloc)
        df_scenario = pd.DataFrame({
            "Kanaal": list(st.session_state["media_alloc"].keys()),
            "Huidige Allocatie": list(st.session_state["media_alloc"].values()),
            "Scenario Allocatie": list(scenario_alloc.values())
        })
        st.bar_chart(df_scenario.set_index("Kanaal"))
    else:
        st.warning("⚠️ Geen media-allocatie beschikbaar. Ga naar 'Invoer' en stel een budget in.")


