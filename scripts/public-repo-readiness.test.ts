import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { existsSync, mkdtempSync, rmSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const root = join(__dirname, '..')

function readRepoText(path: string): string {
  return readFileSync(join(root, path), 'utf8')
}

function privateLocalPathNeedles(): string[] {
  return [
    `C:${'\\\\'}Users`,
    `C:${'/'}Users`,
    ['내 순수', ' 재미'].join(''),
  ]
}

function readTextFrom(basePath: string, relativePath: string): string {
  return readFileSync(join(basePath, relativePath), 'utf8')
}

function runPublicArtifactHygiene(basePath: string, args: string[] = []) {
  return spawnSync(
    process.execPath,
    [join(root, 'scripts/public-artifact-hygiene.ts'), ...args],
    {
      cwd: basePath,
      encoding: 'utf8',
    },
  )
}

function trackedRepoPaths(basePath: string): string[] {
  const result = spawnSync('git', ['ls-files'], {
    cwd: basePath,
    encoding: 'utf8',
  })

  if (result.status !== 0) {
    throw new Error(`git ls-files failed: ${result.stderr}`)
  }

  return result.stdout.split(/\r?\n/).filter(Boolean)
}

function validateKoreanReadmeRoute(basePath: string): string[] {
  const issues: string[] = []
  const readme = readTextFrom(basePath, 'README.md')
  const koreanLink = readme.match(/\[한국어\]\(([^)]+)\)/)

  if (!koreanLink) {
    issues.push('README missing Korean README link')
    return issues
  }

  if (koreanLink[1] !== 'README.ko.md') {
    issues.push('README Korean link must be repo-relative README.ko.md')
    return issues
  }

  const koreanReadmePath = join(basePath, 'README.ko.md')
  if (!existsSync(koreanReadmePath)) {
    issues.push('README.ko.md target is missing')
    return issues
  }

  const koreanReadme = readTextFrom(basePath, 'README.ko.md')
  if (!koreanReadme.includes('Meta/MFH/Orchestra')) {
    issues.push('README.ko.md missing Meta/MFH/Orchestra framing')
  }
  if (!koreanReadme.includes('OpenClaude')) {
    issues.push('README.ko.md missing OpenClaude substrate wording')
  }
  if (!koreanReadme.includes('검증')) {
    issues.push('README.ko.md missing Korean verification wording')
  }

  return issues
}

function readPublicSetupDocs(): Record<string, string> {
  const paths = [
    'README.md',
    'README.ko.md',
    'docs/quick-start-windows.md',
    'docs/quick-start-mac-linux.md',
    'docs/advanced-setup.md',
    'docs/litellm-setup.md',
  ]
  return Object.fromEntries(paths.map((path) => [path, readRepoText(path)]))
}

