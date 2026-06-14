# Phase 3 Plan — Shadow Executor + Cross Review

**Goal**: 코드 변경 turn에서 GPT-A primary + GPT-B alternative + Opus Shadow 3 후보를 git worktree로 격리 생성, GPT/Opus 두 reviewer가 평가한 cross-review 매트릭스를 stdout 요약 + `.planning/phase-3/cross-review-{ts}.md` 파일로 출력. main에는 변경 0 (Phase 4가 승격 결정).

**Approach**: TDD discipline. 각 task는 RED 테스트 → 최소 GREEN 구현 → 회귀 테스트.

**Locked from SPEC user-approval**:
- D1 = **A graceful skip**: git repo cwd면 worktree 사용, 아니면 silent skip + diagnostic.
- D2 = **β**: Edit/Write tool_use 포함된 turn 후에만 fire.
- D3 = **i**: Phase 3는 read-only 비교만. main 적용은 Phase 4.
- D4 = **c**: stdout 요약 + `.planning/phase-3/cross-review-{ts}.md` 파일.
- D5 = **직렬**: 5 model call 순차. async 최적화는 후속 phase.

**Implementation note**: 모든 git 호출은 코드베이스의 안전 wrapper `src/utils/execFileNoThrow.ts`를 경유한다 (shell injection 방지 + Windows 호환 + structured output).

## Task Breakdown

### Task 3.1 — `worktreeManager.ts` (git worktree life-cycle + skip detection)

**REQ**: M3-04 의 전제 (격리 인프라).

**Public surface**:
```typescript
export type WorktreeAvailability =
  | { ok: true; gitRoot: string }
  | { ok: false; reason: 'not-git' | 'git-not-found' | 'detached-bare' }

export function checkWorktreeAvailability(
  cwd: string,
  runner?: ExecFileRunner,
): Promise<WorktreeAvailability>

export type ShadowWorktree = {
  label: 'gpt-a' | 'gpt-b' | 'opus-shadow'
  path: string
  branch: string
  createdAt: string
}

export async function createShadowWorktrees(params: {
  gitRoot: string
  taskId: string
  runner?: ExecFileRunner
}): Promise<ShadowWorktree[]>

export async function pruneShadowWorktrees(params: {
  gitRoot: string
  runner?: ExecFileRunner
}): Promise<{ pruned: string[]; failed: string[] }>
```

`ExecFileRunner`는 `execFileNoThrow`의 result 시그니처를 가진 함수. 테스트에선 mock으로 inject.

**TDD Steps**:
1. **RED** — `worktreeManager.test.ts`:
   - `checkWorktreeAvailability` non-git 디렉토리 → `{ ok: false, reason: 'not-git' }` (mock runner가 git rev-parse exit 128 반환).
   - git 디렉토리 → `{ ok: true, gitRoot: ... }`.
   - `createShadowWorktrees` 3 worktree 메타 반환, 각 다른 label/branch.
   - mock runner: `git worktree add ...` 호출 3번 단언, 각 명령에 unique branch.
   - `pruneShadowWorktrees`가 stale 디렉토리 검출하고 `git worktree remove`로 cleanup.
2. **GREEN**: `worktreeManager.ts` 작성 — `execFileNoThrow` 래핑 헬퍼 사용.
   - branch: `openclaude-shadow/{taskId}/{label}`.
   - path: `{gitRoot}/.openclaude-shadows/{taskId}/{label}`.
3. **REFACTOR**: timeout/에러 매핑.

**Acceptance**: 단위 테스트 pass. 실제 git 호출 없이 mock runner로만 검증 가능.

**Files**:
- `src/services/orchestra/worktreeManager.ts` — NEW
- `src/services/orchestra/worktreeManager.test.ts` — NEW

### Task 3.2 — `shadowExecutor.ts` (3 candidate generation)

**REQ**: M3-01, M3-02.

**Public surface**:
```typescript
export type ShadowCandidate = {
  label: 'gpt-a' | 'gpt-b' | 'opus-shadow'
  worktreePath: string
  status: 'completed' | 'failed' | 'skipped'
  patchSummary?: string
  filesChanged?: string[]
  diff?: string                // capped 8KB
  error?: string
}

export type ShadowExecutionResult = {
  candidates: ShadowCandidate[]
  taskId: string
  durationMs: number
}

export async function runShadowExecutors(params: {
  taskScope: { intent: string; targetFiles?: string[] }
  worktrees: ShadowWorktree[]
  workers?: ShadowWorkerSet         // injectable for tests
  signal?: AbortSignal
}): Promise<ShadowExecutionResult>
```

