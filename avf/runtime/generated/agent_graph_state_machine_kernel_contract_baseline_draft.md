# Agent Graph State Machine Kernel Contract Baseline Draft

Contract status: baseline_draft_not_frozen
Runtime contract frozen: false
Contract freeze executed: false

## Scope

- draft_scope=repo_local_state_machine_contract_baseline_draft_only
- baseline_review_scope=repo_local_state_machine_contract_baseline_review_only
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Draft baseline entries

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

## Next safe goal

next_safe_goal_id=avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1
