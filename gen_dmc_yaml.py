import re
from pathlib import Path
import yaml
from bs4 import BeautifulSoup

INPUT_HTML = Path('generated_html/DMC_20250618.html')
OUTPUT_YAML = Path('reverse_generated.yaml')

def parse_meta(container):
    meta = {}
    meta_div = container.find('div', class_='meta-info')
    if not meta_div:
        return meta
    titles = meta_div.find_all('span', class_='field-title')
    values = meta_div.find_all('span', class_='field-value')
    for t, v in zip(titles, values):
        key = t.get_text(strip=True)
        val = v.get_text(strip=True)
        if 'セッション' in key:
            meta['session_id'] = val
        elif '作成' in key:
            meta['created'] = val
        elif '目的' in key:
            meta['purpose'] = val
    return meta

def parse_packets(container):
    phases = []
    current = None
    for elem in container.find_all(['h2', 'details'], recursive=False):
        if elem.name == 'h2':
            text = elem.get_text(strip=True)
            m = re.match(r'Phase\s*(\d+)[:：]\s*(.*)', text)
            if m:
                phase_id = f'dmc_phase{m.group(1)}'
                phase_name = m.group(2)
                current = {'id': phase_id, 'name': phase_name, 'packets': []}
                phases.append(current)
        elif elem.name == 'details' and current is not None:
            summary = elem.find('summary')
            pkt_id = title = ''
            if summary:
                stext = summary.get_text(strip=True)
                m = re.match(r'Packet\s*(\S+):\s*(.*)', stext)
                if m:
                    pkt_id = m.group(1)
                    title = m.group(2)
                else:
                    pkt_id = stext
            pkt = {'packet_id': pkt_id, 'title': title}
            payload_div = elem.find('div', class_='packet-content')
            if payload_div:
                all_vals = payload_div.find_all('div', class_='field-value')
                for val in all_vals:
                    text = val.get_text(" ", strip=True)
                    if 'Intent:' in text and 'Justification:' in text:
                        intent_match = re.search(r'Intent:\s*(.*?)\s*Justification:', text)
                        just_match = re.search(r'Justification:\s*(.*)', text)
                        if intent_match:
                            pkt['intent'] = intent_match.group(1)
                        if just_match:
                            pkt['justification'] = just_match.group(1)
                    elif val.code:
                        pkt['trace_link'] = val.code.get_text(strip=True)
            current['packets'].append(pkt)
    return phases

def main():
    html = INPUT_HTML.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find('div', class_='container')
    if not container:
        raise SystemExit('container not found')
    meta = parse_meta(container)
    phases = parse_packets(container)
    data = {
        'session_id': meta.get('session_id'),
        'created': meta.get('created'),
        'purpose': meta.get('purpose'),
        'phases': phases,
    }
    OUTPUT_YAML.write_text(yaml.dump(data, allow_unicode=True), encoding='utf-8')
    print(f'YAML written to {OUTPUT_YAML}')

if __name__ == '__main__':
    main()
