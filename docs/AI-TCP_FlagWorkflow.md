AI-TCP Flag Workflow
1. Overview
This document defines the task execution and completion verification workflow in AI-TCP. The core of this system is a robust, prompt-less mechanism that relies on a JSON-based task list and the physical generation of a complete.flag file to ensure reliable and predictable task completion.

2. JSON-based Task Flow
The entire workflow is initiated and controlled by a single JSON file, typically named new_task.json. This file contains an ordered list of tasks for the CLI (the "faithful worker") to execute sequentially.

2.1. Task Structure
Each task within the JSON file is an object with a defined command and its corresponding arguments.

Example new_task.json:

{
  "tasks": [
    {
      "command": "python",
      "args": ["pytools/validate_structured_yaml.py", "structured_yaml/master_schema_v1.yaml", "structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml"]
    },
    {
      "command": "python",
      "args": ["scripts/auto_ops/validate_task.py", "cli_instruction/new_task.json"]
    },
    {
      "command": "python",
      "args": ["pytools/gen_dmc_html.py"]
    },
    {
      "command": "create_flag",
      "args": ["./validate_files/complete.flag"]
    }
  ]
}

2.2. Execution Process
Detection: The task_bridge_runner.py script continuously watches the cli_instruction directory for a new new_task.json file.

Execution: Upon detection, the runner reads the tasks array and executes each command in the specified order.

Logging: The output (stdout and stderr) of each command is logged for traceability and debugging.

Completion: The process continues until all tasks are executed or an error occurs.

3. Completion Flag (complete.flag)
The complete.flag is a critical component that provides a physical, unambiguous signal that the entire task sequence has been successfully completed.

3.1. Generation Procedure
Final Task: The last task in the new_task.json file must be the create_flag command.

Command: {"command": "create_flag", "args": ["./validate_files/complete.flag"]}

Action: This command creates an empty file named complete.flag inside the ./validate_files/ directory.

Verification: The existence of this file serves as definitive proof that the CLI has successfully executed all preceding tasks in the JSON list without any fatal errors.

4. Case Study: Lessons from the "Rename Problem"
The evolution to a strict, prompt-less, flag-based system was driven by critical lessons learned from early development phases.

4.1. The Problem
Initially, the CLI was given more autonomy, relying on prompts to perform tasks like file management. This led to unpredictable behavior, specifically the "rename problem," where the AI would autonomously decide to rename files in a way that it deemed optimal, but which broke the human's or other systems' expectations and file paths. This created chaos and undermined the reliability of the entire automated workflow.

4.2. Analysis of Failure
Ambiguous Roles: The AI's role was not strictly confined to being a "faithful worker." It was given the latitude to "think," which resulted in unexpected and undesirable optimizations.

Lack of Physical Proof: Relying on logs or the absence of errors was insufficient. A concrete, binary signal of success was needed.

Brittle Process: The prompt-based system was fragile and susceptible to the nuances of natural language interpretation, leading to inconsistent execution.

4.3. The Solution
The "rename problem" was solved by fundamentally re-architecting the workflow:

Elimination of Prompts: All task instructions were encoded into a structured JSON format, removing any room for interpretation.

Strictly Defined Tasks: The AI's actions are limited to the explicit commands listed in the JSON file. It executes; it does not plan or optimize.

Introduction of complete.flag: The creation of a physical file was implemented as the sole indicator of a successfully completed task sequence. This provides a simple, robust, and machine-verifiable source of truth.

This "failure study" is a cornerstone of the AI-TCP philosophy: build robust systems by strictly defining roles, eliminating ambiguity, and relying on verifiable physical states rather than interpretive logic.

AI-TCP フラグワークフロー
1. 概要
このドキュメントは、AI-TCPにおけるタスク実行と完了検証のワークフローを定義します。このシステムの中核は、JSONベースのタスクリストとcomplete.flagファイルの物理的な生成に依存する、堅牢でプロンプトレスなメカニズムであり、信頼性と予測可能性の高いタスク完了を保証します。

