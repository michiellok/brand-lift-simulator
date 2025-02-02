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

# Tabs maken
tab1, tab2, tab3, tab4 = st.tabs(["📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie", "📂 Export"])

# 1️⃣ Invoer tab
with tab1:
    st.header("📊 Campagne-instellingen")
    st.session_state["budget"] = st.number_input("Totaal Budget (in €)", min_value=100, max_value=1000000, value=st.session_state["budget"], step=100)
    st.session_state["campaign_duration"] = st.slider("Campagne Duur (dagen)", 1, 90, st.session_state["campaign_duration"])
    
    st.header("📡 Media Allocatie")
    allocation_type = st.radio("Kies allocatiemethode:", ["Percentage", "Budget (€)"])
    
    if allocation_type == "Percentage":
        media_alloc = {channel: st.slider(f"{channel} (%)", 0, 100, 20) for channel in ["Display", "Video", "DOOH", "Social", "CTV"]}
    else:
        media_alloc = {channel: st.number_input(f"{channel} Budget (€)", min_value=0, max_value=st.session_state["budget"], value=st.session_state["budget"]//5, step=100) for channel in ["Display", "Video", "DOOH", "Social", "CTV"]}
    
    st.session_state["media_alloc"] = media_alloc
    
    if st.button("Next →"):
        st.session_state["active_tab"] = "🚀 Resultaten"
        st.rerun()

# 2️⃣ Resultaten tab
    
    # Time Decay Berekening en Grafiek
    st.header("📉 Time Decay van Brand Lift")
    days = np.arange(1, st.session_state["campaign_duration"] + 1)
    decay_rates = {"Display": 0.1, "Video": 0.08, "DOOH": 0.06, "Social": 0.09, "CTV": 0.07}
    decay_values = {channel: [brand_lift_per_channel[channel] * np.exp(-decay_rates[channel] * d) for d in days] for channel in brand_lift_per_channel}
    df_decay = pd.DataFrame(decay_values, index=days)
    st.line_chart(df_decay)
with tab2:
    st.header("🚀 Berekening van Brand Lift per Kanaal")
    media_characteristics = {
        "Display": {"attention": 0.6, "frequency": 3},
        "Video": {"attention": 0.8, "frequency": 5},
        "DOOH": {"attention": 0.7, "frequency": 2},
        "Social": {"attention": 0.75, "frequency": 4},
        "CTV": {"attention": 0.85, "frequency": 6},
    }
    
    brand_lift_per_channel = {}
    for channel, alloc in st.session_state["media_alloc"].items():
        reach = (alloc / 100) * (st.session_state["budget"] / st.session_state["cpm"]) * min(st.session_state["campaign_duration"] / 30, 1)
        brand_lift = reach * media_characteristics[channel]["attention"] * st.session_state["creative_effectiveness"]
        # Simuleer verzadiging: effectiviteit neemt af bij hogere frequenties
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

# 4️⃣ Export tab
with tab4:
    st.header("📂 Download Resultaten")
    df_export = pd.DataFrame({"Kanaal": list(st.session_state["media_alloc"].keys()), "Huidige Allocatie": list(st.session_state["media_alloc"].values()), "Brand Lift": list(brand_lift_per_channel.values())})
    csv = df_export.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download als CSV", data=csv, file_name="brand_lift_results.csv", mime='text/csv')


