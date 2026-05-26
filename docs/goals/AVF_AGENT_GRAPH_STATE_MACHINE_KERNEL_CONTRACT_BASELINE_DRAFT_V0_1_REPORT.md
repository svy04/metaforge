# AVF Agent Graph State Machine Kernel Contract Baseline Draft v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_baseline_draft_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_state_machine_kernel_contract_baseline_draft_v0_1.py
- python scripts\validate_avf_agent_graph_state_machine_kernel_contract_baseline_draft_v0_1.py

## Draft summary

- draft_decision=AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_BASELINE_DRAFT_READY_FOR_REVIEW
- draft_scope=repo_local_state_machine_contract_baseline_draft_only
- baseline_review_scope=repo_local_state_machine_contract_baseline_review_only
- contract_status=baseline_draft_not_frozen
- baseline_entries_created=10
- baseline_markdown_created=true
- baseline_review_allowed=true
- contract_freeze_executed=false
- runtime_contract_frozen=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Baseline entries

| Sequence | Invariant | Category | Baseline status |
| --- | --- | --- | --- |
| 1 | `normal_path_terminal_state_is_evidence_written` | normal_path | draft_candidate |
| 2 | `normal_transition_sequence_is_contiguous` | normal_path | draft_candidate |
| 3 | `normal_transition_order_is_preserved` | normal_path | draft_candidate |
| 4 | `guarded_allowed_path_requires_pass_status` | guarded_outcome | draft_candidate |
| 5 | `blocked_terminal_outcomes_never_reach_evidence_written` | guarded_outcome | draft_candidate |
| 6 | `owner_review_outcomes_never_auto_execute` | guarded_outcome | draft_candidate |
| 7 | `protected_action_flags_remain_false` | guarded_outcome | draft_candidate |
| 8 | `dependency_and_runtime_actions_remain_blocked` | safety_boundary | draft_candidate |
| 9 | `evidence_event_uri_required_before_terminal_success` | safety_boundary | draft_candidate |
| 10 | `node_sequence_gap_or_duplicate_blocks_transition` | safety_boundary | draft_candidate |

## Generated artifacts

- avf/runtime/generated/agent_graph_state_machine_kernel_contract_baseline_draft.json
- avf/runtime/generated/agent_graph_state_machine_kernel_contract_baseline_draft.md
- avf/runtime/generated/agent_graph_state_machine_kernel_contract_baseline_draft_gate.json
- avf/runtime/generated/agent_graph_state_machine_kernel_contract_baseline_draft_next_action.yml
- avf/runtime/generated/agent_graph_state_machine_kernel_contract_baseline_draft_v0_1.validation_result.json

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

next_safe_goal_id=avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1
