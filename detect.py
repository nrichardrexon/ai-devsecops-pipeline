import pandas as pd
from sklearn.ensemble import IsolationForest
import os

# Step 1: Load the dataset
df = pd.read_csv('mock_pipeline_data.csv')

# Step 2: Drop non-numeric columns
df_cleaned = df.select_dtypes(include=['float64', 'int64'])

# Optional: Warn if nothing to work with
if df_cleaned.empty:
    raise ValueError("No numeric columns found in dataset to perform anomaly detection.")

# Step 3: Fit Isolation Forest
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(df_cleaned)

# Step 4: Predict anomalies
df['anomaly'] = model.predict(df_cleaned)

# Step 5: Display results
print("🔍 Anomaly Detection Result:")
print(df[df['anomaly'] == -1])

# Step 6: Filter anomalies
anomalies = df[df['anomaly'] == -1]
print(f"\n🧪 Total anomalies found: {len(anomalies)}")

# Step 7: Save report
if not anomalies.empty:
    try:
        from prettytable import PrettyTable

        table = PrettyTable()
        table.field_names = anomalies.columns.tolist()
        for _, row in anomalies.iterrows():
            table.add_row(row.tolist())

        with open("anomaly_report.md", "w") as f:
            f.write("# Anomaly Report\n\n")
            f.write("### Anomalies Detected:\n\n")
            f.write("```\n")
            f.write(str(table))
            f.write("\n```\n")

        print("\n📄 Anomaly Report saved to 'anomaly_report.md'")

    except Exception as e:
        print(f"\n⚠️ Error using prettytable: {e}")
        anomalies.to_csv("anomaly_report.csv", index=False)
        with open("anomaly_report.md", "w") as f:
            f.write("# Anomaly Report\n\n")
            f.write("⚠️ Failed to use `prettytable`.\n\n")
            f.write("Please refer to `anomaly_report.csv` for anomaly details.")
else:
    print("\n✅ No anomalies detected.")
    if os.path.exists("anomaly_report.md"):
        os.remove("anomaly_report.md")
