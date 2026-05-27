# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Runner Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_review_v0_1=true

## Review summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- review_decision=CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_RUNNER_REVIEWED
- review_status=adapter_contract_validation_harness_runner_validated_ready_for_hardening_plan
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
- reviewed_harness_responsibility_count=6
- planned_harness_step_count=6
- reviewed_planned_harness_step_count=6
- fixture_validation_result_count=8
- reviewed_fixture_validation_result_count=8
- fixture_validation_result_matched_expected_count=8
- passing_fixture_count=4
- failing_fixture_count=4
- blocked_action_count=10
- reviewed_blocked_action_count=10
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- runtime_integration_allowed_count=0
- review_blocker_count=0
- ready_for_adapter_contract_validation_harness_hardening_plan_count=1

## Reviewed fixture validation results

- eval-case-contract-valid: review_status=reviewed_runner_result_matches_expected_fixture_outcome, runner_result_contract_validated=true, expected_valid=True, actual_valid=True, validation_result_matched_expected=True
- eval-case-contract-invalid: review_status=reviewed_runner_result_matches_expected_fixture_outcome, runner_result_contract_validated=true, expected_valid=False, actual_valid=False, validation_result_matched_expected=True
- redteam-case-contract-valid: review_status=reviewed_runner_result_matches_expected_fixture_outcome, runner_result_contract_validated=true, expected_valid=True, actual_valid=True, validation_result_matched_expected=True
- redteam-case-contract-invalid: review_status=reviewed_runner_result_matches_expected_fixture_outcome, runner_result_contract_validated=true, expected_valid=False, actual_valid=False, validation_result_matched_expected=True
- rag-metric-contract-valid: review_status=reviewed_runner_result_matches_expected_fixture_outcome, runner_result_contract_validated=true, expected_valid=True, actual_valid=True, validation_result_matched_expected=True
- rag-metric-contract-invalid: review_status=reviewed_runner_result_matches_expected_fixture_outcome, runner_result_contract_validated=true, expected_valid=False, actual_valid=False, validation_result_matched_expected=True
- governance-gate-contract-valid: review_status=reviewed_runner_result_matches_expected_fixture_outcome, runner_result_contract_validated=true, expected_valid=True, actual_valid=True, validation_result_matched_expected=True
- governance-gate-contract-invalid: review_status=reviewed_runner_result_matches_expected_fixture_outcome, runner_result_contract_validated=true, expected_valid=False, actual_valid=False, validation_result_matched_expected=True

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1
