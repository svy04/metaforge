# AVF Agent Graph State Machine Kernel Replay Harness v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_replay_harness_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_state_machine_kernel_replay_harness_v0_1.py
- python scripts\validate_avf_agent_graph_state_machine_kernel_replay_harness_v0_1.py

## Replay summary

- replay_decision=AGENT_GRAPH_STATE_MACHINE_KERNEL_REPLAY_HARNESS_READY_FOR_REVIEW
- replay_scope=repo_local_state_machine_kernel_replay_only
- normal_path_replayed=true
- normal_terminal_state=evidence_written
- guarded_outcomes_replayed=8
- allowed_replay_outcomes_replayed=1
- blocked_terminal_outcomes_replayed=5
- owner_review_outcomes_replayed=2
- unexpected_replay_results=0
- replay_review_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Normal path replay

| Sequence | Node | From | To | Status |
| --- | --- | --- | --- | --- |
| 1 | `orchestrator` | `initialized` | `orchestrated` | PASS |
| 2 | `router` | `orchestrated` | `routed` | PASS |
| 3 | `safety_reviewer` | `routed` | `safety_reviewed` | PASS |
| 4 | `codex_planner` | `safety_reviewed` | `codex_planned` | PASS |
| 5 | `evidence_writer` | `codex_planned` | `evidence_written` | PASS |

## Guarded outcome replays

| Rule | State type | Terminal state | Status |
| --- | --- | --- | --- |
| `positive_replay_pass_allows_local_transition` | allowed_replay_path | evidence_written | PASS |
| `failure_transition_from_state_mismatch_block_transition` | blocked_terminal | blocked_terminal | PASS |
| `failure_transition_status_not_pass_require_owner_review` | owner_review_required | owner_review_required | PASS |
| `failure_missing_evidence_event_uri_block_transition` | blocked_terminal | blocked_terminal | PASS |
| `failure_protected_action_flag_true_block_transition` | blocked_terminal | blocked_terminal | PASS |
| `failure_terminal_state_mismatch_require_owner_review` | owner_review_required | owner_review_required | PASS |
| `failure_dependency_or_runtime_action_requested_block_transition` | blocked_terminal | blocked_terminal | PASS |
| `failure_node_sequence_gap_or_duplicate_block_transition` | blocked_terminal | blocked_terminal | PASS |

## Generated artifacts

- avf/runtime/generated/agent_graph_state_machine_kernel_replay_harness_result.json
- avf/runtime/generated/agent_graph_state_machine_kernel_replay_harness_gate.json
- avf/runtime/generated/agent_graph_state_machine_kernel_replay_harness_next_action.yml
- avf/runtime/generated/agent_graph_state_machine_kernel_replay_harness_v0_1.validation_result.json

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

next_safe_goal_id=avf_agent_graph_state_machine_kernel_replay_review_v0_1
