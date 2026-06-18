# Eval Flywheel

Status: active

The Eval Flywheel turns Goal OS progress into repeatable evidence. It decides when a goal can move from artifact to static check, unit proof, integration proof, trace proof, and eventually repeated longitudinal evidence.

## Levels

| Level | Evidence | Promotion Meaning |
| --- | --- | --- |
| L0 | Artifact exists and schema/checklist passes | Draft docs and proposed reports can be discussed. |
| L1 | Static checks pass | Docs, links, claim boundaries, and generated reports are internally consistent. |
| L2 | Focused unit tests pass | A validator, parser, or local module behavior is covered. |
| L3 | Integration command or probe passes | A script/CLI workflow executes locally and records output. |
| L4 | Trace or workflow transcript proves ordered behavior | Agent workflows can be graded for sequence and guardrail adherence. |
| L5 | Repeated runs across tasks or time | A workflow may become a Skill or proposed Automation. |

## Required Imports

- EVAL-008 MFH Source Reconciliation Import keeps owner-side harness drift explicit before importing MFH/Meta state.
- EVAL-009 Closure Reality Gate blocks milestone closure from status labels alone.
- EVAL-010 Governed-Code Claim Ledger keeps public claims tagged to their evidence level.

## Current Artifacts

- `docs/evals/autonomous-goal-os-minimal-checklist.md`
- `docs/reports/mfh-meta-source-reconciliation-2026-06-18.md`
- `docs/reports/automation-candidates-2026-06-18.md`
- `docs/product-quality/eval-flywheel-validation-report.json`
- `docs/product-quality/eval-flywheel-validation-report.md`

## Validation

Run:

```powershell
bun run evals:validate
```

The validator is local no-provider evidence. It does not create automations, schedule jobs, call providers, call live models, call external services, or execute protected actions.
