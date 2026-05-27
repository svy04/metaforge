# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1=true

## Plan summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- plan_decision=CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_PLAN
- plan_status=adapter_contract_validation_harness_plan_created_provider_neutral_no_install
- provider_neutral=true
- dependency_free=true
- candidate_tool_import_allowed=false
- dependency_install_allowed=false
- external_fetch_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

- source_schema_artifact_count=4
- reviewed_validation_fixture_count=8
- harness_responsibility_count=6
- planned_harness_step_count=6
- input_contract_count=2
- output_contract_count=2
- blocked_action_count=10
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- runtime_integration_allowed_count=0
- review_blocker_count=0
- ready_for_adapter_contract_validation_harness_plan_review_count=1

## Harness responsibilities

- load-provider-neutral-schema-contracts: provider_neutral=true, dependency_free=true, candidate_tool_import_allowed=false, runtime_integration_allowed=false
- load-repo-local-validation-fixtures: provider_neutral=true, dependency_free=true, candidate_tool_import_allowed=false, runtime_integration_allowed=false
- validate-required-fields: provider_neutral=true, dependency_free=true, candidate_tool_import_allowed=false, runtime_integration_allowed=false
- validate-additional-properties: provider_neutral=true, dependency_free=true, candidate_tool_import_allowed=false, runtime_integration_allowed=false
- compare-expected-vs-actual-fixture-results: provider_neutral=true, dependency_free=true, candidate_tool_import_allowed=false, runtime_integration_allowed=false
- emit-claim-bounded-validation-report: provider_neutral=true, dependency_free=true, candidate_tool_import_allowed=false, runtime_integration_allowed=false

## Blocked actions

- dependency_install
- oss_clone
- candidate_tool_import
- runtime_integration
- provider_call
- live_model_call
- external_fetch
- deploy
- publish
- readiness_claim

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1
