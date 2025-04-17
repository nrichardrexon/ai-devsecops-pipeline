"""🔍 Anomaly detection using Isolation Forest on a CSV dataset."""

import argparse
import os
from datetime import datetime

import pandas as pd
from sklearn.ensemble import IsolationForest

# 🧠 CLI: Parse input file path
parser = argparse.ArgumentParser(description="🔍 Anomaly detection using Isolation Forest")
parser.add_argument('--data', default='mock_pipeline_data.csv', help='Path to the dataset CSV')
args = parser.parse_args()
csv_file = args.data

# 📥 Load dataset
try:
    df = pd.read_csv(csv_file, encoding='utf-8')
except FileNotFoundError as e:
    raise FileNotFoundError(f"🚫 File not found: {csv_file}") from e

# 🧹 Clean: Select only numeric columns
df_cleaned = df.select_dtypes(include=['float64', 'int64'])

if df_cleaned.empty:
    raise ValueError("⚠️ No numeric columns found for anomaly detection.")

# 🌲 Model: Train Isolation Forest
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(df_cleaned)

# 🔎 Predict anomalies
df['anomaly'] = model.predict(df_cleaned)
anomalies = df[df['anomaly'] == -1]

# 📁 Ensure reports directory exists
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# 📌 Metadata for traceability
timestamp = datetime.utcnow().isoformat() + "Z"
github_sha = os.getenv("GITHUB_SHA", "local-dev")
run_id = os.getenv("GITHUB_RUN_ID", "manual-run")

# 🧾 Report generation
report_md = os.path.join(REPORTS_DIR, "anomaly_report.md")
report_csv = os.path.join(REPORTS_DIR, "anomaly_report.csv")
log_file = os.path.join(REPORTS_DIR, "anomaly_log.csv")

if not anomalies.empty:
    print("🚨 Anomalies detected!")
    print(anomalies)

    markdown = [
        "# 🧠 Anomaly Report",
        "## 🔎 Metadata",
        f"- **Timestamp**: `{timestamp}`",
        f"- **GitHub SHA**: `{github_sha}`",
        f"- **Run ID**: `{run_id}`",
        f"- **CSV File**: `{csv_file}`",
        f"- **Total Rows Scanned**: `{len(df)}`",
        f"- **Anomalies Found**: `{len(anomalies)}`\n",
        "## ⚠️ Anomalous Rows",
        "```",
        anomalies.to_string(index=False),
        "```"
    ]

    with open(report_md, "w", encoding='utf-8') as f:
        f.write("\n".join(markdown))

    anomalies.to_csv(report_csv, index=False, encoding='utf-8')
    print(f"✅ Saved '{report_md}' and '{report_csv}'.")

    # 📊 Append anomaly log
    anomalies['timestamp'] = timestamp
    anomalies['run_id'] = run_id
    anomalies['commit_sha'] = github_sha
    anomalies['source_file'] = csv_file

    if os.path.exists(log_file):
        old_log = pd.read_csv(log_file, encoding='utf-8')
        new_log = pd.concat([old_log, anomalies], ignore_index=True)
        new_log.to_csv(log_file, index=False, encoding='utf-8')
    else:
        anomalies.to_csv(log_file, index=False, encoding='utf-8')

    print(f"📝 Anomalies logged in '{log_file}'")

else:
    print("✅ No anomalies detected.")
    for file_name in [report_md, report_csv]:
        if os.path.exists(file_name):
            os.remove(file_name)
