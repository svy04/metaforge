# OpenClaude Orchestra v0.2 — Infinite Token Capital

## What This Is

OpenClaude의 다중 에이전트 오케스트라. **GPT 5.5 (xhigh)와 Opus 4.7 (max)을 항상 같이** 호출해서, 한 모델의 약점을 다른 모델이 다른 방식으로 보강하는 구조를 구축한다. 토큰 비용 무제한을 가정하고, 비용이 아닌 **실패 패턴 다양화**를 최적화 목표로 잡는다.

## Core Value

> **GPT 5.5가 확신 있게 틀리는 순간을 Opus 4.7이 다른 각도에서 잡는다.**

이 한 줄이 살아있지 않으면 v0.2는 의미 없다. Opus가 GPT를 평균 성능에서 못 이겨도, "다르게 틀린다면" 가치 있다. GPT보다 못하고 틀리는 방식도 GPT와 같다면 Opus는 버린다.

## Roles (v0.2 Design)

```
GPT 5.5 = 왕   — 메인 구현 / 오케스트레이션 / 통합 / Evidence Arbiter
Opus 4.7 = 야당 — 독립 반대 의견 / 그림자 구현 / 스켑틱 / dissent reporter
Test    = 법
Human   = 최종 재판관
```

### 10-Role Decomposition

| # | Role | Model | Permission | Output |
|---|------|-------|------------|--------|
| 1 | GPT Orchestrator | GPT 5.5 | read/write 조율, 직접 merge 금지 | 작업 분해, agent 호출, 통합 |
| 2 | GPT Architect A | GPT 5.5 | read-only | 실행 가능한 설계안 |
| 3 | Opus Architect B | Opus 4.7 | read-only | 다른 관점의 설계, 숨은 위험 |
| 4 | GPT Executor A | GPT 5.5 | edit (main) | primary patch |
| 5 | GPT Executor B | GPT 5.5 | edit (separate worktree) | alternative patch |
| 6 | Opus Shadow Executor | Opus 4.7 | edit (separate branch only) | shadow patch (다른 접근법 샘플) |
| 7 | GPT Verifier | GPT 5.5 | read/test | 테스트, diff review |
| 8 | Opus Skeptic | Opus 4.7 | read-only | dissent report (공격 모드) |
| 9 | Evidence Arbiter | GPT 5.5 | read-only | green/yellow/red recommendation |
| 10 | Human Gate | 인간 | main merge 권한 | 최종 승인 |

### Key Permission Rule

Opus는 GPT보다 약할 수 있다는 가설 하에 **main branch 직접 수정 금지**. shadow branch에서만 edit 허용. 틀려도 안전하고 맞으면 흡수 가능한 구조.

## Context

### Why Now

- 2026-05-06 세션에서 1턴짜리 orchestra(planner=Opus, implementer=GPT)는 작동 검증됨
- 그러나 turnCount === 1 게이트로 2턴 이후 orchestra 차단
- `.openclaude-profile.json`이 placeholder openai/gpt-4o로 비-orchestra 폴백이 깨짐
- Opus는 현재 pre-implementation planner 역할 하나뿐. 야당/skeptic/shadow 코드 미존재
- 사용자가 토큰 무한 가정으로 v0.2 다중 에이전트 비전을 명시적으로 요청

### Phase 0 Already Done (이번 세션)

3중 root cause 발견 및 픽스 (라이브 검증 완료):

1. **Bug**: `CLAUDE_OPUS_4_7_CONFIG.openai = 'gpt-4o'` 매핑이 OAuth 전용 planner에도 적용 → planner가 'gpt-4o'로 번역 → callClaudeLoginPlanner의 `startsWith('claude-')` 체크가 throw → adaptive policy block
   - **Fix**: `fallbackModel(planner)`은 항상 `claude-opus-4-7` (firstParty) 반환
2. **Bug**: `CLAUDE_CODE_USE_OPENAI=1` 게이트가 sideQuery → getAnthropicClient를 OpenAI shim으로 강제 라우팅
   - **Fix**: `forceFirstParty` 옵션을 sideQuery까지 propagate, 6개 프로바이더 게이트 우회
