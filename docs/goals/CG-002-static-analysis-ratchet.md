# CG-002 Static Analysis Ratchet

Boundary: this is a local no-provider static-analysis governance goal. It
proves that the Knip, dependency-cruiser, and jscpd report lanes are bound into
Goal OS and MFH trace validation. It does not prove cleanup completion, safe
deletion, topology cleanliness, production readiness, release readiness, public
readiness, external validation, or autonomous reliability.

```yaml
id: CG-002
level: CodexGoal
title: Bind Static Analysis Ratchets To Goal OS Evidence
parent: SG-001
status: active
owner: Orchestrator
createdAt: 2026-06-19
updatedAt: 2026-06-19

objective:
  summary: Turn public static-analysis feedback into a second machine-checkable Goal OS trace.
  whyNow: Community feedback correctly separated useful static-analysis candidates from real behavior evidence, so Metaforge needs a bounded ratchet instead of broad cleanup copy.
  userValue: The owner can point to current Knip, dependency-cruiser, and jscpd evidence without claiming the repo is cleaned up or architecturally fixed.

scope:
  in:
    - Bind the existing Knip dead-export candidate report to a Goal OS record.
    - Bind the existing dependency-cruiser topology ratchet to a Goal OS record.
    - Bind the existing jscpd duplicate-shape audit to a Goal OS record.
    - Bind the static-analysis remediation queue to a Goal OS record.
    - Add a static-analysis trace fixture so MFH evidence spans more than one goal.
    - Update public claim wording to describe current static-analysis evidence without cleanup claims.
  out:
    - Deleting dead exports.
    - Autofixing dependency topology.
    - Refactoring duplicate script helpers.
    - Claiming fallow or Lumin Repo Lens are wired into local gates.
    - Claiming CodeQL hosted runs without inspecting a current GitHub run.
    - Credential or provider changes.
    - Live model calls.
    - Public deployment.
  targetFiles:
    - docs/goals/CG-002-static-analysis-ratchet.md
    - docs/goals/traces/CG-002-static-analysis-ratchet.trace.json
    - scripts/validate-goal-traces.ts
    - scripts/validate-goal-traces.test.ts
    - scripts/product-public-claim-boundary.ts
    - scripts/product-public-claim-boundary.test.ts
    - scripts/product-static-analysis-remediation-queue.ts
    - scripts/product-static-analysis-remediation-queue.test.ts
    - docs/product-quality/dead-export-candidates-report.json
    - docs/product-quality/dead-export-candidates-report.md
    - docs/product-quality/dependency-topology-report.json
    - docs/product-quality/dependency-topology-report.md
    - docs/product-quality/script-duplication-audit-report.json
    - docs/product-quality/script-duplication-audit-report.md
    - docs/product-quality/static-analysis-remediation-queue-report.json
    - docs/product-quality/static-analysis-remediation-queue-report.md
    - reports/openclaude-static-analysis-remediation-queue.jsonl
    - docs/product-quality/public-feedback-snapshot-2026-06-19.md
    - docs/product-quality/public-feedback-triage-2026-06-19.md
    - README.md
  targetDomain: static-analysis-governance

context:
  localSourcesRead:
    - AGENTS.md
    - README.md
    - README.ko.md
    - package.json
    - knip.jsonc
    - .dependency-cruiser.mjs
    - .dependency-cruiser-known-violations.json
    - .jscpd.json
    - scripts/product-dead-export-candidates.ts
    - scripts/product-dependency-topology.ts
    - scripts/product-script-duplication-audit.ts
    - scripts/product-static-analysis-remediation-queue.ts
    - docs/product-quality/dead-export-candidates-report.md
    - docs/product-quality/dependency-topology-report.md
    - docs/product-quality/script-duplication-audit-report.md
    - docs/product-quality/static-analysis-remediation-queue-report.md
    - docs/product-quality/public-feedback-snapshot-2026-06-19.md
    - docs/product-quality/public-feedback-triage-2026-06-19.md
  externalPrimarySources:
    - title: Knip Reporters and Preprocessors
      url: https://knip.dev/features/reporters
      reason: Documents structured reporter output used by the dead-export candidate gate.
    - title: Knip source repository
      url: https://github.com/webpro-nl/knip
      reason: Original maintained implementation for unused files, dependencies, and exports in JavaScript and TypeScript projects.
    - title: dependency-cruiser source repository
      url: https://github.com/sverweij/dependency-cruiser
      reason: Original maintained implementation for dependency graph validation and visualization.
    - title: jscpd source repository
      url: https://github.com/kucherenko/jscpd
      reason: Original maintained implementation for copy-paste and duplicate-shape detection.
  relatedDecisions:
    - D-017
    - D-018

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
    - raw community comments copied into public docs
  openQuestions:
    - Whether fallow or Lumin Repo Lens should be added as separate source-controlled gates after false-positive boundaries are defined.

successCriteria:
  - id: SC-001
    statement: The CG-002 goal file validates as a structured Codex Goal.
    validation: bun run goals:validate
  - id: SC-002
    statement: The goal trace validator requires cross-goal evidence before cross-goal MFH wording.
    validation: bun test scripts/validate-goal-traces.test.ts
  - id: SC-003
    statement: Static-analysis reports and remediation queue refresh without cleanup, deletion, or public-readiness claims.
    validation: bun run product:dead-export-candidates && bun run product:dependency-topology && bun run product:script-duplication-audit && bun run product:static-analysis-remediation-queue
  - id: SC-004
    statement: Public claim evidence points to the new goal and keeps runtime/live-provider gaps blocked.
    validation: bun run product:public-claim-boundary:check

validationCommands:
  - command: bun run goals:validate
    expected: exit 0 with CG-001 and CG-002 goal coverage
    required: true
  - command: bun test scripts/validate-goal-traces.test.ts
    expected: all tests pass, including cross-goal coverage
    required: true
  - command: bun run product:dead-export-candidates
    expected: exit 0 with Knip candidate report refreshed
    required: true
  - command: bun run product:dependency-topology
    expected: exit 0 with dependency-cruiser known-violation ratchet refreshed
    required: true
  - command: bun run product:script-duplication-audit
    expected: exit 0 with jscpd duplicate-shape baseline refreshed
    required: true
  - command: bun run product:static-analysis-remediation-queue
    expected: exit 0 with Knip, dependency-cruiser, and jscpd findings converted into a bounded remediation queue
    required: true
  - command: bun run product:public-claim-boundary:check
    expected: exit 0 with no unauthorized public claims
    required: true
  - command: bun run verify:privacy
    expected: exit 0
    required: false

checkpoints:
  - id: CP-001
    name: Preserve feedback as bounded product input
    doneWhen: Public feedback docs summarize durable signals without raw thread or local-machine leakage.
  - id: CP-002
    name: Add cross-goal trace policy
    doneWhen: The trace validator fails single-goal-only packs for cross-goal MFH coverage.
  - id: CP-003
    name: Bind static-analysis evidence
    doneWhen: CG-002 references the existing Knip, dependency-cruiser, and jscpd reports.
  - id: CP-004
    name: Regenerate evidence
    doneWhen: Goal, static-analysis, claim-boundary, evidence-manifest, and privacy gates pass locally.

pauseConditions:
  - A cleanup deletion, autofix, credential change, provider activation, public deployment, or automation creation is needed.
  - External hosted CI or CodeQL status is needed to support a claim.
  - A static-analysis tool reports candidates that require human false-positive adjudication before deletion.
  - A source cannot be verified from local repo evidence or primary material.

rollbackStrategy:
  type: file-revert
  steps:
    - Remove `docs/goals/CG-002-static-analysis-ratchet.md`.
    - Remove `docs/goals/traces/CG-002-static-analysis-ratchet.trace.json`.
    - Revert cross-goal trace coverage additions.
    - Revert public claim and feedback wording updates.
  validationAfterRollback:
    - bun run goals:validate
    - bun run product:public-claim-boundary:check

agentAssignments:
  orchestrator: Owns goal state, branch scope, and public claim boundaries.
  researcher: Checks official tool docs and original repositories before wording upgrades.
  architect: Keeps static-analysis evidence separate from runtime reliability claims.
  implementer: Edits the scoped Goal OS, trace, and public-surface files.
  eval: Runs focused tests and product-quality gates.
  security: Reviews local-path, credential, provider, external-call, and overclaim surfaces.
  memoryLibrarian: Keeps durable feedback rules in memory only when explicitly requested.

evidence:
  artifacts:
    - docs/goals/CG-002-static-analysis-ratchet.md
    - docs/goals/traces/CG-002-static-analysis-ratchet.trace.json
    - docs/product-quality/dead-export-candidates-report.json
    - docs/product-quality/dead-export-candidates-report.md
    - docs/product-quality/dependency-topology-report.json
    - docs/product-quality/dependency-topology-report.md
    - docs/product-quality/script-duplication-audit-report.json
    - docs/product-quality/script-duplication-audit-report.md
    - docs/product-quality/static-analysis-remediation-queue-report.json
    - docs/product-quality/static-analysis-remediation-queue-report.md
    - reports/openclaude-static-analysis-remediation-queue.jsonl
    - docs/product-quality/goal-validation-report.json
    - docs/product-quality/goal-trace-validation-report.json
    - docs/product-quality/public-claim-boundary-report.json
  testResults:
    - command: bun run goals:validate
      status: pass
      outputSummary: CG-001 and CG-002 goal files validated, with 4 valid traces and cross-goal coverage across CG-001 and CG-002.
    - command: bun test scripts/validate-goal-traces.test.ts
      status: pass
      outputSummary: 9 tests passed, including cross-goal trace coverage.
    - command: bun run product:dead-export-candidates
      status: pass
      outputSummary: Knip dead-export candidate report refreshed without deletion, autofix, or cleanup-completion claims.
    - command: bun run product:dependency-topology
      status: pass
      outputSummary: dependency-cruiser topology report refreshed with known-violation ratchet and no topology-clean claim.
    - command: bun run product:script-duplication-audit
      status: pass
      outputSummary: jscpd duplicate-shape audit refreshed with baseline ratchet and no refactor-completion claim.
    - command: bun run product:static-analysis-remediation-queue
      status: pass
      outputSummary: Static-analysis findings converted into prioritized queue items while cleanup, topology-clean, refactor-completion, and public-readiness claims remain blocked.
    - command: bun run product:public-claim-boundary:check
      status: pass
      outputSummary: Public claim-boundary reports are current with 0 unauthorized positive claims.
  traceLinks:
    - docs/goals/traces/CG-002-static-analysis-ratchet.trace.json

reflection:
  result: keep
  lessons:
    - Static-analysis candidates are useful evidence only when separated from cleanup and runtime reliability claims.
    - Cross-goal MFH wording should require valid traces from more than one structured goal.
  nextGoalCandidates:
    - CG-003-runtime-happy-path-edge-side-effect-evals
    - CG-004-agent-instruction-simplification-ratchet

governedCode:
  category: governed-code
  claimLevel: internal_substrate
  claimBoundary:
    allowed:
      - Knip, dependency-cruiser, and jscpd are source-controlled local static-analysis ratchets in this checkout.
      - CG-002 links static-analysis evidence into Goal OS and MFH trace validation.
      - Static-analysis reports identify candidates, baselines, and known-violation ratchets.
    forbidden:
      - Cleanup completion.
      - Safe deletion.
      - Topology cleanliness.
      - Refactor completion.
      - Production readiness.
      - Release readiness.
      - Public readiness.
      - External validation.
      - Autonomous reliability.
      - Hosted CodeQL health without a current inspected run.
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
      - docs/DECISION_LOG.md#D-018
    rawSources:
      - docs/product-quality/public-feedback-snapshot-2026-06-19.md
      - docs/product-quality/public-feedback-triage-2026-06-19.md
      - docs/product-quality/dead-export-candidates-report.md
      - docs/product-quality/dependency-topology-report.md
      - docs/product-quality/script-duplication-audit-report.md
      - docs/product-quality/static-analysis-remediation-queue-report.md
    wikiOrMemoryUpdates:
      - docs/PROGRESS_LOG.md#2026-06-19-checkpoint-13-static-analysis-goal-ratchet
```
