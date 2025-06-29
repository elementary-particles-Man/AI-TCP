AI-TCP Test Structure
1. Overview
This document defines the testing structure for the AI-TCP project. A robust and multi-layered testing strategy is crucial for ensuring the reliability of the autonomous cooperation between different AI agents and environments.

2. Testing Environments
The AI-TCP system must be validated across various environments to ensure its flexibility and robustness.

2.1. Local LLM (via LM Studio)
Purpose: To test the core logic of AI-TCP with locally hosted models, ensuring functionality without reliance on external APIs or internet connectivity.

Setup:

Install LM Studio.

Download a compatible model (e.g., a GGUF version of a Llama or Mistral model).

Start the local server from the LM Studio UI.

Test Execution:

Scripts designed to interact with LLMs (e.g., for generating document drafts or code snippets) will be configured to point to the local LM Studio server endpoint (e.g., http://localhost:1234/v1).

This setup is ideal for rapid, low-cost testing of agent interaction protocols.

2.2. Remote API (e.g., Gemini, GPT)
Purpose: To test the system in its intended production environment, interacting with powerful, remotely-hosted foundation models.

Setup:

Obtain API keys for the respective services (e.g., Google AI Studio, OpenAI Platform).

Store keys securely using environment variables or a secrets management system.

Test Execution:

Scripts will use the official client libraries or REST APIs to send requests.

Tests in this environment focus on end-to-end workflow validation, including handling of API-specific errors, rate limits, and data formats.

2.3. Simulated Network Conditions (Wi-Fi)
Purpose: To test the system's resilience to unreliable network conditions.

Setup:

Run different components (e.g., the CLI runner and a local LLM server) on different machines connected via Wi-Fi.

Network simulation tools can be used to artificially introduce latency, jitter, or packet loss.

Test Execution:

Focus on timeout handling, retry mechanisms, and the system's ability to recover from transient communication failures.

3. Automated Task Generation for Testing
To streamline testing, the process of creating new_task.json files should be automated.

Script: A dedicated script (e.g., generate_new_task.py) is responsible for this.

Functionality:

Takes a task name or template as input.

Dynamically constructs a valid new_task.json file with the appropriate commands and arguments.

Places the file in the cli_instruction/ directory to trigger a test run.

Benefit: This allows for the rapid creation of repeatable test cases, forming the basis of a continuous integration (CI) pipeline.

4. Physical Verification of Completion
The final step of any successful test is the physical verification of the output artifacts. This provides undeniable proof of success.

validate_files/ Directory: This directory acts as a staging area for critical output validation.

Verification Steps:

Check for complete.flag: The primary check is the existence of the ./validate_files/complete.flag file. A test script can poll for this file.

# Example check in a test script
import os, time
flag_path = os.path.join(os.getenv("REPO_ROOT"), "validate_files", "complete.flag")
timeout = 60 # seconds
start_time = time.time()
while not os.path.exists(flag_path):
    if time.time() - start_time > timeout:
        raise TimeoutError("Test failed: complete.flag was not created.")
    time.sleep(1)
print("Test passed: complete.flag found.")
os.remove(flag_path) # Clean up for next test

Inspect Other Artifacts: Depending on the test case, scripts should also validate the contents of other files generated in validate_files/ or vault_output/. This could involve checking file integrity (checksums), content correctness (schema validation), or other business logic.

This physical verification model ensures that a test's success is based on tangible outcomes, not just the absence of errors in a log stream, making the entire system more robust and trustworthy.

AI-TCP テスト構造
1. 概要
このドキュメントは、AI-TCPプロジェクトのテスト構造を定義します。堅牢で多層的なテスト戦略は、異なるAIエージェントと環境間での自律的な協調の信頼性を確保するために不可欠です。

2. テスト環境
AI-TCPシステムは、その柔軟性と堅牢性を保証するために、さまざまな環境で検証されなければなりません。

2.1. ローカルLLM (LM Studio経由)
目的: 外部APIやインターネット接続に依存せず、ローカルでホストされたモデルを使用してAI-TCPのコアロジックをテストし、機能性を確保するため。

セットアップ:

LM Studioをインストールします。

互換性のあるモデル（例: LlamaやMistralモデルのGGUF版）をダウンロードします。

LM StudioのUIからローカルサーバーを起動します。

テスト実行:

LLMと対話するように設計されたスクリプト（例: ドキュメント草案やコードスニペットの生成用）は、ローカルのLM Studioサーバーエンドポイント（例: http://localhost:1234/v1）を指すように設定されます。

このセットアップは、エージェント間の対話プロトコルの迅速で低コストなテストに最適です。

2.2. リモートAPI (例: Gemini, GPT)
目的: 強力なリモートホスト型基盤モデルと対話する、意図された本番環境でシステムをテストするため。

セットアップ:

各サービス（例: Google AI Studio, OpenAI Platform）のAPIキーを取得します。

環境変数やシークレット管理システムを使用して、キーを安全に保管します。

テスト実行:

スクリプトは、公式のクライアントライブラリまたはREST APIを使用してリクエストを送信します。

この環境でのテストは、API固有のエラー、レート制限、データ形式の処理を含む、エンドツーエンドのワークフロー検証に焦点を当てます。

2.3. 擬似ネットワーク条件 (Wi-Fi)
目的: 信頼性の低いネットワーク条件下でのシステムの回復力をテストするため。

セットアップ:

異なるコンポーネント（例: CLIランナーとローカルLLMサーバー）を、Wi-Fi経由で接続された異なるマシンで実行します。

ネットワークシミュレーションツールを使用して、人為的に遅延、ジッター、またはパケット損失を導入できます。

テスト実行:

タイムアウト処理、リトライメカニズム、および一時的な通信障害から回復するシステムの能力に焦点を当てます。

3. テスト用のタスク自動生成
テストを効率化するため、new_task.jsonファイルの作成プロセスを自動化すべきです。

スクリプト: 専用のスクリプト（例: generate_new_task.py）がこの役割を担います。

機能:

タスク名またはテンプレートを入力として受け取ります。

適切なコマンドと引数を持つ有効なnew_task.jsonファイルを動的に構築します。

テスト実行をトリガーするために、ファイルをcli_instruction/ディレクトリに配置します。

利点: これにより、再現可能なテストケースの迅速な作成が可能になり、継続的インテグレーション（CI）パイプラインの基盤を形成します。

4. 完了の物理的検証
成功したテストの最終ステップは、出力成果物の物理的な検証です。これは、成功の否定できない証拠を提供します。

validate_files/ ディレクトリ: このディレクトリは、重要な出力検証のための一時保管エリアとして機能します。

検証ステップ:

complete.flagの確認: 主要なチェックは、./validate_files/complete.flagファイルの存在です。テストスクリプトは、このファイルをポーリングできます。

# テストスクリプト内のチェック例
import os, time
repo_root = os.getenv("REPO_ROOT")
flag_path = os.path.join(repo_root, "validate_files", "complete.flag")
timeout = 60 # 秒
start_time = time.time()
while not os.path.exists(flag_path):
    if time.time() - start_time > timeout:
        raise TimeoutError("Test failed: complete.flag was not created.")
    time.sleep(1)
print("Test passed: complete.flag found.")
os.remove(flag_path) # 次のテストのためにクリーンアップ

他の成果物の検査: テストケースに応じて、スクリプトはvalidate_files/またはvault_output/で生成された他のファイルの内容も検証する必要があります。これには、ファイルの整合性（チェックサム）、内容の正しさ（スキーマ検証）、またはその他のビジネスロジックのチェックが含まれる場合があります。

この物理的な検証モデルは、テストの成功がログストリームのエラーの不在だけでなく、具体的な成果物に基づいていることを保証し、システム全体をより堅牢で信頼性の高いものにします。