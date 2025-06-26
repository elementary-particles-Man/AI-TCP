import argparse
import os
import re
from bs4 import BeautifulSoup
import yaml


def extract_intent_id(path, soup):
    # Try to extract from HTML title or id
    if soup.title and soup.title.string:
        m = re.search(r"intent[_\s-]*(\w+)", soup.title.string, re.IGNORECASE)
        if m:
            return m.group(1)
    # Fallback to element with id or class
    tag = soup.find(id="intent-id") or soup.find(class_="intent-id")
    if tag:
        return tag.get_text(strip=True)
    # Fallback to filename
    basename = os.path.basename(path)
    m = re.search(r"intent[_-]?(\w+)", basename, re.IGNORECASE)
    if m:
        return m.group(1)
    raise ValueError("Unable to determine intent id")


def extract_section_text(soup, name):
    # Look for id or class
    tag = soup.find(id=name) or soup.find(class_=name)
    if tag:
        return tag.get_text(strip=True)
    # Look for header containing the name
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        if name.lower() in header.get_text(strip=True).lower():
            nxt = header.find_next_sibling()
            while nxt and nxt.name not in ['p', 'div']:
                nxt = nxt.find_next_sibling()
            if nxt:
                return nxt.get_text(strip=True)
    return ''


def parse_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    intent_id = extract_intent_id(path, soup)
    description = extract_section_text(soup, 'description')
    source_text = extract_section_text(soup, 'source')
    process_text = extract_section_text(soup, 'process')
    response_text = extract_section_text(soup, 'response')

    return {
        'intent': {
            'id': intent_id,
            'description': description,
            'source': {'example': source_text},
            'process': {'description': process_text},
            'response': {'text': response_text},
        }
    }


def main():
    parser = argparse.ArgumentParser(description='Convert intent HTML to YAML payload')
    parser.add_argument('html_file', help='Path to intent_XXX_output.html')
    parser.add_argument('-o', '--output', help='Output YAML path (default: payload_<id>.yaml)')
    args = parser.parse_args()

    data = parse_html(args.html_file)

    out_path = args.output
    if not out_path:
        out_dir = os.path.dirname(args.html_file)
        intent_id = data['intent']['id']
        out_path = os.path.join(out_dir, f'payload_{intent_id}.yaml')

    with open(out_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    print(f"YAML saved to {out_path}")


if __name__ == '__main__':
    main()
