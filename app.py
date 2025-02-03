import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Dummy data genereren
def generate_dummy_data(n=100):
    np.random.seed(42)
    data = {
        "Reach": np.random.randint(100000, 5000000, n),
        "Frequency": np.random.uniform(1, 10, n),
        "Attention": np.random.uniform(0.1, 1, n),
        "Creative Quality": np.random.uniform(0.1, 1, n),
        "Context Fit": np.random.uniform(0.1, 1, n),
        "Time Decay": np.random.uniform(0.1, 1, n),
    }
    df = pd.DataFrame(data)
    df["Brand Lift"] = (
        (0.4 * df["Reach"] / 1_000_000) +
        (0.3 * df["Frequency"]) +
        (0.6 * df["Attention"]) +
        (0.4 * df["Creative Quality"]) +
        (0.3 * df["Context Fit"]) -
        (0.2 * df["Time Decay"])
    )
    return df

# Streamlit app
st.title("Brand Lift Model Dashboard")

df = generate_dummy_data()

# KPI's
st.subheader("Kerncijfers")
st.metric("Gemiddelde Brand Lift", round(df["Brand Lift"].mean(), 2))
st.metric("Maximale Brand Lift", round(df["Brand Lift"].max(), 2))
st.metric("Minimale Brand Lift", round(df["Brand Lift"].min(), 2))

# Scatterplot
st.subheader("Brand Lift vs. Reach")
fig = px.scatter(df, x="Reach", y="Brand Lift", color="Attention", 
                 title="Impact van Reach en Attention op Brand Lift",
                 labels={"Reach": "Bereik", "Brand Lift": "Brand Lift Score"})
st.plotly_chart(fig)

# Histogram
st.subheader("Verdeling van Brand Lift Scores")
fig_hist = px.histogram(df, x="Brand Lift", nbins=20, title="Verdeling Brand Lift Scores")
st.plotly_chart(fig_hist)

# Filterfunctie
st.subheader("Filter Data")
reach_slider = st.slider("Selecteer bereik (Reach)", int(df["Reach"].min()), int(df["Reach"].max()), (int(df["Reach"].min()), int(df["Reach"].max())))
filtered_df = df[(df["Reach"] >= reach_slider[0]) & (df["Reach"] <= reach_slider[1])]
st.write(filtered_df)



