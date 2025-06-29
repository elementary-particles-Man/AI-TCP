# scripts/utils/gen_docs.py
import os
import sys


def main():
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        sys.exit(1)
    os.chdir(repo_root)

    docs_dir = os.path.join(repo_root, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    docs = {
        "AI-TCP_FlagWorkflow.md": "# AI-TCP FlagWorkflow\n\n## Overview\n",
        "CLI_Spec.md": "# CLI Spec\n\n## Commands\n",
    }
    for fname, content in docs.items():
        path = os.path.join(docs_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Generated", path)


if __name__ == "__main__":
    main()
