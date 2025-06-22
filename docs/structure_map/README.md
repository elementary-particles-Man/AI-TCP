# 📁 `structured_yaml/` Directory Overview

This directory contains structured YAML definitions for the AI-TCP protocol and its extensions.\
本ディレクトリには、AI-TCP プロトコルおよびその拡張に関する構造化YAML定義が格納されています。

---

## 📐 Naming Convention / 命名規則

```
<schema_name>_v<version>.yaml
```

- Example: `master_schema_v1.yaml`\
  主スキーマのバージョン1

---

## 📦 Schema Structure / スキーマ構造

各YAMLファイルは、以下のトップレベルキーを持つ必要があります：

- `id`: スキーマID（任意の文字列）
- `type`: スキーマタイプ（例：`ai_tcp_specification`）
- `title`: スキーマの名称
- `description`: スキーマの概要
- `structure`: スキーマ本体

> ※これらのキーが存在しない場合、検証に失敗します。

---

## 🧪 Validation Procedure / 検証手順

検証には以下のスクリプトを使用します：

```bash
python tools/validate_structured_yaml.py structured_yaml/<file>.yaml
```

- 成功時：✅ Valid YAML.
- 失敗時：❌ Missing required keys: ...

---

## 🌐 HTML Output / HTML出力

構造可視化は以下のスクリプトで生成されます：

```bash
python tools/gen_structured_yaml_html.py
```

- 出力：`generated_html/structured_yaml_index.html`
- テンプレート：`docs/templates/html_template_structured_yaml.html`

---

## 🔗 Related Files / 関連ファイル

- `structured_yaml/master_schema_v1.yaml`
- `tools/validate_structured_yaml.py`
- `tools/gen_structured_yaml_html.py`
- `generated_html/structured_yaml_index.html`

---

*Last updated: 2025-06-20*

