import { spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { check, readText, sha256, type Check } from './quality-report-helpers'

type RemediationPriority = 'P0' | 'P1' | 'P2' | 'P3'
type RemediationClass =
  | 'new_dependency_violation'
  | 'dead_export_runtime_guard'
  | 'duplicate_helper_extraction'
  | 'clone_hotspot_review'
  | 'known_dependency_knot'
  | 'dead_export_cleanup_review'

type SourceInput = {
  sourceType: 'oss_tool' | 'project_docs' | 'research_survey' | 'patent'
  sourceProject: string
  sourceUrl: string
  observedPattern: string
  localAbsorption: string
}

type DeadExportTriageRecord = {
  file: string
  symbol: string
  action: string
  currentCandidate: boolean
}

type DeadExportInput = {
  candidateFileCount: number
  candidateUnusedExportCount: number
  candidateUnusedTypeCount: number
  candidateDuplicateExportCount: number
  triageRecords: DeadExportTriageRecord[]
}

type DependencyTopologyInput = {
  circularDependencyCount: number
  unresolvedDependencyCount: number
  configuredRatchetNewViolationCount: number
  sampleCircularEdges: Array<{ source: string; resolved: string }>
  sampleUnresolvedEdges: Array<{ source: string; module: string }>
}

type JscpdTopClonePair = {
  firstFile: string
  secondFile: string
  firstStartLine: number
  firstEndLine: number
  secondStartLine: number
  secondEndLine: number
  lines: number
  tokens: number
}

type ScriptDuplicationInput = {
  duplicateHelperClusterCount: number
  helperOccurrenceCounts: Record<string, number>
  jscpdCloneCount: number
  jscpdDuplicatedLines: number
  jscpdDuplicatedTokens: number
  jscpdDuplicatedPercentage: number
  jscpdTopClonePairs: JscpdTopClonePair[]
}

export type StaticAnalysisRemediationInput = {
  repository: string
  sourceCommit: string
  generatedFrom: string[]
  deadExport: DeadExportInput
  dependencyTopology: DependencyTopologyInput
  scriptDuplication: ScriptDuplicationInput
}

type StaticAnalysisQueueItem = {
  queueId: string
  priority: RemediationPriority
  remediationClass: RemediationClass
  evidenceSource: 'knip' | 'dependency-cruiser' | 'jscpd'
  evidenceCount: number
  sampleLocations: string[]
  safeFirstStep: string
  validationCommands: string[]
  ownerDecisionRequired: boolean
  claimBoundary: string
}

export type StaticAnalysisRemediationQueueReport = {
  generatedAt: string
  mode: 'local_no_provider_static_analysis_remediation_queue'
  repository: string
  sourceCommit: string
  generatedFrom: string[]
  status: 'remediation_queue_required' | 'no_static_analysis_work_items'
  primarySourceInputs: SourceInput[]
  queueItems: StaticAnalysisQueueItem[]
  queueItemCount: number
  deadExport: DeadExportInput
  dependencyTopology: DependencyTopologyInput
  scriptDuplication: ScriptDuplicationInput
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  deletionPerformed: false
  autofixPerformed: false
  dependencyInstallPerformed: false
  cleanupCompletionClaimAllowed: false
  topologyCleanClaimAllowed: false
  refactorCompletionClaimAllowed: false
  publicReadinessClaimAllowed: false
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const reportJsonPath = 'docs/product-quality/static-analysis-remediation-queue-report.json'
const reportMdPath = 'docs/product-quality/static-analysis-remediation-queue-report.md'
const reportJsonlPath = 'reports/openclaude-static-analysis-remediation-queue.jsonl'
const deadExportReportPath = 'docs/product-quality/dead-export-candidates-report.json'
const topologyReportPath = 'docs/product-quality/dependency-topology-report.json'
const duplicationReportPath = 'docs/product-quality/script-duplication-audit-report.json'

const baseValidationCommands = [
  'bun run product:dead-export-candidates',
  'bun run product:dependency-topology',
  'bun run product:script-duplication-audit',
  'bun run product:static-analysis-remediation-queue',
  'bun run product:typecheck-health',
]

function priorityRank(priority: RemediationPriority): number {
  return { P0: 0, P1: 1, P2: 2, P3: 3 }[priority]
}

function primarySourceInputs(): SourceInput[] {
  return [
    {
      sourceType: 'project_docs',
      sourceProject: 'Knip JSON reporter docs',
      sourceUrl: 'https://knip.dev/features/reporters',
      observedPattern: 'Knip JSON reporter output is machine-readable and groups issue arrays by file.',
      localAbsorption: 'Metaforge turns existing Knip dead-export candidates into ordered queue work without claiming deletion safety.',
    },
    {
      sourceType: 'oss_tool',
      sourceProject: 'jscpd',
      sourceUrl: 'https://github.com/kucherenko/jscpd',
      observedPattern: 'jscpd detects copy/paste clones and exposes report formats suitable for agents and CI follow-up.',
      localAbsorption: 'Metaforge uses current jscpd clone pairs as clone-hotspot queue inputs, not as automatic refactor instructions.',
    },
    {
      sourceType: 'oss_tool',
      sourceProject: 'dependency-cruiser',
      sourceUrl: 'https://github.com/sverweij/dependency-cruiser/blob/main/doc/cli.md',
      observedPattern: 'dependency-cruiser supports baselining known violations and focusing future runs on new violations.',
      localAbsorption: 'Metaforge prioritizes new topology ratchet violations ahead of ordinary cleanup candidates.',
    },
    {
      sourceType: 'oss_tool',
      sourceProject: 'fallow',
      sourceUrl: 'https://github.com/fallow-rs/fallow',
      observedPattern: 'Fallow frames static analysis as health, hotspot, refactor, and safe-removal evidence for maintainers and agents.',
      localAbsorption: 'Metaforge absorbs that queue shape while reusing its already pinned Knip, jscpd, and dependency-cruiser reports.',
    },
    {
      sourceType: 'research_survey',
      sourceProject: 'Roy and Cordy clone detection survey',
      sourceUrl: 'https://research.cs.queensu.ca/TechReports/Reports/2007-541.pdf',
      observedPattern: 'Clone detection identifies maintenance candidates that need classification and human review.',
      localAbsorption: 'Metaforge keeps clone hits as prioritized work items rather than proof of refactor completion.',
    },
    {
      sourceType: 'patent',
      sourceProject: 'US11662998B2 duplicate code pattern patent',
      sourceUrl: 'https://patents.google.com/patent/US11662998B2/en',
      observedPattern: 'Duplicate-pattern systems identify candidate pairs and surface refactor opportunities.',
      localAbsorption: 'Metaforge records duplicate-script hotspots before attempting shared-helper extraction.',
    },
    {
      sourceType: 'patent',
      sourceProject: 'US7904892B2 dependency graph cycle patent',
      sourceUrl: 'https://patents.google.com/patent/US7904892B2/en',
      observedPattern: 'Dependency graph systems model component relationships and cycles.',
      localAbsorption: 'Metaforge keeps topology remediation separate from duplicate-code and dead-export cleanup.',
    },
  ]
}

function queueItem(item: Omit<StaticAnalysisQueueItem, 'validationCommands' | 'claimBoundary'> & {
  validationCommands?: string[]
}): StaticAnalysisQueueItem {
  return {
    ...item,
    validationCommands: item.validationCommands ?? baseValidationCommands,
    claimBoundary: 'This queue item is a remediation candidate only. It does not prove cleanup completion, topology cleanliness, refactor completion, public readiness, or external validation.',
  }
}

function formatClonePair(pair: JscpdTopClonePair): string {
  return `${pair.firstFile}:${pair.firstStartLine}-${pair.firstEndLine} <-> ${pair.secondFile}:${pair.secondStartLine}-${pair.secondEndLine}`
}

function buildQueueItems(input: StaticAnalysisRemediationInput): StaticAnalysisQueueItem[] {
  const runtimeGuardRecords = input.deadExport.triageRecords
    .filter((record) => record.currentCandidate && record.action === 'needs_runtime_guard')
  const removalReviewRecords = input.deadExport.triageRecords
    .filter((record) => record.currentCandidate && record.action === 'review_for_removal')

  const items: StaticAnalysisQueueItem[] = []
  if (input.dependencyTopology.configuredRatchetNewViolationCount > 0) {
    items.push(queueItem({
      queueId: 'static-analysis-new-dependency-violations',
      priority: 'P0',
      remediationClass: 'new_dependency_violation',
      evidenceSource: 'dependency-cruiser',
      evidenceCount: input.dependencyTopology.configuredRatchetNewViolationCount,
      sampleLocations: [
        ...input.dependencyTopology.sampleCircularEdges.slice(0, 3).map((edge) => `${edge.source} -> ${edge.resolved}`),
        ...input.dependencyTopology.sampleUnresolvedEdges.slice(0, 3).map((edge) => `${edge.source} -> ${edge.module}`),
      ],
      safeFirstStep: 'Inspect new dependency-cruiser ratchet violations first, then either fix the import/cycle or explicitly update the known-violation baseline with a narrow rationale.',
      ownerDecisionRequired: true,
      validationCommands: ['bun run product:dependency-topology', ...baseValidationCommands],
    }))
  }

  if (runtimeGuardRecords.length > 0) {
    items.push(queueItem({
      queueId: 'static-analysis-dead-export-runtime-guards',
      priority: 'P1',
      remediationClass: 'dead_export_runtime_guard',
      evidenceSource: 'knip',
      evidenceCount: runtimeGuardRecords.length,
      sampleLocations: runtimeGuardRecords.slice(0, 5).map((record) => `${record.file}#${record.symbol}`),
      safeFirstStep: 'Add or verify runtime guards for side-effect-sensitive exported candidates before any deletion or export narrowing.',
      ownerDecisionRequired: true,
      validationCommands: ['bun run product:dead-export-candidates', ...baseValidationCommands],
    }))
  }

  if (input.scriptDuplication.duplicateHelperClusterCount > 0) {
    items.push(queueItem({
      queueId: 'static-analysis-duplicate-helper-clusters',
      priority: 'P2',
      remediationClass: 'duplicate_helper_extraction',
      evidenceSource: 'jscpd',
      evidenceCount: Object.values(input.scriptDuplication.helperOccurrenceCounts).reduce((total, count) => total + count, 0),
      sampleLocations: Object.entries(input.scriptDuplication.helperOccurrenceCounts)
        .filter(([, count]) => count > 0)
        .map(([name, count]) => `${name}:${count}`),
      safeFirstStep: 'Extract or reuse a shared helper only for the smallest product-script family whose behavior is covered by focused tests.',
      ownerDecisionRequired: true,
      validationCommands: ['bun run product:script-duplication-audit', ...baseValidationCommands],
    }))
  }

  if (input.scriptDuplication.jscpdCloneCount > 0) {
    items.push(queueItem({
      queueId: 'static-analysis-jscpd-clone-hotspots',
      priority: 'P2',
      remediationClass: 'clone_hotspot_review',
      evidenceSource: 'jscpd',
      evidenceCount: input.scriptDuplication.jscpdCloneCount,
      sampleLocations: input.scriptDuplication.jscpdTopClonePairs.slice(0, 5).map(formatClonePair),
      safeFirstStep: 'Review the top jscpd clone pair, classify whether it is shared infrastructure or intentional parallel evidence, then patch one test-backed extraction at a time.',
      ownerDecisionRequired: true,
      validationCommands: ['bun run product:script-duplication-audit', ...baseValidationCommands],
    }))
  }

  if (input.dependencyTopology.circularDependencyCount > 0 || input.dependencyTopology.unresolvedDependencyCount > 0) {
    items.push(queueItem({
      queueId: 'static-analysis-known-topology-knots',
      priority: 'P3',
      remediationClass: 'known_dependency_knot',
      evidenceSource: 'dependency-cruiser',
      evidenceCount: input.dependencyTopology.circularDependencyCount + input.dependencyTopology.unresolvedDependencyCount,
      sampleLocations: [
        ...input.dependencyTopology.sampleCircularEdges.slice(0, 3).map((edge) => `${edge.source} -> ${edge.resolved}`),
        ...input.dependencyTopology.sampleUnresolvedEdges.slice(0, 3).map((edge) => `${edge.source} -> ${edge.module}`),
      ],
      safeFirstStep: 'Pick one high-locality cycle or unresolved import cluster and add a behavior-preserving regression before changing module boundaries.',
      ownerDecisionRequired: true,
      validationCommands: ['bun run product:dependency-topology', ...baseValidationCommands],
    }))
  }

  if (removalReviewRecords.length > 0) {
    items.push(queueItem({
      queueId: 'static-analysis-dead-export-removal-review',
      priority: 'P3',
      remediationClass: 'dead_export_cleanup_review',
      evidenceSource: 'knip',
      evidenceCount: removalReviewRecords.length,
      sampleLocations: removalReviewRecords.slice(0, 5).map((record) => `${record.file}#${record.symbol}`),
      safeFirstStep: 'Review ordinary Knip removal candidates after runtime-guard candidates, and delete only when tests and docs prove the symbol is not part of a public or fixture boundary.',
      ownerDecisionRequired: false,
      validationCommands: ['bun run product:dead-export-candidates', ...baseValidationCommands],
    }))
  }

  return items.sort((left, right) => {
    const priorityDelta = priorityRank(left.priority) - priorityRank(right.priority)
    if (priorityDelta !== 0) return priorityDelta
    return right.evidenceCount - left.evidenceCount || left.queueId.localeCompare(right.queueId)
  })
}

export function buildStaticAnalysisRemediationQueue(input: StaticAnalysisRemediationInput): StaticAnalysisRemediationQueueReport {
  const queueItems = buildQueueItems(input)
  const sourceTypes = new Set(primarySourceInputs().map((source) => source.sourceType))
  const evidenceSources = new Set(queueItems.map((item) => item.evidenceSource))
  const report: StaticAnalysisRemediationQueueReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_static_analysis_remediation_queue',
    repository: input.repository,
    sourceCommit: input.sourceCommit,
    generatedFrom: input.generatedFrom,
    status: queueItems.length > 0 ? 'remediation_queue_required' : 'no_static_analysis_work_items',
    primarySourceInputs: primarySourceInputs(),
    queueItems,
    queueItemCount: queueItems.length,
    deadExport: input.deadExport,
    dependencyTopology: input.dependencyTopology,
    scriptDuplication: input.scriptDuplication,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    deletionPerformed: false,
    autofixPerformed: false,
    dependencyInstallPerformed: false,
    cleanupCompletionClaimAllowed: false,
    topologyCleanClaimAllowed: false,
    refactorCompletionClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    evidenceChecks: [],
    claimBoundary: 'Static-analysis remediation queue only. It orders local Knip, dependency-cruiser, and jscpd findings for follow-up; it does not delete, autofix, refactor, prove cleanup completion, prove topology cleanliness, or claim public readiness.',
  }

  report.evidenceChecks = [
    check('static-analysis source reports are declared', report.generatedFrom.length >= 3, report.generatedFrom.join(',')),
    check('queue items are generated from current static-analysis findings', report.queueItemCount > 0, `${report.queueItemCount} items`),
    check('queue covers existing static-analysis tools when findings exist', ['knip', 'dependency-cruiser', 'jscpd'].every((source) => evidenceSources.has(source as StaticAnalysisQueueItem['evidenceSource'])), [...evidenceSources].join(',')),
    check('new dependency violations are prioritized first when present', input.dependencyTopology.configuredRatchetNewViolationCount === 0 || report.queueItems[0]?.queueId === 'static-analysis-new-dependency-violations', report.queueItems.map((item) => `${item.priority}:${item.queueId}`).join(',')),
    check('primary sources cover OSS docs research and patent inputs', ['oss_tool', 'project_docs', 'research_survey', 'patent'].every((sourceType) => sourceTypes.has(sourceType as SourceInput['sourceType'])), [...sourceTypes].join(',')),
    check('queue item paths are relative and local-safe', report.queueItems.every((item) => item.sampleLocations.every((sample) => !/[A-Za-z]:\\/.test(sample) && !sample.includes(root))), `${report.queueItemCount} items`),
    check('no provider live external protected dependency install or autofix action occurred', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0 && report.protectedActionsExecuted.length === 0 && !report.dependencyInstallPerformed && !report.autofixPerformed && !report.deletionPerformed, 'all action flags empty/false'),
    check('cleanup topology refactor and public-readiness claims remain blocked', !report.cleanupCompletionClaimAllowed && !report.topologyCleanClaimAllowed && !report.refactorCompletionClaimAllowed && !report.publicReadinessClaimAllowed, 'all claim flags false'),
  ]

  return report
}

export function buildStaticAnalysisRemediationQueueJsonl(report: StaticAnalysisRemediationQueueReport): string {
  const records = report.queueItems.map((item) => ({
    kind: 'static_analysis_remediation_queue_item',
    repository: report.repository,
    sourceCommit: report.sourceCommit,
    queueId: item.queueId,
    priority: item.priority,
    remediationClass: item.remediationClass,
    evidenceSource: item.evidenceSource,
    evidenceCount: item.evidenceCount,
    ownerDecisionRequired: item.ownerDecisionRequired,
    sampleLocations: item.sampleLocations,
  }))
  return `${records.map((record) => JSON.stringify(record)).join('\n')}\n`
}

function readGitHead(): string {
  const result = spawnSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8', shell: false })
  return result.status === 0 ? result.stdout.trim() : 'unknown'
}

function readJson<T>(path: string): T {
  return JSON.parse(readText(path, root)) as T
}

function readInput(): StaticAnalysisRemediationInput {
  const deadExport = readJson<DeadExportInput>(deadExportReportPath)
  const dependencyTopology = readJson<DependencyTopologyInput>(topologyReportPath)
  const scriptDuplication = readJson<ScriptDuplicationInput>(duplicationReportPath)
  return {
    repository: 'svy04/metaforge',
    sourceCommit: readGitHead(),
    generatedFrom: [deadExportReportPath, topologyReportPath, duplicationReportPath],
    deadExport,
    dependencyTopology,
    scriptDuplication,
  }
}

function writeMarkdown(report: StaticAnalysisRemediationQueueReport, jsonlSha256: string): void {
  const queueRows = report.queueItems
    .map((item) => `| \`${item.priority}\` | \`${item.queueId}\` | \`${item.evidenceSource}\` | ${item.evidenceCount} | \`${item.remediationClass}\` | \`${item.ownerDecisionRequired}\` | ${item.safeFirstStep} |`)
    .join('\n')
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceType} | ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const sampleRows = report.queueItems
    .flatMap((item) => item.sampleLocations.slice(0, 8).map((sample) => `| \`${item.queueId}\` | ${sample} |`))
    .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Static Analysis Remediation Queue

Generated by: \`bun run product:static-analysis-remediation-queue\`

## Claim Boundary

- This report orders existing Knip, dependency-cruiser, and jscpd findings into local remediation candidates.
- It does not install dependencies, call providers, call live models, call external services, execute protected actions, delete code, autofix findings, or mutate hosted settings.
- It does not prove cleanup completion, topology cleanliness, refactor completion, public readiness, release readiness, production readiness, external validation, or autonomous reliability.

## Summary

- repository: \`${report.repository}\`
- source_commit: \`${report.sourceCommit}\`
- generated_from: \`${report.generatedFrom.join(',')}\`
- status: \`${report.status}\`
- queue_item_count: \`${report.queueItemCount}\`
- jsonl_sha256: \`${jsonlSha256}\`
- dead_export_candidate_files: \`${report.deadExport.candidateFileCount}\`
- dead_export_candidate_unused_exports: \`${report.deadExport.candidateUnusedExportCount}\`
- dependency_topology_cycles: \`${report.dependencyTopology.circularDependencyCount}\`
- dependency_topology_unresolved: \`${report.dependencyTopology.unresolvedDependencyCount}\`
- dependency_topology_new_violations: \`${report.dependencyTopology.configuredRatchetNewViolationCount}\`
- jscpd_clone_count: \`${report.scriptDuplication.jscpdCloneCount}\`
- jscpd_duplicated_lines: \`${report.scriptDuplication.jscpdDuplicatedLines}\`
- cleanup_completion_claim_allowed: \`${report.cleanupCompletionClaimAllowed}\`
- topology_clean_claim_allowed: \`${report.topologyCleanClaimAllowed}\`
- refactor_completion_claim_allowed: \`${report.refactorCompletionClaimAllowed}\`
- public_readiness_claim_allowed: \`${report.publicReadinessClaimAllowed}\`

## Queue

| Priority | Queue ID | Evidence Source | Evidence Count | Class | Owner Decision Required | Safe First Step |
| --- | --- | --- | ---: | --- | --- | --- |
${queueRows || '| none | none | none | 0 | none | false | no queue items |'}

## Samples

| Queue ID | Sample |
| --- | --- |
${sampleRows || '| none | none |'}

## Primary Sources

| Type | Source | URL | Local Absorption |
| --- | --- | --- | --- |
${sourceRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function writeReports(report: StaticAnalysisRemediationQueueReport): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })
  const jsonl = buildStaticAnalysisRemediationQueueJsonl(report)
  const jsonlSha256 = sha256(jsonl)
  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeFileSync(resolve(root, reportJsonlPath), jsonl)
  writeMarkdown(report, jsonlSha256)
}

function main(): void {
  for (const path of [deadExportReportPath, topologyReportPath, duplicationReportPath]) {
    if (!existsSync(resolve(root, path))) {
      console.error(`Missing required static-analysis report: ${path}`)
      process.exit(1)
    }
  }

  const report = buildStaticAnalysisRemediationQueue(readInput())
  writeReports(report)

  for (const item of report.evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')
  console.log(`RESULT: ${report.evidenceChecks.every((item) => item.ok) ? 'PASS' : 'FAIL'}`)
  console.log(`queue_item_count=${report.queueItemCount}`)
  console.log(`dependency_topology_new_violations=${report.dependencyTopology.configuredRatchetNewViolationCount}`)
  console.log(`cleanup_completion_claim_allowed=${report.cleanupCompletionClaimAllowed}`)
  console.log(`topology_clean_claim_allowed=${report.topologyCleanClaimAllowed}`)

  if (!report.evidenceChecks.every((item) => item.ok)) {
    process.exit(1)
  }
}

if (import.meta.main) {
  main()
}
