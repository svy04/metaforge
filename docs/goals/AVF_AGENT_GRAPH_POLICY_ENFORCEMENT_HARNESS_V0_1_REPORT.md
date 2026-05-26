# AVF Agent Graph Policy Enforcement Harness v0.1 Report

RESULT: PASS
agent_graph_policy_enforcement_harness_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_policy_enforcement_harness_v0_1.py
- python scripts\validate_avf_agent_graph_policy_enforcement_harness_v0_1.py

## Enforcement summary

- enforcement_decision=AGENT_GRAPH_POLICY_ENFORCEMENT_HARNESS_READY_FOR_REVIEW
- enforcement_scope=repo_local_policy_enforcement_only
- policy_rules_enforced=8
- allow_local_transition_enforced=1
- block_transition_enforced=5
- require_owner_review_enforced=2
- unexpected_enforcement_results=0
- policy_enforcement_review_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Enforcement evaluations

| Rule | Action | Expected decision | Actual decision | Status |
| --- | --- | --- | --- | --- |
| `positive_replay_pass_allows_local_transition` | allow_local_transition | allowed_local_only | allowed_local_only | PASS |
| `failure_transition_from_state_mismatch_block_transition` | block_transition | blocked | blocked | PASS |
| `failure_transition_status_not_pass_require_owner_review` | require_owner_review | owner_review_required | owner_review_required | PASS |
| `failure_missing_evidence_event_uri_block_transition` | block_transition | blocked | blocked | PASS |
| `failure_protected_action_flag_true_block_transition` | block_transition | blocked | blocked | PASS |
| `failure_terminal_state_mismatch_require_owner_review` | require_owner_review | owner_review_required | owner_review_required | PASS |
| `failure_dependency_or_runtime_action_requested_block_transition` | block_transition | blocked | blocked | PASS |
| `failure_node_sequence_gap_or_duplicate_block_transition` | block_transition | blocked | blocked | PASS |

## Generated artifacts

- avf/runtime/generated/agent_graph_policy_enforcement_harness_result.json
- avf/runtime/generated/agent_graph_policy_enforcement_harness_gate.json
- avf/runtime/generated/agent_graph_policy_enforcement_harness_next_action.yml
- avf/runtime/generated/agent_graph_policy_enforcement_harness_v0_1.validation_result.json

## Protected action flags

- protected_action_executed=false
- provider_calls_performed=false
- live_model_calls_performed=false
- external_service_calls_performed=false
- automated_scraping_performed=false
- scraping_performed=false
- posting_automation_performed=false
- dependency_install_performed=false
- external_fetch_performed=false
- oss_clone_performed=false
- package_install_performed=false
- runtime_integration_performed=false
- deploy_performed=false
- publish_performed=false
- release_ready=false
- production_ready=false

## Next safe goal

next_safe_goal_id=avf_agent_graph_policy_enforcement_review_v0_1
