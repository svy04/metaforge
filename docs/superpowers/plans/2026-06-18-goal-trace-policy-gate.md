# Goal Trace Policy Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a local no-provider Goal Kernel trace gate that proves a goal can be behaviorally evaluated for happy path, edge-case, and side-effect boundaries.

**Architecture:** Keep the existing Markdown goal validator intact and add a separate JSON trace evaluator. The evaluator grades source-controlled goal traces against MFH closure rules: a goal cannot validate without successful command evidence, claim-boundary review, and no provider/live/external/protected side effects.

**Tech Stack:** Bun test, TypeScript scripts, existing `yaml` dependency only for the existing goal validator, source-controlled JSON/Markdown evidence reports.

---

### Task 1: Trace Evaluator TDD

**Files:**
- Create: `scripts/validate-goal-traces.test.ts`
- Create: `scripts/validate-goal-traces.ts`

- [ ] **Step 1: Write the failing tests**

Add tests for:
- accepting a valid CG-001 trace with loaded, checkpoint, validation, claim review, and validated events;
- rejecting validation without command evidence;
- rejecting protected actions, provider calls, live model calls, or external calls;
- rejecting a trace whose `goalId` is not present in the goal registry.

- [ ] **Step 2: Run test to verify RED**

Run: `bun test scripts/validate-goal-traces.test.ts`
Expected: FAIL because `scripts/validate-goal-traces.ts` does not exist.

- [ ] **Step 3: Implement minimal evaluator**

Implement exported `evaluateGoalTrace(trace, knownGoalIds)` and `buildGoalTraceReport(traceFiles, knownGoalIds)`.

- [ ] **Step 4: Run test to verify GREEN**

Run: `bun test scripts/validate-goal-traces.test.ts`
Expected: PASS.

### Task 2: Source-Controlled Trace Fixture And Report

**Files:**
- Create: `docs/goals/traces/CG-001-goal-kernel-mvp.trace.json`
- Create/update by command: `docs/product-quality/goal-trace-validation-report.json`
- Create/update by command: `docs/product-quality/goal-trace-validation-report.md`
- Modify: `package.json`

- [ ] **Step 1: Add valid trace fixture**

Create one local no-provider trace fixture for `CG-001` with no provider, live model, external, or protected actions.

- [ ] **Step 2: Add package scripts**

Add `goals:trace:validate` and include it in `goals:validate`.

- [ ] **Step 3: Run validator**

Run: `bun run goals:trace:validate`
Expected: PASS and generated product-quality report files.

### Task 3: Public Evidence Wiring

**Files:**
- Modify: `README.md`
- Modify: `README.ko.md`
- Modify: `docs/DECISION_LOG.md`
- Modify: `docs/PROGRESS_LOG.md`
- Modify: `docs/product-quality/public-feedback-triage-2026-06-15.md`
- Update by command if needed: `docs/product-quality/product-evidence-manifest.*`

- [ ] **Step 1: Update proof wording**

Add the Goal Trace gate as L4-style local trace evidence, with explicit non-claims.

- [ ] **Step 2: Update logs**

Record the decision and progress with command evidence.

- [ ] **Step 3: Refresh manifest if evidence count changes**

Run: `bun run product:evidence-manifest`
Expected: PASS and updated manifest count/hash.

### Task 4: Verification And Publication

**Files:**
- All changed files

- [ ] **Step 1: Focused verification**

Run:
- `bun test scripts/validate-goal-traces.test.ts`
- `bun run goals:validate`
- `bun run build`
- `bun run product:public-claim-boundary:check`
- `bun run verify:privacy`

- [ ] **Step 2: Stage, commit, push, PR**

Use branch `codex/goal-trace-policy-gate`, push, open PR, inspect CI, and merge only if checks pass.
