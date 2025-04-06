import pandas as pd
from sklearn.ensemble import IsolationForest

# Step 1: Load the dataset
df = pd.read_csv('mock_pipeline_data.csv')

# Step 2: Drop non-numeric columns (like names or IDs)
df_cleaned = df.select_dtypes(include=['float64', 'int64'])

# Step 3: Fit Isolation Forest
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(df_cleaned)

# Step 4: Predict anomalies
df['anomaly'] = model.predict(df_cleaned)

# Step 5: Display results
print("🔍 Anomaly Detection Result:")
print(df[df['anomaly'] == -1])  # -1 = anomaly, 1 = normal

# Filter only anomalies
anomalies = result[result['anomaly'] == -1]

# Save to Markdown file
if not anomalies.empty:
    anomalies.to_markdown("anomaly_report.md", index=False)
    print("\n📄 Anomaly Report saved to 'anomaly_report.md'")
else:
    print("\n✅ No anomalies detected.")