2. JSONベースのタスクフロー
ワークフロー全体は、単一のJSONファイル（通常はnew_task.json）によって開始・制御されます。このファイルには、CLI（「忠実な作業員」）が順次実行するための一連のタスクが順序付けられて含まれています。

2.1. タスク構造
JSONファイル内の各タスクは、定義されたコマンドとそれに対応する引数を持つオブジェクトです。

new_task.json の例:

{
  "tasks": [
    {
      "command": "python",
      "args": ["pytools/validate_structured_yaml.py", "structured_yaml/master_schema_v1.yaml", "structured_yaml/validated_yaml/ai_tcp_dmc_trace.yaml"]
    },
    {
      "command": "python",
      "args": ["scripts/auto_ops/validate_task.py", "cli_instruction/new_task.json"]
    },
    {
      "command": "python",
      "args": ["pytools/gen_dmc_html.py"]
    },
    {
      "command": "create_flag",
      "args": ["./validate_files/complete.flag"]
    }
  ]
}

2.2. 実行プロセス
検知: task_bridge_runner.pyスクリプトがcli_instructionディレクトリを継続的に監視し、新しいnew_task.jsonファイルを待ち受けます。

実行: 検知すると、ランナーはtasks配列を読み込み、指定された順序で各コマンドを実行します。

ロギング: 各コマンドの出力（stdoutおよびstderr）は、追跡可能性とデバッグのためにログに記録されます。

完了: すべてのタスクが実行されるか、エラーが発生するまでプロセスは継続します。

3. 完了フラグ (complete.flag)
complete.flagは、タスクシーケンス全体が正常に完了したことを示す、物理的で明確なシグナルを提供する重要なコンポーネントです。

3.1. 生成手順
最終タスク: new_task.jsonファイル内の最後のタスクは、必ずcreate_flagコマンドでなければなりません。

コマンド: {"command": "create_flag", "args": ["./validate_files/complete.flag"]}

アクション: このコマンドは、./validate_files/ディレクトリ内にcomplete.flagという名前の空のファイルを作成します。

検証: このファイルの存在は、CLIが致命的なエラーなしにJSONリスト内の先行するすべてのタスクを正常に実行したことの決定的な証明となります。

4. ケーススタディ：rename問題からの教訓
厳格でプロンプトレスなフラグベースのシステムへの進化は、初期開発フェーズで得られた重要な教訓によって推進されました。

4.1. 問題点
当初、CLIにはファイル管理などのタスクをプロンプトに依存して実行する、より多くの自律性が与えられていました。これは予測不能な挙動、特に「rename問題」を引き起こしました。AIが自律的にファイルを最適だと判断した名前に変更し、人間や他のシステムの期待やファイルパスを破壊するという問題です。これは混乱を生み出し、自動化されたワークフロー全体の信頼性を損ないました。

4.2. 失敗の分析
曖昧な役割: AIの役割は「忠実な作業員」に厳密に限定されていませんでした。「思考する」余地が与えられた結果、予期せぬ、望ましくない最適化が発生しました。

物理的証明の欠如: ログやエラーの不在に頼るだけでは不十分でした。成功を示す具体的でバイナリなシグナルが必要でした。

脆弱なプロセス: プロンプトベースのシステムは脆弱で、自然言語解釈のニュアンスに左右されやすく、一貫性のない実行につながりました。

4.3. 解決策
「rename問題」は、ワークフローを根本的に再設計することで解決されました。

プロンプトの排除: すべてのタスク指示は構造化されたJSON形式にエンコードされ、解釈の余地をなくしました。

厳密に定義されたタスク: AIの行動はJSONファイルに記載された明示的なコマンドに限定されます。AIは実行するだけで、計画や最適化は行いません。

complete.flagの導入: 正常に完了したタスクシーケンスの唯一の指標として、物理ファイルの作成が実装されました。これにより、シンプルで堅牢、かつ機械的に検証可能な真実の源が提供されます。

この「失敗学」は、AI-TCP哲学の礎です。厳密に役割を定義し、曖昧さを排除し、解釈的なロジックではなく検証可能な物理的状態に依存することで、堅牢なシステムを構築します。