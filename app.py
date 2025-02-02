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
    
    # Benchmark gemiddelde Brand Lift
    avg_brand_lift = 100  # Normwaarde gebaseerd op industriestandaarden
    
    st.header("📊 Benchmarking: Brand Lift Index")
    brand_lift_index = round((sum(brand_lift_per_channel.values()) / avg_brand_lift) * 100, 2)
    st.metric(label="📈 Brand Lift Index", value=f"{brand_lift_index} (100 = industrienorm)")
    st.write("De Brand Lift Index vergelijkt de berekende uplift met een industriestandaard. Een waarde boven de 100 betekent dat de campagne beter presteert dan gemiddeld.")
with tab2:
    st.header("🚀 Berekening van Brand Lift per Kanaal")
    media_characteristics = {
        "Display": {"attention": 0.6, "frequency": 3, "context_fit": 0.5},
        "Video": {"attention": 0.8, "frequency": 5, "context_fit": 0.7},
        "DOOH": {"attention": 0.7, "frequency": 2, "context_fit": 0.6},
        "Social": {"attention": 0.75, "frequency": 4, "context_fit": 0.65},
        "CTV": {"attention": 0.85, "frequency": 6, "context_fit": 0.8},
    }
    
    brand_lift_per_channel = {}
    for channel, alloc in st.session_state["media_alloc"].items():
        reach = (alloc / 100) * (st.session_state["budget"] / st.session_state["cpm"]) * min(st.session_state["campaign_duration"] / 30, 1)
        brand_lift = reach * media_characteristics[channel]["attention"] * st.session_state["creative_effectiveness"] * media_characteristics[channel]["context_fit"]
        brand_lift *= (1 - np.exp(-media_characteristics[channel]["frequency"] / st.session_state["frequency_cap"]))
        brand_lift_per_channel[channel] = round(brand_lift, 2)
    
    st.metric(label="🚀 Totale Brand Lift", value=round(sum(brand_lift_per_channel.values()), 2))
    st.bar_chart(pd.DataFrame(brand_lift_per_channel, index=["Brand Lift"]).T)
    
# 3️⃣ Optimalisatie tab
with tab3:
    st.header("🔍 Optimalisatie Advies")
    optimal_alloc = {k: round(v * 1.1, 2) for k, v in st.session_state["media_alloc"].items()}
    st.json(optimal_alloc)
    df_comparison = pd.DataFrame({"Huidige Allocatie": st.session_state["media_alloc"], "Geoptimaliseerde Allocatie": optimal_alloc})
    st.bar_chart(df_comparison)

# 4️⃣ Scenario-analyse tab
with tab5:
    st.header("📈 Scenario Analyse")
    scenario_budget = st.slider("Extra Budget (% verhoging)", 0, 100, 10)
    scenario_alloc = {k: round(v * (1 + scenario_budget / 100), 2) for k, v in st.session_state["media_alloc"].items()}
    st.json(scenario_alloc)
    df_scenario = pd.DataFrame({"Huidige Allocatie": st.session_state["media_alloc"], "Scenario Allocatie": scenario_alloc})
    st.bar_chart(df_scenario)

# 5️⃣ Export tab
with tab4:
    st.header("📂 Download Resultaten")
    df_export = pd.DataFrame({"Kanaal": list(st.session_state["media_alloc"].keys()), "Huidige Allocatie": list(st.session_state["media_alloc"].values()), "Brand Lift": list(brand_lift_per_channel.values())})
    csv = df_export.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download als CSV", data=csv, file_name="brand_lift_results.csv", mime='text/csv')








