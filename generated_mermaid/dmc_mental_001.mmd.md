```mmd
flowchart LR
  root["root"]
  root -->|has| n1["id"]
  root -->|has| n2["timestamp"]
  root -->|has| n3["lang"]
  root -->|has| n4["phase"]
  root -->|has| n5["agent"]
  root -->|has| n6["tags"]
  n6 -->|includes| n7["anxiety"]
  n6 -->|includes| n8["screening"]
  root -->|has| n9["meta"]
  n9 -->|has| n10["version"]
  n9 -->|has| n11["source"]
  root -->|has| n12["data"]
  n12 -->|has| n13["input"]
  n12 -->|has| n14["output"]
```
