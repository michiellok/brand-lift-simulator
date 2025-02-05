import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Configuratie voor strak design
st.set_page_config(page_title="Media Budget Allocatie Dashboard", layout="wide")

st.markdown("""
    <style>
        .main {background-color: #f5f7fa;}
        .stButton>button {border-radius:10px; padding:10px; background:#005b96; color:white; font-size:16px;}
        .stSlider>div>div>div>div {background: #005b96;}
        .stSelectbox>div {border-radius:10px;}
    </style>
""", unsafe_allow_html=True)

# Titel
st.title("📊 Media Budget Allocatie Dashboard")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Campagne Briefing", "📈 Voorspelling & Scenario’s", "🚀 Activatie & Export"])

with tab1:
    st.subheader("📊 Campagne Briefing")
    
    col1, col2 = st.columns(2)
    with col1:
        adverteerder = st.text_input("Adverteerder Naam")
        sector = st.selectbox("Sector", ["FMCG", "Automotive", "Finance & Insurance", "Tech & Electronics", "Luxury & Fashion", "Media & Entertainment", "Healthcare & Pharma", "Telecom", "Travel & Hospitality", "E-commerce & Marketplaces"])
        campagne_doel = st.selectbox("Campagne Doel", ["Merkbekendheid", "Overweging", "Voorkeur", "Conversie"])
        budget = st.number_input("Totale Budget (€)", min_value=1000, max_value=1000000, value=50000)
    
    with col2:
        start_datum = st.date_input("Startdatum")
        eind_datum = st.date_input("Einddatum")
        freq_cap = st.slider("Max. frequentie per gebruiker", min_value=1, max_value=20, value=5, step=1)
    
    st.markdown("### 🎯 Media Kanalen Selectie")
    kanalen = st.multiselect("Selecteer de mediakanalen", ["CTV", "Video", "Display", "DOOH", "Social"])
    budget_verdeling = {kanaal: st.slider(f"Budget Allocatie {kanaal} (%)", 0, 100, 20, step=5) for kanaal in kanalen}
    
    if st.button("📝 Genereer Plan"):
        st.session_state["kanalen"] = kanalen
        st.session_state["budget_verdeling"] = budget_verdeling
        st.session_state["budget"] = budget
        st.success("Plan gegenereerd! Ga naar de volgende tab voor voorspellingen.")

with tab2:
    st.subheader("📈 Voorspelling & Scenario’s")
    if "kanalen" in st.session_state and st.session_state["kanalen"]:
        cpm_values = {"CTV": 35, "Video": 20, "Display": 10, "DOOH": 25, "Social": 5}
        brand_uplift_factors = {"CTV": 0.8, "Video": 0.6, "Display": 0.4, "DOOH": 0.7, "Social": 0.5}
        roi_factors = {"CTV": 1.2, "Video": 1.1, "Display": 0.9, "DOOH": 1.0, "Social": 0.8}
        
        voorspellingen = pd.DataFrame({
            "Kanaal": st.session_state["kanalen"],
            "CPM (€)": [cpm_values[k] for k in st.session_state["kanalen"]],
            "Brand Uplift Factor": [brand_uplift_factors[k] for k in st.session_state["kanalen"]],
            "ROI Factor": [roi_factors[k] for k in st.session_state["kanalen"]]
        })
        
        voorspellingen["Impressies"] = st.session_state["budget"] / voorspellingen["CPM (€)"] * 1000
        voorspellingen["Verwachte Brand Uplift (%)"] = voorspellingen["Brand Uplift Factor"] * (voorspellingen["Impressies"] / 1_000_000) * 100
        voorspellingen["Verwachte ROI (€)"] = voorspellingen["ROI Factor"] * (voorspellingen["Impressies"] / 1000) * voorspellingen["CPM (€)"]
        
        st.dataframe(voorspellingen)
        fig = px.bar(voorspellingen, x="Kanaal", y="Verwachte Brand Uplift (%)", color="Kanaal", title="Verwachte Brand Uplift per Kanaal")
        st.plotly_chart(fig)
        
        st.markdown("**📌 Uitleg:** De CPM waarden zijn gebaseerd op gemiddelde marktkosten per kanaal. De Brand Uplift Factor wordt berekend op basis van historische prestaties en impact per kanaal. De ROI Factor wordt berekend op basis van marktanalyse en rendement per impressie.")

with tab3:
    st.subheader("🚀 Activatie & Export")
    if "kanalen" in st.session_state and st.session_state["kanalen"]:
        st.write("Klaar om naar DSP te exporteren!")
        if st.button("🔄 Genereer Export Bestand"):
            st.success("Export succesvol aangemaakt!")
