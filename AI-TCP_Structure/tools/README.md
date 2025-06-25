# 🛠️ AI-TCP Tools Directory

このディレクトリは、**AI-TCP Vault構造を支援するツールスクリプト群**を格納する中核領域です。  
意図（YAML）→ 構造（Mermaid）→ 可視ログ（HTML）といった変換フローを自動化します。

---

## 📁 ディレクトリ構成と用途

| ディレクトリ         | 用途                               |
|----------------------|------------------------------------|
| `yaml/`              | YAML形式の意図定義ファイル群         |
| `mermaid/`           | Mermaid構文出力ファイル（*.mmd.md） |
| `html_logs/`         | 意図トレースのHTML表形式ログ         |
| `tools/`             | 変換スクリプト・リンク生成スクリプト |
| `link_map.json`      | YAML・Mermaid・HTMLの対応関係マップ  |

---

## 📌 このディレクトリの主なスクリプト

### 1. `yaml_to_mermaid.go`
YAMLファイルを読み込み、対応するMermaid構造図を出力します。

- **依存**: `gopkg.in/yaml.v3`
- **実行方法**:
  ```bash
  cd tools/
  go run yaml_to_mermaid.go ../yaml/intent_001.yaml
