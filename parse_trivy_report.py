import json
import pandas as pd
from datetime import datetime

# Load the JSON report
with open("trivy_report.json", "r") as file:
    data = json.load(file)

# Prepare dataset
records = []
timestamp = datetime.now().isoformat()

for result in data.get("Results", []):
    file_path = result.get("Target", "")
    vulns = result.get("Vulnerabilities", [])
    total = len(vulns)
    critical = sum(1 for v in vulns if v.get("Severity") == "CRITICAL")

    record = {
        "timestamp": timestamp,
        "file_path": file_path,
        "vulnerabilities_total": total,
        "critical_vulns": critical,
        "new_vulnerabilities": 0,  # Placeholder, for future comparison
        "anomaly": 1 if critical > 0 or total > 5 else 0,
    }
    records.append(record)

# Save to CSV
df = pd.DataFrame(records)
df.to_csv("vuln_dataset.csv", index=False)

print("✅ Dataset saved to vuln_dataset.csv")
