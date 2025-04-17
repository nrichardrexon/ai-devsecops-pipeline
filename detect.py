"""🔍 Real-time anomaly detection with Isolation Forest (rolling training + live test)."""

import argparse
import os
from datetime import datetime
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# 📥 CLI Argument
parser = argparse.ArgumentParser(description="🔍 Real-time anomaly detection using Isolation Forest")
parser.add_argument('--data', default='Clean Error-Free Mock Dataset.csv', help='Path to the dataset CSV')
args = parser.parse_args()
csv_file = args.data

# 📁 Directories
REPORTS_DIR = "reports"
MODEL_PATH = os.path.join(REPORTS_DIR, "isolation_forest_model.joblib")
LOG_PATH = os.path.join(REPORTS_DIR, "anomaly_log.csv")
os.makedirs(REPORTS_DIR, exist_ok=True)

# 📌 Metadata
timestamp = datetime.utcnow().isoformat() + "Z"
github_sha = os.getenv("GITHUB_SHA", "local-dev")
run_id = os.getenv("GITHUB_RUN_ID", "manual-run")

# 📖 Load dataset
try:
    df = pd.read_csv(csv_file, encoding='utf-8')
except FileNotFoundError:
    raise FileNotFoundError(f"🚫 File not found: {csv_file}")

# 🔍 Data checks
required_numeric = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
if len(required_numeric) < 1:
    raise ValueError("⚠️ No numeric columns found for anomaly detection.")

# 🔄 Rolling window config
MAX_MEMORY_ROWS = 1000

# 🔧 Prepare training/testing data
df_cleaned = df[required_numeric].copy()
latest_row = df_cleaned.tail(1)
training_data = df_cleaned.iloc[:-1]

# 🧠 Load or train model
if os.path.exists(MODEL_PATH) and len(training_data) > 10:
    model = joblib.load(MODEL_PATH)
else:
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)

# 🎓 Train (rolling update)
if os.path.exists(LOG_PATH):
    memory_df = pd.read_csv(LOG_PATH)
    memory_df = memory_df[memory_df['anomaly'] == 0]  # Only clean rows
    memory_df = pd.concat([memory_df, training_data], ignore_index=True).tail(MAX_MEMORY_ROWS)
else:
    memory_df = training_data.tail(MAX_MEMORY_ROWS)

model.fit(memory_df)

# 💾 Save updated model
joblib.dump(model, MODEL_PATH)

# 🔎 Predict on the latest row only
df['anomaly'] = 0
latest_anomaly = model.predict(latest_row)[0]
df.iloc[-1, df.columns.get_loc('anomaly')] = latest_anomaly

# 🚨 If anomaly detected
report_md = os.path.join(REPORTS_DIR, "anomaly_report.md")
report_csv = os.path.join(REPORTS_DIR, "anomaly_report.csv")

if latest_anomaly == -1:
    latest_full = df.tail(1).copy()

    # 📓 Markdown Report
    markdown = [
        "# 🧠 Anomaly Report",
        "## 🔎 Metadata",
        f"- **Timestamp**: `{timestamp}`",
        f"- **GitHub SHA**: `{github_sha}`",
        f"- **Run ID**: `{run_id}`",
        f"- **CSV File**: `{csv_file}`",
        f"- **Total Rows Scanned**: `{len(df)}`",
        f"- **Anomalies Found**: `1`",
        "",
        "## ⚠️ Anomalous Row",
        "```",
        latest_full.to_string(index=False),
        "```"
    ]
    with open(report_md, "w", encoding='utf-8') as f:
        f.write("\n".join(markdown))

    latest_full.to_csv(report_csv, index=False, encoding='utf-8')
    print("🚨 Anomaly detected in latest run.")
    print(f"✅ Saved '{report_md}' and '{report_csv}'.")

    # 🧾 Log anomaly
    latest_full['timestamp'] = timestamp
    latest_full['run_id'] = run_id
    latest_full['commit_sha'] = github_sha
    latest_full['source_file'] = csv_file

    if os.path.exists(LOG_PATH):
        old_log = pd.read_csv(LOG_PATH)
        new_log = pd.concat([old_log, latest_full], ignore_index=True)
        new_log.to_csv(LOG_PATH, index=False)
    else:
        latest_full.to_csv(LOG_PATH, index=False)

    print(f"📝 Anomaly logged in '{LOG_PATH}'")
else:
    print("✅ No anomaly detected.")
    for file in [report_md, report_csv]:
        if os.path.exists(file):
            os.remove(file)
