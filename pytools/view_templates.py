from __future__ import annotations

from pathlib import Path
import yaml

INPUT_FILE = Path("samples/graph_payload_templates.yaml")
OUTPUT_FILE = Path("generated_html/graph_template_view.html")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def _find_graph_structure(obj: object) -> str | None:
    """Recursively locate graph_payload.graph_structure and return its value."""
    if isinstance(obj, dict):
        if "graph_payload" in obj:
            gp = obj.get("graph_payload")
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


def _extract_mermaid(text: str | None) -> str | None:
    if not isinstance(text, str):
        return None
    if "mmd:" in text:
        return text.split("mmd:", 1)[1].strip()
    return text.strip() if text.strip() else None


def generate_html() -> None:
    try:
        data = yaml.safe_load(INPUT_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"❌ Failed to parse {INPUT_FILE}: {exc}")
        OUTPUT_FILE.write_text("", encoding="utf-8")
        return

    html: list[str] = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        "  <title>Graph Templates</title>",
        "  <script src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js\"></script>",
        "  <style>body{font-family:sans-serif;padding:1em;} pre{background:#f8f8f8;padding:1em;border-radius:8px;overflow-x:auto;} h2{margin-top:2em;}</style>",
        "</head>",
        "<body>",
        "  <h1>Graph Templates</h1>",
    ]

    if isinstance(data, dict):
        for name, content in data.items():
            html.append(f"  <h2>{name}</h2>")
            mermaid = _extract_mermaid(_find_graph_structure(content))
            if mermaid:
                html.append("  <pre><code class=\"language-mermaid\">")
                html.append(mermaid)
                html.append("  </code></pre>")
            else:
                html.append("  <!-- No Mermaid structure found -->")
    else:
        html.append("  <!-- Invalid template format -->")

    html.append("  <script>mermaid.initialize({startOnLoad:true});</script>")
    html.append("</body>")
    html.append("</html>")

    OUTPUT_FILE.write_text("\n".join(html), encoding="utf-8")
    print(f"✅ Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_html()
