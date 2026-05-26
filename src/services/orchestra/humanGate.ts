import type { EvidenceMatrix, EvidenceVerdict } from './evidenceArbiter.js'

/**
 * Phase 4 Human Gate — render the EvidenceMatrix as a single human-readable
 * SystemInformationalMessage so the user can act via slash commands.
 *
 * D3=a+c: this module produces text only. The OpenClaude main loop picks up
 * the user's next prompt (e.g. `/orchestra-apply gpt-a`) and dispatches the
 * registered promotion command.
 */

const HEADER = '[Phase 4 Human Gate]'

function checkmark(pass: boolean): string {
  return pass ? '✓' : '✗'
}

function renderEvidenceLines(v: EvidenceVerdict): string[] {
  const e = v.evidence
  return [
    `- 테스트: ${checkmark(e.testsRan.pass)} ran=${e.testsRan.ran}` +
      (e.testsRan.passed !== undefined ? `, passed=${e.testsRan.passed}` : '') +
      (e.testsRan.evidencePath ? `, evidence=${e.testsRan.evidencePath}` : ''),
    `- diff 최소성: ${checkmark(e.diffMinimal.pass)} ${e.diffMinimal.lineCount} / ${e.diffMinimal.under} lines`,
    `- scope 준수: ${checkmark(e.scopeFit.pass)} ${e.scopeFit.keywordsMatched}/${e.scopeFit.keywordsTotal} keywords`,
    `- rollback: ${checkmark(e.rollbackable.pass)} branchIsolated=${e.rollbackable.branchIsolated}`,
    `- 이해 가능성: ${checkmark(e.understandable.pass)} gptVerdict=${e.understandable.gptVerdict ?? 'unavailable'}`,
  ]
}

function recommendationsLine(matrix: EvidenceMatrix): string {
  if (matrix.topRecommended) {
    return `추천: ${matrix.topRecommended} (green)`
  }
  if (matrix.verdicts.every(v => v.recommendation === 'red')) {
    return '추천: 권장 안 함 — 모두 red. /orchestra-reject 권장.'
  }
  return '추천: green 후보 없음 — yellow 중 사용자 판단 필요.'
}

function commandLineFor(verdict: EvidenceVerdict): string {
  const tag =
    verdict.recommendation === 'green'
      ? '권장'
      : verdict.recommendation === 'yellow'
        ? '주의'
        : '거부 권장'
  const command =
    verdict.candidateLabel === 'opus-shadow'
      ? '/orchestra-apply opus-shadow --confirm-opus'
      : `/orchestra-apply ${verdict.candidateLabel}`
  const extra =
    verdict.candidateLabel === 'opus-shadow' ? '  (야당 — 추가 confirm)' : ''
  return `- ${command}   ← ${tag}${extra}`
}

export function formatHumanGateMessage(matrix: EvidenceMatrix): string {
  const lines: string[] = []
  lines.push(`${HEADER} ${recommendationsLine(matrix)}`)
  lines.push('')
  if (matrix.topRecommended) {
    const top = matrix.verdicts.find(
      v => v.candidateLabel === matrix.topRecommended,
    )
    if (top) {
      lines.push(`5축 evidence (${top.candidateLabel}):`)
      lines.push(...renderEvidenceLines(top))
      lines.push('')
    }
  }
  lines.push('승인 절차:')
  for (const verdict of matrix.verdicts) {
    lines.push(commandLineFor(verdict))
  }
  lines.push('- /orchestra-reject   ← 모든 후보 폐기')
  lines.push('')
  lines.push(
    'opus-shadow는 /orchestra-apply opus-shadow --confirm-opus로만 적용됩니다.',
  )
  return lines.join('\n')
}

export function humanGateMessageLevel(
  matrix: EvidenceMatrix,
): 'info' | 'warning' | 'error' {
  const tally = { green: 0, yellow: 0, red: 0 }
  for (const v of matrix.verdicts) tally[v.recommendation]++
  if (tally.green > 0) return 'info'
  if (tally.yellow > 0) return 'warning'
  return 'error'
}
