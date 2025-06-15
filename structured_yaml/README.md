# structured_yaml

このディレクトリは AI‑TCP関連の構造化データ(YAML)を格納します。
すべてのYAMLファイルは`master_schema_v1.yaml`で定義されるスキーマに準拠します。

## validated_yaml/
スキーマ検証を完了したファイルを配置します。
- ai_tcp_timeline.yaml – 制定経緯タイムライン（構文・内容確認済）
- ai_tcp_poc_design.yaml – PoC設計概要（構文OK、構造要整形）

## plain_yaml/
- [その他ファイル名] – 構文はOKだが構造化完了していないファイル

---

## 今後の手順
1. 構造要検討ファイルはフォーマット・内容のYAML化を継続
2. `master_schema_v1.yaml` に基づき各ファイルを検証
3. 統合された構造をCodex/GDで検証・調整
