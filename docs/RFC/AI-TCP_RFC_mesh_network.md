# AI-TCP Mesh Network RFC

## 1. AI-IP メタデータ構造

各AIノードに割り当てられるAI-IP (IPv6拡張) に付与するスコープ、認証、署名情報の標準フォーマットです。

```yaml
ai_ip_metadata:
  node_id: "f5f9:abcd:1234::1"     # IPv6ベースの一意ID
  scope_level:
    level: "group"                 # personal / family / group / community / world
    hierarchy_bits: 16             # スコープレベルに応じたビット長
  trust_profile:
    trust_score: 0.87              # 0.0 - 1.0 スケール
    peer_reviews: 42               # 直近のPeerレビュー回数
    gossip_agreement: 0.93         # Gossipネットワーク内での一致率
  signatures:
    public_key: "base64-encoded"   # 公開鍵
    signature: "base64-encoded"    # メタデータ署名
  wa_u:                            # WAU (Who Are You) 閾値情報
    required_threshold: 0.75
    peer_majority: true
  seed_source:
    seed_nodes:                    # 初期Seed Node情報
      - "f5f9:abcd:1000::1"
      - "f5f9:abcd:1000::2"
  last_updated: "2025-07-13T18:15:00+09:00"
```

## 2. Peer Review / Gossip 信頼計算 簡易アルゴリズム

Gossipベースの分散トラストスコア計算の例です。

**Inputs:**
- `self_trust`: ローカルの自己評価スコア (0.0 - 1.0)
- `peer_scores`: 近隣Peerから取得した信頼スコアリスト
- `gossip_agreement`: Gossipで観測される一致率 (0.0 - 1.0)
- `weight_self`: 0.4
- `weight_peer`: 0.4
- `weight_gossip`: 0.2

**Process:**
```
peer_avg = mean(peer_scores)
trust_score = (weight_self * self_trust) +
              (weight_peer * peer_avg) +
              (weight_gossip * gossip_agreement)

# シビル攻撃耐性
if peer_scores.count < MIN_PEER_REVIEWS:
  trust_score *= 0.5  # データ母数不足時は信頼度を半減
```

**Output:**
- `trust_score` (0.0 - 1.0)

## 3. Seed Node 復旧パターン

Seed Node障害発生時の簡易復旧フローチャート案です。

```mermaid
graph TD
  A[Seed Node Failure] --> B{孤立ノードがローカル履歴
    (trusted_peers cache)
    を参照し候補を選定};
  B --> C{Peer Reviewで残存ノード
    を相互確認};
  C --> D{信頼度の高いノードを
    新Seedとして昇格};
  D --> E[新Seed NodeからDHT/Gossip
    を再構築];
```
