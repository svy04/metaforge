# AVF Primary-Source Evidence Owner Manual Completion Guide v0.1

goal_id: avf_capability_primary_source_evidence_owner_manual_completion_guide_v0_1
previous_goal_id: avf_capability_primary_source_evidence_owner_completion_retry_review_v0_1
created_at: 2026-05-27T00:00:00Z
guide_decision: MANUAL_COMPLETION_GUIDE_READY_EXECUTION_STILL_BLOCKED

This guide explains how the owner can manually complete the missing authorization fields from the retry review gate. It is instruction-only and does not authorize source collection by itself.

## Current locked state

- owner_input_required: true
- owner_authorization_granted: false
- authorization_retry_completed: false
- authorization_retry_review_passed: false
- collection_execution_allowed: false
- source_records_reviewed: 35
- source_records_executable: 0

## Field-by-field completion guide

- `owner_authorization_statement`: Fill this with a plain authorization sentence. It should say what source evidence may be collected and why.
- `authorized_by`: Name the owner or account that is granting authorization.
- `authorized_at`: Use ISO-8601 UTC time. Example: 2026-05-27T00:00:00Z.
- `authorization_expires_at`: Use ISO-8601 UTC time and keep the window narrow.
- `authorized_collection_modes`: Choose only the collection modes the owner explicitly wants reviewed.
- `authorized_source_families`: Choose only the source families the owner actually wants reviewed.
- `authorized_candidate_ids`: List candidate ids from the existing capability records; do not add new candidates here.
- `authorized_source_slot_ids`: List source slot ids, not vague source names.
- `max_records_to_collect`: Set this to a small integer greater than zero only after the scope is real.
- `collection_boundaries`: Explain what Codex may not do. Include no scraping, no login, no account automation, no install, and no clone unless later approved.
- `revocation_note`: Explain how authorization can be revoked.

## Collection mode guide

- `manual_owner_collection`: Owner personally supplies source URLs or excerpts. Safest default.
- `pro_manual_collection`: Owner uses a separate PRO chat to research and paste summarized source records back into the repo. Codex still does not call providers.
- `codex_assisted_link_opening`: Future approval may allow Codex to open owner-listed URLs only. It is not active in this guide.
- `automated_collection`: Blocked by default. Requires a later explicit authorization, policy review, and separate implementation.

## Optional PRO prompt draft

```text
You are helping me manually complete an AVF owner authorization packet.

Do not claim that anything has been collected, validated, deployed, published, or made production ready.
Use only sources I paste into this chat or URLs I explicitly list.
Return a structured proposal for these fields:
owner_authorization_statement, authorized_by, authorized_at, authorization_expires_at,
authorized_collection_modes, authorized_source_families, authorized_candidate_ids,
authorized_source_slot_ids, max_records_to_collect, collection_boundaries, revocation_note.
Keep automated collection, scraping, account automation, package install, clone, deploy, and publish blocked unless I explicitly authorize them later.
```

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

## Minimum completion rule

The owner must fill all 11 authorization fields, select at least one allowed collection mode, bind the chosen source families and source slot ids, set a narrow `max_records_to_collect`, and provide explicit `collection_boundaries` plus `revocation_note`. Even then, a separate review gate must pass before any execution can be considered.

## Next safe goal

next_safe_goal_id: avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1
