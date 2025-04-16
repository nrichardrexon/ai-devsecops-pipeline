import subprocess
import json

def get_outdated_packages():
    result = subprocess.run(
        ['pip', 'list', '--outdated', '--format=json'],
        stdout=subprocess.PIPE,
        check=True
    )
    output = result.stdout.decode('utf-8')
    data = json.loads(output)
    
    outdated = []
    for pkg in data:
        name = pkg['name']
        current_version = pkg['version']
        latest_version = pkg['latest_version']
        outdated.append((name, current_version, latest_version))
    
    return outdated

def update_requirements(requirements_path='requirements.txt'):
    with open(requirements_path, 'r') as file:
        lines = file.readlines()

    outdated = get_outdated_packages()
    updated_lines = []

    for line in lines:
        line_stripped = line.strip()
        for pkg, current, latest in outdated:
            if line_stripped.lower().startswith(pkg.lower()):
                print(f"🔄 Updating {pkg} from {current} to {latest}")
                line = f"{pkg}=={latest}\n"
        updated_lines.append(line)

    with open(requirements_path, 'w') as file:
        file.writelines(updated_lines)

    print("✅ requirements.txt updated.")

if __name__ == '__main__':
    print("🔍 Checking for outdated packages...")
    update_requirements()