3 worker 함수:
- `gptAWorker` — 현재 GPT-A 패턴 그대로
- `gptBWorker` — prompt에 "다른 접근으로 풀어라" 명시
- `opusShadowWorker` — Opus 4.7 OAuth path (callOpusSkeptic의 sideQuery 패턴 재사용)

**TDD Steps**:
1. **RED** — `shadowExecutor.test.ts`:
   - mock 3 worker 주입 → `runShadowExecutors`가 3 candidate 반환.
   - 각 candidate가 자기 worktree path와 label 매칭.
   - 한 worker throw → 그 candidate `status: 'failed'`, error 기록. 다른 2개 정상.
   - signal abort 시 모든 worker 중단 후 부분 결과.
2. **GREEN**: `shadowExecutor.ts` 작성. 직렬 호출 (D5).
3. **REFACTOR**: prompt 차별화 helper로 추출.

**Acceptance**: 단위 테스트 pass.

**Files**:
- `src/services/orchestra/shadowExecutor.ts` — NEW
- `src/services/orchestra/shadowExecutor.test.ts` — NEW

### Task 3.3 — `crossReview.ts` (3×2 matrix)

**REQ**: M3-03.

**Public surface**:
```typescript
export type ReviewerVerdict = {
  candidateLabel: 'gpt-a' | 'gpt-b' | 'opus-shadow'
  reviewer: 'gpt' | 'opus'
  scoresOutOf5: { correctness: number; minimality: number; scopeFit: number }
  verdict: 'green' | 'yellow' | 'red'
  rationale: string
}

export type CrossReviewMatrix = {
  candidates: ShadowCandidate[]
  verdicts: ReviewerVerdict[]   // 3×2 = 6 cells
  generatedAt: string
}

export async function buildCrossReviewMatrix(params: {
  candidates: ShadowCandidate[]
  reviewers?: { gpt: ReviewerFn; opus: ReviewerFn }
  signal?: AbortSignal
}): Promise<CrossReviewMatrix>

export function formatMatrixSummary(matrix: CrossReviewMatrix): string
export function formatMatrixDetail(matrix: CrossReviewMatrix): string
```

**TDD Steps**:
1. **RED** — `crossReview.test.ts`:
   - mock 2 reviewer 주입 → 6 verdict 반환.
   - 한 candidate가 `status: 'failed'` → 그 candidate verdict는 "execution_failed" placeholder.
   - `formatMatrixSummary` 한 줄 (3 verdict).
   - `formatMatrixDetail` markdown 표 + rationale.
2. **GREEN**: `crossReview.ts` 작성.
3. **REFACTOR**: severity → message level helper.

**Acceptance**: 단위 테스트 pass.

**Files**:
- `src/services/orchestra/crossReview.ts` — NEW
- `src/services/orchestra/crossReview.test.ts` — NEW

### Task 3.4 — usageLog role enum + config `shadowEnabled` toggle

**REQ**: M3-01..04 cross-cutting.

**TDD Steps**:
1. **RED**:
   - `usageLog.test.ts`에 `role: 'shadow-gpt-b' | 'shadow-opus' | 'cross-reviewer-gpt' | 'cross-reviewer-opus'` 받는 테스트.
   - `config.test.ts`에 `shadowEnabled: false` 기본 + v0.2-locked일 때도 사용자 명시 안 하면 false 단언.
2. **GREEN**:
   - `usageLog.ts` role enum 확장.
   - `config.ts` `shadowEnabled?: boolean` (default false). v0.2-locked는 *enable 강제하지 않음* — 비용/latency 보호 차원에서 사용자 의식적 opt-in.
3. **REFACTOR**: 주석에 v0.3 결정 후 default 변경 가능성 명시.

**Acceptance**: 단위 테스트 pass.

**Files**:
- `src/services/orchestra/usageLog.ts` / `usageLog.test.ts`
- `src/services/orchestra/config.ts` / `config.test.ts`
- `src/utils/settings/types.ts`

### Task 3.5 — query.ts hook (D2=β: 코드 변경 turn 후)

**REQ**: M3-01..04 통합.

**Hook 위치**: callModel for-loop 종료 후 + assistant final response 후 (skeptic hook 다음). 코드 변경 toolUse 발생한 turn 후만 fire.

```typescript
if (
  deps.shadowReview &&
  shadowEnabled &&
  hasMutationToolUseInTurn &&
  !toolUseContext.agentId &&
  lastShadowReviewTurn < turnCount
) {
  lastShadowReviewTurn = turnCount
  try {
    const shadowResult = await deps.shadowReview({ ... })
    if (shadowResult.summaryMessage) yield shadowResult.summaryMessage
    if (shadowResult.diagnostic) logForDebugging(shadowResult.diagnostic)
  } catch (e) {
    logForDebugging(`shadow review failed: ${e.message}`, { level: 'warn' })
  }
}
```

