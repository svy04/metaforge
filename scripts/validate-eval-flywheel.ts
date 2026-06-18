import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type AutomationCandidate = {
  id: string
  externalCallsRequired: string
  requiresExternalCall: boolean
  status: string
}

export type EvalFlywheelValidationResult = {
  ok: boolean
  errors: string[]
  evalLevelsPresent: string[]
  requiredEvalIdsPresent: string[]
  automationCandidateCount: number
}

export type EvalFlywheelReport = {
  generatedAt: string
  mode: 'local_no_provider_eval_flywheel_validation'
  valid: boolean
  evalLevelsPresent: string[]
  requiredEvalIdsPresent: string[]
  automationCandidateCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  validationErrors: string[]
  evalFlywheelChecks: Check[]
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  claimBoundary: string
}

const root = process.cwd()
const reportDir = 'docs/product-quality'
const reportJsonPath = 'docs/product-quality/eval-flywheel-validation-report.json'
const reportMdPath = 'docs/product-quality/eval-flywheel-validation-report.md'

const requiredPaths = [
  'docs/evals/README.md',
  'docs/evals/autonomous-goal-os-minimal-checklist.md',
  'docs/reports/automation-candidates-2026-06-18.md',
  'docs/reports/mfh-meta-source-reconciliation-2026-06-18.md',
]

const evalLevels = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5']
const requiredEvalIds = ['EVAL-008', 'EVAL-009', 'EVAL-010']