describe('public repository readiness surfaces', () => {
  test('AGENTS.md is public-facing guidance, not a private memory dump', () => {
    const agents = readRepoText('AGENTS.md')
    const lineCount = agents.split(/\r?\n/).length

    expect(lineCount).toBeLessThanOrEqual(220)
    expect(agents).toContain('Meta/MFH/Orchestra')
    expect(agents).toContain('OpenClaude runtime')
    expect(agents).toContain('docs/product-quality/public-feedback-snapshot-2026-06-15.md')
    expect(agents).toContain('docs/product-quality/public-feedback-triage-2026-06-15.md')
    expect(agents).toContain('behavioral happy-path, edge-case, and side-effect evidence')
    expect(agents).not.toContain('OpenClaude Orchestrator Memory')
    expect(agents).not.toContain('Use tools such as Knip')
    expect(agents).not.toMatch(/\b(gpt-5\.1|sonnet 4\.5|Opus 4\.7)\b/i)
    for (const needle of privateLocalPathNeedles()) {
      expect(agents).not.toContain(needle)
    }
  })

  test('README routes Korean readers to a maintained Korean README', () => {
    expect(validateKoreanReadmeRoute(root)).toEqual([])
  })

  test('Korean README route contract rejects broken public navigation fixtures', () => {
    const fixtureRoot = mkdtempSync(join(tmpdir(), 'metaforge-readme-route-'))
    try {
      writeFileSync(join(fixtureRoot, 'README.md'), '[한국어](README.ko.md)\n')
      expect(validateKoreanReadmeRoute(fixtureRoot)).toContain('README.ko.md target is missing')

      writeFileSync(join(fixtureRoot, 'README.ko.md'), 'OpenClaude only\n')
      expect(validateKoreanReadmeRoute(fixtureRoot)).toContain('README.ko.md missing Meta/MFH/Orchestra framing')
      expect(validateKoreanReadmeRoute(fixtureRoot)).toContain('README.ko.md missing Korean verification wording')

      writeFileSync(join(fixtureRoot, 'README.md'), '[한국어](C:/Users/example/README.ko.md)\n')
      expect(validateKoreanReadmeRoute(fixtureRoot)).toContain('README Korean link must be repo-relative README.ko.md')
    } finally {
      rmSync(fixtureRoot, { recursive: true, force: true })
    }
  })

  test('public artifact hygiene rejects private agent-memory breadcrumbs in fixtures', () => {
    const fixtureRoot = mkdtempSync(join(tmpdir(), 'metaforge-public-hygiene-'))
    try {
      writeFileSync(
        join(fixtureRoot, 'README.md'),
        'Internal handoff: .codex/memories and .agents/skills are not public docs.\n',
      )

      const result = runPublicArtifactHygiene(fixtureRoot)
      const output = `${result.stdout}${result.stderr}`

      expect(result.status).toBe(1)
      expect(output).toContain('RESULT: FAIL')
      expect(output).toContain('README.md')
    } finally {
      rmSync(fixtureRoot, { recursive: true, force: true })
    }
  })

  test('tracked public paths stay portable for default Windows checkouts', () => {
    const longPaths = trackedRepoPaths(root).filter((path) => path.length > 240)

    expect(longPaths).toEqual([])
  })

  test('advanced setup uses the current public repository source URL', () => {
    const advancedSetup = readRepoText('docs/advanced-setup.md')

    expect(advancedSetup).toContain('https://github.com/svy04/metaforge.git')
    expect(advancedSetup).not.toContain('node.gitlawb.com')
    expect(advancedSetup).not.toContain('Gitlawb/openclaude')
  })

  test('release workflow is a public boundary gate, not an active publish pipeline', () => {
    const releaseWorkflow = readRepoText('.github/workflows/release.yml')

    expect(releaseWorkflow).toContain('Release Boundary')
    expect(releaseWorkflow).toContain('No npm publish, Docker push, or release creation is authorized')
    expect(releaseWorkflow).not.toMatch(/^\s*run:\s*npm publish\b/m)
    expect(releaseWorkflow).not.toMatch(/docker\/build-push-action/)
    expect(releaseWorkflow).not.toMatch(/release-please-action/)
    expect(releaseWorkflow).not.toContain('Gitlawb/openclaude')
  })

  test('README states runtime wiring honestly', () => {
    const readme = readRepoText('README.md')

    expect(readme).toContain('Orchestra is the runtime-wired layer in this package today')
    expect(readme).toContain('Meta and MFH are governance, schema, and evidence-gate surfaces')
    expect(readme).toContain('AVF Influence Factory is a repo-local manual artifact lane')
    expect(readme).not.toContain('Meta, MFH, and AVF are runtime-wired modules')
  })

  test('public setup docs do not pin stale OpenAI model examples', () => {
    const docs = readPublicSetupDocs()

    for (const [path, text] of Object.entries(docs)) {
      expect(text, path).not.toMatch(/\bgpt-4o\b/i)
    }

    expect(docs['README.md']).toContain('<current-openai-tool-model>')
    expect(docs['docs/quick-start-windows.md']).toContain('<current-openai-tool-model>')
    expect(docs['docs/quick-start-mac-linux.md']).toContain('<current-openai-tool-model>')
    expect(docs['docs/advanced-setup.md']).toContain('<current-openai-tool-model>')
    expect(docs['docs/litellm-setup.md']).toContain('openai-tool-model')
  })

  test('README states origin and license boundaries honestly', () => {
    const readme = readRepoText('README.md')
    const koreanReadme = readRepoText('README.ko.md')
    const license = readRepoText('LICENSE')
    const packageJson = JSON.parse(readRepoText('package.json')) as { license?: string }

    expect(license).toContain("derived from Anthropic's Claude Code CLI")
    expect(license).toContain('modifications only')
    expect(packageJson.license).toBe('SEE LICENSE FILE')

    expect(readme).toContain("derived from Anthropic's Claude Code CLI")
    expect(readme).toContain('modifications are offered under MIT where legally permissible')
    expect(readme).toContain('not a blanket MIT license over the derived runtime')
    expect(readme).not.toContain('license-MIT')

    expect(koreanReadme).toContain('Anthropic Claude Code CLI')
    expect(koreanReadme).toContain('수정분은 법적으로 가능한 범위에서 MIT')
    expect(koreanReadme).toContain('전체 파생 런타임에 대한 단순 MIT 라이선스가 아닙니다')
  })

  test('extension package metadata does not advertise stale origin or blanket MIT licensing', () => {
    const manifestPaths = [
      'packages/openclaude-vscode/package.json',
      'vscode-extension/openclaude-vscode/package.json',
    ]

    for (const manifestPath of manifestPaths) {
      const manifest = JSON.parse(readRepoText(manifestPath)) as {
        license?: string
        repository?: { url?: string } | string
      }
      const repositoryUrl = typeof manifest.repository === 'string'
        ? manifest.repository
        : manifest.repository?.url ?? ''

      expect(manifest.license, manifestPath).toBe('SEE LICENSE FILE')
      expect(repositoryUrl, manifestPath).not.toContain('Gitlawb/openclaude')
      if (repositoryUrl.length > 0) {
        expect(repositoryUrl, manifestPath).toContain('svy04/metaforge')
      }
    }
  })

  test('source license inventory covers the legacy extension surface', () => {
    const report = JSON.parse(readRepoText('docs/product-quality/source-license-metadata-quality-report.json')) as {
      scanRoots?: string[]
      sourceLicenseRecords?: Array<{ path?: string }>
    }

    expect(report.scanRoots).toContain('vscode-extension/openclaude-vscode')
    expect(report.sourceLicenseRecords?.some((record) => record.path === 'vscode-extension/openclaude-vscode/package.json')).toBe(true)
  })
})
