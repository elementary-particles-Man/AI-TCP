# 🛠️ AI-TCP Tools Directory

This directory contains utility scripts implemented in Python and Go, utilized across various phases of the AI-TCP project. These tools automate YAML structure conversion, Mermaid graph generation, HTML rendering, and various validations, supporting efficient project progress.

## 📁 Directory Structure

*   `pytools/`: Python scripts (YAML processing, HTML generation, graph operations, etc.)
*   `scripts/`: Python and JavaScript scripts (Mermaid conversion, MathJax conversion, etc.)
*   `AI-TCP_Structure/tools/`: Go scripts (YAML processing, link map generation, etc.)

## 📌 Key Scripts and Usage

| Script File | Language | Purpose & Overview | Main Input File Types | Main Output File Types | Usage Example (CLI) |
| :---------- | :------- | :----------------- | :-------------------- | :--------------------- | :------------------ |
| `pytools/gen_structure_map_from_yaml.py` | Python | Generates Mermaid structure diagrams from YAML schemas to visualize directory structures. | `.yaml` (schema) | `.mmd` | `python pytools/gen_structure_map_from_yaml.py structured_yaml/master_schema_v1.yaml` |
| `pytools/gen_structured_yaml_html.py` | Python | Converts structured YAML files into an HTML index page. | `structured_yaml/*.yaml` | `.html` | `python pytools/gen_structured_yaml_html.py` |
| `pytools/gen_dmc_html.py` | Python | Converts DMC session YAML traces into human-readable HTML reports. | `.yaml` (DMC trace) | `.html` | `python pytools/gen_dmc_html.py --input dmc_sessions/gemini_dmc_session_20250618.md --output generated_html/DMC_20250618.html` |
| `pytools/reverse_mermaid_parser.py` | Python | Extracts Mermaid code from HTML or .mmd files and formats it into YAML snippets. | `.html`, `.mmd` | YAML snippet | `python pytools/reverse_mermaid_parser.py --input generated_html/structure_map_master_schema.html` |
| `pytools/validate_mermaid_blocks.py` | Python | Validates the syntax of Mermaid code blocks within YAML files. | `.yaml` | Console output | `python pytools/validate_mermaid_blocks.py --fix structured_yaml/master_schema_v1.yaml` |
| `AI-TCP_Structure/tools/yaml_to_mermaid.go` | Go | Converts Intent YAML to Mermaid graph TD diagrams. | Intent `.yaml` | `.mmd.md` | `go run AI-TCP_Structure/tools/yaml_to_mermaid.go AI-TCP_Structure/yaml/intent_001.yaml AI-TCP_Structure/graph/intent_001.mmd.md` |
| `AI-TCP_Structure/tools/gen_link_map.go` | Go | Generates a JSON link map between YAML, Mermaid, and HTML files. | `.yaml`, `.mmd`, `.html` | `.json` | `go run AI-TCP_Structure/tools/gen_link_map.go AI-TCP_Structure/yaml/ AI-TCP_Structure/html_logs/ AI-TCP_Structure/graph/ AI-TCP_Structure/link_map.json` |
| `scripts/convert_md_math_to_mathjax.py` | Python | Converts LaTeX math equations within Markdown to MathJax compatible format. | `.md` | `.md` | `python scripts/convert_md_math_to_mathjax.py docs/rfc_drafts/rfc_lsc_001.md` |
| `pytools/chatlog_to_html.py` | Python | Converts Markdown-formatted chat logs into color-coded HTML viewers. | `.md` (chat log) | `.html` | `python pytools/chatlog_to_html.py samples/chatlog_sample.md generated_html/chatlog_view.html --count-tokens` |

## ⚠️ Notes and Future Expansion

*   **Go Version**: Current Go scripts are confirmed to work with Go 1.23 or later.
*   **Python Version**: Python 3.7 or later is recommended.
*   **External Dependencies**: Python scripts depend on libraries such as `requests`, `PyYAML`, `BeautifulSoup4`, `Jinja2`, `jsonschema`, `markdown2` (mistune). These are listed in `requirements.txt`.
*   **Compatibility**: Each tool is designed with compatibility for Obsidian and GitHub rendering in mind.
*   **Automation**: Currently, the focus is on manual CLI tools, but future considerations include integration into CI/CD pipelines and more advanced automation layers (e.g., direct integration with LM Studio API).
*   **Error Handling**: Scripts include basic error handling, but further robustness is required for production use.

---

# 🛠️ AI-TCP ツールディレクトリ

本ディレクトリには、AI-TCPプロジェクトの様々なフェーズで活用される、PythonおよびGoで実装されたユーティリティスクリプト群が格納されています。これらのツールは、YAML構造の変換、Mermaidグラフの生成、HTMLレンダリング、および各種検証を自動化し、プロジェクトの効率的な進行を支援します。

