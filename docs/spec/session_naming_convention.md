# 🧾 Session Naming Convention / セッション命名規則

This document defines the naming rules for YAML files used in AI-TCP session records.\
本書は AI-TCP セッション記録に使用される YAML ファイルの命名規則を定義します。

---

## 🔤 Format Rule / 命名形式

```
<session_type>_<domain>_<serial>.yaml
```

### 🧱 Components / 構成要素

| Component      | Format Example    | Description (EN)                                     | 説明（日本語）             |
| -------------- | ----------------- | ---------------------------------------------------- | ------------------- |
| `session_type` | `dmc`, `tcp`, etc | Session category or protocol type                    | セッション種別またはプロトコル分類   |
| `domain`       | `mental`, `legal` | Problem domain or target topic                       | 問題領域または対象テーマ        |
| `serial`       | `001`, `042`      | 3-digit serial number (ascending, unique per domain) | ドメインごとの一意な3桁の連番     |
| `.yaml`        | literal extension | File extension (YAML format only)                    | ファイル拡張子（常に `.yaml`） |

---

## 📘 Examples / 使用例

| File Name             | Meaning (EN)                                | 意味（日本語）                  |
| --------------------- | ------------------------------------------- | ------------------------ |
| `dmc_mental_001.yaml` | First DMC session in mental health domain   | メンタル領域における最初の DMC セッション  |
| `tcp_logic_022.yaml`  | 22nd TCP-type session in logic problem area | 論理領域における TCP 型セッションの22件目 |
| `dmc_safety_105.yaml` | Safety-related DMC session #105             | 安全領域における DMC セッション105件目  |

---

## 🔒 Reserved Prefixes / 予約プレフィックス

| Prefix | Usage Scope          | 説明（日本語）            |
| ------ | -------------------- | ------------------ |
| `dmc`  | Direct Mental Care   | メンタルケア対応セッション      |
| `tcp`  | AI-TCP Core Sessions | AI-TCP 中核構造関連セッション |

> 💡 プレフィックス・ドメインは必要に応じて拡張可能です。

---

*Last updated: 2025-06-20*

