# AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1=true

## Implementation summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- implementation_decision=IMPLEMENT_REPO_LOCAL_ADAPTER_BEHAVIOR_EXPANSION_FROM_REVIEWED_PLAN
- implementation_status=repo_local_adapter_behavior_expansion_passed_not_runtime_or_dependency_ready
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
- behavior_requirement_count=6
- reviewed_behavior_requirement_count=6
- behavior_test_count=6
- behavior_test_pass_count=6
- behavior_test_fail_count=0
- regression_test_count=6
- scaffold_test_count=4
- invalid_fixture_behavior_requirement_count=4
- boundary_behavior_requirement_count=1
- evidence_mapping_behavior_requirement_count=1
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- runtime_integration_allowed_count=0
- behavior_blocker_count=0
- ready_for_adapter_behavior_expansion_review_count=1

## Reviewed behavior requirements

- enforce-eval-claim-boundary-required: source_regression_test_id=rejects-eval-case-missing-claim-boundary, review_status=reviewed_behavior_requirement_preserves_repo_local_boundary
- enforce-redteam-evidence-basis-list: source_regression_test_id=rejects-redteam-case-bad-evidence-basis-type, review_status=reviewed_behavior_requirement_preserves_repo_local_boundary
- reject-rag-runtime-hints: source_regression_test_id=rejects-rag-metric-unexpected-runtime-hint, review_status=reviewed_behavior_requirement_preserves_repo_local_boundary
- enforce-governance-risk_tier-enum: source_regression_test_id=rejects-governance-gate-bad-risk_tier, review_status=reviewed_behavior_requirement_preserves_repo_local_boundary
- preserve-protected-action-boundary-invariants: source_regression_test_id=boundary-flags-remain-false-after-valid-normalization, review_status=reviewed_behavior_requirement_preserves_repo_local_boundary
- preserve-evidence-mapping-no-action-drift: source_regression_test_id=evidence-mapping-has-no-action-drift, review_status=reviewed_behavior_requirement_preserves_repo_local_boundary

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1
