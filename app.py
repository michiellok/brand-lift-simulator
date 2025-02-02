import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titel van de app
st.title("Brand Lift & Cross-Channel Optimization Dashboard")
st.subheader("Simuleer en optimaliseer jouw media-allocatie voor maximale impact")

# Initialiseer session state met standaardwaarden indien niet aanwezig
default_values = {
    "active_tab": "📖 Uitleg",
    "media_alloc": {},
    "budget": 10000,
    "campaign_duration": 30,
    "cpm": 10,
    "frequency_cap": 10,
    "creative_effectiveness": 0.7,
    "context_fit": 0.5,
    "selected_channels": ["Display", "Video", "DOOH", "Social", "CTV"],
    "brand_lift_per_channel": {},
    "brand_lift_index": 100,
    "ai_recommendations": {},
    "total_brand_lift": 0
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Tabs maken met Streamlit
tabs = st.tabs(["📖 Uitleg", "📊 Invoer", "🚀 Resultaten", "🔍 Optimalisatie", "📂 Export", "📈 Scenario's"])

# Functie om Brand Lift te berekenen
def bereken_brand_lift():
    if not st.session_state["media_alloc"]:
        st.session_state["total_brand_lift"] = 0
        return

    base_lift = (st.session_state["budget"] / 10000) * 5  # Basis impact per 10k budget
    attention_factor = st.session_state["creative_effectiveness"] * 2
    frequency_factor = st.session_state["frequency_cap"] * 0.1
    lift_per_channel = {}

    for channel, alloc in st.session_state["media_alloc"].items():
        if alloc > 0:
            channel_lift = base_lift * (alloc / 100) * attention_factor * frequency_factor
        else:
            channel_lift = 0
        lift_per_channel[channel] = channel_lift

    st.session_state["brand_lift_per_channel"] = lift_per_channel
    st.session_state["total_brand_lift"] = sum(lift_per_channel.values())

# Uitleg Tab
with tabs[0]:
    st.header("📖 Uitleg")
    st.write("""
    Welkom bij het Brand Lift & Cross-Channel Optimization Dashboard. Met deze tool kun je de impact van je mediacampagnes simuleren en optimaliseren over verschillende kanalen.
    Gebruik de 'Invoer' tab om je campagne-instellingen te specificeren, en bekijk de resultaten en optimalisaties in de respectievelijke tabs.
    """)

# Invoer Tab
with tabs[1]:
    st.header("📊 Campagne-instellingen")
    st.session_state["budget"] = st.number_input("Totaal Budget (in €)", min_value=100, max_value=1000000, value=st.session_state["budget"], step=100)
    st.session_state["campaign_duration"] = st.slider("Campagne Duur (dagen)", 1, 90, st.session_state["campaign_duration"])
    st.session_state["frequency_cap"] = st.slider("Frequency Cap (max. aantal vertoningen per gebruiker)", 1, 20, st.session_state["frequency_cap"])

    st.header("📡 Kies Media Kanalen")
    st.session_state["selected_channels"] = st.multiselect("Selecteer kanalen", ["Display", "Video", "DOOH", "Social", "CTV"], default=st.session_state["selected_channels"])

    st.header("📡 Media Allocatie")
    st.session_state["media_alloc"] = {channel: st.slider(f"{channel} (%)", 0, 100, 20) for channel in st.session_state["selected_channels"]}

    if st.button("Bereken Brand Lift"):
        bereken_brand_lift()

# Resultaten Tab
with tabs[2]:
    st.header("🚀 Resultaten en Analyse")
    if st.session_state["total_brand_lift"] == 0:
        st.write("Geen resultaten beschikbaar. Vul de campagne-instellingen in en genereer de Brand Lift.")
    else:
        st.metric(label="Totale Brand Lift", value=round(st.session_state["total_brand_lift"], 2))
        st.write("De Brand Lift wordt berekend op basis van de gekozen instellingen. Gebruik de optimalisatie-tab om betere resultaten te krijgen.")

        fig, ax = plt.subplots()
        channels = list(st.session_state["brand_lift_per_channel"].keys())
        lifts = list(st.session_state["brand_lift_per_channel"].values())
        ax.barh(channels, lifts, color='skyblue')
        ax.set_xlabel("Brand Lift Score")
        ax.set_title("Brand Lift per Kanaal")
        st.pyplot(fig)

# Optimalisatie Tab
with tabs[3]:
    st.header("🔍 AI-gestuurde Optimalisatie Advies")
    if st.session_state["total_brand_lift"] > 0:
        st.write("Op basis van de ingevoerde waarden wordt hier een aanbeveling weergegeven.")
        st.json(st.session_state["ai_recommendations"])
    else:
        st.write("Geen data beschikbaar voor optimalisatie. Bereken eerst de Brand Lift.")

# Export Tab
with tabs[4]:
    st.header("📂 Export")
    if st.session_state["total_brand_lift"] > 0:
        df = pd.DataFrame.from_dict(st.session_state["brand_lift_per_channel"], orient='index', columns=['Brand Lift'])
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            label="Download resultaten als CSV",
            data=csv,
            file_name='brand_lift_resultaten.csv',
            mime='text/csv',
        )
    else:
        st.write("Geen gegevens beschikbaar om te exporteren. Bereken eerst de Brand Lift.")

# Scenario's Tab
with tabs[5]:
    st.header("📈 Scenario Analyse")
    if st.session_state["total_brand_lift"] > 0:
        st.write("Experimenteer met verschillende budgetten en frequenties om de optimale strategie te vinden.")
    else:
        st.write("Geen gegevens beschikbaar voor scenario-analyse. Bereken eerst de Brand Lift.")






