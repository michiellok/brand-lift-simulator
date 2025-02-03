import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Titel
st.title("📊 Brand Lift Model - Interactieve Simulatie")

# Invoerparameters van de gebruiker
st.sidebar.header("📌 Voer je campagnedata in")

reach = st.sidebar.number_input("🔹 Reach (aantal bereikte personen)", min_value=10000, max_value=10000000, value=500000)
frequency = st.sidebar.slider("🔹 Frequency (Gem. aantal vertoningen per persoon)", min_value=1.0, max_value=10.0, value=3.0, step=0.1)
attention = st.sidebar.slider("🔹 Attention Score", min_value=0.1, max_value=1.0, value=0.5, step=0.05)
creative_quality = st.sidebar.slider("🔹 Creative Quality", min_value=0.1, max_value=1.0, value=0.7, step=0.05)
context_fit = st.sidebar.slider("🔹 Context Fit", min_value=0.1, max_value=1.0, value=0.6, step=0.05)
time_decay = st.sidebar.slider("🔹 Time Decay (Effectiviteit over tijd)", min_value=0.1, max_value=1.0, value=0.3, step=0.05)
budget = st.sidebar.number_input("💰 Budget (in €)", min_value=1000, max_value=1000000, value=50000)

# Berekening van Brand Lift op basis van de formule
brand_lift = (0.4 * reach / 1_000_000) + (0.3 * frequency) + (0.6 * attention) + (0.4 * creative_quality) + (0.3 * context_fit) - (0.2 * time_decay)
cost_per_lift = budget / (brand_lift if brand_lift > 0 else 1)

# Weergeven van de berekende Brand Lift Score en Budget Efficiëntie
st.metric("🔥 Brand Lift Score", round(brand_lift, 3))
st.metric("💰 Kosten per Brand Lift punt", round(cost_per_lift, 2))

# Dummy dataset genereren voor verschillende kanalen
channels = ["CTV", "Video", "Display", "DOOH", "Social"]
data = {
    "Kanaal": np.random.choice(channels, 100),
    "Reach": np.random.randint(100000, 5000000, 100),
    "Frequency": np.random.uniform(1, 10, 100),
    "Attention": np.random.uniform(0.1, 1, 100),
    "Creative Quality": np.random.uniform(0.1, 1, 100),
    "Context Fit": np.random.uniform(0.1, 1, 100),
    "Time Decay": np.random.uniform(0.1, 1, 100),
    "Budget": np.random.randint(10000, 500000, 100)
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
df["Kosten per Brand Lift"] = df["Budget"] / (df["Brand Lift"] + 0.0001)

# Grafiek: Brand Lift per kanaal
st.subheader("📊 Brand Lift per Kanaal")
st.write("Deze boxplot toont de verdeling van Brand Lift per advertentiekanaal. Hogere waarden duiden op een grotere merkimpact per kanaal.")
fig = px.box(df, x="Kanaal", y="Brand Lift", color="Kanaal", title="Verdeling van Brand Lift per Kanaal")
st.plotly_chart(fig)

# Grafiek: Brand Lift vs. Reach
st.subheader("📈 Impact van Reach op Brand Lift")
st.write("Deze grafiek laat zien hoe de toename van bereik de Brand Lift beïnvloedt. Elke kleur vertegenwoordigt een kanaal.")
fig2 = px.scatter(df, x="Reach", y="Brand Lift", color="Kanaal", 
                 title="Impact van Reach op Brand Lift per Kanaal",
                 labels={"Reach": "Bereik", "Brand Lift": "Brand Lift Score"})
st.plotly_chart(fig2)

# Heatmap: Factoren die Brand Lift beïnvloeden
st.subheader("🔍 Correlatie tussen factoren en Brand Lift")
st.write("Deze heatmap toont de correlaties tussen verschillende variabelen en Brand Lift. Sterkere positieve of negatieve waarden geven een sterke relatie aan.")
corr_matrix = df[["Reach", "Frequency", "Attention", "Creative Quality", "Context Fit", "Time Decay", "Brand Lift"]].corr()
fig3 = px.imshow(corr_matrix, labels=dict(color="Correlatie"), title="Correlatie tussen variabelen en Brand Lift", x=corr_matrix.columns, y=corr_matrix.columns)
st.plotly_chart(fig3)

# Grafiek: Budget vs. Brand Lift
st.subheader("💰 Budget vs. Brand Lift Efficiëntie")
st.write("Deze grafiek toont de relatie tussen budget en Brand Lift. Campagnes met een lage kosten per lift-score zijn efficiënter.")
fig4 = px.scatter(df, x="Budget", y="Brand Lift", color="Kanaal", title="Budget vs. Brand Lift per Kanaal", labels={"Budget": "Budget (€)", "Brand Lift": "Brand Lift Score"})
st.plotly_chart(fig4)

# Filterfunctie
st.subheader("Filter Data per Kanaal")
kanaal_selectie = st.multiselect("Selecteer kanalen", options=channels, default=channels)
filtered_df = df[df["Kanaal"].isin(kanaal_selectie)]
st.write(filtered_df)
