# AI-TCP Scope Transition RFC

This RFC defines how a node moves between Personal, Family, Group, Community and World scopes. Implementation details reside in `src/mesh_scope_manager.rs`.

## Trust Score Thresholds

```
Personal -> Family   : >= 0.8
Family   -> Group    : >= 0.85
Group    -> Community: >= 0.9
Community-> World    : >= 0.95
```

Demotions occur when the score drops well below the same thresholds.

## Hysteresis Rules

Scope updates only trigger if a threshold is met for multiple cycles. The manager stores recent scores to avoid oscillation. See the `update_scope_level` logic for examples of promotion and demotion checks.
