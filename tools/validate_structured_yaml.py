import re
import sys
import yaml

REQUIRED_KEYS = ["id", "type", "title", "description", "structure"]


def scan_warnings(path: str):
    """Scan the raw YAML text and return a list of warnings."""
    warnings: list[tuple[int, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()

        # check for commented-out reference keys
        if stripped.startswith("#") and re.search(r"(\$ref:|#ref:)", stripped):
            warnings.append((lineno, "$ref-like comment found"))

        # heuristic check for invalid in-line comment syntax
        if "#" in line and not stripped.startswith("#"):
            prefix = line.split("#", 1)[0]
            if not re.search(r"['\"]", prefix) and not re.search(r"[:\-\[\{,]\s*$", prefix.strip()):
                warnings.append((lineno, "Possibly invalid YAML comment"))

        # detect value that starts with 'mmd:'
        if re.search(r":\s*mmd:", line) or re.match(r"^\s*-\s*mmd:", stripped):
            warnings.append((lineno, "Mermaid block candidate detected"))

    return warnings


def validate_file(path: str) -> int:
    warnings = scan_warnings(path)

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"YAML syntax error: {e}")
            for lineno, msg in warnings:
                print(f"⚠ Warning: {path}:{lineno}: {msg}")
            return 1

    if not isinstance(data, dict):
        print("Top-level YAML is not a dictionary.")
        for lineno, msg in warnings:
            print(f"⚠ Warning: {path}:{lineno}: {msg}")
        return 1

    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        print(f"Missing required keys: {', '.join(missing)}")
        for lineno, msg in warnings:
            print(f"⚠ Warning: {path}:{lineno}: {msg}")
        return 1

    print("✅ Valid YAML.")
    for lineno, msg in warnings:
        print(f"⚠ Warning: {path}:{lineno}: {msg}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_structured_yaml.py <path_to_yaml>")
        sys.exit(1)

    validate_file(sys.argv[1])
