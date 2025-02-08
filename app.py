import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Simulated Dummy Data
np.random.seed(42)
campaigns = ['CTV', 'DOOH', 'Social', 'Display', 'Retail Media']
budgets = np.random.randint(5000, 50000, size=100)
exposed_lift = np.random.uniform(0.01, 0.15, size=100)
non_exposed_lift = np.random.uniform(0.005, 0.08, size=100)
media_channel = np.random.choice(campaigns, size=100)

data = pd.DataFrame({
    'Campaign': media_channel,
    'Budget': budgets,
    'Exposed_Lift': exposed_lift,
    'Non_Exposed_Lift': non_exposed_lift,
    'Lift_Difference': exposed_lift - non_exposed_lift
})

# Train ML Model for Predicting Brand Lift
X = data[['Budget']]
y = data['Lift_Difference']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

# Dashboard Visualization
plt.figure(figsize=(10, 5))
sns.barplot(data=data, x='Campaign', y='Lift_Difference', ci=None)
plt.title('Brand Lift Difference by Campaign')
plt.xlabel('Media Channel')
plt.ylabel('Brand Lift Impact')
plt.show()

# Print Model Performance
print(f'Model MAE: {mae:.4f}')

# Display sample insights
data_sorted = data.sort_values(by='Lift_Difference', ascending=False)
print("\nTop 5 Best Performing Campaigns:")
print(data_sorted.head())
