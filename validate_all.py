import subprocess
import os

print("YAML Validation Start...")

errors = []

# --- Validate DMC YAMLs ---
print("\nValidating DMC YAMLs...")
dmc_dir = "dmc_sessions"
dmc_validator = "scripts/validate_yaml_dmc.py" # Correct path

if not os.path.exists(dmc_validator):
    print(f"ERROR: Validator script not found at {dmc_validator}")
    exit(1)

for root, dirs, files in os.walk(dmc_dir):
    for file in files:
        if file.endswith((".yaml", ".yml")):
            path = os.path.join(root, file)
            print(f"Checking: {path}")
            result = subprocess.run(
                ["python", dmc_validator, path],
                capture_output=True, text=True, encoding='utf-8', errors='replace'
            )
            if result.returncode != 0:
                errors.append((path, result.stdout.strip() + "\n" + result.stderr.strip()))

# --- Validate structured YAMLs ---
print("\nValidating Structured YAMLs...")
yaml_dir = "structured_yaml"
structured_validator = "pytools/validate_structured_yaml.py" # Correct path

if not os.path.exists(structured_validator):
    print(f"ERROR: Validator script not found at {structured_validator}")
    exit(1)

for root, dirs, files in os.walk(yaml_dir):
    for file in files:
        if file.endswith((".yaml", ".yml")):
            path = os.path.join(root, file)
            print(f"Checking: {path}")
            result = subprocess.run(
                ["python", structured_validator, path],
                capture_output=True, text=True, encoding='utf-8', errors='replace'
            )
            if result.returncode != 0:
                errors.append((path, result.stdout.strip() + "\n" + result.stderr.strip()))

# --- Summary ---
print("\n--- Validation Summary ---")
if errors:
    print("Validation failed for the following files:")
    for fname, msg in errors:
        print(f"[-] ERROR in {fname}:\n{msg}\n")
    exit(1)
else:
    print("[+] All YAML files are valid.")