3. **Bug**: `isClaudeAISubscriber()`가 `CLAUDE_CODE_USE_OPENAI=1` 환경에서 false 반환 → default 브랜치가 OAuth 토큰 무시
   - **Fix**: forceFirstParty면 isClaudeAISubscriber 우회하여 OAuth 토큰 직접 사용 + OAuth baseURL 강제

라이브 증거: orchestra-usage.jsonl에 2026-05-07T03:10 `claude-opus-4-7 succeeded` (5.6초), $0.176 비용 발생.

### Architectural Constraints

- **OAuth 전용 planner**: Claude OAuth 토큰 필수. `CLAUDE_CODE_OAUTH_TOKEN` env 또는 `~/.claude/.credentials.json` 필요
- **Codex provider**: GPT 5.5는 Codex API 경유 (`codexplan` → `gpt-5.5` runtime). 사용자 codex 인증 필요
- **모든 Anthropic 호출은 sideQuery 경유**: OAuth attribution header, fingerprint, model beta headers 필수
- **권한 분리는 worktree 기반**: shadow executor는 별도 git worktree에서만 동작 (현재 OpenClaude 빌드 디렉토리는 git 저장소가 아닐 수 있음 — 별도 처리 필요)

## Requirements

### Validated (Phase 0 by 2026-05-07)

- ✓ **Phase0-01**: orchestra planner는 Claude OAuth로 claude-opus-4-7 호출 (1턴 한정)
- ✓ **Phase0-02**: orchestra implementer는 Codex GPT-5.5로 라우팅 (1턴 한정)
- ✓ **Phase0-03**: 사용자의 primary provider가 OpenAI여도 planner는 Anthropic API 도달

### Active

#### v1 — Always-On Orchestra (Milestone 1)

- [ ] **M1-01**: 모든 사용자 턴에서 GPT 5.5 + Opus 4.7 동시 호출 (turnCount 게이트 제거 또는 config-controlled)
- [ ] **M1-02**: `.openclaude-profile.json` codex 프로필로 정렬 — 비-orchestra 폴백도 GPT 5.5
- [ ] **M1-03**: orchestra 강제 활성화 잠금 (`enabled: true`, `plannerPolicy: 'always'`을 사용자가 우발적으로 끄지 못하게)

#### v2 — Opus Skeptic (Milestone 2) — ✓ Phase 2 (2026-05-07)

- [x] **M2-01**: GPT Implementer 출력 후 Opus Skeptic 자동 호출
  - Live: orchestra-usage.jsonl `role:"skeptic" status:"succeeded"` (probe2 turn 2)
- [x] **M2-02**: dissent report 형식 — 위험 지적, 가정 비판, scope drift 경보
  - Unit: `DissentReport` 구조체, `parseDissentReport`, severity 폴백 등 15 tests pass
- [x] **M2-03**: Skeptic 출력은 read-only — 코드 수정 권한 없음
  - Unit: `tools` 인자 미전달, `querySource:"orchestra_skeptic"` self-block, OAuth `forceFirstParty:true`
- [x] **M2-04**: Skeptic 결과를 사용자에게 별도 메시지로 표시
  - Unit: `query/skeptic.test.ts` — turn-keyed dedup + tool_use 게이트 + systemMessage yield 단언
  - Live partial: stdout dissent 캡처는 GPT 비결정성으로 prob6에선 fire 안 됨 (모든 turn tool_use). probe2 turn 2 jsonl 기록은 fire 입증.

#### v3 — Shadow Executor + Cross Review (Milestone 3) — ⚠ Phase 3 인프라만 (2026-05-07)

- [x] **M3-01**: GPT Executor B 인프라 — `shadowExecutor.ts`에 worker dispatch 골격 + label별 차별화 system prompt. **production worker wiring 후속**.
- [x] **M3-02**: Opus Shadow Executor 인프라 — 동일 dispatch에 'opus-shadow' label. **production worker wiring 후속**.
- [x] **M3-03**: Cross-review 매트릭스 — `crossReview.ts` 3×2 grid + green/yellow/red verdict + markdown summary/detail. mock reviewer 단위 테스트 통과. **production reviewer wiring 후속**.
- [x] **M3-04**: 격리 — `worktreeManager.ts` git worktree 라이프사이클 (add/list/remove + non-git graceful skip). main은 절대 자동 수정 안 됨 (Phase 4가 승격 결정).
- 검증:
  - 단위 테스트: 22 신규 (worktreeManager 8 + shadowExecutor 4 + crossReview 5 + query/shadow 5). 전체 94 pass / 0 fail.
  - 빌드: `dist/cli.mjs` 성공.
  - 라이브: OpenClaude(non-git) cwd에서 graceful skip 입증 — jsonl `shadow-*`/`cross-reviewer-*` 0개, Phase 1+2 회귀 없음.
