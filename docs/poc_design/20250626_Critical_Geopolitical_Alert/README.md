# 2025年6月26日 Critical Geopolitical Alert ドキュメント統合版

## 本アラートの目的と経緯

- DRユニットが検知した複合的な地政学リスクを基点に、AI-TCPプロトコル下での情報連携手順を検証するためのPoC。
- GPTによる統合判断とGeminiによるナラティブ構築を経て、政策誘導とリポジトリ保存までを一貫して記録。

## 関連ファイル一覧

- `dmc_sessions/alerts/20250626_Critical_Geopolitical_Alert/G1_Narrative_Summary.md`
- `dmc_sessions/alerts/20250626_Critical_Geopolitical_Alert/G2_YAML_Structured_Report.md`
- `dmc_sessions/alerts/20250626_Critical_Geopolitical_Alert/G3_Analytical_Insight.md`
- `dmc_sessions/alerts/20250626_Critical_Geopolitical_Alert/G4_Actionable_Policy.md`
- `dmc_sessions/alerts/20250626_Critical_Geopolitical_Alert/Alert_Log_20250626_EN.md`
- `dmc_sessions/alerts/20250626_Critical_Geopolitical_Alert/Alert_Log_20250626_JP.md`
- `docs/20250626_Critical_Geopolitical_Alert.html`

## YAMLとMermaidファイルの役割

- `meta_log_structure.yaml` は全フェーズの進行ログをYAML形式で保持し、フェーズ間の因果関係を検証する基盤となる。
- `graph_payload/` 配下の `.mmd.md` ファイル群は、上記YAMLを視覚化するためのMermaidコードを格納し、Obsidian等でのプレビューを想定。

## AI-TCP全体設計との関連（Phase対応表）

| Phase | 役割 | 対応ファイル |
|-------|------|--------------|
| 1 | 危機意識と初期分析 | G1_Narrative_Summary.md |
| 2 | AIの役割定義とアラート作成 | Alert_Log_20250626_EN.md / JP.md |
| 3 | 分析深化と役割分担 | G2_YAML_Structured_Report.md |
| 4 | ドキュメント生成とプロセス管理 | G3_Analytical_Insight.md / G4_Actionable_Policy.md |
| 5 | リポジトリ保存と検証待機 | meta_log_structure.yaml |

