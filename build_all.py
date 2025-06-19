#!/usr/bin/env python
# build_all.py

import subprocess
import datetime

print("\n🛠 AI-TCP Build System Starting...\n")

# DMC session HTMLs
dmc_result = subprocess.run(["python", "tools/gen_dmc_html.py"])
if dmc_result.returncode == 0:
    print("📄 generated_html/index_dmc_sessions.html generated\n")

# Structured YAML HTML
structured_result = subprocess.run(["python", "tools/gen_structured_yaml_html.py"])
if structured_result.returncode == 0:
    print("✅ HTML generated at generated_html/structured_yaml_index.html\n")

# Structure Map HTML
structure_map_result = subprocess.run(["python", "tools/gen_structure_html.py"])
if structure_map_result.returncode == 0:
    print("✅ HTML generated at generated_html/structure_map_master_schema.html\n")

print(f"✅ Build completed at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
