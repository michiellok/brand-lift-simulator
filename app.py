import streamlit as st import numpy as np import pandas as pd import random import matplotlib.pyplot as plt
Titel van de app
st.title("Brand Lift & Cross-Channel Optimization Dashboard") st.subheader("Simuleer en optimaliseer jouw media-allocatie voor maximale impact")
Initialiseer session state
if "active_tab" not in st.session_state: st.session_state["active_tab"] = "📖 Uitleg" if "media_alloc" not in st.session_state: st.session_state["media_alloc"] = {} if "budget" not in st.session_state: st.session_state["budget"] = 10000 if "campaign_duration" not in st.session_state: st.session_state["campaign_duration"] = 30 if "cpm" not in st.session_state: st.session_state["cpm"] = 10 if "frequency_cap" not in st.session_state: st.session_state["frequency_cap"] = 10 if "creative_effectiveness" not in st.session_state: st.session_state["creative_effectiveness"] = 0.7 if "context_fit" not in st.session_state: st.session_state["context_fit"] = 0.5 if "selected_channels" not in st.session_state: st.session_state["selected_channels"] = ["Display", "Video", "DOOH", "Social", "CTV"] if "brand_lift_per_channel" not in st.session_state: st.session_state["brand_lift_per_channel"] = {} if "brand_lift_index" not in st.session_state: st.session_state["brand_lift_index"] = 100 if "ai_recommendations" not in st.session_state: st.session_state["ai_recommendations"] = {} if "total_brand_lift" not in st.session_state: st.session_state["total_brand_lift"] = 0
Tabs maken met Streamlit tabs in plaats van sidebar navigatie
tabs = st.tabs(["📖 Uitleg", "📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie", "📂 Export", "📈 Scenario's"])
with tabs[3]: # Optimalisatie st.header("🔍 AI-gestuurde Optimalisatie Advies") if st.session_state["ai_recommendations"]: st.json(st.session_state["ai_recommendations"])
st.header("🔧 Handmatige Aanpassing")
st.markdown("Pas de media-allocatie handmatig aan op basis van AI-aanbevelingen.")
for channel in st.session_state["selected_channels"]:
    st.session_state["media_alloc"][channel] = st.number_input(f"{channel} Budget (handmatig aanpassen in €)", min_value=0, max_value=st.session_state["budget"], value=st.session_state["media_alloc"].get(channel, 0), step=100)

st.markdown("Nadat je de aanpassingen hebt gemaakt, bekijk je de resultaten in de resultaten-tab.")







