# Phase 4 Spec — Evidence Arbiter + Human Gate

**Status**: Draft — pending user review.
**Goal**: Phase 3의 cross-review 매트릭스를 입력으로 받아 5축 판정 → 한 줄 green/yellow/red 추천 → 사용자에게 명시적 merge 승인 UX. Opus의 main 직접 수정 차단을 권한 layer에서 강제.

## Why Phase 4 Is Lighter Than Phase 3

Phase 3는 실제 파일 변경(worktree 라이프사이클) — 위험. Phase 4는 다시 read-only + 사용자 인터랙션 layer. Phase 3가 mock-driven이어서 매트릭스 type 자체는 안정적이고 거기 위에 분석 logic을 쌓는 게 깔끔.

## Big-Shape Decisions (사용자 답변 필요)

### D1 — 5축 점수화 방식

PROJECT.md / REQUIREMENTS.md 명시된 5축: **테스트 통과 / diff 최소성 / scope 준수 / rollback 가능성 / 이해 가능성**.

| Option | 내용 | Pro | Con |
|--------|------|-----|-----|
| **a. 0-5 정수** | Phase 3의 reviewer scoresOutOf5 패턴 그대로 확장 | 일관성, 산술 가능 | "이해 가능성 = 3"이 무슨 뜻인지 모호 |
| b. 3단계 enum (`pass`/`partial`/`fail`) | 단순, 사용자 직관 | 미묘한 차이 못 잡음 |
| c. 명시적 evidence + boolean | "테스트가 실제 돌았는가? 실제 통과? evidence path는?" 같은 객관 사실 | 가장 robust | UI/구현 복잡 |

**권장 default**: **c**. 5축 각각 evidence (예: 테스트 실행 결과 path, diff line count, scope keywords match)와 pass/fail boolean. 산술 점수가 아니라 fact-based.

**결정 질문 D1**: c 채택? 또는 a/b?

### D2 — green/yellow/red 임계값

5축 결과를 종합해서 한 줄 추천을 어떻게 도출.

| Option | 내용 |
|--------|------|
| α. 모든 축 pass = green / 일부 fail = yellow / 다수 fail = red | 단순 |
| **β. 핵심 축(테스트, scope) fail = red 즉시 / 나머지 부분 fail = yellow / 모두 pass = green** | 위험 가중 |
| γ. ML/heuristic learned threshold | over-engineering |

**권장 default**: **β**.

**결정 질문 D2**: β 채택?

### D3 — Human Gate UX

| Option | 내용 |
|--------|------|
| **a. Phase 4 자체에선 system 메시지로 추천 + "다음 prompt에 'apply' 또는 'reject' 입력" 안내, OpenClaude 메인 루프가 사용자 다음 turn에서 처리** | 비-인터랙티브, `-p` 모드와도 호환 |
| b. 인터랙티브 prompt (stdin block) | UX 좋음 but `-p` 모드와 충돌 |
| c. 슬래시 커맨드 `/orchestra-apply`, `/orchestra-reject` | 명시적, 사용자 의지 분명 |

**권장 default**: **a + c 결합**. 추천 메시지에 슬래시 커맨드 안내 표기. 사용자가 다음 turn에 명령 입력.

**결정 질문 D3**: a+c 결합? 또는 다른?

### D4 — Opus 권한 분리 enforcement 위치

PROJECT.md M4-04 "Opus → read-only / shadow only / main 차단".

| Option | 내용 |
|--------|------|
| **i. 코드 layer (sideQuery 호출 부) — Opus가 sideQuery로 호출될 때 toolset 자체에 mutation tool 미포함** | 이미 Phase 2 skeptic이 이 패턴. shadow worker도 마찬가지. 추가 enforcement 불필요? |
| ii. git layer — `pre-receive` hook으로 `openclaude-shadow/*` branch가 main에 push되는 거 차단 | 인프라 무거움 |
| iii. orchestra promote 함수 layer — Phase 4 promote 함수 안에서 source branch 검사 | 실용적 |

**권장 default**: **i + iii 결합**. Phase 2/3에서 이미 코드 layer 차단 (tool 미전달). Phase 4 promote 함수가 candidate 받을 때 "candidate label/branch가 opus-shadow면 추가 confirm 한 단계 더" 로 추가 가드.

**결정 질문 D4**: i+iii? 또는 다른?

### D5 — 5축 판정자

