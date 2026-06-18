# Autonomous Goal OS Minimal Eval Checklist

Status: active
Date: 2026-06-18

## Eval Levels

| Level | Evidence | Current Metaforge Check |
| --- | --- | --- |
| L0 | Artifact | Required docs and reports exist. |
| L1 | Static | `bun run evals:validate`, public claim checks, and product-quality reports pass. |
| L2 | Unit | Focused validator tests pass before implementation claims. |
| L3 | Integration | `bun run scripts/orchestra-experiment-runner.ts` executes the current experiment runner. |
| L4 | Trace | Goal trace and agent workflow trace gates remain required before workflow claims. |
| L5 | Longitudinal | Skill or automation promotion requires repeated successful manual runs. |

## Required Imported Evals

### EVAL-008 MFH Source Reconciliation Import

Current status: owner-side MFH/Meta source reconciliation remains `drift_carried_forward_awaiting_user_adjudication`. The public OpenClaude/Metaforge repo may import concepts, but it must not claim the companion harness is green.

### EVAL-009 Closure Reality Gate

Current status: goal and milestone closure requires validation output, evidence artifacts, claim boundary review, and where relevant source-reconciliation proof. Status labels or completed markers are not enough.

### EVAL-010 Governed-Code Claim Ledger

Current status: public claims remain tagged as North Star, category, internal substrate, or external user validated. This slice only adds internal local no-provider eval governance evidence.

## Orchestra Experiment Runner Result

- Command: `bun run scripts/orchestra-experiment-runner.ts`
- Exit code: `0`
- orchestra experiment run mode: mock_fallback
- real_20_task_status: not_run
- tasks: `1`
- UVD: `50.0%`
- FPR: `0.0%`
- SDC: `100.0%`
- agreement-with-GPT: `100.0%`
- recommendation: `keep`

Boundary: the runner did not find a source-controlled 20-task task directory and used its one-task mock fallback. This is L3 pipeline exercise evidence only, not a real 20-task value experiment, benchmark result, external validation, or automation promotion result.

## Minimal Checklist

- Required artifacts exist.
- L0-L5 are named with evidence expectations.
- EVAL-008, EVAL-009, and EVAL-010 are imported.
- The Orchestra experiment runner result records mock versus real task status.
- Automation candidates stay proposed-only.
- External-call candidates stay blocked until owner approval.
- Source reconciliation preserves owner-side drift and does not edit private harness workspaces.
- Progress and decision logs record what ran, what did not run, and the claim boundary.

## Claim Boundary

This checklist is local no-provider eval governance evidence only. It does not claim production readiness, hosted deployment, external validation, benchmark superiority, standards compliance, patent clearance, a green companion harness, or autonomous reliability.
