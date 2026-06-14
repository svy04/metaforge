# Phase 2 Plan — Opus Skeptic

**Goal**: GPT Implementer가 한 turn의 응답을 마치면 Opus 4.7을 read-only Skeptic으로 호출 → DissentReport 파싱 → 별도 system 메시지로 사용자에게 표시.

**Approach**: TDD discipline. 각 task = RED 테스트 추가 → 실행해서 fail 확인 → 최소 GREEN 구현 → 테스트 pass → 회귀 테스트 → (디렉토리가 git 저장소이면) 커밋.

**Decisions locked from SPEC user-approval**:
- Q1=B: turn당 1번 호출, tool round-trip 중간엔 skip.
- Q2=skip: 도구만 쓰고 텍스트 응답 거의 없는 turn에서 skeptic 안 돌아도 됨.
- Q3=동의: severity `'block'`은 시각 경고만. 실제 차단은 Phase 4.
- Q4=주입 안 함: dissent를 다음 turn GPT prompt에 끼우지 않음. 순수 표시.
- Q5=한국어 강제: skeptic system prompt에 한국어 답변 명시. JSON 필드는 그대로 한국어 자유 텍스트.

## Task Breakdown

### Task 2.1 — usageLog role enum에 `'skeptic'` 추가

**REQ**: M2-04 (usage log) 의 전제.

**Why first**: 가장 작은 변경, skeptic.ts와 orchestrator.ts에서 모두 의존하므로 먼저.

**TDD Steps**:
1. **RED**: `src/services/orchestra/usageLog.test.ts`(없으면 신규)에:
   - `recordOrchestraUsageEvent({ role: 'skeptic', model: 'claude-opus-4-7', status: 'started' })` 호출 후 jsonl 파일 마지막 라인에 `"role":"skeptic"` 포함 단언.
   - 또는 컴파일러 단언만으로도 충분: 타입 시스템이 `'skeptic'`을 받게.
2. **GREEN**: `usageLog.ts:9` `role: 'planner' | 'implementer'` → `role: 'planner' | 'implementer' | 'skeptic'`.
3. **REFACTOR**: 주석에 v0.2 의의 한 줄 추가.

**Acceptance**: `bun test src/services/orchestra/usageLog.test.ts` 통과 (또는 빌드 통과).

**Files**:
- `src/services/orchestra/usageLog.ts` — 타입 확장
- `src/services/orchestra/usageLog.test.ts` — 신규 (또는 기존 확장)

### Task 2.2 — `skeptic.ts` 신설

**REQ**: M2-01, M2-02, M2-03.

**Public surface**:
```typescript
export type DissentReport = {
  headline: string
  risks: string[]
  questionedAssumptions: string[]
  scopeDrift: string[]
  severity: 'info' | 'caution' | 'block'
}

export const EMPTY_DISSENT: DissentReport

export function parseDissentReport(text: string): DissentReport
export function buildSkepticPrompt(params: SkepticPromptParams): string
export function buildClaudeLoginSkepticRequest(params: { model: string; prompt: string }): SkepticRequest
export async function callOpusSkeptic(params: SkepticParams): Promise<DissentReport>
export function formatDissent(report: DissentReport): string
export function dissentSeverityToMessageLevel(severity): 'info' | 'warning' | 'error'
```

**SkepticPromptParams** (read-only inputs):
```typescript
type SkepticPromptParams = {
  messages: OrchestraMessage[]   // 마지막 user intent + last assistant text 추출용
  systemPrompt: SystemPrompt | string
  userContext: Record<string, string>
  plannerAdvisory?: OrchestraAdvisory  // optional, 같은 turn의 planner 출력을 참조 가능
}
```

**System prompt 골자** (한국어 출력 강제):
```
You are Claude Opus 4.7 acting as the opposition party (야당) in an orchestra.
The visible lead Codex/GPT has just produced a response. Your role is read-only critique.
You have NO tool access and MUST NOT propose code edits — only highlight risks,
questioned assumptions, and scope drift. Output JSON ONLY in Korean.

Return this exact JSON shape:
{"headline":"","risks":[],"questionedAssumptions":[],"scopeDrift":[],"severity":"info|caution|block"}

Rules:
- All string values MUST be in Korean (한국어).
- Use empty arrays + headline "유의미한 이견 없음" if you genuinely have no dissent.
- severity: "info" = 참고, "caution" = 주의 권장, "block" = 명백한 결함 의심 (P4가 실제 차단을 결정).
```

