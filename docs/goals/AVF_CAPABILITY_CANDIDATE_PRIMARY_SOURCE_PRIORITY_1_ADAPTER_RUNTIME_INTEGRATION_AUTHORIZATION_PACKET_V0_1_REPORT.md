# AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Authorization Packet v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1=true

## Authorization summary

- candidate_id=cap-eval-redteam-promptfoo-ragas
- authorization_decision=REQUEST_OWNER_AUTHORIZATION_FOR_FUTURE_RUNTIME_INTEGRATION_ONLY
- authorization_status=owner_authorization_required_not_granted
- owner_authorization_granted=false
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
- runtime_export_performed=false

## Counts

- runtime_preflight_check_count=8
- authorization_item_count=6
- authorization_item_not_granted_count=6
- protected_action_required_count=6
- owner_input_required_count=1
- sandbox_plan_required_count=1
- license_review_required_count=1
- security_review_required_count=1
- runtime_integration_allowed_count=0
- candidate_tool_import_allowed_count=0
- dependency_install_allowed_count=0
- external_fetch_allowed_count=0
- authorization_blocker_count=0
- ready_for_runtime_integration_authorization_packet_review_count=1

## Authorization items

- authorize-candidate-tool-import: authorization_status=not_granted, action_allowed=false
- authorize-dependency-install: authorization_status=not_granted, action_allowed=false
- authorize-external-source-fetch: authorization_status=not_granted, action_allowed=false
- authorize-runtime-integration: authorization_status=not_granted, action_allowed=false
- authorize-runtime-export: authorization_status=not_granted, action_allowed=false
- authorize-external-service-call: authorization_status=not_granted, action_allowed=false

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

next_safe_goal_id=avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_review_v0_1
