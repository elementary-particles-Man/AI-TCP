flowchart TD
    subgraph "PoC Phase 2 Workflow"
        A[1. Define Intent<br>(YAML Structure)] --> B[2. Generate Visual Model<br>(Mermaid Graph)];
        B --> C[3. Create Human-Readable<br>(Intent Narrative)];
        C --> D[4. Reverse-Reception Test<br>(Reconstruct YAML)];
        D --> E[5. Evaluate<br>(Based on GG06 Metrics)];
    end
