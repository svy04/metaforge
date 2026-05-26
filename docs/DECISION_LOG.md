# Decision Log

Status: active

## D-001 - Define `mth` as Mission-to-Harness for the initial planning pass

Date: 2026-05-10
Status: superseded by D-008

Decision:

The initial OpenClaude-only pass did not contain a source definition for `mth`, so it temporarily defined `mth` as Mission-to-Harness. D-008 supersedes this after reading the harness-engineering `mfh` and `meta` projects.

Evidence:

- Targeted repo search found no project-specific `mth` definition.
- User asked to unify `mth`, `meta`, and Orchestra OS.

Consequence:

- Current docs now use MFH as the canonical concrete component and treat `mth` as an unresolved alias/spelling unless the owner defines it separately.

## D-002 - Treat existing `.planning/` and `src/services/orchestra/` as operative evidence

Date: 2026-05-10
Status: accepted

Decision:

The planning package treats `.planning/PROJECT.md`, `.planning/ROADMAP.md`, `.planning/phase-*`, and `src/services/orchestra/` as the current source of truth for Orchestra OS status.

Evidence:

- `.planning/PROJECT.md` contains detailed v0.2 role, milestone, and validation state.
- `src/services/orchestra/` contains tests and implementations for multiple planned roles.

Consequence:

- New docs do not restart the project from zero.
- Roadmap focuses on Goal OS integration and validation loops rather than re-specifying already implemented Orchestra primitives.

## D-003 - Keep AGENTS.md compact and move deep process into docs

Date: 2026-05-10
Status: accepted

Decision:

`AGENTS.md` remains the compact operating law. Detailed schema, evals, research workflow, security policy, roadmap, and next goals live in `docs/`.

Evidence:

- `AGENTS.md` is already large and contains many OpenClaude memory notes.
- The AGENTS.md open format recommends agent-focused instructions, build/test commands, and conventions, while project detail can live in docs.

Consequence:

- Future edits should add pointers and compact routing rules to `AGENTS.md`, not duplicate all docs.

## D-004 - Start autonomy with docs/research/eval domains

Date: 2026-05-10
Status: accepted

Decision:

The first autonomous domains are docs consistency, primary-source research briefs, Orchestra eval trend summaries, and Skill/Automation promotion reports.

Rationale:

- They are narrow, reversible, and evidence-friendly.
- They reduce owner bottleneck without granting unsafe write authority.

Consequence:

- Code modification autonomy remains gated by goal schema, tests, worktree isolation, and human approval.

## D-005 - Require primary-source controls for major claims

Date: 2026-05-10
Status: accepted

Decision:

Every major planning claim must have one of: local code evidence, primary source, validation method, or decision-log assumption.

Evidence:

- Existing `AGENTS.md` standing research rule.
- User's explicit instruction to prefer official docs, papers, patents, standards, and validated open-source implementations.

Consequence:

- Blog-only summaries cannot close research requirements.
- `docs/RESEARCH_PIPELINE.md` owns the source ladder and rejection rules.

## D-006 - Do not create Automations in this pass

Date: 2026-05-10
Status: accepted

Decision:

This pass defines automation promotion criteria but does not create recurring jobs.

Rationale:

- The user requested a planning package, not a live recurring job.
- Stable recurring jobs require three successful manual runs, scope, schedule, output path, pause condition, security review, and owner approval.

Consequence:

- `docs/NEXT_GOALS.md` includes a future goal to identify and dry-run automation candidates.

## D-007 - No runtime behavior changes in planning package

Date: 2026-05-10
Status: accepted

Decision:

This pass creates docs and updates project instructions only. It does not change runtime code, provider config, credentials, or live automation.

Rationale:

- The objective is a first high-resolution planning pass.
- Runtime changes should be separate Codex Goals with focused tests and rollback.

Consequence:

- Validation emphasizes docs consistency plus repo sanity commands.

## D-008 - Supersede provisional `mth` assumption with MFH evidence

Date: 2026-05-10
Status: accepted revision

Decision:

After reading `C:\Users\admin\Desktop\내 순수 재미\하네스 엔지니어링`, this package treats MFH as the canonical project component. The earlier `mth` term remains an unresolved alias/spelling unless the owner defines a separate `mth` project.

Evidence:

- Harness root contains `mfh` and `meta` directories, plus `MASTER_SPEC.md`, `NARROW_SPEC.md`, and `POSITIONING_BRIEF.md`.
- `mfh/.mfh/spec.md` defines MFH as a Claude Code Operating Gate.
- `meta/CLAUDE.md` and `meta/SPEC.md` define Meta as the operator OS and Constitution layer.

Consequence:

- `docs/PROJECT_SPEC.md` now defines `mth / mfh` as unresolved alias plus canonical MFH.
- `docs/MFH_META_SYNTHESIS.md` records the source read and planning import.

## D-009 - Adopt governed-code as the product category

Date: 2026-05-10
Status: accepted

Decision:

Autonomous Goal OS inherits the governed-code framing from MFH/Meta. The system should keep coding-agent freedom while turning intent, scope, risk, verification, and release decisions into evidence-backed gates the owner can judge.

Evidence:

- `meta/decisions/2026-05-05-2388-governed-code-problem-definition.md`.
- `POSITIONING_BRIEF.md`.
- `mfh/.mfh/spec.md` problem-definition section.

Consequence:

- Goal objects now include governed-code claim level and claim boundary.
- Security docs distinguish Operating Gate from security sandbox.
- Roadmap and next goals now include MFH/Meta gate validation.

## D-010 - Import Candidate M lifecycle into Goal OS

Date: 2026-05-10
Status: accepted

Decision:

Autonomous Goal OS should use Candidate M's state-machine lifecycle for goals with implementation or release implications:

```text
Pending -> Active -> Verifying -> Closed
                    \-> Failed -> Active
```

Evidence:

- `mfh/.mfh/spec.md` Candidate M state-machine invariant.
- `mfh/.mfh/plan.md` Candidate M closure and guardrails.
- `mfh/docs/reports/2026-05-09-candidate-m-closure.md`.

Consequence:

- `docs/GOAL_SCHEMA.md` now includes the MFH/Candidate M overlay.
- Goals cannot close from agent self-report alone.

## D-011 - Treat current harness state as drifted, not green

Date: 2026-05-10
Status: accepted evidence

Decision:

The OpenClaude plan may import MFH/Meta concepts, but it must not claim the harness workspace is currently clean or release-ready.

Evidence:

- `python meta\scripts\source_reconciler.py` from `C:\Users\admin\Desktop\내 순수 재미\하네스 엔지니어링` exited 1.
- Output reported `DRIFT`, with mfh working tree dirty: 9 modified and 3 untracked files.
- `.mfh/status.md` says `Current Milestone: awaiting user adjudication` and `Last Verification: not run`.

Consequence:

- `docs/EVALS.md` records EVAL-008 for source reconciliation.
- `docs/MFH_META_SYNTHESIS.md` marks the import as evidence-aware rather than a green-completion claim.
