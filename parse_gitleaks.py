""""🕵️ Parse Gitleaks JSON report and extract useful features for analysis."""

import json


def parse_gitleaks_report(report_path="gitleaks_report.json"):
    """
    Parses a Gitleaks report and extracts key features such as
    secret count, file count, and AWS key presence.
    """
    try:
        with open(report_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"❌ Report file '{report_path}' not found.")
        return {}

    secrets_detected = len(data)
    secret_file_count = len(set(entry["file"] for entry in data)) if data else 0
    aws_keys_found = any("AWS" in entry.get("rule", "") for entry in data)

    result = {
        "secrets_detected": secrets_detected,
        "secret_file_count": secret_file_count,
        "aws_keys_found": aws_keys_found,
    }

    print("🔍 Parsed Gitleaks features:")
    for key, value in result.items():
        print(f"{key}: {value}")

    return result


if __name__ == "__main__":
    parse_gitleaks_report()
