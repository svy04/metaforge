# Phase 2 Spec — Opus Skeptic (Post-Implementation Dissent)

**Status**: Draft — pending user review.
**Goal**: GPT Implementer가 한 turn의 응답을 마치면 Opus 4.7을 read-only Skeptic 모드로 호출해 dissent report를 만들고, 사용자에게 별도 system 메시지로 표시한다.

## What "Done" Means

1. 모든 user turn에서 (orchestra가 활성인 경우) GPT 응답이 완료된 직후 Opus Skeptic이 호출된다.
2. Skeptic은 read-only — 코드/파일 수정 도구를 절대 호출하지 않는다(차단 강제).
3. Skeptic의 dissent report는 사용자 stdout에 별도의 색상/형식 system 메시지로 표시된다.
4. `~/.claude/orchestra-usage.jsonl`에 `role: "skeptic"` 항목이 매 turn 기록된다 (started → succeeded/failed).
5. Skeptic 실패는 GPT 응답을 차단하지 않는다 — best-effort, 실패 시 warning만 stderr/diagnostic.
6. 단위 테스트 + 라이브 멀티턴 프로브 둘 다 통과.

## Skeptic Call Site Decision

> **결정 대상**: skeptic을 한 turn 안 어느 시점에 호출할지.

### Options Considered

| Option | When skeptic fires | Pro | Con |
|--------|--------------------|-----|-----|
| A. 매 callModel for-loop 종료 후 | 매 assistant message yield 직후 (tool round-trip마다) | 가장 자주 — 모든 중간 단계도 비판 | 한 turn에 N번 호출, 사용자 입장에서 시끄럽고 비용/지연 N배 |
| **B. tool_use 없는 마지막 assistant message yield 직후** | turn 응답이 사용자에게 "완료"로 보이는 순간 | 사용자가 "응답 받았다" 인지하는 시점과 1:1 매칭. turn당 1번. | 도구만 쓰고 끝나는 turn은 skeptic 안 돌 가능성 → 가드 필요 |
| C. while(true) loop의 Terminal transition | turn 완전 종료 시점 | 가장 명확한 boundary | Terminal hook이 이미 복잡 — 결합도 ↑ |

### Recommendation

**Option B를 default로 채택.** 사용자 경험 기준이 "응답을 봤다"이고, 도구 round-trip 중간에 끼어드는 skeptic은 잡음이다. turn-keyed dedup(`lastSkepticTurn < turnCount`)로 같은 turn에서 중복 호출 방지. 도구만 쓰고 끝나는 corner case는 추후 발견 시 처리.

## DissentReport Type Contract

OrchestraAdvisory(planner 출력)와 명확히 다른 타입.

```typescript
export type DissentReport = {
  // Skeptic이 한 줄로 표현하는 핵심 dissent. 사용자가 0.5초 안에 읽음.
  headline: string

  // 위험 지적: GPT 답변이 빠뜨렸거나 잘못 가정한 위험.
  risks: string[]

  // 가정 비판: GPT가 "당연한 듯" 한 가정 중 의심스러운 것.
  questionedAssumptions: string[]

  // Scope drift 경보: GPT 답이 사용자 요청 범위를 넘어선 부분.
  scopeDrift: string[]

  // Severity bucket: 'info' | 'caution' | 'block'. 사용자 표시 색상에 영향.
  severity: 'info' | 'caution' | 'block'
}
```

빈 배열 + headline = "no significant dissent"가 정상 출력. severity가 'block'이어도 자동 차단은 안 함 (Phase 4 Evidence Arbiter가 그 역할). Phase 2의 skeptic은 **순수 advisory/시각적 표시**.

## Read-Only Enforcement

Skeptic은 `callClaudeLoginPlanner` 패턴과 동일하게 `sideQuery`로 호출하되:

1. `tools` 인자를 넘기지 않음 — Claude OAuth API 호출에 tool 정의 자체가 없으니 도구 호출 불가.
2. system prompt에 명시: "Read-only critique. You have no tool access. Output JSON dissent report only."
3. 출력 파싱 시 도구 호출 흔적 (예: `<tool_use>` 같은 태그)가 있으면 무시하고 텍스트만 추출.

이는 "권한 강제"의 1단계 enforcement (입력 측). Phase 4에서 worktree/branch 격리가 추가될 때 2단계가 됨.

## User-Facing Display Format

`createSystemMessage(formatted, severity → level)` 사용. severity 매핑:
- `'info'` → level `'info'`
- `'caution'` → level `'warning'`
- `'block'` → level `'error'`

표시 텍스트 형식 (예시):

```
[Opus 4.7 야당] {headline}

⚠ Risks
  - {risk 1}
  - {risk 2}

? Questioned Assumptions
  - {assumption 1}

📍 Scope Drift
  - {drift 1}
```

빈 배열 섹션은 생략. 전체가 비어 있고 headline만 "No significant dissent"면 한 줄로 압축 표시.

## Files to Add / Modify

