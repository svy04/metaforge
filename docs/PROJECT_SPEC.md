# Metaforge Autonomous Goal OS Project Spec

Status: first high-resolution planning pass
Owner: human owner
Operating repo: `<repo>`
Canonical instruction entrypoint: `AGENTS.md`
Harness evidence update: `docs/MFH_META_SYNTHESIS.md`

## Summary

Metaforge is the public Meta + MFH + Orchestra OS project layered over the
OpenClaude CLI/runtime substrate. Its purpose is to make the human owner the
strategic governor, not the execution bottleneck. Agents should be able to
autonomously research, plan, implement, evaluate, reflect, and propose next
goals while leaving durable evidence, validation records, and approval gates.

This pass does not claim the runtime is complete. It creates the planning package that lets the next Codex goals implement the OS in narrow, verifiable increments.

Update after companion harness review: the concrete project component is
**MFH**, a governed-code Operating Gate, while Meta is the operator
Constitution / memory substrate. The earlier `mth` reference is treated as an
unresolved spelling or alias unless separately defined.

## Current Repository Basis

Observed local anchors:

- `README.md` defines Metaforge as Meta + MFH + Orchestra OS with OpenClaude as
  the local CLI/runtime substrate.
- `AGENTS.md` already defines the GStack -> GSD -> Superpowers workflow hierarchy and the primary-source research rule.
- Legacy planning artifacts and `src/services/orchestra/` define the existing
  Orchestra vision: a visible lead/evidence arbiter, private
  planner/skeptic/shadow opposition, tests as law, and the human as final
  judge, without making public model-lock claims. The legacy planning artifacts
  are no longer tracked public authority after the public hygiene cleanup.
- `src/services/orchestra/` already contains implementation surfaces for planner routing, skeptic, shadow executor contract, cross-review, evidence arbiter, human gate, promotion store, worktree manager, and experiment metrics.
- `package.json` exposes verification commands: `bun run build`, `bun test`, `bun run typecheck`, `bun run smoke`, `bun run doctor:runtime`, `bun run verify:privacy`.
- `docs/superpowers/specs/2026-05-05-agent-stack-integration-design.md` and its plan document establish the existing GStack/GSD/Superpowers role split.
- `docs/MFH_META_SYNTHESIS.md` records a public-safe summary of companion
  harness sources that define governed-code, Meta, MFH, and Candidate M.
- Companion Meta sources define Meta as the operator OS: Constitution, decision
  ledger, raw/wiki substrate, technical-decision autonomy, and approval
  boundaries.
- Companion MFH sources define MFH as an Operating Gate that judges drift,
  evidence, state, permissions, and release claims rather than acting as a
  coding agent.
- Companion Candidate M records define the 3-layer vision/session anchor and
  state-machine closure pattern.
- The latest harness source-reconciliation probe reported drift, so the import
  is evidence-aware, not a green-completion claim.

External primary-source anchors:

- OpenAI Agents SDK evolution: controlled workspaces, explicit instructions, MCP, skills, AGENTS.md, shell/apply-patch tools, sandboxing, and checkpoint restore: https://openai.com/index/the-next-evolution-of-the-agents-sdk/
- AGENTS.md open format for agent instructions: https://agents.md/
- Agent Skills open format: https://agentskills.io/
- MCP intro and server features: https://modelcontextprotocol.io/docs/getting-started/intro, https://modelcontextprotocol.io/specification/2025-06-18/server/resources, https://modelcontextprotocol.io/specification/2025-06-18/server/prompts, https://modelcontextprotocol.io/specification/2024-11-05/server/tools
- OpenAI agent evals and trace grading: https://developers.openai.com/api/docs/guides/agent-evals, https://developers.openai.com/api/docs/guides/trace-grading
- OpenAI Evals repository: https://github.com/openai/evals
- NIST AI RMF 1.0: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- W3C PROV overview: https://www.w3.org/TR/prov-overview/
- ReAct paper: https://arxiv.org/abs/2210.03629
- Reflexion paper: https://arxiv.org/abs/2303.11366
- USPTO Patent Public Search: https://www.uspto.gov/patents/search/patent-public-search/

## Role Definitions

### mth / mfh

The public Metaforge role is **MFH**, a governed-code Operating Gate. The
earlier `mth` spelling has no current source definition in this repository, so
this planning package treats it as an unresolved alias/spelling and uses MFH as
the canonical role until the owner says otherwise.

Responsibilities:

- Judge whether execution claims are backed by measured evidence.
- Detect and surface goal drift, false completion, state-integrity risk, scope drift, and weak verification.
- Require closure reports, source reconciliation, ledger evidence, and explicit claim boundaries before success claims.
- Keep the system in governed-code mode: the agent may execute, but product/risk/release approval remains evidence-backed.

### meta

Meta is the governance, memory, and operator Constitution layer. Companion Meta
sources define the operator boundary, decision ledger, LLM Wiki substrate, raw
immutable source storage, and escalation rules.

Responsibilities:

- Preserve decisions, assumptions, evidence paths, progress, and next goals.
- Maintain source-of-truth separation between chat state, repo docs, runtime logs, and eval outputs.
- Keep the human owner out of technical-stack, architecture, code-review, performance, and security decision bottlenecks.
- Escalate taste, product direction, irreversible actions, credentials, public actions, and unresolved conflicts.
- Promote successful repeated workflows into Skills only after evidence.
- Promote stable recurring checks into Automations only after explicit scope and safety review.

### Orchestra OS

