```mermaid
flowchart TD
  DR[DRユニットによる兆候検知] --> GPT[統合判断]
  GPT --> Gemini[ナラティブ構築]
  Gemini --> GitPush[PoC格納]
  GitPush --> RFC[公開整備]
```
