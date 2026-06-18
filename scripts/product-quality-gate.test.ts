import { describe, expect, test } from 'bun:test'

import { manifestCoversSourceControlledEvidence } from './product-quality-gate'

describe('product quality gate manifest evidence contract', () => {
  test('accepts source-controlled evidence without requiring ignored report JSONL artifacts', () => {
    expect(manifestCoversSourceControlledEvidence(
      [
        'docs/product-quality/oss-comparison-readiness-index-report.json',
        'docs/product-quality/oss-comparison-readiness-index-report.md',
      ],
      [],
      [
        'docs/product-quality/oss-comparison-readiness-index-report.json',
        'docs/product-quality/oss-comparison-readiness-index-report.md',
      ],
    )).toBe(true)
  })

  test('rejects missing source-controlled evidence or missing required paths', () => {
    expect(manifestCoversSourceControlledEvidence(
      ['docs/product-quality/oss-comparison-readiness-index-report.json'],
      [],
      [
        'docs/product-quality/oss-comparison-readiness-index-report.json',
        'docs/product-quality/oss-comparison-readiness-index-report.md',
      ],
    )).toBe(false)

    expect(manifestCoversSourceControlledEvidence(
      [
        'docs/product-quality/oss-comparison-readiness-index-report.json',
        'docs/product-quality/oss-comparison-readiness-index-report.md',
      ],
      ['docs/product-quality/missing-report.json'],
      [
        'docs/product-quality/oss-comparison-readiness-index-report.json',
        'docs/product-quality/oss-comparison-readiness-index-report.md',
      ],
    )).toBe(false)
  })
})