| Option | 내용 |
|--------|------|
| α. GPT 단독 (Evidence Arbiter는 GPT 5.5의 역할이라고 PROJECT.md 명시) | 빠름, 단순 |
| **β. GPT 5.5 1차 + Opus 4.7 disagree-check** | 야당 정신 유지, 비용 +1 |
| γ. 코드 (LLM 없이 fact 추출만, 5축 boolean) | 가장 결정적 |

**권장 default**: PROJECT.md "GPT 5.5 = Evidence Arbiter" 명시이지만 야당 정신 위해 **γ + α 결합**: 코드가 가능한 한 fact 추출(테스트 실행 결과, diff line count 등) + GPT가 모호한 축(scope, 이해 가능성) 판정. Opus는 별도 disagree 메시지로.

**결정 질문 D5**: 어떻게? PROJECT.md 그대로 α / 야당 강화 β / fact-based γ?

## Out of Scope for Phase 4 (Phase 5로 미룸)

- 20-task validation experiment + 메트릭 수집 (M5)
- v0.3 결정 (Opus 유지/강등/제거)
- Mythos Preview 통합 (PROJECT 명시 OoS)
- 실제 main merge 자동화 — Phase 4는 "human gate가 승인하면 변경 적용" 구조만, 실제 적용 코드는 후속 phase에서.

## Acceptance — default 채택 시

D1=c / D2=β / D3=a+c / D4=i+iii / D5=γ+α 가정:

1. Phase 3 매트릭스 + candidate diff/test 결과를 input으로 받는 `evidenceArbiter.ts` 신설
2. 5축 evidence 추출 (코드로): 테스트 실행 path 존재? diff line count <= threshold? scope keyword match? 등
3. GPT가 "이해 가능성"/"scope 준수"의 모호한 축 판정 → 5축 모두 채워진 EvidenceReport
4. β 임계값 적용 → green/yellow/red verdict
5. Human Gate system 메시지: "권장: green/yellow/red. apply gpt-a로 patch 승격 / reject로 모두 폐기 / explain로 상세."
6. 사용자가 다음 turn에 `/orchestra-apply gpt-a` 같은 슬래시 커맨드 입력 → 그 candidate 파일을 main에 적용 (Opus shadow면 "확인하시겠습니까" 한 번 더)
7. main 적용 자체는 git apply / cherry-pick 또는 file copy

## Files (default 채택 시)

- `src/services/orchestra/evidenceArbiter.ts` — 5축 추출 + verdict
- `src/services/orchestra/evidenceArbiter.test.ts`
- `src/services/orchestra/humanGate.ts` — 시스템 메시지 + apply/reject 처리
- `src/services/orchestra/humanGate.test.ts`
- `src/commands/orchestra-apply.ts` (또는 동등) — 슬래시 커맨드
- `src/commands/orchestra-reject.ts`
- `src/services/orchestra/promote.ts` — candidate를 main에 적용하는 권한-검사 함수
- `src/services/orchestra/promote.test.ts`
- `src/query.ts` — Phase 3 hook 다음에 evidenceArbiter + humanGate 호출

## Risks

| R | Mitigation |
|---|------------|
| 슬래시 커맨드 시스템이 OpenClaude에 어떻게 등록되는지 모름 | 코드베이스 grep으로 기존 슬래시 커맨드 패턴 학습 |
| `main 적용` 자체가 git operation — 또 worktree 의존 | Phase 3 worktreeManager 재사용 + cherry-pick |
| 사용자 confirm 없이 자동 apply 위험 | 모든 promote는 명시적 슬래시 커맨드만, 자동화 절대 X |
| Opus shadow가 main에 들어가는 건 v0.2 정신 위반 | promote.ts에 "label === 'opus-shadow' 일 때 추가 confirm" 게이트. 단위 테스트로 단언 |
| 5축 GPT 판정 latency 추가 | best-effort. fail이면 "yellow + GPT 의견 누락" 처리 |
| Phase 3 production wiring 없으니 라이브 검증 안 됨 | mock 매트릭스 단위 테스트로 충분. 라이브 검증은 Task 3.7+4.x 통합 후. |

## Open Decision Summary

5개 답해야 할 것:
- **D1** (점수화): a / b / **c** — 권장 c (evidence + boolean)
- **D2** (임계값): α / **β** / γ — 권장 β (위험 가중)
- **D3** (Human Gate): **a+c** / b — 권장 a+c
- **D4** (권한): **i+iii** / ii — 권장 i+iii
- **D5** (판정자): α(GPT) / β(GPT+Opus) / γ(fact-based) / 권장 **γ+α**

**기본안**: D1=c, D2=β, D3=a+c, D4=i+iii, D5=γ+α.

답변이 default면 "ok" 한마디. 다른 게 있으면 알려줘.
