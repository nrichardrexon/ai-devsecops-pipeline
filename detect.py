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
        # Check if prettytable is available
        try:
            from prettytable import PrettyTable
        except ImportError as e:
            raise ImportError("prettytable module is missing. Falling back to CSV format.")
        
        # Create a PrettyTable instance
        table = PrettyTable()
        table.field_names = anomalies.columns.tolist()

        # Add rows to the table
        for _, row in anomalies.iterrows():
            table.add_row(row.tolist())

        # Write the markdown report
        with open("anomaly_report.md", "w") as f:
            f.write("# Anomaly Report\n\n")
            f.write("### Anomalies Detected:\n\n")
            f.write("```\n")
            f.write(str(table))
            f.write("\n```\n")

        # Save anomalies as CSV
        anomalies.to_csv("anomaly_report.csv", index=False)

        print("\n📄 Anomaly Report saved to 'anomaly_report.md' and 'anomaly_report.csv'")

    except ImportError as e:
        print(f"\n⚠️ {e}")
        # Save anomalies in CSV and provide a fallback message in markdown
        anomalies.to_csv("anomaly_report.csv", index=False)
        with open("anomaly_report.md", "w") as f:
            f.write("# Anomaly Report\n\n")
            f.write(f"⚠️ {e}\n\n")
            f.write("Please refer to `anomaly_report.csv` for anomaly details.")

    except Exception as e:
        print(f"\n⚠️ Error while generating report: {e}")
        anomalies.to_csv("anomaly_report.csv", index=False)
        with open("anomaly_report.md", "w") as f:
            f.write("# Anomaly Report\n\n")
            f.write("⚠️ An error occurred while generating the prettytable format.\n\n")
            f.write("Please refer to `anomaly_report.csv` for anomaly details.")
else:
    print("\n✅ No anomalies detected.")
    # Remove the markdown file if no anomalies
    if os.path.exists("anomaly_report.md"):
        os.remove("anomaly_report.md")
    if os.path.exists("anomaly_report.csv"):
        os.remove("anomaly_report.csv")
