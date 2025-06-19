import sys
import yaml

REQUIRED_KEYS = ["id", "type", "title", "description", "structure"]

def validate_file(path):
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"YAML syntax error: {e}")
            sys.exit(1)

    if not isinstance(data, dict):
        print("Top-level YAML is not a dictionary.")
        sys.exit(1)

    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        print(f"Missing required keys: {', '.join(missing)}")
        sys.exit(1)

    print("✅ Valid structured YAML.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_structured_yaml.py <path_to_yaml>")
        sys.exit(1)

    validate_file(sys.argv[1])
