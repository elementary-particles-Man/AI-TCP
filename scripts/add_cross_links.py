import os
import re
from pathlib import Path

# directories
docs_dir = Path('docs/rfc_drafts')
yaml_dir = Path('structured_yaml/validated_yaml')

yaml_files = {p.name for p in yaml_dir.iterdir() if p.suffix == '.yaml'}
# Add README.yaml.md not as cross target? We'll treat .yaml and .yaml.md as cross
yaml_files |= {p.name for p in yaml_dir.iterdir() if p.suffix == '.md' and 'yaml' in p.name}

doc_files = {p.name for p in docs_dir.iterdir() if p.suffix == '.md'}

# function to create relative link from file to target

def rel_link(src: Path, target: Path) -> str:
    return os.path.relpath(target, src.parent)

# pattern to detect file references not already in markdown link
file_pattern = re.compile(r'(\b[A-Za-z0-9_]+\.(?:yaml(?:\.md)?|md))')

changed = False

# Process RFC drafts -> link to YAML
for path in docs_dir.glob('*.md'):
    text = path.read_text(encoding='utf-8')
    matches = list(file_pattern.finditer(text))
    new_text = text
    offset = 0
    for m in matches:
        fname = m.group(1)
        if fname in yaml_files:
            # check if already linked
            start = m.start(1) + offset
            end = m.end(1) + offset
            if new_text[max(0, start-1)] == '[':
                continue
            link = f'[{fname} を参照]({rel_link(path, yaml_dir / fname)})'
            new_text = new_text[:start] + link + new_text[end:]
            offset += len(link) - len(fname)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        changed = True

# Process YAML docs -> link to RFC drafts
for path in yaml_dir.glob('*'):
    if path.suffix not in ('.yaml', '.md'):
        continue
    text = path.read_text(encoding='utf-8')
    matches = list(file_pattern.finditer(text))
    new_text = text
    offset = 0
    for m in matches:
        fname = m.group(1)
        if fname in doc_files:
            start = m.start(1) + offset
            end = m.end(1) + offset
            if new_text[max(0, start-1)] == '[':
                continue
            link = f'[{fname} を参照]({rel_link(path, docs_dir / fname)})'
            new_text = new_text[:start] + link + new_text[end:]
            offset += len(link) - len(fname)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        changed = True

if not changed:
    print('No changes made.')
