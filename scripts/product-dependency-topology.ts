import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { runNoProviderPackageCommand, type PackageCommandRun } from './quality-command-helpers'
import { check, type Check } from './quality-report-helpers'

type DependencyCruiserDependency = {
  circular?: boolean
  couldNotResolve?: boolean
  module?: string
  resolved?: string
}

type DependencyCruiserModule = {
  source: string
  dependencies?: DependencyCruiserDependency[]
}

type DependencyCruiserJson = {
  modules?: DependencyCruiserModule[]
  summary?: {
    totalCruised?: number
    totalDependenciesCruised?: number
  }
}

type DependencyCruiserKnownViolation = {
  rule?: {
    name?: string
  }
}

type TopologyCommand = {
  name: string
  command: string[]
  exitCode: number | null
  passed: boolean
  requiredSubstrings: string[]
  missingSubstrings: string[]
  stdoutPreview: string[]
  stderrPreview: string[]
}

type CommandRun = PackageCommandRun

type DependencyTopologyReport = {
  generatedAt: string
  mode: 'local_no_provider_dependency_topology_gate'
  scannerTargetRoots: string[]
  dependencyCruiserVersion: string
  topologyCommands: TopologyCommand[]
  moduleCount: number
  dependencyEdgeCount: number
  circularDependencyCount: number
  circularDependencyBaseline: number
  unresolvedDependencyCount: number
  unresolvedDependencyBaseline: number
  configuredRatchetMode: 'dependency_cruiser_known_violation_ratchet'
  dependencyCruiserConfigPath: string
  knownViolationBaselinePath: string
  configuredRatchetKnownViolationCount: number
  configuredRatchetKnownViolationRuleCounts: Record<string, number>
  configuredRatchetNewViolationCount: number
  configuredRatchetClaimAllowed: false
  sampleCircularEdges: Array<{
    source: string
    resolved: string
  }>
  sampleUnresolvedEdges: Array<{
    source: string
    module: string
  }>
  primarySourceInputs: Array<{
    sourceType: 'oss_tool' | 'patent'
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
  topologyCleanClaimAllowed: false
  refactorCompletionClaimAllowed: false
  publicReadinessClaimAllowed: false
  topologyChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportJsonPath = 'docs/product-quality/dependency-topology-report.json'
const reportMdPath = 'docs/product-quality/dependency-topology-report.md'
const dependencyCruiserConfigPath = '.dependency-cruiser.mjs'
const knownViolationBaselinePath = '.dependency-cruiser-known-violations.json'
const circularDependencyBaseline = 1737
const unresolvedDependencyBaseline = 863
const dependencyCruiserArgs = [
  'depcruise',
  '--no-config',
  '--output-type',
  'json',
  '--include-only',
  '^src|^scripts',
  '--exclude',
  '(^node_modules|\\.test\\.ts$|^scripts/_fixtures)',
  'src',
  'scripts',
]
const configuredRatchetArgs = [
  'depcruise',
  '--config',
  dependencyCruiserConfigPath,
  '--ignore-known',
  knownViolationBaselinePath,
  '--output-type',
  'err',
  '--include-only',
  '^src|^scripts',
  '--exclude',
  '(^node_modules|\\.test\\.ts$|^scripts/_fixtures)',
  'src',
  'scripts',
]

function normalize(text: string | Buffer | null | undefined): string {
  return String(text ?? '').replace(/\r\n/g, '\n')
}

function preview(text: string): string[] {
  return text
    .split('\n')
    .map((line) => line.trimEnd())
    .filter((line) => line.length > 0)
    .slice(0, 40)
}

function runCommand(name: string, command: string[], requiredSubstrings: string[]): CommandRun {
  return runNoProviderPackageCommand({
    root,
    name,
    command,
    requiredSubstrings,
    noProviderEnvName: 'OPENCLAUDE_PRODUCT_DEPENDENCY_TOPOLOGY_NO_PROVIDER',
    normalize,
    preview,
  })
}

function stripCommand(command: CommandRun): TopologyCommand {
  const { stdoutText: _stdoutText, ...reportCommand } = command
  return reportCommand
}

function parseDependencyCruiserJson(command: CommandRun): DependencyCruiserJson {
  return JSON.parse(command.stdoutText) as DependencyCruiserJson
}

function readKnownViolations(): DependencyCruiserKnownViolation[] {
  return JSON.parse(readFileSync(resolve(root, knownViolationBaselinePath), 'utf8')) as DependencyCruiserKnownViolation[]
}

function countKnownViolationRules(violations: DependencyCruiserKnownViolation[]): Record<string, number> {
  return violations.reduce<Record<string, number>>((counts, violation) => {
    const ruleName = violation.rule?.name ?? 'unknown'
    counts[ruleName] = (counts[ruleName] ?? 0) + 1
    return counts
  }, {})
}

function parseNewViolationCount(command: CommandRun): number {
  const combined = `${command.stdoutPreview.join('\n')}\n${command.stderrPreview.join('\n')}`
  if (command.exitCode === 0 && combined.includes('no dependency violations found')) {
    return 0
  }
  const match = combined.match(/(\d+)\s+(?:error|errors|dependency violation|dependency violations)/i)
  return match ? Number.parseInt(match[1], 10) : 1
}

function buildReport(): DependencyTopologyReport {
  const versionCommand = runCommand('dependency_cruiser_version', ['depcruise', '--version'], ['17.4.3'])
  const topologyCommand = runCommand('dependency_cruiser_src_scripts', dependencyCruiserArgs, ['"modules"', '"summary"'])
  const ratchetCommand = runCommand('dependency_cruiser_known_violation_ratchet', configuredRatchetArgs, ['no dependency violations found', 'known violations ignored'])
  const dependencyJson = parseDependencyCruiserJson(topologyCommand)
  const knownViolations = readKnownViolations()
  const modules = dependencyJson.modules ?? []
  const allEdges = modules.flatMap((module) => (
    (module.dependencies ?? []).map((dependency) => ({ source: module.source, dependency }))
  ))
  const circularEdges = allEdges.filter((edge) => edge.dependency.circular === true)
  const unresolvedEdges = allEdges.filter((edge) => edge.dependency.couldNotResolve === true)

  const report: DependencyTopologyReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_dependency_topology_gate',
    scannerTargetRoots: ['src', 'scripts'],
    dependencyCruiserVersion: versionCommand.stdoutPreview[0] ?? 'unknown',
    topologyCommands: [stripCommand(topologyCommand), stripCommand(ratchetCommand)],
    moduleCount: dependencyJson.summary?.totalCruised ?? modules.length,
    dependencyEdgeCount: dependencyJson.summary?.totalDependenciesCruised ?? allEdges.length,
    circularDependencyCount: circularEdges.length,
    circularDependencyBaseline,
    unresolvedDependencyCount: unresolvedEdges.length,
    unresolvedDependencyBaseline,
    configuredRatchetMode: 'dependency_cruiser_known_violation_ratchet',
    dependencyCruiserConfigPath,
    knownViolationBaselinePath,
    configuredRatchetKnownViolationCount: knownViolations.length,
    configuredRatchetKnownViolationRuleCounts: countKnownViolationRules(knownViolations),
    configuredRatchetNewViolationCount: parseNewViolationCount(ratchetCommand),
    configuredRatchetClaimAllowed: false,
    sampleCircularEdges: circularEdges.slice(0, 20).map((edge) => ({
      source: edge.source,
      resolved: edge.dependency.resolved ?? 'unknown',
    })),
    sampleUnresolvedEdges: unresolvedEdges.slice(0, 20).map((edge) => ({
      source: edge.source,
      module: edge.dependency.module ?? edge.dependency.resolved ?? 'unresolved',
    })),
    primarySourceInputs: [
      {
        sourceType: 'oss_tool',
        sourceProject: 'dependency-cruiser',
        sourceUrl: 'https://github.com/sverweij/dependency-cruiser',
        observedPattern: 'dependency-cruiser extracts dependency graphs, validates configured rules, and supports known-violation baselines through the baseline reporter plus --ignore-known.',
        localAbsorption: 'Metaforge records current src/scripts graph counts and runs a configured known-violation ratchet so new topology violations fail without claiming cleanup of the existing knots.',
      },
      {
        sourceType: 'patent',
        sourceProject: 'US7904892B2 dependency graph cycle patent',
        sourceUrl: 'https://patents.google.com/patent/US7904892B2/en',
        observedPattern: 'Dependency graph systems model directed component relationships to identify levels, cycles, and structural dependencies.',
        localAbsorption: 'OpenClaude keeps dependency topology evidence separate from clone detection and dead-export cleanup.',
      },
    ],
    dependencyInstallPerformed: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    topologyCleanClaimAllowed: false,
    refactorCompletionClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    topologyChecks: [],
    claimBoundary: 'Dependency topology evidence is a local no-provider dependency-cruiser graph baseline plus known-violation ratchet only. It does not prove clean architecture, public readiness, or refactor completion.',
  }

  report.topologyChecks = [
    check('dependency-cruiser version command passes', versionCommand.exitCode === 0 && versionCommand.passed, report.dependencyCruiserVersion),
    check('dependency-cruiser topology command passes', topologyCommand.exitCode === 0 && topologyCommand.passed, `${topologyCommand.exitCode}`),
    check('configured dependency-cruiser ratchet command passes', ratchetCommand.exitCode === 0 && ratchetCommand.passed, `${ratchetCommand.exitCode}`),
    check('modules are discovered', report.moduleCount > 0, `${report.moduleCount} modules`),
    check('dependency edges are discovered', report.dependencyEdgeCount > 0, `${report.dependencyEdgeCount} edges`),
    check('circular dependencies do not exceed baseline', report.circularDependencyCount <= report.circularDependencyBaseline, `${report.circularDependencyCount}/${report.circularDependencyBaseline}`),
    check('unresolved dependencies do not exceed baseline', report.unresolvedDependencyCount <= report.unresolvedDependencyBaseline, `${report.unresolvedDependencyCount}/${report.unresolvedDependencyBaseline}`),
    check('known dependency-cruiser violations are baselined', report.configuredRatchetKnownViolationCount > 0, `${report.configuredRatchetKnownViolationCount} known violations`),
    check('configured dependency-cruiser ratchet has no new violations', report.configuredRatchetNewViolationCount === 0 && report.configuredRatchetClaimAllowed === false, `${report.configuredRatchetNewViolationCount} new violations`),
    check('primary sources include official tool and patent sources', report.primarySourceInputs.length === 2 && report.primarySourceInputs.every((source) => source.sourceUrl.startsWith('https://github.com/') || source.sourceUrl.startsWith('https://patents.google.com/')), report.primarySourceInputs.map((source) => source.sourceProject).join(',')),
    check('provider/live/external calls remain absent', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0, 'all call arrays empty'),
    check('protected actions remain absent', report.protectedActionsExecuted.length === 0, 'zero'),
    check('topology cleanup and public readiness claims remain blocked', report.topologyCleanClaimAllowed === false && report.refactorCompletionClaimAllowed === false && report.publicReadinessClaimAllowed === false, 'all false'),
  ]

  return report
}

function writeMarkdown(report: DependencyTopologyReport): void {
  const commandRows = report.topologyCommands
    .map((command) => `| ${command.name} | \`${command.command.join(' ')}\` | \`${command.passed}\` | \`${command.exitCode ?? 'null'}\` | ${command.missingSubstrings.length === 0 ? 'none' : command.missingSubstrings.map((item) => `\`${item}\``).join('<br>')} |`)
    .join('\n')
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceType} | ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const checkRows = report.topologyChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')
  const circularRows = report.sampleCircularEdges
    .map((edge) => `| \`${edge.source}\` | \`${edge.resolved}\` |`)
    .join('\n')
  const unresolvedRows = report.sampleUnresolvedEdges
    .map((edge) => `| \`${edge.source}\` | \`${edge.module}\` |`)
    .join('\n')

  const markdown = `# Dependency Topology Report

Generated by: \`bun run product:dependency-topology\`

## Claim Boundary

- This is a local no-provider dependency graph baseline for \`src\` and \`scripts\`.
- It uses dependency-cruiser in no-config report mode.
- It records circular and unresolved dependency counts as refactor candidates and ratchet baselines.
- It does not prove clean architecture, public readiness, or refactor completion.

## Summary

- dependency_cruiser_version: \`${report.dependencyCruiserVersion}\`
- scanner_target_roots: \`${report.scannerTargetRoots.join(',')}\`
- module_count: \`${report.moduleCount}\`
- dependency_edge_count: \`${report.dependencyEdgeCount}\`
- circular_dependency_count: \`${report.circularDependencyCount}\`
- circular_dependency_baseline: \`${report.circularDependencyBaseline}\`
- unresolved_dependency_count: \`${report.unresolvedDependencyCount}\`
- unresolved_dependency_baseline: \`${report.unresolvedDependencyBaseline}\`
- topology_clean_claim_allowed: \`${report.topologyCleanClaimAllowed}\`
- refactor_completion_claim_allowed: \`${report.refactorCompletionClaimAllowed}\`
- public_readiness_claim_allowed: \`${report.publicReadinessClaimAllowed}\`

## Commands

| Command | Args | Passed | Exit | Missing Substrings |
| --- | --- | --- | ---: | --- |
${commandRows}

## Primary Sources

| Type | Source | URL | Local Absorption |
| --- | --- | --- | --- |
${sourceRows}

## Configured Ratchet

- dependency_cruiser_config_path: \`${report.dependencyCruiserConfigPath}\`
- known_violation_baseline_path: \`${report.knownViolationBaselinePath}\`
- configured_ratchet_mode: \`${report.configuredRatchetMode}\`
- configured_ratchet_known_violation_count: \`${report.configuredRatchetKnownViolationCount}\`
- configured_ratchet_known_violation_rule_counts: \`${JSON.stringify(report.configuredRatchetKnownViolationRuleCounts)}\`
- configured_ratchet_new_violation_count: \`${report.configuredRatchetNewViolationCount}\`
- configured_ratchet_claim_allowed: \`${report.configuredRatchetClaimAllowed}\`

## Sample Circular Edges

| Source | Resolved |
| --- | --- |
${circularRows || '| none | none |'}

## Sample Unresolved Edges

| Source | Module |
| --- | --- |
${unresolvedRows || '| none | none |'}

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

  for (const item of report.topologyChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.topologyChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`dependency_cruiser_version=${report.dependencyCruiserVersion}`)
  console.log(`dependency_topology_modules=${report.moduleCount}`)
  console.log(`dependency_topology_edges=${report.dependencyEdgeCount}`)
  console.log(`dependency_topology_cycles=${report.circularDependencyCount}`)
  console.log(`dependency_topology_unresolved=${report.unresolvedDependencyCount}`)
  console.log(`dependency_topology_ratchet_known_violations=${report.configuredRatchetKnownViolationCount}`)
  console.log(`dependency_topology_ratchet_new_violations=${report.configuredRatchetNewViolationCount}`)
}

main()
