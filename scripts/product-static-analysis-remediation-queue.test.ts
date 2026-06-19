import { describe, expect, test } from 'bun:test'
import {
  buildStaticAnalysisRemediationQueue,
  buildStaticAnalysisRemediationQueueJsonl,
} from './product-static-analysis-remediation-queue'

describe('static analysis remediation queue', () => {
  test('prioritizes new topology violations before cleanup candidates', () => {
    const report = buildStaticAnalysisRemediationQueue({
      repository: 'svy04/metaforge',
      sourceCommit: 'a'.repeat(40),
      generatedFrom: [
        'docs/product-quality/dead-export-candidates-report.json',
        'docs/product-quality/dependency-topology-report.json',
        'docs/product-quality/script-duplication-audit-report.json',
      ],
      deadExport: {
        candidateFileCount: 637,
        candidateUnusedExportCount: 1396,
        candidateUnusedTypeCount: 364,
        candidateDuplicateExportCount: 12,
        triageRecords: [
          {
            file: 'src/services/api/providerConfig.ts',
            symbol: 'resolveStoredCodexCredentials',
            action: 'needs_runtime_guard',
            currentCandidate: true,
          },
          {
            file: 'src/utils/providerProfile.ts',
            symbol: 'buildNvidiaNimProfileEnv',
            action: 'review_for_removal',
            currentCandidate: true,
          },
        ],
      },
      dependencyTopology: {
        circularDependencyCount: 1737,
        unresolvedDependencyCount: 863,
        configuredRatchetNewViolationCount: 2,
        sampleCircularEdges: [
          { source: 'src/a.ts', resolved: 'src/b.ts' },
        ],
        sampleUnresolvedEdges: [
          { source: 'src/c.ts', module: 'src/missing.js' },
        ],
      },
      scriptDuplication: {
        duplicateHelperClusterCount: 2,
        helperOccurrenceCounts: { check: 63, readText: 28, sha256Text: 0 },
        jscpdCloneCount: 17,
        jscpdDuplicatedLines: 439,
        jscpdDuplicatedTokens: 2979,
        jscpdDuplicatedPercentage: 1.043871121150874,
        jscpdTopClonePairs: [
          {
            firstFile: 'scripts/product-dead-export-candidates.ts',
            secondFile: 'scripts/product-dependency-topology.ts',
            firstStartLine: 217,
            firstEndLine: 240,
            secondStartLine: 160,
            secondEndLine: 183,
            lines: 24,
            tokens: 122,
          },
        ],
      },
    })

    expect(report.status).toBe('remediation_queue_required')
    expect(report.queueItems.map((item) => item.queueId).slice(0, 3)).toEqual([
      'static-analysis-new-dependency-violations',
      'static-analysis-dead-export-runtime-guards',
      'static-analysis-duplicate-helper-clusters',
    ])
    expect(report.queueItems.find((item) => item.queueId === 'static-analysis-new-dependency-violations')?.priority).toBe('P0')
    expect(report.queueItems.find((item) => item.queueId === 'static-analysis-dead-export-runtime-guards')?.validationCommands).toContain('bun run product:dead-export-candidates')
    expect(report.queueItems.find((item) => item.queueId === 'static-analysis-dead-export-runtime-guards')?.validationCommands).toContain('bun test src/services/api/providerConfig.runtimeCodexCredentials.test.ts src/utils/geminiCredentials.test.ts')
    expect(report.queueItems.find((item) => item.queueId === 'static-analysis-duplicate-helper-clusters')?.safeFirstStep).toContain('shared helper')
    expect(report.evidenceChecks.every((item) => item.ok)).toBe(true)
    expect(report.cleanupCompletionClaimAllowed).toBe(false)
    expect(report.topologyCleanClaimAllowed).toBe(false)
    expect(report.refactorCompletionClaimAllowed).toBe(false)
  })

  test('writes JSONL records for queue items', () => {
    const report = buildStaticAnalysisRemediationQueue({
      repository: 'svy04/metaforge',
      sourceCommit: 'b'.repeat(40),
      generatedFrom: ['fixture'],
      deadExport: {
        candidateFileCount: 1,
        candidateUnusedExportCount: 1,
        candidateUnusedTypeCount: 0,
        candidateDuplicateExportCount: 0,
        triageRecords: [
          {
            file: 'src/example.ts',
            symbol: 'unusedExport',
            action: 'review_for_removal',
            currentCandidate: true,
          },
        ],
      },
      dependencyTopology: {
        circularDependencyCount: 0,
        unresolvedDependencyCount: 0,
        configuredRatchetNewViolationCount: 0,
        sampleCircularEdges: [],
        sampleUnresolvedEdges: [],
      },
      scriptDuplication: {
        duplicateHelperClusterCount: 0,
        helperOccurrenceCounts: { check: 0, readText: 0, sha256Text: 0 },
        jscpdCloneCount: 0,
        jscpdDuplicatedLines: 0,
        jscpdDuplicatedTokens: 0,
        jscpdDuplicatedPercentage: 0,
        jscpdTopClonePairs: [],
      },
    })

    const records = buildStaticAnalysisRemediationQueueJsonl(report)
      .trim()
      .split('\n')
      .map((line) => JSON.parse(line))

    expect(records).toHaveLength(report.queueItems.length)
    expect(records.every((record) => record.kind === 'static_analysis_remediation_queue_item')).toBe(true)
    expect(records.map((record) => record.queueId)).toEqual(report.queueItems.map((item) => item.queueId))
  })

  test('does not reopen runtime-guarded credential candidates as unresolved P1 queue work', () => {
    const credentialRuntimeGuardCommand =
      'bun test src/services/api/providerConfig.runtimeCodexCredentials.test.ts src/utils/geminiCredentials.test.ts'
    const report = buildStaticAnalysisRemediationQueue({
      repository: 'svy04/metaforge',
      sourceCommit: 'c'.repeat(40),
      generatedFrom: [
        'docs/product-quality/dead-export-candidates-report.json',
        'docs/product-quality/dependency-topology-report.json',
        'docs/product-quality/script-duplication-audit-report.json',
      ],
      deadExport: {
        candidateFileCount: 2,
        candidateUnusedExportCount: 2,
        candidateUnusedTypeCount: 0,
        candidateDuplicateExportCount: 0,
        triageRecords: [
          {
            file: 'src/services/api/providerConfig.ts',
            symbol: 'resolveStoredCodexCredentials',
            action: 'runtime_guarded',
            currentCandidate: true,
            resolvedEvidence: {
              state: 'resolved_with_runtime_guard',
              validationCommands: [credentialRuntimeGuardCommand],
              evidencePaths: ['src/services/api/providerConfig.runtimeCodexCredentials.test.ts'],
              checkedBehaviors: ['stored Codex credentials preserve explicit auth path and avoid sync secure-storage reads'],
              claimBoundary: 'Runtime guard evidence does not authorize deletion.',
            },
          },
          {
            file: 'src/utils/geminiCredentials.ts',
            symbol: 'clearGeminiAccessToken',
            action: 'runtime_guarded',
            currentCandidate: true,
            resolvedEvidence: {
              state: 'resolved_with_runtime_guard',
              validationCommands: [credentialRuntimeGuardCommand],
              evidencePaths: ['src/utils/geminiCredentials.test.ts'],
              checkedBehaviors: ['Gemini credential clearing removes only Gemini token state'],
              claimBoundary: 'Runtime guard evidence does not authorize deletion.',
            },
          },
          {
            file: 'src/bridge/sessionRunner.ts',
            symbol: '_extractActivitiesForTesting',
            action: 'review_for_removal',
            currentCandidate: true,
          },
        ],
      },
      dependencyTopology: {
        circularDependencyCount: 0,
        unresolvedDependencyCount: 0,
        configuredRatchetNewViolationCount: 0,
        sampleCircularEdges: [],
        sampleUnresolvedEdges: [],
      },
      scriptDuplication: {
        duplicateHelperClusterCount: 0,
        helperOccurrenceCounts: { check: 0, readText: 0, sha256Text: 0 },
        jscpdCloneCount: 0,
        jscpdDuplicatedLines: 0,
        jscpdDuplicatedTokens: 0,
        jscpdDuplicatedPercentage: 0,
        jscpdTopClonePairs: [],
      },
    })

    expect(report.queueItems.some((item) => item.queueId === 'static-analysis-dead-export-runtime-guards')).toBe(false)
    expect(report.queueItems.map((item) => item.queueId)).toContain('static-analysis-dead-export-removal-review')
    expect(report.evidenceChecks.find((item) => item.label === 'runtime-guarded dead-export candidates carry linked validation evidence')?.ok).toBe(true)
    expect(report.evidenceChecks.find((item) => item.label === 'runtime-guarded dead-export candidates stay out of unresolved P1 queue')?.ok).toBe(true)
  })
})
