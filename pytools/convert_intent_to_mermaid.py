import yaml
import sys

def yaml_to_mermaid(yaml_file):
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)

    mermaid_string = "mmd:flowchart LR<br>"

    # Process components (nodes)
    for i, component in enumerate(data.get('components', [])):
        node_id = component.get('id')
        node_name = component.get('name', '')
        node_label = f"{node_name}_{i+1}"
        mermaid_string += f"    {node_id}[{node_label}]<br>"

    # Process connections (edges)
    for connection in data.get('connections', []):
        from_node = connection.get('from')
        to_node = connection.get('to')
        mermaid_string += f"    {from_node} --> {to_node}<br>"

    return mermaid_string

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_intent_to_mermaid.py <path_to_yaml>")
        sys.exit(1)

    mermaid_output = yaml_to_mermaid(sys.argv[1])
    print(mermaid_output)
