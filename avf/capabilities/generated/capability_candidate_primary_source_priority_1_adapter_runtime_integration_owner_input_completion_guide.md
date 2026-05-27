# AVF Adapter Runtime Integration Owner Input Completion Guide v0.1

goal_id: avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_v0_1
previous_goal_id: avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_review_v0_1
created_at: 2026-05-27T00:00:00Z
candidate_id: cap-eval-redteam-promptfoo-ragas
guide_decision: OWNER_INPUT_COMPLETION_GUIDE_READY_RUNTIME_ACTIONS_STILL_BLOCKED
guide_status: completion_guide_instruction_only_authorization_not_granted

This guide explains how the owner would fill a later runtime authorization packet. It is instruction-only and does not grant authorization.

## Current locked state

- owner_authorization_granted: false
- runtime_integration_allowed: false
- candidate_tool_import_allowed: false
- dependency_install_allowed: false
- external_fetch_allowed: false

## Required authorization fields

- `authorization_statement`: required in a later owner-filled packet before review can accept any action.
- `authorized_by`: required in a later owner-filled packet before review can accept any action.
- `authorized_at`: required in a later owner-filled packet before review can accept any action.
- `authorization_expires_at`: required in a later owner-filled packet before review can accept any action.
- `authorized_actions`: required in a later owner-filled packet before review can accept any action.
- `scope_boundaries`: required in a later owner-filled packet before review can accept any action.
- `sandbox_plan_uri`: required in a later owner-filled packet before review can accept any action.
- `license_review_uri`: required in a later owner-filled packet before review can accept any action.
- `security_review_uri`: required in a later owner-filled packet before review can accept any action.
- `rollback_plan_uri`: required in a later owner-filled packet before review can accept any action.
- `revocation_note`: required in a later owner-filled packet before review can accept any action.

## Completion steps

- `choose_authorization_items`: complete this as written, then route to a later review gate.
- `write_owner_authorization_statement`: complete this as written, then route to a later review gate.
- `attach_sandbox_license_security_reviews`: complete this as written, then route to a later review gate.
- `set_scope_boundaries_and_expiration`: complete this as written, then route to a later review gate.
- `define_rollback_and_revocation`: complete this as written, then route to a later review gate.
- `submit_owner_filled_packet_for_review`: complete this as written, then route to a later review gate.

## Authorization items still blocked

- `authorize-candidate-tool-import`: remains decision=unfilled, authorization_status=not_granted, protected_action_required=true, action_allowed=false.
- `authorize-dependency-install`: remains decision=unfilled, authorization_status=not_granted, protected_action_required=true, action_allowed=false.
- `authorize-external-source-fetch`: remains decision=unfilled, authorization_status=not_granted, protected_action_required=true, action_allowed=false.
- `authorize-runtime-integration`: remains decision=unfilled, authorization_status=not_granted, protected_action_required=true, action_allowed=false.
- `authorize-runtime-export`: remains decision=unfilled, authorization_status=not_granted, protected_action_required=true, action_allowed=false.
- `authorize-external-service-call`: remains decision=unfilled, authorization_status=not_granted, protected_action_required=true, action_allowed=false.

## Boundary summary

- No candidate tool import
- No dependency install
- No external fetch
- No runtime integration
- No runtime export
- No external service call
- No deploy
- No publish
- No release readiness claim
- No production readiness claim

## Minimum owner completion rule

The owner-filled packet must choose exact `authorized_actions`, bind them to `scope_boundaries`, provide sandbox/license/security review URIs, include a rollback plan and revocation note, and then pass a separate review gate. Until then, every action remains blocked.

## Next safe goal

next_safe_goal_id: avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_v0_1
