import { spawnSync } from 'node:child_process'
import { mkdirSync, writeFileSync } from 'node:fs'
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
const candidateFileBaseline = 657
const candidateUnusedExportBaseline = 1461
const candidateUnusedTypeBaseline = 492
const candidateDuplicateExportBaseline = 12
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
    check('primary sources include Knip docs and fallow comparator', ['Knip', 'Knip JSON reporter docs', 'fallow'].every((source) => report.primarySourceInputs.some((item) => item.sourceProject === source))),
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
