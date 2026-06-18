import { describe, expect, test } from 'bun:test'

import { buildEvalFlywheelReport, evaluateEvalFlywheelDocs } from './validate-eval-flywheel'

const validDocs = new Map<string, string>([
  ['docs/evals/README.md', `# Eval Flywheel

L0 L1 L2 L3 L4 L5
EVAL-008 EVAL-009 EVAL-010
`],
  ['docs/evals/autonomous-goal-os-minimal-checklist.md', `# Autonomous Goal OS Minimal Checklist

| Level | Evidence | Current check |
| --- | --- | --- |
| L0 | Artifact | present |
| L1 | Static | present |
| L2 | Unit | present |
| L3 | Integration | present |
| L4 | Trace | present |
| L5 | Longitudinal | present |

## EVAL-008 MFH Source Reconciliation Import
## EVAL-009 Closure Reality Gate
## EVAL-010 Governed-Code Claim Ledger

orchestra experiment run mode: mock_fallback
real_20_task_status: not_run
claim boundary: local no-provider eval governance only.
`],
  ['docs/reports/automation-candidates-2026-06-18.md', `# Automation Candidates

No automations were scheduled or created.

| ID | Tier | Workflow | Trigger | Schedule | Permissions | Output path | Pause condition | Required approvals | External calls | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUTO-001 | A0 | Docs consistency report | manual dry run | proposed weekly | read-only repo | docs/reports/docs-consistency.md | validation failure | owner approves schedule | none | proposed_only |
| AUTO-002 | A4 | Primary-source watch | manual dry run | proposed weekly | external web read | docs/reports/primary-source-watch.md | rate limit or source drift | owner approval every run | blocked_until_owner_approval | proposed_only |
`],
  ['docs/reports/mfh-meta-source-reconciliation-2026-06-18.md', `# MFH Meta Source Reconciliation

owner-side status: drift_carried_forward_awaiting_user_adjudication
private harness workspace was not edited.
OpenClaude public docs local reconciliation: pass
This does not claim production readiness, hosted deployment, external validation, benchmark superiority, standards compliance, patent clearance, or autonomous reliability.
`],
])

const requiredPathKeys = {
  evalReadme: 'docs/evals/README.md',
  checklist: 'docs/evals/autonomous-goal-os-minimal-checklist.md',
  automation: 'docs/reports/automation-candidates-2026-06-18.md',
  reconciliation: 'docs/reports/mfh-meta-source-reconciliation-2026-06-18.md',
}

function checklistDoc(): string {
  return [
    '# Autonomous Goal OS Minimal Eval Checklist',
    '',
    'L0 L1 L2 L3 L4 L5',
    '',
    'EVAL-008 MFH Source Reconciliation Import',
    'EVAL-009 Closure Reality Gate',
    'EVAL-010 Governed-Code Claim Ledger',
    '',
    'orchestra experiment run mode: mock_fallback',
    'real_20_task_status: not_run',
  ].join('\n')
}

function reconciliationDoc(): string {
  return [
    '# MFH / Meta Source Reconciliation',
    '',
    'owner-side status: drift_carried_forward_awaiting_user_adjudication',
    '',
    'The private harness workspace was not edited.',
    '',
    'This report does not claim production readiness.',
  ].join('\n')
}

function automationDoc(status: string, externalCallsRequired = 'no'): string {
  return [
    '# Automation Candidates',
    '',
    'No automations were scheduled or created.',
    '',
    '| Candidate ID | Title | Workflow class | Source evidence | Eval level | Tier | Trigger | Schedule | Permissions | Output path | External calls required | Protected action required | Status | Pause condition | Kill switch | Required approvals | Claim boundary |',
    '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |',
    `| AUTO-001 | Eval trend summary | eval trend | eval reports | L1 | A0 | Manual dry run | none | read-only | docs/reports/eval-trend-summary.md | ${externalCallsRequired} | no | ${status} | stop on drift | no schedule exists | owner approval | Local no-provider proposal only. |`,
  ].join('\n')
}

