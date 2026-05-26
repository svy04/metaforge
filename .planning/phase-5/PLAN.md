# Phase 5 Plan — 20-Task Validation Experiment

**Goal**: Opus 4.7의 unique value 정량 측정 인프라 + v0.3 결정 템플릿.

## Tasks

### 5.1 — `experimentMetrics.ts` (UVD, FPR, SDC, agreement)

**Public surface**:
```typescript
export type TaskOutcome = {
  taskId: string
  groundTruthDefects: string[]  // user-validated 실제 결함 set
  gptDefectsFlagged: string[]
  opusDefectsFlagged: string[]   // skeptic + shadow 합산
  scopeDrifts: { byGpt: string[]; byOpus: string[]; truth: string[] }
}

export type ExperimentMetrics = {
  totalTasks: number
  uvdRate: number   // unique valid defects only Opus caught / total truth defects
  fprRate: number   // Opus-flagged but NOT in truth / Opus total flagged
  sdcRate: number   // scope drifts only Opus caught / total truth drifts
  agreementWithGpt: number  // % of tasks where Opus and GPT defect sets overlap
  recommendation: 'keep' | 'demote' | 'remove'
}

export function computeExperimentMetrics(outcomes: TaskOutcome[]): ExperimentMetrics
```

**TDD**:
- 단순 fixture 입력 → 메트릭 계산 단언
- recommendation 임계값 (D5): keep ≥ 15% UVD OR ≥ 25% SDC; remove < 5% UVD AND < 10% SDC

### 5.2 — `scripts/orchestra-experiment-runner.ts` (scaffold)

20 task 디렉토리 입력 받아 mock 실행 또는 실제 실행, 결과를 `.planning/phase-5/results.jsonl`에 append.

이 task는 **scaffold only** — 실제 task를 어떻게 실행할지는 사용자 손에. mock pipeline 보여주는 것까지.

### 5.3 — Decision 템플릿

`.planning/phase-5/v0.3-decision-template.md` — 메트릭 결과 → keep/demote/remove → v0.3 ROADMAP 골격.

## Done

- 5.1 단위 테스트 pass
- 5.2 scaffold script 존재 (실제 20 task 실행 안 해도 됨)
- 5.3 템플릿 작성
- PROJECT.md M5 → 인프라 ✓ + 실제 experiment는 사용자 후속
