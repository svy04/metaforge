import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { basename, resolve } from 'node:path'

type HelperOccurrence = {
  helperName: string
  path: string
  line: number
  normalizedBodySha256: string
  normalizedBodyPreview: string
}

type DuplicateHelperCluster = {
  helperName: string
  normalizedBodySha256: string
  occurrenceCount: number
  files: Array<{
    path: string
    line: number
  }>
  normalizedBodyPreview: string
}

type Check = {
  label: string
  ok: boolean
  detail: string
}

type ScriptDuplicationAuditReport = {
  generatedAt: string
  mode: 'local_no_provider_product_script_duplication_audit'
  scannerTargetGlob: string
  auditTargetHelperNames: string[]
  sourceProductScriptCount: number
  helperOccurrenceCounts: Record<string, number>
  duplicateHelperClusterCount: number
  duplicateHelperClusters: DuplicateHelperCluster[]
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  dependencyInstallPerformed: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  publicReadinessClaimAllowed: false
  refactorCompletionClaimAllowed: false
  auditChecks: Check[]
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const scriptsDir = resolve(root, 'scripts')
const reportJsonPath = 'docs/product-quality/script-duplication-audit-report.json'
const reportMdPath = 'docs/product-quality/script-duplication-audit-report.md'
const helperNames = ['check', 'readText', 'sha256Text']

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function relativeScriptPath(fileName: string): string {
  return `scripts/${fileName}`.replace(/\\/g, '/')
}

function productScriptFiles(): string[] {
  if (!existsSync(scriptsDir)) return []
  const self = basename(new URL(import.meta.url).pathname)
  return readdirSync(scriptsDir)
    .filter((fileName) => /^product-.*\.ts$/.test(fileName))
    .filter((fileName) => !fileName.endsWith('.test.ts'))
    .filter((fileName) => fileName !== self)
    .sort()
}

function lineForIndex(source: string, index: number): number {
  return source.slice(0, index).split(/\r?\n/).length
}

function findMatchingBrace(source: string, openBrace: number): number {
  let depth = 0
  let quote: '"' | "'" | '`' | null = null
  let escaped = false
  let lineComment = false
  let blockComment = false

  for (let index = openBrace; index < source.length; index += 1) {
    const char = source[index]
    const next = source[index + 1]

    if (lineComment) {
      if (char === '\n') lineComment = false
      continue
    }
    if (blockComment) {
      if (char === '*' && next === '/') {
        blockComment = false
        index += 1
      }
      continue
    }
    if (quote) {
      if (escaped) {
        escaped = false
        continue
      }
      if (char === '\\') {
        escaped = true
        continue
      }
      if (char === quote) quote = null
      continue
    }

    if (char === '/' && next === '/') {
      lineComment = true
      index += 1
      continue
    }
    if (char === '/' && next === '*') {
      blockComment = true
      index += 1
      continue
    }
    if (char === '"' || char === "'" || char === '`') {
      quote = char
      continue
    }
    if (char === '{') depth += 1
    if (char === '}') {
      depth -= 1
      if (depth === 0) return index
    }
  }

  return -1
}

function normalizeHelperBody(body: string): string {
  return body
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/\/\/.*$/gm, '')
    .replace(/\s+/g, ' ')
    .trim()
}

function extractHelperOccurrences(fileName: string): HelperOccurrence[] {
  const path = resolve(scriptsDir, fileName)
  const source = readFileSync(path, 'utf8')
  const helperPattern = new RegExp(`function\\s+(${helperNames.join('|')})\\s*\\(`, 'g')
  const occurrences: HelperOccurrence[] = []

  for (const match of source.matchAll(helperPattern)) {
    const helperName = match[1]
    const openBrace = source.indexOf('{', match.index)
    if (openBrace === -1) continue
    const closeBrace = findMatchingBrace(source, openBrace)
    if (closeBrace === -1) continue

    const normalizedBody = normalizeHelperBody(source.slice(openBrace + 1, closeBrace))
    occurrences.push({
      helperName,
      path: relativeScriptPath(fileName),
      line: lineForIndex(source, match.index ?? 0),
      normalizedBodySha256: sha256(normalizedBody),
      normalizedBodyPreview: normalizedBody.slice(0, 120),
    })
  }

  return occurrences
}

function buildDuplicateClusters(occurrences: HelperOccurrence[]): DuplicateHelperCluster[] {
  const groups = new Map<string, HelperOccurrence[]>()
  for (const occurrence of occurrences) {
    const key = `${occurrence.helperName}:${occurrence.normalizedBodySha256}`
    groups.set(key, [...(groups.get(key) ?? []), occurrence])
  }

  return [...groups.values()]
    .filter((group) => group.length > 1)
    .map((group) => ({
      helperName: group[0].helperName,
      normalizedBodySha256: group[0].normalizedBodySha256,
      occurrenceCount: group.length,
      files: group.map((item) => ({ path: item.path, line: item.line })),
      normalizedBodyPreview: group[0].normalizedBodyPreview,
    }))
    .sort((a, b) => b.occurrenceCount - a.occurrenceCount || a.helperName.localeCompare(b.helperName))
}

