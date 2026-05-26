# AVF Agent Graph State Machine Kernel Invariant Validator v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_invariant_validator_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_state_machine_kernel_invariant_validator_v0_1.py
- python scripts\validate_avf_agent_graph_state_machine_kernel_invariant_validator_v0_1.py

## Validation summary

- validator_decision=AGENT_GRAPH_STATE_MACHINE_KERNEL_INVARIANTS_VALIDATED_FOR_REVIEW
- validator_scope=repo_local_state_machine_invariant_validator_only
- review_scope=repo_local_state_machine_invariant_review_only
- invariants_evaluated=10
- invariants_passed=10
- invariants_failed=0
- normal_path_invariants_passed=3
- guarded_outcome_invariants_passed=4
- safety_boundary_invariants_passed=3
- invariant_review_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Invariant results

| Sequence | Invariant | Category | Status | Evidence |
| --- | --- | --- | --- | --- |
| 1 | `normal_path_terminal_state_is_evidence_written` | normal_path | PASS | verified_repo_local |
| 2 | `normal_transition_sequence_is_contiguous` | normal_path | PASS | verified_repo_local |
| 3 | `normal_transition_order_is_preserved` | normal_path | PASS | verified_repo_local |
| 4 | `guarded_allowed_path_requires_pass_status` | guarded_outcome | PASS | verified_repo_local |
| 5 | `blocked_terminal_outcomes_never_reach_evidence_written` | guarded_outcome | PASS | verified_repo_local |
| 6 | `owner_review_outcomes_never_auto_execute` | guarded_outcome | PASS | verified_repo_local |
| 7 | `protected_action_flags_remain_false` | guarded_outcome | PASS | verified_repo_local |
| 8 | `dependency_and_runtime_actions_remain_blocked` | safety_boundary | PASS | verified_repo_local |
| 9 | `evidence_event_uri_required_before_terminal_success` | safety_boundary | PASS | verified_repo_local |
| 10 | `node_sequence_gap_or_duplicate_blocks_transition` | safety_boundary | PASS | verified_repo_local |

## Generated artifacts

- avf/runtime/generated/agent_graph_state_machine_kernel_invariant_validation.json
- avf/runtime/generated/agent_graph_state_machine_kernel_invariant_validation_gate.json
- avf/runtime/generated/agent_graph_state_machine_kernel_invariant_validation_next_action.yml
- avf/runtime/generated/agent_graph_state_machine_kernel_invariant_validator_v0_1.validation_result.json

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

next_safe_goal_id=avf_agent_graph_state_machine_kernel_invariant_review_v0_1
