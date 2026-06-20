import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { existsSync, readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'

import {
  markdownCell,
  publicClaimEvidenceMap,
  publicSurfacePaths,
  scanClaimText,
} from './product-public-claim-boundary'

const root = join(__dirname, '..')
const scriptPath = join(__dirname, 'product-public-claim-boundary.ts')
const generatedEvidencePaths = [
  'docs/product-quality/public-claim-boundary-report.json',
  'docs/product-quality/public-claim-boundary-report.md',
  'reports/metaforge-public-claim-boundary.jsonl',
]

function readOptionalEvidence(path: string) {
  const absolutePath = join(root, path)

  if (!existsSync(absolutePath)) {
    return { exists: false, content: '' }
  }

  return { exists: true, content: readFileSync(absolutePath, 'utf8') }
}

describe('product public claim boundary classifier', () => {
  test('maps each public Metaforge symbol to evidence, non-claims, and unresolved gaps', () => {
    expect(publicClaimEvidenceMap.map((row) => row.symbol)).toEqual([
      'Meta',
      'MFH',
      'Orchestra',
      'OpenClaude runtime',
      'Mimesis Engineering',
      'AVF Influence Factory',
    ])

    for (const row of publicClaimEvidenceMap) {
      expect(row.evidenceClass.length).toBeGreaterThan(0)
      expect(row.evidencePaths.length).toBeGreaterThan(0)
      expect(row.allowedClaim.length).toBeGreaterThan(0)
      expect(row.nonClaims.every((item) => /\bnot\b|does not/i.test(item))).toBe(true)
      expect(row.unresolvedGap.length).toBeGreaterThan(0)
    }
  })

  test('uses source-controlled evidence paths in the public claim evidence map', () => {
    const trackedFiles = new Set(
      spawnSync('git', ['ls-files'], { cwd: root, encoding: 'utf8', shell: false })
        .stdout
        .trim()
        .split(/\r?\n/)
        .filter(Boolean),
    )

    for (const row of publicClaimEvidenceMap) {
      for (const path of row.evidencePaths) {
        const isTrackedFile = trackedFiles.has(path)
        const isTrackedDirectory = [...trackedFiles].some((trackedPath) => trackedPath.startsWith(`${path}/`))
        expect(isTrackedFile || isTrackedDirectory, `${row.symbol} evidence path is not source-controlled: ${path}`).toBe(true)
      }
    }
  })

  test('keeps OpenClaude as runtime substrate while Metaforge symbols carry the thesis', () => {
    const bySymbol = Object.fromEntries(publicClaimEvidenceMap.map((row) => [row.symbol, row]))

    expect(bySymbol['OpenClaude runtime']?.publicRole).toContain('substrate')
    expect(bySymbol['OpenClaude runtime']?.allowedClaim).toContain('local CLI substrate')
    expect(bySymbol['OpenClaude runtime']?.nonClaims.join(' ')).toContain('not the product thesis')
    expect(bySymbol.Meta?.publicRole).toContain('operating memory')
    expect(bySymbol.MFH?.publicRole).toContain('evidence-gated')
    expect(bySymbol.Orchestra?.publicRole).toContain('routing')
    expect(bySymbol['AVF Influence Factory']?.nonClaims.join(' ')).toContain('not a default CLI runtime import')
  })

  test('binds MFH public claims to validated goal-trace evidence', () => {
    const mfh = publicClaimEvidenceMap.find((row) => row.symbol === 'MFH')

    expect(mfh?.evidenceClass).toContain('behavior')
    expect(mfh?.evidencePaths).toEqual(expect.arrayContaining([
      'docs/product-quality/goal-trace-validation-report.md',
      'docs/product-quality/goal-trace-validation-report.json',
      'docs/product-quality/real-session-trace-evals-report.md',
      'docs/product-quality/real-session-trace-evals-report.json',
      'docs/goals/traces/CG-001-goal-kernel-mvp.trace.json',
      'docs/goals/traces/CG-001-missing-evidence-rejected.trace.json',
      'docs/goals/traces/CG-001-protected-action-blocked.trace.json',
      'docs/goals/CG-002-static-analysis-ratchet.md',
      'docs/goals/traces/CG-002-static-analysis-ratchet.trace.json',
      'docs/product-quality/dead-export-candidates-report.md',
      'docs/product-quality/dependency-topology-report.md',
      'docs/product-quality/script-duplication-audit-report.md',
      'docs/product-quality/static-analysis-remediation-queue-report.md',
    ]))
    expect(mfh?.verificationCommand).toContain('goals:validate')
    expect(mfh?.verificationCommand).toContain('product:real-trace-evals')
    expect(mfh?.verificationCommand).toContain('product:dead-export-candidates')
    expect(mfh?.verificationCommand).toContain('product:dependency-topology')
    expect(mfh?.verificationCommand).toContain('product:script-duplication-audit')
    expect(mfh?.verificationCommand).toContain('product:static-analysis-remediation-queue')
    expect(mfh?.allowedClaim).toContain('representative cross-goal trace-validation evidence')
    expect(mfh?.allowedClaim).toContain('local runtime behavior triad evidence')
    expect(mfh?.allowedClaim).toContain('static-analysis ratchets')
    expect(mfh?.allowedClaim).toContain('static-analysis remediation queue')
    expect(mfh?.unresolvedGap).toContain('broader non-fixture behavior coverage')
    expect(mfh?.unresolvedGap).toContain('live-provider evidence')
    expect(mfh?.unresolvedGap).not.toContain('Runtime traces beyond docs-governance and static-analysis goals')
    expect(mfh?.unresolvedGap).not.toContain('representative traces')
  })

  test('check mode reports the MFH trace-evidence binding check', () => {
    const result = spawnSync('bun', [scriptPath, '--check'], {
      cwd: root,
      encoding: 'utf8',
      shell: false,
    })

    expect(result.stdout).toContain('MFH behavior evidence is bound to trace validation')
  })

  test('check mode reports the Orchestra production query-deps wiring check', () => {
    const result = spawnSync('bun', [scriptPath, '--check'], {
      cwd: root,
      encoding: 'utf8',
      shell: false,
    })

    expect(result.stdout).toContain('Orchestra production query deps wire real runtime services')
  })

  test('points English and Korean READMEs to the generated public claim evidence map', () => {
    const readme = readFileSync(join(root, 'README.md'), 'utf8')
    const koreanReadme = readFileSync(join(root, 'README.ko.md'), 'utf8')
    const generatedMapLink = 'docs/product-quality/public-claim-boundary-report.md#public-claim-evidence-map'

    expect(readme).toContain('Public claim evidence map')
    expect(readme).toContain(generatedMapLink)
    expect(koreanReadme).toContain('public claim evidence map')
    expect(koreanReadme).toContain(generatedMapLink)
  })

  test('includes AGENTS.md in public claim-boundary surfaces', () => {
    expect(publicSurfacePaths).toContain('AGENTS.md')
  })

  test('includes public goal artifacts in claim-boundary surfaces', () => {
    expect(publicSurfacePaths).toContain('docs/goals/INFLUENCE_FACTORY_PRODUCT_MVP_COMPLETION_AUDIT.md')
  })

  test('includes extension package manifests in public claim-boundary surfaces', () => {
    expect(publicSurfacePaths).toContain('packages/openclaude-vscode/package.json')
    expect(publicSurfacePaths).toContain('vscode-extension/openclaude-vscode/package.json')
  })

  test('includes generated public markdown reports while avoiding recursive self-report scans', () => {
    expect(publicSurfacePaths).toContain('docs/product-quality/community-profile-quality-report.md')
    expect(publicSurfacePaths).toContain('docs/product-quality/github-hosted-trust-posture-report.md')
    expect(publicSurfacePaths).toContain('docs/marketing/metaforge-public-proof-pack-2026-06-18.md')
    expect(publicSurfacePaths).toContain('docs/marketing/metaforge-public-proof-pack-2026-06-14.md')
    expect(publicSurfacePaths).toContain('docs/profile/github-profile-refresh-evidence-2026-06-20.md')
    expect(publicSurfacePaths).toContain('docs/profile/github-profile-refresh-evidence-2026-06-14.md')
    expect(publicSurfacePaths).toContain('docs/marketing/README.md')
    expect(publicSurfacePaths).not.toContain('docs/product-quality/public-claim-boundary-report.md')
    expect(publicSurfacePaths).not.toContain('docs/product-quality/product-evidence-manifest.md')
  })

  test('classifies unsupported public-readiness claims as unauthorized positives', () => {
    const findings = scanClaimText(
      'README.md',
      'Metaforge public readiness achieved with production readiness completed.\n',
    )

    expect(findings.map((finding) => finding.status)).toEqual(
      expect.arrayContaining([
        'unauthorized_positive_claim',
        'unauthorized_positive_claim',
      ]),
    )
    expect(findings.map((finding) => finding.category).sort()).toEqual([
      'production_readiness',
      'public_readiness',
    ])
  })

  test('classifies unsupported package manifest claims as unauthorized positives', () => {
    const manifestText = JSON.stringify(
      {
        description: 'OpenClaude extension package is production-ready and externally validated.',
      },
      null,
      2,
    )
    const findings = scanClaimText('packages/openclaude-vscode/package.json', manifestText)

    expect(findings.map((finding) => finding.status)).toEqual(
      expect.arrayContaining([
        'unauthorized_positive_claim',
        'unauthorized_positive_claim',
      ]),
    )
    expect(findings.map((finding) => finding.category).sort()).toEqual([
      'external_validation',
      'production_readiness',
    ])
  })

  test('classifies unbounded public goal artifact status as unauthorized', () => {
    const findings = scanClaimText(
      'docs/goals/example.md',
      [
        '# Example Completion Audit',
        '',
        'status: PROVEN',
      ].join('\n'),
    )

    expect(findings).toHaveLength(1)
    expect(findings[0]?.status).toBe('unauthorized_positive_claim')
    expect(findings[0]?.category).toBe('goal_artifact_status')
  })

  test('keeps public goal artifact status bounded when a top boundary is present', () => {
    const findings = scanClaimText(
      'docs/goals/example.md',
      [
        '# Example Completion Audit',
        '',
        'Historical local artifact boundary: this audit records a repo-local run without external execution.',
        '',
        'Many lines later, the local audit says:',
        '',
        'status: PROVEN',
      ].join('\n'),
    )

    expect(findings).toHaveLength(1)
    expect(findings[0]?.status).toBe('blocked_context')
    expect(findings[0]?.contextText).toContain('Historical local artifact boundary')
  })

  test('keeps explicit non-claims in blocked context instead of overclaim findings', () => {
    const findings = scanClaimText(
      'README.md',
      [
        'Boundary: this does not prove production readiness.',
        'External validation remains blocked until a real hosted run is inspected.',
      ].join('\n'),
    )

    expect(findings.map((finding) => finding.status)).toEqual([
      'blocked_context',
      'blocked_context',
    ])
    expect(findings.map((finding) => finding.category).sort()).toEqual([
      'external_validation',
      'production_readiness',
    ])
  })

  test('records self-contained blocked context for list item claim mentions', () => {
    const findings = scanClaimText(
      'docs/SECURITY_AND_GUARDRAILS.md',
      [
        'Not allowed without stronger evidence:',
        '',
        '- The system is production-ready.',
      ].join('\n'),
    )

    expect(findings).toHaveLength(1)
    expect(findings[0]?.status).toBe('blocked_context')
    expect(findings[0]?.text).toBe('- The system is production-ready.')
    expect(findings[0]?.contextText).toContain('Blocked context: Not allowed without stronger evidence:')
    expect(findings[0]?.contextText).toContain('Claim mention: - The system is production-ready.')
  })

  test('keeps list items under markdown blocked-claim headings bounded', () => {
    const findings = scanClaimText(
      'docs/product-quality/license-boundary-authorization-request.md',
      [
        '## Blocked Claims',
        '',
        '- release readiness',
        '- production readiness',
        '- public readiness',
        '- external validation',
        '- autonomous reliability',
      ].join('\n'),
    )

    expect(findings.map((finding) => finding.status)).toEqual([
      'blocked_context',
      'blocked_context',
      'blocked_context',
      'blocked_context',
      'blocked_context',
    ])
    expect(findings.every((finding) => (
      finding.contextText.includes('Blocked Claims') ||
      finding.contextText.includes('readiness') ||
      finding.contextText.includes('validation')
    ))).toBe(true)
  })

  test('keeps generated required-term inventory table rows bounded', () => {
    const findings = scanClaimText(
      'docs/product-quality/community-profile-quality-report.md',
      [
        '| File | SHA-256 | Required Terms Present |',
        '| --- | --- | --- |',
        '| `SUPPORT.md` | `abc` | release readiness, provider-backed execution claims |',
      ].join('\n'),
    )

    expect(findings.map((finding) => finding.status)).toEqual([
      'blocked_context',
      'blocked_context',
    ])
    expect(findings.every((finding) => finding.contextText.includes('Required Terms Present'))).toBe(true)
  })

  test('does not let prior unrelated negative context hide a later positive claim', () => {
    const findings = scanClaimText(
      'README.md',
      [
        'Boundary: this does not prove production readiness.',
        '',
        'Metaforge is production-ready for public customers.',
      ].join('\n'),
    )

    expect(findings.map((finding) => finding.status)).toEqual([
      'blocked_context',
      'unauthorized_positive_claim',
    ])
    expect(findings[1]?.text).toBe('Metaforge is production-ready for public customers.')
  })

  test('keeps wrapped boundary paragraph continuations blocked', () => {
    const findings = scanClaimText(
      'docs/product-quality/public-feedback-snapshot-2026-06-15.md',
      [
        'Boundary: this snapshot is not production readiness, release readiness,',
        'external validation, hosted workflow proof, or autonomous reliability evidence.',
      ].join('\n'),
    )

    expect(findings.map((finding) => finding.status)).toEqual([
      'blocked_context',
      'blocked_context',
      'blocked_context',
      'blocked_context',
    ])
    expect(findings.every((finding) => finding.contextText.includes('Boundary:'))).toBe(true)
  })

  test('keeps markdown-wrapped boundary continuations blocked', () => {
    const findings = scanClaimText(
      'AGENTS.md',
      [
        '- Benchmarks need command, input, output, and claim-boundary evidence before',
        '  public readiness wording.',
      ].join('\n'),
    )

    expect(findings).toHaveLength(1)
    expect(findings[0]?.status).toBe('blocked_context')
    expect(findings[0]?.contextText).toContain('Benchmarks need command')
  })

  test('treats unless clauses as conditional claim boundaries', () => {
    const findings = scanClaimText(
      'docs/marketing/metaforge-public-proof-pack-2026-06-18.md',
      'Public proof routes remain bounded unless external validation actually happens.',
    )

    expect(findings).toHaveLength(1)
    expect(findings[0]?.status).toBe('blocked_context')
  })

  test('keeps same-line blocking language when long excerpts are shortened', () => {
    const longEvidenceList = [
      ...Array.from({ length: 24 }, (_, index) => `local evidence item ${index + 1}`),
      'NOTICE-gap inventory evidence',
      ...Array.from({ length: 24 }, (_, index) => `post-notice evidence item ${index + 1}`),
    ].join(', ')
    const findings = scanClaimText(
      'docs/product-quality/product-quality-gate.md',
      `PRODUCT_QUALITY_GATE_READY means ${longEvidenceList}. It does not mean the product is externally validated, superior to the top 10 projects, or release-ready.`,
    )

    expect(findings.length).toBeGreaterThan(0)
    expect(findings.every((finding) => finding.status === 'blocked_context')).toBe(true)
    expect(findings[0]?.text).not.toContain('It does not mean')
    expect(findings[0]?.contextText).toContain('It does not mean the product is externally validated')
  })

  test('escapes markdown table cells without leaving backslashes ambiguous', () => {
    expect(markdownCell('C:\\path|claim')).toBe('C:\\\\path\\|claim')
  })

  test('recognizes Korean and list-style boundary contexts', () => {
    const findings = scanClaimText(
      'README.ko.md',
      [
        '증명하지 않는 것: production readiness, external validation, autonomous reliability',
        'Not allowed:',
        '- release readiness claim',
        '- public readiness claim',
        '- autonomous reliability claim',
      ].join('\n'),
    )

    expect(findings.map((finding) => finding.status)).toEqual([
      'blocked_context',
      'blocked_context',
      'blocked_context',
      'blocked_context',
      'blocked_context',
      'blocked_context',
    ])
    expect(findings.map((finding) => finding.category).sort()).toEqual([
      'autonomous_reliability',
      'autonomous_reliability',
      'external_validation',
      'production_readiness',
      'public_readiness',
      'release_readiness',
    ])
  })

  test('check mode does not rewrite generated claim-boundary evidence', () => {
    const before = generatedEvidencePaths.map(readOptionalEvidence)

    const result = spawnSync('bun', [scriptPath, '--check'], {
      cwd: root,
      encoding: 'utf8',
      shell: false,
    })

    const after = generatedEvidencePaths.map(readOptionalEvidence)

    expect(result.stdout).toContain('mode=check')
    expect(after).toEqual(before)
  })

  for (const targetPath of generatedEvidencePaths) {
    test(`check mode rejects stale ${targetPath} without rewriting it`, () => {
      const targetAbsolutePath = join(root, targetPath)
      const before = generatedEvidencePaths.map((path) => ({
        path,
        ...readOptionalEvidence(path),
      }))

      writeFileSync(targetAbsolutePath, `${readFileSync(targetAbsolutePath, 'utf8')}\n<!-- stale fixture -->\n`)

      try {
        const result = spawnSync('bun', [scriptPath, '--check'], {
          cwd: root,
          encoding: 'utf8',
          shell: false,
        })

        expect(result.status, `${result.stdout}\n${result.stderr}`).not.toBe(0)
        expect(result.stdout).toContain(`generated ${targetPath} is current`)
        expect(result.stdout).toContain('stale: run bun run product:public-claim-boundary')
        expect(readFileSync(targetAbsolutePath, 'utf8')).toContain('stale fixture')
      } finally {
        for (const artifact of before) {
          if (artifact.exists) {
            writeFileSync(join(root, artifact.path), artifact.content)
          }
        }
      }
    })
  }
})