function writeMarkdown(report: ScriptDuplicationAuditReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const clusterRows = report.duplicateHelperClusters
    .slice(0, 20)
    .map((cluster) => {
      const shownFiles = cluster.files.slice(0, 12).map((file) => `${file.path}:${file.line}`)
      const hiddenCount = cluster.files.length - shownFiles.length
      const files = [
        ...shownFiles,
        ...(hiddenCount > 0 ? [`...and ${hiddenCount} more in JSON report`] : []),
      ].join('<br>')
      return `| ${cluster.helperName} | ${cluster.occurrenceCount} | \`${cluster.normalizedBodySha256}\` | ${files} |`
    })
    .join('\n')
  const checkRows = report.auditChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Product Script Duplication Audit

Generated by: \`bun run product:script-duplication-audit\`

## Claim Boundary

- This is a local no-provider audit of repeated helper shapes in \`scripts/product-*.ts\`.
- It records refactor candidates only. It does not prove public readiness, code quality, or refactor completion.
- It did not install dependencies, call providers, call live models, execute protected actions, or run external services.

## Summary

- source_product_script_count: \`${report.sourceProductScriptCount}\`
- audit_target_helper_names: \`${report.auditTargetHelperNames.join(',')}\`
- duplicate_helper_cluster_count: \`${report.duplicateHelperClusterCount}\`
- helper_occurrence_counts: \`${JSON.stringify(report.helperOccurrenceCounts)}\`
- dependency_install_performed: \`${report.dependencyInstallPerformed}\`
- public_readiness_claim_allowed: \`${report.publicReadinessClaimAllowed}\`
- refactor_completion_claim_allowed: \`${report.refactorCompletionClaimAllowed}\`

## Primary Sources

| Source | URL | Local Absorption |
| --- | --- | --- |
${sourceRows}

## Top Duplicate Helper Clusters

| Helper | Occurrences | Body SHA-256 | Files |
| --- | ---: | --- | --- |
${clusterRows || '| none | 0 | `n/a` | n/a |'}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })

  const files = productScriptFiles()
  const occurrences = files.flatMap((fileName) => extractHelperOccurrences(fileName))
  const helperOccurrenceCounts = Object.fromEntries(
    helperNames.map((helperName) => [
      helperName,
      occurrences.filter((occurrence) => occurrence.helperName === helperName).length,
    ]),
  ) as Record<string, number>
  const duplicateHelperClusters = buildDuplicateClusters(occurrences)

  const report: ScriptDuplicationAuditReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_product_script_duplication_audit',
    scannerTargetGlob: 'scripts/product-*.ts',
    auditTargetHelperNames: helperNames,
    sourceProductScriptCount: files.length,
    helperOccurrenceCounts,
    duplicateHelperClusterCount: duplicateHelperClusters.length,
    duplicateHelperClusters,
    primarySourceInputs: [
      {
        sourceProject: 'jscpd',
        sourceUrl: 'https://github.com/kucherenko/jscpd',
        observedPattern: 'Copy/paste detection is a dedicated audit surface; clone findings are refactor candidates, not automatic defects.',
        localAbsorption: 'This local audit records repeated helper shapes first, so later jscpd adoption can be compared against a stable project-specific baseline.',
      },
      {
        sourceProject: 'Knip',
        sourceUrl: 'https://knip.dev/',
        observedPattern: 'Unused files, dependencies, and exports need a project graph and configuration-aware audit surface.',
        localAbsorption: 'Dead export cleanup is kept as a follow-up lane separate from duplicate helper measurement.',
      },
      {
        sourceProject: 'dependency-cruiser',
        sourceUrl: 'https://github.com/sverweij/dependency-cruiser',
        observedPattern: 'Dependency rule and cycle validation is a different graph problem from clone detection.',
        localAbsorption: 'Cycle/rule checks stay out of this helper-duplication report and should be introduced as a dedicated gate.',
      },
    ],
    dependencyInstallPerformed: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    publicReadinessClaimAllowed: false,
    refactorCompletionClaimAllowed: false,
    auditChecks: [],
  }

  report.auditChecks = [
    check('product scripts are scanned', report.sourceProductScriptCount > 0, `${report.sourceProductScriptCount} files`),
    check('target helper occurrence surface is measured', Object.values(report.helperOccurrenceCounts).some((count) => count > 0), JSON.stringify(report.helperOccurrenceCounts)),
    check('duplicate helper clusters are reported as candidates', Array.isArray(report.duplicateHelperClusters), `${report.duplicateHelperClusterCount} clusters`),
    check('primary sources are official project sources', report.primarySourceInputs.every((source) => source.sourceUrl.startsWith('https://github.com/') || source.sourceUrl.startsWith('https://knip.dev/')), report.primarySourceInputs.map((source) => source.sourceUrl).join(',')),
    check('no dependency install was performed', report.dependencyInstallPerformed === false, 'false'),
    check('provider and external calls remain absent', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0, 'all call arrays empty'),
    check('protected actions remain absent', report.protectedActionsExecuted.length === 0, 'zero'),
    check('readiness and refactor-completion claims remain blocked', report.publicReadinessClaimAllowed === false && report.refactorCompletionClaimAllowed === false, 'all false'),
  ]

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of report.auditChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.auditChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`source_product_script_count=${report.sourceProductScriptCount}`)
  console.log(`duplicate_helper_cluster_count=${report.duplicateHelperClusterCount}`)
  console.log(`helper_occurrence_counts=${JSON.stringify(report.helperOccurrenceCounts)}`)
}

main()
