from pathlib import Path
import yaml

DMC_DIR = Path("dmc_sessions")
OUTPUT_DIR = Path("generated_html/dmc_sessions")

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _find_graph_structure(obj):
    """Recursively search for graph_payload.graph_structure."""
    if isinstance(obj, dict):
        if "graph_payload" in obj:
            gp = obj["graph_payload"]
            if isinstance(gp, dict) and "graph_structure" in gp:
                return gp["graph_structure"]
        for v in obj.values():
            result = _find_graph_structure(v)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = _find_graph_structure(item)
            if result is not None:
                return result
    return None


def _extract_mermaid(code: str) -> str | None:
    if not isinstance(code, str):
        return None
    if "mmd:" not in code:
        return None
    return code.split("mmd:", 1)[1].strip()


def generate_html_from_yaml(yaml_path: Path) -> None:
    output_file = OUTPUT_DIR / f"{yaml_path.stem}.html"
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ Failed to parse {yaml_path.name}: {e}")
        # write 0 byte file for fail safe
        output_file.write_text("", encoding="utf-8")
        return

    yaml_text = yaml.dump(data, allow_unicode=True, sort_keys=False)
    mermaid = _extract_mermaid(_find_graph_structure(data))

    html_parts = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>{yaml_path.name}</title>",
        "  <script src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js\"></script>",
        "  <style>",
        "    body {font-family: sans-serif; display: flex; margin: 0; padding: 1em;}",
        "    .yaml {flex: 1; margin-right: 1em; overflow-x: auto; background:#f8f8f8; padding:1em; border-radius:8px;}",
        "    .mermaid {flex: 2;}",
        "    pre {white-space: pre-wrap;}",
        "  </style>",
        "</head>",
        "<body>"
    ]

    html_parts.append("  <div class=\"yaml\">")
    html_parts.append("    <h2>YAML</h2>")
    html_parts.append("    <pre>")
    html_parts.append(yaml_text)
    html_parts.append("    </pre>")
    html_parts.append("  </div>")

    if mermaid:
        html_parts.append("  <div class=\"mermaid\">")
        html_parts.append("    <h3>Graph構造:</h3>")
        html_parts.append("    <!-- Mermaid構造部 -->")
        html_parts.append("    <pre><code class=\"language-mermaid\">")
        html_parts.append(mermaid)
        html_parts.append("    </code></pre>")
        html_parts.append("  </div>")
    else:
        html_parts.append("  <div class=\"mermaid\"><p>Mermaid構造は含まれていません</p></div>")

    html_parts.append("  <script>mermaid.initialize({startOnLoad:true});</script>")
    html_parts.append("</body></html>")

    output_file.write_text("\n".join(html_parts), encoding="utf-8")
    print(f"✅ Generated {output_file}")


def generate_all():
    for path in sorted(DMC_DIR.glob("*.yaml")):
        generate_html_from_yaml(path)


if __name__ == "__main__":
    generate_all()
