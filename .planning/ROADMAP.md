# Roadmap — OpenClaude Orchestra v0.2

5 milestones | 18 active requirements | All v0.2 vision covered ✓

## Phase Overview

| # | Phase | Goal | Requirements | Success Criteria | Depends |
|---|-------|------|--------------|------------------|---------|
| 1 | Always-On Orchestra | 매 턴 GPT 5.5 + Opus 4.7 동시 호출 | M1-01..04 | 3턴 라이브 프로브 매 턴 둘 다 호출 | — |
| 2 | Opus Skeptic ✓ | GPT 출력 후 Opus가 야당 dissent report | M2-01..04 | 사용자가 Skeptic 메시지를 별도 출력으로 본다 | Phase 1 |
| 3 | Shadow Executor + Cross Review ⚠ | 3 후보 + 2 reviewer 매트릭스 | M3-01..04 | shadow worktree 격리 + 매트릭스 표 출력 | Phase 2 |
| 4 | Evidence Arbiter ⚠ | 5축 판정 + green/yellow/red + Human Gate | M4-01..04 | 자동 추천 + 명시적 사용자 승인 | Phase 3 |
| 5 | Validation Experiment ⚠ | 20-task로 Opus value 정량 측정 | M5-01..03 | 메트릭 출력 + v0.3 결정 문서화 | Phase 4 |

## Phase Details

### Phase 1: Always-On Orchestra

**Goal**: turnCount === 1 게이트를 제거하거나 config-controlled로 전환하여 모든 사용자 턴에서 orchestra가 작동하게 만든다. 비-orchestra 폴백도 GPT 5.5로 정렬.

**Requirements covered**:
- M1-01: 모든 턴에서 동시 호출
- M1-02: 폴백 모델 GPT 5.5
- M1-03: orchestra 강제 활성화 잠금
- M1-04: Multi-turn 자동 검증 스크립트

**Success Criteria**:
1. `bun run scripts/probe-orchestra-multiturn.ts` (신규)가 3턴 대화에서 매 턴 `claude-opus-4-7 succeeded` 기록 확인
2. orchestra가 비활성화된 경우에도 visible 모델이 gpt-5.5로 폴백
3. `~/.claude/settings.json`에서 orchestra를 끄려고 시도해도 v0.2 lock으로 무시됨
4. 단위 테스트: `shouldRunOrchestra({turnCount: 2})` → true (config 활성 시)

**Files to modify**:
- `src/services/orchestra/orchestrator.ts` — `shouldRunOrchestra` turnCount 게이트 변경
- `src/services/orchestra/config.ts` — `orchestraEveryTurn` 또는 `mode: 'v0.2-locked'` 추가
- `.openclaude-profile.json` — codex 프로필로 교체 또는 OPENAI_MODEL 정렬
- `scripts/probe-orchestra-multiturn.ts` (신규) — 3턴 시뮬레이션 라이브 프로브

**Files to add tests for**:
- `src/services/orchestra/orchestrator.test.ts` — turnCount 2, 3에서 활성화 단언
- `src/services/orchestra/config.test.ts` (신규/추가) — v0.2-locked 모드 단언

### Phase 2: Opus Skeptic

**Goal**: GPT Implementer가 응답을 생성한 직후 Opus 4.7을 read-only Skeptic 모드로 호출해서 dissent report를 만든다. 사용자에게 별도 메시지로 표시.

**Requirements covered**:
- M2-01: post-implementation Opus 호출
- M2-02: dissent report 형식 (위험/가정/scope drift)
- M2-03: read-only — 파일 수정 권한 없음
- M2-04: 사용자 표시

**Success Criteria**:
1. orchestra-usage.jsonl에 `role: skeptic` 항목이 매 턴 기록
2. Skeptic이 코드 도구(Edit/Write) 호출 시도 시 명시적 차단
3. 사용자가 GPT 응답 후 별도 색상/형식의 "Opus 야당 의견" 메시지 확인 가능
4. 단위 테스트: `callOpusSkeptic` 함수 존재, read-only 권한 enforcement, dissent 파싱

**Files to add**:
- `src/services/orchestra/skeptic.ts` — Skeptic 호출 로직
- `src/services/orchestra/skeptic.test.ts` — 권한 차단 + dissent 형식 테스트
- `src/services/orchestra/orchestrator.ts` — Skeptic 통합 hook
- `src/query.ts` — 응답 후 Skeptic 호출 + 메시지 yield

### Phase 3: Shadow Executor + Cross Review

**Goal**: 별도 worktree에서 GPT Executor B와 Opus Shadow Executor를 돌려 3 후보 패치를 만들고 cross-review 매트릭스를 생성.

**Requirements covered**:
- M3-01: GPT Executor B (별도 worktree)
- M3-02: Opus Shadow Executor (별도 worktree)
- M3-03: Cross-review 매트릭스 (3 후보 × 2 reviewer)
- M3-04: shadow branch는 main 차단

