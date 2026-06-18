import { describe, expect, test } from 'bun:test'

import { evidenceManifestIncludesSourceControlledComparisonEvidence } from './product-oss-comparison-readiness-index'

describe('OSS comparison readiness evidence-manifest contract', () => {
  test('accepts source-controlled comparison report evidence without requiring ignored JSONL artifacts', () => {
    expect(evidenceManifestIncludesSourceControlledComparisonEvidence(
      [
        'docs/product-quality/oss-benchmark-comparison-matrix-report.json',
        'docs/product-quality/oss-comparison-readiness-index-report.json',
      ],
      [],
    )).toBe(true)
  })

  test('rejects missing source-controlled comparison evidence or missing required paths', () => {
    expect(evidenceManifestIncludesSourceControlledComparisonEvidence([], [])).toBe(false)
    expect(evidenceManifestIncludesSourceControlledComparisonEvidence(
      ['docs/product-quality/oss-benchmark-comparison-matrix-report.json'],
      ['docs/product-quality/missing-report.json'],
    )).toBe(false)
  })
})
