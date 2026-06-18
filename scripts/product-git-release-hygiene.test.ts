import { describe, expect, test } from 'bun:test'
import { sanitizeGitCommandForPublicReport } from './product-git-release-hygiene'

describe('git release hygiene public report sanitization', () => {
  test('summarizes dirty git status entries instead of publishing local filenames', () => {
    const command = sanitizeGitCommandForPublicReport({
      name: 'status_short',
      command: ['git', 'status', '--short'],
      exitCode: 0,
      stdoutPreview: [
        ' M docs/product-quality/agent-instructions-quality-report.json',
        '?? reports/local-only.jsonl',
      ],
      stderrPreview: [],
    })

    expect(command.stdoutPreview).toEqual(['<git-status-short: 2 entries>'])
    expect(JSON.stringify(command)).not.toContain('agent-instructions-quality-report.json')
    expect(JSON.stringify(command)).not.toContain('reports/local-only.jsonl')
  })
})
