# AVF Agent Graph Adapter Stub v0.1 Report

RESULT: PASS
agent_graph_adapter_stub_v0_1=true

## Commands

- python scripts\run_avf_agent_graph_adapter_stub_v0_1.py
- python scripts\validate_avf_agent_graph_adapter_stub_v0_1.py

## Stub summary

- stub_decision=AGENT_GRAPH_ADAPTER_STUB_READY_FOR_REVIEW
- stub_scope=deterministic_repo_local_stub_only
- selected_candidate_id=langgraph-agent-runtime-adapter
- selected_contract_uri=avf/runtime/agent_graph_adapter_contract.md
- nodes_executed=5
- stub_review_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false
- external_runtime_dependency_required=false
- langgraph_dependency_installed=false

## Node trace

- 1. orchestrator: Goal normalized into a local adapter stub run.
- 2. router: Runtime, safety, Codex, and evidence cells selected.
- 3. safety_reviewer: Protected actions blocked and local artifact scope confirmed.
- 4. codex_planner: PR-sized deterministic stub task emitted.
- 5. evidence_writer: Trace and validation artifact contract emitted.

## Generated artifacts

- avf/runtime/fixtures/agent_graph_adapter_stub_sample_packet.json
- avf/runtime/generated/agent_graph_adapter_stub_trace.json
- avf/runtime/generated/agent_graph_adapter_stub_gate.json
- avf/runtime/generated/agent_graph_adapter_stub_next_action.yml
- avf/runtime/generated/agent_graph_adapter_stub_v0_1.validation_result.json

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

next_safe_goal_id=avf_agent_graph_adapter_stub_review_v0_1