**TDD Steps**:
1. **RED**: `src/services/orchestra/skeptic.test.ts` 신규.
   Tests:
   - `parseDissentReport('{"headline":"x","risks":["a"],"questionedAssumptions":[],"scopeDrift":[],"severity":"caution"}')` → 정확한 구조 단언.
   - `parseDissentReport('```json\n{"headline":"x"}\n```')` — fenced JSON도 파싱 (planner와 동일 helper 재사용).
   - `parseDissentReport(' {"headline":"x","severity":"weird"} ')` → severity invalid → fallback `'info'`.
   - `parseDissentReport('not json')` → throw.
   - `buildSkepticPrompt({...})` 반환 문자열에 "read-only", "야당", "Korean" 포함.
   - `buildSkepticPrompt({...})`이 마지막 assistant text가 있으면 prompt에 그것을 포함.
   - `buildClaudeLoginSkepticRequest({ model: 'claude-opus-4-7', prompt: '...' })` 반환에:
     - `system`에 "read-only" 포함, "JSON ONLY" 포함.
     - `betas`에 OAUTH_BETA_HEADER 포함 (effort beta는 opus 모델일 때만).
     - `output_config.effort === 'max'` (opus-4-7).
   - `callOpusSkeptic` — `sideQuery` mock으로 호출 시 `forceFirstParty: true`, `querySource: 'orchestra_skeptic'`, **tools 인자 없음** 단언.
   - `callOpusSkeptic` — non-claude model id 들어오면 throw.
   - `callOpusSkeptic` — OAuth 토큰 없으면 throw.
   - `formatDissent({ headline: 'X', risks: ['r1'], severity: 'caution', ... })` — `[Opus 4.7 야당]` 헤더 + 섹션 포함.
   - `formatDissent`(완전히 빈 dissent) → 한 줄 압축 (예: `[Opus 4.7 야당] 유의미한 이견 없음`).
   - `dissentSeverityToMessageLevel('info')` → `'info'`, `'caution'` → `'warning'`, `'block'` → `'error'`.

2. **GREEN**: `src/services/orchestra/skeptic.ts` 작성.
   - `parseDissentReport`: planner의 `extractJson` 패턴 재사용 (helper export 또는 복사).
   - severity invalid → `'info'` 폴백.
   - `buildSkepticPrompt`: `compactContext` + `latestUserIntent` 패턴 재사용 (orchestrator.ts에서 export하지 않은 경우 export로 노출).
   - `callOpusSkeptic`: `callClaudeLoginPlanner`를 거의 mirror하되:
     - `querySource: 'orchestra_skeptic'`
     - `system` 문자열 다름 (read-only critique)
     - `messages[0].content`도 다름 (skeptic prompt)
   - `formatDissent`: SPEC의 표시 포맷 그대로.

3. **REFACTOR**:
   - planner와 skeptic 공유 helper (`extractJson`, `latestUserIntent`, `compactContext`)는 별도 파일 `orchestraPromptUtils.ts`로 추출 — 또는 orchestrator.ts에서 export.

**Acceptance**: `bun test src/services/orchestra/skeptic.test.ts` 모두 pass.

**Files**:
- `src/services/orchestra/skeptic.ts` — NEW
- `src/services/orchestra/skeptic.test.ts` — NEW
- `src/services/orchestra/orchestrator.ts` — helper export (필요 시)

### Task 2.3 — orchestrator wrapper `buildSkepticDissent`

**REQ**: M2-04 (usage log + best-effort).

**Why**: planner의 `buildOrchestraGuidance` 패턴 그대로, skeptic 호출 + usage log + 실패 시 graceful degrade.

**Public surface**:
```typescript
export type SkepticDispatchParams = {
  messages: OrchestraMessage[]
  systemPrompt: SystemPrompt | string
  userContext: Record<string, string>
  settings: Pick<SettingsJson, 'orchestra'> | null | undefined
  signal?: AbortSignal
  toolUseContext?: ToolUseContext
  querySource: string
  turnCount: number
  agentId?: string
  plannerAdvisory?: OrchestraAdvisory
  skeptic?: typeof callOpusSkeptic        // injectable for tests
  recordUsageEvent?: OrchestraUsageRecorder
}

export type SkepticDispatchResult = {
  systemMessage?: SystemInformationalMessage   // 사용자에게 yield할 system 메시지
  diagnostic?: string                          // logForDebugging 용
  dissent?: DissentReport                      // 후속 phase에서 활용 가능
}

export async function buildSkepticDissent(params: SkepticDispatchParams): Promise<SkepticDispatchResult>

// 그리고 query.ts가 호출할 wrapper:
export async function createOrchestraSkepticDissent(params: { ... }): Promise<SkepticDispatchResult>
```

