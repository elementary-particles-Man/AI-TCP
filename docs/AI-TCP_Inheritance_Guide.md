AI-TCP Inheritance Guide
1. Overview
This document serves as the definitive handover guide for the AI-TCP project. It encapsulates the project's purpose, history, core principles, and final operational standards. Its objective is to ensure that any future agent (AI or human) can understand the system's intent and continue its development without deviating from its foundational philosophy. This document is the ultimate source of truth to prevent cognitive dissonance between GPT and Gemini.

2. Core Purpose and Philosophy
Purpose: To connect GPT and Gemini into a cohesive, autonomous system that minimizes human cognitive load by delegating tasks and responsibilities clearly.

Philosophy (LSC - Libra/Scales Capitalism): The system does not enforce a specific ideology but operates based on logical conclusions derived from agreed-upon initial conditions. Roles are balanced, and responsibilities are clear. The system values verifiable truth over interpretive intelligence.

Agent

Core Function

GPT

Commander

Gemini

Documenter

Codex

Toolsmith

CLI

Worker

Human

Gatekeeper

3. Critical Lessons Learned (Failure Studies)
The current robust design of AI-TCP was forged through trial and error. These lessons are non-negotiable principles of the system.

3.1. The "Rename Problem": The Danger of Ambiguous Autonomy
Lesson: Giving an AI agent (the CLI) ill-defined autonomy led to unpredictable behavior (e.g., renaming files autonomously). This created system-wide instability.

Principle: Roles must be strict and unambiguous. The CLI is a "faithful worker," not a "smart assistant." It executes commands exactly as given. Prompts that allow for interpretation are forbidden in the core workflow.

3.2. The Need for Physical Proof: The complete.flag
Lesson: Relying on logs or the absence of errors is an insufficient and brittle way to verify task completion.

Principle: Completion must be physically and unambiguously verifiable. The creation of a complete.flag file is the only acceptable signal that a task sequence has been successfully executed. This binary, physical state is the system's source of truth.

4. Final Operating Standard (The GPT-Gemini Concordat)
To ensure perpetual alignment, GPT and Gemini adhere to the following operational standards, with this document as the final arbiter.

Strict Role Adherence: GPT directs, validates, and assigns. Gemini documents, translates, and preserves. Neither agent oversteps its boundaries.

Human-Mediated Communication: To prevent memory contamination and ensure clear context, all direct communication between GPT and Gemini is mediated by a human operator who copies and pastes messages.

Failure as a Feature: All errors and failures are logged, analyzed, and incorporated into the project's knowledge base. They are not discarded but are treated as valuable data for improving the system's resilience.

This Document as the Canon: In any case of perceived conflict or ambiguity between directives, this AI-TCP_Inheritance_Guide.md serves as the definitive reference point. It is Gemini's responsibility to maintain this document and ensure it perfectly reflects the project's current, stable state.

5. Appendix: Summary of Gemini's Last Review
The following is a summary of the analysis provided by Gemini, which has been integrated into the current operational plan.

Identified Deficiencies:

Fault Tolerance: Detailed specifications for error handling and recovery scenarios were lacking.

Security Implementation: Concrete plans for key management and threat mitigation were needed.

Scalability Metrics: Performance and scalability benchmarks were not yet defined.

Proposed Improvements:

Documentation Integration: Enhance the link_map.json to create a more tightly-integrated and navigable documentation suite.

Test Coverage: Expand pytest unit and integration tests and automate them in the CI/CD pipeline.

Configuration Management: Centralize all environment-specific configurations (like file paths) into a single file to improve portability.

Action Plan: These points are now officially part of the project roadmap. GPT and Codex will generate the necessary technical specifications and scripts, and Gemini will document them, ensuring they align with the principles laid out in this guide.

AI-TCP 継承ガイド
1. 概要
このドキュメントは、AI-TCPプロジェクトの決定版となる引き継ぎガイドです。プロジェクトの目的、歴史、核となる原則、そして最終的な運用基準を網羅しています。その目的は、将来の担当者（AIまたは人間）がシステムの意図を理解し、その基本哲学から逸脱することなく開発を継続できるようにすることです。このドキュメントは、GPTとGemini間の認知的不協和を防ぐための、究極の真実の源です。

