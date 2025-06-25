from pathlib import Path
import os
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
import html

DMC_DIR = Path("dmc_sessions")
OUTPUT_DIR = Path("generated_html/dmc_sessions")
TEMPLATE_DIR = Path("html_templates")
TEMPLATE_FILE = "dmc_session_template.html"

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


def _extract_mermaid(code: str | None) -> str | None:
    if not isinstance(code, str):
        return None
    if "mmd:" not in code:
        return None
    return code.split("mmd:", 1)[1].strip()


def _to_html_tree(obj) -> str:
    """Convert a Python object to nested <ul> HTML."""
    if isinstance(obj, dict):
        items = [f"<li><strong>{html.escape(str(k))}:</strong> {_to_html_tree(v)}</li>" for k, v in obj.items()]
        return "<ul>" + "".join(items) + "</ul>"
    elif isinstance(obj, list):
        items = [f"<li>{_to_html_tree(v)}</li>" for v in obj]
        return "<ul>" + "".join(items) + "</ul>"
    else:
        return html.escape(str(obj))


def generate_html_from_yaml(yaml_path: Path, template) -> None:
    output_file = OUTPUT_DIR / f"{yaml_path.stem}.html"
    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        print(f"❌ Failed to parse {yaml_path.name}: {e}")
        output_file.write_text("", encoding="utf-8")
        return

    mermaid = _extract_mermaid(_find_graph_structure(data))
    tree_html = _to_html_tree(data)
    rel_path = os.path.relpath(yaml_path, OUTPUT_DIR)

    html_text = template.render(
        title=yaml_path.name,
        yaml_tree=tree_html,
        mermaid=mermaid,
        yaml_rel_path=rel_path,
    )
    output_file.write_text(html_text, encoding="utf-8")
    print(f"✅ Generated {output_file}")


def generate_all():
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html"]))
    template = env.get_template(TEMPLATE_FILE)
    for path in sorted(DMC_DIR.glob("*.yaml")):
        generate_html_from_yaml(path, template)


if __name__ == "__main__":
    generate_all()
