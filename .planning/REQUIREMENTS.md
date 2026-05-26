# Requirements — OpenClaude Orchestra v0.2

## v1 Requirements (Always-On Orchestra — Milestone 1)

### Orchestra Activation

- [ ] **M1-01**: 모든 사용자 턴(turnCount ≥ 1)에서 GPT 5.5 + Opus 4.7 동시 호출
  - **Acceptance**: 3턴 이상 멀티턴 라이브 프로브에서 매 턴 `orchestra-usage.jsonl`에 `claude-opus-4-7 succeeded` 기록 + `modelUsage.gpt-5.5` 존재
  - **Existing gate**: `src/services/orchestra/orchestrator.ts:151` — `if (turnCount !== 1) return false`
  - **Approach**: 게이트를 config-controlled로 전환 (예: `orchestraEveryTurn: true` 기본)
- [ ] **M1-02**: 비-orchestra 폴백 모델도 GPT 5.5 (gpt-4o로 떨어지지 않음)
  - **Acceptance**: orchestra가 어떤 이유로 skip되어도 visible 모델이 gpt-5.5
  - **Approach**: `.openclaude-profile.json`을 codex 프로필로 교체, 또는 `OPENAI_MODEL`을 적절한 값으로 (Codex가 codexplan→gpt-5.5 매핑하므로)
- [ ] **M1-03**: Orchestra 강제 활성화 잠금 — 우발적 비활성화 방지
  - **Acceptance**: `~/.claude/settings.json`의 `orchestra.enabled: false`나 `plannerPolicy: 'off'`가 v0.2 모드에서는 무시되거나 경고
  - **Approach**: v0.2 mode flag (예: `orchestra.mode: 'v0.2-locked'`) 도입, 잠긴 상태에선 enabled/plannerPolicy 강제

### Validation

- [ ] **M1-04**: Multi-turn live probe 자동 검증
  - **Acceptance**: `bun run scripts/probe-orchestra-multiturn.ts` (신규)가 3턴 대화 시뮬레이션 후 매 턴 둘 다 호출됐는지 확인
  - **Approach**: 신규 검증 스크립트, CI에 포함

## v2 Requirements (Opus Skeptic — Milestone 2)

- [ ] **M2-01**: GPT Implementer 출력 직후 Opus Skeptic 호출
- [ ] **M2-02**: Skeptic dissent report 형식 (위험 지적, 가정 비판, scope drift 경보)
- [ ] **M2-03**: Skeptic은 read-only — 코드/파일 수정 권한 없음
- [ ] **M2-04**: Skeptic 결과를 사용자에게 별도 system 메시지로 표시 (orchestra-meta 형식)

## v3 Requirements (Shadow Executor + Cross Review — Milestone 3)

- [ ] **M3-01**: GPT Executor B — 별도 worktree에서 다른 접근의 GPT 구현
- [ ] **M3-02**: Opus Shadow Executor — 별도 worktree에서 Opus 그림자 구현
- [ ] **M3-03**: Cross-review 매트릭스 (3 후보 × 2 reviewer) 자동 생성
- [ ] **M3-04**: shadow branch가 main을 수정하지 못하게 권한 차단

## v4 Requirements (Evidence Arbiter — Milestone 4)

- [ ] **M4-01**: Evidence Arbiter 역할 — 5축 판정 (테스트/diff 최소성/scope/rollback/이해)
- [ ] **M4-02**: green/yellow/red 추천 출력
- [ ] **M4-03**: Human Gate UX — 사용자에게 명시적 merge 승인 요청
- [ ] **M4-04**: 권한 분리 강제 (Opus → read-only / shadow only / main 차단)

## v5 Requirements (Validation Experiment — Milestone 5)

- [ ] **M5-01**: 20-task experiment 프레임 (Opus unique valid defect 측정)
- [ ] **M5-02**: 메트릭 정의 (unique valid defect율, false positive율, scope drift catch율)
- [ ] **M5-03**: 결과 기반 v0.3 결정 (Opus 유지/강등/제거)

## Out of Scope

- Mythos Preview 통합 — 별도 마일스톤
- 3+ 모델 혼합 — v0.2는 양당 구조 유지
- Token cost optimization — 무한 가정으로 제외
- Cross-session orchestra state — 세션 내만

## Quality Criteria

각 요구는:
- **Specific and testable**: 라이브 프로브로 검증 가능
- **User-centric**: "사용자가 X를 본다" 또는 "시스템이 Y를 자동으로 한다"
- **Atomic**: 한 능력 = 한 REQ-ID
- **Independent**: 다른 REQ에 강한 의존성 최소

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| Phase0-01 | Phase 0 (이 세션) | ✓ Validated 2026-05-07 |
| Phase0-02 | Phase 0 (이 세션) | ✓ Validated 2026-05-07 |
| Phase0-03 | Phase 0 (이 세션) | ✓ Validated 2026-05-07 |
| M1-01..04 | Phase 1 | Pending |
| M2-01..04 | Phase 2 | Pending |
| M3-01..04 | Phase 3 | Pending |
| M4-01..04 | Phase 4 | Pending |
| M5-01..03 | Phase 5 | Pending |
