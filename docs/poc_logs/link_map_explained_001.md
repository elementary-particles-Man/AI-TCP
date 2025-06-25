リンクマップ解説: link_map.json
ファイルパス: docs/poc_logs/link_map_explained_001.md
ソース: AI-TCP_Structure/link_map/link_map.json

1. 概要と目的
この文書は、link_map.jsonファイルに定義された構造化リンクマップを解説するものです。このJSONファイルは、AI-TCPリポジトリ内に散在する各成果物（RFC、PoCログ、YAML定義、Mermaidグラフなど）間の論理的な関係性を、機械判読可能な形式で定義します。

主な目的は以下の通りです。

構造の可視化: プロジェクト全体の依存関係と情報フローを明確にします。

ナビゲーションの支援: 人間とAIの両方が、関連文書間を効率的に移動するためのハブとして機能します。

整合性の自動検証: 成果物間のリンク切れや意図の不一致をプログラムで検証するための基礎データを提供します。

2. リンク構造の解説
link_map.json内の各リンクは、from (起点) と to (終点) を持つ有向グラフとして定義されています。

キー

型

説明

from

string

リンクの起点となる成果物のファイルパス。

to

string

リンクの終点となる成果物のファイルパス。

relation

string

起点と終点の関係性を示す動詞句 (例: is_narrative_for, validates)。

intent_id

string

このリンク関係が持つ一意の意図ID。YAMLファイル内のIDと整合性を取る。

意図の流れ (from → to)
この構造は、**「成果物Aは、成果物Bに対して『特定の関係』を持つ」**という明確な論理の流れを示します。例えば、「このナラティブ文書(from)は、あのMermaidグラフ(to)を解説するもの(is_narrative_for)である」といった関係性を定義します。

3. 具体例による解説
以下は、link_map.jsonに含まれる典型的なリンクの解説です。

Intent ID

From (起点)

To (終点)

Relation (関係性)

解説

DMC-NARRATIVE-001

intent_narrative_001.md

intent_001.html

is_narrative_for

このリンクは、ナラティブ解説文書が、特定のHTMLログの内容を説明するものであることを示します。

DMC-GRAPH-VERIFY-001

verify_graph_001.md

intent_001.mmd.md

validates

検証ログが、Mermaidグラフの構文と意味の整合性を検証した結果であることを示します。

RFC-POC-LINK-012

rfc_drafts/012...

poc_logs/poc_005...

is_implemented_by

RFC 012で定義された仕様が、PoC #5によって概念実証された、という実装関係を示します。

4. 整合性検証
このリンクマップの信頼性を担保するため、以下の検証が行われます。

ファイル存在確認: fromおよびtoに記述されたファイルパスが、リポジトリ内に実際に存在するかを確認します。

意図IDの整合性: intent_idが、関連するYAMLファイルや他の成果物で定義されたIDと一致しているか、あるいは命名規則に沿っているかを確認します。これにより、プロジェクト全体での概念の統一が図られます。

5. Obsidian Vaultにおけるナビゲーションハブ
この文書は、Obsidian内で強力なナビゲーションツールとして機能するように設計されています。以下のリンクは、実際のファイルへ直接移動するためのものです。

DMCセッションのナラティブ解説:

起点: [[intent_narrative_001.md]]

終点: (HTMLファイルのため直接リンク不可)

Mermaidグラフの検証ログ:

起点: [[verify_graph_001.md]]

終点: [[AI-TCP_Structure/graph/intent_001.mmd.md]]

競合解決の仕様と実装:

起点: [[rfc_drafts/012_conflict_resolution.md]]

終点: [[poc_005_conflict_resolution.md]]

このように、link_map.jsonはAI-TCPプロジェクトの論理的な骨格を定義し、この解説文書はその地図として機能します。