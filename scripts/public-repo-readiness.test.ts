import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { existsSync, mkdtempSync, rmSync, readFileSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const root = join(__dirname, '..')

function readRepoText(path: string): string {
  return readFileSync(join(root, path), 'utf8')
}

function readPackageScripts(): Record<string, string> {
  const packageJson = JSON.parse(readRepoText('package.json')) as {
    scripts?: Record<string, string>
  }
  return packageJson.scripts ?? {}
}

function privateLocalPathNeedles(): string[] {
  return [
    `C:${'\\\\'}Users`,
    `C:${'/'}Users`,
    `/Users${'/'}`,
  ]
}

function privateLocalPathNeedleFunctionBody(relativePath: string): string {
  const match = readRepoText(relativePath).match(/function privateLocalPathNeedles\(\): string\[\] \{([\s\S]*?)\n\}/)
  expect(match).not.toBeNull()
  return match?.[1] ?? ''
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
    'docs/non-technical-setup.md',
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
  test('private-path sentinels stay generic instead of embedding local folder names', () => {
    const sentinelBodies = [
      privateLocalPathNeedleFunctionBody('scripts/product-agent-instructions-quality.ts'),
      privateLocalPathNeedleFunctionBody('scripts/public-repo-readiness.test.ts'),
    ].join('\n')

    expect(sentinelBodies).toContain('Users')
    expect(sentinelBodies).not.toMatch(/\p{Script=Hangul}/u)
  })

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

  test('public feedback docs preserve latest community signals without raw private breadcrumbs', () => {
    const snapshot = readRepoText('docs/product-quality/public-feedback-snapshot-2026-06-15.md')
    const triage = readRepoText('docs/product-quality/public-feedback-triage-2026-06-15.md')
    const latestSnapshot = readRepoText('docs/product-quality/public-feedback-snapshot-2026-06-19.md')
    const latestTriage = readRepoText('docs/product-quality/public-feedback-triage-2026-06-19.md')
    const combined = `${snapshot}\n${triage}\n${latestSnapshot}\n${latestTriage}`

    expect(combined).toContain('2026-06-18 Restated Feedback Packet')
    expect(combined).toContain('The same community thread was restated as an active operating input')
    expect(combined).toContain('Provenance is a trust surface')
    expect(combined).toContain('fork/adaptation questions should be')
    expect(combined).toContain('private-to-public transition')
    expect(combined).toContain('OpenClaude runtime substrate')
    expect(combined).toMatch(/behavioral happy paths, edge cases,[\s\S]*side-effect (?:guards|checks)/)
    expect(combined).toContain('Knip')
    expect(combined).toContain('fallow')
    expect(combined).toContain('dependency-cruiser')
    expect(combined).toContain('jscpd')
    expect(combined).toContain('Korean docs')
    expect(combined).not.toContain('갤로그')
    for (const needle of privateLocalPathNeedles()) {
      expect(combined).not.toContain(needle)
    }
  })

  test('README surfaces the public feedback response without upgrading claims', () => {
    const readme = readRepoText('README.md')
    const koreanReadme = readRepoText('README.ko.md')

    expect(readme).toContain('## Public Feedback Response')
    expect(readme).toContain('2026-06-19 snapshot')
    expect(readme).toContain('provenance and fork/adaptation boundaries')
    expect(readme).toContain('OpenClaude remains the runtime substrate')
    expect(readme).toContain('behavioral happy paths, edge cases, and side-effect guards')
    expect(readme).toContain('Knip, dependency-cruiser, and jscpd are wired')
    expect(readme).toContain('fallow and Lumin Repo Lens remain optional/manual backlog inputs')
    expect(readme).toContain('none of these gates prove cleanup completion')
    expect(readme).toContain('Static analysis evidence:')
    expect(readme).toContain('[Knip dead-export candidates](docs/product-quality/dead-export-candidates-report.md)')
    expect(readme).toContain('[dependency-cruiser topology ratchet](docs/product-quality/dependency-topology-report.md)')
    expect(readme).toContain('[jscpd product-script clone ratchet](docs/product-quality/script-duplication-audit-report.md)')
    expect(readme).toContain('[architecture map](docs/product-quality/metaforge-architecture-map.md#static-analysis-trust-stack)')
    expect(readme).toContain('[CG-002 static-analysis goal](docs/goals/CG-002-static-analysis-ratchet.md)')
    expect(readme).toContain('[evidence manifest](docs/product-quality/product-evidence-manifest.md)')
    expect(readme).toContain('candidate/baseline/ratchet evidence only')
    expect(readme).toContain('not cleanup completion, topology-clean, refactor-completion, public-readiness, or external-validation proof')
    expect(readme).toContain('Korean docs stay current')
    expect(readme).toContain('not applause or validation')
    expect(readme).not.toContain('external validation from reviewers')

    expect(koreanReadme).toContain('## 공개 피드백 응답')
    expect(koreanReadme).toContain('칭찬이나 외부 검증이 아니라 제품 입력')
    expect(koreanReadme).toContain('OpenClaude는 runtime substrate')
    expect(koreanReadme).toContain('Metaforge = Meta + MFH + Orchestra OS')
    expect(koreanReadme).toContain('behavioral happy path, edge case, side-effect guard')
    expect(koreanReadme).toContain('Knip, dependency-cruiser, jscpd는 현재 local no-provider product-quality gate')
    expect(koreanReadme).toContain('Fallow와 Lumin Repo Lens는 여전히 선택적/manual backlog input')
    expect(koreanReadme).toContain('정적 분석 증거:')
    expect(koreanReadme).toContain('[Knip dead-export 후보](docs/product-quality/dead-export-candidates-report.md)')
    expect(koreanReadme).toContain('[dependency-cruiser topology ratchet](docs/product-quality/dependency-topology-report.md)')
    expect(koreanReadme).toContain('[jscpd product-script clone ratchet](docs/product-quality/script-duplication-audit-report.md)')
    expect(koreanReadme).toContain('[architecture map](docs/product-quality/metaforge-architecture-map.md#static-analysis-trust-stack)')
    expect(koreanReadme).toContain('[CG-002 static-analysis goal](docs/goals/CG-002-static-analysis-ratchet.md)')
    expect(koreanReadme).toContain('[evidence manifest](docs/product-quality/product-evidence-manifest.md)')
    expect(koreanReadme).toContain('candidate/baseline/ratchet 증거')
    expect(koreanReadme).toContain('cleanup 완료, topology clean, refactor 완료, public readiness, external validation을 증명하지 않습니다')
  })

  test('OpenSSF Scorecard workflow is source-controlled but claim-bounded', () => {
    const workflowPath = '.github/workflows/scorecard.yml'
    expect(existsSync(join(root, workflowPath))).toBe(true)

    const workflow = readRepoText(workflowPath)
    const postureGate = readRepoText('scripts/product-openssf-security-posture.ts')

    expect(workflow).toContain('name: OpenSSF Scorecard')
    expect(workflow).toContain('ossf/scorecard-action@4eaacf0543bb3f2c246792bd56e8cdeffafb205a # v2.4.3')
    expect(workflow).toContain('results_file: results.sarif')
    expect(workflow).toContain('results_format: sarif')
    expect(workflow).toContain('publish_results: true')
    expect(workflow).toMatch(/^permissions:\s*\r?\n[^\S\r\n]+contents:\s+read\s*$/m)
    expect(workflow).not.toMatch(/^permissions:\s*\r?\n(?:[^\S\r\n]+[^\r\n]+\r?\n)*[^\S\r\n]+(security-events|id-token|contents):\s+write\s*$/m)
    expect(workflow).toMatch(/scorecard:\s*\r?\n(?:[^\S\r\n]+[^\r\n]*\r?\n)*[^\S\r\n]+permissions:\s*\r?\n[^\S\r\n]+contents:\s+read\s*\r?\n[^\S\r\n]+security-events:\s+write\s*\r?\n[^\S\r\n]+id-token:\s+write/)
    expect(workflow).not.toMatch(/^env:\s*$/m)
    expect(workflow).not.toMatch(/^\s*defaults:\s*$/m)
    expect(workflow).not.toContain('pull_request_target')

    expect(postureGate).toContain("scorecardWorkflowPath = '.github/workflows/scorecard.yml'")
    expect(postureGate).toContain('scorecardWorkflowPresent')
    expect(postureGate).toContain('scorecardWorkflowActionsPinned')
    expect(postureGate).toContain('scorecardWorkflowPublishRestrictionsCompliant')
    expect(postureGate).toContain('scorecardHostedExecutionPerformed: false')
    expect(postureGate).toContain('scorecardExternalClaimAllowed: false')
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

  test('product quality uses public artifact hygiene as a check gate, not an auto-fixer', () => {
    const scripts = readPackageScripts()

    expect(scripts['product:public-artifact-hygiene:write']).toContain('--write')
    expect(scripts['product:quality']).not.toContain('product:public-artifact-hygiene:write')
    expect(scripts['product:quality']).toContain('bun run verify:privacy')
    expect(scripts['verify:privacy']).toContain('bun run product:public-artifact-hygiene')
    expect(scripts['verify:privacy']).not.toContain('product:public-artifact-hygiene:write')
  })

  test('tracked public paths stay portable for default Windows checkouts', () => {
    const longPaths = trackedRepoPaths(root).filter((path) => path.length > 240)

    expect(longPaths).toEqual([])
  })

  test('tracked product-quality docs do not expose historical live trace paths or task ids', () => {
    const trackedProductQualityDocs = trackedRepoPaths(root)
      .filter((path) => path.startsWith('docs/product-quality/'))
      .filter((path) => /\.(?:json|jsonl|md|txt|ya?ml)$/.test(path))
    const forbiddenMarkers = [
      'reports/orchestra-live',
      'openclaude.trace.reports_orchestra-live',
    ]
    const offenders = trackedProductQualityDocs.flatMap((path) => {
      const text = readRepoText(path)
      return forbiddenMarkers
        .filter((marker) => text.includes(marker))
        .map((marker) => `${path}: ${marker}`)
    })

    expect(offenders).toEqual([])
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

  test('OpenSSF posture evidence does not carry stale Git-root wording', () => {
    const staleGitRootWording = 'this workspace is not currently a Git repository root'
    const surfaces = [
      'scripts/product-openssf-security-posture.ts',
      'docs/product-quality/openssf-security-posture-report.md',
      'docs/product-quality/openssf-security-posture-report.json',
    ].map((path) => readRepoText(path))

    for (const surface of surfaces) {
      expect(surface).not.toContain(staleGitRootWording)
    }
  })

  test('issue templates keep Metaforge as the public thesis', () => {
    const bugReport = readRepoText('.github/ISSUE_TEMPLATE/bug_report.md')
    const featureRequest = readRepoText('.github/ISSUE_TEMPLATE/feature_request.md')

    expect(bugReport).toContain('Metaforge or its OpenClaude runtime substrate')
    expect(bugReport).toContain('Metaforge commit or OpenClaude runtime version')
    expect(bugReport).not.toContain('Report a reproducible problem in OpenClaude')
    expect(featureRequest).toContain('Metaforge, Meta/MFH/Orchestra OS, or its OpenClaude runtime substrate')
    expect(featureRequest).toContain('What would you like Metaforge to do?')
    expect(featureRequest).not.toContain('What would you like OpenClaude to do?')
  })

  test('README states runtime wiring honestly', () => {
    const readme = readRepoText('README.md')
    const koreanReadme = readRepoText('README.ko.md')
    const proofPack = readRepoText('docs/marketing/metaforge-public-proof-pack-2026-06-18.md')
    const architectureMap = readRepoText('docs/product-quality/metaforge-architecture-map.md')
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
    expect(readme).toContain('[Architecture Map](docs/product-quality/metaforge-architecture-map.md)')
    expect(readme).toContain('Meta and MFH are governance, schema, and evidence-gate surfaces')
    expect(readme).toContain('AVF Influence Factory is a repo-local manual artifact lane')
    expect(readme).toContain('| Symbol | Public role | Evidence class | Runtime boundary |')
    expect(readme).toContain('| Orchestra |')
    expect(readme).toContain('runtime-wired import path')
    expect(readme).toContain('`src/services/orchestra/`')
    expect(readme).toContain('| Meta/MFH |')
    expect(readme).toContain('governance/docs/gates')
    expect(readme).toContain('| Mimesis Engineering |')
    expect(readme).toContain('source-ledger loop, not a default runtime module')
    expect(readme).toContain('| AVF Influence Factory |')
    expect(readme).toContain('manual artifact lane, not a default CLI runtime import')
    expect(readme).not.toContain('Meta, MFH, and AVF are runtime-wired modules')
    expect(koreanReadme).toMatch(/Orchestra는 현재 이 package에서 runtime-wired layer입니다/)
    expect(koreanReadme).toContain('[Architecture Map](docs/product-quality/metaforge-architecture-map.md)')
    expect(koreanReadme).toMatch(/Meta와 MFH는\s+governance, schema, evidence-gate surface입니다/)
    expect(koreanReadme).toMatch(/AVF Influence Factory는\s+repo-local manual artifact lane입니다/)
    expect(koreanReadme).toContain('| 심볼 | 공개 역할 | 증거 등급 | 런타임 경계 |')
    expect(koreanReadme).toContain('| Orchestra |')
    expect(koreanReadme).toContain('runtime-wired import path')
    expect(koreanReadme).toContain('`src/services/orchestra/`')
    expect(koreanReadme).toContain('| Meta/MFH |')
    expect(koreanReadme).toContain('governance/docs/gates')
    expect(koreanReadme).toContain('| Mimesis Engineering |')
    expect(koreanReadme).toContain('source-ledger loop이며 기본 runtime module이 아닙니다')
    expect(koreanReadme).toContain('| AVF Influence Factory |')
    expect(koreanReadme).toContain('manual artifact lane이며 기본 CLI runtime import가 아닙니다')
    expect(koreanReadme).not.toContain('Meta, MFH, AVF가 모두 runtime-wired module입니다')
    expect(proofPack).toContain('## Wiring Evidence Map')
    expect(proofPack).toContain('| Surface | Evidence class | Public wording allowed | Boundary |')
    expect(proofPack).toContain('Runtime import')
    expect(proofPack).toContain('Governance/docs/gates')
    expect(proofPack).toContain('Local no-provider proof boundary')
    expect(proofPack).toContain('Manual artifact lane')
    expect(architectureMap).toContain('# Metaforge Architecture Map')
    expect(architectureMap).toContain('```mermaid')
    expect(architectureMap).toContain('flowchart TD')
    expect(architectureMap).toContain('Meta + MFH + Orchestra OS')
    expect(architectureMap).toContain('OpenClaude runtime substrate')
    expect(architectureMap).toContain('runtime-wired import path')
    expect(architectureMap).toContain('CandidateBoundary["Candidate/baseline/ratchet only')
    expect(architectureMap).toContain('candidate_file_count: `637`')
    expect(architectureMap).toContain('candidate_unused_export_count: `1396`')
    expect(architectureMap).toContain('triage_record_count: `4`')
    expect(architectureMap).toContain('module_count: `2630`')
    expect(architectureMap).toContain('dependency_edge_count: `11984`')
    expect(architectureMap).toContain('circular_dependency_baseline: `1737`')
    expect(architectureMap).toContain('unresolved_dependency_baseline: `863`')
    expect(architectureMap).toContain('jscpd_clone_count: `17`')
    expect(architectureMap).toContain('jscpd_duplicated_lines: `439`')
    expect(architectureMap).toContain('jscpd_duplicated_tokens: `2979`')
    expect(architectureMap).toContain('not clean-architecture proof')
    expect(architectureMap).toContain('not production readiness')
    expect(architectureMap).toContain('docs/product-quality/public-claim-boundary-report.md')
    expect(architectureMap).toContain('docs/product-quality/dependency-topology-report.md')
    expect(architectureMap).toContain('docs/product-quality/script-duplication-audit-report.md')
    expect(architectureMap).toContain('docs/product-quality/dead-export-candidates-report.md')
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

  test('public setup docs avoid current-model recency claims', () => {
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
      expect(text, path).not.toMatch(/<current-[^>\n]*model>/i)
      expect(text, path).not.toMatch(/\bcurrent\s+(?:OpenAI|Anthropic|Mistral)\s+model\b/i)
      expect(text, path).not.toMatch(/\b[a-z0-9][a-z0-9.-]*-latest\b/i)
    }

    expect(docs['README.md']).toContain('<openai-tool-model-id>')
    expect(docs['README.md']).toContain('<local-ollama-model>')
    expect(docs['docs/quick-start-windows.md']).toContain('<openai-tool-model-id>')
    expect(docs['docs/quick-start-mac-linux.md']).toContain('<openai-tool-model-id>')
    expect(docs['docs/advanced-setup.md']).toContain('<openai-tool-model-id>')
    expect(docs['docs/litellm-setup.md']).toContain('openai-tool-model')
    expect(docs['docs/litellm-setup.md']).toContain('<anthropic-tool-model-id>')
    expect(docs['docs/advanced-setup.md']).toContain('<mistral-tool-model-id>')
    expect(docs['PLAYBOOK.md']).toContain('<openai-tool-model-id>')
    expect(docs['PLAYBOOK.md']).toContain('<local-ollama-model>')
  })

  test('public setup docs keep Metaforge as product thesis and OpenClaude as runtime substrate', () => {
    const docs = readPublicSetupDocs()
    const setupPaths = [
      'docs/non-technical-setup.md',
      'docs/quick-start-windows.md',
      'docs/quick-start-mac-linux.md',
    ]

    for (const path of setupPaths) {
      expect(docs[path], path).toContain('Metaforge')
      expect(docs[path], path).toMatch(/OpenClaude[\s\S]*runtime\s+substrate|runtime\s+substrate[\s\S]*OpenClaude/i)
      expect(docs[path], path).not.toContain('## What OpenClaude Does')
    }

    const scorecard = readRepoText('docs/product-quality/competitive-scorecard.md')
    expect(scorecard).toContain('# Metaforge Competitive Evidence Scorecard')
    expect(scorecard).toContain('OpenClaude is the runtime substrate')
    expect(scorecard).not.toContain('## OpenClaude Product Thesis')
  })

  test('product-quality evidence docs keep Metaforge as product layer over OpenClaude substrate', () => {
    const evidenceDocs = {
      'docs/product-quality/primary-source-learning-loop.md': readRepoText('docs/product-quality/primary-source-learning-loop.md'),
      'docs/product-quality/product-evidence-manifest.md': readRepoText('docs/product-quality/product-evidence-manifest.md'),
      'docs/product-quality/benchmark-readiness-matrix.md': readRepoText('docs/product-quality/benchmark-readiness-matrix.md'),
    }
    const evidenceGenerators = {
      'scripts/product-evidence-manifest.ts': readRepoText('scripts/product-evidence-manifest.ts'),
      'scripts/product-benchmark-readiness-matrix.ts': readRepoText('scripts/product-benchmark-readiness-matrix.ts'),
    }
    const forbiddenDrift = [
      'OpenClaude must keep improving',
      'whether OpenClaude should',
      'proves OpenClaude is learning',
      'OpenClaude product-quality evidence',
      'local OpenClaude product-quality evidence',
    ]

    for (const [path, text] of Object.entries({ ...evidenceDocs, ...evidenceGenerators })) {
      expect(text, path).toContain('Metaforge')
      for (const marker of forbiddenDrift) {
        expect(text, `${path}: ${marker}`).not.toContain(marker)
      }
    }

    expect(evidenceDocs['docs/product-quality/primary-source-learning-loop.md']).toContain('OpenClaude runtime substrate')
    expect(evidenceDocs['docs/product-quality/product-evidence-manifest.md']).toContain('Metaforge product-quality evidence over the OpenClaude runtime substrate')
    expect(evidenceDocs['docs/product-quality/benchmark-readiness-matrix.md']).toContain('Metaforge product-quality evidence over the OpenClaude runtime substrate')
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

  test('public Mimesis docs use neutral private-workbench labels', () => {
    const concretePrivateRepoNames = [
      `mimesis-${'plugin'}`,
      `mimesis-${'source'}-${'packet'}`,
    ]
    const docs = [
      'docs/MIMESIS_ENGINEERING.md',
      'docs/product-quality/public-feedback-snapshot-2026-06-19.md',
      'docs/product-quality/public-feedback-triage-2026-06-19.md',
    ]

    for (const path of docs) {
      const text = readRepoText(path)
      for (const name of concretePrivateRepoNames) {
        expect(text, path).not.toContain(name)
      }
    }
  })

  test('scanner-unfriendly dummy key literals stay split or neutralized', () => {
    const secretPrefix = 's' + 'k-'
    const quoteGroup = "(['\"`])"
    const dummySecretLiteralPattern = new RegExp(
      `${quoteGroup}${secretPrefix}(?:secret|openai|test|persisted|live|legacy|moonshot|ant(?:-(?:key|test|x))?)[A-Za-z0-9_-]*\\1`,
      'i',
    )
    const scannedPublicSourcePaths = trackedRepoPaths(root).filter((path) => {
      if (path === 'src/utils/settings/types.ts') {
        return true
      }
      if (!(path.startsWith('src/') || path.startsWith('scripts/'))) {
        return false
      }
      if (!/\.(?:test|spec)\.(?:ts|tsx|js|jsx)$/.test(path)) {
        return false
      }
      return path !== 'scripts/public-repo-readiness.test.ts'
    })

    expect(scannedPublicSourcePaths).toContain('src/utils/settings/types.ts')
    for (const path of scannedPublicSourcePaths) {
      expect(readRepoText(path), path).not.toMatch(dummySecretLiteralPattern)
    }
  })

  test('public operating docs do not cite removed planning artifacts as current authority', () => {
    const trackedPlanningArtifacts = trackedRepoPaths(root).filter((path) => path.startsWith('.planning/'))
    const docs = [
      'docs/DECISION_LOG.md',
      'docs/PROJECT_SPEC.md',
      'docs/EVALS.md',
    ]

    expect(trackedPlanningArtifacts).toEqual([])
    for (const path of docs) {
      const text = readRepoText(path)
      expect(text, path).not.toMatch(/\.planning\/(?:PROJECT|ROADMAP|phase-)/)
    }
  })

  test('profile refresh evidence does not expose non-public artifact repo breadcrumbs', () => {
    const evidence = [
      readRepoText('docs/profile/github-profile-refresh-evidence-2026-06-14.md'),
      readRepoText('docs/profile/github-profile-refresh-evidence-2026-06-19.md'),
    ].join('\n')
    const forbiddenEvidence = [
      `mimesis-${'plugin'}`,
      `mimesis-${'source'}-${'packet'}`,
      'harness-meta',
      `https://github.com/svy04/mimesis-${'plugin'}.git`,
      `https://github.com/svy04/mimesis-${'source'}-${'packet'}.git`,
      'dirty working tree',
      'untracked hero preview files',
    ]

    expect(evidence).toContain('non-public artifact repos were checked locally and are not public proof')
    expect(evidence).toContain('This packet proves a profile README and proof-surface maintenance update only')
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
    expect(readme).toContain('pre-public work outside this checkout')
    expect(readme).toContain('current public repository')
    expect(readme).toContain('not adoption evidence, external validation, or production readiness')
    expect(koreanReadme).toContain('공개 히스토리 경계')
    expect(koreanReadme).toContain('checkout 밖의 공개 전 작업 이력')
    expect(koreanReadme).toContain('현재 공개')
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
