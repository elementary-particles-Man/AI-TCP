import os
import re

HEADER_PATTERN = re.compile(r'^(#{1,4})\s*(.+)$')


def slugify(title: str) -> str:
    """Generate GitHub-style anchor from title."""
    anchor = title.strip().lower()
    anchor = re.sub(r'[^a-z0-9\s-]', '', anchor)
    anchor = anchor.replace(' ', '-')
    anchor = re.sub(r'-+', '-', anchor)
    return anchor


def extract_headers(lines):
    headers = []
    for line in lines:
        m = HEADER_PATTERN.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            headers.append((level, title))
    return headers


def build_toc(headers):
    toc_lines = []
    for level, title in headers:
        anchor = slugify(title)
        indent = '  ' * (level - 1)
        toc_lines.append(f"{indent}- [{title}](#{anchor})")
    toc = ["<!-- TOC START -->"] + toc_lines + ["<!-- TOC END -->", ""]
    return '\n'.join(toc)


def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Remove existing TOC block at start
    if lines and lines[0].strip() == "<!-- TOC START -->":
        end_idx = 0
        for i, line in enumerate(lines):
            if line.strip() == "<!-- TOC END -->":
                end_idx = i
                break
        if end_idx:
            lines = lines[end_idx + 1:]

    headers = extract_headers(lines)
    toc = build_toc(headers)

    # Backup original file
    backup_path = path + '.bak'
    with open(backup_path, 'w', encoding='utf-8') as bf:
        bf.writelines(lines)

    # Write new file with TOC
    with open(path, 'w', encoding='utf-8') as f:
        f.write(toc)
        f.writelines(lines)


def main():
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    for root, _, files in os.walk(docs_dir):
        for name in files:
            if name.endswith('.md'):
                update_file(os.path.join(root, name))


if __name__ == '__main__':
    main()
