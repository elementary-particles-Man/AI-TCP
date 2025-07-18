🛠️ AI-TCP Tools Directory (Legacy Go/Python Tools)

## Overview

This directory contains Go and Python scripts that were used for various transformations and utilities within the AI-TCP project, primarily for converting YAML structures to HTML, Mermaid, and JSON. These tools are now considered legacy as the main development focus shifts to Rust. They are preserved here for historical reference and for specific legacy tasks.

---

## 📁 Directory Structure

| Directory | Purpose                                                              |
| :-------- | :------------------------------------------------------------------- |
| `yaml/`   | Input YAML files                                                     |
| `graph/`  | Output directory for Mermaid format graphs                           |
| `html_logs/` | Output directory for HTML tables                                     |
| `link_map/` | Generated link map JSON                                              |
| `tools/`  | This script group (within AI-TCP_Structure/tools)                    |

---

## 📌 Key Scripts and Usage (Legacy)

These scripts are primarily for historical reference. New tools will be developed in Rust.

### ✅ `yaml_to_mermaid.go`

Converts Intent YAML to Mermaid graph TD diagrams.

```bash
cd tools
go run yaml_to_mermaid.go ../yaml/intent_001.yaml ../graph/intent_001.mmd.md
```

### ✅ `yaml_to_html.go`

Converts Intent YAML to HTML.

```bash
cd tools
go run yaml_to_html.go ../yaml/intent_001.yaml ../html_logs/intent_001.html
```

### ✅ `gen_link_map.go`

Generates a JSON link map between YAML, Mermaid, and HTML files.

```bash
cd tools
go run gen_link_map.go ../yaml ../html_logs ../graph ../link_map/map.json
```

### ✅ `gen_structure_tree.go`

Generates a structure tree.

```bash
cd tools
go run gen_structure_tree.go .. ../../docs/poc_logs/structure_map.mmd.md
```

### ✅ `check_semantics.go`

Checks semantics of YAML files.

```bash
cd tools
go run check_semantics.go ../yaml/intent_001.yaml
```

### ✅ `enrich_yaml_semantics.go`

Enriches YAML semantics.

```bash
cd tools
go run enrich_yaml_semantics.go ../yaml/intent_001.yaml ../enriched_yaml -description "Sample" -next intent_002
```

### ✅ `inject_graph_labels.go`

Injects graph labels.

```bash
cd tools
go run inject_graph_labels.go ../yaml/intent_001.yaml ../graph/intent_001.mmd.md ../graph_labeled/intent_001.mmd.md
```

### ✅ `intent_yaml_to_mermaid.py`

Converts Intent YAML to Mermaid graph diagrams (Python).

```bash
cd ../..
python scripts/intent_yaml_to_mermaid.py AI-TCP_Structure/yaml/intent_001.yaml AI-TCP_Structure/graph/intent_001.mmd.md
```

---

## 📝 Note on `.mmd.md` Files

`.mmd.md` files are output in Markdown format containing Mermaid drawing blocks, and can be directly rendered as graphs in Obsidian's live preview. Combined with link maps and structure trees, this enables visual traceability of the entire Vault.

---

# 🛠️ AI-TCP ツールディレクトリ (レガシー Go/Python ツール)

## 概要

本ディレクトリには、AI-TCPプロジェクト内で様々な変換やユーティリティに使用されたGoおよびPythonスクリプトが格納されています。主にYAML構造をHTML、Mermaid、JSONに変換するために利用されました。現在、主要な開発がRustに移行したしたため、これらのツールはレガシーとして扱われます。これらは履歴参照用、および特定のレガシータスク用に保存されています。

---

## 📁 ディレクトリ構成

| ディレクトリ | 用途                                                              |
| :----------- | :---------------------------------------------------------------- |
| `yaml/`      | 入力 YAML ファイル群                                              |
| `graph/`     | Mermaid 形式のグラフ出力先                                        |
| `html_logs/` | HTML テーブル出力先                                               |
| `link_map/`  | 生成されるリンクマップ JSON                                       |
| `tools/`     | 本スクリプト群 (AI-TCP_Structure/tools 内)                        |

---

## 📌 主要スクリプトと使用例 (レガシー)

これらのスクリプトは主に履歴参照用です。新しいツールはRustで開発されます。

### ✅ `yaml_to_mermaid.go`

Intent YAML を Mermaid graph TD 図に変換します。

```bash
cd tools
go run yaml_to_mermaid.go ../yaml/intent_001.yaml ../graph/intent_001.mmd.md
```

### ✅ `yaml_to_html.go`

Intent YAML を HTML に変換します。

```bash
cd tools
go run yaml_to_html.go ../yaml/intent_001.yaml ../html_logs/intent_001.html
```

### ✅ `gen_link_map.go`

YAML、Mermaid、HTML ファイル間のリンクマップを JSON で生成します。

```bash
cd tools
go run gen_link_map.go ../yaml ../html_logs ../graph ../link_map/map.json
```

### ✅ `gen_structure_tree.go`

構造ツリーを生成します。

```bash
cd tools
go run gen_structure_tree.go .. ../../docs/poc_logs/structure_map.mmd.md
```

### ✅ `check_semantics.go`

YAML ファイルのセマンティクスをチェックします。

```bash
cd tools
go run check_semantics.go ../yaml/intent_001.yaml
```

### ✅ `enrich_yaml_semantics.go`

YAML のセマンティクスを強化します。

```bash
cd tools
go run enrich_yaml_semantics.go ../yaml/intent_001.yaml ../enriched_yaml -description "Sample" -next intent_002
```

### ✅ `inject_graph_labels.go`

グラフラベルを挿入します。

```bash
cd tools
go run inject_graph_labels.go ../yaml/intent_001.yaml ../graph/intent_001.mmd.md ../graph_labeled/intent_001.mmd.md
```

### ✅ `intent_yaml_to_mermaid.py`

Intent YAML を Mermaid graph 図に変換します (Python)。

```bash
cd ../..
python scripts/intent_yaml_to_mermaid.py AI-TCP_Structure/yaml/intent_001.yaml AI-TCP_Structure/graph/intent_001.mmd.md
```

---

## 📝 .mmd.md ファイルに関する注記

.mmd.md ファイルは Mermaid 描画ブロックを含む Markdown 形式で出力され、Obsidian のライブプレビューで直接グラフとして描画可能です。リンクマップや構造ツリーと合わせて、Vault全体のトレース可視化が可能になります。