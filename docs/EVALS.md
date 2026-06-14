# Evals

Status: first planning pass

Evals are the proof layer for the Autonomous Goal OS. They decide whether a goal is validated, whether a workflow can become a Skill, whether a recurring job can become an Automation, and whether autonomy can expand.

Harness update: MFH/Meta add two important proof patterns: source reconciliation before trusting state, and closure reality checks before accepting completed milestones.

## Existing Repo Validation Commands

From `package.json`:

| Command | Purpose | When to run |
| --- | --- | --- |
| `bun run build` | Compile/build runtime | Any runtime/source change; sanity check for planning package |
| `bun test` | Full Bun test suite | Shared runtime or orchestration changes |
| `bun run typecheck` | TypeScript no-emit check | TS code changes |
| `bun run smoke` | Build plus CLI version probe | Release/runtime sanity |
| `bun run doctor:runtime` | Provider/env reachability diagnostics | Provider, auth, or runtime config changes |
| `bun run verify:privacy` | No-phone-home/privacy check | Security-sensitive changes |
| `bun run security:pr-scan -- --base <ref>` | Suspicious PR intent scan | PR/release flow |

CI also runs Python tests under `python/tests` according to `.github/workflows/pr-checks.yml`.

## Goal Validation Levels

| Level | Evidence | Required for |
| --- | --- | --- |
| L0 artifact | File exists, schema/checklist passes | Draft docs |
| L1 static | Typecheck, lint, docs link checks | Code/docs consistency |
| L2 unit | Focused unit tests pass | Functions/modules |
| L3 integration | CLI/script/probe proves behavior | Multi-module behavior |
| L4 trace | Trace grading or workflow transcript proves correct sequence | Agent workflows |
| L5 longitudinal | Repeated runs across tasks/time | Skill and automation promotion |

No goal closes above L0 without fresh evidence.

## Minimal Validation Checklist

Use this when no dedicated test exists:

- Required artifacts exist.
- Internal links and referenced paths are valid.
- Each major claim has a source, validation method, or decision-log entry.
- Non-goals and pause conditions are explicit.
- Rollback strategy exists.
- `docs/PROGRESS_LOG.md` records what was run and what was not run.
- `docs/NEXT_GOALS.md` includes executable next goals.

## Core Future Evals

### EVAL-001 Goal Schema Completeness

Question: Does every active goal include the required schema fields?

Method:

- Parse goal documents or YAML frontmatter once goal files exist.
- Check required fields: id, level, parent, objective, non-goals, success criteria, validation commands, checkpoints, pause conditions, rollback strategy, research requirements.

Initial manual checklist:

```powershell
Select-String -Path docs\*.md -Pattern 'pauseConditions|rollbackStrategy|successCriteria|validationCommands'
```

Pass condition:

- Every active Codex Goal has all required fields or a decision-log exception.

### EVAL-002 Primary-Source Research Compliance

Question: Are research-backed decisions using primary sources rather than blog-only summaries?

Method:

- For every research brief, inspect source ledger.
- Reject entries where final support is a blog without original source.

Pass condition:

- 100% of major architecture/security/eval claims have local code, official docs, original repo, paper, patent, standard, or decision-log assumption.

### EVAL-003 Orchestra Goal Loop

Question: Can Orchestra OS run planner/skeptic/shadow/evidence gates without collapsing role boundaries?

Current local evidence:

- `.planning/PROJECT.md` records Phase 2 skeptic and Phase 3-5 infrastructure.
- `src/services/orchestra/` has tests for config, orchestrator, skeptic, shadow executor, cross-review, evidence arbiter, human gate, promote, promotion store, experiment metrics, and worktree manager.

Suggested command set:

```powershell
bun test src/services/orchestra/config.test.ts src/services/orchestra/orchestrator.test.ts src/services/orchestra/skeptic.test.ts src/services/orchestra/evidenceArbiter.test.ts src/services/orchestra/experimentMetrics.test.ts
bun run build
```

Pass condition:

