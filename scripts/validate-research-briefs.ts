import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type RequiredSource = {
  id: string
  sourceProject: string
  sourceUrl?: string
  sourcePath?: string
  observedPattern: string
  localAbsorption: string
}

type SourceRow = {
  source: string
  urlOrPath: string
  sourceClass: string
  finding: string
  mapsTo: string
  boundary: string
}

type Check = {
  label: string
  ok: boolean
  detail: string
}

export type ResearchBriefValidationResult = {
  path?: string
  ok: boolean
  errors: string[]
  sourceRowCount: number
  requiredSourceCoverage: {
    present: string[]
    missing: string[]
  }
  disallowedSources: string[]
  mappedRowCount: number
  sha256?: string
}

export type ResearchBriefValidationReport = {
  generatedAt: string
  mode: 'local_no_provider_research_brief_validation'
  briefDirectory: string
  briefFilePattern: string
  briefFileCount: number
  validBriefCount: number
  invalidBriefCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  validationResults: ResearchBriefValidationResult[]
  researchBriefChecks: Check[]
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  localAuthorityInputs: Array<{
    sourceProject: string
    sourcePath: string
    observedPattern: string
    localAbsorption: string
  }>
  claimBoundary: string
}

type BriefInput = {
  path: string
  markdown: string
  sha256?: string
}

const root = process.cwd()
const briefDirectory = 'docs/research'
const briefFilePattern = 'goal-os-*.md'
const reportDir = 'docs/product-quality'
const reportJsonPath = 'docs/product-quality/research-brief-validation-report.json'
const reportMdPath = 'docs/product-quality/research-brief-validation-report.md'

const requiredSections = [
  '## Question',
  '## Decision Needed',
  '## Local Authority Sources',
  '## Primary Source Ledger',
  '## Findings To Requirements / Evals / Guardrails / Decisions',
  '## Rejected Sources',
  '## Follow-Up Goal Candidates',
  '## Claim Boundary',
]

