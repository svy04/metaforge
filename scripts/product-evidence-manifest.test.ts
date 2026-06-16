import { describe, expect, test } from 'bun:test'
import {
  buildEvidenceManifestJsonl,
  buildProductEvidenceManifestReport,
  hasCredentialPattern,
  roleFor,
  type EvidenceRecord,
} from './product-evidence-manifest'

const sha = 'a'.repeat(64)

function record(path: string, role: EvidenceRecord['role'], overrides: Partial<EvidenceRecord> = {}): EvidenceRecord {
  return {
    path,
    role,
    sha256: sha,
    sizeBytes: 10,
    ...overrides,
  }
}

function okFor(report: ReturnType<typeof buildProductEvidenceManifestReport>['report'], label: string): boolean {
  const check = report.evidenceChecks.find((item) => item.label === label)
  if (!check) throw new Error(`missing check: ${label}`)
  return check.ok
}

const completeRecords = [
  record('package.json', 'source'),
  record('docs/product-quality/example-report.json', 'evidence_report'),
  record('reports/openclaude-example.jsonl', 'evidence_artifact'),
  record('docs/product-quality/product-quality-gate.md', 'quality_gate'),
  record('.github/workflows/pr-checks.yml', 'workflow'),
]

describe('product evidence manifest behavior', () => {
  test('builds a bounded manifest report from concrete records', () => {
    const { report, manifestText } = buildProductEvidenceManifestReport({
      evidenceRecords: completeRecords,
      generatedAt: '2026-06-16T00:00:00.000Z',
      requiredPaths: completeRecords.map((item) => item.path),
      recursiveSelfInputs: ['docs/product-quality/product-evidence-manifest.json'],
    })

    expect(report.generatedAt).toBe('2026-06-16T00:00:00.000Z')
    expect(report.evidenceRecordCount).toBe(completeRecords.length)
    expect(report.evidenceTotalSizeBytes).toBe(50)
    expect(report.evidenceRoles).toEqual({
      source: 1,
      evidence_report: 1,
      evidence_artifact: 1,
      quality_gate: 1,
      workflow: 1,
    })
    expect(report.providerCallsPerformed).toEqual([])
    expect(report.externalAttestationGenerated).toBe(false)
    expect(report.releaseReadinessClaimAllowed).toBe(false)
    expect(report.evidenceChecks.every((item) => item.ok)).toBe(true)
    expect(manifestText).toBe(buildEvidenceManifestJsonl(completeRecords))
  })

  test('fails behavior checks for missing evidence, invalid records, self-input recursion, and credential-shaped paths', () => {
    const credentialPath = `reports/ghp_${'A'.repeat(30)}.jsonl`
    const { report } = buildProductEvidenceManifestReport({
      evidenceRecords: [
        ...completeRecords,
        record('docs/product-quality/product-evidence-manifest.json', 'evidence_report'),
        record(credentialPath, 'evidence_artifact', { sha256: 'not-a-sha', sizeBytes: 0 }),
      ],
      requiredPaths: [...completeRecords.map((item) => item.path), 'reports/missing-required.jsonl'],
      recursiveSelfInputs: ['docs/product-quality/product-evidence-manifest.json'],
    })

    expect(report.missingRequiredEvidencePaths).toEqual(['reports/missing-required.jsonl'])
    expect(okFor(report, 'required evidence paths are present')).toBe(false)
    expect(okFor(report, 'evidence records have SHA-256 digests')).toBe(false)
    expect(okFor(report, 'evidence records have nonzero sizes')).toBe(false)
    expect(okFor(report, 'recursive self inputs are excluded')).toBe(false)
    expect(okFor(report, 'manifest contains no credential patterns')).toBe(false)
  })

  test('classifies record roles by behavior instead of filename string presence only', () => {
    expect(roleFor('package.json')).toBe('source')
    expect(roleFor('bun.lock')).toBe('source')
    expect(roleFor('.github/workflows/pr-checks.yml')).toBe('workflow')
    expect(roleFor('docs/product-quality/product-quality-gate.md')).toBe('quality_gate')
    expect(roleFor('docs/product-quality/example-report.json')).toBe('evidence_report')
    expect(roleFor('reports/openclaude-example.jsonl')).toBe('evidence_artifact')
  })

  test('detects credential-shaped values before manifest packaging is treated as clean evidence', () => {
    expect(hasCredentialPattern(`github_pat_${'A'.repeat(40)}`)).toBe(true)
    expect(hasCredentialPattern('reports/openclaude-safe-evidence.jsonl')).toBe(false)
  })
})
