graph TD
    ai_agent_1["AI Agent 1"]:::source
    ai_agent_2["AI Agent 2"]:::source
    negotiation_module["Negotiation Engine"]:::process
    consensus_validator["Consensus Validator"]:::process
    outcome_response["Final Response"]:::response

    ai_agent_1 -->|| negotiation_module
    ai_agent_2 -->|| negotiation_module
    negotiation_module -->|| consensus_validator
    consensus_validator -->|| outcome_response

    classDef source fill:#f9f,stroke:#333,stroke-width:1px
    classDef process fill:#bbf,stroke:#333,stroke-width:1px
    classDef response fill:#bfb,stroke:#333,stroke-width:1px
    classDef log fill:#ffb,stroke:#333,stroke-width:1px

    class ai_agent_1 source
    class ai_agent_2 source
    class negotiation_module process
    class consensus_validator process
    class outcome_response response
