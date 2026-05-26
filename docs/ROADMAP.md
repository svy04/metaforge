# Roadmap

Status: first planning pass

The roadmap starts narrow and verifiable, then expands autonomy only when evals and guardrails prove the loop.

Harness update: Phase 1 now starts by importing MFH/Meta concepts as evidence-backed constraints. The goal is not to rebuild MFH inside OpenClaude; it is to connect Goal OS to Meta's operator OS and MFH's governed-code gates.

## Phase 0: Planning Package

Goal: Create the Autonomous Goal OS planning package.

Deliverables:

- `docs/PROJECT_SPEC.md`
- `docs/GOAL_SCHEMA.md`
- `docs/AGENT_REGISTRY.md`
- `docs/RESEARCH_PIPELINE.md`
- `docs/EVALS.md`
- `docs/SECURITY_AND_GUARDRAILS.md`
- `docs/ROADMAP.md`
- `docs/PROGRESS_LOG.md`
- `docs/DECISION_LOG.md`
- `docs/NEXT_GOALS.md`
- Updated `AGENTS.md`

Validation:

- Docs exist and internally cross-reference.
- Major claims have source, validation, or decision-log control.
- Available repo checks are attempted.

## Phase 1: Goal Kernel MVP

Goal: Turn this planning package into a machine-checkable goal kernel that carries Meta operator boundaries and MFH claim/evidence gates.

Scope:

- Add `docs/goals/` or `.planning/goals/` with one goal object per Codex Goal.
- Implement a schema validator script.
- Validate required fields from `docs/GOAL_SCHEMA.md`.
- Validate governed-code fields: claim level, claim boundary, authority sources, MFH gate requirements, and Meta decision links.
- Add a progress-log updater convention.

Success criteria:

- `bun run scripts/validate-goals.ts` or equivalent passes.
- At least one real Codex Goal is represented as a structured object.
- Missing success criteria, validation commands, pause conditions, or rollback strategy fail validation.

## Phase 2: Research Evidence Ledger

Goal: Make primary-source research auditable using Meta's raw/wiki/decision pattern.

Scope:

- Add `docs/research/` brief template.
- Add source ledger fields: type, URL/path, accessed date, claim supported, decision affected.
- Add rejection list for blog-only summaries.
- Tie research briefs to goals and decision log entries.
- Add a local-source lane for harness-engineering MFH/Meta artifacts.

Success criteria:

- One research brief validates against template.
- Every external claim in a goal links to source ledger or decision-log assumption.
- Blog-only final sources are rejected by checklist.

## Phase 3: Eval Flywheel

Goal: Make goal closure dependent on reproducible evidence and MFH-style closure gates.

Scope:

- Add docs/eval result format or structured `.planning/evals/*.json`.
- Run focused Orchestra tests and build for Orchestra-related goals.
- Add trace/eval checklist for agent workflows.
- Promote the existing 20-task experiment from mock to seeded real tasks.
- Add source-reconciliation and closure-reality checklist entries for any goal importing harness state.

Success criteria:

- Eval result artifacts capture command, exit code, summary, and follow-up.
- At least one failed eval creates a next Codex Goal.
- 20-task experiment has real tasks or a decision-log entry explaining why not.

## Phase 4: Skill Promotion Loop

Goal: Convert repeated successful workflows into Skills.

Scope:

- Define skill candidate report.
- Select one repeated workflow, likely primary-source research brief or docs consistency review.
- Create a Skill only after three successful manual runs.
- Add cold-start eval for the Skill.

Success criteria:

- Skill has `SKILL.md`, description, trigger, instructions, validation, and examples.
- Cold-start eval passes.
- `AGENTS.md` references the Skill only if it should be discoverable.

## Phase 5: Automation Promotion Loop

Goal: Convert stable recurring jobs into Automations.

Scope:

- Identify read-only recurring reports first.
- Dry-run manually three times.
- Add schedule, owner, scope, output path, pause condition, and rollback/no-op behavior.
- Use automation only after owner approval.

Success criteria:

- At least one A0 read-only automation candidate has three manual reports.
- Owner-approved schedule exists.
- Automation writes only to approved artifact path.

## Phase 6: Autonomous Narrow Domain Pilot

Goal: Let agents autonomously run a narrow domain from goal intake to next-goal proposal.

Candidate domains:

- Docs consistency and drift review.
- Primary-source weekly research report.
- Orchestra eval trend summary.
- MFH/Meta drift report that reads state and writes a report only.

Success criteria:

- Agent completes research, plan, edit/report, eval, reflection, and next-goal proposal without human micro-steering.
- Human only approves gates and strategic changes.
- Failure modes are recorded and lead to revised guardrails.

## Phase 7: Broader Orchestra Integration

Goal: Connect the goal kernel to existing Orchestra OS runtime surfaces.

Scope:

- Feed goal objects into planner prompts.
- Attach goal IDs to usage logs, shadow reviews, evidence matrices, and promotion store entries.
- Require `goalId` before `/orchestra-apply`.
- Create trace grading dataset for agent workflows.

Success criteria:

- Goal ID appears in planning, execution, eval, and promotion artifacts.
- Evidence Arbiter can read goal success criteria.
- Human Gate displays goal context and validation status.

## Program Goals

| Program | Description | First validation |
| --- | --- | --- |
| PG-001 Goal Kernel | Structured goals and validation | schema validator |
| PG-002 Research Pipeline | Primary-source briefs and source ledger | research checklist |
| PG-003 Eval Flywheel | Goal/eval/trace feedback loop | eval artifact |
| PG-004 Skill Promotion | Repeated workflows become skills | cold-start skill eval |
| PG-005 Automation Promotion | Stable jobs become automations | dry-run and approval |
| PG-006 Orchestra Integration | Goal IDs flow through runtime | focused Orchestra tests |
| PG-007 MFH/Meta Integration | Governed-code claim boundaries and Meta operator memory become part of goals | source reconciliation and goal schema validation |

## Non-Goals For This Roadmap

- No public deployment.
- No credential/account changes.
- No new provider activation.
- No destructive cleanup.
- No broad runtime refactor during planning.
- No automation creation until promotion criteria are met.