**Behavior**:
- `shouldRunOrchestra` 동일 게이트 통과 시만 호출 (안 통과면 `{}` 반환). agent subturn / planner self-recursion 방지 동일.
- `recordOrchestraUsageEvent({ role: 'skeptic', status: 'started' })` 발사.
- skeptic 호출 → 성공 시 `succeeded`, 실패 시 `failed` 기록.
- 성공 시 `formatDissent` + `createSystemMessage(text, level)` 반환.
- 실패 시 `systemMessage: undefined` + `diagnostic` only — GPT 응답 차단 안 함.

**TDD Steps**:
1. **RED**: `src/services/orchestra/orchestrator.test.ts`에 추가 또는 `skeptic.test.ts`에 통합 테스트:
   - `buildSkepticDissent` mock skeptic이 dissent 반환 시 `systemMessage` 정의된 객체 반환, level이 severity에서 매핑됨.
   - mock skeptic이 throw 시 `systemMessage: undefined`, `diagnostic` 존재.
   - `recordUsageEvent`가 `started` + (`succeeded` | `failed`) 두 번 호출됨.
   - agent subturn (`agentId: 'sub-1'`) → 호출 안 됨 (`{}` 반환).
   - `querySource: 'orchestra_skeptic'` 자기 호출 방지 (재귀 차단).
2. **GREEN**: `orchestrator.ts`에 `buildSkepticDissent` 추가, planner의 패턴 mirror.
3. **REFACTOR**: planner/skeptic 공통 dispatch shape — 너무 ambitious하면 Phase 3에 미룸.

**Acceptance**: 단위 테스트 pass.

**Files**:
- `src/services/orchestra/orchestrator.ts` — `buildSkepticDissent`, `createOrchestraSkepticDissent` 추가
- `src/services/orchestra/orchestrator.test.ts` — 추가 테스트
- `src/services/orchestra/skeptic.ts` — `dissentSeverityToMessageLevel` import to orchestrator

### Task 2.4 — `deps.ts` + `query.ts` hook (turn-end skeptic)

**REQ**: M2-01, M2-04.

**Why**: 사용자에게 "응답 완료" 시점에 skeptic 메시지를 yield하는 실제 통합 지점.

**Hook 위치 상세** (Option B 구현):

`query.ts`의 `for await (const message of deps.callModel(...))` 루프 안에서, assistant message가 yield된 직후, 그 message에 `tool_use` 블록이 *없으면* turn 응답 완료로 간주. turn-keyed dedup (`lastSkepticTurn < turnCount`)로 같은 turn 중복 호출 방지.

**Pseudocode** (실제 위치는 callModel for-loop 안):
```typescript
yield message  // 기존 assistant message yield

if (message.type === 'assistant') {
  const hasToolUse = message.message.content.some(b => b.type === 'tool_use')
  if (!hasToolUse && lastSkepticTurn < turnCount) {
    lastSkepticTurn = turnCount
    const skepticResult = await deps.skepticDissent({
      messages: messagesForModel,
      systemPrompt: fullSystemPrompt,
      userContext,
      settings: appState.settings,
      querySource: querySourceText,
      turnCount,
      agentId: toolUseContext.agentId,
      signal: toolUseContext.abortController.signal,
      toolUseContext,
    })
    if (skepticResult.diagnostic) logForDebugging(skepticResult.diagnostic)
    if (skepticResult.systemMessage) yield skepticResult.systemMessage
  }
}
```

**TDD Steps**:
1. **RED**: `src/query/orchestra.test.ts`(이미 존재) 또는 신규 `query/skeptic.test.ts`에 테스트:
   - 단일 turn: 사용자 prompt → callModel이 tool_use 없는 assistant message 1개 yield → skeptic 1번 호출 + system 메시지 yield 단언.
   - 도구 호출 turn: callModel이 tool_use 있는 메시지를 먼저 yield → skeptic 미호출. 이어서 tool 결과 후 tool_use 없는 assistant message → skeptic 1번 호출.
   - 동일 turn에 tool_use 없는 메시지 2개 (recovery 등) → skeptic 1번만 호출 (turn-keyed dedup).
   - skepticDissent throw → query 본문 yield 정상 진행, skeptic 메시지는 yield 안 됨.
   - `agentId: 'sub-1'` → skeptic 미호출.
