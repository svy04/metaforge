# Automation Candidates

Status: proposed only
Date: 2026-06-18

This report lists proposed automation candidates only. It does not create, schedule, install, authorize, or run automations. It performs no provider calls, live model calls, external service calls, public actions, protected actions, deploys, publishes, commits, pushes, or readiness claims.

No automations were scheduled or created.

These are manual-run candidates for future promotion. A candidate can become an Automation only after repeated successful manual runs, owner approval, and the approval tier required by `docs/SECURITY_AND_GUARDRAILS.md`.

| Candidate ID | Title | Workflow class | Source evidence | Eval level | Tier | Trigger | Schedule | Permissions | Output path | External calls required | Protected action required | Status | Pause condition | Kill switch | Required approvals | Claim boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUTO-001 | Docs consistency and claim-boundary snapshot | public hygiene | `product:doc-link-integrity`, `product:public-claim-boundary:check` | L1 | A0 | Manual dry run after public-surface edits | proposed weekly | Read-only repo scan plus docs/product-quality report read | `docs/reports/docs-consistency-snapshot.md` | no | no | proposed_only | Any broken link, unauthorized claim, or private-path finding | Delete/disable schedule before next run | Owner approves schedule | Local no-provider report only; no readiness claim. |
| AUTO-002 | Eval trend summary | eval trend | `scripts/product-quality-gate.ts`, eval reports | L1/L3 | A0 | Manual dry run after eval/product-quality runs | proposed weekly | Read-only repo scan plus generated report read | `docs/reports/eval-trend-summary.md` | no | no | proposed_only | Product Quality Gate failure, new unresolved blocker, or missing evidence artifact | Delete/disable schedule before next run | Owner approves schedule | Local no-provider trend summary only. |
| AUTO-003 | Stale goal review | goal hygiene | `goals:validate`, `docs/goals` | L1 | A0 | Manual dry run after goal registry changes | proposed weekly | Read-only `docs/goals`, `docs/PROGRESS_LOG.md`, and generated goal reports | `docs/reports/stale-goal-review.md` | no | no | proposed_only | Missing goal evidence, dirty state, or closure disagreement | Delete/disable schedule before next run | Owner approves schedule | Local goal review only; no closure claim. |
| AUTO-004 | Primary-source research ledger refresh | research hygiene | `research:validate`, primary-source registry | L1 | A1 | Manual dry run after source-ledger edits | proposed weekly | Write docs/reports only after local source scan | `docs/reports/primary-source-ledger-refresh.md` | no | yes: docs/reports write | proposed_only | Any secondary/blog source used as final evidence | Disable schedule and stop writes | Owner plus security approval | Local source-ledger refresh only; no external validation. |
| AUTO-005 | Primary-source watch report | research watch | official/original public sources | L1/L3 | A4 | Manual dry run only | none | External web read of approved official/original sources | `docs/reports/primary-source-watch.md` | yes | yes: external call | blocked_external_call_owner_approval_required; blocked_until_owner_approval | Rate limit, source drift, auth prompt, or source trust ambiguity | No schedule exists; require explicit run approval | Owner approval every run until mature | Watch proposal only; no external call was made. |
| AUTO-006 | GitHub remote surface monitor | remote surface watch | GitHub public remote audit | L1/L3 | A4 | Manual dry run only | none | External GitHub read via configured public remote tooling | `docs/reports/github-remote-surface-monitor.md` | yes | yes: external call | blocked_external_call_owner_approval_required; blocked_until_owner_approval | Any auth, rate-limit, private repo, branch, issue, PR, or public claim uncertainty | No schedule exists; require explicit run approval | Owner approval every run until mature | Remote watch proposal only; no scheduled monitor exists. |
| AUTO-007 | MFH/Meta public reconciliation snapshot | source reconciliation | `docs/MFH_META_SYNTHESIS.md`, `docs/EVALS.md` | L1 | A0 | Manual dry run after MFH/Meta docs change | proposed weekly | Read-only public docs only; no private harness edit | `docs/reports/mfh-meta-public-reconciliation.md` | no | no | proposed_only | Owner-side source drift, private workspace need, or closure evidence gap | Delete/disable schedule before next run | Owner approves schedule | Public-doc reconciliation only; no green harness claim. |

## Promotion Rule

- A0 candidates still require owner schedule approval.
- A1 candidates require owner plus security approval because they can write docs/reports.
- A4 candidates require explicit owner approval every run until they have repeated safe manual evidence.
- Any candidate that needs credentials, paid APIs, notifications, deployment, release, public posting, or external side effects stays blocked.

## Claim Boundary

This report proposes future automations only. It does not create, schedule, enable, deploy, publish, or run any recurring job. It does not authorize external calls, credential access, protected actions, or public readiness claims.
