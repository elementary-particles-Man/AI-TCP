import re
import sys
import yaml

REQUIRED_KEYS = ["id", "type", "title", "description", "structure"]


def scan_warnings(path: str):
    """Scan the raw YAML text and return a list of warnings."""
    warnings: list[tuple[int, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    inside_graph = False
    graph_indent = 0
    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()

        # check for commented-out reference keys
        if re.search(r"^\s*#\s*\$?ref:", line):
            warnings.append((lineno, "参照風記述あり：手動整合性確認要"))

        # heuristic check for invalid in-line comment syntax
        if "#" in line and not stripped.startswith("#"):
            prefix = line.split("#", 1)[0]
            if not re.search(r"['\"]", prefix) and not re.search(r"[:\-\[\{,]\s*$", prefix.strip()):
                warnings.append((lineno, "無効なコメント構文の可能性"))

        # track graph_payload section
        if re.match(r"^\s*graph_payload\s*:", line):
            inside_graph = True
            graph_indent = len(line) - len(line.lstrip())
        elif inside_graph:
            curr_indent = len(line) - len(line.lstrip())
            if curr_indent <= graph_indent:
                inside_graph = False
            elif "mmd:" in line:
                warnings.append((lineno, "Mermaidブロック候補あり"))

    return warnings


def validate_file(path: str) -> int:
    warnings = scan_warnings(path)
    for lineno, msg in warnings:
        print(f"Warning: {path}:{lineno}: {msg}")

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"YAML syntax error: {e}")
            return 1

    if not isinstance(data, dict):
        print("Top-level YAML is not a dictionary.")
        return 1

    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        print(f"Missing required keys: {', '.join(missing)}")
        return 1

    print("✅ Valid structured YAML.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_structured_yaml.py <path_to_yaml>")
        sys.exit(1)

    validate_file(sys.argv[1])
