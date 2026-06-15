import { describe, expect, test } from 'bun:test'
import {
  analyzeHostedTrustPosture,
  buildHostedTrustPostureJsonl,
} from './product-github-hosted-trust-posture'

describe('GitHub hosted trust posture analysis', () => {
  test('classifies hosted security gaps without enabling readiness claims', () => {
    const report = analyzeHostedTrustPosture({
      repository: 'svy04/metaforge',
      defaultBranch: 'main',
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
    expect(report.primarySourceInputs.map((source) => source.sourceType)).toEqual(
      expect.arrayContaining(['github_doc', 'oss_tool', 'standard', 'paper', 'patent']),
    )
    expect(report.evidenceChecks.some((check) => check.label === 'hosted settings were read only' && check.ok)).toBe(true)
  })

  test('writes JSONL risk records when hosted risks are present', () => {
    const report = analyzeHostedTrustPosture({
      repository: 'svy04/metaforge',
      defaultBranch: 'main',
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
      },
    })

    const jsonl = buildHostedTrustPostureJsonl(report)
    const records = jsonl.trim().split('\n').map((line) => JSON.parse(line))

    expect(records.some((record) => record.kind === 'github_hosted_trust_risk')).toBe(true)
    expect(records.some((record) => record.category === 'code_scanning_alert_backlog')).toBe(true)
  })
})
