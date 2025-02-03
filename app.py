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
        cpm = st.number_input("📉 Gemiddelde CPM (kosten per 1000 impressies in €)", min_value=1.0, max_value=50.0, value=5.0, step=0.5)
    
    with col2:
        start_datum = st.date_input("📅 Startdatum")
        eind_datum = st.date_input("📅 Einddatum")
        weken = max((eind_datum - start_datum).days // 7, 1)  # Zorg ervoor dat weken minimaal 1 is
        freq_cap = st.slider("🔄 Max. frequentie per gebruiker", min_value=1, max_value=20, value=5, step=1)
        time_decay_factor = st.slider("⏳ Impact verloop over tijd ❔", min_value=0.01, max_value=1.0, value=0.5, step=0.01, help="Dit modelleert hoe de impact van advertenties afneemt over dagen.")
    
    # Kanaalselectie
    geselecteerde_kanalen = st.multiselect("📡 Selecteer kanalen", ["CTV", "Video", "Display", "DOOH", "Social"], default=["CTV", "Video", "Display"])
    
    # Budgetverdeling per week
    st.subheader("📊 Budgetverdeling per week")
    budget_per_week = []
    for i in range(weken):
        budget = st.slider(f"Week {i+1} budget (%)", 0, 100, 100 // weken, step=5)
        budget_per_week.append(budget)
    
    # Normaliseer budget per week zodat het totaal 100% is
    budget_per_week = np.array(budget_per_week) / sum(budget_per_week) * totaal_budget
    
    # Scenario-optimalisatie
    if st.button("🔍 Bereken optimale mediaselectie"):
        optimalisatie_data = []
        totaal_bereik = (totaal_budget / cpm) * 1000
        
        kanaal_effectiviteit = {
            "Merkbekendheid verhogen": {"CTV": 0.9, "Video": 0.8, "Display": 0.7, "DOOH": 0.9, "Social": 0.6},
            "Overweging stimuleren": {"CTV": 0.6, "Video": 0.9, "Display": 0.7, "DOOH": 0.7, "Social": 0.8},
            "Voorkeur opbouwen": {"CTV": 0.5, "Video": 0.8, "Display": 0.9, "DOOH": 0.6, "Social": 0.7},
            "Koopintentie versterken": {"CTV": 0.4, "Video": 0.7, "Display": 0.8, "DOOH": 0.5, "Social": 0.9}
        }
        
        for kanaal in geselecteerde_kanalen:
            effectiviteit = kanaal_effectiviteit[campagne_doel][kanaal]
            bereik = (effectiviteit / sum([kanaal_effectiviteit[campagne_doel][k] for k in geselecteerde_kanalen])) * totaal_bereik
            impact = effectiviteit * bereik * np.exp(-time_decay_factor * weken)
            optimalisatie_data.append([kanaal, effectiviteit, bereik, impact])
        
        optimalisatie_df = pd.DataFrame(optimalisatie_data, columns=["Kanaal", "Effectiviteit", "Bereik", "Impact"])
        optimalisatie_df = optimalisatie_df.sort_values(by="Effectiviteit", ascending=False)
        totaal_impact = optimalisatie_df["Impact"].sum()
        optimalisatie_df["Budget Allocatie (€)"] = (optimalisatie_df["Impact"] / totaal_impact) * totaal_budget
        st.session_state["optimalisatie_df"] = optimalisatie_df
        
        st.subheader("📢 Optimale Budgetverdeling")
        st.dataframe(optimalisatie_df[["Kanaal", "Budget Allocatie (€)", "Bereik", "Effectiviteit"]].reset_index(drop=True))

        # Lijngrafiek voor impact verloop per week
        st.subheader("📊 Impact Verloop per Week")
        impact_over_weken = [np.exp(-time_decay_factor * w) for w in range(weken + 1)]
        impact_df = pd.DataFrame({"Week": range(weken + 1), "Impact Factor": impact_over_weken})
        fig = px.line(impact_df, x="Week", y="Impact Factor", title="Impact verloop per week")
        st.plotly_chart(fig)

