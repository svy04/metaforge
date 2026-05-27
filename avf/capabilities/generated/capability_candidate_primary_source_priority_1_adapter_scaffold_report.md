# AVF Capability Candidate Primary-Source Priority 1 Adapter Scaffold v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1=true

## Scaffold summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- scaffold_decision=CREATE_REPO_LOCAL_ADAPTER_SCAFFOLD_FROM_IMPLEMENTATION_PLAN
- scaffold_status=repo_local_adapter_scaffold_created_not_runtime_or_dependency_ready
- provider_neutral=true
- dependency_free=true
- candidate_tool_import_allowed=false
- dependency_install_allowed=false
- external_fetch_allowed=false
- runtime_integration_allowed=false
- selection_allowed=false
- dependency_adoption_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

- source_contract_count=4
- implementation_task_count=7
- adapter_module_count=4
- normalized_record_count=4
- evidence_entry_count=4
- validation_command_count=3
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- runtime_integration_allowed_count=0
- scaffold_blocker_count=0
- ready_for_adapter_scaffold_review_count=1

## Adapter modules

- avf/capabilities/adapters/priority_1/adapter_contracts.py
- avf/capabilities/adapters/priority_1/record_normalizers.py
- avf/capabilities/adapters/priority_1/repo_local_validation_harness.py
- avf/capabilities/adapters/priority_1/evidence_mapping.py

## Normalized records

- eval-case-contract: normalized_record_type=eval_case, record_id=eval-case-contract-valid-001
- redteam-case-contract: normalized_record_type=redteam_case, record_id=redteam-case-contract-valid-001
- rag-metric-contract: normalized_record_type=rag_metric, record_id=rag-metric-contract-valid-001
- governance-gate-contract: normalized_record_type=governance_gate, record_id=governance-gate-contract-valid-001

## Evidence entries

- evidence_entry_count=4

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
- runtime_export_performed=false
- collector_started=false
- telemetry_export_performed=false
- deploy_performed=false
- publish_performed=false
- release_ready=false
- production_ready=false

## Next safe goal

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1
