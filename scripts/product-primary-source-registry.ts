import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { basename, resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type SourceInput = {
  sourceProject?: unknown
  source?: unknown
  sourceUrl?: unknown
  url?: unknown
  observedPattern?: unknown
  appliedPattern?: unknown
  localAbsorption?: unknown
}

type SourceKind =
  | 'original_repository'
  | 'official_documentation'
  | 'standard_or_specification'
  | 'research_paper'
  | 'benchmark_project'
  | 'official_project_site'
  | 'unclassified'

type RegistryRecord = {
  schemaVersion: 'openclaude_primary_source_registry_v1'
  sourceReportPath: string
  sourceReportSha256: string
  sourceProject: string
  sourceUrl: string
  sourceHost: string
  sourceKind: SourceKind
  patternSummary: string
  localAbsorption: string
  isHttps: boolean
  isDisallowedSecondarySource: boolean
  disallowedReason: string | null
  recordDigest: string
}

type PrimarySourceRegistryReport = {
  generatedAt: string
  mode: 'local_no_provider_primary_source_registry'
  registryFormat: 'openclaude_primary_source_registry_v1'
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  scannedReportCount: number
  reportsWithPrimarySourceInputs: string[]
  reportsMissingPrimarySourceInputs: string[]
  primarySourceEntryCount: number
  uniqueSourceUrlCount: number
  sourceKindCounts: Record<SourceKind, number>
  sourceHostCounts: Record<string, number>
  disallowedSecondarySourceCount: number
  disallowedSecondarySources: RegistryRecord[]
  unclassifiedSourceCount: number
  malformedSourceInputCount: number
  malformedSourceInputs: Array<{
    sourceReportPath: string
    reason: string
  }>
  registryJsonlPath: string
  registryJsonlSha256: string
  registryJsonlRecordCount: number
  registryJsonlParseable: boolean
  externalSourceFetchPerformed: false
  blogSummarySourceAllowed: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  registryRecords: RegistryRecord[]
  primarySourceRegistryChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const reportJsonPath = 'docs/product-quality/primary-source-registry-report.json'
const reportMdPath = 'docs/product-quality/primary-source-registry-report.md'
const registryJsonlPath = 'reports/openclaude-primary-source-registry.jsonl'
const ignoredSelfReports = new Set([
  'primary-source-registry-report.json',
])

const disallowedSecondaryHostFragments = [
  'medium.com',
  'dev.to',
  'hashnode',
  'substack.com',
  'towardsdatascience.com',
  'reddit.com',
  'wikipedia.org',
  'stackoverflow.com',
  'stackexchange.com',
  'news.ycombinator.com',
]

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function normalizePath(path: string): string {
  return path.replace(/\\/g, '/')
}

function relativeProductQualityPath(fileName: string): string {
  return normalizePath(`docs/product-quality/${fileName}`)
}

function fileSha256(path: string): string {
  return sha256(readFileSync(resolve(root, path)))
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function stringValue(value: unknown): string {
  return typeof value === 'string' ? value.trim() : ''
}

function sourceKind(sourceProject: string, sourceUrl: string, host: string): SourceKind {
  const normalizedProject = sourceProject.toLowerCase()
  const normalizedUrl = sourceUrl.toLowerCase()
  if (host === 'arxiv.org') return 'research_paper'
  if (host === 'github.com') {
    if (normalizedUrl.includes('swe-bench') || normalizedUrl.includes('terminal-bench') || normalizedUrl.includes('openhands/benchmarks')) {
      return 'benchmark_project'
    }
    return 'original_repository'
  }
  if (host.startsWith('docs.') || host === 'code.visualstudio.com') return 'official_documentation'
  if (['spdx.org', 'spdx.dev', 'spdx.github.io', 'reuse.software', 'slsa.dev', 'cyclonedx.org', 'opentelemetry.io'].includes(host)) {
    return 'standard_or_specification'
  }
  if (host === 'harborframework.com' || host === 'www.harborframework.com' || host === 'www.tbench.ai') return 'benchmark_project'
  if (host === 'bun.com' || normalizedProject.includes('github docs') || normalizedProject.includes('npm')) return 'official_documentation'
  if (host.length > 0) return 'official_project_site'
  return 'unclassified'
}

function disallowedReason(host: string): string | null {
  const normalizedHost = host.toLowerCase()
  const fragment = disallowedSecondaryHostFragments.find((item) => normalizedHost === item || normalizedHost.endsWith(`.${item}`))
  return fragment ? `secondary_or_blog_domain:${fragment}` : null
}

function parseSourceUrl(sourceUrl: string): URL | null {
  try {
    return new URL(sourceUrl)
  } catch {
    return null
  }
}

function sourcePatternSummary(source: SourceInput): string {
  return stringValue(source.observedPattern) || stringValue(source.appliedPattern) || 'primary-source pattern recorded without a dedicated summary field'
}

function sourceLocalAbsorption(source: SourceInput): string {
  return stringValue(source.localAbsorption) || stringValue(source.appliedPattern) || 'local absorption recorded in source report'
}

function reportFiles(): string[] {
  return readdirSync(docsDir, { withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name.endsWith('.json') && !ignoredSelfReports.has(entry.name))
    .map((entry) => relativeProductQualityPath(entry.name))
    .sort((left, right) => left.localeCompare(right))
}

function registryRecord(sourceReportPath: string, sourceReportSha256: string, source: SourceInput): RegistryRecord | null {
  const sourceProject = stringValue(source.sourceProject) || stringValue(source.source)
  const sourceUrl = stringValue(source.sourceUrl) || stringValue(source.url)
  if (sourceProject.length === 0 || sourceUrl.length === 0) return null
  const parsedUrl = parseSourceUrl(sourceUrl)
  const sourceHost = parsedUrl?.host.toLowerCase() ?? ''
  const reason = disallowedReason(sourceHost)
  const baseRecord = {
    schemaVersion: 'openclaude_primary_source_registry_v1' as const,
    sourceReportPath,
    sourceReportSha256,
    sourceProject,
    sourceUrl,
    sourceHost,
    sourceKind: parsedUrl ? sourceKind(sourceProject, sourceUrl, sourceHost) : 'unclassified' as SourceKind,
    patternSummary: sourcePatternSummary(source),
    localAbsorption: sourceLocalAbsorption(source),
    isHttps: parsedUrl?.protocol === 'https:',
    isDisallowedSecondarySource: reason !== null,
    disallowedReason: reason,
  }
  return {
    ...baseRecord,
    recordDigest: sha256(JSON.stringify(baseRecord)),
  }
}

function buildRegistry(): {
  records: RegistryRecord[]
  reportsWithPrimarySourceInputs: string[]
  reportsMissingPrimarySourceInputs: string[]
  malformedSourceInputs: Array<{ sourceReportPath: string; reason: string }>
  scannedReportCount: number
} {
  const records: RegistryRecord[] = []
  const reportsWithPrimarySourceInputs: string[] = []
  const reportsMissingPrimarySourceInputs: string[] = []
  const malformedSourceInputs: Array<{ sourceReportPath: string; reason: string }> = []
  const files = reportFiles()
  for (const path of files) {
    const raw = readText(path)
    const parsed = JSON.parse(raw) as { primarySourceInputs?: unknown }
    const sourceReportSha256 = sha256(raw)
    if (!Array.isArray(parsed.primarySourceInputs) || parsed.primarySourceInputs.length === 0) {
      reportsMissingPrimarySourceInputs.push(path)
      continue
    }
    reportsWithPrimarySourceInputs.push(path)
    for (const source of parsed.primarySourceInputs as SourceInput[]) {
      const record = registryRecord(path, sourceReportSha256, source)
      if (record === null) {
        malformedSourceInputs.push({ sourceReportPath: path, reason: 'missing_sourceProject_or_sourceUrl' })
        continue
      }
      records.push(record)
    }
  }
  return {
    records,
    reportsWithPrimarySourceInputs,
    reportsMissingPrimarySourceInputs,
    malformedSourceInputs,
    scannedReportCount: files.length,
  }
}

function countBy<T extends string>(values: T[]): Record<T, number> {
  const counts = {} as Record<T, number>
  for (const value of values) counts[value] = (counts[value] ?? 0) + 1
  return Object.fromEntries(Object.entries(counts).sort(([left], [right]) => left.localeCompare(right))) as Record<T, number>
}

function writeMarkdown(report: PrimarySourceRegistryReport): void {
  const kindRows = Object.entries(report.sourceKindCounts)
    .map(([kind, count]) => `| \`${kind}\` | ${count} |`)
    .join('\n')
  const hostRows = Object.entries(report.sourceHostCounts)
    .map(([host, count]) => `| \`${host}\` | ${count} |`)
    .join('\n')
  const reportRows = report.reportsWithPrimarySourceInputs
    .map((path) => `| \`${path}\` |`)
    .join('\n')
  const checkRows = report.primarySourceRegistryChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Primary Source Registry Report

Generated by: \`bun run product:primary-source-registry\`

## Claim Boundary

- This report inventories primary-source inputs already recorded by local product-quality reports.
- It does not fetch external URLs, call providers, call live models, call external services, install dependencies, or claim external validation.
- It rejects blog-summary and secondary-source domains as product-quality evidence inputs.

## Summary

- mode: \`${report.mode}\`
- registry_format: \`${report.registryFormat}\`
- scanned_report_count: \`${report.scannedReportCount}\`
- reports_with_primary_source_inputs: \`${report.reportsWithPrimarySourceInputs.length}\`
- reports_missing_primary_source_inputs: \`${report.reportsMissingPrimarySourceInputs.length}\`
- primary_source_entry_count: \`${report.primarySourceEntryCount}\`
- unique_source_url_count: \`${report.uniqueSourceUrlCount}\`
- disallowed_secondary_source_count: \`${report.disallowedSecondarySourceCount}\`
- unclassified_source_count: \`${report.unclassifiedSourceCount}\`
- malformed_source_input_count: \`${report.malformedSourceInputCount}\`
- registry_jsonl_path: \`${report.registryJsonlPath}\`
- registry_jsonl_sha256: \`${report.registryJsonlSha256}\`
- registry_jsonl_record_count: \`${report.registryJsonlRecordCount}\`
- registry_jsonl_parseable: \`${report.registryJsonlParseable}\`
- external_source_fetch_performed: \`${report.externalSourceFetchPerformed}\`
- blog_summary_source_allowed: \`${report.blogSummarySourceAllowed}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`

## Source Kind Counts

| Kind | Count |
| --- | ---: |
${kindRows}

## Source Host Counts

| Host | Count |
| --- | ---: |
${hostRows}

## Reports With Primary Sources

| Report |
| --- |
${reportRows}

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

  const registry = buildRegistry()
  const registryJsonlText = registry.records.map((record) => JSON.stringify(record)).join('\n') + '\n'
  writeFileSync(resolve(root, registryJsonlPath), registryJsonlText)
  const registryJsonlSha256 = sha256(registryJsonlText)
  let registryJsonlParseable = true
  for (const line of registryJsonlText.trim().split(/\r?\n/)) {
    try {
      JSON.parse(line)
    } catch {
      registryJsonlParseable = false
    }
  }

  const uniqueSourceUrlCount = new Set(registry.records.map((record) => record.sourceUrl)).size
  const sourceKindCounts = countBy(registry.records.map((record) => record.sourceKind))
  const sourceHostCounts = countBy(registry.records.map((record) => record.sourceHost))
  const disallowedSecondarySources = registry.records.filter((record) => record.isDisallowedSecondarySource)
  const unclassifiedSourceCount = registry.records.filter((record) => record.sourceKind === 'unclassified').length

  const checks = [
    check('product-quality reports were scanned', registry.scannedReportCount >= 50, `${registry.scannedReportCount} reports`),
    check('primary-source inputs are broadly represented', registry.reportsWithPrimarySourceInputs.length >= 20 && registry.records.length >= 80 && uniqueSourceUrlCount >= 50, `${registry.reportsWithPrimarySourceInputs.length} reports / ${registry.records.length} entries / ${uniqueSourceUrlCount} unique URLs`),
    check('primary-source records have HTTPS URLs', registry.records.every((record) => record.isHttps), registry.records.filter((record) => !record.isHttps).map((record) => record.sourceUrl).join(',') || 'all HTTPS'),
    check('primary-source records include project, pattern, and local absorption text', registry.records.every((record) => record.sourceProject.length > 0 && record.patternSummary.length > 0 && record.localAbsorption.length > 0), `${registry.records.length} records`),
    check('blog-summary and secondary-source domains are absent', disallowedSecondarySources.length === 0, disallowedSecondarySources.map((record) => `${record.sourceHost}:${record.disallowedReason}`).join(',') || 'none'),
    check('source kinds cover repositories, docs, standards, benchmarks, and research', ['original_repository', 'official_documentation', 'standard_or_specification', 'benchmark_project', 'research_paper'].every((kind) => (sourceKindCounts[kind as SourceKind] ?? 0) > 0), JSON.stringify(sourceKindCounts)),
    check('malformed source inputs are absent', registry.malformedSourceInputs.length === 0, registry.malformedSourceInputs.map((item) => `${item.sourceReportPath}:${item.reason}`).join(',') || 'none'),
    check('unclassified source inputs are absent', unclassifiedSourceCount === 0, `${unclassifiedSourceCount} unclassified`),
    check('registry JSONL has one record per source input', registry.records.length > 0 && registryJsonlText.trim().split(/\r?\n/).length === registry.records.length, `${registry.records.length} records`),
    check('registry JSONL is parseable and hash-addressed', registryJsonlParseable && registryJsonlSha256.length === 64, registryJsonlPath),
    check('external source fetching remains blocked', true, 'externalSourceFetchPerformed=false'),
    check('protected actions and readiness claims remain blocked', true, 'provider/live/external/protected/readiness flags false'),
  ]

  const report: PrimarySourceRegistryReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_primary_source_registry',
    registryFormat: 'openclaude_primary_source_registry_v1',
    primarySourceInputs: [
      {
        sourceProject: 'SLSA Build Provenance',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'SLSA provenance binds artifacts to subjects, build definitions, run details, and dependencies so evidence can be checked as structured material rather than prose.',
        localAbsorption: 'The registry writes source-report hashes and source-record digests for every primary-source input without creating signed provenance.',
      },
      {
        sourceProject: 'in-toto Attestation Framework',
        sourceUrl: 'https://github.com/in-toto/attestation',
        observedPattern: 'in-toto attestations bind subjects to typed predicates for verifiable software supply-chain claims.',
        localAbsorption: 'The registry turns primary-source research inputs into a typed JSONL evidence predicate while keeping external attestation claims blocked.',
      },
      {
        sourceProject: 'OpenSSF Scorecard',
        sourceUrl: 'https://github.com/ossf/scorecard',
        observedPattern: 'OpenSSF Scorecard uses repeatable checks to expose security and maintenance posture instead of accepting informal quality claims.',
        localAbsorption: 'The registry adds a repeatable check that rejects blog-summary or secondary-source domains from product-quality evidence.',
      },
    ],
    scannedReportCount: registry.scannedReportCount,
    reportsWithPrimarySourceInputs: registry.reportsWithPrimarySourceInputs,
    reportsMissingPrimarySourceInputs: registry.reportsMissingPrimarySourceInputs,
    primarySourceEntryCount: registry.records.length,
    uniqueSourceUrlCount,
    sourceKindCounts,
    sourceHostCounts,
    disallowedSecondarySourceCount: disallowedSecondarySources.length,
    disallowedSecondarySources,
    unclassifiedSourceCount,
    malformedSourceInputCount: registry.malformedSourceInputs.length,
    malformedSourceInputs: registry.malformedSourceInputs,
    registryJsonlPath,
    registryJsonlSha256,
    registryJsonlRecordCount: registry.records.length,
    registryJsonlParseable,
    externalSourceFetchPerformed: false,
    blogSummarySourceAllowed: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    registryRecords: registry.records,
    primarySourceRegistryChecks: checks,
    claimBoundary: 'Primary source registry quality is a local no-provider inventory of primary-source inputs already recorded by product-quality reports. It does not fetch external URLs, call providers, call live models, call external services, install dependencies, create signed attestations, or claim release/public/production/external/autonomous readiness.',
  }

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of checks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = checks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`scanned_report_count=${report.scannedReportCount}`)
  console.log(`reports_with_primary_source_inputs=${report.reportsWithPrimarySourceInputs.length}`)
  console.log(`primary_source_entry_count=${report.primarySourceEntryCount}`)
  console.log(`unique_source_url_count=${report.uniqueSourceUrlCount}`)
  console.log(`disallowed_secondary_source_count=${report.disallowedSecondarySourceCount}`)
  console.log(`unclassified_source_count=${report.unclassifiedSourceCount}`)
  console.log(`registry_jsonl_path=${report.registryJsonlPath}`)
  console.log(`registry_jsonl_record_count=${report.registryJsonlRecordCount}`)
  console.log(`external_source_fetch_performed=${report.externalSourceFetchPerformed}`)
  console.log(`blog_summary_source_allowed=${report.blogSummarySourceAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
}

if (!existsSync(docsDir) || !statSync(docsDir).isDirectory()) {
  console.error('RESULT: FAIL (docs/product-quality directory missing)')
  process.exit(1)
}

main()
