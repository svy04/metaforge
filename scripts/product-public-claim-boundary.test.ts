import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { existsSync, readFileSync } from 'node:fs'
import { join } from 'node:path'

import { markdownCell, publicSurfacePaths, scanClaimText } from './product-public-claim-boundary'

const root = join(__dirname, '..')
const scriptPath = join(__dirname, 'product-public-claim-boundary.ts')
const generatedEvidencePaths = [
  'docs/product-quality/public-claim-boundary-report.json',
  'docs/product-quality/public-claim-boundary-report.md',
  'reports/openclaude-public-claim-boundary.jsonl',
]

function readOptionalEvidence(path: string) {
  const absolutePath = join(root, path)

  if (!existsSync(absolutePath)) {
    return { exists: false, content: '' }
  }

  return { exists: true, content: readFileSync(absolutePath, 'utf8') }
}

describe('product public claim boundary classifier', () => {
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
      'docs/marketing/metaforge-public-proof-pack-2026-06-14.md',
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

    expect(result.status, `${result.stdout}\n${result.stderr}`).toBe(0)
    expect(result.stdout).toContain('RESULT: PASS')
    expect(after).toEqual(before)
  })
})
