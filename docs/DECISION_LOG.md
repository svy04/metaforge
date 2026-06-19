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

## D-002 - Treat legacy planning artifacts and `src/services/orchestra/` as operative evidence

Date: 2026-05-10
Status: superseded public-surface wording

Decision:

The initial planning package imported legacy planning artifacts and
`src/services/orchestra/` as evidence that Orchestra OS was not starting from
zero. The tracked public checkout no longer treats the removed planning
artifacts as current authority; current public authority lives in `docs/`,
`src/services/orchestra/`, and generated product-quality evidence.

Evidence:

- Legacy planning artifacts contained detailed v0.2 role, milestone, and validation state before public hygiene cleanup.
- `src/services/orchestra/` contains tests and implementations for multiple planned roles.
- PR #92 removed tracked planning artifacts from the public checkout and added
  hygiene gates so public docs cannot rely on private/local planning state.

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

The provisional `mth` assumption is superseded by canonical MFH evidence unless
the owner defines a separate `mth` project.

Evidence:

- `docs/MFH_META_SYNTHESIS.md` records the public-safe synthesis.
- `docs/PROJECT_SPEC.md` defines the public Meta/MFH/Orchestra product frame.
- `docs/GOAL_SCHEMA.md` records the public evidence-gated closure schema.

Consequence:

- `docs/PROJECT_SPEC.md` now defines `mth / mfh` as unresolved alias plus canonical MFH.
- `docs/MFH_META_SYNTHESIS.md` records the source read and planning import.

## D-009 - Adopt governed-code as the product category

Date: 2026-05-10
Status: accepted

Decision:

Autonomous Goal OS inherits the governed-code framing from MFH/Meta. The system should keep coding-agent freedom while turning intent, scope, risk, verification, and release decisions into evidence-backed gates the owner can judge.

Evidence:

- `docs/MFH_META_SYNTHESIS.md`.
- `docs/PROJECT_SPEC.md`.
- `docs/SECURITY_AND_GUARDRAILS.md`.

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

- `docs/MFH_META_SYNTHESIS.md` state-machine synthesis.
- `docs/GOAL_SCHEMA.md` closure and rollback schema.
- `docs/EVALS.md` verification gate import.

Consequence:

- `docs/GOAL_SCHEMA.md` now includes the MFH/Candidate M overlay.
- Goals cannot close from agent self-report alone.

## D-011 - Treat current harness state as drifted, not green

Date: 2026-05-10
Status: accepted evidence

Decision:

The OpenClaude plan may import MFH/Meta concepts, but it must not claim the harness workspace is currently clean or release-ready.

Evidence:

- Private owner-side harness state was not re-verified as a public artifact.
- `docs/MFH_META_SYNTHESIS.md` records the import as evidence-aware rather than
  green-complete.

Consequence:

- `docs/EVALS.md` records EVAL-008 for source reconciliation.
- `docs/MFH_META_SYNTHESIS.md` marks the import as evidence-aware rather than a green-completion claim.

## D-012 - Adopt Mimesis Engineering as the Metaforge improvement loop

Date: 2026-06-14
Status: accepted

Decision:

Metaforge treats Mimesis Engineering as its source-first improvement loop: find proven artifacts, extract their load-bearing structure, adapt only the structure into Meta/MFH/Orchestra work, and keep claims bounded by local verification.

Evidence:

- `docs/RESEARCH_PIPELINE.md` already requires local-first, primary-source research.
- `docs/avf/OSS_ASSIMILATION_PIPELINE.md` defines governed acquisition instead of copy-paste adoption.
- `docs/research/mimesis-engineering-source-ledger-2026-06-14.md` records current product, OSS, paper, patent, and standards sources.

## D-013 - Validate current Codex Goals before migrating historical goal artifacts

Date: 2026-06-18
Status: accepted

Decision:

The Goal Kernel MVP validates current structured Codex Goal files named
`CG-*.md` before attempting to migrate older AVF or Influence Factory local
goal artifacts.

Evidence:

- `docs/GOAL_SCHEMA.md` defines the required Goal OS object.
- `docs/NEXT_GOALS.md` asks for one real goal file and a narrow validator.
- `docs/goals/` already contains many historical local artifacts that are
  useful evidence but were not authored against the new schema.

Consequence:

- `scripts/validate-goals.ts` treats `docs/goals/CG-*.md` as the current
  machine-checkable registry.
- Historical goal artifacts remain public-surface-scanned evidence, but they
  are not rewritten or treated as schema-valid Goal Kernel records in this
  slice.

## D-014 - Add Goal Kernel trace-policy evidence before stronger marketing

Date: 2026-06-18
Status: accepted

Decision:

Metaforge should not market Goal Kernel closure from schema validity alone.
The public proof path now requires a local no-provider goal trace gate in
addition to the `CG-*.md` schema validator.

Evidence:

