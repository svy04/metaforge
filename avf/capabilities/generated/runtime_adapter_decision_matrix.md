# Runtime Adapter Decision Matrix v0.1

runtime_adapter_decision_matrix_v0_1=true
matrix_decision=RUNTIME_ADAPTER_DECISION_MATRIX_READY_FOR_CONTRACT_SKELETONS
matrix_scope=planning_and_contract_selection_only
decision_records=7
dependency_adoption_allowed=false
runtime_integration_allowed=false

## Decision table

| Candidate | Plane | Recommendation | Next contract |
| --- | --- | --- | --- |
| LangGraph | `agent_runtime_plane` | `primary_contract_candidate` | `avf/runtime/agent_graph_adapter_contract.md` |
| Temporal | `durable_workflow_plane` | `defer_until_runtime_state_machine` | `avf/runtime/durable_workflow_adapter_contract.md` |
| OpenTelemetry | `observability_eval_plane` | `design_contract_now` | `avf/observability/telemetry_event_contract.md` |
| MCP | `tool_registry_plane` | `design_contract_now` | `avf/integrations/mcp_tool_registry_contract.md` |
| LiteLLM | `model_tool_plane` | `later_gateway_candidate` | `avf/integrations/llm_gateway_contract.md` |
| vLLM | `model_serving_plane` | `later_serving_candidate` | `avf/integrations/open_model_serving_contract.md` |
| WebArena | `safety_eval_plane` | `cautionary_benchmark_only` | `avf/evals/web_autonomy_safety_eval_contract.md` |

## Interpretation

- LangGraph is the primary contract candidate for AVF's future agent runtime adapter.
- Temporal is deferred until the AVF run state machine needs durable crash-resumable workflow execution.
- OpenTelemetry should shape observability contracts before any SDK or collector is adopted.
- MCP should shape the tool registry boundary before tool servers are executed.
- LiteLLM is a later provider-independent gateway candidate, not an active dependency.
- vLLM is a later open-model serving candidate, not an active serving layer.
- WebArena is a cautionary safety/eval reference for web autonomy limits.

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

next_safe_goal_id=avf_runtime_adapter_contract_skeletons_v0_1
