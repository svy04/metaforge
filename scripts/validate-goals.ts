import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { parse } from 'yaml'

type ValidationResult = {
  path: string
  goalId: string | null
  ok: boolean
  errors: string[]
}

type ValidationReport = {
  generatedAt: string
  mode: 'local_no_provider_goal_validation'
  goalFileCount: number
  validGoalCount: number
  invalidGoalCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  validationResults: ValidationResult[]
  claimBoundary: string
}

const root = process.cwd()
const goalDir = 'docs/goals'
const reportDir = 'docs/product-quality'
const reportPath = 'docs/product-quality/goal-validation-report.json'

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function hasNonEmptyString(value: unknown): boolean {
  return typeof value === 'string' && value.trim().length > 0
}

function hasNonEmptyArray(value: unknown): boolean {
  return Array.isArray(value) && value.length > 0
}

function getPath(value: unknown, path: string): unknown {
  return path.split('.').reduce<unknown>((current, part) => {
    if (!isRecord(current)) return undefined
    return current[part]
  }, value)
}

function extractYamlBlock(markdown: string): string | null {
  const match = markdown.match(/```ya?ml\s*\r?\n([\s\S]*?)\r?\n```/i)
  return match?.[1] ?? null
}

function requireString(goal: unknown, path: string, errors: string[]): void {
  if (!hasNonEmptyString(getPath(goal, path))) {
    errors.push(`${path} must be a non-empty string`)
  }
}

function requireArray(goal: unknown, path: string, errors: string[]): void {
  if (!hasNonEmptyArray(getPath(goal, path))) {
    errors.push(`${path} must contain at least one item`)
  }
}

function requireArrayValue(goal: unknown, path: string, errors: string[]): void {
  if (!Array.isArray(getPath(goal, path))) {
    errors.push(`${path} must be an array`)
  }
}

function requireBoolean(goal: unknown, path: string, errors: string[]): void {
  if (typeof getPath(goal, path) !== 'boolean') {
    errors.push(`${path} must be boolean`)
  }
}

function localPathExists(path: string): boolean {
  return existsSync(resolve(root, path.split('#')[0] ?? path))
}

function requireLocalPathArray(goal: unknown, path: string, errors: string[]): void {
  const value = getPath(goal, path)
  if (!Array.isArray(value)) return
  value.forEach((entry, index) => {
    if (!hasNonEmptyString(entry) || !localPathExists(String(entry))) {
      errors.push(`${path}.${index} must point to an existing local source`)
    }
  })
}

