

import os
from pathlib import Path

def get_file_structure(startpath):
    structure = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        structure.append(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            structure.append(f'{subindent}{f}')
    return "\n".join(structure)

if __name__ == "__main__":
    repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd()))
    file_structure = get_file_structure(str(repo_root))
    with open(repo_root / "temp_file_structure.txt", "w", encoding="utf-8") as f:
        f.write(file_structure)

