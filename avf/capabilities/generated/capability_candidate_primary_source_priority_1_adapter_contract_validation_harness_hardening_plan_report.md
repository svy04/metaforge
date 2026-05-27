# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Hardening Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1=true

## Plan summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- plan_decision=CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_HARDENING_PLAN
- plan_status=adapter_contract_validation_harness_hardening_plan_created_ready_for_fixture_mutation_pack
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
- reviewed_fixture_validation_result_count=8
- existing_passing_fixture_count=4
- existing_failing_fixture_count=4
- reviewed_failure_reason_count=4
- hardening_area_count=5
- fixture_mutation_plan_count=5
- blocked_action_count=10
- reviewed_blocked_action_count=10
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- runtime_integration_allowed_count=0
- review_blocker_count=0
- ready_for_adapter_contract_validation_harness_fixture_mutation_pack_count=1

## Hardening areas

- missing-required-field-coverage: current_coverage=present_from_eval_case_contract_invalid_fixture, proposed_negative_fixture_family=required-field-removal-mutations
- type-mismatch-coverage: current_coverage=present_from_redteam_case_contract_invalid_fixture, proposed_negative_fixture_family=type-mismatch-mutations
- enum-mismatch-coverage: current_coverage=present_from_governance_gate_contract_invalid_fixture, proposed_negative_fixture_family=enum-boundary-mutations
- additional-property-coverage: current_coverage=present_from_rag_metric_contract_invalid_fixture, proposed_negative_fixture_family=additional-property-mutations
- malformed-fixture-record-coverage: current_coverage=gap_requires_new_fixture_family, proposed_negative_fixture_family=malformed-fixture-record-mutations

## Fixture mutation plan

- mutation-required-field-removal: area_id=missing-required-field-coverage, target_schema_id=all-reviewed-schema-contracts, expected_failure_reason_prefix=missing_required
- mutation-type-mismatch: area_id=type-mismatch-coverage, target_schema_id=all-reviewed-schema-contracts, expected_failure_reason_prefix=type_mismatch
- mutation-enum-boundary: area_id=enum-mismatch-coverage, target_schema_id=enum-bearing-schema-contracts, expected_failure_reason_prefix=enum_mismatch
- mutation-additional-property: area_id=additional-property-coverage, target_schema_id=all-reviewed-schema-contracts, expected_failure_reason_prefix=additional_properties
- mutation-malformed-fixture-record: area_id=malformed-fixture-record-coverage, target_schema_id=fixture-record-loader-boundary, expected_failure_reason_prefix=malformed_fixture_record

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1
