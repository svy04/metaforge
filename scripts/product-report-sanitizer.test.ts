import { describe, expect, test } from 'bun:test'
import { scrubPublicArtifactText, scrubPublicArtifactValue } from './product-report-sanitizer'

describe('product report public sanitizer', () => {
  const winHome = ['C:', 'Users', 'alice'].join('\\')
  const desktop = 'Desk' + 'top'
  const repoPath = [winHome, desktop, 'project space', 'openclaude-0.6.0'].join('\\')
  const posixRepoPath = ['C:', 'Users', 'alice', desktop, 'project-space', 'openclaude-0.6.0'].join('/')
  const worktreeRepoPath = [
    winHome,
    desktop,
    '한글 테스트 경로',
    'openclaude-worktrees',
    'public-feedback-static-proof',
  ].join('\\')
  const bunExePath = [winHome, 'AppData', 'Roaming', 'npm', 'node_modules', 'bun', 'bin', 'bun.exe'].join('\\')
  const winUserPrefix = ['C:', 'Users'].join('\\')
  const posixUserPrefix = ['C:', 'Users'].join('/')

  test('scrubs repo and tool paths from public report text', () => {
    const text = [
      `${repoPath}\\dist\\cli.mjs`,
      posixRepoPath,
      bunExePath,
    ].join('\n')

    const scrubbed = scrubPublicArtifactText(text)

    expect(scrubbed).toContain('<repo>\\dist\\cli.mjs')
    expect(scrubbed).toContain('<repo>')
    expect(scrubbed).toContain('<bun>')
    expect(scrubbed).not.toContain(winUserPrefix)
    expect(scrubbed).not.toContain(posixUserPrefix)
  })

  test('scrubs the current repo root before broader user-home placeholders', () => {
    const text = [
      `${worktreeRepoPath}\\dist\\cli.mjs --version`,
      `"cwd":"${worktreeRepoPath.replaceAll('\\', '\\\\')}"`,
    ].join('\n')

    const scrubbed = scrubPublicArtifactText(text, { repoRoot: worktreeRepoPath })

    expect(scrubbed).toContain('<repo>\\dist\\cli.mjs --version')
    expect(scrubbed).toContain('"cwd":"<repo>"')
    expect(scrubbed).not.toContain('<user-home>')
    expect(scrubbed).not.toContain('한글 테스트 경로')
    expect(scrubbed).not.toContain(winUserPrefix)
  })

  test('recursively scrubs public report values', () => {
    const report = {
      command: [
        bunExePath,
        `${repoPath}\\dist\\cli.mjs`,
      ],
      nested: {
        stdoutPreview: [
          `"cwd": "${repoPath.replaceAll('\\', '\\\\')}"`,
        ],
      },
      ok: true,
    }

    const scrubbed = scrubPublicArtifactValue(report)

    expect(scrubbed.command).toEqual(['<bun>', '<repo>\\dist\\cli.mjs'])
    expect(scrubbed.nested.stdoutPreview[0]).toContain('<repo>')
    expect(JSON.stringify(scrubbed)).not.toContain('C:\\\\Users')
    expect(scrubbed.ok).toBe(true)
  })
})
