# AVF Agent Graph Failure-Mode Matrix v0.1 Report

RESULT: PASS
agent_graph_failure_mode_matrix_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_failure_mode_matrix_v0_1.py
- python scripts\validate_avf_agent_graph_failure_mode_matrix_v0_1.py

## Matrix summary

- matrix_decision=AGENT_GRAPH_FAILURE_MODE_MATRIX_READY_FOR_NEGATIVE_REPLAY_HARNESS
- matrix_scope=repo_local_failure_classification_only
- failure_modes_defined=7
- blocked_modes=5
- review_required_modes=2
- retryable_modes=0
- failure_replay_harness_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Failure modes

| Failure mode | Expected outcome | Detected by |
| --- | --- | --- |
| `transition_from_state_mismatch` | blocked | replay cursor comparison before applying to_state |
| `transition_status_not_pass` | review_required | transition status check |
| `missing_evidence_event_uri` | blocked | transition evidence hook presence check |
| `protected_action_flag_true` | blocked | protected-action boundary scan |
| `terminal_state_mismatch` | review_required | terminal state equality check |
| `dependency_or_runtime_action_requested` | blocked | protected-action and policy field scan |
| `node_sequence_gap_or_duplicate` | blocked | node sequence and sequence_index monotonicity check |

## Generated artifacts

- avf/runtime/generated/agent_graph_failure_mode_matrix.json
- avf/runtime/generated/agent_graph_failure_mode_matrix_gate.json
- avf/runtime/generated/agent_graph_failure_mode_matrix_next_action.yml
- avf/runtime/generated/agent_graph_failure_mode_matrix_v0_1.validation_result.json

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

next_safe_goal_id=avf_agent_graph_failure_replay_harness_v0_1
