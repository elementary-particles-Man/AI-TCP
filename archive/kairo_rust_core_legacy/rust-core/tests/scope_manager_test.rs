#[path = "../../../../src/mesh_scope_manager.rs"]
mod mesh_scope_manager;
use mesh_scope_manager::{MeshScopeManager, Scope};

#[test]
fn promotes_scope_when_threshold_met() {
    let next = MeshScopeManager::update_scope_level(0.85, Scope::Personal);
    assert_eq!(next, Some(Scope::Family));
}

#[test]
fn demotes_scope_when_below_threshold() {
    let next = MeshScopeManager::update_scope_level(0.3, Scope::Family);
    assert_eq!(next, Some(Scope::Personal));
}
