# AVF Telemetry Event Evidence Binding v0.1 Report

RESULT: PASS
telemetry_event_evidence_binding_v0_1=true

## Commands

- python scripts\run_avf_telemetry_event_evidence_binding_v0_1.py
- python scripts\validate_avf_telemetry_event_evidence_binding_v0_1.py

## Binding summary

- binding_decision=TELEMETRY_EVENTS_BOUND_TO_EVIDENCE_LEDGER_V2_RECORDS
- binding_scope=repo_local_evidence_binding_only
- evidence_records_created=4
- evidence_ledger_v2_shape_valid=true
- trace_identity_preserved=true
- artifact_hashes_created=true
- runtime_state_link_allowed=true
- runtime_export_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Generated artifacts

- avf/observability/generated/telemetry_event_evidence_binding.json
- avf/observability/generated/telemetry_event_evidence_binding_records.jsonl
- avf/observability/generated/telemetry_event_evidence_binding_gate.json
- avf/observability/generated/telemetry_event_evidence_binding_report.md
- avf/observability/generated/telemetry_event_evidence_binding_next_action.yml
- avf/observability/generated/telemetry_event_evidence_binding_v0_1.validation_result.json

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
- deploy_performed=false
- publish_performed=false
- release_ready=false
- production_ready=false

## Next safe goal

next_safe_goal_id=avf_telemetry_event_runtime_state_link_v0_1
