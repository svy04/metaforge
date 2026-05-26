# Temporal Adapter Contract Skeleton

contract_status: skeleton_only
candidate_id: temporal-durable-workflow-backend
source_target_id: src-temporal-official-docs
primary_source_uri: https://docs.temporal.io/
plane: durable_workflow_plane
recommendation: defer_until_runtime_state_machine
dependency_adoption_allowed=false
runtime_integration_allowed=false
provider_calls_performed=false
external_service_calls_performed=false
protected_action_executed=false
release_ready=false
production_ready=false

## Purpose

This skeleton captures the AVF contract boundary for Temporal based on the runtime adapter decision matrix. It is not an implementation, dependency adoption, runtime integration, provider call, deployment, publication, or readiness claim.

Primary-source planning claim:
AVF durable workflow phases should evaluate crash-resumable workflow execution.

Fit for AVF:
Use later for crash-resumable, long-running venture runs after the local kernel has stable run states and idempotency rules.

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
- Do not introduce worker services or deployment assumptions in the foundation branch.
- Require explicit rollback and resume semantics before adoption.

## Evidence Hooks

- Source title: Temporal Docs
- Source kind: official_docs
- Source reference lines: turn0view1 lines 37-40, 87
- Evidence summary: The Temporal docs describe Temporal as an open-source platform for reliable applications and emphasize crash-proof execution that resumes where work left off after crashes, network failures, or infrastructure outages.

## Non-goals

- Do not install or import Temporal.
- Do not start workers, servers, collectors, gateways, model serving, web agents, or external tools.
- Do not perform provider calls, live model calls, external service calls, scraping, posting automation, deploy, publish, or readiness claims.
- Do not convert this skeleton into a production interface without a separate owner-approved implementation gate.

## Next Review Gate

next_safe_goal_id=avf_runtime_adapter_contract_review_v0_1
