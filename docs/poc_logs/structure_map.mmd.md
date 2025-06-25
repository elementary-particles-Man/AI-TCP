```mermaid
graph TD
    graph["graph/"]
    graph__gitkeep[".gitkeep"]
    graph_intent_001_mmd_md["Mermaid: intent_001.mmd.md"]
    html_logs["html_logs/"]
    html_logs_intent_001_html["intent_001.html"]
    html_logs_intent_003_html["intent_003.html"]
    link_map["link_map/"]
    link_map__gitkeep[".gitkeep"]
    link_map_json["link_map.json"]
    mermaid["mermaid/"]
    mermaid_intent_001_mmd_md["Mermaid: intent_001.mmd.md"]
    mermaid_intent_002_mmd_md["Mermaid: intent_002.mmd.md"]
    root[".."]
    tools["tools/"]
    tools_README_md["MD: README.md"]
    tools_gen_link_map_go["gen_link_map.go"]
    tools_gen_structure_tree_go["gen_structure_tree.go"]
    tools_go_mod["go.mod"]
    tools_go_sum["go.sum"]
    tools_yaml_to_html_go["yaml_to_html.go"]
    tools_yaml_to_mermaid_go["yaml_to_mermaid.go"]
    yaml["yaml/"]
    yaml_intent_001_yaml["YAML: intent_001.yaml"]
    yaml_intent_002_yaml["YAML: intent_002.yaml"]
    yaml_intent_003_yaml["YAML: intent_003.yaml"]
    root --> graph
    graph --> graph__gitkeep
    graph --> graph_intent_001_mmd_md
    root --> html_logs
    html_logs --> html_logs_intent_001_html
    html_logs --> html_logs_intent_003_html
    root --> link_map
    root --> link_map_json
    link_map --> link_map__gitkeep
    root --> mermaid
    mermaid --> mermaid_intent_001_mmd_md
    mermaid --> mermaid_intent_002_mmd_md
    root --> tools
    tools --> tools_README_md
    tools --> tools_gen_link_map_go
    tools --> tools_gen_structure_tree_go
    tools --> tools_go_mod
    tools --> tools_go_sum
    tools --> tools_yaml_to_html_go
    tools --> tools_yaml_to_mermaid_go
    root --> yaml
    yaml --> yaml_intent_001_yaml
    yaml --> yaml_intent_002_yaml
    yaml --> yaml_intent_003_yaml
```
