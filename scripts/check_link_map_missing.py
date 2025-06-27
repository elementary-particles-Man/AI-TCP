import json
import os
from typing import Dict, Any


def main():
    input_path = 'AI-TCP_Structure/link_map.json'
    missing_json = 'missing_files.json'
    summary_txt = 'summary.txt'

    with open(input_path, 'r', encoding='utf-8') as f:
        data: Dict[str, Any] = json.load(f)

    missing_data: Dict[str, Any] = {}
    total_missing = 0
    missing_mmd = 0
    missing_html = 0

    for key, entry in data.items():
        if entry.get('missing') is True:
            missing_entry = {}
            for field in ('mermaid', 'html'):
                path = entry.get(field)
                if path and not os.path.exists(path):
                    missing_entry[field] = path
                    total_missing += 1
                    if path.endswith('.mmd.md'):
                        missing_mmd += 1
                    elif path.endswith('.html'):
                        missing_html += 1
            if missing_entry:
                missing_data[key] = missing_entry

    with open(missing_json, 'w', encoding='utf-8') as f:
        json.dump(missing_data, f, ensure_ascii=False, indent=2)

    with open(summary_txt, 'w', encoding='utf-8') as f:
        f.write(f'Total missing files: {total_missing}\n')
        f.write(f'Missing .mmd.md files: {missing_mmd}\n')
        f.write(f'Missing .html files: {missing_html}\n')


if __name__ == '__main__':
    main()
