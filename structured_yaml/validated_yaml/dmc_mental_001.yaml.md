# dmc_mental_001.yaml フィールド一覧

| キー | 意味・役割 | データ型 | 必須/任意 | 説明 |
| --- | --- | --- | --- | --- |
| `id` | セッションを一意に識別するID | string | 必須 | `dmc_<domain>_<serial>` 形式の識別子 |
| `timestamp` | 記録日時 | string | 必須 | ISO 8601形式でセッション開始時刻を表す |
| `lang` | 使用言語 | string | 必須 | `en` などの言語コード |
| `phase` | 現在のセッション段階 | string | 必須 | 例:`pre_assessment`、セッション進行状況を示す |
| `agent` | 対応したAIモデル名 | string | 任意 | 応答を生成したモデルを記録 |
| `tags` | セッションのタグ | list[string] | 任意 | `anxiety` など、セッションに関連するキーワード |
| `meta.version` | データ形式のバージョン | string | 任意 | スキーマや定義のバージョン管理用 |
| `meta.source` | 入力元の種別 | string | 任意 | `user-initial-input` など、データ取得経緯を表す |
| `data.input` | ユーザーからの入力 | string | 必須 | 相談内容や質問文などの実際の発話 |
| `data.output` | AIからの返答 | string | 必須 | 入力に対するAIの応答メッセージ |
