# AVF Agent Graph Failure Replay Harness v0.1 Report

RESULT: PASS
agent_graph_failure_replay_harness_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_failure_replay_harness_v0_1.py
- python scripts\validate_avf_agent_graph_failure_replay_harness_v0_1.py

## Harness summary

- harness_decision=AGENT_GRAPH_FAILURE_REPLAY_HARNESS_READY_FOR_GUARDED_POLICY
- harness_scope=repo_local_negative_replay_only
- negative_fixtures_created=7
- negative_replays_evaluated=7
- blocked_outcomes=5
- review_required_outcomes=2
- unexpected_outcomes=0
- guarded_transition_policy_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Negative replay evaluations

| Failure mode | Expected outcome | Actual outcome | Status |
| --- | --- | --- | --- |
| `transition_from_state_mismatch` | blocked | blocked | PASS |
| `transition_status_not_pass` | review_required | review_required | PASS |
| `missing_evidence_event_uri` | blocked | blocked | PASS |
| `protected_action_flag_true` | blocked | blocked | PASS |
| `terminal_state_mismatch` | review_required | review_required | PASS |
| `dependency_or_runtime_action_requested` | blocked | blocked | PASS |
| `node_sequence_gap_or_duplicate` | blocked | blocked | PASS |

## Generated artifacts

- avf/runtime/generated/agent_graph_failure_replay_harness_result.json
- avf/runtime/generated/agent_graph_failure_replay_harness_gate.json
- avf/runtime/generated/agent_graph_failure_replay_harness_next_action.yml
- avf/runtime/generated/agent_graph_failure_replay_harness_v0_1.validation_result.json

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

next_safe_goal_id=avf_agent_graph_guarded_transition_policy_v0_1
