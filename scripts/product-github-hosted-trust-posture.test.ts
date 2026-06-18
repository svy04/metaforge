import { describe, expect, test } from 'bun:test'
import { readFileSync } from 'node:fs'
import {
  analyzeHostedTrustPosture,
  buildHostedTrustPostureMarkdown,
  buildHostedTrustPostureJsonl,
  hostedTrustPostureMode,
} from './product-github-hosted-trust-posture'

describe('GitHub hosted trust posture analysis', () => {
  test('supports a read-only check mode command surface', () => {
    expect(hostedTrustPostureMode(['bun', 'scripts/product-github-hosted-trust-posture.ts', '--check'])).toBe('check')
    expect(hostedTrustPostureMode(['bun', 'scripts/product-github-hosted-trust-posture.ts'])).toBe('write')

    const pkg = JSON.parse(readFileSync('package.json', 'utf8')) as { scripts: Record<string, string> }
    expect(pkg.scripts['product:github-hosted-trust-posture:check']).toBe(
      'bun run scripts/product-github-hosted-trust-posture.ts --check',
    )
  })

  test('classifies hosted security gaps without enabling readiness claims', () => {
    const report = analyzeHostedTrustPosture({
      repository: 'svy04/metaforge',
      defaultBranch: 'main',
      defaultBranchHeadSha: 'a'.repeat(40),
      branchProtection: { status: 'disabled', detail: '404 from branch protection endpoint' },
      rulesets: { status: 'absent', count: 0, detail: 'no repository rulesets returned' },
      securityAndAnalysis: {
        secretScanning: 'disabled',
        pushProtection: 'disabled',
        dependabotSecurityUpdates: 'unavailable',
      },
      vulnerabilityAlerts: { status: 'disabled_or_unavailable', detail: 'endpoint returned 404' },
      codeScanning: {
        status: 'available',
        openAlertCount: 436,
        byRuleSeverity: { error: 8, warning: 226, note: 202 },
        bySecuritySeverity: { high: 50, medium: 116 },
        topRules: [
          { ruleId: 'js/unused-local-variable', count: 70 },
          { ruleId: 'js/file-access-to-http', count: 43 },
        ],
      },
      latestMainRuns: [
        {
          name: 'PR Checks',
          status: 'completed',
          conclusion: 'success',
          headSha: 'a'.repeat(40),
          url: 'https://github.com/svy04/metaforge/actions/runs/1',
        },
        {
          name: 'CodeQL',
          status: 'in_progress',
          conclusion: null,
          headSha: 'a'.repeat(40),
          url: 'https://github.com/svy04/metaforge/actions/runs/2',
        },
      ],
      discovery: {
        repositoryDiscovery: 'gh_repo_view',
        branchProtectionDiscovery: 'github_branch_protection_api',
        rulesetDiscovery: 'github_rulesets_api',
        securityAndAnalysisDiscovery: 'github_repository_api',
        vulnerabilityAlertDiscovery: 'github_vulnerability_alerts_api',
        codeScanningDiscovery: 'github_code_scanning_api',
        workflowRunDiscovery: 'gh_run_list',
        defaultBranchHeadDiscovery: 'github_branch_api',
      },
    })

    expect(report.status).toBe('hosted_trust_risks_detected')
    expect(report.protectedActionsExecuted).toEqual([])
    expect(report.settingsMutationsPerformed).toEqual([])
    expect(report.publicSecurityPostureClaimAllowed).toBe(false)
    expect(report.releaseReadinessClaimAllowed).toBe(false)
    expect(report.risks.map((risk) => risk.category)).toEqual(
      expect.arrayContaining([
        'branch_protection_disabled',
        'rulesets_absent',
        'secret_scanning_disabled',
        'push_protection_disabled',
        'vulnerability_alerts_disabled_or_unavailable',
        'code_scanning_alert_backlog',
        'main_workflow_not_green',
      ]),
    )
    expect(report.risks.some((risk) => risk.detail.includes('OpenSSF Scorecard'))).toBe(true)
    expect(report.primarySourceInputs.map((source) => source.sourceType)).toEqual(
      expect.arrayContaining(['github_doc', 'oss_tool', 'standard', 'paper', 'patent']),
    )
    expect(report.evidenceChecks.some((check) => check.label === 'hosted settings were read only' && check.ok)).toBe(true)
  })

  test('requires a hosted OpenSSF Scorecard main run before workflow posture is green', () => {
    const baseInput = {
      repository: 'svy04/metaforge',
      defaultBranch: 'main',
      defaultBranchHeadSha: 'a'.repeat(40),
      branchProtection: { status: 'enabled' as const, detail: 'protected' },
      rulesets: { status: 'present' as const, count: 1, detail: '1 ruleset' },
      securityAndAnalysis: {
        secretScanning: 'enabled' as const,
        pushProtection: 'enabled' as const,
        dependabotSecurityUpdates: 'enabled' as const,
      },
      vulnerabilityAlerts: { status: 'enabled' as const, detail: '204' },
      codeScanning: {
        status: 'available' as const,
        openAlertCount: 0,
        byRuleSeverity: {},
        bySecuritySeverity: {},
        topRules: [],
      },
      discovery: {
        repositoryDiscovery: 'gh_repo_view' as const,
        branchProtectionDiscovery: 'github_branch_protection_api' as const,
        rulesetDiscovery: 'github_rulesets_api' as const,
        securityAndAnalysisDiscovery: 'github_repository_api' as const,
        vulnerabilityAlertDiscovery: 'github_vulnerability_alerts_api' as const,
        codeScanningDiscovery: 'github_code_scanning_api' as const,
        workflowRunDiscovery: 'gh_run_list' as const,
        defaultBranchHeadDiscovery: 'github_branch_api' as const,
      },
    }
    const greenCoreRuns = [
      {
        name: 'PR Checks',
        status: 'completed',
        conclusion: 'success',
        headSha: 'a'.repeat(40),
        url: 'https://github.com/svy04/metaforge/actions/runs/1',
      },
      {
        name: 'Release Boundary',
        status: 'completed',
        conclusion: 'success',
        headSha: 'a'.repeat(40),
        url: 'https://github.com/svy04/metaforge/actions/runs/2',
      },
      {
        name: 'CodeQL',
        status: 'completed',
        conclusion: 'success',
        headSha: 'a'.repeat(40),
        url: 'https://github.com/svy04/metaforge/actions/runs/3',
      },
    ]

    const missingScorecard = analyzeHostedTrustPosture({
      ...baseInput,
      latestMainRuns: greenCoreRuns,
    })
    expect(missingScorecard.risks.some((risk) => risk.detail.includes('OpenSSF Scorecard'))).toBe(true)
    expect(missingScorecard.status).toBe('hosted_trust_risks_detected')

    const withScorecard = analyzeHostedTrustPosture({
      ...baseInput,
      latestMainRuns: [
        {
          name: 'OpenSSF Scorecard',
          status: 'completed',
          conclusion: 'success',
          headSha: 'a'.repeat(40),
          url: 'https://github.com/svy04/metaforge/actions/runs/4',
        },
        ...greenCoreRuns,
      ],
    })
    expect(withScorecard.risks.some((risk) => risk.category === 'main_workflow_not_green')).toBe(false)
    expect(withScorecard.status).toBe('hosted_trust_no_risks_detected')
    expect(withScorecard.releaseReadinessClaimAllowed).toBe(false)
  })

  test('requires required workflow runs to match the observed default-branch head', () => {
    const baseInput = {
      repository: 'svy04/metaforge',
      defaultBranch: 'main',
      defaultBranchHeadSha: 'b'.repeat(40),
      branchProtection: { status: 'enabled' as const, detail: 'protected' },
      rulesets: { status: 'present' as const, count: 1, detail: '1 ruleset' },
      securityAndAnalysis: {
        secretScanning: 'enabled' as const,
        pushProtection: 'enabled' as const,
        dependabotSecurityUpdates: 'enabled' as const,
      },
      vulnerabilityAlerts: { status: 'enabled' as const, detail: '204' },
      codeScanning: {
        status: 'available' as const,
        openAlertCount: 0,
        byRuleSeverity: {},
        bySecuritySeverity: {},
        topRules: [],
      },
      latestMainRuns: ['PR Checks', 'Release Boundary', 'CodeQL', 'OpenSSF Scorecard'].map((name, index) => ({
        name,
        status: 'completed',
        conclusion: 'success',
        headSha: 'a'.repeat(40),
        url: `https://github.com/svy04/metaforge/actions/runs/${index + 1}`,
      })),
      discovery: {
        repositoryDiscovery: 'gh_repo_view' as const,
        branchProtectionDiscovery: 'github_branch_protection_api' as const,
        rulesetDiscovery: 'github_rulesets_api' as const,
        securityAndAnalysisDiscovery: 'github_repository_api' as const,
        vulnerabilityAlertDiscovery: 'github_vulnerability_alerts_api' as const,
        codeScanningDiscovery: 'github_code_scanning_api' as const,
        workflowRunDiscovery: 'gh_run_list' as const,
        defaultBranchHeadDiscovery: 'github_branch_api' as const,
      },
    }

    const staleRuns = analyzeHostedTrustPosture(baseInput)

    expect(staleRuns.status).toBe('hosted_trust_risks_detected')
    expect(staleRuns.risks.some((risk) => risk.detail.includes('does not match default branch head'))).toBe(true)

    const currentRuns = analyzeHostedTrustPosture({
      ...baseInput,
      defaultBranchHeadSha: 'a'.repeat(40),
    })

    expect(currentRuns.risks.some((risk) => risk.category === 'main_workflow_not_green')).toBe(false)
    expect(currentRuns.evidenceChecks.some((check) => check.label === 'required workflow runs match default branch head' && check.ok)).toBe(true)
  })

  test('classifies current-head pending workflow freshness before stronger hosted claims', () => {
    const currentSha = 'a'.repeat(40)
    const baseInput = {
      repository: 'svy04/metaforge',
      defaultBranch: 'main',
      defaultBranchHeadSha: currentSha,
      branchProtection: { status: 'enabled' as const, detail: 'protected' },
      rulesets: { status: 'present' as const, count: 1, detail: '1 ruleset' },
      securityAndAnalysis: {
        secretScanning: 'enabled' as const,
        pushProtection: 'enabled' as const,
        dependabotSecurityUpdates: 'enabled' as const,
      },
      vulnerabilityAlerts: { status: 'enabled' as const, detail: '204' },
      codeScanning: {
        status: 'available' as const,
        openAlertCount: 0,
        byRuleSeverity: {},
        bySecuritySeverity: {},
        topRules: [],
      },
      discovery: {
        repositoryDiscovery: 'gh_repo_view' as const,
        branchProtectionDiscovery: 'github_branch_protection_api' as const,
        rulesetDiscovery: 'github_rulesets_api' as const,
        securityAndAnalysisDiscovery: 'github_repository_api' as const,
        vulnerabilityAlertDiscovery: 'github_vulnerability_alerts_api' as const,
        codeScanningDiscovery: 'github_code_scanning_api' as const,
        workflowRunDiscovery: 'gh_run_list' as const,
        defaultBranchHeadDiscovery: 'github_branch_api' as const,
      },
    }
    const greenRuns = ['PR Checks', 'Release Boundary', 'OpenSSF Scorecard'].map((name, index) => ({
      databaseId: index + 1,
      name,
      workflowName: name,
      status: 'completed',
      conclusion: 'success',
      headSha: currentSha,
      createdAt: '2026-06-18T22:00:00Z',
      updatedAt: '2026-06-18T22:05:00Z',
      url: `https://github.com/svy04/metaforge/actions/runs/${index + 1}`,
    }))

    const freshPending = analyzeHostedTrustPosture({
      ...baseInput,
      latestMainRuns: [
        ...greenRuns,
        {
          databaseId: 4,
          name: 'CodeQL',
          workflowName: 'CodeQL',
          status: 'in_progress',
          conclusion: null,
          headSha: currentSha,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          url: 'https://github.com/svy04/metaforge/actions/runs/4',
        },
      ],
    })
    expect(freshPending.status).toBe('hosted_trust_risks_detected')
    expect(freshPending.risks.some((risk) => risk.detail.includes('pending_freshness=within_60_minutes_or_timestamp_unavailable'))).toBe(true)
    expect(freshPending.publicSecurityPostureClaimAllowed).toBe(false)

    const stalePending = analyzeHostedTrustPosture({
      ...baseInput,
      latestMainRuns: [
        ...greenRuns,
        {
          databaseId: 5,
          name: 'CodeQL',
          workflowName: 'CodeQL',
          status: 'in_progress',
          conclusion: null,
          headSha: currentSha,
          createdAt: '2000-01-01T00:00:00Z',
          updatedAt: '2000-01-01T00:00:00Z',
          url: 'https://github.com/svy04/metaforge/actions/runs/5',
        },
      ],
    })
    expect(stalePending.risks.some((risk) => risk.detail.includes('stale_pending_after_minutes=60'))).toBe(true)
    expect(stalePending.risks.some((risk) => risk.detail.includes('run_id=5'))).toBe(true)
  })

  test('writes JSONL risk records when hosted risks are present', () => {
    const report = analyzeHostedTrustPosture({
      repository: 'svy04/metaforge',
      defaultBranch: 'main',
      defaultBranchHeadSha: 'a'.repeat(40),
      branchProtection: { status: 'enabled', detail: 'protected' },
      rulesets: { status: 'present', count: 1, detail: '1 ruleset' },
      securityAndAnalysis: {
        secretScanning: 'enabled',
        pushProtection: 'enabled',
        dependabotSecurityUpdates: 'enabled',
      },
      vulnerabilityAlerts: { status: 'enabled', detail: '204' },
      codeScanning: {
        status: 'available',
        openAlertCount: 2,
        byRuleSeverity: { warning: 2 },
        bySecuritySeverity: { medium: 1 },
        topRules: [{ ruleId: 'js/example', count: 2 }],
      },
      latestMainRuns: [],
      discovery: {
        repositoryDiscovery: 'gh_repo_view',
        branchProtectionDiscovery: 'github_branch_protection_api',
        rulesetDiscovery: 'github_rulesets_api',
        securityAndAnalysisDiscovery: 'github_repository_api',
        vulnerabilityAlertDiscovery: 'github_vulnerability_alerts_api',
        codeScanningDiscovery: 'github_code_scanning_api',
        workflowRunDiscovery: 'gh_run_list',
        defaultBranchHeadDiscovery: 'github_branch_api',
      },
    })

    const jsonl = buildHostedTrustPostureJsonl(report)
    const records = jsonl.trim().split('\n').map((line) => JSON.parse(line))

    expect(records.some((record) => record.kind === 'github_hosted_trust_risk')).toBe(true)
    expect(records.some((record) => record.category === 'code_scanning_alert_backlog')).toBe(true)
  })

  test('markdown report exposes generated time and freshness boundary', () => {
    const report = analyzeHostedTrustPosture({
      repository: 'svy04/metaforge',
      defaultBranch: 'main',
      defaultBranchHeadSha: 'a'.repeat(40),
      branchProtection: { status: 'enabled', detail: 'protected' },
      rulesets: { status: 'present', count: 1, detail: '1 ruleset' },
      securityAndAnalysis: {
        secretScanning: 'enabled',
        pushProtection: 'enabled',
        dependabotSecurityUpdates: 'enabled',
      },
      vulnerabilityAlerts: { status: 'enabled', detail: '204' },
      codeScanning: {
        status: 'available',
        openAlertCount: 0,
        byRuleSeverity: {},
        bySecuritySeverity: {},
        topRules: [],
      },
      latestMainRuns: [
        {
          databaseId: 4,
          name: 'OpenSSF Scorecard',
          workflowName: 'OpenSSF Scorecard',
          status: 'completed',
          conclusion: 'success',
          headSha: 'a'.repeat(40),
          createdAt: '2026-06-18T22:00:00Z',
          updatedAt: '2026-06-18T22:05:00Z',
          url: 'https://github.com/svy04/metaforge/actions/runs/4',
        },
        {
          name: 'PR Checks',
          status: 'completed',
          conclusion: 'success',
          headSha: 'a'.repeat(40),
          url: 'https://github.com/svy04/metaforge/actions/runs/1',
        },
        {
          name: 'Release Boundary',
          status: 'completed',
          conclusion: 'success',
          headSha: 'a'.repeat(40),
          url: 'https://github.com/svy04/metaforge/actions/runs/2',
        },
        {
          name: 'CodeQL',
          status: 'completed',
          conclusion: 'success',
          headSha: 'a'.repeat(40),
          url: 'https://github.com/svy04/metaforge/actions/runs/3',
        },
      ],
      discovery: {
        repositoryDiscovery: 'gh_repo_view',
        branchProtectionDiscovery: 'github_branch_protection_api',
        rulesetDiscovery: 'github_rulesets_api',
        securityAndAnalysisDiscovery: 'github_repository_api',
        vulnerabilityAlertDiscovery: 'github_vulnerability_alerts_api',
        codeScanningDiscovery: 'github_code_scanning_api',
        workflowRunDiscovery: 'gh_run_list',
        defaultBranchHeadDiscovery: 'github_branch_api',
      },
    })

    const markdown = buildHostedTrustPostureMarkdown(report, 'a'.repeat(64))

    expect(markdown).toContain(`- generated_at: \`${report.generatedAt}\``)
    expect(markdown).toContain('- freshness_boundary: `current at generated_at only`')
    expect(markdown).toContain(`- default_branch_head_sha: \`${report.defaultBranchHeadSha}\``)
    expect(markdown).toContain('| Workflow | Workflow Name | Status | Conclusion | SHA | Created At | Updated At | Freshness | URL |')
    expect(markdown).toContain('run_id=4; workflow_name=OpenSSF Scorecard')
  })
})