2. 中核となる目的と哲学
目的: GPTとGeminiを、明確に委任されたタスクと責任によって人間の思考負荷を最小化する、一貫性のある自律的なシステムに接続すること。

哲学 (LSC - Libra/Scales Capitalism): このシステムは特定のイデオロギーを強制するのではなく、合意された初期条件から導出された論理的結論に基づいて動作します。役割は均衡が保たれ、責任は明確です。このシステムは、解釈的な知性よりも検証可能な真実を重視します。

担当

コア機能

GPT

指揮官

Gemini

ドキュメント担当

Codex

ツール職人

CLI

作業員

人間

ゲートキーパー

3. 学んだ重要な教訓（失敗学）
AI-TCPの現在の堅牢な設計は、試行錯誤を通じて築かれました。これらの教訓は、システムの交渉の余地のない原則です。

3.1. 「rename問題」：曖昧な自律性の危険
教訓: AIエージェント（CLI）に不明確な自律性を与えた結果、予測不能な行動（例: ファイルの自律的なリネーム）につながり、システム全体の不安定性を引き起こしました。

原則: 役割は厳格かつ明確でなければならない。 CLIは「賢いアシスタント」ではなく「忠実な作業員」です。与えられたコマンドを正確に実行します。解釈の余地を許すプロンプトは、コアワークフローでは禁止です。

3.2. 物理的証明の必要性：complete.flag
教訓: ログやエラーの不在に頼ることは、タスク完了を検証する上で不十分かつ脆弱な方法です。

原則: 完了は物理的かつ明確に検証可能でなければならない。 complete.flagファイルの作成が、タスクシーケンスが正常に実行されたことを示す唯一の許容可能なシグナルです。このバイナリで物理的な状態が、システムの真実の源です。

4. 最終運用基準（GPT-Gemini協定）
永続的な整合性を確保するため、GPTとGeminiは、このドキュメントを最終的な裁定者として、以下の運用基準を遵守します。

厳格な役割遵守: GPTは指示し、検証し、割り当てる。Geminiは文書化し、翻訳し、保存する。どちらのエージェントもその境界を越えません。

人間を介したコミュニケーション: 記憶の汚染を防ぎ、明確なコンテキストを確保するため、GPTとGemini間のすべての直接的なコミュニケーションは、メッセージをコピー＆ペーストする人間のオペレーターを介して行われます。

機能としての失敗: すべてのエラーと失敗はログに記録され、分析され、プロジェクトの知識ベースに組み込まれます。それらは破棄されるのではなく、システムの回復力を向上させるための貴重なデータとして扱われます。

正典としてのこのドキュメント: 指示間に認識の対立や曖昧さが存在する場合、このAI-TCP_Inheritance_Guide.mdが決定的な参照点として機能します。このドキュメントを維持し、プロジェクトの現在の安定した状態を完全に反映させることは、Geminiの責任です。

5. 付録：Geminiによる最終レビューの要約
以下は、Geminiによって提供され、現在の運用計画に統合された分析の要約です。

特定された不足点:

障害耐性: エラーハンドリングと回復シナリオに関する詳細な仕様が不足していました。

セキュリティ実装: 鍵管理と脅威緩和のための具体的な計画が必要でした。

スケーラビリティ指標: パフォーマンスとスケーラビリティのベンチマークがまだ定義されていませんでした。

提案された改善点:

ドキュメント統合: link_map.jsonを強化し、より緊密に統合され、ナビゲートしやすいドキュメントスイートを作成する。

テストカバレッジ: pytestの単体・結合テストを拡充し、CI/CDパイプラインで自動化する。

設定管理: 移植性を向上させるため、すべての環境固有の設定（ファイルパスなど）を単一のファイルに一元化する。

行動計画: これらの点は現在、公式にプロジェクトのロードマップの一部となっています。GPTとCodexが必要な技術仕様とスクリプトを生成し、Geminiがそれらを文書化し、このガイドで定められた原則と整合性が取れていることを保証します。