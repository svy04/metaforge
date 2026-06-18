import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { tmpdir } from 'node:os'

const scriptPath = join(__dirname, 'public-artifact-hygiene.ts')
const tempDirs: string[] = []
const windowsPrivatePath = ['C:', 'Users', 'fixture-owner', 'Desktop', 'private-space', 'openclaude-0.6.0'].join('\\')
const secretLikePlaceholder = ['OPENAI_API_KEY=', 'sk', 'openai', 'placeholder'].join('-')

function makeTempRepo(): string {
  const dir = mkdtempSync(join(tmpdir(), 'openclaude-public-hygiene-'))
  tempDirs.push(dir)
  return dir
}

function runHygiene(cwd: string) {
  return spawnSync('bun', ['run', scriptPath], {
    cwd,
    encoding: 'utf8',
    shell: false,
  })
}

afterEach(() => {
  for (const dir of tempDirs.splice(0)) {
    rmSync(dir, { recursive: true, force: true })
  }
})

describe('public artifact hygiene scanner', () => {
  test('scans root environment examples for local path disclosure', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, '.env.example'),
      `OPENCLAUDE_HOME=${windowsPrivatePath}`,
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('.env.example')
  })

  test('rejects scanner-unfriendly fake API key placeholders in public examples', () => {
    const repo = makeTempRepo()
    writeFileSync(join(repo, '.env.example'), `${secretLikePlaceholder}\n`)

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('.env.example')
  })

  test('rejects stale model locks in tracked planning artifacts', () => {
    const repo = makeTempRepo()
    const planningDir = join(repo, '.planning')
    mkdirSync(planningDir, { recursive: true })
    writeFileSync(
      join(planningDir, 'PROJECT.md'),
      'Always call GPT 5.5 + Opus 4.7; fallback must not use gpt-4o.\n',
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('.planning/PROJECT.md')
    expect(`${result.stdout}\n${result.stderr}`).toContain('stale-model-lock')
  })

  test('rejects ignored local OpenClaude profiles with secret-shaped placeholders', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, '.openclaude-profile.json'),
      JSON.stringify({
        profile: 'openai',
        env: {
          OPENAI_MODEL: 'gpt-4o',
          OPENAI_API_KEY: 'sk-openai-key',
        },
      }),
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('.openclaude-profile.json')
    expect(`${result.stdout}\n${result.stderr}`).toContain('actual-looking-sk-token')
  })

  test('rejects ignored local tool config files with private paths or runtime context', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, '.mcp.json'),
      JSON.stringify({
        mcpServers: {
          local: {
            command: windowsPrivatePath,
          },
        },
      }),
    )
    const cursorDir = join(repo, '.cursor')
    mkdirSync(cursorDir, { recursive: true })
    writeFileSync(
      join(cursorDir, 'rules.md'),
      '<codex_internal_context source="goal">\n',
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('.mcp.json')
    expect(`${result.stdout}\n${result.stderr}`).toContain('.cursor/rules.md')
  })

  test('rejects private workspace placeholders in public docs', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, 'README.md'),
      'Use <private-workspace>/meta/CLAUDE.md as the authority file.\n',
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('README.md')
  })

  test('rejects private agent-memory placeholder breadcrumbs in public docs', () => {
    const repo = makeTempRepo()
    writeFileSync(join(repo, 'README.md'), 'Memory root: <private-codex-memory-dir>\n')
    writeFileSync(join(repo, 'SUPPORT.md'), 'Skill root: <private-agent-skill-dir>\n')

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('README.md')
    expect(`${result.stdout}\n${result.stderr}`).toContain('SUPPORT.md')
    expect(`${result.stdout}\n${result.stderr}`).toContain('private-codex-memory-placeholder')
    expect(`${result.stdout}\n${result.stderr}`).toContain('private-agent-skill-placeholder')
  })

  test('rejects environment-expanded user workspace paths in public docs', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, 'README.md'),
      [
        String.raw`Internal capture: %USERPROFILE%\Desktop\client-lab\trace.json`,
        String.raw`Local proof: $HOME/Documents/private-research/session.md`,
        String.raw`Operator note: ~/Desktop/private-run/output.log`,
      ].join('\n'),
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('README.md')
    expect(`${result.stdout}\n${result.stderr}`).toContain('user-workspace-path')
  })

  test('rejects pasted internal runtime context in public docs', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, 'README.md'),
      [
        '<codex_internal_context source="goal">',
        '<environment_context>',
        '<workspace_roots><root><repo></root></workspace_roots>',
        '<permissions instructions>',
      ].join('\n'),
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('README.md')
  })

  test('rejects raw public-comment UI dumps in public docs', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, 'README.md'),
      [
        '갤로그로 이동합니다.',
        '댓글돌이',
        '삭제',
      ].join('\n'),
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('README.md')
  })

  test('scans the root license for local path disclosure', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, 'LICENSE'),
      `Derived runtime note copied from ${windowsPrivatePath}\n`,
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('LICENSE')
  })

  test('scans root support docs for local path disclosure', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, 'SUPPORT.md'),
      `Support packet copied from ${windowsPrivatePath}\n`,
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('SUPPORT.md')
  })

  test('rejects actual-looking public credential tokens', () => {
    const repo = makeTempRepo()
    const githubToken = 'ghp_' + 'A'.repeat(36)
    const awsKey = 'AKIA' + 'A'.repeat(16)
    const slackToken = 'xoxb-' + 'A'.repeat(12)
    writeFileSync(
      join(repo, 'README.md'),
      [
        `GITHUB_TOKEN=${githubToken}`,
        `AWS_ACCESS_KEY_ID=${awsKey}`,
        `SLACK_BOT_TOKEN=${slackToken}`,
      ].join('\n'),
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('README.md')
    expect(`${result.stdout}\n${result.stderr}`).toContain('github-token')
  })

  test('scans the canonical VS Code extension README for local path disclosure', () => {
    const repo = makeTempRepo()
    const extensionDir = join(repo, 'packages', 'openclaude-vscode')
    mkdirSync(extensionDir, { recursive: true })
    writeFileSync(
      join(extensionDir, 'README.md'),
      `Derived runtime note copied from ${windowsPrivatePath}\n`,
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('packages/openclaude-vscode/README.md')
  })

  test('scans the canonical VS Code extension package manifest for local path disclosure', () => {
    const repo = makeTempRepo()
    const extensionDir = join(repo, 'packages', 'openclaude-vscode')
    mkdirSync(extensionDir, { recursive: true })
    writeFileSync(
      join(extensionDir, 'package.json'),
      JSON.stringify({ description: `Derived runtime note copied from ${windowsPrivatePath}` }),
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('packages/openclaude-vscode/package.json')
  })

  test('scans the legacy VS Code extension package manifest for local path disclosure', () => {
    const repo = makeTempRepo()
    const extensionDir = join(repo, 'vscode-extension', 'openclaude-vscode')
    mkdirSync(extensionDir, { recursive: true })
    writeFileSync(
      join(extensionDir, 'package.json'),
      JSON.stringify({ description: `Derived runtime note copied from ${windowsPrivatePath}` }),
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('vscode-extension/openclaude-vscode/package.json')
  })

  test('scans AVF evidence reports for local file URL self-test disclosure', () => {
    const repo = makeTempRepo()
    const reportDir = join(repo, 'avf', 'influence_factory', 'product_app')
    mkdirSync(reportDir, { recursive: true })
    writeFileSync(
      join(reportDir, 'self_test_report_v35.md'),
      'chrome --headless --dump-dom file:///.../index.html#selftest\n',
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('avf/influence_factory/product_app/self_test_report_v35.md')
    expect(`${result.stdout}\n${result.stderr}`).toContain('local-file-url')
  })

  test('rejects placeholder user-home VS Code update sentinel paths in public reports', () => {
    const repo = makeTempRepo()
    const reportDir = join(repo, 'docs', 'product-quality')
    mkdirSync(reportDir, { recursive: true })
    writeFileSync(
      join(reportDir, 'vscode-startup-diagnostics-report.md'),
      '| `<user-home>\\AppData\\Local\\Programs\\Microsoft VS Code\\commit\\resources\\app\\updating` | `false` | `null` |\n',
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('docs/product-quality/vscode-startup-diagnostics-report.md')
    expect(`${result.stdout}\n${result.stderr}`).toContain('vscode-user-home-sentinel-path')
  })

  test('rejects bare local self-test targets in goal evidence reports', () => {
    const repo = makeTempRepo()
    const reportDir = join(repo, 'docs', 'goals')
    mkdirSync(reportDir, { recursive: true })
    writeFileSync(
      join(reportDir, 'INFLUENCE_FACTORY_COMPLETION_CANDIDATE_V42_VALIDATION_REPORT.md'),
      'chrome --headless --dump-dom index.html#selftest\n',
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('docs/goals/INFLUENCE_FACTORY_COMPLETION_CANDIDATE_V42_VALIDATION_REPORT.md')
    expect(`${result.stdout}\n${result.stderr}`).toContain('local-selftest-target')
  })

  test('rejects repo-relative local self-test targets in AVF reports', () => {
    const repo = makeTempRepo()
    const reportDir = join(repo, 'avf', 'influence_factory', 'product_app')
    mkdirSync(reportDir, { recursive: true })
    writeFileSync(
      join(reportDir, 'self_test_report.md'),
      '- Target: `avf/influence_factory/product_app/index.html#selftest`\n',
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('avf/influence_factory/product_app/self_test_report.md')
    expect(`${result.stdout}\n${result.stderr}`).toContain('local-selftest-target')
  })

  test('rejects generated evidence references to local executable paths', () => {
    const repo = makeTempRepo()
    const reportDir = join(repo, 'docs', 'goals')
    mkdirSync(reportDir, { recursive: true })
    writeFileSync(
      join(reportDir, 'INFLUENCE_FACTORY_LOCAL_ITERATION_EXECUTION_V18_VALIDATION_REPORT.md'),
      'HEADLESS_BROWSER=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\n',
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('docs/goals/INFLUENCE_FACTORY_LOCAL_ITERATION_EXECUTION_V18_VALIDATION_REPORT.md')
    expect(`${result.stdout}\n${result.stderr}`).toContain('windows-local-executable-path')
  })
})
