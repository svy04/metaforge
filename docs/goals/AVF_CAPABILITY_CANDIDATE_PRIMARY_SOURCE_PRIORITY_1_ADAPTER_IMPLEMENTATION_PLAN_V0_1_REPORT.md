# AVF Capability Candidate Primary-Source Priority 1 Adapter Implementation Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1=true

## Plan summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- plan_decision=CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_IMPLEMENTATION_PLAN_FROM_REVIEWED_ACCEPTANCE_GATE
- plan_status=planned_for_repo_local_adapter_scaffold_not_runtime_or_dependency_ready
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

- source_schema_artifact_count=4
- baseline_fixture_result_count=8
- mutation_runner_result_count=5
- all_fixture_result_count=13
- all_fixture_result_matched_expected_count=13
- reviewed_acceptance_criteria_count=6
- reviewed_acceptance_criteria_passed_count=6
- source_contract_count=4
- implementation_task_count=7
- planned_file_target_count=4
- validation_command_count=3
- blocked_action_count=10
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- runtime_integration_allowed_count=0
- plan_blocker_count=0
- ready_for_adapter_scaffold_count=1

## Source contracts

- eval-case-contract: schema_uri=avf/capabilities/generated/capability_candidate_primary_source_priority_1_eval_case_contract.schema.json, implementation_scope=Normalize repo-local eval case records into the future adapter boundary
- redteam-case-contract: schema_uri=avf/capabilities/generated/capability_candidate_primary_source_priority_1_redteam_case_contract.schema.json, implementation_scope=Normalize repo-local red-team case records into the future adapter boundary
- rag-metric-contract: schema_uri=avf/capabilities/generated/capability_candidate_primary_source_priority_1_rag_metric_contract.schema.json, implementation_scope=Normalize repo-local RAG metric records into the future adapter boundary
- governance-gate-contract: schema_uri=avf/capabilities/generated/capability_candidate_primary_source_priority_1_governance_gate_contract.schema.json, implementation_scope=Normalize repo-local governance gate records into the future adapter boundary

## Implementation tasks

- adapter-contract-boundary-module: goal=Define repo-local adapter contract dataclasses and protected-action constants
- eval-case-record-normalizer: goal=Plan deterministic eval case record normalization without importing Promptfoo or Ragas
- redteam-case-record-normalizer: goal=Plan deterministic red-team case record normalization without importing Promptfoo or Ragas
- rag-metric-record-normalizer: goal=Plan deterministic RAG metric record normalization without importing Promptfoo or Ragas
- governance-gate-record-normalizer: goal=Plan deterministic governance gate record normalization without importing Promptfoo or Ragas
- repo-local-validation-harness-entrypoint: goal=Plan a local harness entrypoint over generated fixtures only
- evidence-ledger-v2-mapping: goal=Plan evidence ledger v2 mapping for scaffold output and validation reports

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1