const requiredSources: RequiredSource[] = [
  {
    id: 'AGENTS.md',
    sourceProject: 'Local AGENTS instructions',
    sourcePath: 'AGENTS.md',
    observedPattern: 'Agent-facing repo law keeps Metaforge centered on Meta/MFH/Orchestra OS and bounds OpenClaude as runtime substrate.',
    localAbsorption: 'Research briefs must cite local operating law before changing public framing or proof copy.',
  },
  {
    id: 'README.md',
    sourceProject: 'Local README public frame',
    sourcePath: 'README.md',
    observedPattern: 'The public surface presents Metaforge as the operating system and OpenClaude as local CLI substrate.',
    localAbsorption: 'Research mapping cannot let OpenClaude become the thesis again.',
  },
  {
    id: 'docs/RESEARCH_PIPELINE.md',
    sourceProject: 'Metaforge Research Pipeline',
    sourcePath: 'docs/RESEARCH_PIPELINE.md',
    observedPattern: 'Research follows local-first, primary-source, raw/wiki/decision workflow with blog-only rejection rules.',
    localAbsorption: 'This validator enforces the reusable research brief shape from the pipeline.',
  },
  {
    id: 'docs/PROJECT_SPEC.md',
    sourceProject: 'Metaforge Project Spec',
    sourcePath: 'docs/PROJECT_SPEC.md',
    observedPattern: 'The project spec defines Meta, MFH, and Orchestra as the durable product frame.',
    localAbsorption: 'The research brief maps prior art into those product primitives instead of broad runtime claims.',
  },
  {
    id: 'docs/MFH_META_SYNTHESIS.md',
    sourceProject: 'MFH Meta Synthesis',
    sourcePath: 'docs/MFH_META_SYNTHESIS.md',
    observedPattern: 'MFH/Meta concepts are imported as governed-code gates with explicit drift boundaries.',
    localAbsorption: 'Research claims must remain evidence-aware and not imply the companion harness is green.',
  },
  {
    id: 'docs/GOAL_SCHEMA.md',
    sourceProject: 'Goal OS Schema',
    sourcePath: 'docs/GOAL_SCHEMA.md',
    observedPattern: 'Goals include research requirements, governed-code claim level, closure state, and evidence gates.',
    localAbsorption: 'The research ledger feeds goal requirements and validation evidence.',
  },
  {
    id: 'docs/EVALS.md',
    sourceProject: 'Metaforge Evals',
    sourcePath: 'docs/EVALS.md',
    observedPattern: 'Eval design includes source reconciliation, trace scoring, and verification gates.',
    localAbsorption: 'Brief findings must map to evals when they affect closure or proof quality.',
  },
  {
    id: 'docs/SECURITY_AND_GUARDRAILS.md',
    sourceProject: 'Metaforge Guardrails',
    sourcePath: 'docs/SECURITY_AND_GUARDRAILS.md',
    observedPattern: 'Security policy distinguishes operating gates from a security sandbox and keeps protected actions explicit.',
    localAbsorption: 'Research findings map to guardrails before stronger automation or public claims.',
  },
  {
    id: 'docs/DECISION_LOG.md',
    sourceProject: 'Metaforge Decision Log',
    sourcePath: 'docs/DECISION_LOG.md',
    observedPattern: 'Plan-changing research decisions are recorded as durable public authority.',
    localAbsorption: 'This slice records the research-ledger gate as a decision before marketing copy can rely on it.',
  },
  {
    id: 'docs/research/mimesis-engineering-source-ledger-2026-06-14.md',
    sourceProject: 'Mimesis Engineering Source Ledger',
    sourcePath: 'docs/research/mimesis-engineering-source-ledger-2026-06-14.md',
    observedPattern: 'Existing research ledgers preserve source-first improvement and rejected-source wording.',
    localAbsorption: 'The Goal OS brief reuses that pattern in a narrower auditable format.',
  },
  {
    id: 'docs/research/public-proof-pack-source-ledger-2026-06-14.md',
    sourceProject: 'Public Proof Pack Source Ledger',
    sourcePath: 'docs/research/public-proof-pack-source-ledger-2026-06-14.md',
    observedPattern: 'Public proof copy is bounded by local artifacts and explicit non-claims.',
    localAbsorption: 'The research ledger applies the same boundary to Goal OS prior-art claims.',
  },
  {
    id: 'https://openai.com/index/the-next-evolution-of-the-agents-sdk/',
    sourceProject: 'OpenAI Agents SDK Evolution',
    sourceUrl: 'https://openai.com/index/the-next-evolution-of-the-agents-sdk/',
    observedPattern: 'Agent runtimes are described around controlled workspaces, instructions, MCP, skills, checkpointing, and evaluation surfaces.',
    localAbsorption: 'Metaforge keeps these as runtime substrate primitives while Meta/MFH/Orchestra remains the public product thesis.',
  },
  {
    id: 'https://agents.md/',
    sourceProject: 'AGENTS.md Format',
    sourceUrl: 'https://agents.md/',
    observedPattern: 'AGENTS.md provides predictable agent instructions for setup, testing, conventions, and security notes.',
    localAbsorption: 'Local AGENTS.md stays compact and routes deeper governance into docs.',
  },
  {
    id: 'https://agentskills.io/',
    sourceProject: 'Agent Skills',
    sourceUrl: 'https://agentskills.io/',
    observedPattern: 'Skills package procedural knowledge with progressive disclosure, optional references, scripts, and assets.',
    localAbsorption: 'Repeated research workflows can become skills only after validated runs.',
  },
  {
    id: 'https://modelcontextprotocol.io/docs/getting-started/intro',
    sourceProject: 'Model Context Protocol Intro',
    sourceUrl: 'https://modelcontextprotocol.io/docs/getting-started/intro',
    observedPattern: 'MCP standardizes how applications expose context and capabilities to models.',
    localAbsorption: 'Orchestra integrations should retain typed resource/tool boundaries.',
  },
  {
    id: 'https://modelcontextprotocol.io/specification/2025-06-18/server/resources',
    sourceProject: 'MCP Resources Specification',
    sourceUrl: 'https://modelcontextprotocol.io/specification/2025-06-18/server/resources',
    observedPattern: 'Resources expose application-controlled context and data to clients.',
    localAbsorption: 'Meta state should be exposed as bounded resources rather than untracked prompt sprawl.',
  },
  {
    id: 'https://modelcontextprotocol.io/specification/2025-06-18/server/prompts',
    sourceProject: 'MCP Prompts Specification',
    sourceUrl: 'https://modelcontextprotocol.io/specification/2025-06-18/server/prompts',
    observedPattern: 'Prompts are reusable templates with declared arguments.',
    localAbsorption: 'Goal OS prompt surfaces should be reusable and inspectable before promotion.',
  },
  {
    id: 'https://modelcontextprotocol.io/specification/2024-11-05/server/tools',
    sourceProject: 'MCP Tools Specification',
    sourceUrl: 'https://modelcontextprotocol.io/specification/2024-11-05/server/tools',
    observedPattern: 'Tools are model-controlled external actions and require clear boundaries.',
    localAbsorption: 'Protected-action gates stay explicit in Goal OS and trace validation.',
  },
  {
    id: 'https://developers.openai.com/api/docs/guides/agent-evals',
    sourceProject: 'OpenAI Agent Evals',
    sourceUrl: 'https://developers.openai.com/api/docs/guides/agent-evals',
    observedPattern: 'Agent quality should be evaluated with datasets, graders, traces, and repeatable runs.',
    localAbsorption: 'Research findings map to eval changes instead of narrative-only claims.',
  },
  {
    id: 'https://developers.openai.com/api/docs/guides/trace-grading',
    sourceProject: 'OpenAI Trace Grading',
    sourceUrl: 'https://developers.openai.com/api/docs/guides/trace-grading',
    observedPattern: 'Trace-level grading evaluates complete workflows, tool calls, and outcomes.',
    localAbsorption: 'MFH closure should be trace-aware before stronger public proof copy.',
  },
  {
    id: 'https://github.com/openai/evals',
    sourceProject: 'OpenAI Evals',
    sourceUrl: 'https://github.com/openai/evals',
    observedPattern: 'Open-source eval frameworks make evaluation definitions and runs inspectable.',
    localAbsorption: 'Metaforge eval loops should be source-controlled and reproducible.',
  },
  {
    id: 'https://www.w3.org/TR/prov-overview/',
    sourceProject: 'W3C PROV',
    sourceUrl: 'https://www.w3.org/TR/prov-overview/',
    observedPattern: 'Provenance records entities, activities, agents, and relationships for evidence lineage.',
    localAbsorption: 'Research rows tie sources to findings, mappings, and claim boundaries.',
  },
  {
    id: 'https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10',
    sourceProject: 'NIST AI RMF 1.0',
    sourceUrl: 'https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10',
    observedPattern: 'AI risk management is framed as governance, mapping, measuring, and managing risks.',
    localAbsorption: 'Metaforge public claims stay proportional to local evidence and risk controls.',
  },
  {
    id: 'https://owasp.org/www-project-top-10-for-large-language-model-applications/',
    sourceProject: 'OWASP Top 10 for LLM Applications',
    sourceUrl: 'https://owasp.org/www-project-top-10-for-large-language-model-applications/',
    observedPattern: 'LLM application risks include prompt injection, sensitive information disclosure, and excessive agency.',
    localAbsorption: 'Goal OS keeps protected actions, secrets, and unsafe autonomy outside public proof claims.',
  },
  {
    id: 'https://arxiv.org/abs/2210.03629',
    sourceProject: 'ReAct',
    sourceUrl: 'https://arxiv.org/abs/2210.03629',
    observedPattern: 'Reasoning and acting can be interleaved so actions, observations, and reasoning remain inspectable.',
    localAbsorption: 'Orchestra traces should preserve action/observation structure for evals.',
  },
  {
    id: 'https://arxiv.org/abs/2303.11366',
    sourceProject: 'Reflexion',
    sourceUrl: 'https://arxiv.org/abs/2303.11366',
    observedPattern: 'Feedback and reflection memory can improve agent behavior across trials.',
    localAbsorption: 'Meta memory updates should be evidence-backed and source-linked.',
  },
  {
    id: 'https://www.uspto.gov/patents/search/patent-public-search/',
    sourceProject: 'USPTO Patent Public Search',
    sourceUrl: 'https://www.uspto.gov/patents/search/patent-public-search/',
    observedPattern: 'Patent public search is a primary route for prior-art and patent-family investigation.',
    localAbsorption: 'The research ledger records prior-art search duty without claiming patent clearance.',
  },
]

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

