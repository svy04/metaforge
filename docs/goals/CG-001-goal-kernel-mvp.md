# CG-001 Goal Kernel MVP

Boundary: this is a local no-provider docs-governance goal object. It proves
that one Goal OS record is machine-checkable against MFH/Meta fields after the
validator passes. It does not prove production readiness, release readiness,
public readiness, external validation, or autonomous reliability.

```yaml
id: CG-001
level: CodexGoal
title: Implement Goal Kernel MVP
parent: SG-001
status: active
owner: Orchestrator
createdAt: 2026-06-18
updatedAt: 2026-06-18

objective:
  summary: Create a machine-checkable goal registry for the Autonomous Goal OS.
  whyNow: Metaforge needs proof-bound goal state before stronger Meta/MFH/Orchestra marketing claims.
  userValue: The owner gets durable execution state, non-goals, validation commands, and claim boundaries without becoming the technical bottleneck.

scope:
  in:
    - Create the current structured goal registry entry.
    - Add a local validator for required Goal OS fields.
    - Bind the goal to MFH gate flags and Meta record fields.
    - Record local validation commands and claim boundaries.
  out:
    - Public deployment.
    - Credential or provider changes.
    - Live model calls.
    - External benchmark submission.
    - Automation creation.
    - Rewriting historical AVF or Influence Factory goal artifacts.
  targetFiles:
    - docs/goals/README.md
    - docs/goals/CG-001-goal-kernel-mvp.md
    - scripts/validate-goals.ts
    - scripts/validate-goals.test.ts
    - package.json
    - docs/PROGRESS_LOG.md
    - docs/DECISION_LOG.md
  targetDomain: docs-governance

context:
  localSourcesRead:
    - AGENTS.md
    - docs/NEXT_GOALS.md
    - docs/GOAL_SCHEMA.md
    - docs/PROJECT_SPEC.md
    - docs/MFH_META_SYNTHESIS.md
    - docs/ROADMAP.md
    - docs/EVALS.md
    - package.json
  externalPrimarySources:
    - title: W3C PROV-DM
      url: https://www.w3.org/TR/prov-dm/
      reason: Models provenance as entities, activities, and agents for evidence-bearing state.
    - title: NIST AI Risk Management Framework
      url: https://www.nist.gov/itl/ai-risk-management-framework
      reason: Frames trustworthy AI work as design, development, use, and evaluation controls.
    - title: OpenAI Agent Evals
      url: https://developers.openai.com/api/docs/guides/agent-evals
      reason: Supports trace, grader, dataset, and eval-run based agent quality loops.
    - title: OpenAI Trace Grading
      url: https://developers.openai.com/api/docs/guides/trace-grading
      reason: Supports trace-level assessment rather than final-output-only claims.
    - title: ReAct paper
      url: https://arxiv.org/abs/2210.03629
      reason: Supports interleaved reasoning and acting trajectories as inspectable agent behavior.
    - title: USPTO Patent Public Search
      url: https://www.uspto.gov/patents/search/patent-public-search
      reason: Keeps patent search as a primary-source lane before stronger product-method claims.
  relatedDecisions:
    - D-008
    - D-009
    - D-010
    - D-011
    - D-012

researchRequirements:
  required: true
  sourceLadder:
    - local repo evidence
    - official docs
    - original repositories
    - papers
    - patents
    - standards
  rejectedSources:
    - blog-only summaries without original source links
  openQuestions:
    - Whether future goals should use separate YAML files after the Markdown registry proves stable.

successCriteria:
  - id: SC-001
    statement: The CG-001 goal file validates as a structured Codex Goal.
    validation: bun run goals:validate
  - id: SC-002
    statement: The validator rejects missing success criteria and MFH gate fields.
    validation: bun test scripts/validate-goals.test.ts
  - id: SC-003
    statement: The repo still builds after the docs-governance script is added.
    validation: bun run build
  - id: SC-004
    statement: Claim boundaries remain explicit and no protected actions are performed.
    validation: bun run goals:validate and bun run verify:privacy

validationCommands:
  - command: bun run goals:validate
    expected: exit 0
    required: true
  - command: bun test scripts/validate-goals.test.ts
    expected: all tests pass
    required: true
  - command: bun run build
    expected: exit 0
    required: true
  - command: bun run verify:privacy
    expected: exit 0
    required: false

checkpoints:
  - id: CP-001
    name: Read existing Goal OS state
    doneWhen: Local and primary-source inputs are listed in this goal object.
  - id: CP-002
    name: Add validator
    doneWhen: The goal validator exists and rejects missing required fields.
  - id: CP-003
    name: Add first structured goal
    doneWhen: The CG-001 goal file validates.
  - id: CP-004
    name: Record outcome
    doneWhen: Progress and decision logs mention the Goal Kernel MVP.

pauseConditions:
  - A protected action, credential change, provider activation, public deployment, or automation creation is needed.
  - External benchmark or external validation is required to support a claim.
  - The validator would need to rewrite historical local goal artifacts.
  - A source cannot be verified from local repo evidence or primary material.

rollbackStrategy:
  type: file-revert
  steps:
    - Revert `docs/goals/README.md`.
    - Revert `docs/goals/CG-001-goal-kernel-mvp.md`.
    - Revert `scripts/validate-goals.ts` and `scripts/validate-goals.test.ts`.
    - Remove `goals:validate` from `package.json`.
    - Revert progress and decision log additions.
  validationAfterRollback:
    - bun run build

agentAssignments:
  orchestrator: Owns goal state, branch scope, and stop/go decisions.
  researcher: Provides primary-source anchors and rejected-source boundaries.
  architect: Converts Goal OS schema into a narrow validator contract.
  implementer: Edits the scoped docs-governance files.
  eval: Runs validation commands and records pass or failure.
  security: Reviews protected-action, credential, external-call, and claim boundaries.
  memoryLibrarian: Proposes durable memory or skill promotion only after repeated success.

evidence:
  artifacts:
    - docs/goals/README.md
    - docs/goals/CG-001-goal-kernel-mvp.md
    - scripts/validate-goals.ts
    - scripts/validate-goals.test.ts
    - docs/product-quality/goal-validation-report.json
  testResults:
    - command: bun run goals:validate
      status: pass
      outputSummary: 1 goal file passed, 0 invalid, with no provider, live model, external, or protected calls.
    - command: bun test scripts/validate-goals.test.ts
      status: pass
      outputSummary: 3 tests passed, including MFH/Meta fields, missing gate fields, malformed item fields, filename mismatch, and missing local sources.
    - command: bun run build
      status: pass
      outputSummary: Built openclaude v0.6.0 to dist/cli.mjs.
    - command: bun run verify:privacy
      status: pass
      outputSummary: No banned build-output patterns, no unauthorized positive public claims, and no origin/license provenance blockers.
  traceLinks: []

reflection:
  result: keep
  lessons:
    - The first registry slice should validate only `CG-*.md` files so historical local artifacts can remain as evidence without being rewritten.
  nextGoalCandidates:
    - CG-002-primary-source-research-ledger
    - CG-003-eval-flywheel-source-reconciliation

governedCode:
  category: governed-code
  claimLevel: internal_substrate
  claimBoundary:
    allowed:
      - A local structured Codex Goal can be validated for required Goal OS, MFH, and Meta fields.
      - Historical goal artifacts remain local evidence and are not upgraded by this slice.
    forbidden:
      - Production readiness.
      - Release readiness.
      - Public readiness.
      - External validation.
      - Autonomous reliability.
      - Hosted deployment or benchmark success.
  authoritySources:
    - docs/PROJECT_SPEC.md
    - docs/GOAL_SCHEMA.md
    - docs/MFH_META_SYNTHESIS.md
    - docs/ROADMAP.md
    - docs/EVALS.md
    - docs/SECURITY_AND_GUARDRAILS.md
  mfhGates:
    sourceReconcilerRequired: true
    closureRealityRequired: true
    dirtyStateAttributionRequired: true
    humanAdjudicationRequired: true
  metaRecords:
    decisionLedgerEntries:
      - docs/DECISION_LOG.md#D-009
      - docs/DECISION_LOG.md#D-010
      - docs/DECISION_LOG.md#D-013
    rawSources:
      - docs/NEXT_GOALS.md
      - docs/GOAL_SCHEMA.md
      - docs/MFH_META_SYNTHESIS.md
      - docs/ROADMAP.md
    wikiOrMemoryUpdates: []
```

## Current Human-Readable Summary

This goal turns the planning-package idea of a Goal Kernel into one concrete
registry entry plus a validator. It deliberately does not rewrite every older
goal artifact because that would mix public hygiene work with a broad migration.
Future goals can migrate or retire historical records in smaller, verified
slices.
