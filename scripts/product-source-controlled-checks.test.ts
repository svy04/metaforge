import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const scriptPath = join(__dirname, 'product-source-controlled-checks.ts')

function makeTempRepo(): string {
  const repo = mkdtempSync(join(tmpdir(), 'openclaude-source-controlled-checks-'))
  mkdirSync(join(repo, '.github', 'workflows'), { recursive: true })
  return repo
}

function writeWorkflow(repo: string, path: string, body: string): void {
  writeFileSync(join(repo, '.github', 'workflows', path), body)
}

function minimalWorkflow(extra = ''): string {
  return [
    'name: PR Checks',
    '',
    'on:',
    '  pull_request:',
    '  push:',
    '    branches:',
    '      - main',
    '',
    extra.trimEnd(),
    '',
    'jobs:',
    '  test:',
    '    runs-on: ubuntu-latest',
    '    steps:',
    '      - name: Check out repository',
    '        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683',
    '      - run: bun run product:quality',
  ].filter((line) => line !== '').join('\n')
}

function workflowWithSetupBun(extra = '', setupBunRef = '0c5077e51419868618aeaa5fe8019c62421857d6 # v2.2.0'): string {
  return [
    'name: PR Checks',
    '',
    'on:',
    '  pull_request:',
    '  push:',
    '    branches:',
    '      - main',
    '',
    extra.trimEnd(),
    '',
    'jobs:',
    '  test:',
    '    runs-on: ubuntu-latest',
    '    steps:',
    '      - name: Check out repository',
    '        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683',
    '      - name: Set up Bun',
    `        uses: oven-sh/setup-bun@${setupBunRef}`,
    '      - run: bun run product:quality',
  ].filter((line) => line !== '').join('\n')
}

function runSourceControlledChecks(repo: string) {
  return spawnSync('bun', ['run', scriptPath], {
    cwd: repo,
    encoding: 'utf8',
    shell: false,
  })
}

describe('product source-controlled checks', () => {
  test('fails when workflows do not opt in to the Node 24 action runtime', () => {
    const repo = makeTempRepo()
    try {
      writeWorkflow(repo, 'pr-checks.yml', minimalWorkflow())
      writeWorkflow(repo, 'codeql.yml', minimalWorkflow())
      writeWorkflow(repo, 'dependency-review.yml', minimalWorkflow())
      writeWorkflow(repo, 'release.yml', minimalWorkflow())

      const result = runSourceControlledChecks(repo)

      expect(result.status).not.toBe(0)
      expect(`${result.stdout}\n${result.stderr}`).toContain('Node 24 JavaScript action runtime opt-in is present')
    } finally {
      rmSync(repo, { recursive: true, force: true })
    }
  })

  test('passes when all workflows opt in to the Node 24 action runtime', () => {
    const repo = makeTempRepo()
    const optIn = [
      'env:',
      '  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"',
    ].join('\n')

    try {
      writeWorkflow(repo, 'pr-checks.yml', minimalWorkflow(optIn))
      writeWorkflow(repo, 'codeql.yml', minimalWorkflow(optIn))
      writeWorkflow(repo, 'dependency-review.yml', minimalWorkflow(optIn))
      writeWorkflow(repo, 'release.yml', minimalWorkflow(optIn))

      const result = runSourceControlledChecks(repo)

      expect(result.status, `${result.stdout}\n${result.stderr}`).toBe(0)
      expect(result.stdout).toContain('node24_action_runtime_opt_in_present=true')
    } finally {
      rmSync(repo, { recursive: true, force: true })
    }
  })

  test('fails when a known Node 20 JavaScript action remains pinned', () => {
    const repo = makeTempRepo()
    const optIn = [
      'env:',
      '  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"',
    ].join('\n')

    try {
      writeWorkflow(repo, 'pr-checks.yml', workflowWithSetupBun(optIn, '4bc047ad259df6fc24a6c9b0f9a0cb08cf17fbe5 # v2.0.1'))
      writeWorkflow(repo, 'codeql.yml', minimalWorkflow(optIn))
      writeWorkflow(repo, 'dependency-review.yml', minimalWorkflow(optIn))
      writeWorkflow(repo, 'release.yml', workflowWithSetupBun(optIn, '4bc047ad259df6fc24a6c9b0f9a0cb08cf17fbe5 # v2.0.1'))

      const result = runSourceControlledChecks(repo)

      expect(result.status).not.toBe(0)
      expect(`${result.stdout}\n${result.stderr}`).toContain('known Node 20 JavaScript action references are absent')
    } finally {
      rmSync(repo, { recursive: true, force: true })
    }
  })
})
