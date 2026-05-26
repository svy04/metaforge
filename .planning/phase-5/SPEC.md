# Phase 5 Spec — 20-Task Validation Experiment

**Status**: Draft (default-go: 사용자가 다 진행하라고 명시).
**Goal**: Opus 4.7의 unique value를 정량 측정. v0.3 결정 (Opus 유지 vs 강등 vs 제거)을 데이터 기반으로 정당화.

## 핵심 질문

> Opus가 GPT 5.5보다 못해도, **다르게 틀린다면** 가치 있다.
> 20개 실제 task에서 Opus가 GPT가 놓친 valid defect를 잡은 비율 vs 잡지 못한 false positive 비율은?

## 핵심 결정 (Defaults Go)

| Decision | Default |
|----------|---------|
| **D1 Task 출처** | `.planning/phase-5/tasks/*.md` 20개 (사용자 manual seed). PROJECT/MFH 등 실 작업 회고. |
| **D2 모델 조합** | GPT-A primary + GPT-B alternative + Opus Skeptic + Opus Shadow (4 출력) |
| **D3 Ground truth** | 실제 적용 결과 + 사용자 retrospective (사후 평가). `.planning/phase-5/ground-truth.jsonl` |
| **D4 메트릭** | 4개 — UVD(unique valid defect catch rate), FPR(false positive rate), SDC(scope drift catch rate), agreement-with-GPT(Opus와 GPT 답변 차이 정도) |
| **D5 결정 임계값** | Opus 유지 = `UVD ≥ 15% OR SDC ≥ 25%`. 강등 = `5% ≤ UVD < 15%`. 제거 = `UVD < 5% AND SDC < 10%`. |

## What Phase 5 Delivers

- `scripts/orchestra-experiment-runner.ts` — 20 task 시뮬레이션/실행 + jsonl 결과 수집
- `src/services/orchestra/experimentMetrics.ts` — 메트릭 계산 함수 (UVD/FPR/SDC/agreement)
- `src/services/orchestra/experimentMetrics.test.ts` — 단위 테스트
- `.planning/phase-5/results-template.md` — 결과 채울 표
- `.planning/phase-5/v0.3-decision-template.md` — 결정 문서 템플릿

## Out of Scope (Phase 5에선 안 함)

- 실제 20 task 실행 — *사용자가 별도 시간에 직접* (자동화는 Phase 5 인프라까지만)
- Opus가 *왜* 다르게 틀렸는지 정성 분석 — 수동
- Mythos Preview 통합 — 별도 마일스톤

## Acceptance

- 메트릭 함수 단위 테스트 통과
- experiment-runner 스크립트가 mock task 한 개로 jsonl 라인을 정확히 produce
- decision 템플릿이 메트릭 → 결정 매핑 표 포함
