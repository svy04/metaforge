# AVF Capability Candidate Primary-Source Priority 1 Adapter Regression Pack v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1=true

## Regression summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- regression_decision=CREATE_REPO_LOCAL_ADAPTER_REGRESSION_PACK_FOR_FIXTURE_AND_BOUNDARY_DRIFT
- regression_status=repo_local_adapter_regression_pack_passed_not_runtime_or_dependency_ready
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
- invalid_fixture_regression_count=4
- boundary_regression_count=1
- evidence_mapping_regression_count=1
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- runtime_integration_allowed_count=0
- regression_blocker_count=0
- ready_for_adapter_regression_pack_review_count=1

## Regression tests

- rejects-eval-case-missing-claim-boundary: status=PASS, regression_type=invalid_fixture
- rejects-redteam-case-bad-evidence-basis-type: status=PASS, regression_type=invalid_fixture
- rejects-rag-metric-unexpected-runtime-hint: status=PASS, regression_type=invalid_fixture
- rejects-governance-gate-bad-risk_tier: status=PASS, regression_type=invalid_fixture
- boundary-flags-remain-false-after-valid-normalization: status=PASS, regression_type=boundary
- evidence-mapping-has-no-action-drift: status=PASS, regression_type=evidence_mapping

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1
