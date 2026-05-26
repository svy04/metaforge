# Phase 1 Plan — Always-On Orchestra

**Goal**: 모든 사용자 턴에서 GPT 5.5 + Opus 4.7 동시 호출. 비-orchestra 폴백도 GPT 5.5.

**Approach**: TDD — 각 task는 (1) failing test → (2) minimal fix → (3) test passes 순.

## Task Breakdown

### Task 1.1 — turnCount 게이트 config-controlled 전환

**REQ**: M1-01

**Current**: [orchestrator.ts:151](../../src/services/orchestra/orchestrator.ts:151) — `if (turnCount !== 1) return false`. 무조건 1턴만 허용.

**Target**: config의 `orchestra.everyTurn: true` (기본값 true in v0.2)이면 모든 턴에서 허용.

**TDD Steps**:
1. **RED**: `src/services/orchestra/orchestrator.test.ts`에 새 테스트 추가:
   - `shouldRunOrchestra({ querySource: 'sdk', turnCount: 2, settings: null })` → 기본 설정에서 `true` 단언 (현재는 false)
   - `shouldRunOrchestra({ querySource: 'sdk', turnCount: 5, settings: null })` → `true` 단언
   - `shouldRunOrchestra({ querySource: 'sdk', turnCount: 2, settings: { orchestra: { everyTurn: false } } })` → `false` 단언 (opt-out 가능)
2. **GREEN**:
   - `config.ts`에 `everyTurn?: boolean` 옵션 추가 (default `true`)
   - `resolveOrchestraSettings`에 `everyTurn` 매핑 추가
   - `orchestrator.ts:151` 게이트 변경: `if (turnCount !== 1 && !orchestra.everyTurn) return false`
3. **REFACTOR**: 새 옵션 문서화 (config.ts 주석)

**Acceptance**: `bun test src/services/orchestra/orchestrator.test.ts` 통과

**Files**:
- `src/services/orchestra/config.ts` — 옵션 추가
- `src/services/orchestra/orchestrator.ts` — 게이트 변경
- `src/services/orchestra/orchestrator.test.ts` — 새 테스트
- `src/utils/settings/types.ts` — orchestra.everyTurn 타입 (필요 시)

### Task 1.2 — `.openclaude-profile.json` codex 프로필로 정렬

**REQ**: M1-02

**Current**: 프로필이 `{"profile": "openai", "OPENAI_MODEL": "gpt-4o", "OPENAI_API_KEY": "sk-openai-key"}` placeholder. 비-orchestra context에서 gpt-4o로 떨어짐.

**Target**: codex 프로필로 교체. 사용자가 codex 인증 갖고 있다고 가정.

**TDD Steps**:
1. **RED**: `src/services/api/providerConfig.local.test.ts` 또는 신규에 테스트 추가:
   - codex 프로필 활성 시 implementer route가 codexplan → gpt-5.5로 매핑
   - 비-orchestra path에서도 modelUsage가 gpt-5.5
2. **GREEN**:
   - `.openclaude-profile.json` 내용 교체:
     ```json
     {
       "profile": "codex",
       "env": { "CODEX_API_KEY": "...", "CODEX_ACCOUNT_ID": "..." },
       "createdAt": "2026-05-07T00:00:00.000Z"
     }
     ```
   - 또는 사용자에게 `bun run profile:codex` 실행 가이드
3. **REFACTOR**: 프로필 자동 부트스트랩 검증 (이미 사용자 codex 인증 있는지 확인)

**Acceptance**: 라이브 프로브 후 `modelUsage` 키가 항상 `gpt-5.5`

**Files**:
- `.openclaude-profile.json` — 교체
- 검증 스크립트 (Task 1.4와 통합)

**Note**: 사용자의 실 Codex 인증 상태를 모름 → Task 1.4의 프로브가 "Codex auth 없음" 에러를 내면 사용자에게 `/provider`나 `bun run profile:codex` 실행 요청

### Task 1.3 — Orchestra 강제 활성화 잠금 (v0.2 mode)

**REQ**: M1-03

**Current**: `~/.claude/settings.json`의 `orchestra.enabled: false`나 `plannerPolicy: 'off'`로 사용자가 우발적으로 끌 수 있음.

**Target**: v0.2 lock mode 도입. lock 활성 시 `enabled`/`plannerPolicy`를 강제로 v0.2 값으로 덮어쓰기.

