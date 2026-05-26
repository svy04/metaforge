# Phase 4 Plan — Evidence Arbiter + Human Gate

**Goal**: Phase 3의 cross-review 매트릭스 + candidate diff/test 결과를 입력으로 받아 5축 fact-based 판정 → green/yellow/red verdict → Human Gate system 메시지(슬래시 커맨드 안내) → promote() 권한-검사 함수.

**Locked from SPEC default**:
- D1=c (evidence + pass/fail), D2=β (위험 가중), D3=a+c (system msg + slash cmd), D4=i+iii (코드 layer + promote 게이트), D5=γ+α (fact-based + GPT 모호 축).

## Tasks

### 4.1 — `evidenceArbiter.ts` (5축 fact-based + verdict)

**Public surface**:
```typescript
export type FiveAxisEvidence = {
  testsRan: { ran: boolean; passed?: boolean; evidencePath?: string }
  diffMinimal: { lineCount: number; under?: number; pass: boolean }
  scopeFit: { keywordsMatched: number; pass: boolean }
  rollbackable: { branchIsolated: boolean; pass: boolean }
  understandable: { gptVerdict?: 'pass' | 'fail'; pass: boolean }
}

export type EvidenceVerdict = {
  candidateLabel: ShadowLabel
  evidence: FiveAxisEvidence
  recommendation: 'green' | 'yellow' | 'red'
  rationale: string
}

export type EvidenceMatrix = {
  verdicts: EvidenceVerdict[]
  topRecommended?: ShadowLabel  // green이면 추천. 다 red면 undefined.
  generatedAt: string
}

export async function buildEvidenceMatrix(params: {
  candidates: ShadowCandidate[]
  crossReview: CrossReviewMatrix
  taskScope: { intent: string }
  understandableJudge?: UnderstandableJudgeFn  // GPT inject (D5=γ+α)
}): Promise<EvidenceMatrix>
```

**β verdict 매핑**:
- 테스트 fail OR scope fail → **red** 즉시
- 그 외 fail이 1개 이상 → **yellow**
- 모두 pass → **green**

**TDD**: 단위 테스트 mock candidate + cross-review로 5축 추출, verdict β 임계값 검증.

### 4.2 — `humanGate.ts` (system 메시지 + slash 안내)

**Public surface**:
```typescript
export function formatHumanGateMessage(matrix: EvidenceMatrix): string
export function dissentHumanGateLevel(matrix: EvidenceMatrix): 'info' | 'warning' | 'error'
```

메시지 형식:
```
[Phase 4 Human Gate] 추천: gpt-a (green)

5축 evidence:
- 테스트: ✓ ran=true, passed=true (path: ...)
- diff 최소성: ✓ 12 lines (under 100)
- scope 준수: ✓ matched 3 keywords
- rollback: ✓ shadow branch 격리
- 이해 가능성: ✓ GPT verdict = pass

승인 절차:
- /orchestra-apply gpt-a   ← 권장
- /orchestra-apply gpt-b   ← 대안
- /orchestra-apply opus-shadow  ← 야당 (추가 confirm)
- /orchestra-reject        ← 모두 폐기
```

red verdict면 'error' level + "권장 안 함" 명시.

### 4.3 — `promote.ts` (권한 검사 게이트)

**Public surface**:
```typescript
export type PromoteRequest = {
  candidateLabel: ShadowLabel
  candidates: ShadowCandidate[]
  evidenceMatrix: EvidenceMatrix
  /** Opus shadow 적용 시 사용자가 두 번째 confirm 통과했는지. */
  confirmedOpusShadow?: boolean
}

export type PromoteOutcome =
  | { ok: true; appliedLabel: ShadowLabel; diff: string }
  | { ok: false; reason: 'red-verdict' | 'opus-shadow-needs-confirm' | 'candidate-not-found' | 'candidate-failed' }

export function evaluatePromoteRequest(req: PromoteRequest): PromoteOutcome
```

**규칙** (D4=i+iii):
- candidate가 매트릭스에 없으면 → `candidate-not-found`
- candidate.status !== 'completed' → `candidate-failed`
- evidenceMatrix verdict가 'red' → `red-verdict` (사용자가 강제로 force flag 안 주면 거부)
- candidate.label === 'opus-shadow' && !confirmedOpusShadow → `opus-shadow-needs-confirm`
- 그 외 → `{ ok: true, appliedLabel, diff }`

실제 git apply는 별도 후속 — promote.ts는 **결정만** 반환. 적용 코드는 Task 4.6 (후속)에 명시.

### 4.4 — query.ts hook

Phase 3 shadow hook 다음에 evidenceArbiter 호출, humanGate 메시지 yield. shadowEnabled + shadow 매트릭스 존재 + 코드 변경 turn 조건. dedup `lastArbiterTurn`.

### 4.5 — 라이브 검증

OpenClaude(non-git) cwd: shadowEnabled false → arbiter도 fire 안 됨. graceful skip 그대로 입증.

## Done

- [ ] 4.1-4.3 단위 테스트 pass
- [ ] 4.4 통합 단위 테스트 pass
- [ ] 빌드 성공
- [ ] 라이브 graceful skip
- [ ] PROJECT.md M4 → 인프라 ✓

## Out of Scope (후속)
- 실제 git apply / cherry-pick 코드 (Task 4.6)
- 슬래시 커맨드 OpenClaude 등록 (Task 4.7) — 일단 system 메시지에 안내만
