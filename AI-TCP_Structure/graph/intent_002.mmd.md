# Intent 002: ファイル生成タスクのフロー

```mermaid
graph TD
    A[タスク要求: new_task.json<br/>task_type: generate_file] --> B{Gemini CLI Agent};
    B --> C{ファイル生成モジュール};
    C --成功--> D[ファイル書き出し<br/>/path/to/new_file.txt];
    C --失敗--> E[エラーログ出力<br/>output.json];
    D --> F[成功ログ出力<br/>output.json];
