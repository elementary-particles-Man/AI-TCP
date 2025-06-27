# Intent 003: API連携タスクのフロー

```mermaid
graph TD
    subgraph GPTによる事前定義
        A[タスク要求: new_task.json<br/>task_type: call_remote_api]
    end

    subgraph Gemini CLI Agentによる実行
        B{タスク受信・検証};
        C{APIクライアント};
        D[HTTPリクエスト送信];
        E{レスポンス解析};
        F[結果をoutput.jsonへ記録];
    end

    A --> B;
    B --> C;
    C --> D;
    D --> E;
    E --> F;
