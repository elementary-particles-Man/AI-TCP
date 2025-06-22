from pathlib import Path
import os
import yaml

YAML_DIR = Path("structured_yaml")
STRUCTURE_DIR = Path("docs/structure_map")
OUTPUT_DIR = Path("generated_html")


def _find_mermaid_blocks(obj: object) -> list[str]:
    """Recursively collect Mermaid code blocks under graph_payload.graph_structure."""
    blocks: list[str] = []

    def _walk(node: object) -> None:
        if isinstance(node, dict):
            if "graph_payload" in node:
                gp = node.get("graph_payload")
                if isinstance(gp, dict):
                    gs = gp.get("graph_structure")
                    if isinstance(gs, str) and gs.strip().startswith("mmd:"):
                        blocks.append(gs.split("mmd:", 1)[1].strip())
            for v in node.values():
                _walk(v)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(obj)
    return blocks


def generate_html(yaml_path: Path) -> None:
    structure_path = STRUCTURE_DIR / f"{yaml_path.stem}.mmd"
    mmd_content = structure_path.read_text(encoding="utf-8") if structure_path.exists() else ""

    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        print(f"❌ Failed to parse {yaml_path}: {e}")
        return

    mermaid_blocks = _find_mermaid_blocks(data)

    rel_path = os.path.relpath(yaml_path, OUTPUT_DIR)

    html_lines = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>Structure Map: {yaml_path.name}</title>",
        "  <script type=\"module\" src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs\"></script>",
        "  <style>",
        "    body { background: #fffbe6; font-family: sans-serif; padding: 1em; }",
        "    .mermaid { background: #fff; border: 1px solid #ccc; border-radius: 8px; padding: 1em; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <h2>Structure Map: {yaml_path.name}</h2>",
        f"  <p><a href=\"{rel_path}\" target=\"_blank\">🔗 YAMLソースを見る</a></p>",
    ]

    if mmd_content:
        html_lines.append("  <div class=\"mermaid\">")
        html_lines.append(mmd_content)
        html_lines.append("  </div>")

    if mermaid_blocks:
        html_lines.append("  <h3>Mermaid構造:</h3>")
        for block in mermaid_blocks:
            html_lines.append("  <!-- Mermaid構造部 -->")
            html_lines.append("  <pre><code class=\"language-mermaid\">")
            html_lines.append(block)
            html_lines.append("  </code></pre>")

    html_lines.append("  <script>mermaid.initialize({startOnLoad:true});</script>")
    html_lines.append("</body>")
    html_lines.append("</html>")

    output_path = OUTPUT_DIR / f"structure_map_{yaml_path.stem}.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(html_lines), encoding="utf-8")
    print(f"✅ HTML structure map written to {output_path}")


def main() -> None:
    for yaml_file in sorted(YAML_DIR.glob("*.yaml")):
        generate_html(yaml_file)


if __name__ == "__main__":
    main()