Orchestra OS is the multi-agent execution and challenge layer already partially implemented under `src/services/orchestra/`.

Responsibilities:

- Route Codex/GPT as visible writer/executor.
- Route Opus or equivalent opposition as private planner, skeptic, reviewer, or shadow candidate, without direct mainline write authority.
- Generate cross-review and evidence-arbiter outputs.
- Keep human approval for irreversible or high-risk changes.

### Autonomous Goal Operating System

The unified OS is the composition:

- Meta defines the operator boundary, decision ledger, raw/wiki memory, and approval semantics.
- Goal Kernel defines and decomposes durable goals.
- Orchestra OS executes and challenges work through agents, evals, and gates.
- MFH judges closure, drift, evidence, and claim integrity.

## North Star

Build an evidence-driven agent operating system where the human owner sets direction and approval boundaries, while agents autonomously move narrow domains from research to plan to implementation to eval to reflection to next goal proposals.

Governed-code version: preserve Claude Code/OpenClaude freedom, but turn intent, scope, risk, verification, and release decisions into evidence that a non-technical product owner can judge.

## Goal Hierarchy

| Level | Purpose | Owner | Time horizon | Output |
| --- | --- | --- | --- | --- |
| North Star Goal | Durable strategic direction | Human owner | months | `docs/PROJECT_SPEC.md` |
| Program Goals | Major capability tracks | Orchestrator + human gate | weeks | `docs/ROADMAP.md` |
| Sprint Goals | Narrow verifiable increments | Orchestrator | days | `docs/PROGRESS_LOG.md`, `docs/NEXT_GOALS.md`, product-quality reports |
| Codex Goals | Executable `/goal` prompts | Codex lead | one session | `docs/NEXT_GOALS.md` |
| Atomic Tasks | Small testable actions | assigned agent role | minutes-hours | diffs, tests, evidence entries |

## Operating Loop

1. Intake a Codex Goal with explicit success criteria and non-goals.
2. Classify the request through AGENTS.md routing:
   - GStack for idea, judgment, primary-source research, spec challenge.
   - GSD for phase decomposition and execution state.
   - Superpowers for TDD, debugging, code review, and verification.
3. Create or update a goal object from `docs/GOAL_SCHEMA.md`.
4. Research from primary sources first. Blog-only summaries are rejected unless they are only used to discover original sources.
5. Run implementation in the narrowest verifiable domain.
6. Produce eval evidence using unit tests, integration probes, trace grading, security checks, or manual review checklists.
7. Reflect: decide continue, revise, pause, rollback, promote to Skill, promote to Automation, or propose next goal.
8. Update progress, decision, and next-goals artifacts.

MFH/Candidate M lifecycle overlay:

```text
Pending -> Active -> Verifying -> Closed
                    \-> Failed -> Active
```

`Closed` requires evidence artifacts, validation output, dirty-state attribution where applicable, and a progress/decision record. `Failed` returns to `Active` only after diagnosis or owner adjudication.

## Agent/Tool Surface Policy

| Surface | Use | Guardrail |
| --- | --- | --- |
| Codex `/goal` | Main executable unit for a session | Must include success criteria and stopping condition |
| `AGENTS.md` | Compact project operating law | Keep stable and short; deep detail belongs in docs |
| Skills | Reusable verified workflows | Promote only after repeated successful execution and eval |
| MCP | Typed access to external data/tools/workflows | Validate server, resource URI, tool schema, and permissions |
| Subagents | Parallel independent side work | Use only with disjoint scope and explicit ownership |
| Automations | Stable recurring jobs | Human-approved schedule, bounded permissions, clear output artifact |
| Evals | Regression and quality flywheel | Required before promoting autonomy level |

## Initial Narrow Domains

The system starts with narrow domains because autonomy without evidence is just unsupervised drift.

1. Documentation/governance package maintenance.
2. Primary-source research briefs with source ledger.
3. Orchestra OS validation and experiment metrics.
4. Skill promotion for repeated repo workflows.
5. Automation candidates that only read state and write reports until proven safe.

## Claim Controls

| Claim | Control |
| --- | --- |
| Human owner should not be execution bottleneck | North Star and roadmap decision; validate by autonomous goal completion count |
| Agents can research-plan-implement-evaluate-reflect | Requires goal object, role registry, research pipeline, evals, progress log |
| Research must prefer primary sources | `docs/RESEARCH_PIPELINE.md` source ladder and rejection rules |
| Start narrow, align to larger vision | `docs/ROADMAP.md` phase gates |
| Goals are durable/revisable/evidence-driven | `docs/GOAL_SCHEMA.md` and decision/progress logs |
| Security uses deterministic guardrails first | `docs/SECURITY_AND_GUARDRAILS.md`, OWASP/NIST controls, explicit approvals |
| MFH/Meta have already solved part of this | `docs/MFH_META_SYNTHESIS.md` summarizes companion harness evidence; imported as evidence, not as current green status |
| Governed-code is the category | Companion harness positioning sources and `docs/DECISION_LOG.md` |

## First Package Acceptance

This planning package is acceptable when:

- All requested docs exist.
- `AGENTS.md` points agents to the package and preserves the existing GStack/GSD/Superpowers split.
- Progress log records the inspection, writing, and validation checkpoints.
- Decision log records major assumptions, especially the `mth` naming assumption.
- `docs/NEXT_GOALS.md` contains three executable Codex `/goal` commands.
- Available repo validation commands were attempted and outcomes recorded.
