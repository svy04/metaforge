# Phase 3 Spec — Shadow Executor + Cross Review

**Status**: Draft — pending user review. Big-shape decisions needed before any code.
**Goal**: 한 user task에 대해 GPT 5.5의 두 가지 다른 접근(GPT-A primary + GPT-B alternative) + Opus 4.7의 그림자 구현(Shadow), 총 3 후보를 만들고 cross-review 매트릭스로 비교.

## Why This Phase Is Different

Phase 1-2는 read-only 또는 advisory 추가 — 위험 거의 없었다. Phase 3는 **실제 파일을 다른 worktree에서 변경**한다. 결정의 영향이 코드 안전, 라이프사이클 관리, 사용자 경험까지 미친다. 그래서 SPEC에 결정 질문이 많다.

## Big-Shape Decisions (사용자 답변 필요)

### D1 — 격리 모델

3 후보 패치를 어디에 만들지.

| Option | 내용 | Pros | Cons |
|--------|------|------|------|
| **A. git worktree** | `git worktree add ../shadow-A`, `../shadow-B`, `../shadow-opus` | 표준, branch 격리 자동, diff/merge 도구 풍부 | OpenClaude 빌드 디렉토리는 git repo 아님. 사용자 적용처 디렉토리도 git 아닐 수 있음. fixture 필요. |
| B. 형제 디렉토리 (cp -r) | 임시 디렉토리 3개에 코드 복제, 각 후보 거기서 작업 | git 의존성 없음 | 디스크 공간, cleanup, diff 직접 비교해야 |
| C. in-memory diff (no real worktree) | 패치를 메모리/JSON으로만 보관, 실제 파일 안 만짐 | 격리 100%, 디스크 zero | 실제 빌드/테스트 못 돌림 → "패치가 컴파일되는가" 같은 검증 불가 |

**권장 default**: **A**. 단 OpenClaude 자체는 git 아니므로 *Phase 3는 OpenClaude self-modify가 아니라 "사용자가 OpenClaude를 사용해 외부 프로젝트를 작업하는 turn"에 작동* 한다고 명확화. 즉 사용자 cwd가 git repo이면 Phase 3 활성, 아니면 skip(diagnostic만).

**결정 질문 D1**: A 채택? 아니면 B/C? 또는 D1-A를 default로 두되 non-git cwd면 graceful skip?

### D2 — 발사 시점

매 user prompt마다 GPT-A/B + Opus Shadow 3 후보 모두 만들지, 코드 변경 요청에서만 만들지.

| Option | 내용 |
|--------|------|
| α. 매 prompt | 단순. 비용 무한 가정이라 OK. but 90% prompts는 코드 변경 아닐 거라 cross-review 의미 없음 (3 후보 모두 "텍스트 답변" → 비교 불가) |
| **β. 코드 변경 turn만** | tool_use에 Edit/Write 포함된 turn만 후보 생성. risk-gated. |
| γ. 사용자가 명시적 `/orchestra-shadow` 같은 슬래시 커맨드로 발사 | 가장 안전, 사용자 의지 명확. but 자동화 정신 약화 |

**권장 default**: **β**. 코드 변경이 정말로 일어나는 turn에만 3-way 후보 의미.

**결정 질문 D2**: β 채택? 또는 자동화 우선해서 α? 또는 사용자 통제 우선해서 γ?

### D3 — Phase 3에서 main에 patch가 들어가나?

Phase 3 자체는 후보 생성 + cross-review만. **main 적용은 Phase 4 Evidence Arbiter + Human Gate**의 책임.

| Option | 내용 |
|--------|------|
| **i. Phase 3 = 비교 read-only** | 3 후보 + 매트릭스 표만 출력. main 변경 0. Phase 4가 승격 결정. |
| ii. Phase 3 = primary 자동 적용 + B/Shadow는 비교용 보관 | GPT-A 패치는 즉시 main에. B/Shadow는 리뷰 자료로 보관. Phase 4 없이도 작동 가능. |

**권장 default**: **i**. 야당 정신 + 안전. 단 사용자 입장에선 매 코드 turn마다 patch 안 들어가는 게 답답할 수 있음.

**결정 질문 D3**: i 채택? Phase 3 끝나도 GPT-A primary는 main에 들어갔으면 좋겠으면 ii.

### D4 — Cross-review 매트릭스 형식 + 어디 출력

3 후보 × 2 reviewer (GPT, Opus) = 6 평가 cell.

| Option | 어디 보임 |
|--------|-----------|
| **a. stdout system 메시지** | Phase 2와 동일 패턴. 사용자가 즉시 봄. |
| b. 별도 파일 (`.planning/phase-3/cross-review-{turn}.md`) | 영구 보관. stdout은 요약만. |
| c. 둘 다 | 요약 stdout + 상세 파일 |

