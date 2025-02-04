import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Configuratie voor strak design
st.set_page_config(page_title="Campagne Optimalisatie", layout="wide")

st.markdown("""
    <style>
        .main {background-color: #f5f7fa;}
        .stButton>button {border-radius:10px; padding:10px; background:#005b96; color:white; font-size:16px;}
        .stSlider>div>div>div>div {background: #005b96;}
        .stSelectbox>div {border-radius:10px;}
    </style>
""", unsafe_allow_html=True)

# Titel
st.title("📊 Campagne Optimalisatie Adviseur")

# Brand Uplift per sector
brand_uplift_sector = {
    "FMCG": 8,
    "Automotive": 6,
    "Finance & Insurance": 7,
    "Tech & Electronics": 10,
    "Luxury & Fashion": 9,
    "Media & Entertainment": 5,
    "Healthcare & Pharma": 6,
    "Telecom": 7,
    "Travel & Hospitality": 8,
    "E-commerce & Marketplaces": 6
}

# Media impact op Brand Uplift
media_impact = {
    "CTV": 0.2,
    "Video": 0.15,
    "Display": 0.05,
    "DOOH": 0.10,
    "Social": 0.08
}

# Impact factoren en kosten per kanaal
impact_factors = {
    "CTV": 255,
    "TV": 309,
    "Video": 145,
    "Display": 138,
    "DOOH": 180,
    "Social": 72
}

cpm_costs = {
    "CTV": 30,
    "TV": 50,
    "Video": 12,
    "Display": 5,
    "DOOH": 20,
    "Social": 3
}

# Benchmarking data voor ROI en sector prestaties
roi_benchmark = {
    "FMCG": 2.5,
    "Automotive": 3.0,
    "Finance & Insurance": 2.8,
    "Tech & Electronics": 3.5,
    "Luxury & Fashion": 2.2,
    "Media & Entertainment": 1.8,
    "Healthcare & Pharma": 2.6,
    "Telecom": 3.1,
    "Travel & Hospitality": 2.9,
    "E-commerce & Marketplaces": 3.3
}

# Tabs voor structuur
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Basis Optimalisatie", "🛠 Scenario Analyse", "📈 ROI & Brand Uplift", "🔄 Budget Optimalisatie", "📊 Impact vs Kosten Analyse"])

if "optimalisatie_df" not in st.session_state:
    st.session_state["optimalisatie_df"] = None
if "totaal_budget" not in st.session_state:
    st.session_state["totaal_budget"] = 50000  # Standaard budget

with tab5:
    st.subheader("📊 Impact vs Kosten Analyse")
    if st.session_state["optimalisatie_df"] is not None:
        optimalisatie_df = st.session_state["optimalisatie_df"].copy()
        optimalisatie_df["Impact Score"] = optimalisatie_df["Kanaal"].map(impact_factors)
        optimalisatie_df["CPM Kosten (€)"] = optimalisatie_df["Kanaal"].map(cpm_costs)
        optimalisatie_df["Impact per Euro"] = optimalisatie_df["Impact Score"] / optimalisatie_df["CPM Kosten (€)"]
        
        st.dataframe(optimalisatie_df)
        
        fig = px.scatter(optimalisatie_df, x="CPM Kosten (€)", y="Impact Score", size="Impact per Euro", color="Kanaal", title="Impact vs Kosten per Kanaal")
        st.plotly_chart(fig)

        best_option = optimalisatie_df.loc[optimalisatie_df["Impact per Euro"].idxmax()]
        st.markdown(f"**🎯 Beste optie:** {best_option['Kanaal']} met een impact per euro van {best_option['Impact per Euro']:.2f}!")
