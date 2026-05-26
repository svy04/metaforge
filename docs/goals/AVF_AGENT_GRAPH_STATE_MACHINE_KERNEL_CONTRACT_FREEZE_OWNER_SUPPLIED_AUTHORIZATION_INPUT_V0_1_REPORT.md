# AVF Agent Graph State Machine Kernel Contract Freeze Owner-Supplied Authorization Input v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1.py
- python scripts\validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1.py

## Input summary

- input_decision=OWNER_SUPPLIED_AUTHORIZATION_INPUT_PACKET_CREATED_EMPTY_NOT_AUTHORIZED
- owner_input_status=not_supplied
- owner_authorization_granted=false
- owner_supplied_fields_count=0
- missing_required_fields_count=7
- contract_freeze_execution_allowed=false
- contract_freeze_executed=false
- runtime_contract_frozen=false
- codex_fabricated_owner_input=false
- codex_must_not_fill_owner_approval=true

## Missing required owner fields

- owner_identity
- authorization_scope
- accepted_invariant_ids
- freeze_execution_allowed
- rollback_or_unfreeze_plan
- validation_commands_required_after_freeze
- explicit_timestamp

## Generated artifacts

- avf/runtime/generated/agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input.yml
- avf/runtime/generated/agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_gate.json
- avf/runtime/generated/agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_next_action.yml
- avf/runtime/generated/agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1.validation_result.json

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

next_safe_goal_id=avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_v0_1
