# Generated Documentation

This directory contains documentation and reports that are automatically generated from various structured data sources within the AI-TCP project. These generated files provide human-readable outputs for analysis, review, and sharing.

## How to Generate:

Use the following command to convert a validated YAML trace into an HTML report:

```bash
python scripts/gen_dmc_html.py --input structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml --output docs/generated/DMC_20250618.html
```

The default template for HTML generation is located at `html_templates/dmc_base_template.html`.

---

# 生成されたドキュメント

本ディレクトリには、AI-TCPプロジェクト内の様々な構造化データソースから自動生成されたドキュメントやレポートが格納されています。これらの生成ファイルは、分析、レビュー、共有のための人間が読める形式の出力を提供します。

## 生成方法:

検証済みのYAMLトレースをHTMLレポートに変換するには、以下のコマンドを使用します：

```bash
python scripts/gen_dmc_html.py --input structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml --output docs/generated/DMC_20250618.html
```

HTML生成のデフォルトテンプレートは `html_templates/dmc_base_template.html` にあります。