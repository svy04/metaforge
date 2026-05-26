# AVF Agent Graph Run-State Transitions v0.1 Report

RESULT: PASS
agent_graph_run_state_transitions_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_run_state_transitions_v0_1.py
- python scripts\validate_avf_agent_graph_run_state_transitions_v0_1.py

## Transition summary

- transition_decision=AGENT_GRAPH_RUN_STATE_TRANSITIONS_READY_FOR_REPLAY_VALIDATOR
- transition_scope=repo_local_deterministic_state_model_only
- transitions_created=5
- terminal_state=evidence_written
- replay_validator_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Transition table

| Sequence | Node | From | To |
| --- | --- | --- | --- |
| 1 | `orchestrator` | `initialized` | `orchestrated` |
| 2 | `router` | `orchestrated` | `routed` |
| 3 | `safety_reviewer` | `routed` | `safety_reviewed` |
| 4 | `codex_planner` | `safety_reviewed` | `codex_planned` |
| 5 | `evidence_writer` | `codex_planned` | `evidence_written` |

## Generated artifacts

- avf/runtime/agent_graph_run_state_transition.schema.yml
- avf/runtime/generated/agent_graph_run_state_transitions.json
- avf/runtime/generated/agent_graph_run_state_transitions_gate.json
- avf/runtime/generated/agent_graph_run_state_transitions_next_action.yml
- avf/runtime/generated/agent_graph_run_state_transitions_v0_1.validation_result.json

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

next_safe_goal_id=avf_agent_graph_replay_validator_v0_1