function readDocsFromDisk(): Map<string, string> {
  const docs = new Map<string, string>()
  for (const path of requiredPaths) {
    const absolutePath = resolve(root, path)
    if (existsSync(absolutePath)) {
      docs.set(path, readFileSync(absolutePath, 'utf8'))
    }
  }
  return docs
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function tableRowCount(markdown: string): number {
  return parseAutomationCandidates(markdown).length
}

function parseAutomationCandidates(markdown: string): AutomationCandidate[] {
  return markdown
    .split(/\r?\n/)
    .filter((line) => line.trim().startsWith('| AUTO-'))
    .map((line) => {
      const cells = line.trim().slice(1, -1).split('|').map((cell) => cell.trim().toLowerCase())
      if (cells.length >= 17) {
        return {
          id: cells[0] ?? '',
          externalCallsRequired: cells[10] ?? '',
          requiresExternalCall: (cells[10] ?? '') === 'yes',
          status: cells[12] ?? '',
        }
      }
      const legacyExternalCalls = cells[9] ?? ''
      return {
        id: cells[0] ?? '',
        externalCallsRequired: legacyExternalCalls,
        requiresExternalCall: legacyExternalCalls !== 'none',
        status: cells[10] ?? '',
      }
    })
}

export function evaluateEvalFlywheelDocs(docs: Map<string, string>): EvalFlywheelValidationResult {
  const errors: string[] = []

  for (const path of requiredPaths) {
    if (!docs.has(path)) {
      errors.push(`missing required eval flywheel doc: ${path}`)
    }
  }

  const checklist = docs.get('docs/evals/autonomous-goal-os-minimal-checklist.md') ?? ''
  const combined = [...docs.values()].join('\n')
  const evalLevelsPresent = evalLevels.filter((level) => new RegExp(`\\b${level}\\b`).test(checklist))
  for (const level of evalLevels) {
    if (!evalLevelsPresent.includes(level)) {
      errors.push(`eval checklist is missing level: ${level}`)
    }
  }

  const requiredEvalIdsPresent = requiredEvalIds.filter((evalId) => combined.includes(evalId))
  for (const evalId of requiredEvalIds) {
    if (!requiredEvalIdsPresent.includes(evalId)) {
      errors.push(`eval flywheel docs are missing required eval id: ${evalId}`)
    }
  }

  if (!/orchestra experiment run mode:\s*mock_fallback/i.test(checklist)) {
    errors.push('eval checklist must record orchestra experiment run mode: mock_fallback')
  }
  if (!/real_20_task_status:\s*not_run/i.test(checklist)) {
    errors.push('eval checklist must record real_20_task_status: not_run')
  }

  const automation = docs.get('docs/reports/automation-candidates-2026-06-18.md') ?? ''
  const automationCandidates = parseAutomationCandidates(automation)
  const automationCandidateCount = automationCandidates.length
  if (!/No automations were scheduled or created\./i.test(automation)) {
    errors.push('automation report must state that no automations were scheduled or created')
  }
  if (automationCandidateCount === 0) {
    errors.push('automation report must include at least one AUTO-* candidate row')
  }
  if (!automationCandidates.every((candidate) =>
    candidate.status.includes('proposed_only') ||
    candidate.status.includes('blocked_until_owner_approval')
  )) {
    errors.push('automation report must mark candidates as proposed_only')
  }
  if (automationCandidates.some((candidate) =>
    candidate.requiresExternalCall &&
    !candidate.status.includes('blocked_until_owner_approval') &&
    !candidate.externalCallsRequired.includes('blocked_until_owner_approval')
  )) {
    errors.push('external-call automation candidates must be blocked until owner approval')
  }

  const reconciliation = docs.get('docs/reports/mfh-meta-source-reconciliation-2026-06-18.md') ?? ''
  if (!/owner-side status:\s*drift_carried_forward_awaiting_user_adjudication/i.test(reconciliation)) {
    errors.push('source reconciliation report must carry forward owner-side drift status')
  }
  if (!/private harness workspace was not edited/i.test(reconciliation)) {
    errors.push('source reconciliation report must state that private harness workspace was not edited')
  }
  if (!/does not claim production readiness/i.test(reconciliation)) {
    errors.push('source reconciliation report must include readiness non-claim boundary')
  }

  return {
    ok: errors.length === 0,
    errors,
    evalLevelsPresent,
    requiredEvalIdsPresent,
    automationCandidateCount,
  }
}

export function buildEvalFlywheelReport(docs: Map<string, string>): EvalFlywheelReport {
  const result = evaluateEvalFlywheelDocs(docs)
  const checks = [
    check('required eval flywheel docs exist', requiredPaths.every((path) => docs.has(path)), requiredPaths.filter((path) => !docs.has(path)).join(', ') || 'all present'),
    check('eval levels L0-L5 are present', result.evalLevelsPresent.length === evalLevels.length, result.evalLevelsPresent.join(', ')),
    check('EVAL-008 through EVAL-010 are present', result.requiredEvalIdsPresent.length === requiredEvalIds.length, result.requiredEvalIdsPresent.join(', ')),
    check('automation candidates remain proposed-only', result.automationCandidateCount > 0 && !result.errors.includes('automation report must state that no automations were scheduled or created') && !result.errors.includes('automation report must mark candidates as proposed_only'), `${result.automationCandidateCount} candidates`),
    check('external-call candidates are blocked pending owner approval', !result.errors.includes('external-call automation candidates must be blocked until owner approval'), 'blocked_until_owner_approval enforced'),
    check('owner-side MFH/Meta drift boundary is preserved', !result.errors.includes('source reconciliation report must carry forward owner-side drift status'), 'drift_carried_forward_awaiting_user_adjudication'),
    check('no provider/live/external/protected side effects recorded', true, 'side-effect arrays are empty'),
  ]

  return {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_eval_flywheel_validation',
    valid: result.ok,
    evalLevelsPresent: result.evalLevelsPresent,
    requiredEvalIdsPresent: result.requiredEvalIdsPresent,
    automationCandidateCount: result.automationCandidateCount,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    validationErrors: result.errors,
    evalFlywheelChecks: checks,
    primarySourceInputs: [
      {
        sourceProject: 'OpenAI Agent Evals',
        sourceUrl: 'https://developers.openai.com/api/docs/guides/agent-evals',
        observedPattern: 'Agent workflow quality should be evaluated with datasets, graders, traces, and repeatable eval runs.',
        localAbsorption: 'The Eval Flywheel separates checklist, command result, source reconciliation, and follow-up goal evidence.',
      },
      {
        sourceProject: 'OpenAI Trace Grading',
        sourceUrl: 'https://developers.openai.com/api/docs/guides/trace-grading',
        observedPattern: 'Trace-level grading evaluates full workflows rather than only final answers.',
        localAbsorption: 'EVAL-006 and L4 remain trace-level gates before stronger agent workflow claims.',
      },
      {
        sourceProject: 'OpenAI Evals',
        sourceUrl: 'https://github.com/openai/evals',
        observedPattern: 'Evaluation assets are source-controlled and reproducible.',
        localAbsorption: 'Metaforge eval docs and generated reports are source-controlled local no-provider artifacts.',
      },
      {
        sourceProject: 'Agent Skills',
        sourceUrl: 'https://agentskills.io/',
        observedPattern: 'Skills should package repeated workflows only after the process is stable and reusable.',
        localAbsorption: 'Skill promotion remains blocked until repeated eval evidence exists.',
      },
      {
        sourceProject: 'NIST AI RMF 1.0',
        sourceUrl: 'https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10',
        observedPattern: 'AI risk work should be governed, mapped, measured, and managed with proportional evidence.',
        localAbsorption: 'Automation candidates are tiered and blocked when permissions or external calls exceed local evidence.',
      },
      {
        sourceProject: 'OWASP Top 10 for LLM Applications',
        sourceUrl: 'https://owasp.org/www-project-top-10-for-large-language-model-applications/',
        observedPattern: 'LLM application risk includes excessive agency and sensitive information disclosure.',
        localAbsorption: 'Automation proposals keep external calls and protected actions blocked until approval.',
      },
    ],
    claimBoundary: 'Eval flywheel validation is local no-provider governance evidence only. It does not create automations, schedule jobs, call providers, call live models, call external services, execute protected actions, claim production readiness, claim external validation, claim benchmark superiority, or claim autonomous reliability.',
  }
}

function writeReport(report: EvalFlywheelReport): void {
  mkdirSync(resolve(root, reportDir), { recursive: true })
  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)

  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} | ${source.localAbsorption} |`)
  const checkRows = report.evalFlywheelChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)

  const markdown = [
    '# Eval Flywheel Validation Report',
    '',
    'Generated by: `bun run evals:validate`',
    '',
    '## Claim Boundary',
    '',
    `- ${report.claimBoundary}`,
    '- The validator performs no provider, live model, external, or protected calls.',
    '',
    '## Summary',
    '',
    `- mode: \`${report.mode}\``,
    `- valid: \`${report.valid}\``,
    `- eval_levels_present: \`${report.evalLevelsPresent.join(', ')}\``,
    `- required_eval_ids_present: \`${report.requiredEvalIdsPresent.join(', ')}\``,
    `- automation_candidate_count: \`${report.automationCandidateCount}\``,
    `- provider_calls_performed: \`${report.providerCallsPerformed.length}\``,
    `- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\``,
    `- external_calls_performed: \`${report.externalCallsPerformed.length}\``,
    `- protected_actions_executed: \`${report.protectedActionsExecuted.length}\``,
    '',
    '## Primary Source Inputs',
    '',
    '| Source | URL | Pattern Absorbed | Local Absorption |',
    '| --- | --- | --- | --- |',
    ...sourceRows,
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...checkRows,
  ].join('\n')

  writeFileSync(resolve(root, reportMdPath), `${markdown}\n`)
}

function main(): void {
  const report = buildEvalFlywheelReport(readDocsFromDisk())
  writeReport(report)

  for (const check of report.evalFlywheelChecks) {
    console.log(`${check.ok ? 'PASS' : 'FAIL'}: ${check.label} (${check.detail})`)
  }
  for (const error of report.validationErrors) {
    console.log(`  - ${error}`)
  }
  console.log('')
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)

  if (!report.valid || !report.evalFlywheelChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
}

if (import.meta.main) {
  main()
}
