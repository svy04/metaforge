# Goal Schema

Status: first planning pass

This schema defines durable, revisable, evidence-driven goals for the Autonomous Goal OS. It is intentionally concrete enough to become JSON/YAML later, while still readable as Markdown during planning.

Harness update: goals also inherit the MFH/Candidate M discipline from `docs/MFH_META_SYNTHESIS.md`: state is durable, closure is evidence-gated, and claims must carry a measured boundary.

## Goal Levels

| Level | ID prefix | Description | Example |
| --- | --- | --- | --- |
| North Star Goal | `NSG` | Strategic owner intent that rarely changes | `NSG-001 Autonomous Goal OS` |
| Program Goal | `PG` | Capability track under the North Star | `PG-002 Research Pipeline` |
| Sprint Goal | `SG` | Verifiable multi-day increment | `SG-004 Goal Kernel MVP` |
| Codex Goal | `CG` | One executable `/goal` command | `CG-007 Implement goal parser` |
| Atomic Task | `AT` | Small action with a single validation path | `AT-021 Add schema test` |

## Required Goal Object

```yaml
id: CG-000
level: CodexGoal
title: Short imperative title
parent: SG-000
status: proposed # proposed | active | blocked | paused | validated | closed | rolled_back
owner: Orchestrator
createdAt: 2026-05-10
updatedAt: 2026-05-10

objective:
  summary: One sentence describing the intended outcome.
  whyNow: Why this matters now.
  userValue: How it reduces the human owner's execution bottleneck.

scope:
  in:
    - Explicit included behavior or artifact.
  out:
    - Explicit non-goal.
  targetFiles:
    - docs/PROJECT_SPEC.md
  targetDomain: docs-governance

context:
  localSourcesRead:
    - README.md
    - AGENTS.md
  externalPrimarySources:
    - title: Source title
      url: https://example.com/original
      reason: Why it matters.
  relatedDecisions:
    - D-000

researchRequirements:
  required: true
  sourceLadder:
    - official docs
    - original repositories
    - papers
    - patents
    - standards
  rejectedSources:
    - blog-only summary without original source link
  openQuestions:
    - Question that must be resolved before implementation.

successCriteria:
  - id: SC-001
    statement: Observable criterion.
    validation: Command, test, review checklist, or artifact check.

validationCommands:
  - command: bun run build
    expected: exit 0
    required: true
  - command: bun test src/services/orchestra/experimentMetrics.test.ts
    expected: all tests pass
    required: false

checkpoints:
  - id: CP-001
    name: Read existing project state
    doneWhen: Source list is captured in progress log.
  - id: CP-002
    name: Write artifact
    doneWhen: File exists and internal links resolve.

pauseConditions:
  - Missing credentials or auth required for live probe.
  - Destructive operation or public deployment would be needed.
  - Required source cannot be verified from primary material.

rollbackStrategy:
  type: file-revert # file-revert | git-revert | restore-backup | no-op-docs-only
  steps:
    - Restore previous version of touched docs from backup or version control.
  validationAfterRollback:
    - Re-run docs consistency check.

agentAssignments:
  orchestrator: Owns goal state and stop/go decisions.
  researcher: Provides primary-source ledger.
  architect: Converts evidence into design.
  implementer: Edits files in scoped target set.
  eval: Runs validation and records result.
  security: Reviews permissions and approval gates.
  memoryLibrarian: Proposes Skill/Automation promotion after repeated success.

evidence:
  artifacts:
    - docs/PROGRESS_LOG.md
  testResults:
    - command: bun run build
      status: not_run
      outputSummary: To be filled after execution.
  traceLinks: []

reflection:
  result: unknown # keep | revise | pause | rollback | promote_to_skill | promote_to_automation
  lessons:
    - To be filled after validation.
  nextGoalCandidates:
    - CG-001

governedCode:
  category: governed-code
  claimLevel: internal_substrate # north_star | category | internal_substrate | external_user_validated
  claimBoundary:
    allowed:
      - What this goal can honestly claim after validation.
    forbidden:
      - External user success or production readiness unless separately validated.
  authoritySources:
    - docs/PROJECT_SPEC.md
    - docs/MFH_META_SYNTHESIS.md
  mfhGates:
    sourceReconcilerRequired: false
    closureRealityRequired: false
    dirtyStateAttributionRequired: false
    humanAdjudicationRequired: false
  metaRecords:
    decisionLedgerEntries:
      - docs/DECISION_LOG.md#D-000
    rawSources:
      - docs/research/example.md
    wikiOrMemoryUpdates: []
```

## State Machine

```text
proposed -> active -> validated -> closed
active -> blocked -> active
active -> paused -> active
active -> rolled_back -> closed
validated -> revise -> active
```

Rules:

- A goal cannot move to `validated` without fresh evidence.
- A goal cannot move to `closed` while required success criteria are unverified.
- A goal can be revised when evidence changes; the revision must update `updatedAt`, decision refs, and success criteria if affected.
- A blocked goal must name the blocker and the next safe action.

MFH/Candidate M overlay for execution state:

```text
Pending -> Active -> Verifying -> Closed
                    \-> Failed -> Active
```

Use this overlay when a goal has runtime, implementation, or release implications. `Verifying` is mandatory before `Closed`; a goal moves to `Failed` when validation, source reconciliation, dirty-state attribution, or claim-boundary review fails.

## Success Criteria Contract

Every success criterion must be one of:

- Command evidence: a command and expected result.
- Artifact evidence: an expected file, section, or schema.
- Runtime evidence: a live probe, log entry, or trace.
- Human gate: explicit owner approval for taste, strategy, destructive action, credential change, or deployment.
- Decision-log evidence: an accepted assumption when direct validation is not yet possible.
- Claim-boundary evidence: an explicit statement of what the goal does not prove.

## Validation Command Policy

- Prefer focused commands for narrow changes.
- Run broader commands when shared runtime, orchestration, provider routing, permissions, or eval logic is touched.
- For docs-only changes, run a docs consistency check and at least one repo sanity command when available.
- Do not claim success from file presence alone.

## Pause Conditions

Pause and ask the owner before:

- Destructive filesystem changes.
- Credential/account changes.
- Public deployment or publication.
- Major architecture pivots not implied by the current goal.
- A new provider/model activation not explicitly requested.
- Any automation that can write to production, push branches, send messages, spend money, or call external services at scale.

## Rollback Strategy Patterns

| Pattern | Use when | Validation |
| --- | --- | --- |
| `file-revert` | Docs or small config changed | Re-read changed files and rerun docs check |
| `git-revert` | Git repo with committed change | `git status`, focused tests |
| `restore-backup` | User/global config changed after explicit approval | Compare before/after files, run loader probe |
| `no-op-docs-only` | New docs are additive and no runtime changed | Delete added docs if owner rejects |

## Goal Review Checklist

- Goal has a parent.
- Non-goals are explicit.
- Research source ladder is declared.
- Validation commands are concrete.
- Pause conditions include approval boundaries.
- Rollback is possible or the reason it is not possible is logged.
- Next goal proposal is included.
- Governed-code claim level is declared.
- MFH/Meta gates are marked required or explicitly out of scope.