function docsWithAutomation(status: string, externalCallsRequired = 'no'): Map<string, string> {
  return new Map([
    [requiredPathKeys.evalReadme, '# Eval Flywheel'],
    [requiredPathKeys.checklist, checklistDoc()],
    [requiredPathKeys.automation, automationDoc(status, externalCallsRequired)],
    [requiredPathKeys.reconciliation, reconciliationDoc()],
  ])
}

describe('eval flywheel validator', () => {
  test('accepts eval flywheel docs with levels, required evals, proposed automations, and source reconciliation boundary', () => {
    const result = evaluateEvalFlywheelDocs(validDocs)

    expect(result.ok).toBe(true)
    expect(result.errors).toEqual([])
    expect(result.evalLevelsPresent).toEqual(['L0', 'L1', 'L2', 'L3', 'L4', 'L5'])
    expect(result.requiredEvalIdsPresent).toEqual(['EVAL-008', 'EVAL-009', 'EVAL-010'])
    expect(result.automationCandidateCount).toBe(2)
  })

  test('rejects checklist docs that omit required eval levels', () => {
    const docs = new Map(validDocs)
    docs.set('docs/evals/autonomous-goal-os-minimal-checklist.md', validDocs.get('docs/evals/autonomous-goal-os-minimal-checklist.md')!.replace('| L4 | Trace | present |\n', ''))

    const result = evaluateEvalFlywheelDocs(docs)

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('eval checklist is missing level: L4')
  })

  test('rejects automation reports that schedule or create automations', () => {
    const docs = new Map(validDocs)
    docs.set('docs/reports/automation-candidates-2026-06-18.md', validDocs.get('docs/reports/automation-candidates-2026-06-18.md')!.replace('No automations were scheduled or created.', 'AUTO-001 was scheduled.'))

    const result = evaluateEvalFlywheelDocs(docs)

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('automation report must state that no automations were scheduled or created')
  })

  test('rejects external-call automation candidates that are not blocked', () => {
    const docs = new Map(validDocs)
    docs.set('docs/reports/automation-candidates-2026-06-18.md', validDocs.get('docs/reports/automation-candidates-2026-06-18.md')!.replace('blocked_until_owner_approval', 'allowed'))

    const result = evaluateEvalFlywheelDocs(docs)

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('external-call automation candidates must be blocked until owner approval')
  })

  test('builds a local no-provider report with source inputs and side-effect arrays empty', () => {
    const report = buildEvalFlywheelReport(validDocs)

    expect(report.valid).toBe(true)
    expect(report.primarySourceInputs.some((source) => source.sourceUrl === 'https://developers.openai.com/api/docs/guides/agent-evals')).toBe(true)
    expect(report.providerCallsPerformed).toEqual([])
    expect(report.liveModelCallsPerformed).toEqual([])
    expect(report.externalCallsPerformed).toEqual([])
    expect(report.protectedActionsExecuted).toEqual([])
  })

  test('marks the proposed-only check false when a candidate is not proposed-only', () => {
    const report = buildEvalFlywheelReport(docsWithAutomation('ready_for_schedule'))
    const proposedOnlyCheck = report.evalFlywheelChecks.find((item) => item.label === 'automation candidates remain proposed-only')

    expect(report.valid).toBe(false)
    expect(report.validationErrors).toContain('automation report must mark candidates as proposed_only')
    expect(proposedOnlyCheck?.ok).toBe(false)
  })

  test('requires external-call candidates to carry owner-approval blocking status', () => {
    const result = evaluateEvalFlywheelDocs(docsWithAutomation('proposed_only', 'yes'))

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('external-call automation candidates must be blocked until owner approval')
  })

  test('accepts external-call candidates only when the status is blocked until owner approval', () => {
    const result = evaluateEvalFlywheelDocs(
      docsWithAutomation('blocked_external_call_owner_approval_required; blocked_until_owner_approval', 'yes'),
    )

    expect(result.ok).toBe(true)
    expect(result.automationCandidateCount).toBe(1)
  })
})
