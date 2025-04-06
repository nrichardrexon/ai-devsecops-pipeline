import pandas as pd
from sklearn.ensemble import IsolationForest
import os

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

# Step 6: Filter and Save Anomalies
anomalies = df[df['anomaly'] == -1]

# Step 7: Save anomaly report with fallback
if not anomalies.empty:
    try:
        from tabulate import tabulate
        anomalies.to_markdown("anomaly_report.md", index=False)
        print("\n📄 Anomaly Report saved to 'anomaly_report.md'")
    except ImportError:
        print("\n⚠️ 'tabulate' not found. Saving fallback CSV report.")
        anomalies.to_csv("anomaly_report.csv", index=False)
        # Create a dummy markdown file to avoid workflow break
        with open("anomaly_report.md", "w") as f:
            f.write("# Anomaly Report\n\nTabulate module missing. See anomaly_report.csv instead.")
else:
    print("\n✅ No anomalies detected.")
    # Ensure markdown file is absent if no anomalies
    if os.path.exists("anomaly_report.md"):
        os.remove("anomaly_report.md")
