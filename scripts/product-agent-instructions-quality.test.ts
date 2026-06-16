import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, rmSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'

const root = join(__dirname, '..')
const scriptPath = join(__dirname, 'product-agent-instructions-quality.ts')
const fakeHash = 'a'.repeat(64)
const workflowPaths = [
  '.github/workflows/pr-checks.yml',
  '.github/workflows/codeql.yml',
  '.github/dependabot.yml',
]

function workflowMap(value: boolean): Record<string, boolean> {
  return Object.fromEntries(workflowPaths.map((path) => [path, value]))
}

function cleanAgentInstructions(): string {
  return [
    '# Metaforge Agent Workflow',
    '',
    '## Repository Orientation',
    '',
    '### Repository Purpose',
    '',
    'Metaforge is the public Meta/MFH/Orchestra OS product surface.',
    '',
    '### Setup And Verification Commands',
    '',
    '- `bun run build`',
    '- `bun run typecheck --pretty false`',
    '- `bun run product:quality`',
    '- `bun run verify:privacy`',
    '',
    '### Repository Structure',
    '',
    '- `src/`',
    '- `scripts/`',
    '- `docs/`',
    '- `reports/`',
    '- `packages/openclaude-vscode/`',
    '- `.github/`',
    '',
    '## Workflow Stack',
    '',
    'GStack, GSD, and Superpowers stay separated.',
    '',
    '## Standing Research Rule',
    '',
    'Use primary sources. Blogs only as pointers.',
    '',
    '## Verification Standard',
    '',
    'Do not claim completion from file presence alone. Verify by running the relevant command.',
    '',
    '## Public Claim Boundaries',
    '',
    'Protected actions and readiness claim language need explicit authorization.',
  ].join('\n')
}

async function analyze(agentInstructions: string) {
  const module = await import('./product-agent-instructions-quality')
  return module.analyzeAgentInstructionsQuality({
    agentInstructions,
    packageJson: {
      scripts: {
        'product:quality': 'bun run product:agent-instructions-quality',
      },
    },
    workflowPresence: workflowMap(true),
    workflowSha256: Object.fromEntries(workflowPaths.map((path) => [path, fakeHash])),
    sourceAgentInstructionsSha256: fakeHash,
    sourcePackageJsonSha256: fakeHash,
    generatedAt: '2026-06-16T00:00:00.000Z',
  })
}

describe('product agent instructions quality analyzer', () => {
  test('check mode does not write generated reports', () => {
    const tempRoot = join(root, '.tmp-agent-instructions-quality-check')
    rmSync(tempRoot, { recursive: true, force: true })
    mkdirSync(join(tempRoot, '.github/workflows'), { recursive: true })
    mkdirSync(join(tempRoot, '.github'), { recursive: true })
    writeFileSync(join(tempRoot, 'AGENTS.md'), cleanAgentInstructions())
    writeFileSync(
      join(tempRoot, 'package.json'),
      JSON.stringify({ scripts: { 'product:quality': 'bun run product:agent-instructions-quality' } }, null, 2),
    )
    writeFileSync(join(tempRoot, '.github/workflows/pr-checks.yml'), 'run: bun run product:quality\n')
    writeFileSync(join(tempRoot, '.github/workflows/codeql.yml'), 'name: CodeQL\n')
    writeFileSync(join(tempRoot, '.github/dependabot.yml'), 'version: 2\n')

    const result = spawnSync('bun', [scriptPath, '--check'], {
      cwd: tempRoot,
      encoding: 'utf8',
      shell: false,
    })

    expect(result.status, `${result.stdout}\n${result.stderr}`).toBe(0)
    expect(result.stdout).toContain('RESULT: PASS')
    expect(existsSync(join(tempRoot, 'docs/product-quality/agent-instructions-quality-report.json'))).toBe(false)
    expect(existsSync(join(tempRoot, 'docs/product-quality/agent-instructions-quality-report.md'))).toBe(false)

    rmSync(tempRoot, { recursive: true, force: true })
  })

  test('passes a clean public AGENTS fixture', async () => {
    const report = await analyze(cleanAgentInstructions())

    expect(report.purposeSectionPresent).toBe(true)
    expect(report.verificationStandardPresent).toBe(true)
    expect(report.privateMemoryDumpPresent).toBe(false)
    expect(report.localPathLeakPresent).toBe(false)
    expect(report.stalePublicModelLockPresent).toBe(false)
    expect(report.instructionQualityChecks.every((item) => item.ok)).toBe(true)
  })

  test('flags private memory breadcrumbs, local paths, and stale model locks', async () => {
    const localPath = ['C:', 'Users', 'owner', 'Desktop'].join('\\')
    const staleModel = ['gpt', '5.1'].join('-')
    const privateMarker = ['OpenClaude Orchestrator', ' Memory'].join('')
    const report = await analyze(`${cleanAgentInstructions()}\n${privateMarker}\n${localPath}\n${staleModel}\n`)

    expect(report.privateMemoryDumpPresent).toBe(true)
    expect(report.localPathLeakPresent).toBe(true)
    expect(report.stalePublicModelLockPresent).toBe(true)
    expect(report.instructionQualityChecks.find((item) => item.label === 'AGENTS.md excludes private memory dumps')?.ok).toBe(false)
    expect(report.instructionQualityChecks.find((item) => item.label === 'AGENTS.md excludes local user paths')?.ok).toBe(false)
    expect(report.instructionQualityChecks.find((item) => item.label === 'AGENTS.md excludes stale public model-lock lines')?.ok).toBe(false)
  })

  test('does not satisfy structural checks with unrelated marker text', async () => {
    const report = await analyze([
      '# Metaforge Agent Workflow',
      '',
      '## Repository Orientation',
      '',
      'This sentence mentions ### Repository Purpose without creating that heading.',
      '',
      'The phrase file presence appears here, and Verify by running appears here too.',
      '',
      '```md',
      '## Verification Standard',
      'file presence',
      'Verify by running',
      '```',
      '',
      '## Workflow Stack',
      'GStack, GSD, and Superpowers.',
      '',
      '## Standing Research Rule',
      'Use primary sources. Blogs only as pointers.',
      '',
      '## Public Claim Boundaries',
      'Protected actions and readiness claim language need explicit authorization.',
      '',
      'src/ scripts/ docs/ reports/ packages/openclaude-vscode/ .github/',
      'bun run build bun run typecheck bun run product:quality bun run verify:privacy',
    ].join('\n'))

    expect(report.purposeSectionPresent).toBe(false)
    expect(report.verificationStandardPresent).toBe(false)
    expect(report.instructionQualityChecks.find((item) => item.label === 'repository purpose is explicit')?.ok).toBe(false)
    expect(report.instructionQualityChecks.find((item) => item.label === 'verification standard remains explicit')?.ok).toBe(false)
  })
})
