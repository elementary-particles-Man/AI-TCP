AI-TCP CLI Specification
1. Overview
This document provides the technical specifications for the AI-TCP Command Line Interface (CLI). The CLI is designed as a "faithful worker," executing a predefined sequence of tasks without deviation. Its reliability is paramount to the entire AI-TCP ecosystem.

2. Core Component: task_bridge_runner.py
The heart of the CLI is the task_bridge_runner.py script. It acts as a daemon that monitors a specific directory for new task instructions and executes them.

2.1. Monitoring Structure
Target Directory: The runner script watches the cli_instruction/ directory located at the repository root.

Target File: It specifically looks for the creation or modification of a file named new_task.json.

Mechanism: It uses a polling mechanism to check for the file's existence at regular intervals. Once found, it processes the file and then awaits the next instruction, preventing duplicate processing of the same file.

2.2. Execution Logic
Read JSON: When new_task.json is detected, the script parses it to load the tasks array.

Sequential Execution: It iterates through the array, executing each task's command with its args in strict order.

Subprocess Management: Each command is executed as a separate subprocess. The runner waits for each subprocess to complete before starting the next one.

Error Handling: If any command returns a non-zero exit code, the runner stops execution and logs the error. It will not proceed to the subsequent tasks.

Archiving: Upon successful completion of all tasks (including create_flag), the new_task.json and its corresponding output log are archived to the cli_archives/ directory with a timestamp to maintain a clean working directory and historical record.

3. Environment Variable: REPO_ROOT
To ensure portability and prevent issues with relative vs. absolute paths, the CLI relies on a REPO_ROOT environment variable.

3.1. Purpose
Path Consistency: REPO_ROOT provides a stable base path to the repository's root directory. All file paths within scripts and tasks should be constructed relative to this root.

Decoupling: It decouples the execution logic from the physical location of the repository on any given machine.

3.2. Usage
Setting the Variable: The user or an environment setup script must set REPO_ROOT to the absolute path of the AI-TCP project directory before running any CLI scripts.

Example (in a script):

import os
repo_root = os.getenv("REPO_ROOT")
instruction_path = os.path.join(repo_root, "cli_instruction", "new_task.json")

4. Conditions for Normal Operation
For the CLI to function correctly, the following conditions must be met:

REPO_ROOT is Set: The REPO_ROOT environment variable must be correctly set to the project's root directory.

Python Environment: A Python environment with all dependencies listed in requirements.txt must be active.

Valid new_task.json: The instruction file must be valid JSON and adhere to the specified task structure. The final task must be create_flag.

File Permissions: The script must have read/write permissions for the cli_instruction/, cli_archives/, vault_output/, and validate_files/ directories.

task_bridge_runner.py is Running: The runner script must be active in the background to monitor for new tasks.

AI-TCP CLI 仕様書
1. 概要
このドキュメントは、AI-TCPコマンドラインインターフェース（CLI）の技術仕様を提供します。CLIは「忠実な作業員」として設計されており、事前定義されたタスクシーケンスを逸脱することなく実行します。その信頼性は、AI-TCPエコシステム全体にとって最も重要です。

2. コアコンポーネント: task_bridge_runner.py
CLIの中心はtask_bridge_runner.pyスクリプトです。これは、特定のディレクトリを監視して新しいタスク指示を検出し、それを実行するデーモンのように機能します。

2.1. 監視構造
ターゲットディレクトリ: ランナースクリプトは、リポジトリのルートにあるcli_instruction/ディレクトリを監視します。

ターゲットファイル: 具体的には、new_task.jsonという名前のファイルの作成または変更を探索します。

メカニズム: ポーリングメカニズムを使用して、一定間隔でファイルの存在を確認します。ファイルが見つかると処理し、同じファイルの重複処理を防ぐために次の指示を待ちます。

2.2. 実行ロジック
JSON読み込み: new_task.jsonが検出されると、スクリプトはそれを解析してtasks配列を読み込みます。

順次実行: 配列を反復処理し、各タスクのcommandをそのargsと共に厳密な順序で実行します。

サブプロセス管理: 各コマンドは個別のサブプロセスとして実行されます。ランナーは、次のタスクを開始する前に各サブプロセスが完了するのを待ちます。

エラーハンドリング: いずれかのコマンドがゼロ以外の終了コードを返した場合、ランナーは実行を停止し、エラーをログに記録します。後続のタスクには進みません。

アーカイブ: すべてのタスク（create_flagを含む）が正常に完了すると、new_task.jsonとそれに対応する出力ログがタイムスタンプ付きでcli_archives/ディレクトリにアーカイブされ、クリーンな作業ディレクトリと履歴が維持されます。

3. 環境変数: REPO_ROOT
移植性を確保し、相対パスと絶対パスの問題を防ぐため、CLIはREPO_ROOT環境変数に依存します。

3.1. 目的
パスの一貫性: REPO_ROOTは、リポジトリのルートディレクトリへの安定したベースパスを提供します。スクリプトやタスク内のすべてのファイルパスは、このルートを基準に構築されるべきです。

分離: 実行ロジックを、特定のマシン上でのリポジトリの物理的な場所から分離します。

3.2. 使用方法
変数の設定: ユーザーまたは環境設定スクリプトは、CLIスクリプトを実行する前に、REPO_ROOTをAI-TCPプロジェクトディレクトリの絶対パスに設定する必要があります。

使用例（スクリプト内）:

import os
repo_root = os.getenv("REPO_ROOT")
instruction_path = os.path.join(repo_root, "cli_instruction", "new_task.json")

4. 正常稼働の条件
CLIが正しく機能するためには、以下の条件が満たされている必要があります。

REPO_ROOTが設定されていること: REPO_ROOT環境変数がプロジェクトのルートディレクトリに正しく設定されていなければなりません。

Python環境: requirements.txtにリストされているすべての依存関係を持つPython環境がアクティブである必要があります。

有効なnew_task.json: 指示ファイルは有効なJSONであり、指定されたタスク構造に従っている必要があります。最後のタスクはcreate_flagでなければなりません。

ファイルパーミッション: スクリプトはcli_instruction/、cli_archives/、vault_output/、およびvalidate_files/ディレクトリに対する読み取り/書き込み権限を持っている必要があります。

task_bridge_runner.pyが実行中であること: 新しいタスクを監視するために、ランナースクリプトがバックグラウンドでアクティブである必要があります。