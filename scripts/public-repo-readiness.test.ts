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
    'ANDROID_INSTALL.md',
    'PLAYBOOK.md',
    'docs/quick-start-windows.md',
    'docs/quick-start-mac-linux.md',
    'docs/advanced-setup.md',
    'docs/litellm-setup.md',
  ]
  return Object.fromEntries(paths.map((path) => [path, readRepoText(path)]))
}

function listFilesUnder(relativePath: string): string[] {
  return trackedRepoPaths(root).filter((path) => path.startsWith(`${relativePath}/`))
}

describe('public repository readiness surfaces', () => {
  test('AGENTS.md is public-facing guidance, not a private memory dump', () => {
    const agents = readRepoText('AGENTS.md')
    const lineCount = agents.split(/\r?\n/).length
    const bulletCount = agents.split(/\r?\n/).filter((line) => /^\s*[-*]\s+/.test(line)).length
    const directiveWordCount = agents.match(/\bmust\b|\bMUST\b|해야|하지 마|Do not|Never/g)?.length ?? 0

    expect(lineCount).toBeLessThanOrEqual(110)
    expect(bulletCount).toBeLessThanOrEqual(35)
    expect(directiveWordCount).toBeLessThanOrEqual(12)
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
    const koreanReadme = readRepoText('README.ko.md')
    const gitignore = readRepoText('.gitignore')
    const orchestraFiles = listFilesUnder('src/services/orchestra')
    const orchestraRuntimeFiles = orchestraFiles.filter((path) => path.endsWith('.ts') && !path.endsWith('.test.ts'))
    const orchestraTestFiles = orchestraFiles.filter((path) => path.endsWith('.test.ts'))
    const metaMfhDocs = [
      'docs/MFH_META_SYNTHESIS.md',
      'docs/GOAL_SCHEMA.md',
      'docs/EVALS.md',
      'docs/SECURITY_AND_GUARDRAILS.md',
    ]
    const avfDocs = [
      'docs/avf/WEB_FIRST_AUTONOMOUS_VENTURE_FACTORY_SPEC.md',
      'avf/influence_factory/operator_runs.md',
    ]

    expect(readme).toContain('Orchestra is the runtime-wired layer in this package today')
    expect(readme).toContain('Meta and MFH are governance, schema, and evidence-gate surfaces')
    expect(readme).toContain('AVF Influence Factory is a repo-local manual artifact lane')
    expect(readme).not.toContain('Meta, MFH, and AVF are runtime-wired modules')
    expect(koreanReadme).toMatch(/Orchestra는 현재 이 package에서 runtime-wired layer입니다/)
    expect(koreanReadme).toMatch(/Meta와 MFH는\s+governance, schema, evidence-gate surface입니다/)
    expect(koreanReadme).toMatch(/AVF Influence Factory는\s+repo-local manual artifact lane입니다/)
    expect(koreanReadme).not.toContain('Meta, MFH, AVF가 모두 runtime-wired module입니다')
    expect(orchestraRuntimeFiles.length).toBeGreaterThan(0)
    expect(orchestraTestFiles.length).toBeGreaterThan(0)
    for (const path of metaMfhDocs) {
      expect(existsSync(join(root, path)), path).toBe(true)
    }
    for (const path of avfDocs) {
      expect(existsSync(join(root, path)), path).toBe(true)
    }
    expect(gitignore).toContain('avf/influence_factory/operator_package_v*/')
    expect(gitignore).toContain('avf/influence_factory/owner_goal_runs/')
    expect(gitignore).toContain('avf/influence_factory/active/')
  })

  test('generated AVF operator runs are not tracked in the public checkout', () => {
    const generatedAvfRuns = trackedRepoPaths(root).filter((path) =>
      path.startsWith('avf/influence_factory/owner_goal_runs/')
      || path.startsWith('avf/influence_factory/active/')
      || /^avf\/influence_factory\/operator_package_v\d+\//.test(path),
    )

    expect(generatedAvfRuns).toEqual([])
  })

  test('public setup docs do not pin stale OpenAI model examples', () => {
    const docs = readPublicSetupDocs()

    for (const [path, text] of Object.entries(docs)) {
      expect(text, path).not.toMatch(/\bgpt-4o\b/i)
      expect(text, path).not.toMatch(/\bsk-\.\.\./i)
      expect(text, path).not.toMatch(/\byour[_-]?[a-z0-9_-]*key[a-z0-9_-]*\b/i)
      expect(text, path).not.toMatch(/\bqwen\/qwen3\.6-plus-preview:free\b/i)
      expect(text, path).not.toMatch(/\bqwen2\.5-coder\b/i)
      expect(text, path).not.toMatch(/\bllama3\.3:70b\b/i)
      expect(text, path).not.toMatch(/\bclaude-sonnet-4-5-20250929\b/i)
      expect(text, path).not.toMatch(/~\/\.codex\/auth\.json/i)
      expect(text, path).not.toMatch(/\b(?:current[-\s]?best|best[-\s]?(?:available\s+)?(?:provider|model|benchmark)|recommended\s+(?:free\s+)?(?:provider|model|benchmark))\b/i)
    }

    expect(docs['README.md']).toContain('<current-openai-tool-model>')
    expect(docs['README.md']).toContain('<local-ollama-model>')
    expect(docs['docs/quick-start-windows.md']).toContain('<current-openai-tool-model>')
    expect(docs['docs/quick-start-mac-linux.md']).toContain('<current-openai-tool-model>')
    expect(docs['docs/advanced-setup.md']).toContain('<current-openai-tool-model>')
    expect(docs['docs/litellm-setup.md']).toContain('openai-tool-model')
    expect(docs['docs/litellm-setup.md']).toContain('<current-anthropic-tool-model>')
    expect(docs['PLAYBOOK.md']).toContain('<current-openai-tool-model>')
    expect(docs['PLAYBOOK.md']).toContain('<local-ollama-model>')
  })

  test('runtime diagnostics do not recommend pinned local model examples', () => {
    const runtimeHintDocs = {
      'scripts/system-check.ts': readRepoText('scripts/system-check.ts'),
      'scripts/provider-recommend.ts': readRepoText('scripts/provider-recommend.ts'),
    }

    for (const [path, text] of Object.entries(runtimeHintDocs)) {
      expect(text, path).toContain('<local-ollama-model>')
      expect(text, path).not.toMatch(/\bqwen2\.5-coder\b/i)
      expect(text, path).not.toMatch(/\bllama3\.3:70b\b/i)
    }
  })

  test('Android install notes stay legacy-bounded and avoid unsupported superiority claims', () => {
    const androidInstall = readRepoText('ANDROID_INSTALL.md')
    const publicClaimBoundary = readRepoText('scripts/product-public-claim-boundary.ts')

    expect(publicClaimBoundary).toContain("'ANDROID_INSTALL.md'")
    expect(androidInstall).toContain('Legacy OpenClaude Android Notes')
    expect(androidInstall).toMatch(/not a Metaforge release or\s+support claim/)
    expect(androidInstall).not.toMatch(/\b(best|beats?|outperforms?)\b/i)
    expect(androidInstall).not.toMatch(/\bas of (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b/i)
  })

  test('public planning docs do not point readers at private source workspaces', () => {
    const docs = [
      'docs/RESEARCH_PIPELINE.md',
      'docs/PROGRESS_LOG.md',
      'docs/DECISION_LOG.md',
    ]

    for (const path of docs) {
      const text = readRepoText(path)
      expect(text, path).not.toContain('<private-workspace>')
      expect(text, path).not.toMatch(/\bmeta\/CLAUDE\.md\b|\bmfh\/\.mfh\/spec\.md\b/i)
    }
  })

  test('profile refresh evidence does not expose private workbench repo breadcrumbs', () => {
    const evidence = readRepoText('docs/profile/github-profile-refresh-evidence-2026-06-14.md')
    const forbiddenEvidence = [
      'mimesis-plugin',
      'mimesis-source-packet',
      'harness-meta',
      'https://github.com/svy04/mimesis-plugin.git',
      'https://github.com/svy04/mimesis-source-packet.git',
      'dirty working tree',
      'untracked hero preview files',
    ]

    expect(evidence).toContain('private workbench repos were checked locally and are not public proof')
    for (const marker of forbiddenEvidence) {
      expect(evidence, marker).not.toContain(marker)
    }
  })

  test('legacy VS Code extension README points to the canonical Metaforge extension surface', () => {
    const legacyReadme = readRepoText('vscode-extension/openclaude-vscode/README.md')

    expect(legacyReadme).toContain('Legacy Extension Surface')
    expect(legacyReadme).toContain('packages/openclaude-vscode')
    expect(legacyReadme).toContain('Metaforge')
    expect(legacyReadme).not.toMatch(/^# OpenClaude VS Code Extension/m)
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

  test('README states public history boundary without adoption overclaims', () => {
    const readme = readRepoText('README.md')
    const koreanReadme = readRepoText('README.ko.md')
    const forbiddenEnglishHistoryOverclaims = [
      /\bwidely adopted\b/i,
      /\b(?:is|was|has been)\s+externally validated\b/i,
      /\b(?:is|was|has been)\s+production ready\b/i,
      /\bstar history proves\b/i,
      /\bstars prove\b/i,
    ]
    const forbiddenKoreanHistoryOverclaims = [
      /널리\s*채택/,
      /외부\s*검증\s*완료/,
      /프로덕션\s*준비\s*완료/,
      /스타가\s*증명/,
    ]

    expect(readme).toContain('Public history boundary')
    expect(readme).toContain('private/local workbench')
    expect(readme).toContain('public checkout')
    expect(readme).toContain('not adoption evidence, external validation, or production readiness')
    expect(koreanReadme).toContain('공개 히스토리 경계')
    expect(koreanReadme).toContain('프라이빗/로컬 workbench')
    expect(koreanReadme).toContain('공개 checkout')
    expect(koreanReadme).toContain('채택, 외부 검증, production readiness 증거가 아닙니다')

    for (const pattern of forbiddenEnglishHistoryOverclaims) {
      expect(readme, String(pattern)).not.toMatch(pattern)
    }
    for (const pattern of forbiddenKoreanHistoryOverclaims) {
      expect(koreanReadme, String(pattern)).not.toMatch(pattern)
    }
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
