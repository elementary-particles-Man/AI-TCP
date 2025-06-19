import yaml
import os
from pathlib import Path

def traverse(node, parent, lines, prefix=""):
    if isinstance(node, dict):
        for key, value in node.items():
            node_id = f"{prefix}{key}"
            label = f"{key} : dict" if isinstance(value, dict) else f"{key}"
            lines.append(f"  {parent} --> {node_id}[\"{label}\"]")
            traverse(value, node_id, lines, prefix=node_id + "_")
    elif isinstance(node, list):
        lines.append(f"  {parent} --> {parent}_item[\"- item\"]")
    else:
        typename = type(node).__name__
        lines.append(f"  {parent} --> leaf_{prefix}[\"{node} : {typename}\"]")

# 入力と出力の設定
yaml_path = "structured_yaml/master_schema_v1.yaml"
output_dir = Path("docs/structure_map")
output_dir.mkdir(parents=True, exist_ok=True)
mmd_path = output_dir / "master_schema.mmd"

# YAML読み取り
with open(yaml_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

root = data.get("structure", {})

lines = ["graph TD", "  root[\"structure\"]"]
traverse(root, "root", lines)

with open(mmd_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Mermaid diagram written to {mmd_path}")
