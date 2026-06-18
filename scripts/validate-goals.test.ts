import { describe, expect, test } from 'bun:test'

import { validateGoalDocument } from './validate-goals'

const validGoal = `# CG-001 Goal Kernel MVP

\`\`\`yaml
id: CG-001
level: CodexGoal
title: Implement Goal Kernel MVP
parent: SG-001
status: active
owner: Orchestrator
createdAt: 2026-06-18
updatedAt: 2026-06-18
objective:
  summary: Create a machine-checkable goal registry.
  whyNow: Public claims need evidence-backed goal state.
  userValue: Reduces owner execution bottleneck.
scope:
  in:
    - docs/goals/CG-001-goal-kernel-mvp.md
  out:
    - public deployment
  targetFiles:
    - docs/goals/CG-001-goal-kernel-mvp.md
  targetDomain: docs-governance
context:
  localSourcesRead:
    - AGENTS.md
  externalPrimarySources:
    - title: W3C PROV-DM
      url: https://www.w3.org/TR/prov-dm/
      reason: Models provenance with entities, activities, and agents.
  relatedDecisions:
    - D-009
researchRequirements:
  required: true
  sourceLadder:
    - official docs
    - papers
  rejectedSources:
    - blog-only summary without primary source
  openQuestions:
    - none
successCriteria:
  - id: SC-001
    statement: Goal validator passes.
    validation: bun run goals:validate
validationCommands:
  - command: bun run goals:validate
    expected: exit 0
    required: true
checkpoints:
  - id: CP-001
    name: Write validator
    doneWhen: Validator accepts CG-001.
pauseConditions:
  - Protected action required.
rollbackStrategy:
  type: file-revert
  steps:
    - Revert docs and validator files.
  validationAfterRollback:
    - bun run goals:validate
agentAssignments:
  orchestrator: Owns goal state.
  researcher: Provides primary-source ledger.
  architect: Converts evidence into design.
  implementer: Edits scoped files.
  eval: Runs validation.
  security: Reviews permission gates.
  memoryLibrarian: Proposes promotion.
evidence:
  artifacts:
    - docs/goals/CG-001-goal-kernel-mvp.md
  testResults:
    - command: bun run goals:validate
      status: not_run
      outputSummary: Pending.
  traceLinks: []
reflection:
  result: unknown
  lessons:
    - Pending validation.
  nextGoalCandidates:
    - CG-002
governedCode:
  category: governed-code
  claimLevel: internal_substrate
  claimBoundary:
    allowed:
      - A local goal object validates against required MFH/Meta fields.
    forbidden:
      - Production readiness.
  authoritySources:
    - docs/PROJECT_SPEC.md
    - docs/MFH_META_SYNTHESIS.md
  mfhGates:
    sourceReconcilerRequired: true
    closureRealityRequired: true
    dirtyStateAttributionRequired: true
    humanAdjudicationRequired: true
  metaRecords:
    decisionLedgerEntries:
      - docs/DECISION_LOG.md#D-009
    rawSources:
      - docs/GOAL_SCHEMA.md
    wikiOrMemoryUpdates: []
\`\`\`
`

describe('goal validator', () => {
  test('accepts a Goal Kernel object with MFH and Meta gate fields', () => {
    const result = validateGoalDocument('docs/goals/CG-001-goal-kernel-mvp.md', validGoal)

    expect(result.ok).toBe(true)
    expect(result.goalId).toBe('CG-001')
    expect(result.errors).toEqual([])
  })

  test('rejects missing required success criteria and governed-code gate fields', () => {
    const invalid = validGoal
      .replace('successCriteria:', 'successCriteriaMissing:')
      .replace('  mfhGates:', '  mfhGatesMissing:')

    const result = validateGoalDocument('docs/goals/CG-001-goal-kernel-mvp.md', invalid)

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('successCriteria must contain at least one item')
    expect(result.errors).toContain('governedCode.mfhGates.sourceReconcilerRequired must be boolean')
  })

  test('rejects malformed item fields, filename mismatch, and missing local sources', () => {
    const invalid = validGoal
      .replace('    - title: W3C PROV-DM', '    - title: W3C PROV-DM')
      .replace('    - AGENTS.md', '    - docs/MISSING_LOCAL_SOURCE.md')
      .replace('  - id: SC-001\n    statement: Goal validator passes.', '  - statement: Goal validator passes.')
      .replace('  - id: CP-001\n    name: Write validator', '  - id: CP-001')
      .replace('    wikiOrMemoryUpdates: []', '    wikiOrMemoryUpdates: missing')

    const result = validateGoalDocument('docs/goals/CG-999-wrong-file.md', invalid)

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('id must match filename prefix CG-999')
    expect(result.errors).toContain('context.localSourcesRead.0 must point to an existing local source')
    expect(result.errors).toContain('successCriteria.0.id must be a non-empty string')
    expect(result.errors).toContain('checkpoints.0.name must be a non-empty string')
    expect(result.errors).toContain('governedCode.metaRecords.wikiOrMemoryUpdates must be an array')
  })

  test('accepts validated goals only when required commands have passing evidence and artifacts exist', () => {
    const validated = validGoal
      .replace('status: active', 'status: validated')
      .replace('      status: not_run', '      status: pass')
      .replace('      outputSummary: Pending.', '      outputSummary: Local validation passed.')

    const result = validateGoalDocument('docs/goals/CG-001-goal-kernel-mvp.md', validated)

    expect(result.ok).toBe(true)
  })

  test('rejects validated goals with missing passing command evidence', () => {
    const validatedWithoutEvidence = validGoal.replace('status: active', 'status: validated')

    const result = validateGoalDocument('docs/goals/CG-001-goal-kernel-mvp.md', validatedWithoutEvidence)

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('validated or closed goals require passing evidence.testResults for required validation command: bun run goals:validate')
  })

  test('rejects missing evidence artifact paths', () => {
    const missingArtifact = validGoal.replace(
      'evidence:\n  artifacts:\n    - docs/goals/CG-001-goal-kernel-mvp.md',
      'evidence:\n  artifacts:\n    - docs/MISSING_GOAL_ARTIFACT.md',
    )

    const result = validateGoalDocument('docs/goals/CG-001-goal-kernel-mvp.md', missingArtifact)

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('evidence.artifacts.0 must point to an existing local source')
  })
})
