# 🗺️ AI-TCP Project Structure (Graph View)

This diagram shows the logical structure of the AI-TCP project and the relation between its core components.

```mermaid
graph TD
    A[AI-TCP Root] --> B[docs/]
    B --> B1[rfc_drafts/]
    B --> B2[dmc_sessions/]
    B --> B3[assets/]
    B --> B4[README.md]
    
    B1 --> B1_0[000_rfc_index.md]
    B1 --> B1_1[001_ai_tcp_overview.md]
    B1 --> B1_2[002_llm_compliance.md]
    B1 --> B1_3[003_packet_definition.md]
    B1 --> B1_4[004_thought_logging.md]

    B2 --> B2_1[YAML: dmc_mental_001.yaml]
    B2 --> B2_2[HTML: dmc_mental_001.html]

    B3 --> B3_1[Mermaid Graphs]
    B3 --> B3_2[Embedded Diagrams]

    A --> C[structured_yaml/]
    C --> C1[validated_yaml/]
    C --> C2[README.md]

    A --> D[scripts/]
    D --> D1[gen_dmc_html.py]

    A --> E[generated_html/]