**권장 default**: **c**. stdout에 한줄 요약 + 파일에 상세.

**결정 질문 D4**: c 또는 다른 형식?

### D5 — Opus Shadow가 Codex API 인증 필요한가?

GPT 5.5 두 번 부르려면 Codex 인증 사용 횟수 두 배. Opus Shadow는 OAuth Claude path. 즉 한 turn당:
- planner (Opus, OAuth) — 1회 (Phase 1)
- skeptic (Opus, OAuth) — 1회 (Phase 2)
- GPT-A primary (Codex) — 1회 (이미 있음)
- GPT-B alternative (Codex) — **신규 1회**
- Opus Shadow (OAuth) — **신규 1회**

코드 변경 turn 1번이 5번 model call. latency 수십 초. 사용자 토큰 무한 가정해도 latency는 별개.

**결정 질문 D5**: latency 5-30초 추가 OK? 또는 GPT-B/Shadow를 background async로 보내 사용자 답변 yield 후 별도로 reveal?

## Out of Scope for Phase 3 (Phase 4로 미룸)

- Evidence Arbiter 5축 판정
- green/yellow/red 추천
- main 자동 승격 결정
- Human Gate explicit confirm UX
- Opus → main 직접 차단 enforce (Phase 3는 "다른 worktree만 쓰게 가이드", Phase 4가 강제)

## Acceptance — 답변 받기 전 추정

D1=A graceful skip / D2=β / D3=i / D4=c / D5=직렬 5번 (latency 수십초) 가정 시:

1. 사용자가 git repo cwd에서 코드 변경 prompt 보냄
2. 시스템이 3 worktree 생성 (`.openclaude-shadows/A`, `B`, `opus`)
3. GPT-A 패치 worktree A에, GPT-B 패치 worktree B에, Opus 패치 worktree opus에 적용
4. cross-review: GPT가 3 후보 read + 평가, Opus가 3 후보 read + 평가
5. stdout에 매트릭스 요약 + 상세 파일 경로 출력
6. main 변경 zero (Phase 4까지 모두 read-only/shadow)

## Files (D1=A, D3=i 가정)

- `src/services/orchestra/shadowExecutor.ts` — worktree 생성/cleanup + 후보 생성
- `src/services/orchestra/crossReview.ts` — 3 후보 read + 2 reviewer 호출 + 매트릭스 생성
- `src/services/orchestra/worktreeManager.ts` — git worktree 라이프사이클 (add, remove, prune)
- `src/services/orchestra/shadowExecutor.test.ts`
- `src/services/orchestra/crossReview.test.ts`
- `src/services/orchestra/worktreeManager.test.ts`
- `src/query.ts` — 코드 변경 turn에서 hook (D2=β)
- `.planning/phase-3/cross-review-{ts}.md` — 매트릭스 영구 보관

## Risks

| R | Mitigation |
|---|------------|
| OpenClaude self-modify 위험 (자기 코드 수정 시 worktree 충돌) | Phase 3는 사용자 cwd가 OpenClaude 자체이면 자동 skip. self-bootstrap은 별도 phase. |
| 3 후보 패치가 서로 다른 파일 건드림 → "alternative" 의미 약화 | shadowExecutor가 각 worker에 같은 task scope를 동일하게 전달, "다른 접근법" prompt 명시 |
| worktree cleanup 실패 시 디스크 누수 | 매 turn 시작 전 stale worktree prune; 명시적 `/orchestra-cleanup-shadows` 슬래시 커맨드 |
| GPT-B/Opus Shadow가 Codex/OAuth 인증 fail로 silent skip | per-worker 실패는 매트릭스에 "execution_failed" cell로 기록 |
| Phase 3 직렬 호출로 turn latency 30s+ → 사용자 답답 | D5 결정에 따라 background async 옵션 고려 |
| 매 코드 turn 5 model call로 비용 폭증 | 사용자 "토큰 무한" 명시 — 비용 무시. 단 사용자가 후속 phase에서 정책 조정 가능하도록 `orchestra.shadowEnabled` 토글 추가 |

## Open Decision Summary

답해야 할 것 5개:
- **D1** (격리): A / B / C — 권장 A graceful skip
- **D2** (발사): α / β / γ — 권장 β
- **D3** (main 적용): i / ii — 권장 i
- **D4** (매트릭스 출력): a / b / c — 권장 c
- **D5** (latency): 직렬 OK / async — 권장 직렬

**기본안**: D1=A graceful skip, D2=β, D3=i, D4=c, D5=직렬.

답변이 다 default면 "ok" 하나면 진행. 다른 게 있으면 알려줘.
