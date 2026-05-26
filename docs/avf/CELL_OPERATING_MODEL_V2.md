# Cell Operating Model v2

## Purpose

Cells are production lines inside AVF. Each cell receives a bounded input packet, creates draft-first artifacts, records evidence, and hands off to the next cell.

## Cell Contract

```yaml
cell:
  cell_id:
  role:
  input_packet:
  output_artifacts:
  claim_boundary:
  validation_method:
  handoff_target:
```

## Core Cells

- Product Cell: PRD, MVP scope, architecture slice, validation plan.
- Infra Product Cell: technical empathy memo, SLO framing, integration boundary, developer workflow map.
- Brand/IP Cell: brand DNA, character bible, style memory, prompt packs, asset registry.
- Content Cell: blog, SNS, newsletter, community, short-form, long-form, media prompt drafts.
- Growth Cell: experiment plan, audience test, acquisition loop, retention signal.
- Code Cell: Codex task packet, acceptance criteria, forbidden changes, validation commands.
- Evidence Cell: evidence ledger v2 entries, success/failure criteria, decision records.
- Safety Cell: protected action boundary, platform risk, approval gate.

## Operating Rule

Cells may create local artifacts and internal evidence. They may not publish, deploy, post, call providers, install dependencies, or claim readiness without explicit future authorization.

## Boundary

- repo_local_internal_only
- runtime implementation: blocked
- provider calls: blocked
- live model calls: blocked
- external service calls: blocked
- scraping implementation: blocked
- posting automation: blocked
- deploy: blocked
- publish: blocked
- production readiness claim: blocked
- release readiness claim: blocked
- public readiness claim: blocked
- fake human impersonation: blocked
- engagement manipulation: blocked
- protected_action_executed=false
