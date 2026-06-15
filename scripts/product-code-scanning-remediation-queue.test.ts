import { describe, expect, test } from 'bun:test'
import {
  buildCodeScanningRemediationQueue,
  buildCodeScanningRemediationQueueJsonl,
} from './product-code-scanning-remediation-queue'

describe('CodeQL remediation queue', () => {
  test('prioritizes security-sensitive CodeQL rules before cleanup-heavy buckets', () => {
    const report = buildCodeScanningRemediationQueue({
      repository: 'svy04/metaforge',
      defaultBranch: 'main',
      sourceCommit: 'a'.repeat(40),
      generatedFrom: 'docs/product-quality/github-hosted-trust-posture-report.json',
      codeScanning: {
        status: 'available',
        openAlertCount: 436,
        topRules: [
          { ruleId: 'js/unused-local-variable', count: 184 },
          { ruleId: 'js/file-access-to-http', count: 74 },
          { ruleId: 'js/http-to-file-access', count: 33 },
          { ruleId: 'js/insecure-temporary-file', count: 23 },
          { ruleId: 'js/file-system-race', count: 22 },
        ],
      },
      sampleLocationsByRule: {
        'js/insecure-temporary-file': [
          { path: 'scripts/example-temp.ts', startLine: 12 },
        ],
        'js/file-system-race': [
          { path: 'scripts/example-race.ts', startLine: 34 },
        ],
      },
      latestMainRuns: [
        {
          name: 'CodeQL',
          status: 'in_progress',
          conclusion: null,
          headSha: 'a'.repeat(40),
          url: 'https://github.com/svy04/metaforge/actions/runs/1',
        },
      ],
    })

    expect(report.status).toBe('remediation_queue_required')
    expect(report.queueItems.map((item) => item.ruleId).slice(0, 2)).toEqual([
      'js/file-system-race',
      'js/insecure-temporary-file',
    ])

    const unused = report.queueItems.find((item) => item.ruleId === 'js/unused-local-variable')
    expect(unused?.priority).toBe('P3')
    expect(unused?.ownerDecisionRequired).toBe(false)

    const temp = report.queueItems.find((item) => item.ruleId === 'js/insecure-temporary-file')
    expect(temp?.priority).toBe('P0')
    expect(temp?.ownerDecisionRequired).toBe(true)
    expect(temp?.sourceUrl).toBe('https://codeql.github.com/codeql-query-help/javascript/js-insecure-temporary-file/')
    expect(temp?.validationCommands).toContain('bun run product:github-hosted-trust-posture')

    expect(report.publicSecurityPostureClaimAllowed).toBe(false)
    expect(report.releaseReadinessClaimAllowed).toBe(false)
    expect(report.productionReadinessClaimAllowed).toBe(false)
    expect(report.externalValidationClaimAllowed).toBe(false)
    expect(report.evidenceChecks.every((item) => item.ok)).toBe(true)
  })

  test('writes JSONL records for each remediation queue item', () => {
    const report = buildCodeScanningRemediationQueue({
      repository: 'svy04/metaforge',
      defaultBranch: 'main',
      sourceCommit: 'b'.repeat(40),
      generatedFrom: 'fixture',
      codeScanning: {
        status: 'available',
        openAlertCount: 2,
        topRules: [
          { ruleId: 'js/file-access-to-http', count: 1 },
          { ruleId: 'js/unused-local-variable', count: 1 },
        ],
      },
      sampleLocationsByRule: {},
      latestMainRuns: [],
    })

    const records = buildCodeScanningRemediationQueueJsonl(report)
      .trim()
      .split('\n')
      .map((line) => JSON.parse(line))

    expect(records).toHaveLength(report.queueItems.length)
    expect(records.every((record) => record.kind === 'code_scanning_remediation_queue_item')).toBe(true)
    expect(records.map((record) => record.ruleId)).toEqual(report.queueItems.map((item) => item.ruleId))
  })
})