## 📁 ディレクトリ構成

*   `pytools/`: Python製スクリプト（YAML処理、HTML生成、グラフ操作など）
*   `scripts/`: PythonおよびJavaScript製スクリプト（Mermaid変換、MathJax変換など）
*   `AI-TCP_Structure/tools/`: Go製スクリプト（YAML処理、リンクマップ生成など）

## 📌 主要スクリプトと使用方法

| スクリプトファイル | 言語 | 目的と概要 | 主な入力ファイル形式 | 主な出力ファイル形式 | 使用例 (CLI) |
| :----------------- | :--- | :--------- | :------------------- | :------------------- | :----------- |
| `pytools/gen_structure_map_from_yaml.py` | Python | YAMLスキーマからMermaid構造図を生成し、ディレクトリ構造を可視化します。 | `.yaml` (スキーマ) | `.mmd` | `python pytools/gen_structure_map_from_yaml.py structured_yaml/master_schema_v1.yaml` |
| `pytools/gen_structured_yaml_html.py` | Python | 構造化されたYAMLファイル群をHTMLインデックスページに変換します。 | `structured_yaml/*.yaml` | `.html` | `python pytools/gen_structured_yaml_html.py` |
| `pytools/gen_dmc_html.py` | Python | DMCセッションのYAMLトレースを人間可読なHTMLレポートに変換します。 | `.yaml` (DMCトレース) | `.html` | `python pytools/gen_dmc_html.py --input dmc_sessions/gemini_dmc_session_20250618.md --output generated_html/DMC_20250618.html` |
| `pytools/reverse_mermaid_parser.py` | Python | HTMLまたは.mmdファイルからMermaidコードを抽出し、YAMLスニペットに整形します。 | `.html`, `.mmd` | YAMLスニペット | `python pytools/reverse_mermaid_parser.py --input generated_html/structure_map_master_schema.html` |
| `pytools/validate_mermaid_blocks.py` | Python | YAMLファイル内のMermaidコードブロックの構文を検証します。 | `.yaml` | コンソール出力 | `python pytools/validate_mermaid_blocks.py --fix structured_yaml/master_schema_v1.yaml` |
| `AI-TCP_Structure/tools/yaml_to_mermaid.go` | Go | Intent YAMLをMermaid graph TD図に変換します。 | Intent `.yaml` | `.mmd.md` | `go run AI-TCP_Structure/tools/yaml_to_mermaid.go AI-TCP_Structure/yaml/intent_001.yaml AI-TCP_Structure/graph/intent_001.mmd.md` |
| `AI-TCP_Structure/tools/gen_link_map.go` | Go | YAML、Mermaid、HTMLファイル間のリンクマップをJSONで生成します。 | `.yaml`, `.mmd`, `.html` | `.json` | `go run AI-TCP_Structure/tools/gen_link_map.go AI-TCP_Structure/yaml/ AI-TCP_Structure/html_logs/ AI-TCP_Structure/graph/ AI-TCP_Structure/link_map.json` |
| `scripts/convert_md_math_to_mathjax.py` | Python | Markdown内のLaTeX数式をMathJax互換形式に変換します。 | `.md` | `.md` | `python scripts/convert_md_math_to_mathjax.py docs/rfc_drafts/rfc_lsc_001.md` |
| `pytools/chatlog_to_html.py` | Python | Markdown形式の対話ログを色分けされたHTMLビューアに変換します。 | `.md` (対話ログ) | `.html` | `python pytools/chatlog_to_html.py samples/chatlog_sample.md generated_html/chatlog_view.html --count-tokens` |

## ⚠️ 注意点と今後の拡張余地

*   **Goバージョン**: 現在のGoスクリプトはGo 1.23以降で動作することを確認しています。
*   **Pythonバージョン**: Python 3.7以降が推奨されます。
*   **外部依存モジュール**: Pythonスクリプトは`requests`、`PyYAML`、`BeautifulSoup4`、`Jinja2`、`jsonschema`、`markdown2` (mistune)などのライブラリに依存します。これらは`requirements.txt`に記載されています。
*   **互換性**: 各ツールはObsidianおよびGitHubのレンダリングとの互換性を考慮して設計されています。
*   **自動化**: 現在は手動で実行するCLIツールが中心ですが、将来的にはCI/CDパイプラインへの統合や、より高度な自動化レイヤー（例: LM Studio APIとの直接連携）を検討しています。
*   **エラーハンドリング**: スクリプトは基本的なエラーハンドリングを含みますが、本番運用にはさらなる堅牢性強化が必要です。