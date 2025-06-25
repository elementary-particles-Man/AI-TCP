🛠️ AI-TCP ツールディレクトリ
このディレクトリには、AI-TCP プロジェクトの様々なフェーズで活用される、Python および Go で実装されたユーティリティスクリプト群が格納されています。これらのツールは、YAML 構造の変換、Mermaid グラフの生成、HTML レンダリング、および各種検証を自動化し、プロジェクトの効率的な進行を支援します。

📁 ディレクトリ構成
pytools/: Python 製スクリプト（YAML 処理、HTML 生成、グラフ操作など）

scripts/: Python および JavaScript 製スクリプト（Mermaid 変換、MathJax 変換など）

AI-TCP_Structure/tools/: Go 製スクリプト（YAML 処理、リンクマップ生成など）

📌 主要スクリプトと使用方法
スクリプトファイル

言語

目的と概要

主な入力ファイル形式

主な出力ファイル形式

使用例 (CLI)

pytools/gen_structure_map_from_yaml.py

Python

YAML スキーマから Mermaid 構造図を生成し、ディレクトリ構造を可視化します。

.yaml (スキーマ)

.mmd

python pytools/gen_structure_map_from_yaml.py structured_yaml/master_schema_v1.yaml

pytools/gen_structured_yaml_html.py

Python

構造化された YAML ファイル群を HTML インデックスページに変換します。

structured_yaml/*.yaml

.html

python pytools/gen_structured_yaml_html.py

pytools/gen_dmc_html.py

Python

DMC セッションの YAML トレースを人間可読な HTML レポートに変換します。

.yaml (DMC トレース)

.html

python pytools/gen_dmc_html.py --input dmc_sessions/gemini_dmc_session_20250618.md --output generated_html/DMC_20250618.html

pytools/reverse_mermaid_parser.py

Python

HTML または .mmd ファイルから Mermaid コードを抽出し、YAML スニペットに整形します。

.html, .mmd

YAML スニペット

python pytools/reverse_mermaid_parser.py --input generated_html/structure_map_master_schema.html

pytools/validate_mermaid_blocks.py

Python

YAML ファイル内の Mermaid コードブロックの構文を検証します。

.yaml

コンソール出力

python pytools/validate_mermaid_blocks.py --fix structured_yaml/master_schema_v1.yaml

AI-TCP_Structure/tools/yaml_to_mermaid.go

Go

Intent YAML を Mermaid graph TD 図に変換します。

Intent .yaml

.mmd.md

go run AI-TCP_Structure/tools/yaml_to_mermaid.go AI-TCP_Structure/yaml/intent_001.yaml AI-TCP_Structure/graph/intent_001.mmd.md

AI-TCP_Structure/tools/gen_link_map.go

Go

YAML、Mermaid、HTML ファイル間のリンクマップを JSON で生成します。

.yaml, .mmd, .html

.json

go run AI-TCP_Structure/tools/gen_link_map.go AI-TCP_Structure/yaml/ AI-TCP_Structure/html_logs/ AI-TCP_Structure/graph/ AI-TCP_Structure/link_map.json

scripts/convert_md_math_to_mathjax.py

Python

Markdown 内の LaTeX 数式を MathJax 互換形式に変換します。

.md

.md

python scripts/convert_md_math_to_mathjax.py docs/rfc_drafts/rfc_lsc_001.md

⚠️ 注意点と今後の拡張余地
Go バージョン: 現在の Go スクリプトは Go 1.23 以降で動作することを確認しています。

Python バージョン: Python 3.7 以降が推奨されます。

外部依存モジュール: Python スクリプトは requests, PyYAML, BeautifulSoup4, Jinja2, jsonschema, markdown2 (mistune) などのライブラリに依存します。これらは requirements.txt に記載されています。

互換性: 各ツールは Obsidian および GitHub のレンダリングとの互換性を考慮して設計されています。

自動化: 現在は手動で実行する CLI ツールが中心ですが、将来的には CI/CD パイプラインへの統合や、より高度な自動化レイヤー（例: LM Studio API との直接連携）を検討しています。

エラーハンドリング: スクリプトは基本的なエラーハンドリングを含みますが、本番運用にはさらなる堅牢性強化が必要です。

最終更新日: 2025-06-25