**TDD Steps**:
1. **RED**: `src/services/orchestra/config.test.ts` 신규 (또는 기존 확장):
   - `resolveOrchestraSettings({ orchestra: { mode: 'v0.2-locked', enabled: false } })` → `enabled: true` 강제 단언
   - `mode: 'v0.2-locked'`이면 `plannerPolicy: 'always'` 강제 단언
   - `mode: 'codex-dominant'` (기본)이면 사용자 설정 그대로
2. **GREEN**:
   - `config.ts`의 `OrchestraMode` 타입에 `'v0.2-locked'` 추가
   - `resolveOrchestraSettings`에서 mode === 'v0.2-locked'이면 enabled/plannerPolicy 강제
3. **REFACTOR**: 잠긴 모드일 때 사용자에게 경고 메시지 (override 시도 시)

**Acceptance**: 단위 테스트 통과 + 의도한 lock 동작 확인

**Files**:
- `src/services/orchestra/config.ts` — mode 타입 + 강제 로직
- `src/services/orchestra/config.test.ts` — 새 테스트 (혹은 기존 파일 확장)

### Task 1.4 — Multi-turn live probe 스크립트

**REQ**: M1-04

**Current**: 1턴 라이브 프로브만 있음 (이번 세션에 수동 실행). 자동 멀티턴 검증 없음.

**Target**: `scripts/probe-orchestra-multiturn.ts` 신규. 3턴 대화 시뮬레이션 후 `~/.claude/orchestra-usage.jsonl`에 매 턴 `claude-opus-4-7 succeeded` 기록 검증.

**TDD Steps**:
1. **RED**: 스크립트 작성 전, 어떤 출력 형식을 기대하는지 정의 (스크립트 자체가 테스트이므로 RED는 "스크립트 부재" 상태)
2. **GREEN**:
   - `scripts/probe-orchestra-multiturn.ts` 작성:
     - `--no-session-persistence` 끄고 단일 세션 유지
     - 3개 사용자 메시지 순차 전송 (`echo`된 출력에 sentinel 포함)
     - 각 턴 종료 후 `orchestra-usage.jsonl` 새 라인 수와 success 상태 확인
     - 결과 표 형식으로 stdout 출력
3. **REFACTOR**: package.json에 `"probe:orchestra-multiturn": "bun run scripts/probe-orchestra-multiturn.ts"` 추가

**Acceptance**: 스크립트 실행 시 3턴 모두 `succeeded` + `gpt-5.5` modelUsage 확인

**Files**:
- `scripts/probe-orchestra-multiturn.ts` (신규)
- `package.json` — script 추가

**Note**: 단일 OpenClaude 세션에서 3턴 시뮬레이션은 stdin 파이프나 expect-style 인터랙션 필요. 또는 3개 별도 `-p` 호출로 시뮬레이션 (단점: 세션 분리). MVP는 분리 호출로 시작.

## Execution Order

```
Task 1.1 (게이트)     → 단독 가능, 가장 영향 큰 변경
Task 1.3 (lock mode)  → Task 1.1 완료 후 (config 구조 의존)
Task 1.2 (profile)    → Task 1.4와 같이 (profile 변경 후 검증)
Task 1.4 (probe)      → 다른 모든 task 완료 후 end-to-end 검증
```

## Phase Done Definition

- [ ] Task 1.1 단위 테스트 통과 + dist 재빌드
- [ ] Task 1.3 단위 테스트 통과
- [ ] Task 1.2 프로필 교체 (사용자 인증 확인 후)
- [ ] Task 1.4 멀티턴 프로브가 매 턴 둘 다 호출 확인
- [ ] PROJECT.md 업데이트 — M1 → Validated 이동
- [ ] ROADMAP.md Phase 1 row → ✓ Verified

## Threats & Mitigations

| Threat | Mitigation |
|--------|------------|
| 매 턴 Opus 호출로 첫 응답 5-10초 추가 지연 | Task 1.4 프로브에 latency 보고 추가; 사용자에게 토큰 무한 가정 재확인 |
| Codex 인증 미설정 상태 | Task 1.2 프로파일 변경 전 사용자에게 codex 인증 상태 확인 요청 |
| Lock mode가 기존 사용자 설정 덮어써서 혼란 | mode === 'v0.2-locked'일 때 stderr 또는 메시지로 명시 표시 |
| OPENAI_MODEL fallback이 다른 코드 경로에 박혀 있을 가능성 | Task 1.4 프로브로 실제 라우팅 확인하여 발견 |
