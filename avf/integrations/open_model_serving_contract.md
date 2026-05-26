# vLLM Adapter Contract Skeleton

contract_status: skeleton_only
candidate_id: vllm-open-model-serving
source_target_id: src-vllm-original-repository
primary_source_uri: https://github.com/vllm-project/vllm
plane: model_serving_plane
recommendation: later_serving_candidate
dependency_adoption_allowed=false
runtime_integration_allowed=false
provider_calls_performed=false
external_service_calls_performed=false
protected_action_executed=false
release_ready=false
production_ready=false

## Purpose

This skeleton captures the AVF contract boundary for vLLM based on the runtime adapter decision matrix. It is not an implementation, dependency adoption, runtime integration, provider call, deployment, publication, or readiness claim.

Primary-source planning claim:
AVF model plane should evaluate open model serving for later approved runtime phases.

Fit for AVF:
Use later as an open-model serving candidate when local or self-hosted inference becomes a real bottleneck.

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
- Do not assume GPU capacity, model weights, or serving readiness.
- Require license, model-card, resource, and safety review before any serving work.

## Evidence Hooks

- Source title: vllm-project/vllm repository and vLLM docs
- Source kind: original_repository
- Source reference lines: turn4view4 lines 377-405, 478-480; turn4view5 lines 2433-2453
- Evidence summary: The vLLM repository describes vLLM as a fast, easy-to-use library for LLM inference and serving, with throughput and memory management features. The docs note an OpenAI-compatible API server and broad model/hardware support.

## Non-goals

- Do not install or import vLLM.
- Do not start workers, servers, collectors, gateways, model serving, web agents, or external tools.
- Do not perform provider calls, live model calls, external service calls, scraping, posting automation, deploy, publish, or readiness claims.
- Do not convert this skeleton into a production interface without a separate owner-approved implementation gate.

## Next Review Gate

next_safe_goal_id=avf_runtime_adapter_contract_review_v0_1
