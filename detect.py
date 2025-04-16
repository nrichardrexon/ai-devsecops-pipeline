import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime
import argparse
import os
import json

# 🧠 Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--data', default='mock_pipeline_data.csv', help='Path to the dataset')
args = parser.parse_args()
csv_file = args.data

# 🔍 Load the dataset
df = pd.read_csv(csv_file)

# 🧹 Keep only numeric columns
df_cleaned = df.select_dtypes(include=['float64', 'int64'])

if df_cleaned.empty:
    raise ValueError("No numeric columns found to perform anomaly detection.")

# 🌲 Isolation Forest with custom threshold
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(df_cleaned)
df['anomaly'] = model.predict(df_cleaned)

# 🧬 Identify anomalies
anomalies = df[df['anomaly'] == -1]
print("🔍 Anomaly Detection Result:")
print(anomalies)
print(f"\n🧪 Total anomalies found: {len(anomalies)}")

# 🧾 Track run-level metadata
timestamp = datetime.utcnow().isoformat() + "Z"
github_sha = os.getenv("GITHUB_SHA", "local-dev")
run_id = os.getenv("GITHUB_RUN_ID", "manual-run")

# 📄 Generate anomaly_report.md
if not anomalies.empty:
    markdown = []
    markdown.append("# 🧠 Anomaly Report\n")
    markdown.append("## 🔎 Metadata")
    markdown.append(f"- **Timestamp**: `{timestamp}`")
    markdown.append(f"- **GitHub SHA**: `{github_sha}`")
    markdown.append(f"- **Run ID**: `{run_id}`")
    markdown.append(f"- **CSV File**: `{csv_file}`")
    markdown.append(f"- **Total Rows**: `{len(df)}`")
    markdown.append(f"- **Anomalies Found**: `{len(anomalies)}`\n")

    markdown.append("## ⚠️ Anomalous Rows:\n```")
    markdown.append(anomalies.to_string(index=False))
    markdown.append("```\n")

    with open("anomaly_report.md", "w") as f:
        f.write("\n".join(markdown))
    anomalies.to_csv("anomaly_report.csv", index=False)

    print("✅ Anomaly report saved to 'anomaly_report.md' and 'anomaly_report.csv'")

    # 🧠 Log anomalies over time for audit trail
    anomalies['timestamp'] = timestamp
    anomalies['run_id'] = run_id
    anomalies['commit_sha'] = github_sha
    anomalies['source_file'] = csv_file

    log_file = "anomaly_log.csv"
    if os.path.exists(log_file):
        prev_log = pd.read_csv(log_file)
        combined = pd.concat([prev_log, anomalies], ignore_index=True)
        combined.to_csv(log_file, index=False)
    else:
        anomalies.to_csv(log_file, index=False)
    print(f"📝 Logged {len(anomalies)} anomaly entries to '{log_file}'")

else:
    print("✅ No anomalies detected.")
    if os.path.exists("anomaly_report.md"):
        os.remove("anomaly_report.md")
    if os.path.exists("anomaly_report.csv"):
        os.remove("anomaly_report.csv")
