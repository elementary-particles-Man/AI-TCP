# Autonomous Negotiation Flow (PoC #008)

*ファイルパス: `AI-TCP_Structure/playground/negotiation_logs/negotiation_008.mmd.md`*

```mermaid
flowchart TD
    %% --- クラス定義 ---
    classDef gptAgent fill:#dbeafe,stroke:#1e40af,color:#1e293b;
    classDef gemmaAgent fill:#dcfce7,stroke:#15803d,color:#1e293b;
    classDef mediatorAgent fill:#e5e7eb,stroke:#4b5563,color:#1e293b;

    %% --- サブグラフ定義 ---
    subgraph "Phase 1: Initial Proposals (T+0s)"
        AgentA["Agent A (GPT)<br><b>Creative-AI</b>"]:::gptAgent
        AgentB["Agent B (Gemma 3)<br><b>Maintenance-AI</b>"]:::gemmaAgent
        
        ProposalA(Proposal: `timestamp.md`<br>Reason: Speed)
        ProposalB(Proposal: `semantic_name.md`<br>Reason: Readability)

        AgentA --> ProposalA
        AgentB --> ProposalB
    end

    subgraph "Phase 2: Mediation (T+1s to T+3s)"
        MediatorC["Agent C (Gemini)<br><b>Mediator-AI</b>"]:::mediatorAgent
        
        ConflictPoint{Conflict Detected<br>Resource: `filename_convention`}
        
        ProposalA --> ConflictPoint
        ProposalB --> ConflictPoint
        
        ConflictPoint -- "Sends `interrupt` signal" --> AgentA
        ConflictPoint -- "Sends `interrupt` signal" --> AgentB
        
        MediatorC -- "Analyzes both proposals" --> ResolutionGraph(Resolution Graph<br>Proposal: `YYYYMMDD_semantic_name.md`)
    end
    
    subgraph "Phase 3: Final Agreement (T+5s)"
        FinalAgreement[Final Agreement<br>Compromise Reached]
        
        ResolutionGraph --> FinalAgreement
        AgentA -- "Sends `ack`" --> FinalAgreement
        AgentB -- "Sends `ack`" --> FinalAgreement
    end

