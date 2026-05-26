# AVF Primary-Source Evidence Owner Authorization Completion Guide v0.1

goal_id: avf_capability_primary_source_evidence_owner_authorization_completion_guide_v0_1
previous_goal_id: avf_capability_primary_source_evidence_owner_authorization_input_review_v0_1
created_at: 2026-05-27T00:00:00Z
guide_decision: GUIDE_READY_EXECUTION_STILL_BLOCKED

This guide tells the owner how to fill the authorization fields for a later, narrower review. It does not authorize any primary-source collection by itself.

## Current locked state

- owner_authorization_granted: false
- collection_execution_allowed: false
- source_records_reviewed: 35
- source_records_executable: 0

## Required authorization fields

- `owner_authorization_statement`: required before any collection path can be reviewed.
- `authorized_by`: required before any collection path can be reviewed.
- `authorized_at`: required before any collection path can be reviewed.
- `authorization_expires_at`: required before any collection path can be reviewed.
- `authorized_collection_modes`: required before any collection path can be reviewed.
- `authorized_source_families`: required before any collection path can be reviewed.
- `authorized_candidate_ids`: required before any collection path can be reviewed.
- `authorized_source_slot_ids`: required before any collection path can be reviewed.
- `max_records_to_collect`: required before any collection path can be reviewed.
- `collection_boundaries`: required before any collection path can be reviewed.
- `revocation_note`: required before any collection path can be reviewed.

## Collection mode choices

- `manual_owner_collection`: default false; requires explicit owner scope and later review.
- `pro_manual_collection`: default false; requires explicit owner scope and later review.
- `codex_assisted_link_opening`: default false; requires explicit owner scope and later review.
- `automated_collection`: default false; requires explicit owner scope and later review.

## Boundary summary

- No source collection execution
- No provider calls
- No live model calls
- No external service calls
- No automated scraping
- No OSS clone
- No package install
- No dependency install
- No runtime integration
- No deploy
- No publish
- No release readiness claim
- No production readiness claim

## Minimum owner completion rule

The owner must fill every required field, choose only the intended collection modes, bound source families and source slots, set `max_records_to_collect`, and provide `collection_boundaries` plus `revocation_note`. A later filled packet and review gate are required before execution.

## Next safe goal

next_safe_goal_id: avf_capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1
