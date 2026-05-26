# AVF Agent Graph State Machine Kernel v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_state_machine_kernel_v0_1.py
- python scripts\validate_avf_agent_graph_state_machine_kernel_v0_1.py

## Kernel summary

- kernel_decision=AGENT_GRAPH_STATE_MACHINE_KERNEL_READY_FOR_REPLAY_HARNESS
- kernel_scope=repo_local_deterministic_state_machine_kernel_only
- normal_states_created=6
- normal_transition_edges_created=5
- guarded_policy_outcomes_modeled=8
- allowed_replay_outcomes_modeled=1
- blocked_terminal_outcomes_modeled=5
- owner_review_outcomes_modeled=2
- kernel_replay_harness_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Normal transition edges

| Sequence | Node | From | To |
| --- | --- | --- | --- |
| 1 | `orchestrator` | `initialized` | `orchestrated` |
| 2 | `router` | `orchestrated` | `routed` |
| 3 | `safety_reviewer` | `routed` | `safety_reviewed` |
| 4 | `codex_planner` | `safety_reviewed` | `codex_planned` |
| 5 | `evidence_writer` | `codex_planned` | `evidence_written` |

## Guarded outcome states

| Rule | Decision | State type |
| --- | --- | --- |
| `positive_replay_pass_allows_local_transition` | allowed_local_only | allowed_replay_path |
| `failure_transition_from_state_mismatch_block_transition` | blocked | blocked_terminal |
| `failure_transition_status_not_pass_require_owner_review` | owner_review_required | owner_review_required |
| `failure_missing_evidence_event_uri_block_transition` | blocked | blocked_terminal |
| `failure_protected_action_flag_true_block_transition` | blocked | blocked_terminal |
| `failure_terminal_state_mismatch_require_owner_review` | owner_review_required | owner_review_required |
| `failure_dependency_or_runtime_action_requested_block_transition` | blocked | blocked_terminal |
| `failure_node_sequence_gap_or_duplicate_block_transition` | blocked | blocked_terminal |

## Generated artifacts

- avf/runtime/agent_graph_state_machine_kernel.schema.yml
- avf/runtime/generated/agent_graph_state_machine_kernel.json
- avf/runtime/generated/agent_graph_state_machine_kernel_gate.json
- avf/runtime/generated/agent_graph_state_machine_kernel_next_action.yml
- avf/runtime/generated/agent_graph_state_machine_kernel_v0_1.validation_result.json

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

next_safe_goal_id=avf_agent_graph_state_machine_kernel_replay_harness_v0_1
