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
if "ai_recommendations" not in st.session_state:
    st.session_state["ai_recommendations"] = {}
if "total_brand_lift" not in st.session_state:
    st.session_state["total_brand_lift"] = 0

# Dummy data voor validatie
def generate_dummy_data():
    return {
        "historische_brandlift": random.uniform(80, 120),  # Simulatie van historische Brand Lift
        "gemiddelde_attention_score": random.uniform(0.3, 0.8),  # Simulatie attentiescore per kanaal
        "benchmark_brandlift": 100  # Industrie benchmark
    }

st.session_state["dummy_data"] = generate_dummy_data()

# Berekening Brand Lift
if st.session_state["media_alloc"]:
    industry_norm = st.session_state["dummy_data"]["benchmark_brandlift"]  # Gebruik benchmark
    st.session_state["brand_lift_per_channel"] = {
        channel: round((st.session_state["media_alloc"][channel] / 1000) *
                       (st.session_state["frequency_cap"] / 10) *
                       st.session_state["creative_effectiveness"] *
                       st.session_state["context_fit"] *
                       (st.session_state["budget"] / 10000), 2)
        for channel in st.session_state["media_alloc"]
    }
    st.session_state["total_brand_lift"] = sum(st.session_state["brand_lift_per_channel"].values())
    st.session_state["brand_lift_index"] = round((st.session_state["total_brand_lift"] / industry_norm) * 100, 2)

# AI-gestuurde optimalisatie
if st.session_state["media_alloc"]:
    st.session_state["ai_recommendations"] = {
        channel: round(value * random.uniform(1.05, 1.2), 2) for channel, value in st.session_state["media_alloc"].items()
    }

# Tabs maken
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie", "📂 Export", "📈 Scenario's"])

# 2️⃣ Resultaten tab
with tab2:
    st.header("🚀 Resultaten en Analyse")
    st.metric(label="Totale Brand Lift", value=round(st.session_state["total_brand_lift"], 2))
    st.metric(label="📊 Brand Lift Index", value=f"{st.session_state["brand_lift_index"]} (100 = industrienorm)")
    
    # Analyse en aanbevelingen
    if st.session_state["brand_lift_index"] < 90:
        st.warning("⚠️ De Brand Lift is lager dan de industrienorm. Overweeg de volgende verbeteringen:")
        st.markdown("- **Verhoog de budgetallocatie** naar kanalen met een hogere effectiviteit.")
        st.markdown("- **Optimaliseer de frequency cap** om herhaalde blootstelling te maximaliseren.")
        st.markdown("- **Verbeter de creatieve effectiviteit** voor meer impact op merkherinnering.")
    elif st.session_state["brand_lift_index"] > 110:
        st.success("✅ De Brand Lift presteert boven de industrienorm! Overweeg de volgende stappen:")
        st.markdown("- **Analyseer welke kanalen het beste presteren** en schaal deze verder op.")
        st.markdown("- **Experimenteer met nieuwe allocaties** om de prestaties nog verder te verhogen.")
    else:
        st.info("ℹ️ De Brand Lift is in lijn met de industrienorm. Monitor de prestaties en test verdere optimalisaties.")
    
    # Grafiek toevoegen
    fig, ax = plt.subplots()
    ax.bar(st.session_state["brand_lift_per_channel"].keys(), st.session_state["brand_lift_per_channel"].values())
    ax.set_title("Brand Lift per Kanaal")
    st.pyplot(fig)

# 3️⃣ Optimalisatie tab
with tab3:
    st.header("🔍 AI-gestuurde Optimalisatie Advies")
    if st.session_state["ai_recommendations"]:
        st.json(st.session_state["ai_recommendations"])







