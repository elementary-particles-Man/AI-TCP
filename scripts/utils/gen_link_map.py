# scripts/utils/gen_link_map.py
import os
import json
from pathlib import Path


def main() -> None:
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        return
    os.chdir(repo_root)

    docs_dir = Path("docs")
    mapping = {}
    for md in docs_dir.rglob("*.md"):
        slug = md.stem
        mapping[slug] = md.as_posix()

    out_path = Path("link_map.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    print(f"Generated {out_path}")


if __name__ == "__main__":
    main()
