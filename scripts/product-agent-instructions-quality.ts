import { existsSync, mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

import { check, fileSha256, includesAll, readText, type Check } from './quality-report-helpers'

export type PackageJson = {
  scripts?: Record<string, string>
}

export type AgentInstructionsQualityReport = {
  generatedAt: string
  mode: 'local_no_provider_agent_instructions_quality'
  sourceAgentInstructionsPath: string
  sourceAgentInstructionsSha256: string
  sourcePackageJsonPath: string
  sourcePackageJsonSha256: string
  sourceWorkflowPaths: string[]
  sourceWorkflowSha256: Record<string, string>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  purposeSectionPresent: boolean
  setupVerificationCommandsPresent: string[]
  repositoryStructureSectionsPresent: string[]
  workflowEvidencePresent: boolean
  agentStackBoundariesPresent: string[]
  primarySourceRulePresent: boolean
  verificationStandardPresent: boolean
  protectedBoundaryLanguagePresent: boolean
  publicInstructionLineCount: number
  publicInstructionMaxLines: number
  privateMemoryDumpPresent: boolean
  stalePublicModelLockPresent: boolean
  localPathLeakPresent: boolean
  claimBoundary: string
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  instructionQualityChecks: Check[]
}

const agentInstructionsPath = 'AGENTS.md'
const packageJsonPath = 'package.json'
const workflowPaths = [
  '.github/workflows/pr-checks.yml',
  '.github/workflows/codeql.yml',
  '.github/dependabot.yml',
]

function privateLocalPathNeedles(): string[] {
  return [
    ['C:', 'Users'].join('\\'),
    ['C:', 'Users'].join('/'),
    ['/Users', '/'].join(''),
  ]
}

export type AgentInstructionsQualityInput = {
  agentInstructions: string
  packageJson: PackageJson
  workflowPresence: Record<string, boolean>
  workflowSha256: Record<string, string>
  sourceAgentInstructionsSha256: string
  sourcePackageJsonSha256: string
  generatedAt?: string
}

type MarkdownHeading = {
  level: number
  title: string
  lineIndex: number
}

function markdownHeadingsOutsideFences(text: string): MarkdownHeading[] {
  const headings: MarkdownHeading[] = []
  let inFence = false
  const lines = text.split(/\r?\n/)

  for (const [lineIndex, line] of lines.entries()) {
    if (/^\s*(```|~~~)/.test(line)) {
      inFence = !inFence
      continue
    }

    if (inFence) {
      continue
    }

    const match = /^(#{1,6})\s+(.+?)\s*$/.exec(line)
    if (!match) {
      continue
    }

    headings.push({
      level: match[1].length,
      title: match[2].replace(/\s+#+\s*$/, '').trim().toLowerCase(),
      lineIndex,
    })
  }

  return headings
}

function hasHeadingPath(text: string, parentTitle: string, childTitle: string): boolean {
  const headings = markdownHeadingsOutsideFences(text)
  const parent = headings.find((heading) => heading.title === parentTitle.toLowerCase())
  if (!parent) {
    return false
  }

  return headings.some((heading) => (
    heading.lineIndex > parent.lineIndex &&
    heading.level > parent.level &&
    heading.title === childTitle.toLowerCase()
  ))
}

function sectionText(text: string, title: string): string | null {
  const headings = markdownHeadingsOutsideFences(text)
  const target = headings.find((heading) => heading.title === title.toLowerCase())
  if (!target) {
    return null
  }

  const nextBoundary = headings.find((heading) => (
    heading.lineIndex > target.lineIndex &&
    heading.level <= target.level
  ))
  const lines = text.split(/\r?\n/)
  return lines.slice(target.lineIndex + 1, nextBoundary?.lineIndex).join('\n')
}

export function analyzeAgentInstructionsQuality(input: AgentInstructionsQualityInput): AgentInstructionsQualityReport {
  const {
    agentInstructions,
    packageJson,
    workflowPresence,
    workflowSha256,
    sourceAgentInstructionsSha256,
    sourcePackageJsonSha256,
    generatedAt = new Date().toISOString(),
  } = input
  const setupVerificationCommandsPresent = includesAll(agentInstructions, [
    'bun run build',
    'bun run typecheck',
    'bun run product:quality',
    'bun run verify:privacy',
  ])
  const repositoryStructureSectionsPresent = includesAll(agentInstructions, [
    'src/',
    'scripts/',
    'docs/',
    'reports/',
    'packages/openclaude-vscode/',
    '.github/',
  ])
  const agentStackBoundariesPresent = includesAll(agentInstructions, [
    'GStack',
    'GSD',
    'Superpowers',
  ])
  const publicInstructionLineCount = agentInstructions.split(/\r?\n/).length
  const privateMemoryDumpPresent = /OpenClaude Orchestrator Memory|User's intent|Diagnostic finding:/.test(agentInstructions)
  const stalePublicModelLockPresent = /\b(gpt-5\.1|sonnet 4\.5|Opus 4\.7)\b/i.test(agentInstructions)
  const localPathLeakPresent = privateLocalPathNeedles().some((needle) => agentInstructions.includes(needle))

  const productQualityScript = packageJson.scripts?.['product:quality'] ?? ''
  const verificationSection = sectionText(agentInstructions, 'Verification Standard') ?? ''
  const report: AgentInstructionsQualityReport = {
    generatedAt,
    mode: 'local_no_provider_agent_instructions_quality',
    sourceAgentInstructionsPath: agentInstructionsPath,
    sourceAgentInstructionsSha256,
    sourcePackageJsonPath: packageJsonPath,
    sourcePackageJsonSha256,
    sourceWorkflowPaths: workflowPaths,
    sourceWorkflowSha256: workflowSha256,
    primarySourceInputs: [
      {
        sourceProject: 'AGENTS.md open format',
        sourceUrl: 'https://agents.md/',
        observedPattern: 'Repository agent instructions should act as a concise README for agents with setup, tests, and project-specific guidance.',
        localAbsorption: 'AGENTS.md is kept concise and checked for public-safe repository orientation instead of private session memory.',
      },
      {
        sourceProject: 'OpenAI Codex AGENTS.md guidance',
        sourceUrl: 'https://developers.openai.com/codex/guides/agents-md',
        observedPattern: 'Codex uses layered AGENTS.md instructions before work starts, so repository guidance needs predictable scope and precedence.',
        localAbsorption: 'This report verifies root AGENTS.md scope, setup commands, verification boundaries, and public hygiene as a local quality gate.',
      },
    ],
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    purposeSectionPresent: hasHeadingPath(agentInstructions, 'Repository Orientation', 'Repository Purpose'),
    setupVerificationCommandsPresent,
    repositoryStructureSectionsPresent,
    workflowEvidencePresent: workflowPaths.every((path) => workflowPresence[path]) && productQualityScript.includes('product:agent-instructions-quality'),
    agentStackBoundariesPresent,
    primarySourceRulePresent: /primary sources/i.test(agentInstructions) && /blogs only as pointers/i.test(agentInstructions),
    verificationStandardPresent: /file presence/i.test(verificationSection) && /Verify by running/i.test(verificationSection),
    protectedBoundaryLanguagePresent: /protected/i.test(agentInstructions) && /readiness claim/i.test(agentInstructions),
    publicInstructionLineCount,
    publicInstructionMaxLines: 110,
    privateMemoryDumpPresent,
    stalePublicModelLockPresent,
    localPathLeakPresent,
    claimBoundary: 'Agent instruction quality evidence only; this does not authorize release, production, public, external-validation, or autonomous-reliability claims.',
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    instructionQualityChecks: [],
  }

  report.instructionQualityChecks = [
    check('AGENTS.md imported', report.sourceAgentInstructionsSha256.length === 64, report.sourceAgentInstructionsPath),
    check('package.json imported', report.sourcePackageJsonSha256.length === 64, report.sourcePackageJsonPath),
    check('primary-source inputs are official project sources', report.primarySourceInputs.every((source) => source.sourceUrl.startsWith('https://agents.md/') || source.sourceUrl.startsWith('https://developers.openai.com/')), report.primarySourceInputs.map((source) => source.sourceUrl).join(',')),
    check('repository purpose is explicit', report.purposeSectionPresent, 'Repository Orientation / Repository Purpose'),
    check('setup and verification commands are explicit', report.setupVerificationCommandsPresent.length === 4, report.setupVerificationCommandsPresent.join(',')),
    check('repository structure is explicit', report.repositoryStructureSectionsPresent.length === 6, report.repositoryStructureSectionsPresent.join(',')),
    check('workflow evidence is wired', report.workflowEvidencePresent, workflowPaths.join(',')),
    check('agent-stack boundaries remain explicit', report.agentStackBoundariesPresent.length === 3, report.agentStackBoundariesPresent.join(',')),
    check('primary-source research rule remains explicit', report.primarySourceRulePresent, 'primary sources / blogs only as pointers'),
    check('verification standard remains explicit', report.verificationStandardPresent, 'verification by command, not file presence'),
    check('protected boundary language remains explicit', report.protectedBoundaryLanguagePresent, 'protected boundary / readiness claim'),
    check('AGENTS.md stays concise for public readers', report.publicInstructionLineCount <= report.publicInstructionMaxLines, `${report.publicInstructionLineCount}/${report.publicInstructionMaxLines} lines`),
    check('AGENTS.md excludes private memory dumps', report.privateMemoryDumpPresent === false, `present=${report.privateMemoryDumpPresent}`),
    check('AGENTS.md excludes stale public model-lock lines', report.stalePublicModelLockPresent === false, `present=${report.stalePublicModelLockPresent}`),
    check('AGENTS.md excludes local user paths', report.localPathLeakPresent === false, `present=${report.localPathLeakPresent}`),
    check('provider live external calls remain absent', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0, 'all call arrays empty'),
    check('protected actions remain absent', report.protectedActionsExecuted.length === 0, 'zero'),
    check('readiness and reliability claims remain blocked', report.releaseReadinessClaimAllowed === false && report.productionReadinessClaimAllowed === false && report.publicReadinessClaimAllowed === false && report.externalValidationClaimAllowed === false && report.autonomousReliabilityClaimAllowed === false, 'all false'),
  ]

  return report
}

function writeMarkdown(report: AgentInstructionsQualityReport, cwd = process.cwd()): void {
  const checkRows = report.instructionQualityChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const workflowRows = report.sourceWorkflowPaths
    .map((path) => `| \`${path}\` | \`${report.sourceWorkflowSha256[path] ?? 'missing'}\` |`)
    .join('\n')

  const markdown = `# Agent Instructions Quality Report

Generated by: \`bun run product:agent-instructions-quality\`

## Claim Boundary

- This is a local no-provider quality report for repository agent instructions.
- It uses primary-source guidance from the AGENTS.md open format and OpenAI Codex AGENTS.md documentation as a local product-quality pattern.
- It does not call providers, live models, or external services.
- It does not install dependencies, publish, deploy, launch, modify production systems, or claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- source_agent_instructions: \`${report.sourceAgentInstructionsPath}\`
- purpose_section_present: \`${report.purposeSectionPresent}\`
- setup_verification_commands_present: \`${report.setupVerificationCommandsPresent.join(',')}\`
- repository_structure_sections_present: \`${report.repositoryStructureSectionsPresent.join(',')}\`
- workflow_evidence_present: \`${report.workflowEvidencePresent}\`
- agent_stack_boundaries_present: \`${report.agentStackBoundariesPresent.join(',')}\`
- primary_source_rule_present: \`${report.primarySourceRulePresent}\`
- verification_standard_present: \`${report.verificationStandardPresent}\`
- protected_boundary_language_present: \`${report.protectedBoundaryLanguagePresent}\`
- public_instruction_line_count: \`${report.publicInstructionLineCount}\`
- public_instruction_max_lines: \`${report.publicInstructionMaxLines}\`
- private_memory_dump_present: \`${report.privateMemoryDumpPresent}\`
- stale_public_model_lock_present: \`${report.stalePublicModelLockPresent}\`
- local_path_leak_present: \`${report.localPathLeakPresent}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`
- release_readiness_claim_allowed: \`${report.releaseReadinessClaimAllowed}\`
- production_readiness_claim_allowed: \`${report.productionReadinessClaimAllowed}\`
- public_readiness_claim_allowed: \`${report.publicReadinessClaimAllowed}\`
- external_validation_claim_allowed: \`${report.externalValidationClaimAllowed}\`
- autonomous_reliability_claim_allowed: \`${report.autonomousReliabilityClaimAllowed}\`

## Primary Sources

| Source | URL | Local Absorption |
| --- | --- | --- |
${sourceRows}

## Workflow Evidence Inputs

| Path | SHA-256 |
| --- | --- |
${workflowRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(cwd, 'docs/product-quality/agent-instructions-quality-report.md'), markdown)
}

function runAgentInstructionsQuality(options: { checkOnly?: boolean, cwd?: string } = {}): AgentInstructionsQualityReport {
  const { checkOnly = false, cwd = process.cwd() } = options
  const docsDir = resolve(cwd, 'docs/product-quality')

  const agentInstructions = readText(agentInstructionsPath, cwd)
  const packageJson = JSON.parse(readText(packageJsonPath, cwd)) as PackageJson
  const workflowSha256: Record<string, string> = {}
  const workflowPresence: Record<string, boolean> = {}
  for (const path of workflowPaths) {
    workflowPresence[path] = existsSync(resolve(cwd, path))
    if (workflowPresence[path]) {
      workflowSha256[path] = fileSha256(path, cwd)
    }
  }

  const report = analyzeAgentInstructionsQuality({
    agentInstructions,
    packageJson,
    workflowPresence,
    workflowSha256,
    sourceAgentInstructionsSha256: fileSha256(agentInstructionsPath, cwd),
    sourcePackageJsonSha256: fileSha256(packageJsonPath, cwd),
  })

  if (!checkOnly) {
    mkdirSync(docsDir, { recursive: true })
    writeFileSync(resolve(docsDir, 'agent-instructions-quality-report.json'), `${JSON.stringify(report, null, 2)}\n`)
    writeMarkdown(report, cwd)
  }

  for (const item of report.instructionQualityChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.instructionQualityChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`setup_verification_command_count=${report.setupVerificationCommandsPresent.length}`)
  console.log(`repository_structure_section_count=${report.repositoryStructureSectionsPresent.length}`)
  console.log(`workflow_evidence_present=${report.workflowEvidencePresent}`)
  console.log(`agent_stack_boundary_count=${report.agentStackBoundariesPresent.length}`)

  return report
}

function main(): void {
  runAgentInstructionsQuality({ checkOnly: process.argv.includes('--check') })
}

if (import.meta.main) {
  main()
}
