import { describe, expect, test } from 'bun:test'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import {
  buildEvidenceManifestJsonl,
  buildProductEvidenceManifestReport,
  filterSourceControlledEvidencePaths,
  hasCredentialPattern,
  isSourceControlledReportArtifactPath,
  proofClassFor,
  rawRequiredEvidencePaths,
  roleFor,
  type EvidenceRecord,
} from './product-evidence-manifest'

const sha = 'a'.repeat(64)
const root = join(__dirname, '..')

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
  record('.jscpd.json', 'source'),
  record('docs/product-quality/example-report.json', 'evidence_report'),
  record('docs/product-quality/terminal-failure-recovery-transcripts-report.json', 'evidence_report'),
  record('docs/product-quality/script-duplication-audit-report.json', 'evidence_report'),
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
    expect(report.evidenceTotalSizeBytes).toBe(80)
    expect(report.evidenceRoles).toEqual({
      source: 2,
      evidence_report: 3,
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

  test('separates behavioral evidence from structural audit evidence before public claims', () => {
    const { report } = buildProductEvidenceManifestReport({
      evidenceRecords: [
        record('docs/product-quality/terminal-failure-recovery-transcripts-report.json', 'evidence_report'),
        record('reports/orchestra-protected-action-denial-trace-local-fixture.jsonl', 'evidence_artifact'),
        record('docs/product-quality/script-duplication-audit-report.json', 'evidence_report'),
        record('.dependency-cruiser.mjs', 'source'),
        record('docs/product-quality/public-claim-boundary-report.json', 'evidence_report'),
      ],
      requiredPaths: [],
    })

    expect(proofClassFor('docs/product-quality/terminal-failure-recovery-transcripts-report.json')).toBe(
      'behavioral_runtime',
    )
    expect(proofClassFor('reports/orchestra-protected-action-denial-trace-local-fixture.jsonl')).toBe(
      'behavioral_runtime',
    )
    expect(proofClassFor('docs/product-quality/script-duplication-audit-report.json')).toBe('static_analysis')
    expect(proofClassFor('.dependency-cruiser.mjs')).toBe('static_analysis')
    expect(proofClassFor('knip.jsonc')).toBe('static_analysis')
    expect(proofClassFor('docs/product-quality/public-claim-boundary-report.json')).toBe('governance_boundary')
    expect(proofClassFor('docs/product-quality/secret-scanner-evidence-report.json')).toBe('governance_boundary')
    expect(report.evidenceProofClasses.behavioral_runtime).toBe(2)
    expect(report.evidenceProofClasses.static_analysis).toBe(2)
    expect(report.evidenceProofClasses.governance_boundary).toBe(1)
    expect(
      report.evidenceChecks.some(
        (item) => item.label === 'behavioral evidence is separated from structural audit evidence' && item.ok,
      ),
    ).toBe(true)
  })

  test('detects credential-shaped values before manifest packaging is treated as clean evidence', () => {
    expect(hasCredentialPattern(`github_pat_${'A'.repeat(40)}`)).toBe(true)
    expect(hasCredentialPattern('reports/openclaude-safe-evidence.jsonl')).toBe(false)
  })

  test('excludes ignored local report artifacts from public evidence manifests', () => {
    const paths = [
      'docs/product-quality/real-session-trace-evals-report.json',
      'reports/openclaude-github-hosted-trust-posture.jsonl',
      'reports/openclaude-portable-trace-events.jsonl',
      'reports/orchestra-code-editing-trace-local-fixture.jsonl',
    ]

    expect(filterSourceControlledEvidencePaths(paths, new Set([
      'reports/openclaude-github-hosted-trust-posture.jsonl',
    ]))).toEqual([
      'docs/product-quality/real-session-trace-evals-report.json',
      'reports/openclaude-github-hosted-trust-posture.jsonl',
    ])
  })

  test('wires proof-class evidence buckets into English and Korean proof ladders', () => {
    const readme = readFileSync(join(root, 'README.md'), 'utf8')
    const koreanReadme = readFileSync(join(root, 'README.ko.md'), 'utf8')

    expect(readme).toContain('evidence manifest now separates behavioral runtime evidence')
    expect(readme).toContain('static analysis, governance-boundary, source-control, and structural-inventory evidence')
    expect(koreanReadme).toContain('evidence manifest는 behavioral runtime evidence')
    expect(koreanReadme).toContain('static analysis, governance-boundary, source-control, structural-inventory evidence')
  })

  test('requires the Knip config as static-analysis evidence', () => {
    expect(rawRequiredEvidencePaths).toContain('knip.jsonc')
  })

  test('includes Metaforge-owned source-controlled report artifacts', () => {
    expect(rawRequiredEvidencePaths).toContain('reports/metaforge-public-claim-boundary.jsonl')
    expect(rawRequiredEvidencePaths).toContain('docs/product-quality/secret-scanner-evidence-report.json')
    expect(rawRequiredEvidencePaths).toContain('reports/openclaude-secret-scanner-evidence.jsonl')
    expect(isSourceControlledReportArtifactPath('reports/openclaude-product-evidence-manifest.jsonl')).toBe(true)
    expect(isSourceControlledReportArtifactPath('reports/orchestra-protected-action-denial-trace-local-fixture.jsonl')).toBe(true)
    expect(isSourceControlledReportArtifactPath('reports/metaforge-public-claim-boundary.jsonl')).toBe(true)
    expect(isSourceControlledReportArtifactPath('reports/private-runtime-dump.jsonl')).toBe(false)
  })
})