const mappingPattern = /\b(requirement|eval|guardrail|decision)\b/i

function normalizePath(path: string): string {
  return path.replace(/\\/g, '/')
}

function sha256(input: string): string {
  return createHash('sha256').update(input).digest('hex')
}

function hasSection(markdown: string, heading: string): boolean {
  return new RegExp(`^${escapeRegExp(heading)}\\s*$`, 'im').test(markdown)
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function sectionBody(markdown: string, heading: string): string {
  const lines = markdown.split(/\r?\n/)
  const start = lines.findIndex((line) => line.trim() === heading)
  if (start === -1) return ''
  const body: string[] = []
  for (let index = start + 1; index < lines.length; index += 1) {
    const line = lines[index] ?? ''
    if (/^##\s+/.test(line)) break
    body.push(line)
  }
  return body.join('\n')
}

function parseTableRows(markdown: string): SourceRow[] {
  const body = sectionBody(markdown, '## Primary Source Ledger')
  const rows: SourceRow[] = []
  for (const line of body.split(/\r?\n/)) {
    const trimmed = line.trim()
    if (!trimmed.startsWith('|') || !trimmed.endsWith('|')) continue
    if (/^\|\s*-+/.test(trimmed)) continue
    if (/^\|\s*source\s*\|/i.test(trimmed)) continue
    const cells = trimmed.slice(1, -1).split('|').map((cell) => cell.trim())
    if (cells.length < 6) continue
    rows.push({
      source: cells[0] ?? '',
      urlOrPath: cells[1] ?? '',
      sourceClass: cells[2] ?? '',
      finding: cells[3] ?? '',
      mapsTo: cells[4] ?? '',
      boundary: cells.slice(5).join(' | '),
    })
  }
  return rows
}

function sourceMatches(row: SourceRow, requiredSource: RequiredSource): boolean {
  const haystack = `${row.source} ${row.urlOrPath}`.toLowerCase()
  const needle = (requiredSource.sourceUrl ?? requiredSource.sourcePath ?? requiredSource.id).toLowerCase()
  return haystack.includes(needle)
}

function disallowedSource(urlOrPath: string): string | null {
  let host = ''
  try {
    host = new URL(urlOrPath).host.toLowerCase()
  } catch {
    return null
  }
  const fragment = disallowedSecondaryHostFragments.find((item) => host === item || host.endsWith(`.${item}`))
  return fragment ? urlOrPath : null
}

function nonEmpty(value: string): boolean {
  return value.trim().length > 0
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

export function evaluateResearchBrief(
  markdown: string,
  path?: string,
  contentSha256?: string,
): ResearchBriefValidationResult {
  const errors: string[] = []

  for (const section of requiredSections) {
    if (!hasSection(markdown, section)) {
      errors.push(`missing required section: ${section}`)
    }
  }

  if (!/Date accessed:\s*20\d{2}-\d{2}-\d{2}/i.test(markdown)) {
    errors.push('brief must include Date accessed: YYYY-MM-DD')
  }

  const rows = parseTableRows(markdown)
  if (rows.length === 0) {
    errors.push('primary source ledger must contain at least one source row')
  }

  const missingSources = requiredSources
    .filter((source) => !rows.some((row) => sourceMatches(row, source)))
    .map((source) => source.id)
  for (const source of missingSources) {
    errors.push(`primary source ledger is missing required source: ${source}`)
  }

  const disallowedSources = rows
    .map((row) => disallowedSource(row.urlOrPath))
    .filter((value): value is string => value !== null)
  for (const source of disallowedSources) {
    errors.push(`primary source ledger contains disallowed secondary/blog source: ${source}`)
  }

  for (const row of rows) {
    if (![row.source, row.urlOrPath, row.sourceClass, row.finding, row.mapsTo, row.boundary].every(nonEmpty)) {
      errors.push(`primary source ledger row has an empty required cell: ${row.urlOrPath || row.source || 'unknown'}`)
    }
    if (!mappingPattern.test(row.mapsTo)) {
      errors.push(`primary source ledger row must map to requirement, eval, guardrail, or decision: ${row.urlOrPath || row.source || 'unknown'}`)
    }
    if (!/\b(local|no-provider|not|boundary|claim|evidence|validation|clearance|production|external)\b/i.test(row.boundary)) {
      errors.push(`primary source ledger row must include an explicit claim boundary: ${row.urlOrPath || row.source || 'unknown'}`)
    }
  }

  const forbiddenReadinessClaims = [
    /\bis production ready\b/i,
    /\bhas external validation\b/i,
    /\bis benchmark[- ]leading\b/i,
    /\bpatent cleared\b/i,
    /\bis autonomously reliable\b/i,
  ]
  if (forbiddenReadinessClaims.some((pattern) => pattern.test(markdown))) {
    errors.push('brief contains forbidden readiness or clearance wording')
  }

  const presentSources = requiredSources
    .filter((source) => rows.some((row) => sourceMatches(row, source)))
    .map((source) => source.id)

  return {
    path,
    ok: errors.length === 0,
    errors,
    sourceRowCount: rows.length,
    requiredSourceCoverage: {
      present: presentSources,
      missing: missingSources,
    },
    disallowedSources,
    mappedRowCount: rows.filter((row) => mappingPattern.test(row.mapsTo)).length,
    sha256: contentSha256,
  }
}

export function buildResearchBriefReport(briefs: BriefInput[]): ResearchBriefValidationReport {
  const validationResults = briefs.map((brief) =>
    evaluateResearchBrief(brief.markdown, brief.path, brief.sha256),
  )
  const validBriefCount = validationResults.filter((result) => result.ok).length
  const invalidBriefCount = validationResults.length - validBriefCount
  const missingSources = [...new Set(validationResults.flatMap((result) => result.requiredSourceCoverage.missing))].sort()

  const researchBriefChecks = [
    check('goal-os research briefs discovered', briefs.length > 0, `${briefs.length} files`),
    check('all goal-os research briefs pass primary-source validation', invalidBriefCount === 0, `${validBriefCount}/${briefs.length} valid`),
    check('all required source anchors are covered', missingSources.length === 0, missingSources.join(', ') || 'all required sources present'),
    check('secondary/blog sources are absent from final source ledgers', validationResults.every((result) => result.disallowedSources.length === 0), validationResults.flatMap((result) => result.disallowedSources).join(', ') || 'none'),
    check('no provider/live/external/protected side effects recorded', true, 'side-effect arrays are empty'),
  ]

  return {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_research_brief_validation',
    briefDirectory,
    briefFilePattern,
    briefFileCount: briefs.length,
    validBriefCount,
    invalidBriefCount,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    validationResults,
    researchBriefChecks,
    primarySourceInputs: requiredSources
      .filter((source): source is RequiredSource & { sourceUrl: string } => typeof source.sourceUrl === 'string')
      .map((source) => ({
        sourceProject: source.sourceProject,
        sourceUrl: source.sourceUrl,
        observedPattern: source.observedPattern,
        localAbsorption: source.localAbsorption,
      })),
    localAuthorityInputs: requiredSources
      .filter((source): source is RequiredSource & { sourcePath: string } => typeof source.sourcePath === 'string')
      .map((source) => ({
        sourceProject: source.sourceProject,
        sourcePath: source.sourcePath,
        observedPattern: source.observedPattern,
        localAbsorption: source.localAbsorption,
      })),
    claimBoundary: 'Research brief validation is local no-provider documentation governance evidence only. It does not fetch sources, call providers, call live models, call external services, perform protected actions, claim production readiness, claim external validation, claim benchmark superiority, claim patent clearance, or claim autonomous reliability.',
  }
}

function listBriefFiles(): BriefInput[] {
  const absoluteBriefDir = resolve(root, briefDirectory)
  if (!existsSync(absoluteBriefDir)) return []
  return readdirSync(absoluteBriefDir)
    .filter((name) => /^goal-os-.*\.md$/i.test(name))
    .sort((left, right) => left.localeCompare(right))
    .map((name) => {
      const path = normalizePath(`${briefDirectory}/${name}`)
      const markdown = readFileSync(resolve(root, path), 'utf8')
      return {
        path,
        markdown,
        sha256: sha256(markdown),
      }
    })
}

function writeReport(report: ResearchBriefValidationReport): void {
  mkdirSync(resolve(root, reportDir), { recursive: true })
  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)

  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} | ${source.localAbsorption} |`)
  const localRows = report.localAuthorityInputs
    .map((source) => `| ${source.sourceProject} | \`${source.sourcePath}\` | ${source.observedPattern} | ${source.localAbsorption} |`)
  const resultRows = report.validationResults
    .map((result) => `| \`${result.path ?? 'memory'}\` | \`${result.ok}\` | ${result.sourceRowCount} | ${result.requiredSourceCoverage.missing.length === 0 ? 'none' : result.requiredSourceCoverage.missing.map((source) => `\`${source}\``).join('<br>')} | ${result.errors.length === 0 ? 'none' : result.errors.map((error) => `\`${error}\``).join('<br>')} | \`${result.sha256 ?? 'n/a'}\` |`)
  const checkRows = report.researchBriefChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)

  const markdown = [
    '# Research Brief Validation Report',
    '',
    'Generated by: `bun run research:validate`',
    '',
    '## Claim Boundary',
    '',
    `- ${report.claimBoundary}`,
    '- The validator performs no provider, live model, external, or protected calls.',
    '',
    '## Summary',
    '',
    `- mode: \`${report.mode}\``,
    `- brief_directory: \`${report.briefDirectory}\``,
    `- brief_file_pattern: \`${report.briefFilePattern}\``,
    `- brief_file_count: \`${report.briefFileCount}\``,
    `- valid_brief_count: \`${report.validBriefCount}\``,
    `- invalid_brief_count: \`${report.invalidBriefCount}\``,
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
    '## Local Authority Inputs',
    '',
    '| Source | Path | Pattern Absorbed | Local Absorption |',
    '| --- | --- | --- | --- |',
    ...localRows,
    '',
    '## Brief Results',
    '',
    '| Brief | Passed | Source Rows | Missing Required Sources | Errors | SHA-256 |',
    '| --- | --- | ---: | --- | --- | --- |',
    ...resultRows,
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
  const report = buildResearchBriefReport(listBriefFiles())
  writeReport(report)

  for (const result of report.validationResults) {
    console.log(`${result.ok ? 'PASS' : 'FAIL'}: ${result.path ?? 'memory'} (${result.sourceRowCount} source rows)`)
    for (const error of result.errors) {
      console.log(`  - ${error}`)
    }
  }
  for (const check of report.researchBriefChecks) {
    console.log(`${check.ok ? 'PASS' : 'FAIL'}: ${check.label} (${check.detail})`)
  }
  console.log('')
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)

  if (report.briefFileCount === 0 || report.invalidBriefCount > 0 || !report.researchBriefChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
}

if (import.meta.main) {
  main()
}
