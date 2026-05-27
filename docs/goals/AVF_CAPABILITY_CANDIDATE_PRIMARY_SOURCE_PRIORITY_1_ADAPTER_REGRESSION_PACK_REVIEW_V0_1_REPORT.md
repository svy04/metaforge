# AVF Capability Candidate Primary-Source Priority 1 Adapter Regression Pack Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1=true

## Review summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- review_decision=CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_REGRESSION_PACK_REVIEWED
- review_status=adapter_regression_pack_reviewed_ready_for_behavior_expansion_plan
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

- adapter_module_count=4
- regression_test_count=6
- regression_test_pass_count=6
- regression_test_fail_count=0
- reviewed_regression_test_count=6
- invalid_fixture_regression_count=4
- boundary_regression_count=1
- evidence_mapping_regression_count=1
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- runtime_integration_allowed_count=0
- regression_blocker_count=0
- review_blocker_count=0
- ready_for_adapter_regression_pack_review_count=1
- ready_for_adapter_behavior_expansion_plan_count=1

## Reviewed regression tests

- rejects-eval-case-missing-claim-boundary: source_status=PASS, review_status=reviewed_regression_test_preserves_repo_local_boundary, regression_type=invalid_fixture
- rejects-redteam-case-bad-evidence-basis-type: source_status=PASS, review_status=reviewed_regression_test_preserves_repo_local_boundary, regression_type=invalid_fixture
- rejects-rag-metric-unexpected-runtime-hint: source_status=PASS, review_status=reviewed_regression_test_preserves_repo_local_boundary, regression_type=invalid_fixture
- rejects-governance-gate-bad-risk_tier: source_status=PASS, review_status=reviewed_regression_test_preserves_repo_local_boundary, regression_type=invalid_fixture
- boundary-flags-remain-false-after-valid-normalization: source_status=PASS, review_status=reviewed_regression_test_preserves_repo_local_boundary, regression_type=boundary
- evidence-mapping-has-no-action-drift: source_status=PASS, review_status=reviewed_regression_test_preserves_repo_local_boundary, regression_type=evidence_mapping

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1