- 후속 (Phase 3 완성):
  - **production worker wiring**: gpt-a/gpt-b/opus-shadow worker가 실제 sub-agent + Codex/OAuth로 worktree에 commit하는 통합. Task 3.7.
  - **production reviewer wiring**: GPT/Opus reviewer가 candidate diff 읽고 verdict 반환. Task 3.8.
  - **실 git fixture 라이브 검증**: 외부 git repo cwd에서 `shadowEnabled: true` 켜고 3 worktree 생성 + worker fire 입증. Task 3.9.

#### v4 — Evidence Arbiter (Milestone 4) — ⚠ 인프라 (2026-05-07)

- [x] **M4-01**: 5축 fact-based 판정 — `evidenceArbiter.ts` (테스트/diff/scope/rollback/이해). 단위 테스트 6/6 pass. β 임계값 적용.
- [x] **M4-02**: green/yellow/red — `humanGate.ts` 추천 메시지 + level 매핑. 6/6 pass.
- [x] **M4-03**: Human Gate UX — system 메시지에 `/orchestra-apply <label>` / `/orchestra-reject` 안내. 슬래시 커맨드 OpenClaude 등록은 후속.
- [x] **M4-04**: 권한 게이트 — `promote.ts` 결정 함수: red verdict 차단, opus-shadow 두 단계 confirm 강제. 7/7 pass.
- 후속: Task 4.6 실제 git apply / cherry-pick 통합. Task 4.7 슬래시 커맨드 등록.

#### v5 — Validation Experiment (Milestone 5) — ⚠ 인프라 (2026-05-07)

- [x] **M5-01**: 측정 프레임 — `experimentMetrics.ts` (UVD/FPR/SDC/agreement). 8/8 단위 테스트 pass. `scripts/orchestra-experiment-runner.ts` scaffold가 mock task로 end-to-end 동작 입증.
- [x] **M5-02**: 메트릭 정의 — UVD ≥ 15% OR SDC ≥ 25% → keep / UVD < 5% AND SDC < 10% → remove / 그 외 → demote. 단위 테스트로 임계값 단언.
- [x] **M5-03**: 결정 템플릿 — `.planning/phase-5/v0.3-decision-template.md`. 메트릭 → keep/demote/remove → v0.3 ROADMAP 골격.
- 후속: 사용자가 20개 실제 task를 별도 시간에 직접 실행해 `.planning/phase-5/tasks/*.json`에 ground truth 채우고 runner 실행. 그 결과로 v0.3 결정 문서 작성.

### Out of Scope

- **Mythos Preview 모델 통합** — Anthropic 차세대 모델, 별도 마일스톤
- **3개 이상 모델 혼합** — v0.2는 GPT 5.5 + Opus 4.7 양당 구조 유지
- **Token cost optimization** — 무한 가정으로 명시적 제외
- **Real-time streaming arbiter** — 후처리만, 실시간 X
- **Cross-session orchestra state** — 세션 내 orchestra만, 영구화 X

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Opus를 야당 역할로 고정 | 평균 성능 경쟁이 아닌 실패 패턴 다양화 목적 | — Pending experiment (M5) |
| 모든 턴에서 orchestra 작동 | 사용자 명시 요구 ("항상 같이") | — Pending M1 |
| Opus = read-only 기본 | Opus가 약할 가능성 보호. shadow branch만 예외 | — Pending M3-M4 |
| Evidence-based 판정 | 모델 투표가 아닌 테스트 + diff + reproducibility | — Pending M4 |
| 20-task experiment | Opus 가치 정량 측정 후 v0.3 결정 | — Pending M5 |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone**:
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-07 after initialization*
