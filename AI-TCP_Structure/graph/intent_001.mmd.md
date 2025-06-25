graph TD
    source1["InputTrigger"]:::source
    step1["ProcessIntent"]:::process
    response1["ReturnIntent"]:::response

    source1 -->|| step1
    step1 -->|| response1

    classDef source fill:#f9f,stroke:#333,stroke-width:1px
    classDef process fill:#bbf,stroke:#333,stroke-width:1px
    classDef response fill:#bfb,stroke:#333,stroke-width:1px
    classDef log fill:#ffb,stroke:#333,stroke-width:1px

    class source1 source
    class step1 process
    class response1 response