`hasMutationToolUseInTurn`은 turn 동안 본 tool_use 블록 중 mutating tool 이름(Edit/Write/NotebookEdit/MultiEdit)이 있었는지 트래킹.

**TDD Steps**:
1. **RED**: `src/query/shadow.test.ts`:
   - 코드 변경(Edit tool_use) turn 후 `shadowReview` 1번 호출.
   - 텍스트 응답만 turn → 미호출.
   - agentId → 미호출.
   - non-git → graceful skip (mock으로 worktree 비활성화).
   - shadowReview throw → query yield 정상.
2. **GREEN**: `query.ts`에 `lastShadowReviewTurn` + hook + helper.
3. **REFACTOR**: hook 길면 helper 추출.

**Acceptance**: 단위 테스트 pass + 빌드.

**Files**:
- `src/query/deps.ts` — `shadowReview?` dep
- `src/query.ts` — state + hook
- `src/query/shadow.test.ts` — NEW

### Task 3.6 — Live verification (graceful skip 입증)

**REQ**: M3-01..04 통합.

OpenClaude 빌드 디렉토리는 **non-git** → `checkWorktreeAvailability` "not-git" 반환 → Phase 3 graceful skip → diagnostic 로그만, jsonl shadow role 0개 (정상).

**Steps**:
1. `bun run build`
2. `"src/services/orchestra/dummy.ts에 'use strict' 한 줄 추가" | node dist/cli.mjs -p ...`
3. `Get-Content "<config-dir>/orchestra-usage.jsonl" -Tail 10` — `role:"shadow-*"` / `cross-reviewer-*` 라인 0개.
4. debug log 또는 stdout에 "Phase 3 skipped: not-git" 메시지 검증.

OpenClaude 자체는 git 아니므로 *실제 worktree 생성*은 라이브로 검증 못 함. 단위 테스트가 mock runner로 보증. 실 git 환경 검증은 Done Definition의 후속 항목.

## Execution Order

```
3.4 (config + usageLog enum)   — 가장 작음
   ↓
3.1 (worktreeManager)          — 인프라
   ↓
3.2 (shadowExecutor)           — 3.1 의존
   ↓
3.3 (crossReview)              — 3.2 의존
   ↓
3.5 (query.ts hook)            — 모든 의존
   ↓
3.6 (live skip verify)         — 통합
```

## Phase Done Definition

- [ ] 3.4 config + usageLog 단위 테스트 pass
- [ ] 3.1 worktreeManager 단위 테스트 pass (mock runner)
- [ ] 3.2 shadowExecutor 단위 테스트 pass (mock workers)
- [ ] 3.3 crossReview 단위 테스트 pass (mock reviewers)
- [ ] 3.5 query 통합 단위 테스트 pass
- [ ] 빌드 성공
- [ ] 라이브: OpenClaude(non-git) cwd에서 graceful skip 입증 (jsonl shadow role 0개 + diagnostic)
- [ ] PROJECT.md M3 → ✓ + 후속(실 git fixture에서 worktree 라이브 검증) 명시

## Threats & Mitigations

| Threat | Mitigation |
|--------|------------|
| OpenClaude self-modify trap | non-git이라 자동 skip; 별도 phase에서 self-bootstrap |
| worktree cleanup 실패 → 디스크 누수 | `pruneShadowWorktrees`를 매 turn 시작 전 실행; 명시적 슬래시 커맨드 후속 |
| 3 worker 직렬 호출 latency 30s+ | D5 직렬. async optimization 후속 |
| GPT-B prompt 차별화 약함 | shadowExecutor.test에 prompt 차이 단언; 정성적 차이는 v0.3 experiment에서 측정 |
| `shadowEnabled: false` default → 사용자 모르고 안 켜짐 | 명시적 toggle. v0.2-locked README 안내 후속 |
| Phase 3 hook 실패가 Phase 1-2까지 영향 | hook 전체 try/catch best-effort, query 본문 yield 절대 차단 안 함 |
| live verification 부분만 — 실 git fixture 미검증 | Done Definition에 후속 명시. Phase 3 부분 검증 표기 |
| 보안 — git 호출 인자에 사용자 입력 주입 | `execFileNoThrow` 사용 (shell injection 방지). 단위 테스트에 special-char taskId 인자도 단언 |
