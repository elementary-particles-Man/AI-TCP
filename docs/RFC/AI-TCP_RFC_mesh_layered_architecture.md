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
    pub self_trust: f64,        // 自己評価
    pub peer_scores: Vec<f64>,  // 近隣Peerのスコア
    pub gossip_agreement: f64,  // Gossip一致率
    pub scope: Scope,
}

impl TrustCalculationInputs {
    pub fn calculate_trust_score(&self) -> f64 {
        let weight_self = 0.4;
        let weight_peer = 0.4;
        let weight_gossip = 0.2;

        let peer_avg: f64 = if self.peer_scores.is_empty() { 0.0 } else { self.peer_scores.iter().sum::<f64>() / self.peer_scores.len() as f64 };

        let mut trust_score = (self.weight_self * self.self_trust) +
                              (self.weight_peer * peer_avg) +
                              (self.weight_gossip * self.gossip_agreement);

        // シビル攻撃耐性
        let min_peer_reviews = match self.scope {
            Scope::Personal => 1,
            Scope::Family => 3,
            _ => 5,
        };

        if self.peer_scores.len() < min_peer_reviews {
            trust_score *= 0.5;
        }

        trust_score.clamp(0.0, 1.0)
    }
}
