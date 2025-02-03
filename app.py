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

# Tabs voor structuur
tab1, tab2, tab3 = st.tabs(["📊 Basis Optimalisatie", "🛠 Scenario Analyse", "📈 ROI & Budget Optimalisatie"])

if "optimalisatie_df" not in st.session_state:
    st.session_state["optimalisatie_df"] = None
if "totaal_budget" not in st.session_state:
    st.session_state["totaal_budget"] = 50000  # Standaard budget

with tab1:
    st.subheader("📌 Campagne-instellingen")
    
    # Invoerparameters
    col1, col2 = st.columns(2)
    with col1:
        campagne_doel = st.selectbox("Wat is het primaire doel van je campagne?", [
            "Merkbekendheid verhogen",
            "Overweging stimuleren",
            "Voorkeur opbouwen",
            "Koopintentie versterken"
        ])
        totaal_budget = st.number_input("💰 Wat is het totale budget (in €)?", min_value=1000, max_value=1000000, value=50000)
        st.session_state["totaal_budget"] = totaal_budget  # Sla budget op voor andere tabs
        cpm = st.number_input("📉 Gemiddelde CPM (kosten per 1000 impressies in €)", min_value=1.0, max_value=50.0, value=5.0, step=0.5)
    
    with col2:
        start_datum = st.date_input("📅 Startdatum")
        eind_datum = st.date_input("📅 Einddatum")
        weken = max((eind_datum - start_datum).days // 7, 1)  # Zorg ervoor dat weken minimaal 1 is
        freq_cap = st.slider("🔄 Max. frequentie per gebruiker", min_value=1, max_value=20, value=5, step=1)
        time_decay_factor = st.slider("⏳ Impact verloop over tijd ❔", min_value=0.01, max_value=1.0, value=0.5, step=0.01, help="Dit modelleert hoe de impact van advertenties afneemt over dagen.")
    
    # Kanaalselectie
    geselecteerde_kanalen = st.multiselect("📡 Selecteer kanalen", ["CTV", "Video", "Display", "DOOH", "Social"], default=["CTV", "Video", "Display"])
    
    # Effectiviteitscores per kanaal
    effectiviteit_scores = {"CTV": 0.9, "Video": 0.8, "Display": 0.7, "DOOH": 0.6, "Social": 0.5}
    
    # Budgetverdeling per kanaal op basis van effectiviteit
    totale_effectiviteit = sum([effectiviteit_scores[k] for k in geselecteerde_kanalen])
    budget_allocatie = {k: (effectiviteit_scores[k] / totale_effectiviteit) * totaal_budget for k in geselecteerde_kanalen}
    impressies_per_kanaal = {k: budget_allocatie[k] / cpm * 1000 for k in geselecteerde_kanalen}
    
    # Scenario-optimalisatie
    if st.button("🔍 Bereken optimale mediaselectie"):
        st.session_state["optimalisatie_df"] = pd.DataFrame({
            "Kanaal": list(budget_allocatie.keys()),
            "Budget Allocatie (€)": list(budget_allocatie.values()),
            "Impressies": list(impressies_per_kanaal.values()),
            "Effectiviteit": [effectiviteit_scores[k] for k in budget_allocatie.keys()]
        })
        st.success("✅ Mediaselectie berekend!")
        
        # Grafieken genereren
        st.subheader("📊 Budget Allocatie per Kanaal")
        fig = px.bar(st.session_state["optimalisatie_df"], x="Kanaal", y="Budget Allocatie (€)", color="Kanaal", title="Budget Allocatie per Kanaal")
        st.plotly_chart(fig)
        
        st.subheader("📊 Impressies per Kanaal")
        fig = px.bar(st.session_state["optimalisatie_df"], x="Kanaal", y="Impressies", color="Kanaal", title="Impressies per Kanaal")
        st.plotly_chart(fig)

with tab2:
    st.subheader("🛠 Scenario Analyse")
    if st.session_state["optimalisatie_df"] is None:
        st.warning("🔹 Voer eerst een berekening uit in het tabblad 'Basis Optimalisatie'.")
    else:
        scenario_budget_pct = st.slider("💰 Wat als we het budget verhogen? (in %)", min_value=100, max_value=200, value=100, step=5)
        scenario_budget = (scenario_budget_pct / 100) * st.session_state["totaal_budget"]
        impact_toename = scenario_budget / st.session_state["totaal_budget"]
        optimalisatie_df = st.session_state["optimalisatie_df"].copy()
        optimalisatie_df["Budget Allocatie (€)"] *= impact_toename
        optimalisatie_df["Impressies"] *= impact_toename
        st.dataframe(optimalisatie_df)
        fig = px.bar(optimalisatie_df, x="Kanaal", y="Budget Allocatie (€)", color="Kanaal", title="Scenario Impact op Budgetverdeling")
        st.plotly_chart(fig)

with tab3:
    st.subheader("📈 ROI & Budget Optimalisatie")
    if st.session_state["optimalisatie_df"] is None:
        st.warning("🔹 Voer eerst een berekening uit in het tabblad 'Basis Optimalisatie'.")
    else:
        st.write("🔍 ROI analyse op basis van budgetverdeling.")
        optimalisatie_df = st.session_state["optimalisatie_df"].copy()
        optimalisatie_df["ROI"] = optimalisatie_df["Budget Allocatie (€)"] / st.session_state["totaal_budget"] * 100
        st.dataframe(optimalisatie_df)
        fig = px.line(optimalisatie_df, x="Kanaal", y="ROI", title="ROI per Kanaal")
        st.plotly_chart(fig)