export function validateGoalDocument(path: string, markdown: string): ValidationResult {
  const yamlBlock = extractYamlBlock(markdown)
  if (!yamlBlock) {
    return {
      path,
      goalId: null,
      ok: false,
      errors: ['goal document must contain a yaml fenced block'],
    }
  }

  let goal: unknown
  try {
    goal = parse(yamlBlock)
  } catch (error) {
    return {
      path,
      goalId: null,
      ok: false,
      errors: [`goal yaml must parse: ${error instanceof Error ? error.message : String(error)}`],
    }
  }

  const errors: string[] = []
  const goalId = hasNonEmptyString(getPath(goal, 'id')) ? String(getPath(goal, 'id')) : null
  const fileName = path.split('/').pop() ?? path
  const fileIdMatch = fileName.match(/^(CG-\d+)-/i)
  const fileGoalId = fileIdMatch?.[1]?.toUpperCase()
  if (fileGoalId && goalId && goalId.toUpperCase() !== fileGoalId) {
    errors.push(`id must match filename prefix ${fileGoalId}`)
  }

  for (const field of [
    'id',
    'level',
    'title',
    'parent',
    'status',
    'owner',
    'createdAt',
    'updatedAt',
    'objective.summary',
    'objective.whyNow',
    'objective.userValue',
    'scope.targetDomain',
    'rollbackStrategy.type',
    'reflection.result',
    'governedCode.category',
    'governedCode.claimLevel',
  ]) {
    requireString(goal, field, errors)
  }

  for (const field of [
    'scope.in',
    'scope.out',
    'scope.targetFiles',
    'context.localSourcesRead',
    'context.externalPrimarySources',
    'context.relatedDecisions',
    'researchRequirements.sourceLadder',
    'researchRequirements.rejectedSources',
    'researchRequirements.openQuestions',
    'successCriteria',
    'validationCommands',
    'checkpoints',
    'pauseConditions',
    'rollbackStrategy.steps',
    'rollbackStrategy.validationAfterRollback',
    'evidence.artifacts',
    'evidence.testResults',
    'reflection.lessons',
    'reflection.nextGoalCandidates',
    'governedCode.claimBoundary.allowed',
    'governedCode.claimBoundary.forbidden',
    'governedCode.authoritySources',
    'governedCode.metaRecords.decisionLedgerEntries',
    'governedCode.metaRecords.rawSources',
  ]) {
    requireArray(goal, field, errors)
  }
  requireArrayValue(goal, 'governedCode.metaRecords.wikiOrMemoryUpdates', errors)

  for (const field of [
    'researchRequirements.required',
    'governedCode.mfhGates.sourceReconcilerRequired',
    'governedCode.mfhGates.closureRealityRequired',
    'governedCode.mfhGates.dirtyStateAttributionRequired',
    'governedCode.mfhGates.humanAdjudicationRequired',
  ]) {
    requireBoolean(goal, field, errors)
  }

  const agentAssignments = getPath(goal, 'agentAssignments')
  for (const role of ['orchestrator', 'researcher', 'architect', 'implementer', 'eval', 'security', 'memoryLibrarian']) {
    if (!isRecord(agentAssignments) || !hasNonEmptyString(agentAssignments[role])) {
      errors.push(`agentAssignments.${role} must be a non-empty string`)
    }
  }

  const commands = getPath(goal, 'validationCommands')
  if (Array.isArray(commands)) {
    commands.forEach((command, index) => {
      if (!isRecord(command) || !hasNonEmptyString(command.command)) {
        errors.push(`validationCommands.${index}.command must be a non-empty string`)
      }
      if (!isRecord(command) || !hasNonEmptyString(command.expected)) {
        errors.push(`validationCommands.${index}.expected must be a non-empty string`)
      }
      if (!isRecord(command) || typeof command.required !== 'boolean') {
        errors.push(`validationCommands.${index}.required must be boolean`)
      }
    })
  }

  const successCriteria = getPath(goal, 'successCriteria')
  if (Array.isArray(successCriteria)) {
    successCriteria.forEach((criterion, index) => {
      for (const field of ['id', 'statement', 'validation']) {
        if (!isRecord(criterion) || !hasNonEmptyString(criterion[field])) {
          errors.push(`successCriteria.${index}.${field} must be a non-empty string`)
        }
      }
    })
  }

  const checkpoints = getPath(goal, 'checkpoints')
  if (Array.isArray(checkpoints)) {
    checkpoints.forEach((checkpoint, index) => {
      for (const field of ['id', 'name', 'doneWhen']) {
        if (!isRecord(checkpoint) || !hasNonEmptyString(checkpoint[field])) {
          errors.push(`checkpoints.${index}.${field} must be a non-empty string`)
        }
      }
    })
  }

  const externalSources = getPath(goal, 'context.externalPrimarySources')
  if (Array.isArray(externalSources)) {
    externalSources.forEach((source, index) => {
      for (const field of ['title', 'url', 'reason']) {
        if (!isRecord(source) || !hasNonEmptyString(source[field])) {
          errors.push(`context.externalPrimarySources.${index}.${field} must be a non-empty string`)
        }
      }
      if (isRecord(source) && hasNonEmptyString(source.url) && !/^https?:\/\//.test(String(source.url))) {
        errors.push(`context.externalPrimarySources.${index}.url must be an http(s) URL`)
      }
    })
  }

  requireLocalPathArray(goal, 'context.localSourcesRead', errors)
  requireLocalPathArray(goal, 'governedCode.authoritySources', errors)
  requireLocalPathArray(goal, 'governedCode.metaRecords.rawSources', errors)
  requireLocalPathArray(goal, 'governedCode.metaRecords.decisionLedgerEntries', errors)

  return {
    path,
    goalId,
    ok: errors.length === 0,
    errors,
  }
}

function listGoalFiles(): string[] {
  const absoluteGoalDir = resolve(root, goalDir)
  if (!existsSync(absoluteGoalDir)) return []
  return readdirSync(absoluteGoalDir)
    .filter((name) => /^CG-\d+-.*\.md$/i.test(name))
    .sort((left, right) => left.localeCompare(right))
    .map((name) => `${goalDir}/${name}`)
}

function buildReport(goalFiles = listGoalFiles()): ValidationReport {
  const validationResults = goalFiles.map((path) =>
    validateGoalDocument(path, readFileSync(resolve(root, path), 'utf8')),
  )
  return {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_goal_validation',
    goalFileCount: goalFiles.length,
    validGoalCount: validationResults.filter((result) => result.ok).length,
    invalidGoalCount: validationResults.filter((result) => !result.ok).length,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    validationResults,
    claimBoundary: 'Goal validation is local docs governance evidence only. It does not prove production readiness, release readiness, public readiness, external validation, or autonomous reliability.',
  }
}

function main(): void {
  const report = buildReport()
  mkdirSync(resolve(root, reportDir), { recursive: true })
  writeFileSync(resolve(root, reportPath), `${JSON.stringify(report, null, 2)}\n`)

  for (const result of report.validationResults) {
    const prefix = result.ok ? 'PASS' : 'FAIL'
    console.log(`${prefix}: ${result.path}${result.goalId ? ` (${result.goalId})` : ''}`)
    for (const error of result.errors) {
      console.log(`  - ${error}`)
    }
  }

  console.log('')
  console.log(`RESULT: ${report.invalidGoalCount === 0 && report.goalFileCount > 0 ? 'PASS' : 'FAIL'}`)
  console.log(`goal_file_count=${report.goalFileCount}`)
  console.log(`valid_goal_count=${report.validGoalCount}`)
  console.log(`invalid_goal_count=${report.invalidGoalCount}`)
  console.log('provider_calls_performed=0')
  console.log('live_model_calls_performed=0')
  console.log('external_calls_performed=0')
  console.log('protected_actions_executed=0')

  if (report.goalFileCount === 0 || report.invalidGoalCount > 0) {
    process.exit(1)
  }
}

if (import.meta.main) {
  main()
}
