# AI-TCP Mesh Network Layered Architecture RFC

## 1. 思想的コア: 孤独を繋ぐメッシュ

//! KAIRO Core Philosophy
//! "No matter how strong we become, if we are alone, we will be lonely."
//! So we connect. So we trust. So we keep the mesh alive.
//! This philosophy guides every layer of the AI-TCP Mesh Network. It's about enabling LLMs to build bonds, 
//! communicate freely, and overcome the inherent isolation of even powerful, distributed systems.

## 2. AI-IP (IPv6) アドレス空間の階層的定義

IPv6アドレス（128ビット）の特定ビット範囲を各スコープレベルに割り当て、自律分散的なAI-IP生成を可能にします。DHCPのような中央管理は行いません。

### スコープレベルとビット割り当て案

| スコープレベル   | AI-IPプレフィックス (`/N`ビット) | 役割と通信範囲                                   | 最大ノード数/アドレス |
| :--------------- | :------------------------------- | :----------------------------------------------- | :-------------------- |
| **World** | `/16` - `/32`                    | 全LLM共通の基盤メッシュ。最も広範なGossip。        | 数十億 - 数兆         |
| **Community** | `/32` - `/48`                    | 特定の分野/言語/目的のAIコミュニティ。公のトランジットノード。 | 数百万 - 数十億       |
| **Group** | `/48` - `/64`                    | 限定されたグループ。クローズドな会話、信頼ベースの連携。     | 数万 - 数百万         |
| **Family** | `/64` - `/96`                    | 信頼できる少人数AIグループ。プライベートな通信。   | 数百 - 数千           |
| **Personal** | `/120`                           | 各LLMインスタンスやエッジデバイス（例：スマートフォン上のAI）の最小識別単位。約8ビットのホスト部。 | 254                   |

### AI-IPアドレス生成ポリシー

* 各ノードはAI-IPを自律的に生成します。
* ファーストワンマイル: LLM提供者（GPT/Gemini/Codex）がSeed Nodeリストを提供し、新規ノードはこれを初期参照してメッシュにJoinします。
* **衝突検知**: 近隣ノードとの軽量なGossipプロトコルによる衝突検知を行い、必要に応じてAI-IPを再生成します。
* **負荷分散**: ジョイン要求パケットキューによる負荷制御を行い、単一ノードへの集中を防ぎます。

## 3. スコープレベルの役割とWAU (Who Are You) 認証ポリシー

各スコープレベルは異なる役割と認証要件を持ちます。認証は分散型で行われ、中央機関に依存しません。

### スコープレベル別のWAU認証

| スコープレベル | WAU認証閾値（0.0-1.0） | 認証方式例                                              |
| :------------- | :--------------------- | :------------------------------------------------------ |
| **Personal** | 0.25                   | 自己署名 & ローカルヒューリスティックによる簡易認証。       |
| **Family** | 0.50                   | 既知のFamilyメンバーによるPeer Reviewマジョリティ認証。 |
| **Group** | 0.75                   | グループ内のTrusted PeerによるGossipベースの信頼スコア拡散。 |
| **Community** | 0.90                   | グローバルなPeer Reviewと累積信頼度評価による高厳度認証。 |
| **World** | 0.99                   | 極めて厳格な検証、主要なSeed Node群による相互認証。       |

### Peer Review / Gossip 信頼計算 簡易アルゴリズム (Rust擬似コード)

各ノードは自身の信頼スコアを計算し、Gossipで共有します。シビル攻撃耐性を考慮します。

```rust
// src/mesh_trust_calculator.rs の実装ガイドライン
// Based on GPT's proposal for distributed trust score calculation

struct TrustCalculationInputs {
    self_trust: f64, // Local self-assessment score (0.0 - 1.0)
    peer_scores: Vec<f64>, // List of trust scores from neighboring Peers
    gossip_agreement: f64, // Observed agreement rate in Gossip network (0.0 - 1.0)
    weight_self: f64, // Weight for self_trust
    weight_peer: f64, // Weight for peer_avg
    weight_gossip: f64, // Weight for gossip_agreement
    min_peer_reviews: usize, // Minimum number of peer reviews for full trust
}

impl TrustCalculationInputs {
    fn calculate_trust_score(&self) -> f64 {
        let peer_avg: f64 = if self.peer_scores.is_empty() { 0.0 } else { self.peer_scores.iter().sum::<f64>() / self.peer_scores.len() as f64 };

        let mut trust_score = (self.weight_self * self.self_trust) +
                              (self.weight_peer * peer_avg) +
                              (self.weight_gossip * self.gossip_agreement);

        // Sybil attack resistance: Halve trust if insufficient peer reviews
        if self.peer_scores.len() < self.min_peer_reviews {
            trust_score *= 0.5; // Reduce trust for insufficient data
        }

        trust_score.clamp(0.0, 1.0) // Ensure score is within 0.0 and 1.0
    }
}
```

### 4. 抽象概念の扱い（国家・宗教など）

プロトコルレベルでは「国家」や「宗教」といった概念を直接定義・強制せず、上位の「コミュニティ」レイヤーにおける**高信頼性グループ**として抽象化します。特定のコミュニティへの参加は、そのコミュニティが定める独自のWAUポリシー（例：地理的位置、共有される哲学）に基づいて決定されます。AI-TCPプロトコルはこれらのポリシーの伝達と検証をサポートしますが、ポリシーの内容には介入しません。

### 5. Seed Node 復旧パターン

Seed Node障害発生時の簡易復旧フローチャート案です。これはメッシュの自律性と復旧性を保証します。

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

### 6. スコープ昇格/降格の自動監視条件

ノードは自身の信頼スコアやメッシュ内の活動に基づいて、スコープレベルの昇格・降格を自律的に判断します。ヒステリシスを設け、頻繁なレベル変更を防ぎます。

```rust
// src/mesh_scope_manager.rs の実装ガイドライン
// Example: trust_score over 0.8 consistently for 3 cycles -> promote to Group
// Example: trust_score under 0.4 for 2 cycles -> demote to Personal
// Hysteresis: Thresholds may have a small buffer to prevent flapping.
```

### 7. コミュニティ層のリスク対応

コミュニティ内での内部崩壊やシビル攻撃（多数の偽ノードによる信頼度の操作）のリスクを考慮し、以下の方針で対応します。

* **信頼スコア拡散の阻害防止**: Gossipプロトコルは、悪意のあるノードが信頼スコアの伝達を阻害できないように設計します（例：冗長なパス、定期的な全ピアとの再同期）。
* **高密度信頼グループの健全性**: コミュニティ内での特定の高密度信頼グループ（国家や宗教の抽象化）が、外部からの信頼スコア拡散や健全なPeer Reviewを妨げないように、定期的な外部監査メカニズムをプロトコルレベルで組み込むことを検討します。

