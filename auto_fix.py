""""📦 Script to auto-update outdated Python packages in requirements.txt"""

import subprocess  # nosec B404 - subprocess used safely with constant arguments
import json
import shutil
import sys


def get_outdated_packages():
    """Returns a list of tuples (name, current_version, latest_version) for outdated packages."""
    pip_path = shutil.which("pip")
    if pip_path is None:
        print("❌ pip not found in system PATH.", file=sys.stderr)
        sys.exit(1)

    try:
        # subprocess used with static, safe arguments and no shell=True
        result = subprocess.run(  # nosec B603
            [pip_path, 'list', '--outdated', '--format=json'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        output = result.stdout.decode('utf-8')
        data = json.loads(output)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching outdated packages: {e}", file=sys.stderr)
        sys.exit(1)

    outdated = []
    for pkg in data:
        name = pkg['name']
        current_version = pkg['version']
        latest_version = pkg['latest_version']
        outdated.append((name, current_version, latest_version))

    return outdated


def update_requirements(requirements_path='requirements.txt'):
    """
    Updates the given requirements.txt file with latest versions
    for all outdated packages listed.
    """
    try:
        with open(requirements_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"❌ {requirements_path} not found.", file=sys.stderr)
        sys.exit(1)

    outdated = get_outdated_packages()
    updated_lines = []

    for line in lines:
        line_stripped = line.strip()
        for pkg, current, latest in outdated:
            if line_stripped.lower().startswith(pkg.lower()):
                print(f"🔄 Updating {pkg} from {current} to {latest}")
                line = f"{pkg}=={latest}\n"
                break
        updated_lines.append(line)

    with open(requirements_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)

    print("✅ requirements.txt updated.")


if __name__ == '__main__':
    print("🔍 Checking for outdated packages...")
    update_requirements()
