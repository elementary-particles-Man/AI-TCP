# 📁 `dmc_sessions/` Directory Overview

This directory contains session logs for Direct Mental Care (DMC) scenarios used in AI-TCP experiments.  \
本ディレクトリには、AI-TCP 実験におけるメンタルケア向けセッションログが含まれます。

---

## 📐 File Naming / ファイル命名規則

```
dmc_<domain>_<serial>.yaml
```

- Example: `dmc_mental_001.yaml`\
  メンタルケア領域の第1セッション

---

## 📦 File Format / ファイル構造

各YAMLファイルは以下のような構造です：

```yaml
id: "session-uuid"
timestamp: "ISO8601形式の日時"
lang: "en" または "ja"
phase: "pre_assessment" | "intervention" | "decision"
agent: "gpt-4o" など
meta:
  version: "1.0"
  source: "manual" など
tags:
  - "anxiety"
  - "self-esteem"
data:
  input: |
    ユーザーからの入力文
  output: |
    AIによる応答文
```

---

## 🌐 View as HTML / HTML閲覧

HTML形式で各セッションを見るには以下を参照してください：

➡️ [`generated_html/dmc_mental_001.html`](../generated_html/dmc_mental_001.html) など

> 出力は [`html_template_dmc.html`](../docs/templates/html_template_dmc.html) により生成されます。

---

*Last updated: 2025-06-20*

