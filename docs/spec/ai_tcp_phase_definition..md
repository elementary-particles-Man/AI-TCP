# 🧭 AI-TCP Phase Definition / フェーズ定義

This document defines all valid values of `phase:` used in AI-TCP YAML schemas and how they function across PoC pipelines.  
本書は AI-TCP の YAML 構造において使用される `phase:` 値と、それぞれの意味・役割について定義します。

---

## 🔄 Phase Mapping Table

| Phase Key         | Description (EN)                                      | 説明（日本語）                                  |
|-------------------|--------------------------------------------------------|-------------------------------------------------|
| `pre_assessment`  | Initial contextual analysis before session start       | セッション開始前の背景分析                     |
| `triage`          | Urgency-based classification of user input             | ユーザー入力の緊急度分類                       |
| `intervention`    | Core processing / response generation                  | 対応フェーズ（AIの介入）                        |
| `reflection`      | Feedback collection and model-side introspection       | 応答後のフィードバックおよび内省処理           |
| `closure`         | Session finalization and trace record generation       | セッションの終結とログ生成                     |

---

## 🔍 Usage Guidelines

- `phase:` must appear exactly once per DMC YAML root-level block.  
  `phase:` は DMC YAML のルートブロックに必ず1回だけ記述されなければなりません。

- Phases must follow this canonical order unless explicitly overridden.  
  フェーズは特別な指定がない限り、上記の順序に従う必要があります。

- Multi-phase sessions must be explicitly mapped in `dmc_session_*.md`.  
  複数フェーズを跨るセッションは `dmc_session_*.md` ファイル内で明示的に対応付けされる必要があります。

- Phase definitions can be extended in future variants (e.g., `diagnostics`, `standby`).  
  将来の拡張版ではフェーズ定義が追加される場合があります（例：`diagnostics`、`standby` など）。

---

_Last updated: 2025-06-20_

