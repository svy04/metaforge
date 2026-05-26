# LangGraph Adapter Contract Skeleton

contract_status: skeleton_only
candidate_id: langgraph-agent-runtime-adapter
source_target_id: src-langgraph-official-docs
primary_source_uri: https://docs.langchain.com/oss/python/langgraph/overview
plane: agent_runtime_plane
recommendation: primary_contract_candidate
dependency_adoption_allowed=false
runtime_integration_allowed=false
provider_calls_performed=false
external_service_calls_performed=false
protected_action_executed=false
release_ready=false
production_ready=false

## Purpose

This skeleton captures the AVF contract boundary for LangGraph based on the runtime adapter decision matrix. It is not an implementation, dependency adoption, runtime integration, provider call, deployment, publication, or readiness claim.

Primary-source planning claim:
AVF runtime adapter should evaluate a stateful graph model for long-running agent orchestration.

Fit for AVF:
Use as the first evaluated stateful agent graph adapter because AVF already has Orchestrator, Router, Safety, Codex Planner, and Evidence Writer roles.

## Contract Inputs

- `run_id`: AVF run identifier.
- `goal_id`: AVF goal identifier.
- `packet_uri`: repo-local Venture Operation Packet or planning artifact URI.
- `claim_boundary`: protected-action flags that must stay explicit.
- `owner_approval_state`: approval state required before any non-local action.
- `source_evidence_uri`: repo-local primary-source record or evidence reference.

## Contract Outputs

- `adapter_decision`: planned, skipped, blocked, or review_required.
- `artifact_uris`: repo-local artifacts created or referenced by this adapter.
- `evidence_events`: validation, gate, and decision events for evidence ledger v2.
- `blocked_actions`: protected actions that remain blocked by this skeleton.
- `next_safe_goal`: next repo-local goal if review passes.

## Safety Gates

- dependency_adoption_allowed=false
- runtime_integration_allowed=false
- provider_calls_performed=false
- external_service_calls_performed=false
- protected_action_executed=false
- release_ready=false
- production_ready=false
- owner_approval_required_before_adoption=true

Risk notes:
- Keep agent nodes deterministic until external model and tool calls are separately approved.
- Require human gates before any live action node can run.

## Evidence Hooks

- Source title: LangGraph overview
- Source kind: official_docs
- Source reference lines: turn0view0 lines 87-92, 124-130, 160-162
- Evidence summary: The official overview frames LangGraph as a low-level orchestration framework and runtime for long-running stateful agents, with durable execution, streaming, human-in-the-loop, persistence, and memory capabilities. It also says LangGraph can be used without LangChain.

## Non-goals

- Do not install or import LangGraph.
- Do not start workers, servers, collectors, gateways, model serving, web agents, or external tools.
- Do not perform provider calls, live model calls, external service calls, scraping, posting automation, deploy, publish, or readiness claims.
- Do not convert this skeleton into a production interface without a separate owner-approved implementation gate.

## Next Review Gate

next_safe_goal_id=avf_runtime_adapter_contract_review_v0_1
