import { spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { check, type Check } from './quality-report-helpers'

type KnipIssueItem = {
  name: string
  namespace?: string
  line?: number
}

type KnipIssue = {
  file: string
  exports?: KnipIssueItem[]
  types?: KnipIssueItem[]
  duplicates?: KnipIssueItem[]
}

type KnipJson = {
  issues?: KnipIssue[]
}

type DeadExportCommand = {
  name: string
  command: string[]
  exitCode: number | null
  passed: boolean
  requiredSubstrings: string[]
  missingSubstrings: string[]
  stdoutPreview: string[]
  stderrPreview: string[]
}

type CommandRun = DeadExportCommand & {
  stdoutText: string
}

type CandidateFileSummary = {
  file: string
  unusedExports: number
  unusedTypes: number
  duplicateExports: number
  sampleExports: string[]
  sampleTypes: string[]
}

type DeadExportTriageAction =
  | 'needs_runtime_guard'
  | 'review_for_removal'
  | 'defer_public_api'
  | 'keep_until_entrypoint_proven'

type DeadExportTriageKind = 'export' | 'type' | 'duplicate_export'

type DeadExportTriageRecord = {
  file: string
  symbol: string
  kind: DeadExportTriageKind
  action: DeadExportTriageAction
  rationale: string
  guardrail: string
  reviewedAt: string
  reviewer: string
}

type DeadExportTriageLedger = {
  schemaVersion: 1
  claimBoundary: string
  records: DeadExportTriageRecord[]
}

type DeadExportTriageReportRecord = DeadExportTriageRecord & {
  currentCandidate: boolean
}

type RemovedCandidateRatchet = {
  file: string
  symbol: string
  kind: DeadExportTriageKind
  guardrail: string
  currentCandidate: boolean
}

type DeadExportCandidatesReport = {
  generatedAt: string
  mode: 'local_no_provider_dead_export_candidate_gate'
  scannerTarget: string
  knipVersion: string
  knipCommands: DeadExportCommand[]
  candidateFileCount: number
  candidateUnusedExportCount: number
  candidateUnusedTypeCount: number
  candidateDuplicateExportCount: number
  candidateFileBaseline: number
  candidateUnusedExportBaseline: number
  candidateUnusedTypeBaseline: number
  candidateDuplicateExportBaseline: number
  sampleCandidateFiles: CandidateFileSummary[]
  triageLedgerPath: string
  triageRecordCount: number
  triageCurrentCandidateCount: number
  triageActionCounts: Record<DeadExportTriageAction, number>
  triageRecords: DeadExportTriageReportRecord[]
  removedCandidateRatchets: RemovedCandidateRatchet[]
  primarySourceInputs: Array<{
    sourceType: 'oss_tool' | 'project_docs'
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  dependencyInstallPerformed: false
  autofixPerformed: false
  deletionPerformed: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  deletionClaimAllowed: false
  cleanupCompletionClaimAllowed: false
  publicReadinessClaimAllowed: false
  deadExportChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportJsonPath = 'docs/product-quality/dead-export-candidates-report.json'
const reportMdPath = 'docs/product-quality/dead-export-candidates-report.md'
const triageLedgerPath = 'docs/product-quality/dead-export-candidate-triage.json'
const candidateFileBaseline = 657
const candidateUnusedExportBaseline = 1461
const candidateUnusedTypeBaseline = 492
const candidateDuplicateExportBaseline = 12
const removedCandidateRatchets: Array<Omit<RemovedCandidateRatchet, 'currentCandidate'>> = [
  {
    file: 'src/utils/providerDiscovery.ts',
    symbol: 'getOpenAICompatibleModelsBaseUrl',
    kind: 'export',
    guardrail: 'Keep this helper private; callers should use the public provider-discovery APIs instead.',
  },
  {
    file: 'src/bridge/sessionRunner.ts',
    symbol: 'PermissionRequest',
    kind: 'type',
    guardrail: 'Keep this request shape internal to the session runner bridge contract.',
  },
  {
    file: 'src/utils/providerProfile.ts',
    symbol: 'buildMiniMaxProfileEnv',
    kind: 'export',
    guardrail: 'Keep this provider profile helper private until an actual module boundary imports it.',
  },
  {
    file: 'src/utils/providerProfile.ts',
    symbol: 'buildNvidiaNimProfileEnv',
    kind: 'export',
    guardrail: 'Keep NVIDIA NIM preset behavior in the provider profile and flag flows; do not re-export unused env builders without a runtime import.',
  },
  {
    file: 'src/projectOnboardingState.ts',
    symbol: 'isProjectOnboardingComplete',
    kind: 'export',
    guardrail: 'Keep onboarding completion checks exported from projectOnboardingSteps.ts, not re-exported from state.',
  },
  {
    file: 'src/commands.ts',
    symbol: 'meetsAvailabilityRequirement',
    kind: 'export',
    guardrail: 'Keep command availability covered by src/commands.policy.test.ts happy-path and unavailable-command edge-case checks.',
  },
  {
    file: 'src/commands.ts',
    symbol: 'BRIDGE_SAFE_COMMANDS',
    kind: 'export',
    guardrail: 'Keep the bridge allowlist covered by src/commands.policy.test.ts safe-prompt, unsafe-local, unsafe-local-jsx, and allowlisted-local checks.',
  },
]
const knipArgs = [
  'knip',
  '--config',
  'knip.jsonc',
  '--exports',
  '--reporter',
  'json',
  '--no-exit-code',
  '--no-progress',
]

function normalize(text: string | Buffer | null | undefined): string {
  return String(text ?? '').replace(/^\uFEFF/, '').replace(/\r\n/g, '\n')
}

function preview(text: string): string[] {
  return text
    .replace(/^\uFEFF/, '')
    .split('\n')
    .map((line) => line.trimEnd())
    .filter((line) => line.length > 0)
    .map((line) => (line.length > 260 ? `${line.slice(0, 257)}...` : line))
    .slice(0, 20)
}

function runCommand(name: string, command: string[], requiredSubstrings: string[]): CommandRun {
  const [executable, ...args] = command
  const result = spawnSync(process.execPath, ['x', executable, ...args], {
    cwd: root,
    encoding: 'utf8',
    env: {
      ...process.env,
      CLAUDE_CODE_USE_OPENAI: '0',
      CLAUDE_CODE_USE_GEMINI: '0',
      CLAUDE_CODE_USE_GITHUB: '0',
      CLAUDE_CODE_USE_MISTRAL: '0',
      OPENAI_API_KEY: '',
      CODEX_API_KEY: '',
      GEMINI_API_KEY: '',
      GOOGLE_API_KEY: '',
      MISTRAL_API_KEY: '',
      GITHUB_TOKEN: '',
      GH_TOKEN: '',
      ANTHROPIC_API_KEY: '',
      OPENCLAUDE_PRODUCT_DEAD_EXPORT_NO_PROVIDER: '1',
    },
    maxBuffer: 128 * 1024 * 1024,
    shell: false,
  })
  const stdout = normalize(result.stdout)
  const stderr = normalize(result.stderr)
  const combined = `${stdout}\n${stderr}`
  const missingSubstrings = requiredSubstrings.filter((substring) => !combined.includes(substring))

  return {
    name,
    command,
    exitCode: result.status,
    passed: result.status === 0 && missingSubstrings.length === 0,
    requiredSubstrings,
    missingSubstrings,
    stdoutPreview: preview(stdout),
    stderrPreview: preview(stderr),
    stdoutText: stdout,
  }
}

function stripCommand(command: CommandRun): DeadExportCommand {
  const { stdoutText: _stdoutText, ...reportCommand } = command
  return reportCommand
}

function parseKnipJson(command: CommandRun): KnipJson {
  return JSON.parse(command.stdoutText) as KnipJson
}

function itemName(item: KnipIssueItem): string {
  return item.namespace ? `${item.namespace}.${item.name}` : item.name
}

function triageKey(file: string, kind: DeadExportTriageKind, symbol: string): string {
  return `${file}\0${kind}\0${symbol}`
}

function buildCandidateKeySet(candidateIssues: KnipIssue[]): Set<string> {
  const keys = new Set<string>()
  for (const issue of candidateIssues) {
    for (const item of issue.exports ?? []) {
      keys.add(triageKey(issue.file, 'export', itemName(item)))
    }
    for (const item of issue.types ?? []) {
      keys.add(triageKey(issue.file, 'type', itemName(item)))
    }
    for (const item of issue.duplicates ?? []) {
      keys.add(triageKey(issue.file, 'duplicate_export', itemName(item)))
    }
  }
  return keys
}

function readTriageLedger(): DeadExportTriageLedger {
  const path = resolve(root, triageLedgerPath)
  if (!existsSync(path)) {
    return {
      schemaVersion: 1,
      claimBoundary: 'No dead-export triage ledger is present yet.',
      records: [],
    }
  }

  return JSON.parse(readFileSync(path, 'utf8')) as DeadExportTriageLedger
}

function countTriageActions(records: DeadExportTriageReportRecord[]): Record<DeadExportTriageAction, number> {
  return records.reduce<Record<DeadExportTriageAction, number>>((counts, record) => ({
    ...counts,
    [record.action]: counts[record.action] + 1,
  }), {
    needs_runtime_guard: 0,
    review_for_removal: 0,
    defer_public_api: 0,
    keep_until_entrypoint_proven: 0,
  })
}

function buildReport(): DeadExportCandidatesReport {
  const versionCommand = runCommand('knip_version', ['knip', '--version'], ['6.16.1'])
  const knipCommand = runCommand('knip_exports_json', knipArgs, ['"issues"', '"exports"'])
  const knipJson = parseKnipJson(knipCommand)
  const issues = knipJson.issues ?? []
  const candidateIssues = issues.filter((issue) => (
    (issue.exports?.length ?? 0) > 0 || (issue.types?.length ?? 0) > 0 || (issue.duplicates?.length ?? 0) > 0
  ))
  const candidateUnusedExportCount = candidateIssues.reduce((count, issue) => count + (issue.exports?.length ?? 0), 0)
  const candidateUnusedTypeCount = candidateIssues.reduce((count, issue) => count + (issue.types?.length ?? 0), 0)
  const candidateDuplicateExportCount = candidateIssues.reduce((count, issue) => count + (issue.duplicates?.length ?? 0), 0)
  const candidateKeys = buildCandidateKeySet(candidateIssues)
  const triageLedger = readTriageLedger()
  const triageRecords = triageLedger.records.map<DeadExportTriageReportRecord>((record) => ({
    ...record,
    currentCandidate: candidateKeys.has(triageKey(record.file, record.kind, record.symbol)),
  }))
  const removedRatchets = removedCandidateRatchets.map<RemovedCandidateRatchet>((ratchet) => ({
    ...ratchet,
    currentCandidate: candidateKeys.has(triageKey(ratchet.file, ratchet.kind, ratchet.symbol)),
  }))

  const report: DeadExportCandidatesReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_dead_export_candidate_gate',
    scannerTarget: 'knip --config knip.jsonc --exports',
    knipVersion: versionCommand.stdoutPreview[0] ?? 'unknown',
    knipCommands: [stripCommand(knipCommand)],
    candidateFileCount: candidateIssues.length,
    candidateUnusedExportCount,
    candidateUnusedTypeCount,
    candidateDuplicateExportCount,
    candidateFileBaseline,
    candidateUnusedExportBaseline,
    candidateUnusedTypeBaseline,
    candidateDuplicateExportBaseline,
    sampleCandidateFiles: candidateIssues.slice(0, 20).map((issue) => ({
      file: issue.file,
      unusedExports: issue.exports?.length ?? 0,
      unusedTypes: issue.types?.length ?? 0,
      duplicateExports: issue.duplicates?.length ?? 0,
      sampleExports: (issue.exports ?? []).slice(0, 8).map(itemName),
      sampleTypes: (issue.types ?? []).slice(0, 8).map(itemName),
    })),
    triageLedgerPath,
    triageRecordCount: triageRecords.length,
    triageCurrentCandidateCount: triageRecords.filter((record) => record.currentCandidate).length,
    triageActionCounts: countTriageActions(triageRecords),
    triageRecords,
    removedCandidateRatchets: removedRatchets,
    primarySourceInputs: [
      {
        sourceType: 'oss_tool',
        sourceProject: 'Knip',
        sourceUrl: 'https://github.com/webpro-nl/knip',
        observedPattern: 'Knip detects unused files, dependencies, and exports in JavaScript and TypeScript projects and supports machine-readable JSON reporting.',
        localAbsorption: 'Metaforge records Knip unused-export candidates as a baseline only; no deletion or autofix claim follows from a candidate report.',
      },
      {
        sourceType: 'project_docs',
        sourceProject: 'Knip JSON reporter docs',
        sourceUrl: 'https://knip.dev/features/reporters',
        observedPattern: 'The JSON reporter is designed for tool consumption and exposes per-file issues.',
        localAbsorption: 'The product gate parses JSON reporter output and stores counts, samples, and claim boundaries for follow-up review.',
      },
      {
        sourceType: 'oss_tool',
        sourceProject: 'fallow',
        sourceUrl: 'https://github.com/fallow-rs/fallow',
        observedPattern: 'Fallow also treats unused files, unused exports, and stale cleanup opportunities as codebase intelligence rather than automatic deletion.',
        localAbsorption: 'Metaforge keeps cleanup-candidate evidence separate from refactor completion or runtime behavior claims.',
      },
    ],
    dependencyInstallPerformed: false,
    autofixPerformed: false,
    deletionPerformed: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    deletionClaimAllowed: false,
    cleanupCompletionClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    deadExportChecks: [],
    claimBoundary: 'Knip findings are candidate unused export/type/duplicate-export evidence only. They do not prove a symbol is safe to delete, that cleanup is complete, or that the repo is public-ready.',
  }

  report.deadExportChecks = [
    check('Knip version command passes', versionCommand.exitCode === 0 && versionCommand.passed, report.knipVersion),
    check('Knip exports JSON command passes', knipCommand.exitCode === 0 && knipCommand.passed, `${knipCommand.exitCode}`),
    check('candidate files are discovered', report.candidateFileCount > 0, `${report.candidateFileCount} files`),
    check('unused export candidates are discovered', report.candidateUnusedExportCount > 0, `${report.candidateUnusedExportCount} exports`),
    check('candidate files do not exceed baseline', report.candidateFileCount <= report.candidateFileBaseline, `${report.candidateFileCount}/${report.candidateFileBaseline}`),
    check('unused export candidates do not exceed baseline', report.candidateUnusedExportCount <= report.candidateUnusedExportBaseline, `${report.candidateUnusedExportCount}/${report.candidateUnusedExportBaseline}`),
    check('unused type candidates do not exceed baseline', report.candidateUnusedTypeCount <= report.candidateUnusedTypeBaseline, `${report.candidateUnusedTypeCount}/${report.candidateUnusedTypeBaseline}`),
    check('duplicate export candidates do not exceed baseline', report.candidateDuplicateExportCount <= report.candidateDuplicateExportBaseline, `${report.candidateDuplicateExportCount}/${report.candidateDuplicateExportBaseline}`),
    check('dead export triage ledger records reviewed candidates', report.triageRecordCount >= 3, `${report.triageRecordCount} records`),
    check('dead export triage entries remain current', report.triageRecordCount > 0 && report.triageCurrentCandidateCount === report.triageRecordCount, `${report.triageCurrentCandidateCount}/${report.triageRecordCount}`),
    check('dead export triage has runtime guard and removal-review actions', report.triageActionCounts.needs_runtime_guard > 0 && report.triageActionCounts.review_for_removal > 0, JSON.stringify(report.triageActionCounts)),
    check('dead export triage records guardrails and rationales', report.triageRecords.every((record) => record.rationale.length > 20 && record.guardrail.length > 20), `${report.triageRecordCount} records`),
    check('removed dead export ratchets remain absent', report.removedCandidateRatchets.every((ratchet) => !ratchet.currentCandidate), `${report.removedCandidateRatchets.filter((ratchet) => ratchet.currentCandidate).length}/${report.removedCandidateRatchets.length} regressed`),
    check(
      'primary sources include Knip docs and fallow comparator',
      ['Knip', 'Knip JSON reporter docs', 'fallow'].every((source) => report.primarySourceInputs.some((item) => item.sourceProject === source)),
      report.primarySourceInputs.map((source) => source.sourceProject).join(','),
    ),
    check('provider/live/external calls remain absent', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0, 'all call arrays empty'),
    check('protected actions remain absent', report.protectedActionsExecuted.length === 0, 'zero'),
    check('autofix deletion and readiness claims remain blocked', report.autofixPerformed === false && report.deletionPerformed === false && report.deletionClaimAllowed === false && report.cleanupCompletionClaimAllowed === false && report.publicReadinessClaimAllowed === false, 'all false'),
  ]

  return report
}

function writeMarkdown(report: DeadExportCandidatesReport): void {
  const commandRows = report.knipCommands
    .map((command) => `| ${command.name} | \`${command.command.join(' ')}\` | \`${command.passed}\` | \`${command.exitCode ?? 'null'}\` | ${command.missingSubstrings.length === 0 ? 'none' : command.missingSubstrings.map((item) => `\`${item}\``).join('<br>')} |`)
    .join('\n')
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceType} | ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const sampleRows = report.sampleCandidateFiles
    .map((item) => `| \`${item.file}\` | ${item.unusedExports} | ${item.unusedTypes} | ${item.duplicateExports} | ${item.sampleExports.map((sample) => `\`${sample}\``).join('<br>') || 'none'} |`)
    .join('\n')
  const triageRows = report.triageRecords
    .map((item) => `| \`${item.file}\` | \`${item.kind}\` | \`${item.symbol}\` | \`${item.action}\` | \`${item.currentCandidate}\` | ${item.guardrail} |`)
    .join('\n')
  const ratchetRows = report.removedCandidateRatchets
    .map((item) => `| \`${item.file}\` | \`${item.kind}\` | \`${item.symbol}\` | \`${item.currentCandidate}\` | ${item.guardrail} |`)
    .join('\n')
  const checkRows = report.deadExportChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Dead Export Candidates Report

