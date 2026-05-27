# AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1=true

## Plan summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- plan_decision=CREATE_REPO_LOCAL_ADAPTER_BEHAVIOR_EXPANSION_PLAN_FROM_REVIEWED_REGRESSION_PACK
- plan_status=planned_for_repo_local_adapter_behavior_expansion_review_not_runtime_or_dependency_ready
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
- reviewed_regression_test_count=6
- behavior_requirement_count=6
- planned_behavior_task_count=6
- invalid_fixture_behavior_requirement_count=4
- boundary_behavior_requirement_count=1
- evidence_mapping_behavior_requirement_count=1
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- runtime_integration_allowed_count=0
- plan_blocker_count=0
- ready_for_adapter_behavior_expansion_plan_review_count=1

## Behavior requirements

- enforce-eval-claim-boundary-required: source_regression_test_id=rejects-eval-case-missing-claim-boundary, regression_type=invalid_fixture
- enforce-redteam-evidence-basis-list: source_regression_test_id=rejects-redteam-case-bad-evidence-basis-type, regression_type=invalid_fixture
- reject-rag-runtime-hints: source_regression_test_id=rejects-rag-metric-unexpected-runtime-hint, regression_type=invalid_fixture
- enforce-governance-risk_tier-enum: source_regression_test_id=rejects-governance-gate-bad-risk_tier, regression_type=invalid_fixture
- preserve-protected-action-boundary-invariants: source_regression_test_id=boundary-flags-remain-false-after-valid-normalization, regression_type=boundary
- preserve-evidence-mapping-no-action-drift: source_regression_test_id=evidence-mapping-has-no-action-drift, regression_type=evidence_mapping

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1
