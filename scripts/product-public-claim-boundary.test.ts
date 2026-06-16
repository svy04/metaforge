import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { existsSync, readFileSync } from 'node:fs'
import { join } from 'node:path'

import { publicSurfacePaths, scanClaimText } from './product-public-claim-boundary'

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
