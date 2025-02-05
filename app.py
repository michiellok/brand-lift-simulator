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

with tab2:
    st.subheader("📈 Voorspelling & Scenario’s")
    if kanalen:
        voorspellingen = pd.DataFrame({
            "Kanaal": kanalen,
            "CPM (€)": [np.random.randint(5, 50) for _ in kanalen],
            "Brand Uplift (%)": [np.random.uniform(1, 10) for _ in kanalen]
        })
        voorspellingen["Impressies"] = budget * (voorspellingen["Brand Uplift (%)"] / 100)
        st.dataframe(voorspellingen)
        fig = px.bar(voorspellingen, x="Kanaal", y="Brand Uplift (%)", color="Kanaal", title="Verwachte Brand Uplift per Kanaal")
        st.plotly_chart(fig)

with tab3:
    st.subheader("🚀 Activatie & Export")
    if kanalen:
        st.write("Klaar om naar DSP te exporteren!")
        if st.button("🔄 Genereer Export Bestand"):
            st.success("Export succesvol aangemaakt!")
