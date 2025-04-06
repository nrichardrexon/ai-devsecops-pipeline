import json

def parse_gitleaks_report(report_path="gitleaks_report.json"):
    with open(report_path, "r") as file:
        data = json.load(file)

    result = {
        "secrets_detected": len(data),
        "secret_file_count": len(set(entry["file"] for entry in data)) if data else 0,
        "aws_keys_found": any("AWS" in entry["rule"] for entry in data)
    }

    print("Parsed Gitleaks features:")
    for k, v in result.items():
        print(f"{k}: {v}")

    return result

if __name__ == "__main__":
    parse_gitleaks_report()
