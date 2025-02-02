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
    st.session_state["active_tab"] = "📖 Uitleg"
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

# Tabs maken met Streamlit tabs
tabs = st.tabs(["📖 Uitleg", "📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie", "📂 Export", "📈 Scenario's"])

# Uitleg Tab
with tabs[0]:
    st.header("📖 Uitleg van het Model")
    st.write("Dit model voorspelt de Brand Lift op basis van verschillende factoren zoals budget, kanaalallocatie, aandacht en creatieve effectiviteit. Het doel is om mediabureaus en adverteerders te helpen bij het optimaliseren van hun media-inzet.")
    st.write("\n\n**Wat houdt het model in?**\n\nHet model berekent de impact van verschillende mediakanalen en hoe ze bijdragen aan de Brand Lift. Hierbij wordt rekening gehouden met factoren zoals frequentie, creatieve effectiviteit en contextuele geschiktheid.")
    st.write("\n\n**Wat ontbreekt nog?**\n\nHet model bevat nog geen real-time feedback loops en externe datakoppelingen zoals live marktdata en concurrentie-analyse. In de volgende fasen worden deze toegevoegd om de nauwkeurigheid en betrouwbaarheid te vergroten.")

# Invoer Tab
with tabs[1]:
    st.header("📊 Campagne-instellingen")
    st.session_state["budget"] = st.number_input("Totaal Budget (in €)", min_value=100, max_value=1000000, value=st.session_state["budget"], step=100)
    st.session_state["campaign_duration"] = st.slider("Campagne Duur (dagen)", 1, 90, st.session_state["campaign_duration"])
    st.session_state["frequency_cap"] = st.slider("Frequency Cap (max. aantal vertoningen per gebruiker)", 1, 20, st.session_state["frequency_cap"])
    
    st.header("📡 Kies Media Kanalen")
    st.session_state["selected_channels"] = st.multiselect("Selecteer kanalen", ["Display", "Video", "DOOH", "Social", "CTV"], default=st.session_state["selected_channels"])
    
    st.header("📡 Media Allocatie")
    media_alloc = {channel: st.slider(f"{channel} (%)", 0, 100, 20) for channel in st.session_state["selected_channels"]}
    st.session_state["media_alloc"] = media_alloc

# Resultaten Tab
with tabs[2]:
    st.header("🚀 Resultaten en Analyse")
    st.metric(label="Totale Brand Lift", value=round(st.session_state["total_brand_lift"], 2))
    st.write("De Brand Lift wordt berekend op basis van de gekozen instellingen. Gebruik de optimalisatie-tab om betere resultaten te krijgen.")
    st.write("\n**Waarom is de Brand Lift zo hoog of laag?**\n\nDe berekening houdt rekening met: budget, aandacht, creatieve effectiviteit en de media-allocatie. Lage aandacht en ongeschikte allocatie kunnen de Brand Lift verlagen.")

# Optimalisatie Tab
with tabs[3]:
    st.header("🔍 AI-gestuurde Optimalisatie Advies")
    if st.session_state["ai_recommendations"]:
        st.json(st.session_state["ai_recommendations"])
    else:
        st.write("Nog geen AI-aanbevelingen beschikbaar. Voer gegevens in om een advies te ontvangen.")
    
    st.header("🔧 Handmatige Aanpassing")
    st.markdown("Pas de media-allocatie handmatig aan op basis van AI-aanbevelingen.")
    for channel in st.session_state["selected_channels"]:
        st.session_state["media_alloc"][channel] = st.number_input(f"{channel} Budget (handmatig aanpassen in €)", min_value=0, max_value=st.session_state["budget"], value=st.session_state["media_alloc"].get(channel, 0), step=100)
    
    st.markdown("Nadat je de aanpassingen hebt gemaakt, bekijk je de resultaten in de resultaten-tab.")

# Export Tab
with tabs[4]:
    st.header("📂 Export Resultaten")
    df_export = pd.DataFrame(st.session_state["media_alloc"], index=[0])
    st.download_button("Download als CSV", df_export.to_csv(), "brand_lift_results.csv")

# Scenario Tab
with tabs[5]:
    st.header("📈 Scenario Analyse")
    st.write("Werkende scenario's worden hier weergegeven.")



















