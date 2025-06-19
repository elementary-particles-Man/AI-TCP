from pathlib import Path

mmd_path = Path("docs/structure_map/master_schema.mmd")
html_path = Path("generated_html/structure_map_master_schema.html")

if not mmd_path.exists():
    print(f"❌ Mermaid source not found: {mmd_path}")
    exit(1)

mmd_content = mmd_path.read_text(encoding="utf-8")

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI-TCP Structure Map</title>
  <script type="module" src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"></script>
  <style>
    body {{ background: #fffbe6; font-family: sans-serif; padding: 1em; }}
    .mermaid {{ background: #fff; border: 1px solid #ccc; border-radius: 8px; padding: 1em; }}
  </style>
</head>
<body>
  <h2>Structure Map: master_schema_v1.yaml</h2>
  <div class="mermaid">
{mmd_content}
  </div>
</body>
</html>
"""

html_path.parent.mkdir(parents=True, exist_ok=True)
html_path.write_text(html_template, encoding="utf-8")
print(f"✅ HTML structure map written to {html_path}")