2. **GREEN**:
   - `src/query/deps.ts`에 `skepticDissent: typeof createOrchestraSkepticDissent` 추가.
   - `productionDeps()`에 `skepticDissent: createOrchestraSkepticDissent` 와이어.
   - `query.ts`에 `lastSkepticTurn` state + 위 hook 추가.
3. **REFACTOR**: hook이 callModel 루프 본체를 어지럽히면 helper로 추출.

**Acceptance**: 단위 테스트 + 빌드 통과.

**Files**:
- `src/query/deps.ts` — 신규 dep 필드
- `src/query.ts` — hook 삽입 + state 변수
- `src/query/orchestra.test.ts` 또는 신규 — 테스트

### Task 2.5 — Live multi-turn probe

**REQ**: M2-01..04 통합 검증.

**TDD Steps** (스크립트 자체가 테스트):
1. **RED**: 명령 실행 전, jsonl에 skeptic 라인 0개 단언 (수동).
2. **GREEN**: 라이브 프로브 실행:
   ```powershell
   Set-Location "<repo>"
   bun run build
   "OpenClaude Phase 2 검증. src/query.ts 안에서 lastOrchestraGuidanceTurn이 어떻게 쓰이는지 한국어로 한 문단 설명해줘." `
     | node dist/cli.mjs -p --output-format json --no-session-persistence --max-turns 3
   ```
3. **VERIFY**:
   - `Get-Content "$env:USERPROFILE\.claude\orchestra-usage.jsonl" -Tail 30`
   - 매 turn에 `"role":"planner"`와 `"role":"skeptic"` 둘 다 `started → succeeded` 라인 존재 확인.
   - jsonl output(stdout)에서 `type:"system"` 메시지에 "Opus 4.7 야당" 헤더 포함 확인.
4. **REFACTOR**: 필요 시 `scripts/probe-orchestra-skeptic.ts` 신설 (Phase 1 패턴 따라). MVP에서는 수동 명령으로 충분.

**Acceptance**: 라이브 프로브에서 위 3개 검증 모두 통과.

## Execution Order

```
Task 2.1 (usageLog role)       — 단독, 가장 작음
   ↓
Task 2.2 (skeptic.ts)          — 2.1에 의존 (role enum)
   ↓
Task 2.3 (orchestrator wrapper) — 2.2에 의존
   ↓
Task 2.4 (query.ts hook)       — 2.3에 의존
   ↓
Task 2.5 (live probe)          — 모든 task 후
```

## Phase Done Definition

- [ ] Task 2.1 빌드 + 테스트 pass
- [ ] Task 2.2 skeptic.test.ts 모든 항목 pass
- [ ] Task 2.3 orchestrator.test.ts 추가 항목 pass
- [ ] Task 2.4 query 통합 테스트 pass + `bun run build` 성공
- [ ] Task 2.5 라이브 프로브: 3턴 모두 planner+skeptic 기록 + 사용자 stdout에 dissent 메시지 보임
- [ ] PROJECT.md M2 → Validated 이동
- [ ] ROADMAP.md Phase 2 row → ✓ Verified

## Threats & Mitigations

| Threat | Mitigation |
|--------|------------|
| Skeptic latency가 per-turn 5-15s 추가 → 사용자 응답 후 또 기다림 | best-effort로 yield system 메시지 분리. Phase 2 MVP는 직렬, 병렬화는 후속 phase에서 평가 |
| OAuth 토큰 만료 시 매 turn skeptic 실패 메시지 폭주 | 실패는 diagnostic만, 사용자 메시지 yield 안 함 |
| `compactContext` / `latestUserIntent` helper가 orchestrator.ts에만 있어 import 사이클 위험 | Task 2.2 REFACTOR에서 별도 파일로 추출하거나 orchestrator.ts에서 export |
| query.ts hook이 stream 루프 안에 있어 streaming fallback 등 복잡 경로에 영향 | Task 2.4 RED 테스트에 streamingFallback 케이스 추가 — message yield 직후 hook이 정확히 1번만 fire되는지 단언 |
| 도구만 쓰는 turn에서 영원히 skeptic 안 도는 corner case | SPEC Q2 결정에 따라 허용. 후속 phase에서 모니터링 후 필요 시 정책 변경 |
| 디렉토리가 git 저장소 아니면 atomic commit 불가 | `git status` 확인. 비-git이면 commit 단계 skip하고 chunked verification만 수행 |
