# 🛠️ AI-TCP Tools Directory

AI-TCP Vault 構造の変換を支援する Go スクリプト群を格納しています。
YAML で記述された意図定義を HTML/Mermaid/JSON へ変換できます。

## 📁 ディレクトリ構成

| ディレクトリ | 用途 |
|--------------|--------------------------------------------|
| `yaml/`      | 入力 YAML ファイル群 |
| `graph/`     | Mermaid 形式のグラフ出力先 |
| `html_logs/` | HTML テーブル出力先 |
| `link_map/`  | 生成されるリンクマップ JSON |
| `tools/`     | 本スクリプト群 |

## 📌 主なスクリプトと使用例

- **yaml_to_mermaid.go**
  ```bash
  cd tools
  go run yaml_to_mermaid.go ../yaml/intent_001.yaml ../graph/intent_001.mmd
  ```
- **yaml_to_html.go**
  ```bash
  cd tools
  go run yaml_to_html.go ../yaml/intent_001.yaml ../html_logs/intent_001.html
  ```
- **gen_link_map.go**
  ```bash
  cd tools
  go run gen_link_map.go ../yaml ../html_logs ../graph ../link_map/map.json
  ```
- **check_semantics.go**
  ```bash
  cd tools
  go run check_semantics.go ../yaml/intent_001.yaml
  ```
