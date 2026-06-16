import { readFileSync } from 'node:fs'
import { describe, expect, test } from 'bun:test'
import {
  analyzeOriginLicenseProvenanceBoundary,
  buildOriginLicenseProvenanceJsonl,
  originLicenseProvenanceMode,
} from './product-origin-license-provenance-boundary'

const cleanInput = {
  packageJson: {
    name: '@gitlawb/openclaude',
    license: 'SEE LICENSE FILE',
    repository: { url: 'https://github.com/svy04/metaforge.git' },
  },
  originRemoteUrl: 'https://github.com/svy04/metaforge.git',
  readmeText: [
    "OpenClaude includes runtime code derived from Anthropic's Claude Code CLI.",
    'This is not a blanket MIT license over the entire derived runtime.',
    'Metaforge = Meta + MFH + Orchestra OS.',
  ].join('\n'),
  koreanReadmeText: [
    'OpenClaude runtime에는 Anthropic Claude Code CLI에서 파생된 코드가 포함되어 있습니다.',
    '파생 runtime 전체에 대한 blanket MIT license가 아닙니다.',
    'Metaforge는 Meta + MFH + Orchestra OS입니다.',
  ].join('\n'),
  licenseText: [
    "This repository contains code derived from Anthropic's Claude Code CLI.",
    'OpenClaude contributors (modifications only) license their changes under the MIT License where legally permissible.',
    "The underlying derived code remains subject to Anthropic's copyright.",
  ].join('\n'),
  sourceLicenseMetadataReport: {
    mode: 'local_no_provider_source_license_metadata_quality',
    packageLicenseField: 'SEE LICENSE FILE',
    rootLicenseContainsDerivedCodeBoundary: true,
    rootLicenseContainsMitModificationBoundary: true,
    reuseComplianceClaimAllowed: false,
    sourceLicenseComplianceClaimAllowed: false,
    sourceMetadataReadyClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
  },
  thirdPartyLicenseReport: {
    mode: 'local_no_provider_third_party_license_quality',
    licenseComplianceClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
  },
  licenseBoundaryAuthorizationReport: {
    mode: 'local_no_provider_license_boundary_authorization',
    legalReviewPerformed: false,
    ownerAuthorizationRecorded: false,
    licenseBoundaryAuthorizationClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
  },
  githubRemoteSurfaceAuditReport: {
    mode: 'github_public_remote_surface_audit',
    status: 'no_public_github_surface_findings_detected',
    blockerCount: 0,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    protectedActionsExecuted: [],
  },
  releaseArtifactProvenanceReport: {
    mode: 'local_no_provider_release_artifact_hash_sbom_provenance',
    publishAttempted: false,
    deployAttempted: false,
    launchAttempted: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
  },
}

describe('origin/license provenance boundary', () => {
  test('blocks stale repository origins and blanket MIT or original-CLI claims', () => {
    const report = analyzeOriginLicenseProvenanceBoundary({
      ...cleanInput,
      packageJson: {
        ...cleanInput.packageJson,
        license: 'MIT',
        repository: { url: 'https://github.com/Gitlawb/openclaude.git' },
      },
      readmeText: 'OpenClaude is a fully original MIT-licensed CLI built from scratch.',
    })

    expect(report.status).toBe('blocked_origin_license_provenance_boundary')
    expect(report.blockers.map((blocker) => blocker.category)).toContain('stale_repository_origin')
    expect(report.blockers.map((blocker) => blocker.category)).toContain('blanket_mit_license_claim')
    expect(report.blockers.map((blocker) => blocker.category)).toContain('missing_derived_runtime_boundary')
    expect(report.blockers.map((blocker) => blocker.category)).toContain('fully_original_cli_claim')
  })

  test('blocks upstream reports that upgrade local inventories into readiness or compliance claims', () => {
    const report = analyzeOriginLicenseProvenanceBoundary({
      ...cleanInput,
      sourceLicenseMetadataReport: {
        ...cleanInput.sourceLicenseMetadataReport,
        reuseComplianceClaimAllowed: true,
      },
      licenseBoundaryAuthorizationReport: {
        ...cleanInput.licenseBoundaryAuthorizationReport,
        legalReviewPerformed: true,
      },
      githubRemoteSurfaceAuditReport: {
        ...cleanInput.githubRemoteSurfaceAuditReport,
        blockerCount: 2,
        status: 'blocked_public_github_surface_findings',
      },
      releaseArtifactProvenanceReport: {
        ...cleanInput.releaseArtifactProvenanceReport,
        publishAttempted: true,
      },
    })

    expect(report.status).toBe('blocked_origin_license_provenance_boundary')
    expect(report.blockers.map((blocker) => blocker.category)).toEqual(
      expect.arrayContaining([
        'source_license_claim_overreach',
        'legal_review_claim_present',
        'public_remote_surface_blocked',
        'protected_release_action_attempted',
      ]),
    )
  })

  test('blocks npm install commands that imply this checkout is the published package', () => {
    const report = analyzeOriginLicenseProvenanceBoundary({
      ...cleanInput,
      readmeText: `${cleanInput.readmeText}\n\nnpm install -g @gitlawb/openclaude`,
    })

    expect(report.status).toBe('blocked_origin_license_provenance_boundary')
    expect(report.blockers.map((blocker) => blocker.category)).toContain(
      'ambiguous_external_npm_install_claim',
    )
  })

  test('writes nonempty JSONL evidence when the boundary is clean', () => {
    const report = analyzeOriginLicenseProvenanceBoundary(cleanInput)
    const jsonl = buildOriginLicenseProvenanceJsonl(report)

    expect(report.status).toBe('no_origin_license_provenance_boundary_findings')
    expect(report.blockerCount).toBe(0)
    expect(jsonl.trim().length).toBeGreaterThan(0)
    expect(JSON.parse(jsonl.trim())).toMatchObject({
      kind: 'origin_license_provenance_boundary_summary',
      status: 'no_origin_license_provenance_boundary_findings',
      blockerCount: 0,
    })
  })

  test('exposes no-write check mode and wires privacy verification to it', () => {
    const packageJson = JSON.parse(readFileSync('package.json', 'utf8')) as {
      scripts: Record<string, string>
    }

    expect(originLicenseProvenanceMode(['bun', 'script'])).toBe('write')
    expect(originLicenseProvenanceMode(['bun', 'script', '--check'])).toBe('check')
    expect(packageJson.scripts['product:origin-license-provenance-boundary:check']).toBe(
      'bun run scripts/product-origin-license-provenance-boundary.ts --check',
    )
    expect(packageJson.scripts['verify:privacy']).toContain(
      'product:origin-license-provenance-boundary:check',
    )
  })
})
