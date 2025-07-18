# Autonomous Negotiation Playground (PoC #008)

## Overview

This `playground` directory is a dedicated area for storing simulation results of PoC #008, "Autonomous AI Negotiation," within the AI-TCP project.

It records the entire process where multiple AI agents with different objectives negotiate, resolve conflicts, and reach a final agreement using Graph Payloads, all without human intervention. This demonstrates that AI-TCP is not merely a communication protocol but a foundational technology supporting the sociality of autonomous AI ecosystems.

## Directory Structure and Role of Each File

### 📁 agents/

Contains YAML files defining the "personality" and "initial intent" of each negotiating participant.

*   **`agent_A.yaml`**: Definition file for Creative-AI, handled by GPT. Describes a thought process prioritizing speed.
*   **`agent_B.yaml`**: Definition file for Maintenance-AI, handled by Gemma 3. Describes a thought process prioritizing readability and maintainability.
*   **`mediator_C.yaml`**: Definition file for Moderator-AI, handled by Gemini. Describes the mediation logic to balance both parties and derive an optimal solution.

### 📁 negotiation_logs/

Contains log files recording the entire negotiation process in different formats.

*   **`negotiation_008.mmd.md`**: Mermaid file recording the transitions of Graph Payloads exchanged at each stage of the negotiation. Allows visual tracking of intent changes.
*   **`negotiation_008.html`**: HTML log recording all negotiation turns in a chronological table format. Allows humans to easily view who, when, and what proposals or signals were sent.

### 📁 summary/

Contains summary files compiling the final results and analysis of the negotiation.

*   **`negotiation_outcome_008.md`**: Official report summarizing what agreement was reached through negotiation, or why an agreement was not reached.

## Relationship with PoC #008

All files in this directory are primary source materials directly generated from the PoC #008 simulation. By analyzing these outputs, one can concretely verify how the AI-TCP protocol (specifically RFCs 004, 012, 016, 017) enables advanced collaborative work among autonomous AIs.

---

# 自律型ネゴシエーション・プレイグラウンド (PoC #008)

## 概要

本 `playground` ディレクトリは、AI-TCPプロジェクトにおけるPoC #008「自律型AIネゴシエーション」のシミュレーション成果物を格納する専用エリアです。

ここでは、異なる目的を持つ複数のAIエージェントが、人間の介入なしに Graph Payload を用いて交渉し、対立を解決し、最終的な合意に至るまでの一連のプロセスが記録されています。これは、AI-TCPが単なる通信規約ではなく、自律的なAIエコシステムの社会性を支える基盤技術であることを実証するものです。

## ディレクトリ構成と各ファイルの役割

### 📁 agents/

各交渉参加者の「人格」と「初期意図」を定義するYAMLファイルが格納されています。

*   **`agent_A.yaml`**: GPTが担当するCreative-AIの定義ファイル。迅速性を最優先する思考様式が記述されています。
*   **`agent_B.yaml`**: Gemma 3が担当するMaintenance-AIの定義ファイル。可読性と保守性を最優先する思考様式が記述されています。
*   **`mediator_C.yaml`**: Geminiが担当するModerator-AIの定義ファイル。両者の均衡を取り、最適解を導き出す調停ロジックが記述されています。

### 📁 negotiation_logs/

交渉の全プロセスを、異なる形式で記録したログファイルが格納されています。

*   **`negotiation_008.mmd.md`**: 交渉の各段階で交換されたGraph Payloadの変遷を記録したMermaidファイルです。意図の視覚的な変化を追跡できます。
*   **`negotiation_008.html`**: 交渉の全ターンを時系列のテーブル形式で記録したHTMLログです。誰が、いつ、どのような提案やシグナルを発信したかを人間が容易に閲覧できます。

### 📁 summary/

交渉の最終結果と分析をまとめたサマリーファイルが格納されています。

*   **`negotiation_outcome_008.md`**: 交渉がどのような合意に至ったか、あるいはなぜ合意に至らなかったかを要約した公式レポートです。

## PoC #008との関係

このディレクトリ内の全てのファイルは、PoC #008のシミュレーションから直接生成された一次資料です。これらの成果物を分析することで、AI-TCPプロトコル（特にRFC 004, 012, 016, 017）が、いかにして自律的なAI間の高度な協調作業を実現するかを具体的に検証することができます。