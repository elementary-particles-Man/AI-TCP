🛠️ AI-TCP Tools Directory
AI-TCP Vault 構造の変換を支援する Go スクリプト群を格納しています。
YAML で記述された意図定義を HTML / Mermaid / JSON へ変換可能です。

📁 ディレクトリ構成
ディレクトリ	用途
yaml/	入力 YAML ファイル群
graph/	Mermaid 形式のグラフ出力先
html_logs/	HTML テーブル出力先
link_map/	生成されるリンクマップ JSON
tools/	本スクリプト群

📌 主なスクリプトと使用例
✅ yaml_to_mermaid.go
cd tools
go run yaml_to_mermaid.go ../yaml/intent_001.yaml ../graph/intent_001.mmd.md
✅ yaml_to_html.go
cd tools
go run yaml_to_html.go ../yaml/intent_001.yaml ../html_logs/intent_001.html
✅ gen_link_map.go
cd tools
go run gen_link_map.go ../yaml ../html_logs ../graph ../link_map/map.json
✅ gen_structure_tree.go
cd tools
go run gen_structure_tree.go .. ../../docs/poc_logs/structure_map.mmd.md
✅ check_semantics.go
cd tools
go run check_semantics.go ../yaml/intent_001.yaml
✅ enrich_yaml_semantics.go
cd tools
go run enrich_yaml_semantics.go ../yaml/intent_001.yaml ../enriched_yaml -description "Sample" -next intent_002
✅ inject_graph_labels.go
cd tools
go run inject_graph_labels.go ../yaml/intent_001.yaml ../graph/intent_001.mmd.md ../graph_labeled/intent_001.mmd.md

📝 .mmd.md ファイルは Mermaid 描画ブロックを含む Markdown 形式で出力され、Obsidian のライブプレビューで直接グラフとして描画可能です。
リンクマップや構造ツリーと合わせて、Vault全体のトレース可視化が可能になります。
✅ intent_yaml_to_mermaid.py
cd ../..
python scripts/intent_yaml_to_mermaid.py AI-TCP_Structure/yaml/intent_001.yaml AI-TCP_Structure/graph/intent_001.mmd.md
