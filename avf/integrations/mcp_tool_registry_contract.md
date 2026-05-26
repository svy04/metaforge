# MCP Adapter Contract Skeleton

contract_status: skeleton_only
candidate_id: mcp-tool-protocol-boundary
source_target_id: src-mcp-official-docs
primary_source_uri: https://modelcontextprotocol.io/docs/getting-started/intro
plane: tool_registry_plane
recommendation: design_contract_now
dependency_adoption_allowed=false
runtime_integration_allowed=false
provider_calls_performed=false
external_service_calls_performed=false
protected_action_executed=false
release_ready=false
production_ready=false

## Purpose

This skeleton captures the AVF contract boundary for MCP based on the runtime adapter decision matrix. It is not an implementation, dependency adoption, runtime integration, provider call, deployment, publication, or readiness claim.

Primary-source planning claim:
AVF tool integration should use an explicit tool protocol boundary before plugin execution.

Fit for AVF:
Use as the future tool/plugin boundary so AVF can connect tools through explicit capability, permission, and evidence contracts.

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
- Treat tool descriptions and tool outputs as untrusted inputs.
- Block write, publish, deploy, scraping, and account automation tools until owner approval and policy gates exist.

## Evidence Hooks

- Source title: What is the Model Context Protocol?
- Source kind: standard
- Source reference lines: turn1view2 lines 61-73, 85-90
- Evidence summary: The MCP docs define MCP as an open-source standard for connecting AI applications to external systems, including data sources, tools, and workflows. The same page positions MCP as a standardized connector boundary for AI applications.

## Non-goals

- Do not install or import MCP.
- Do not start workers, servers, collectors, gateways, model serving, web agents, or external tools.
- Do not perform provider calls, live model calls, external service calls, scraping, posting automation, deploy, publish, or readiness claims.
- Do not convert this skeleton into a production interface without a separate owner-approved implementation gate.

## Next Review Gate

next_safe_goal_id=avf_runtime_adapter_contract_review_v0_1
