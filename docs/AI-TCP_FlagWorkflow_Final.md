AI-TCP Flag Workflow (Final)
English Version

日本語版

English Version
Table of Contents
Principle: Why the Completion Flag Contains Text

Workflow: Pairing of new_task.json and complete.flag

Audit Trail: Evidence in cli_archives/

Connectivity: Link with link_map.json

1. Principle: Why the Completion Flag Contains Text
The complete.flag file must contain a summary text of the execution result for the following reasons:

Beyond Binary Verification: While the existence of the file confirms that the task sequence ran without fatal errors, it does not confirm the outcome. An empty file is a binary signal (0 or 1), which is insufficient for quality assurance.

Human-Readable Summary: The text inside the flag provides a concise, human-readable summary of what was accomplished (e.g., "Validation successful for 3 files. HTML generated."). This allows for immediate, high-level verification without needing to parse lengthy log files.

Enhanced Auditability: Storing the outcome summary directly within the flag makes the audit trail in cli_archives/ more potent. It directly links the instruction (new_task.json) to its final, summarized result (complete.flag).

In short, the text transforms the flag from a simple "done" signal to a "done, and here is the result" receipt, which is a core principle of AI-TCP's verifiable and robust design.

2. Workflow: Pairing of new_task.json and complete.flag
The new_task.json and complete.flag files operate as a matched pair, representing the beginning and end of a single, atomic transaction.

Initiation (The Instruction): A new_task.json file is placed in the cli_instruction/ directory. This is the official "work order" for the CLI.

Execution: The CLI's runner (task_bridge_runner.py) detects and locks onto this file, executing the tasks within it sequentially.

Completion (The Receipt): The final task in the JSON is always to generate the complete.flag file. The content of this flag is a summary of the results of the preceding tasks.

Pairing Validation: A successful cycle is defined by the existence of a complete.flag that corresponds to the most recently processed new_task.json. The system is designed to process only one such pair at a time.

3. Audit Trail: Evidence in cli_archives/
To ensure perfect traceability, a complete record of every transaction is preserved.

Trigger: After the complete.flag is successfully generated, an archiving script is triggered.

Bundling: The script bundles the following three artifacts, which together form a complete audit trail:

The original instruction: new_task.json

The detailed execution log: output_<timestamp>.log (or similar)

The final result summary: complete.flag

Archiving: All three files are moved into the cli_archives/ directory, typically with a shared timestamp in their filenames to ensure they are forever linked.

This process guarantees that every instruction has a corresponding, immutable record of its execution and outcome, which is fundamental for debugging and system governance.

4. Connectivity: Link with link_map.json
This document is a critical component of the project's knowledge graph. Within the master link_map.json, it is referenced as a key technical specification for the core workflow.

Example link_map.json entry:

{
  "workflow": {
    "flag_workflow": {
      "path": "docs/AI-TCP_FlagWorkflow_Final.md",
      "description": "Definitive specification for the task instruction and completion verification mechanism, including the role of the result text and archiving. The source of truth for the CLI's core loop.",
      "related_to": [
        "governance.inheritance_guide",
        "workflow.test_structure"
      ]
    }
  }
}

This ensures that any agent (AI or human) studying the test structure or the project's core philosophy can easily navigate to this definitive document for technical details.

日本語版
目次
原則：完了フラグが必ず「作業結果テキスト」を持つ理由

ワークフロー：new_task.json と complete.flag のペアリング

監査証跡：cli_archives/ における証跡

接続性：link_map.json との接続例

1. 原則：完了フラグが必ず「作業結果テキスト」を持つ理由
complete.flagファイルが実行結果の要約テキストを必ず含む理由は以下の通りです。

単なる二元的な検証を超えて: ファイルの存在はタスクシーケンスが致命的なエラーなく実行されたことを確認しますが、その成果までは確認しません。空のファイルはバイナリ信号（0か1）に過ぎず、品質保証には不十分です。

人間が判読可能な要約: フラグ内のテキストは、何が達成されたかの簡潔で人間が判読可能な要約（例：「3ファイルの検証成功。HTMLを生成しました。」）を提供します。これにより、長大なログファイルを解析することなく、即座に高レベルの検証が可能になります。

監査可能性の強化: 結果の要約をフラグ内に直接保存することで、cli_archives/内の監査証跡がより強力になります。指示（new_task.json）とその最終的な要約結果（complete.flag）を直接結びつけます。

要するに、テキストはフラグを単なる「完了」の合図から、「完了し、これが結果です」という領収書へと変容させます。これはAI-TCPの検証可能で堅牢な設計における核となる原則です。

2. ワークフロー：new_task.json と complete.flag のペアリング
new_task.jsonとcomplete.flagファイルは、単一の不可分なトランザクションの開始と終了を表す、対となるペアとして機能します。

開始（指示書）: new_task.jsonファイルがcli_instruction/ディレクトリに配置されます。これがCLIに対する公式の「作業指示書」です。

実行: CLIのランナー（task_bridge_runner.py）がこのファイルを検知してロックし、内部のタスクを順次実行します。

完了（領収書）: JSON内の最終タスクは常にcomplete.flagファイルを生成することです。このフラグの内容は、先行するタスクの結果の要約です。

ペアリング検証: 成功したサイクルは、直近に処理されたnew_task.jsonに対応するcomplete.flagの存在によって定義されます。システムは、一度に一つのペアのみを処理するように設計されています。

3. 監査証跡：cli_archives/ における証跡
完全な追跡可能性を確保するため、すべてのトランザクションの完全な記録が保存されます。

トリガー: complete.flagが正常に生成された後、アーカイブ用スクリプトが起動します。

バンドル化: スクリプトは、完全な監査証跡を形成する以下の3つの成果物を一つにまとめます。

元の指示書: new_task.json

詳細な実行ログ: output_<timestamp>.log（または同様の形式）

最終結果の要約: complete.flag

アーカイブ: これら3つのファイルはすべてcli_archives/ディレクトリに移動され、ファイル名に共通のタイムスタンプが付与されることで、永続的に関連付けられます。

このプロセスは、すべての指示がその実行と結果に関する不変の記録を持つことを保証し、デバッグとシステムガバナンスの基礎となります。

4. 接続性：link_map.json との接続例
このドキュメントは、プロジェクトの知識グラフにおける重要な構成要素です。マスターとなるlink_map.json内では、コアワークフローの主要な技術仕様として参照されます。

link_map.json のエントリ例:

{
  "workflow": {
    "flag_workflow": {
      "path": "docs/AI-TCP_FlagWorkflow_Final.md",
      "description": "タスク指示と完了検証メカニズムの決定版仕様。結果テキストとアーカイブの役割を含む。CLIのコアループにおける真実の源。",
      "related_to": [
        "governance.inheritance_guide",
        "workflow.test_structure"
      ]
    }
  }
}

これにより、テスト構造やプロジェクトの基本哲学を調査するエージェント（AIまたは人間）が誰であっても、技術的な詳細を求めてこの決定版ドキュメントに容易にナビゲートできます。