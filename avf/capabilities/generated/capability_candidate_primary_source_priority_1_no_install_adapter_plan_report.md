# AVF Capability Candidate Primary-Source Priority 1 No-Install Adapter Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1=true

## Plan summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- plan_decision=CREATE_NO_INSTALL_ADAPTER_PLAN_ONLY
- plan_status=no_install_adapter_contract_plan_created
- dependency_install_allowed=false
- oss_clone_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

- adapter_component_count=5
- contract_boundary_count=6
- blocked_action_count=8
- dependency_install_allowed_count=0
- oss_clone_allowed_count=0
- runtime_integration_allowed_count=0
- ready_for_no_install_adapter_plan_review_count=1

## Adapter components

- candidate-evidence-reader: file_contract_only_no_dependency_import
- eval-case-contract: schema_only_no_tool_execution
- redteam-case-contract: schema_only_no_provider_call
- rag-metric-contract: schema_only_no_runtime_integration
- governance-gate-contract: policy_contract_only

## Contract boundaries

- repo_local_files_only
- no_dependency_install
- no_oss_clone
- no_runtime_import
- no_provider_call
- no_readiness_claim

## Blocked actions

- install_dependency
- clone_or_fetch_oss_source
- execute_candidate_tool
- import_candidate_runtime
- call_model_provider
- export_telemetry
- deploy_or_publish
- claim_release_or_production_readiness

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1