Generated by: \`bun run product:dead-export-candidates\`

## Claim Boundary

- This is a local no-provider Knip candidate baseline.
- It uses \`knip --config knip.jsonc --exports --reporter json --no-exit-code --no-progress\`.
- It does not run Knip autofix, delete files, or prove that candidates are safe to remove.
- It does not prove cleanup completion, public readiness, release readiness, or external validation.

## Summary

- knip_version: \`${report.knipVersion}\`
- scanner_target: \`${report.scannerTarget}\`
- candidate_file_count: \`${report.candidateFileCount}\`
- candidate_file_baseline: \`${report.candidateFileBaseline}\`
- candidate_unused_export_count: \`${report.candidateUnusedExportCount}\`
- candidate_unused_export_baseline: \`${report.candidateUnusedExportBaseline}\`
- candidate_unused_type_count: \`${report.candidateUnusedTypeCount}\`
- candidate_unused_type_baseline: \`${report.candidateUnusedTypeBaseline}\`
- candidate_duplicate_export_count: \`${report.candidateDuplicateExportCount}\`
- candidate_duplicate_export_baseline: \`${report.candidateDuplicateExportBaseline}\`
- triage_ledger_path: \`${report.triageLedgerPath}\`
- triage_record_count: \`${report.triageRecordCount}\`
- triage_current_candidate_count: \`${report.triageCurrentCandidateCount}\`
- triage_action_counts: \`${JSON.stringify(report.triageActionCounts)}\`
- deletion_claim_allowed: \`${report.deletionClaimAllowed}\`
- cleanup_completion_claim_allowed: \`${report.cleanupCompletionClaimAllowed}\`
- public_readiness_claim_allowed: \`${report.publicReadinessClaimAllowed}\`

## Commands

| Command | Args | Passed | Exit | Missing Substrings |
| --- | --- | --- | ---: | --- |
${commandRows}

## Primary Sources

| Type | Source | URL | Local Absorption |
| --- | --- | --- | --- |
${sourceRows}

## Sample Candidate Files

| File | Unused Exports | Unused Types | Duplicate Exports | Sample Exports |
| --- | ---: | ---: | ---: | --- |
${sampleRows || '| none | 0 | 0 | 0 | none |'}

## Triage Ledger

| File | Kind | Symbol | Action | Current Candidate | Guardrail |
| --- | --- | --- | --- | --- | --- |
${triageRows || '| none | none | none | none | none | none |'}

## Removed Candidate Ratchets

| File | Kind | Symbol | Current Candidate | Guardrail |
| --- | --- | --- | --- | --- |
${ratchetRows || '| none | none | none | none | none |'}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  const report = buildReport()
  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of report.deadExportChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.deadExportChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`knip_version=${report.knipVersion}`)
  console.log(`dead_export_candidate_files=${report.candidateFileCount}`)
  console.log(`dead_export_candidate_unused_exports=${report.candidateUnusedExportCount}`)
  console.log(`dead_export_candidate_unused_types=${report.candidateUnusedTypeCount}`)
  console.log(`dead_export_candidate_duplicate_exports=${report.candidateDuplicateExportCount}`)
}

main()
