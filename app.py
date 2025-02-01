import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titel van de app
st.title("Brand Lift & Time Decay Simulator")
st.subheader("Pas de parameters aan en bekijk direct de impact op Brand Lift")

# Inputvelden voor scenario
st.sidebar.header("Campagne-instellingen")
media_type = st.sidebar.selectbox("Mediatype", ["Display", "Video", "DOOH", "Social"])
reach = st.sidebar.slider("Reach (miljoen)", 1, 50, 10)
frequency = st.sidebar.slider("Frequency", 1, 10, 5)
attention = st.sidebar.slider("Attention Score", 0.1, 1.0, 0.7)
creative_quality = st.sidebar.slider("Creative Quality", 0.1, 1.0, 0.8)
context_fit = st.sidebar.slider("Context Fit", 0.1, 1.0, 0.7)

decay_rates = {"Display": 0.20, "Video": 0.10, "DOOH": 0.05, "Social": 0.15}
decay_rate = decay_rates[media_type]

# Berekening van Brand Lift
brand_lift = (0.4 * reach) + (0.3 * frequency) + (0.6 * attention) + (0.4 * creative_quality) + (0.3 * context_fit)

# Weergeven van resultaten
st.metric(label="📊 Brand Lift", value=round(brand_lift, 2))
st.write("Mediatype:", media_type)
st.write("Time Decay Rate:", decay_rate)

# Time Decay simulatie
days = np.arange(0, 30, 1)
lift_values = brand_lift * np.exp(-decay_rate * days)

df_decay = pd.DataFrame({"Dagen": days, "Brand Lift": lift_values})
st.line_chart(df_decay.set_index("Dagen"))

st.write("🔹 Hoe werkt dit model?")
st.write("- Pas de waarden in de zijbalk aan om direct het effect op Brand Lift te zien.")
st.write("- De Time Decay-grafiek toont hoe de impact afneemt over 30 dagen.")
