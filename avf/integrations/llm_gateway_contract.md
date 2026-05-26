# LiteLLM Adapter Contract Skeleton

contract_status: skeleton_only
candidate_id: litellm-provider-gateway
source_target_id: src-litellm-original-repository
primary_source_uri: https://github.com/BerriAI/litellm
plane: model_tool_plane
recommendation: later_gateway_candidate
dependency_adoption_allowed=false
runtime_integration_allowed=false
provider_calls_performed=false
external_service_calls_performed=false
protected_action_executed=false
release_ready=false
production_ready=false

## Purpose

This skeleton captures the AVF contract boundary for LiteLLM based on the runtime adapter decision matrix. It is not an implementation, dependency adoption, runtime integration, provider call, deployment, publication, or readiness claim.

Primary-source planning claim:
AVF model plane should evaluate a provider-independent LLM gateway.

Fit for AVF:
Use later as the provider-independent model gateway candidate after AVF has model routing, cost, policy, and redaction contracts.

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
- Provider keys, base URLs, and model choices require explicit owner configuration.
- Gateway traces must preserve claim boundaries and avoid public-readiness claims.

## Evidence Hooks

- Source title: BerriAI/litellm repository and LiteLLM docs
- Source kind: original_repository
- Source reference lines: turn4view3 lines 449-467, 473-479; turn4view2 lines 360-363, 426-435
- Evidence summary: The LiteLLM repository describes LiteLLM as an open-source AI Gateway for 100+ LLM providers using the OpenAI format. The official docs also describe a self-hosted OpenAI-compatible proxy and gateway surface for models, agents, and MCP.

## Non-goals

- Do not install or import LiteLLM.
- Do not start workers, servers, collectors, gateways, model serving, web agents, or external tools.
- Do not perform provider calls, live model calls, external service calls, scraping, posting automation, deploy, publish, or readiness claims.
- Do not convert this skeleton into a production interface without a separate owner-approved implementation gate.

## Next Review Gate

next_safe_goal_id=avf_runtime_adapter_contract_review_v0_1
