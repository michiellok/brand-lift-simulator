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

# Tabs maken
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie", "📂 Export", "📈 Scenario's"])

# 3️⃣ Optimalisatie tab
with tab3:
    st.header("🔍 Optimalisatie Advies")
    optimal_alloc = {k: round(v * 1.1, 2) for k, v in st.session_state["media_alloc"].items()}
    st.json(optimal_alloc)
    df_comparison = pd.DataFrame({
        "Kanaal": list(st.session_state["media_alloc"].keys()),
        "Huidige Allocatie": list(st.session_state["media_alloc"].values()),
        "Geoptimaliseerde Allocatie": list(optimal_alloc.values())
    })
    st.bar_chart(df_comparison.set_index("Kanaal"))

# 4️⃣ Export tab
with tab4:
    st.header("📂 Download Resultaten")
    df_export = pd.DataFrame({
        "Kanaal": list(st.session_state["media_alloc"].keys()),
        "Huidige Allocatie": list(st.session_state["media_alloc"].values()),
        "Brand Lift": list(st.session_state["brand_lift_per_channel"].values()) if st.session_state["brand_lift_per_channel"] else [0] * len(st.session_state["media_alloc"])
    })
    csv = df_export.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download als CSV", data=csv, file_name="brand_lift_results.csv", mime='text/csv')

# 5️⃣ Scenario-analyse tab
with tab5:
    st.header("📈 Scenario Analyse")
    scenario_budget = st.slider("Extra Budget (% verhoging)", 0, 100, 10)
    scenario_alloc = {k: round(v * (1 + scenario_budget / 100), 2) for k, v in st.session_state["media_alloc"].items()}
    st.json(scenario_alloc)
    df_scenario = pd.DataFrame({
        "Kanaal": list(st.session_state["media_alloc"].keys()),
        "Huidige Allocatie": list(st.session_state["media_alloc"].values()),
        "Scenario Allocatie": list(scenario_alloc.values())
    })
    st.bar_chart(df_scenario.set_index("Kanaal"))












