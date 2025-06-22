### 🧭 **[G6] `docs/poc_scenario.md`：PoC実演シナリオマニュアル**

```markdown
# 🧪 AI-TCP PoC Scenario Manual

## Scenario 1: 意図共有と構造解釈

1. `dmc_mental_001.yaml` を送信（sender.py）
2. 受信側（receiver.py）が graph_payload を抽出し Mermaid図で描画
3. reasoning_trace に従ってステップ実行
4. auto_redirect で応答または分岐提案を返す

## Scenario 2: Graph合意失敗による再送

- `reasoning_trace` に `feedback: "graph mismatch"` を挿入
- senderが再送用の graph_payload を修正し送信
- 受信側が再評価後、auto_redirectで承認応答を返す

## Scenario 3: 合意形成ループ

- traceが `step: propose` → `reject` → `revise` → `agree` の流れを経る
- `graph_payload` が逐次変化することで、合意へ至る構造を描く

## 実行コマンド例

```bash
python tools/graph_sender.py dmc_sessions/dmc_mental_001.yaml
python tools/graph_receiver.py input/packet001.yaml
