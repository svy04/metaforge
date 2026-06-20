import { describe, expect, test } from 'bun:test'
import { readFileSync } from 'node:fs'
import {
  buildSecretScannerEvidenceJsonl,
  buildSecretScannerEvidenceReport,
  buildSecretScannerEvidenceMarkdown,
} from './product-secret-scanner-evidence'

describe('secret scanner evidence report', () => {
  test('records scanner availability and hosted gaps without unlocking secret-clean claims', () => {
    const report = buildSecretScannerEvidenceReport({
      repository: 'svy04/metaforge',
      sourceCommit: 'a'.repeat(40),
      generatedFrom: [
        'docs/product-quality/github-remote-surface-audit-report.json',
        'docs/product-quality/github-hosted-trust-posture-report.json',
      ],
      externalScanners: [
        { name: 'Gitleaks', command: 'gitleaks', status: 'unavailable', detail: 'not found' },
        { name: 'TruffleHog', command: 'trufflehog', status: 'unavailable', detail: 'not found' },
        { name: 'detect-secrets', command: 'detect-secrets', status: 'unavailable', detail: 'not found' },
      ],
      hostedSecretScanning: {
        secretScanning: 'disabled',
        pushProtection: 'disabled',
        sourceReportPath: 'docs/product-quality/github-hosted-trust-posture-report.json',
      },
      remoteSurfaceAudit: {
        status: 'no_public_github_surface_findings_detected',
        blockerCount: 0,
        sourceReportPath: 'docs/product-quality/github-remote-surface-audit-report.json',
      },
    })

    expect(report.mode).toBe('claim_bounded_secret_scanner_evidence')
    expect(report.status).toBe('secret_scanner_evidence_gaps_recorded')
    expect(report.externalScannerUnavailableCount).toBe(3)
    expect(report.findings.map((finding) => finding.category)).toEqual(
      expect.arrayContaining([
        'external_scanner_unavailable',
        'hosted_secret_scanning_disabled',
        'hosted_push_protection_disabled',
      ]),
    )
    expect(report.fullHistorySecretCleanClaimAllowed).toBe(false)
    expect(report.hostedSecretScanningCleanClaimAllowed).toBe(false)
    expect(report.verifiedSecretCleanClaimAllowed).toBe(false)
    expect(report.publicSecurityPostureClaimAllowed).toBe(false)
    expect(report.releaseReadinessClaimAllowed).toBe(false)
    expect(report.evidenceChecks.every((item) => item.ok)).toBe(true)
    expect(report.primarySourceInputs.map((source) => source.sourceType)).toEqual(
      expect.arrayContaining(['github_doc', 'oss_tool', 'standard', 'paper', 'patent']),
    )
  })

  test('keeps stronger claims blocked even when scanner and hosted inputs are green', () => {
    const report = buildSecretScannerEvidenceReport({
      repository: 'svy04/metaforge',
      sourceCommit: 'b'.repeat(40),
      generatedFrom: [],
      externalScanners: [
        { name: 'Gitleaks', command: 'gitleaks', status: 'available', detail: 'version 8.x' },
        { name: 'TruffleHog', command: 'trufflehog', status: 'available', detail: 'version 3.x' },
        { name: 'detect-secrets', command: 'detect-secrets', status: 'available', detail: 'version 1.x' },
      ],
      hostedSecretScanning: {
        secretScanning: 'enabled',
        pushProtection: 'enabled',
        sourceReportPath: 'docs/product-quality/github-hosted-trust-posture-report.json',
      },
      remoteSurfaceAudit: {
        status: 'no_public_github_surface_findings_detected',
        blockerCount: 0,
        sourceReportPath: 'docs/product-quality/github-remote-surface-audit-report.json',
      },
    })

    expect(report.status).toBe('secret_scanner_evidence_recorded')
    expect(report.findingCount).toBe(0)
    expect(report.fullHistorySecretCleanClaimAllowed).toBe(false)
    expect(report.hostedSecretScanningCleanClaimAllowed).toBe(false)
    expect(report.verifiedSecretCleanClaimAllowed).toBe(false)
    expect(report.claimBoundary).toContain('does not claim full-history secret cleanliness')
  })

  test('writes JSONL and Markdown with claim boundaries', () => {
    const report = buildSecretScannerEvidenceReport({
      repository: 'svy04/metaforge',
      sourceCommit: 'c'.repeat(40),
      generatedFrom: [],
      externalScanners: [
        { name: 'Gitleaks', command: 'gitleaks', status: 'unavailable', detail: 'not found' },
      ],
      hostedSecretScanning: {
        secretScanning: 'unavailable',
        pushProtection: 'unavailable',
        sourceReportPath: 'docs/product-quality/github-hosted-trust-posture-report.json',
      },
      remoteSurfaceAudit: {
        status: 'blocked_public_github_surface_findings',
        blockerCount: 2,
        sourceReportPath: 'docs/product-quality/github-remote-surface-audit-report.json',
      },
    })

    const jsonl = buildSecretScannerEvidenceJsonl(report)
    const records = jsonl.trim().split('\n').map((line) => JSON.parse(line))
    const markdown = buildSecretScannerEvidenceMarkdown(report, 'd'.repeat(64))

    expect(records.some((record) => record.kind === 'secret_scanner_evidence_finding')).toBe(true)
    expect(markdown).toContain('# Secret Scanner Evidence Report')
    expect(markdown).toContain('does not claim full-history secret cleanliness')
    expect(markdown).toContain('jsonl_sha256')
  })

  test('package quality and evidence manifest wire the report without putting it in verify:privacy', () => {
    const packageJson = JSON.parse(readFileSync('package.json', 'utf8')) as { scripts: Record<string, string> }
    const manifestSource = readFileSync('scripts/product-evidence-manifest.ts', 'utf8')

    expect(packageJson.scripts['product:secret-scanner-evidence']).toBe(
      'bun run scripts/product-secret-scanner-evidence.ts',
    )
    expect(packageJson.scripts['product:secret-scanner-evidence:check']).toBe(
      'bun run scripts/product-secret-scanner-evidence.ts --check',
    )
    expect(packageJson.scripts['product:quality']).toContain('bun run product:secret-scanner-evidence')
    expect(packageJson.scripts['verify:privacy']).toContain('bun run product:secret-scanner-evidence:check')
    expect(packageJson.scripts['verify:privacy']).not.toContain('product:secret-scanner-evidence &&')
    expect(manifestSource).toContain('docs/product-quality/secret-scanner-evidence-report.json')
    expect(manifestSource).toContain('docs/product-quality/secret-scanner-evidence-report.md')
    expect(manifestSource).toContain('reports/openclaude-secret-scanner-evidence.jsonl')
  })
})
