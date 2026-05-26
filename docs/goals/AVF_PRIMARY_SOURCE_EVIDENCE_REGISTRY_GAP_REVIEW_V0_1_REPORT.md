# AVF Primary-Source Evidence Registry Gap Review v0.1 Report

RESULT: PASS
primary_source_evidence_registry_gap_review_v0_1=true

## Commands

- python scripts\run_avf_primary_source_evidence_registry_gap_review_v0_1.py
- python scripts\validate_avf_primary_source_evidence_registry_gap_review_v0_1.py

## Gate summary

- review_decision=PRIMARY_SOURCE_EVIDENCE_REGISTRY_GAPS_REVIEWED_REPO_LOCAL
- review_status=gaps_found_closure_plan_required

## Counts

- primary_source_entry_count=153
- unique_source_url_count=84
- reports_with_primary_source_inputs_count=49
- reports_missing_primary_source_inputs_count=35
- avf_ledger_source_count=9
- manual_source_record_count=7
- content_safety_policy_sources_missing_manual_records_count=2
- gap_count=4

## Gaps

- gap-product-quality-reports-missing-primary-source-inputs
- gap-avf-ledger-to-manual-record-namespace-map
- gap-content-safety-policy-sources-missing-manual-records
- gap-adoption-evidence-gates-not-yet-linked-to-registry

## Generated artifacts

- avf/capabilities/generated/primary_source_evidence_registry_gap_review.json
- avf/capabilities/generated/primary_source_evidence_registry_gap_review_gate.json
- avf/capabilities/generated/primary_source_evidence_registry_gap_review_report.md
- avf/capabilities/generated/primary_source_evidence_registry_gap_review_next_action.yml
- avf/capabilities/generated/primary_source_evidence_registry_gap_review_v0_1.validation_result.json

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

next_safe_goal_id=avf_primary_source_evidence_registry_gap_closure_plan_v0_1
