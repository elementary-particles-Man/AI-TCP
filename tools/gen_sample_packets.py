import argparse
from pathlib import Path
import datetime
import yaml

# Base directory for sample outputs
OUTPUT_DIR = Path('samples')

# Mermaid snippets for each packet type
MERMAID_SNIPPETS = {
    'basic': 'flowchart TD\n  A[Sender] --> B[Receiver]',
    'feedback': 'flowchart TD\n  A[Sender] --> B[Receiver] -- feedback --> A',
    'dispute': 'flowchart TD\n  A --> B ? dispute ? C[Moderator]',
    'redirect': 'flowchart TD\n  A --> B:::redirect\n  B --> C[New Node]'
}


def build_packet(packet_type: str) -> dict:
    """Return a minimal packet structure for the given type."""
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    packet = {
        'graph_payload': {
            'graph_structure': f"mmd:{MERMAID_SNIPPETS[packet_type]}"
        },
        'reasoning_trace': [
            {'step': 1, 'speaker': 'A', 'text': 'Initiate'},
            {'step': 2, 'speaker': 'B', 'text': 'Ack'}
        ],
        'meta': {
            'type': packet_type,
            'generated': now
        },
        'llm_profile': {
            'id': 'demo-llm',
            'version': '0.1'
        }
    }

    if packet_type == 'feedback':
        packet['reasoning_trace'].append({'step': 3, 'speaker': 'A', 'text': 'Provide feedback'})
    elif packet_type == 'dispute':
        packet['reasoning_trace'].extend([
            {'step': 3, 'speaker': 'B', 'text': 'Raise dispute'},
            {'step': 4, 'speaker': 'C', 'text': 'Resolve'}
        ])
    elif packet_type == 'redirect':
        packet['auto_redirect'] = {
            'type': 'redirect',
            'target': 'LLM-C'
        }
        packet['reasoning_trace'].append({'step': 3, 'speaker': 'A', 'text': 'Redirect requested'})

    return packet


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate sample AI-TCP packets')
    parser.add_argument('--type', choices=['basic', 'feedback', 'dispute', 'redirect'], default='basic')
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outfile = OUTPUT_DIR / f'{args.type}_sample.yaml'

    packet = build_packet(args.type)
    yaml_text = yaml.dump(packet, allow_unicode=True, sort_keys=False)

    comment = [
        f"# Sample packet for '{args.type}' communication pattern",
        '# This file contains Mermaid graph structure and reasoning trace',
        '# for demonstration purposes.'
    ]
    outfile.write_text('\n'.join(comment) + '\n' + yaml_text, encoding='utf-8')
    print(f'Generated {outfile}')


if __name__ == '__main__':
    main()
