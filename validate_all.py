import subprocess
import os

print("\n🧪 YAML Validation Start...")

errors = []

# Validate DMC YAMLs
print("\n🔎 Validating DMC YAMLs...")
dmc_dir = "dmc_sessions"
for file in os.listdir(dmc_dir):
    if file.endswith(".yaml"):
        path = os.path.join(dmc_dir, file)
        result = subprocess.run(["python", "tools/validate_dmc_yaml.py", path], capture_output=True, text=True)
        if result.returncode != 0:
            errors.append((file, result.stdout.strip()))

# Validate structured YAMLs
print("\n🔎 Validating Structured YAMLs...")
yaml_dir = "structured_yaml"
for file in os.listdir(yaml_dir):
    if file.endswith(".yaml"):
        path = os.path.join(yaml_dir, file)
        result = subprocess.run(["python", "tools/validate_structured_yaml.py", path], capture_output=True, text=True)
        if result.returncode != 0:
            errors.append((file, result.stdout.strip()))

# Summary
print("\n📋 Validation Summary:")
if errors:
    for fname, msg in errors:
        print(f"❌ {fname}: {msg}")
    exit(1)
else:
    print("✅ All YAML files are valid.")