| File | Mode | What |
|------|------|------|
| `src/services/orchestra/skeptic.ts` | NEW | `callOpusSkeptic`, `parseDissentReport`, `formatDissent`, `buildSkepticPrompt` |
| `src/services/orchestra/skeptic.test.ts` | NEW | RED tests for parser, prompt build, read-only contract, severity mapping |
| `src/services/orchestra/orchestrator.ts` | MODIFY | export `buildSkepticDissent` (planner와 평행) — usage log + best-effort 처리 |
| `src/services/orchestra/orchestrator.test.ts` | MODIFY | skeptic dispatch 테스트 추가 |
| `src/services/orchestra/usageLog.ts` | MODIFY | `role` enum에 `'skeptic'` 추가 |
| `src/services/orchestra/usageLog.test.ts` | MODIFY (or create) | 새 role 기록 테스트 |
| `src/query.ts` | MODIFY | turn 종료 hook 추가 — 마지막 assistant message + skeptic 호출 + system 메시지 yield |
| `src/query/deps.ts` | MODIFY | `skepticDissent: typeof buildSkepticDissent` 추가 (테스트 mock 가능) |

## Acceptance / Verification

### Unit Tests (must pass)

1. `parseDissentReport` — JSON 파싱 + 누락 필드 default 처리 + 잘못된 severity → `'info'`로 떨어짐.
2. `buildSkepticPrompt` — system prompt에 "read-only" 문구 포함, 사용자 의도 + 마지막 assistant 응답이 prompt에 들어감.
3. `callOpusSkeptic` — `sideQuery`에 `forceFirstParty:true`, `querySource:'orchestra_skeptic'` 전달, tools 인자 없음 단언.
4. `formatDissent` — severity별로 적절한 level 매핑, 빈 dissent는 한 줄 압축.
5. `usageLog` — `role: 'skeptic'`이 타입 안전하게 기록됨.
6. `query.ts` flow — mock skeptic이 turn당 1번만 호출됨 (tool round-trip이 여러 번이어도). best-effort 실패 시 GPT 응답 yield 안 막힘.

### Live Probe

```powershell
"orchestra v0.2 phase 2 skeptic 검증을 위해 src/query.ts에서 작은 함수 하나만 grep해줘"   |
  node dist/cli.mjs -p --output-format json --no-session-persistence --max-turns 5
```

검증 항목:
- `Get-Content "<config-dir>/orchestra-usage.jsonl" -Tail 30` →
  매 turn에 `role:"planner"` 와 `role:"skeptic"` 둘 다 `started → succeeded` 기록.
- 사용자 stdout에 `[Opus 4.7 야당]` 헤더가 들어간 system 메시지가 보임 (jsonl output에서는 `type:"system", subtype:"info|warning|error"` 항목으로).
- skeptic 호출 latency가 turn당 5-15초 추가되는지 측정 (REQ R1 위험에 적힘).

## Open Questions (사용자 검토 시 결정 필요)

1. **Q1 — Skeptic 호출 빈도**: Option B(turn당 1번, tool round-trip 중간 skip)로 진행해도 되나? 아니면 Option A(매 round-trip)가 야당 정신에 더 충실?
2. **Q2 — 도구만 쓰고 끝나는 turn**: 사용자가 "파일 X 수정해" 같은 명령으로 GPT가 도구만 호출하고 응답 텍스트가 거의 없는 turn에서도 skeptic이 돌아야 하나? (Option B의 corner)
3. **Q3 — Severity 'block'의 의미**: Phase 2에서는 시각적 경고만, 실제 차단은 Phase 4에서 추가. 동의?
4. **Q4 — Skeptic 출력의 prompt 영향**: dissent report를 다음 turn의 GPT prompt에 (memory candidate처럼) 주입할지, 순수 사용자 표시용으로 둘지? Default 권장 = **사용자 표시만, prompt 무영향** (Phase 4까지는 GPT가 dissent를 "보지 않게" 유지해서 순수 야당 비교군 보존).
5. **Q5 — 한국어 prompt**: skeptic system prompt에 영어로만 쓸지, 한국어 강제할지? 현재 planner는 영어 JSON. dissent 텍스트는 한국어로 받고 싶으면 prompt에 명시 필요.

이 5개 답을 받은 후 PLAN.md를 작성.

## Risks / Threats

| Risk | Mitigation |
|------|------------|
| Skeptic이 latency 5-15초 추가 → 사용자 답변 후에도 또 기다림 | best-effort: skeptic 결과를 별도 메시지로 yield하되 GPT 응답 stream을 기다리지 않음. 또는 skeptic을 stream과 병렬로 시작해 응답 후 join. (Phase 2 MVP는 직렬 OK, 병렬화는 후속) |
| Skeptic이 잘못 파싱돼 빈 dissent → 사용자 매 turn 무의미한 메시지 | parseDissentReport 실패 시 그 turn은 skeptic 메시지 yield 안 함 + diagnostic 로그 |
| 도구만 쓰고 끝나는 turn에서 skeptic skip → coverage 누락 | open question Q2에서 결정. 현재 권장: skip 허용, 다음 round-trip에서 호출 |
| OAuth 토큰/Codex 토큰 만료 시 skeptic 실패 → user-visible 에러 폭주 | best-effort: 실패는 diagnostic만, 사용자 메시지로 yield 안 함 |
| Skeptic이 매 turn 호출되어 비용 늘어남 | 사용자 "토큰 무한 가정" 명시 — 비용은 무시. latency는 R1으로 별도 트래킹 |
