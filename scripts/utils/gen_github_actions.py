# scripts/utils/gen_github_actions.py
import os
import sys


def main():
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        print("REPO_ROOT environment variable not set")
        sys.exit(1)
    os.chdir(repo_root)

    workflow_dir = os.path.join(repo_root, ".github", "workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    path = os.path.join(workflow_dir, "validate.yml")

    content = """name: Validate\n"""
    content += "on:\n  push:\n    branches:\n      - main\n\n"
    content += "jobs:\n  validate:\n    runs-on: ubuntu-latest\n    steps:\n"
    content += "      - uses: actions/checkout@v4\n"
    content += "      - uses: actions/setup-python@v5\n        with:\n          python-version: '3.7'\n"
    content += "      - name: Install dependencies\n        run: pip install pytest\n"
    content += "      - name: Run tests\n        run: |\n          mkdir -p test-results\n          pytest -q --junitxml=test-results/results.xml\n"
    content += "      - name: Upload Artifacts\n        uses: actions/upload-artifact@v4\n        with:\n          name: test-results\n          path: test-results\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated", path)


if __name__ == "__main__":
    main()