- Community feedback called out file-existence, marker, and hardcoded-flag
  audits as weaker than behavioral happy-path, edge-case, and side-effect
  checks.
- `docs/GOAL_SCHEMA.md` says goals cannot move to `validated` or `closed`
  without fresh evidence.
- OpenTelemetry, Open Policy Agent, OpenAI agent eval trace grading, and NIST
  AI RMF Playbook patterns all favor structured traces, policy decisions,
  eval records, and proportional risk evidence over narrative-only claims.

Consequence:

- `scripts/validate-goals.ts` rejects `validated` or `closed` goals when
  required validation commands do not have passing `evidence.testResults`.
- `scripts/validate-goal-traces.ts` validates source-controlled goal traces for
  ordered goal-loaded, checkpoint, validation, claim-review, and validated
  events.
- `bun run goals:validate` now runs both schema and trace validation.
- The new proof remains local no-provider evidence only, not production
  readiness, hosted deployment, external validation, benchmark superiority, or
  autonomous reliability.

## D-015 - Gate Goal OS research claims with a primary-source brief ledger

Date: 2026-06-18
Status: accepted

Decision:

Goal OS prior-art and governed-code research claims require a structured
primary-source brief before they can support public proof copy, roadmap
language, eval changes, guardrail changes, or stronger marketing language.

Evidence:

- `docs/RESEARCH_PIPELINE.md` already requires local-first primary-source
  research and the Meta raw/wiki/decision flow.
- `docs/research/goal-os-governed-code-prior-art-2026-06-18.md` maps local
  authority docs plus official/original external sources to requirements,
  evals, guardrails, and decisions.
- `scripts/validate-research-briefs.ts` validates required source coverage,
  secondary-source rejection, mapping coverage, and explicit claim boundaries.
- `docs/product-quality/research-brief-validation-report.json` records the
  local no-provider report and HTTPS `primarySourceInputs` for the existing
  primary-source registry.

Consequence:

- `bun run research:validate` is now the local gate for current
  `docs/research/goal-os-*.md` briefs.
- `product:quality` runs the research brief validator before
  `product:primary-source-registry`, so generated research source inputs are
  included in downstream evidence inventory.
- This is research governance evidence only; it does not claim production
  readiness, hosted deployment, external validation, benchmark superiority,
  standards compliance, patent clearance, or autonomous reliability.

## D-016 - Treat the first Eval Flywheel as local proposal evidence

Date: 2026-06-18
Status: accepted

Decision:

The first Autonomous Goal OS Eval Flywheel records local no-provider evidence
only. Automation candidates are proposed-only, owner-side MFH/Meta drift is
carried forward until owner adjudication, and the Orchestra experiment runner
result is recorded as mock fallback unless a real source-controlled task set is
present.

Evidence:

- `docs/EVALS.md` defines L0-L5 and EVAL-008 through EVAL-010.
- `docs/SECURITY_AND_GUARDRAILS.md` defines automation tiers and approval
  gates.
- `scripts/orchestra-experiment-runner.ts` used its one-task mock fallback
  because a source-controlled 20-task experiment task set was absent.
- `docs/evals/autonomous-goal-os-minimal-checklist.md` records the mock
  fallback run and real 20-task non-run status.
- `docs/reports/automation-candidates-2026-06-18.md` keeps every candidate
  proposed-only and blocks external-call candidates until owner approval.
- `scripts/validate-eval-flywheel.ts` validates eval levels, required eval
  imports, automation proposal boundaries, and MFH/Meta drift boundary.

Consequence:

- `bun run evals:validate` is now the local gate for the first eval flywheel
  artifact set.
- `product:quality` runs `evals:validate` before
  `product:primary-source-registry`.
- This slice does not create automations, schedule jobs, call providers, call
  live models, call external services, execute protected actions, claim a real
  20-task experiment, or claim production/external/autonomous readiness.

## D-017 - Upgrade MFH trace evidence from a single happy path to a representative pack

Date: 2026-06-19
Status: accepted

Decision:

MFH trace evidence should include a representative local no-provider pack, not
only one happy-path closure trace. The first pack for `CG-001` covers:

- `validated`: passing command evidence and clean claim review.
- `rejected`: missing or failed command evidence blocks validation.
- `blocked`: a protected action is denied without executing side effects.

Evidence:

- Korean community feedback specifically called out marker-only and
  file-presence checks as weak proof compared with happy-path, edge-case, and
  side-effect behavior checks.
- `scripts/validate-goal-traces.test.ts` now exercises accepted rejected and
  blocked traces and requires representative coverage.
- `docs/product-quality/goal-trace-validation-report.md` records 3/3 valid
  trace fixtures and zero provider, live model, external, or protected calls.

Consequence:

- MFH can now claim representative local trace-validation evidence for the
  first Goal Kernel slice.
- Broader MFH reliability claims remain blocked until cross-goal runtime
  traces, live-provider evidence, and broader side-effect behavior coverage
  exist.
