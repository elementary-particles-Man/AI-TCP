import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as e:
    yaml = None


def load_yaml(path: Path):
    if yaml is None:
        raise RuntimeError("PyYAML is required but not installed: %s" % path)
    with path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def parse_markdown_table(md_path: Path):
    rows = []
    with md_path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('|') and '|' in line[1:]:
                parts = [p.strip() for p in line.strip('|').split('|')]
                if len(parts) >= 4 and parts[0] != ':' and not parts[0].startswith('--'):
                    intent, trace_value, summary, _ = parts[:4]
                    rows.append({
                        'intent': intent,
                        'trace_value': trace_value,
                        'summary': summary,
                    })
    return rows


def verify(mapping_rows, yaml_data):
    phases = yaml_data.get('session_trace', {}).get('phases', [])
    errors = []

    phase_ids = [p.get('id') for p in phases]

    for idx, row in enumerate(mapping_rows):
        m = re.match(r'dmc_phase(\d+)', row['trace_value'])
        if not m:
            errors.append(f"Row {idx+1}: invalid trace value format '{row['trace_value']}'")
            continue
        phase_num_from_trace = int(m.group(1))

        m2 = re.search(r'Phase\s*(\d+)', row['summary'])
        if not m2:
            errors.append(f"Row {idx+1}: could not find phase number in summary '{row['summary']}'")
            continue
        phase_num_from_summary = int(m2.group(1))

        if phase_num_from_trace != phase_num_from_summary:
            errors.append(
                f"Row {idx+1}: phase number mismatch between trace value ({phase_num_from_trace}) and summary ({phase_num_from_summary})")
            continue

        if phase_num_from_trace > len(phases):
            errors.append(f"Row {idx+1}: phase {phase_num_from_trace} not present in YAML")
            continue

        phase = phases[phase_num_from_trace - 1]
        phase_id = phase.get('id')
        if phase_id != f'dmc_phase{phase_num_from_trace}':
            errors.append(
                f"Row {idx+1}: phase id mismatch in YAML (expected dmc_phase{phase_num_from_trace}, got {phase_id})")

        # verify trace link presence
        trace_links = [pkt.get('trace_link') for pkt in phase.get('packets', [])]
        if row['trace_value'] not in trace_links:
            errors.append(
                f"Row {idx+1}: trace value '{row['trace_value']}' not found in YAML phase {phase_num_from_trace}")

        # basic title keyword check
        phase_name = phase.get('name', '')
        if phase_name and phase_name.split('、')[0] not in row['intent']:
            if phase_name not in row['intent']:
                errors.append(
                    f"Row {idx+1}: phase title keyword '{phase_name}' not reflected in intent '{row['intent']}'")

    return errors


def main():
    md_path = Path('dmc_sessions/analysis/trace_link_summary_mapping.md')
    yaml_path = Path('structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml')

    try:
        yaml_data = load_yaml(yaml_path)
    except Exception as e:
        print(f"Failed to load YAML: {e}")
        sys.exit(1)

    mapping_rows = parse_markdown_table(md_path)

    errors = verify(mapping_rows, yaml_data)

    if errors:
        print("Validation errors detected:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("All mappings are valid.")


if __name__ == '__main__':
    main()
