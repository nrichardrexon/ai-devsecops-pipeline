"""
🔧 Auto-Remediation Script for Anomalies Detected by detect.py
This script scans the anomaly_report.csv and provides recommended actions.
"""

import os
import pandas as pd
from datetime import datetime

# 📁 Paths
REPORTS_DIR = "reports"
ANOMALY_CSV = os.path.join(REPORTS_DIR, "anomaly_report.csv")
REMEDIATION_LOG = os.path.join(REPORTS_DIR, "remediation_log.md")

# 🛡️ Rules for Remediation
def suggest_remediation(row):
    suggestions = []

    if row.get('secrets_detected', 0) > 0:
        suggestions.append("🔐 **Secrets detected** — Revoke and rotate exposed credentials immediately.")

    if row.get('critical_vulns', 0) > 0:
        suggestions.append("🛑 **Critical vulnerabilities** — Patch dependencies and rebuild the environment.")

    if row.get('suspicious_keywords_found', 0) > 0:
        suggestions.append("🕵️ **Suspicious keywords** — Review for hardcoded tokens or malicious logic.")

    if row.get('workflow_modified', 0) == 1:
        suggestions.append("⚙️ **Workflow file modified** — Check for unauthorized CI/CD changes.")

    if row.get('dockerfile_modified', 0) == 1:
        suggestions.append("🐳 **Dockerfile changed** — Ensure changes follow secure container practices.")

    if row.get('duration_ratio', 0) > 2:
        suggestions.append("⏱️ **Job duration spike** — Check for stuck steps or heavy image pulls.")

    if not suggestions:
        suggestions.append("✅ No critical issues found — No action required.")

    return suggestions

# 🚀 Run remediation analysis
if not os.path.exists(ANOMALY_CSV):
    print("❌ No anomaly_report.csv found. Skipping remediation.")
    exit(0)

df = pd.read_csv(ANOMALY_CSV)
remediation_entries = []

timestamp = datetime.utcnow().isoformat() + "Z"
print(f"🕒 Running auto-remediation at {timestamp}")

for idx, row in df.iterrows():
    reason = suggest_remediation(row)
    remediation_entries.append({
        "timestamp": timestamp,
        "row_summary": f"Row {idx + 1}",
        "recommendations": reason
    })

# 📝 Save remediation log
with open(REMEDIATION_LOG, "w", encoding="utf-8") as f:
    f.write("# 🩺 Auto-Remediation Log\n\n")
    f.write(f"**Timestamp**: `{timestamp}`\n\n")
    for entry in remediation_entries:
        f.write(f"## 📍 {entry['row_summary']}\n")
        for rec in entry['recommendations']:
            f.write(f"- {rec}\n")
        f.write("\n")

print(f"✅ Remediation suggestions saved to '{REMEDIATION_LOG}'")