**Success Criteria**:
1. 한 task가 들어오면 worktree A/B/C에 GPT-A/GPT-B/Opus-Shadow 패치가 각각 생성
2. main branch는 어떤 shadow patch도 자동으로 받지 않음 (block test)
3. cross-review 표가 stdout 또는 별도 파일에 출력 (각 후보 × 각 reviewer 평가)

**Files to add**:
- `src/services/orchestra/shadowExecutor.ts`
- `src/services/orchestra/crossReview.ts`
- `scripts/orchestra-worktree-manager.ts` — git worktree 라이프사이클
- 통합 테스트

### Phase 4: Evidence Arbiter + Human Gate

**Goal**: cross-review 결과를 5축 (test/diff/scope/rollback/이해)으로 판정하고 green/yellow/red 추천 + Human 명시 승인 플로우.

**Requirements covered**:
- M4-01: 5축 판정
- M4-02: green/yellow/red 추천
- M4-03: Human Gate
- M4-04: 권한 분리 enforcement

**Success Criteria**:
1. arbiter 출력에 5축 점수 + 종합 추천이 명시
2. 사용자가 명시적 confirm 없이는 Opus shadow patch가 main에 들어가지 않음
3. 권한 위반 시도 (Opus가 main 수정) 모두 차단

**Files to add**:
- `src/services/orchestra/arbiter.ts`
- `src/services/orchestra/permissions.ts` — Opus = read-only/shadow 강제
- 통합 테스트

### Phase 5: Validation Experiment

**Goal**: 20개 실제 Meta+MFH task로 Opus의 unique value를 측정해서 v0.3 결정.

**Requirements covered**:
- M5-01: 20-task experiment
- M5-02: 메트릭 (unique valid defect, false positive, scope drift catch)
- M5-03: 결정 문서화

**Success Criteria**:
1. 20-task 실행 결과 데이터 수집 완료
2. Opus 유지/강등/제거 결정이 메트릭 기반으로 정당화됨
3. v0.3 ROADMAP.md 작성

**Files to add**:
- `scripts/orchestra-experiment-runner.ts`
- `.planning/experiments/20-task-results.md`
- `.planning/decisions/v0.3-direction.md`

## Coverage Validation

| REQ-ID | Phase | Verified |
|--------|-------|----------|
| M1-01 | Phase 1 | Pending |
| M1-02 | Phase 1 | Pending |
| M1-03 | Phase 1 | Pending |
| M1-04 | Phase 1 | Pending |
| M2-01 | Phase 2 | ✓ 2026-05-07 (live: probe2 turn 2 skeptic succeeded) |
| M2-02 | Phase 2 | ✓ 2026-05-07 (unit: 15 skeptic tests) |
| M2-03 | Phase 2 | ✓ 2026-05-07 (unit: forceFirstParty + no tools + self-block) |
| M2-04 | Phase 2 | ✓ 2026-05-07 (unit yield + jsonl); ⚠ live stdout 부분 — GPT 비결정성 |
| M3-01 | Phase 3 | ⚠ 2026-05-07 인프라 (mock worker pass); production wiring 후속 |
| M3-02 | Phase 3 | ⚠ 2026-05-07 인프라 (mock worker pass); production wiring 후속 |
| M3-03 | Phase 3 | ⚠ 2026-05-07 인프라 (mock reviewer pass); production wiring 후속 |
| M3-04 | Phase 3 | ✓ 2026-05-07 (worktreeManager + 게이트 + non-git skip) |
| M4-01 | Phase 4 | ✓ 2026-05-07 (evidenceArbiter 6 tests) |
| M4-02 | Phase 4 | ✓ 2026-05-07 (humanGate 6 tests) |
| M4-03 | Phase 4 | ⚠ 2026-05-07 (text contract — slash cmd 등록 후속) |
| M4-04 | Phase 4 | ✓ 2026-05-07 (promote 7 tests, opus-shadow 두 단계 confirm) |
| M5-01 | Phase 5 | ✓ 2026-05-07 (experimentMetrics 8 tests + runner scaffold) |
| M5-02 | Phase 5 | ✓ 2026-05-07 (UVD/FPR/SDC + 임계값 단언) |
| M5-03 | Phase 5 | ⚠ 2026-05-07 (template — 20-task 실행은 사용자 후속) |

**Coverage**: 18/18 active requirements mapped to phases. ✓

## Risk / Decision Log

- **Risk R1**: 매 턴 Opus 호출 → 5-10초 추가 지연 per turn. 사용자가 토큰 무한 가정했으나 latency는 별개. → Phase 1 verification에서 latency 보고 포함.
- **Risk R2**: Codex 인증이 사용자 환경에서 작동하는지 미확인. `.openclaude-profile.json`에 codex 설정 시 실 라이브 프로브로 검증 필요.
- **Risk R3**: Phase 3-4의 worktree 격리는 OpenClaude 빌드 디렉토리가 git 저장소가 아니면 실패. 테스트 fixture로 임시 git 저장소 생성 필요.
- **Risk R4**: Opus가 v0.2의 야당 역할에서도 가치를 못 만들면 v0.3에서 GPT-only multi-agent로 전환. M5에서 결정.
