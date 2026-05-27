# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Runner Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1=true

## Review summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- review_decision=CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_RUNNER_REVIEWED
- review_status=adapter_contract_validation_harness_fixture_mutation_runner_validated_ready_for_acceptance_gate
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
- mutation_fixture_count=5
- reviewed_mutation_fixture_count=5
- mutation_runner_result_count=5
- reviewed_mutation_runner_result_count=5
- mutation_fixture_expected_invalid_count=5
- mutation_fixture_actual_invalid_count=5
- mutation_fixture_result_matched_expected_count=5
- schema_boundary_mutation_count=4
- malformed_fixture_record_count=1
- blocked_action_count=10
- reviewed_blocked_action_count=10
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- runtime_integration_allowed_count=0
- review_blocker_count=0
- ready_for_adapter_contract_validation_harness_acceptance_gate_count=1

## Reviewed mutation runner results

- mutation-required-field-removal-eval-case: review_status=reviewed_mutation_runner_result_matches_reviewed_fixture_outcome, mutation_runner_result_contract_validated=true, actual_valid=False, reviewed_result_matched=True
- mutation-type-mismatch-redteam-case: review_status=reviewed_mutation_runner_result_matches_reviewed_fixture_outcome, mutation_runner_result_contract_validated=true, actual_valid=False, reviewed_result_matched=True
- mutation-enum-boundary-governance-gate: review_status=reviewed_mutation_runner_result_matches_reviewed_fixture_outcome, mutation_runner_result_contract_validated=true, actual_valid=False, reviewed_result_matched=True
- mutation-additional-property-rag-metric: review_status=reviewed_mutation_runner_result_matches_reviewed_fixture_outcome, mutation_runner_result_contract_validated=true, actual_valid=False, reviewed_result_matched=True
- mutation-malformed-fixture-record-loader-boundary: review_status=reviewed_mutation_runner_result_matches_reviewed_fixture_outcome, mutation_runner_result_contract_validated=true, actual_valid=False, reviewed_result_matched=True

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1