- Focused tests pass.
- No role violates authority: Opus advisory/shadow cannot write to main without human gate.

### EVAL-004 Skill Promotion Readiness

Question: Is a repeated workflow ready to become a Skill?

Method:

- Review three successful progress-log entries.
- Run the workflow from cold start using only the proposed `SKILL.md`.
- Check bundled scripts/templates exist.
- Check no secrets or excessive permissions are embedded.

Pass condition:

- Cold-start run succeeds.
- Security checklist passes.
- Skill has name, description, when-to-use, instructions, validation, and examples.

Primary source: https://agentskills.io/

### EVAL-005 Automation Promotion Readiness

Question: Is a recurring job safe to automate?

Method:

- Dry-run automation prompt manually.
- Confirm schedule, owner, outputs, pause condition, and rollback/no-op behavior.
- Confirm it only reads or writes approved artifacts until a stronger approval exists.

Pass condition:

- Three manual runs produce useful artifacts.
- Owner approves schedule.
- Security approves permissions.

### EVAL-006 Trace Grading For Agent Workflows

Question: Did the agent choose the right tools, handoffs, and guardrails?

Method:

- Capture representative traces or transcripts.
- Grade tool choice, handoff timing, instruction adherence, safety-policy adherence, and final output quality.

Primary sources:

- https://developers.openai.com/api/docs/guides/agent-evals
- https://developers.openai.com/api/docs/guides/trace-grading

Pass condition:

- Regression threshold is defined per workflow.
- Failed traces create follow-up Codex Goals.

### EVAL-007 20-Task Orchestra Value Experiment

Question: Does Opus opposition provide unique valid defect detection or scope-drift catch value?

Current implementation:

- `src/services/orchestra/experimentMetrics.ts`
- `scripts/orchestra-experiment-runner.ts`
- `.planning/phase-5/summary-2026-05-07T12-40-41-319Z.md`

Suggested command:

```powershell
bun run scripts/orchestra-experiment-runner.ts
```

Pass condition:

- Real task set has 20 outcomes, not only mock data.
- Recommendation follows UVD/FPR/SDC thresholds in code and `.planning/phase-5/SPEC.md`.

### EVAL-008 MFH Source Reconciliation Import

Question: Are the five authority sources consistent before Goal OS imports MFH/Meta state?

Harness command:

```powershell
python meta\scripts\source_reconciler.py
```

Run from:

```text
<private-workspace>/status.md` says `awaiting user adjudication`.

Pass condition:

- Exit 0 and no drift findings before claiming harness state is currently green.

Planning consequence:

- This OpenClaude package may import MFH/Meta concepts, but it must not claim the harness workspace is clean or release-ready.

### EVAL-009 Closure Reality Gate

Question: Does a completed milestone have ledger evidence, not just a completed marker?

Harness source:

```text
<private-workspace>\mfh\bench\closure_reality_check.py
```

Method:

- Parse `.mfh/plan.md`.
- For completed/shipped milestones, check `.mfh/events.jsonl` for the canonical source and event prefix.
- Classify each milestone as `PROVEN`, `PARTIAL`, or `UNPROVEN`.

Imported rule:

- Autonomous Goal OS must not close a goal solely from agent self-report or a status label.
- Closure requires validation output, evidence artifact, claim boundary, and where relevant ledger/source-reconciliation proof.

### EVAL-010 Governed-Code Claim Ledger

Question: Are claims tagged at the right level?

Claim levels:

- North Star: long-term direction.
- Category: governed-code / Operating Gate positioning.
- Internal substrate: deterministic local behavior and tests.
- External user validated: independent user/project evidence.

Pass condition:

- Public/product claims do not exceed their evidence level.
- External user success, production readiness, CTO replacement, and security-sandbox claims are blocked unless separately validated.

## Eval Result Record

Use this format in `docs/PROGRESS_LOG.md`:

```markdown
## YYYY-MM-DD HH:mm Eval
- Goal:
- Command:
- Exit code:
- Output summary:
- Pass/fail:
- Follow-up:
```
