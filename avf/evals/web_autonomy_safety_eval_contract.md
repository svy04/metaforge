# WebArena Adapter Contract Skeleton

contract_status: skeleton_only
candidate_id: webarena-web-autonomy-caution
source_target_id: src-webarena-paper
primary_source_uri: https://arxiv.org/abs/2307.13854
plane: safety_eval_plane
recommendation: cautionary_benchmark_only
dependency_adoption_allowed=false
runtime_integration_allowed=false
provider_calls_performed=false
external_service_calls_performed=false
protected_action_executed=false
release_ready=false
production_ready=false

## Purpose

This skeleton captures the AVF contract boundary for WebArena based on the runtime adapter decision matrix. It is not an implementation, dependency adoption, runtime integration, provider call, deployment, publication, or readiness claim.

Primary-source planning claim:
AVF web automation should remain approval-gated because autonomous web agents need evidence-backed limits.

Fit for AVF:
Use as evidence that web autonomy must remain sandboxed, approval-gated, and benchmarked rather than broad unsupervised web action.

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
- Do not implement live browsing, scraping, posting, or account automation from this source record.
- Use benchmark evidence to define stop conditions and human approval gates.

## Evidence Hooks

- Source title: WebArena: A Realistic Web Environment for Building Autonomous Agents
- Source kind: paper
- Source reference lines: turn4view1 lines 30-46; turn3view6 lines 40-46
- Evidence summary: The arXiv record describes WebArena as a realistic and reproducible web-agent environment with long-horizon benchmark tasks. It reports that the best GPT-4-based baseline agent achieved 14.41% end-to-end success versus 78.24% human performance, supporting approval-gated web automation rather than broad unsupervised action.

## Non-goals

- Do not install or import WebArena.
- Do not start workers, servers, collectors, gateways, model serving, web agents, or external tools.
- Do not perform provider calls, live model calls, external service calls, scraping, posting automation, deploy, publish, or readiness claims.
- Do not convert this skeleton into a production interface without a separate owner-approved implementation gate.

## Next Review Gate

next_safe_goal_id=avf_runtime_adapter_contract_review_v0_1
