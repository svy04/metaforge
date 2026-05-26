# AVF Agent Graph Replay Validator v0.1 Report

RESULT: PASS
agent_graph_replay_validator_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_replay_validator_v0_1.py
- python scripts\validate_avf_agent_graph_replay_validator_v0_1.py

## Replay summary

- replay_decision=AGENT_GRAPH_REPLAY_VALIDATOR_READY_FOR_FAILURE_MODE_MATRIX
- replay_scope=repo_local_deterministic_replay_only
- replay_passed=true
- transitions_replayed=5
- terminal_state=evidence_written
- failure_mode_matrix_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## State path

initialized -> orchestrated -> routed -> safety_reviewed -> codex_planned -> evidence_written

## Generated artifacts

- avf/runtime/generated/agent_graph_replay_result.json
- avf/runtime/generated/agent_graph_replay_gate.json
- avf/runtime/generated/agent_graph_replay_next_action.yml
- avf/runtime/generated/agent_graph_replay_validator_v0_1.validation_result.json

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

next_safe_goal_id=avf_agent_graph_failure_mode_matrix_v0_1
