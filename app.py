import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import streamlit as st

# Simulated Dummy Data
np.random.seed(42)
campaigns = ['CTV', 'DOOH', 'Social', 'Display', 'Retail Media']
budgets = np.random.randint(5000, 50000, size=100)
exposed_lift = np.random.uniform(0.01, 0.15, size=100)
non_exposed_lift = np.random.uniform(0.005, 0.08, size=100)
media_channel = np.random.choice(campaigns, size=100)
attention_scores = np.random.uniform(0.1, 1.0, size=100)

data = pd.DataFrame({
    'Campaign': media_channel,
    'Budget': budgets,
    'Exposed_Lift': exposed_lift,
    'Non_Exposed_Lift': non_exposed_lift,
    'Lift_Difference': exposed_lift - non_exposed_lift,
    'Attention_Score': attention_scores
})

# Train ML Model for Predicting Brand Lift
X = data[['Budget', 'Attention_Score']]
y = data['Lift_Difference']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

# Streamlit Dashboard
st.title("Brand Impact & Media Optimization Dashboard")
st.write("Predicting Brand Lift based on Budget and Attention Scores")

# Display Metrics
st.metric(label="Model MAE", value=f"{mae:.4f}")

# Display Data
st.subheader("Top Performing Campaigns")
data_sorted = data.sort_values(by='Lift_Difference', ascending=False)
st.dataframe(data_sorted.head())
