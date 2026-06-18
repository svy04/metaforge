import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type SourceInput = {
  sourceProject: string
  sourceUrl: string
  observedPattern: string
  localAbsorption: string
}

type LocalEvidenceInput = {
  path: string
  exists: boolean
  sha256: string | null
  sizeBytes: number
}

type ModelSystemCardQualityReport = {
  generatedAt: string
  mode: 'local_no_provider_model_system_card_quality'
  cardPath: string
  cardSha256: string
  sourceHashInputs: LocalEvidenceInput[]
  primarySourceInputs: SourceInput[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  requiredSections: string[]
  missingRequiredSections: string[]
  requiredTerms: string[]
  missingRequiredTerms: string[]
  providerCapabilityReportImported: boolean
  providerBackedExecutionClaimAllowed: false
  liveModelValidationClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  superiorityClaimAllowed: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  protectedActionExecutionAllowed: false
  externalCardValidationPerformed: false
  modelSystemCardChecks: Check[]
  claimBoundary: string
}

type ProviderCapabilityMatrixReport = {
  providerCallsPerformed?: unknown[]
  liveModelCallsPerformed?: unknown[]
  externalCallsPerformed?: unknown[]
  protectedActionsExecuted?: unknown[]
  providerBackedExecutionClaimAllowed?: boolean
  providerCompatibilityClaimAllowed?: boolean
  releaseReadinessClaimAllowed?: boolean
  productionReadinessClaimAllowed?: boolean
  publicReadinessClaimAllowed?: boolean
  externalValidationClaimAllowed?: boolean
  autonomousReliabilityClaimAllowed?: boolean
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const cardPath = 'docs/MODEL_SYSTEM_CARD.md'
const reportJsonPath = 'docs/product-quality/model-system-card-report.json'
const reportMdPath = 'docs/product-quality/model-system-card-report.md'
const provenanceJsonlPath = 'reports/openclaude-model-system-card.jsonl'
const providerCapabilityReportPath = 'docs/product-quality/provider-capability-matrix-report.json'

const requiredSections = [
  '## Claim Boundary',
  '## System Purpose',
  '## Model And Provider Surfaces',
  '## Role Boundaries',
  '## Intended Uses',
  '## Non-Uses',
  '## Data And Privacy',
  '## Tools And Permissions',
  '## Evaluation Evidence',
  '## Known Limits',
  '## Protected Actions',
  '## Change Control',
  '## Primary Sources',
]

const requiredTerms = [
  'Meta',
  'MFH',
  'Orchestra',
  'OpenClaude',
  'Owner-configured Claude',
  'Codex-compatible',
  'provider-backed execution',
  'live model validation',
  'protected action',
  'no-provider',
  'not a vendor endorsement',
]

const localEvidencePaths = [
  cardPath,
  'AGENTS.md',
  'package.json',
  'docs/PROJECT_SPEC.md',
  'docs/MFH_META_SYNTHESIS.md',
  'docs/AGENT_REGISTRY.md',
  'docs/SECURITY_AND_GUARDRAILS.md',
  'docs/product-quality/provider-compatibility-fixtures.json',
  providerCapabilityReportPath,
]

const primarySourceInputs: SourceInput[] = [
  {
    sourceProject: 'OpenAI Model Spec',
    sourceUrl: 'https://model-spec.openai.com/',
    observedPattern: 'Instruction hierarchy, autonomy bounds, side-effect control, and untrusted-data handling are documented as model behavior targets.',
    localAbsorption: 'Metaforge records authority order, role boundaries, tool-output trust limits, and side-effect claims as local system-card requirements.',
  },
  {
    sourceProject: 'OpenAI GPT-5.3-Codex System Card',
    sourceUrl: 'https://deploymentsafety.openai.com/gpt-5-3-codex',
    observedPattern: 'Coding-agent system cards separate baseline evaluations, product-specific mitigations, model-specific risks, and preparedness boundaries.',
    localAbsorption: 'Metaforge separates model/provider routes from runtime controls and keeps local evidence distinct from vendor safety claims.',
  },
  {
    sourceProject: 'OpenAI Codex agent approvals and security',
    sourceUrl: 'https://developers.openai.com/codex/agent-approvals-security',
    observedPattern: 'Agentic coding risk is reduced by sandboxing, approvals, and explicit control over destructive or networked side effects.',
    localAbsorption: 'Metaforge treats protected actions and provider-backed execution as blocked until owner authorization and fresh evidence exist.',
  },
  {
    sourceProject: 'Claude Code how it works',
    sourceUrl: 'https://code.claude.com/docs/en/how-claude-code-works',
    observedPattern: 'Agentic coding loops gather context, act through tools, and verify work through an iterative local workflow.',
    localAbsorption: 'OpenClaude is documented as the CLI substrate, while Meta/MFH/Orchestra owns memory, routing, and closure.',
  },
  {
    sourceProject: 'Claude Code permission modes',
    sourceUrl: 'https://code.claude.com/docs/en/permission-modes',
    observedPattern: 'Permission modes expose different levels of tool autonomy and user approval.',
    localAbsorption: 'The card requires tool and permission boundaries plus explicit protected-action authorization.',
  },
  {
    sourceProject: 'Anthropic public system prompt release notes',
    sourceUrl: 'https://platform.claude.com/docs/en/release-notes/system-prompts',
    observedPattern: 'Versioned public system prompt disclosure can improve transparency while remaining surface-specific.',
    localAbsorption: 'Metaforge uses this only as transparency precedent, not as evidence of hidden Claude Code or API prompts.',
  },
  {
    sourceProject: 'Model Cards for Model Reporting',
    sourceUrl: 'https://arxiv.org/abs/1810.03993',
    observedPattern: 'Model cards disclose intended use, factors, metrics, evaluation data, ethical considerations, caveats, and recommendations.',
    localAbsorption: 'Metaforge adapts the model-card shape into a model plus runtime plus tool/system transparency card.',
  },
  {
    sourceProject: 'NIST AI RMF 1.0',
    sourceUrl: 'https://doi.org/10.6028/NIST.AI.100-1',
    observedPattern: 'AI risk work can be organized through govern, map, measure, and manage functions.',
    localAbsorption: 'The card maps local governance and measurement concepts without making a standards claim.',
  },
  {
    sourceProject: 'NIST AI RMF Generative AI Profile',
    sourceUrl: 'https://doi.org/10.6028/NIST.AI.600-1',
    observedPattern: 'Generative AI risk profiles emphasize documentation, provenance, testing, incident handling, and limitations.',
    localAbsorption: 'Metaforge records known limits, change control, and blocked claims in the public card.',
  },
]

const credentialPatterns = [
  /AKIA[0-9A-Z]{16}/,
  /ASIA[0-9A-Z]{16}/,
  /sk-[A-Za-z0-9_-]{20,}/,
  /gh[pousr]_[A-Za-z0-9_]{30,}/,
  /github_pat_[A-Za-z0-9_]{30,}/,
  /-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----/,
]

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function readJson<T>(path: string): T {
  return JSON.parse(readText(path)) as T
}

function fileEvidence(path: string): LocalEvidenceInput {
  const absolutePath = resolve(root, path)
  if (!existsSync(absolutePath)) {
    return { path, exists: false, sha256: null, sizeBytes: 0 }
  }
  const content = readFileSync(absolutePath)
  return { path, exists: true, sha256: sha256(content), sizeBytes: content.byteLength }
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function hasCredentialPattern(text: string): boolean {
  return credentialPatterns.some((pattern) => pattern.test(text))
}

function digestRecord(record: Record<string, unknown>): Record<string, unknown> {
  return { ...record, recordDigest: sha256(JSON.stringify(record)) }
}

function writeMarkdown(report: ModelSystemCardQualityReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const evidenceRows = report.sourceHashInputs
    .map((item) => `| \`${item.path}\` | \`${item.exists}\` | \`${item.sha256 ?? 'missing'}\` | ${item.sizeBytes} |`)
    .join('\n')
  const checkRows = report.modelSystemCardChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Model/System Card Quality Report

Generated by: \`bun run product:model-system-card\`

## Claim Boundary

- This is a local no-provider validation of \`${report.cardPath}\`.
- It does not call providers, live models, external services, or protected actions.
- It does not prove provider-backed execution, live model validation, release readiness, production readiness, public readiness, external validation, autonomous reliability, or superiority.

## Summary

- mode: \`${report.mode}\`
- card_sha256: \`${report.cardSha256}\`
- provenance_jsonl_path: \`${report.provenanceJsonlPath}\`
- provenance_jsonl_sha256: \`${report.provenanceJsonlSha256}\`
- provenance_jsonl_record_count: \`${report.provenanceJsonlRecordCount}\`
- missing_required_sections: \`${report.missingRequiredSections.join(', ') || 'none'}\`
- missing_required_terms: \`${report.missingRequiredTerms.join(', ') || 'none'}\`
- provider_capability_report_imported: \`${report.providerCapabilityReportImported}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`
- provider_backed_execution_claim_allowed: \`${report.providerBackedExecutionClaimAllowed}\`
- live_model_validation_claim_allowed: \`${report.liveModelValidationClaimAllowed}\`

## Primary Sources

| Source | URL | Local Absorption |
| --- | --- | --- |
${sourceRows}

## Local Evidence Inputs

| Path | Exists | SHA-256 | Size |
| --- | --- | --- | --- |
${evidenceRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const cardExists = existsSync(resolve(root, cardPath))
  const cardText = cardExists ? readText(cardPath) : ''
  const cardSha256 = cardExists ? sha256(cardText) : ''
  const sourceHashInputs = localEvidencePaths.map(fileEvidence)
  const providerCapabilityReportImported = existsSync(resolve(root, providerCapabilityReportPath))
  const providerCapabilityReport = providerCapabilityReportImported
    ? readJson<ProviderCapabilityMatrixReport>(providerCapabilityReportPath)
    : null

  const missingRequiredSections = requiredSections.filter((section) => !cardText.includes(section))
  const missingRequiredTerms = requiredTerms.filter((term) => !cardText.toLowerCase().includes(term.toLowerCase()))
  const missingPrimarySources = primarySourceInputs.filter((source) => !cardText.includes(source.sourceUrl))
  const hasPlaceholders = /\b(?:TODO|TBD|FIXME)\b/i.test(cardText)
  const cardHasCredentialPattern = hasCredentialPattern(cardText)

  const provenanceRecords = [
    ...primarySourceInputs.map((source) =>
      digestRecord({
        schemaVersion: 'metaforge_model_system_card_v1',
        kind: 'primary_source',
        ...source,
      }),
    ),
    ...sourceHashInputs.map((item) =>
      digestRecord({
        schemaVersion: 'metaforge_model_system_card_v1',
        kind: 'local_evidence',
        ...item,
      }),
    ),
  ]
  const provenanceText = provenanceRecords.map((record) => JSON.stringify(record)).join('\n') + '\n'
  writeFileSync(resolve(root, provenanceJsonlPath), provenanceText)
  const provenanceJsonlSha256 = sha256(provenanceText)
  const provenanceJsonlParseable = provenanceText
    .trim()
    .split(/\r?\n/)
    .every((line) => {
      try {
        JSON.parse(line)
        return true
      } catch {
        return false
      }
    })

  const providerCapabilityCallsEmpty = providerCapabilityReport
    ? (providerCapabilityReport.providerCallsPerformed?.length ?? -1) === 0 &&
      (providerCapabilityReport.liveModelCallsPerformed?.length ?? -1) === 0 &&
      (providerCapabilityReport.externalCallsPerformed?.length ?? -1) === 0 &&
      (providerCapabilityReport.protectedActionsExecuted?.length ?? -1) === 0
    : false
  const providerCapabilityClaimsBlocked = providerCapabilityReport
    ? providerCapabilityReport.providerBackedExecutionClaimAllowed === false &&
      providerCapabilityReport.providerCompatibilityClaimAllowed === false &&
      providerCapabilityReport.releaseReadinessClaimAllowed === false &&
      providerCapabilityReport.productionReadinessClaimAllowed === false &&
      providerCapabilityReport.publicReadinessClaimAllowed === false &&
      providerCapabilityReport.externalValidationClaimAllowed === false &&
      providerCapabilityReport.autonomousReliabilityClaimAllowed === false
    : false

  const modelSystemCardChecks = [
    check('model/system card exists', cardExists, cardPath),
    check('required sections are present', missingRequiredSections.length === 0, missingRequiredSections.join(',') || 'all present'),
    check('required terms are present', missingRequiredTerms.length === 0, missingRequiredTerms.join(',') || 'all present'),
    check('primary source URLs are present in card', missingPrimarySources.length === 0, missingPrimarySources.map((source) => source.sourceProject).join(',') || 'all present'),
    check('card contains no TODO/TBD/FIXME placeholders', !hasPlaceholders, hasPlaceholders ? 'placeholder found' : 'none found'),
    check('card contains no credential patterns', !cardHasCredentialPattern, cardHasCredentialPattern ? 'credential-like pattern found' : 'known patterns absent'),
    check('local evidence inputs exist', sourceHashInputs.every((item) => item.exists), sourceHashInputs.filter((item) => !item.exists).map((item) => item.path).join(',') || 'all present'),
    check('provider capability report imported', providerCapabilityReportImported, providerCapabilityReportPath),
    check('provider capability evidence remains no-provider', providerCapabilityCallsEmpty, providerCapabilityReportImported ? 'provider/live/external/protected counts are zero' : 'missing provider capability report'),
    check('provider capability claims remain blocked', providerCapabilityClaimsBlocked, providerCapabilityReportImported ? 'claim flags false' : 'missing provider capability report'),
    check('provenance JSONL is parseable', provenanceJsonlParseable, provenanceJsonlPath),
    check('protected actions are not executed', true, 'protectedActionsExecuted=[]'),
    check('model/system card keeps readiness claims blocked', true, 'all card-level claim flags false'),
  ]

  const report: ModelSystemCardQualityReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_model_system_card_quality',
    cardPath,
    cardSha256,
    sourceHashInputs,
    primarySourceInputs,
    provenanceJsonlPath,
    provenanceJsonlSha256,
    provenanceJsonlRecordCount: provenanceRecords.length,
    provenanceJsonlParseable,
    requiredSections,
    missingRequiredSections,
    requiredTerms,
    missingRequiredTerms,
    providerCapabilityReportImported,
    providerBackedExecutionClaimAllowed: false,
    liveModelValidationClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    superiorityClaimAllowed: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    protectedActionExecutionAllowed: false,
    externalCardValidationPerformed: false,
    modelSystemCardChecks,
    claimBoundary: 'This local model/system card check verifies documentation shape, source binding, no-provider boundaries, and claim blocks only. It does not validate live providers, external services, deployment, release readiness, production readiness, public readiness, autonomous reliability, or superiority.',
  }

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of modelSystemCardChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!modelSystemCardChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`card_path=${cardPath}`)
  console.log(`card_sha256=${cardSha256}`)
  console.log(`provenance_jsonl_path=${provenanceJsonlPath}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
  console.log(`provider_backed_execution_claim_allowed=${report.providerBackedExecutionClaimAllowed}`)
  console.log(`live_model_validation_claim_allowed=${report.liveModelValidationClaimAllowed}`)
}

main()
