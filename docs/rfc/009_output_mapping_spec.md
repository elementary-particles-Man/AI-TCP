RFC 009: AI-TCP 成果物出力マッピング仕様書
1. 概要
この RFC は、AI-TCP プロジェクトにおいて、構造定義（Intent YAML）から最終的な成果物（Mermaid グラフ、自然言語解説、Graph Payload、RFC ドキュメントなど）がどのように生成・変換されるかのマッピングとフローを定義します。これにより、AI-TCP エコシステム内でのデータの整合性、再利用性、および自動化されたドキュメント生成の標準化を目指します。

2. 変換フローの全体像
AI-TCP プロジェクトにおける主要な成果物生成フローは、Intent YAML を起点とする多段階の変換プロセスです。

graph TD
    A[1. Intent YAML<br>(`intent_007.yaml`)] --> B[2. Mermaid グラフ生成<br>(`gen_mermaid.py`)];
    B --> C[3. 自然言語解説生成<br>(Gemini Flash)];
    C --> D[4. Graph Payloadへの統合<br>(RFC 004 準拠)];
    D --> E[5. RFC ドキュメントへの組み込み<br>(`docs/rfc/`)];
    E --> F[6. GitHub / Obsidian 公開];

3. 各ステップの入力/出力と変換ロジック
3.1. Intent YAML (起点)
入力: AI の意図、目標、制約、およびコンポーネントと接続を定義した YAML 構造。

出力: 構造化されたデータ (.yaml)。

変換ロジック: 人間または AI (GPT など) による手動作成。各フィールドは master_schema_v1.yaml に準拠。

特徴: AI-TCP における「単一の信頼できる情報源 (Single Source of Truth)」。

3.2. Mermaid グラフ生成
入力: Intent YAML (.yaml)。

出力: Mermaid 構文 (.mmd.md)。

変換ロジック: Codex が実装した Python/Go スクリプト (AI-TCP_Structure/tools/yaml_to_mermaid.go や pytools/yaml_to_mermaid_simple.py など) による自動変換。YAML の components は Mermaid のノードに、connections はエッジにマッピングされます。

特徴: AI の意図構造を視覚化し、人間と AI の両方に直感的な理解を促します。

3.3. 自然言語解説生成
入力: Mermaid グラフ (.mmd.md)、または Intent YAML (.yaml)。

出力: 自然言語ナラティブ (.md)。

変換ロジック: Gemini Flash などの LLM が、入力された構造化データ（Mermaid や YAML）を解釈し、その「意味」や「設計思想」、「プロセスの流れ」を人間が理解できる文章に変換します。

特徴: AI の思考プロセスを透明化し、技術的な詳細を知らない読者にも意図を伝達可能にします。

3.4. Graph Payload への統合
入力: Mermaid グラフ (.mmd.md)、および関連するメタデータ。

出力: AI-TCP パケットのペイロード内に埋め込まれた Mermaid 構文。

変換ロジック: RFC 004 (Graph Payload Specification) に準拠し、Mermaid 構文を mmd: プレフィックス付きでペイロードの graph_structure フィールドに格納。

特徴: AI 間での視覚的・構造的な「意図」の直接的な交換を可能にします。

3.5. RFC ドキュメントへの組み込み
入力: Intent YAML、Mermaid グラフ、自然言語解説、Graph Payload、関連する PoC データ。

出力: RFC 形式の Markdown ドキュメント (.md)。

変換ロジック: GPT や Gemini Flash が、上記全ての成果物を統合し、標準的な RFC テンプレート（例えば docs/templates/ai_tcp_rfc_template.md）に従って、セクション分け、表組み、コードブロックの挿入などを行います。

特徴: プロジェクトの公式な技術仕様として、国際的な議論と標準化の土台となります。

3.6. GitHub / Obsidian 公開
入力: 全ての .md, .html, .mmd.md, .json, .yaml 成果物。

出力: Web 上での公開されたリポジトリ。

変換ロジック: Git (add, commit, push) によるバージョン管理と同期。Obsidian Vault の構造に合わせたディレクトリ配置により、Obsidian のライブプレビューや内部リンク機能も活用。

特徴: プロジェクトの透明性を最大化し、誰もが成果物を参照、検証、貢献できるようにします。

4. 今後の自動化・連結計画
このマッピング仕様は、将来的な自動化システムの設計基盤となります。

CLI/スクリプト/API の活用: 各変換ステップは、Python や Go で書かれた CLI ツール、またはローカル LLM API と連携するスクリプトによって自動化されます。

CI/CD パイプラインへの統合: 全ての変換と検証プロセスを自動化された CI/CD パイプラインに組み込むことで、ドキュメントの鮮度と整合性を常に保ちます。

双方向変換: 特に、自然言語と構造化された表現（YAML/Mermaid）間の双方向変換の精度向上は、AI-TCP の汎用性を高める上で重要です。

最終更新日: 2025-06-25