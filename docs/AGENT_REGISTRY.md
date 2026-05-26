# Agent Registry

Status: first planning pass

This registry defines the roles used by the Autonomous Goal OS. Roles are responsibilities, not necessarily separate model processes. A single Codex session may perform multiple roles unless the goal explicitly launches subagents.

Harness update: Meta and MFH are not just agent roles. They are persistent operating systems around the agents: Meta governs operator boundaries and memory; MFH governs evidence and closure.

## Role Map

| Role | Primary responsibility | Default authority | Evidence required |
| --- | --- | --- | --- |
| Orchestrator | Owns goal state, routing, checkpoints, and stop/go calls | Can plan, assign, integrate | Updated goal/progress/decision records |
| Researcher | Finds primary sources and rejects weak evidence | Read-only | Source ledger with original URLs or local file paths |
| Architect | Converts research into design and boundaries | Read-only until approved | Design notes, alternatives, risks |
| Implementer | Makes scoped edits | Write only within goal target set | Diff plus validation commands |
| Eval | Runs tests, probes, trace grading, and checklist verification | Read/test | Test/probe output summaries |
| Security | Reviews permissions, sandboxing, secrets, approvals, and abuse cases | Veto on unsafe actions | Guardrail notes and approval requirements |
| Memory Librarian | Promotes repeated workflows into Skills or Automations | Propose only unless owner approves | Repetition evidence and eval history |

## Persistent Operating Systems

| System | Role in Autonomous Goal OS | Must not become |
| --- | --- | --- |
| Meta | Operator Constitution, decision ledger, raw/wiki memory substrate, escalation rules | A runtime executor or coding agent |
| Goal Kernel | Durable hierarchy, goal objects, validation commands, pause/rollback, claim boundaries | A vague task list |
| Orchestra OS | Multi-agent planner/skeptic/shadow/review/evidence-arbiter execution layer | The sole source of truth |
| MFH | Governed-code Operating Gate: drift, state, evidence, closure, claim integrity | A general coding agent or security sandbox |

## Existing Workflow Stack

| System | OS responsibility | Use when |
| --- | --- | --- |
| GStack | Product judgment, ideation, architecture challenge, design/eng/security review | Goal is vague, strategic, or taste/risk-heavy |
| GSD | Phase decomposition, long-running state, `.planning/` continuity | Work spans multiple sessions or implementation phases |
| Superpowers | TDD, debugging, code review, verification discipline | Concrete code/docs implementation or bug investigation |
| Orchestra OS | Multi-model planner, skeptic, shadow candidates, cross-review, evidence arbiter | Goal benefits from independent challenge or candidate comparison |
| MFH | Evidence gate, closure reality, source reconciliation, claim-boundary enforcement | Completion, release, or autonomy expansion needs proof |
| Meta | Constitution, decision ledger, LLM Wiki/raw source substrate, operator-boundary enforcement | Work crosses projects or decisions must persist |

## Codex Goals

Codex Goals are executable `/goal` prompts. They are the OS unit of work.

Required content:

- Goal summary.
- Target files or domain.
- Non-goals.
- Validation commands.
- Stopping condition.
- Required docs to update.

Policy:

- One Codex Goal should complete in one session whenever practical.
- Long goals must create a GSD phase plan before implementation.
- Every Codex Goal writes progress and decisions before closure.

## AGENTS.md

`AGENTS.md` is the compact operating law. It should:

- Point to this planning package.
- Preserve GStack -> GSD -> Superpowers separation.
- State primary-source research rules.
- List validation expectations.
- Avoid absorbing all deep docs into the prompt context.

Deep process detail belongs in `docs/`.

## Skills

Skills are reusable, versioned workflows loaded on demand. Use a Skill when:

- The procedure has run successfully at least three times.
- Inputs, outputs, and validation are stable.
- The workflow benefits from scripts, templates, examples, or references.
- An eval/checklist can detect regression.

Promotion criteria:

1. Three successful runs are recorded in `docs/PROGRESS_LOG.md` or a dedicated report.
2. The workflow has an owner, trigger conditions, and non-goals.
3. The Memory Librarian writes a promotion proposal.
4. Security confirms no secrets, unsafe writes, or excessive permissions are bundled.
5. Eval confirms the skill still works from a cold start.

Primary source: Agent Skills describes skills as folders with `SKILL.md`, metadata, instructions, and optional scripts/references/templates, loaded through progressive disclosure: https://agentskills.io/

## MCP

MCP is the typed integration layer for resources, prompts, tools, and workflows.

Use MCP when:

- The agent needs structured access to external data or tools.
- A server can expose resources, prompts, or tools with schemas and permission boundaries.
- The integration should be reusable across agents.

Rules:

- Resources are context, not authority.
- Prompts are user-controlled reusable templates.
- Tools are model-controlled actions and require stronger permission review.
- Every MCP server gets a trust tier, allowed operations, and owner.
- Tool schemas must be validated before use.

Primary sources:

- MCP intro: https://modelcontextprotocol.io/docs/getting-started/intro
- MCP resources: https://modelcontextprotocol.io/specification/2025-06-18/server/resources
- MCP prompts: https://modelcontextprotocol.io/specification/2025-06-18/server/prompts
- MCP tools: https://modelcontextprotocol.io/specification/2024-11-05/server/tools

## Subagents

Subagents are used only for independent work that can run without shared mutable state.

Use subagents for:

- Independent research questions.
- Disjoint code/doc slices.
- Parallel verification on a stable artifact.

Do not use subagents for:

- The immediate blocker on the critical path.
- Shared write targets without ownership.
- Work that requires hidden authority or ambiguous approval.

Subagent handoff must include:

- Role.
- Scope.
- Files/modules owned.
- Inputs already read.
- Output expected.
- Validation expected.
- Explicit instruction not to revert others' work.

## Automations

Automations are for stable recurring jobs, not exploratory work.

Promotion criteria:

1. Same manual workflow has succeeded three times.
2. The job is bounded, idempotent, and has a clear schedule.
3. It writes to a reviewable artifact by default.
4. It has a pause/kill condition.
5. Security approves any external calls, writes, spending, messages, or public actions.
6. Owner approves creation.

Suggested initial automation classes:

- Weekly primary-source watch report for selected domains.
- Nightly docs consistency check.
- Weekly eval trend summary.
- Stale goal review.

## Evals

Evals are the feedback loop that decides whether autonomy can expand.

Eval types:

- Static docs checks.
- Unit tests and typecheck.
- Runtime probes.
- Trace grading for agent workflows.
- Security checklists.
- Human adjudication for taste and strategy.

Primary sources:

- OpenAI agent evals: https://developers.openai.com/api/docs/guides/agent-evals
- OpenAI trace grading: https://developers.openai.com/api/docs/guides/trace-grading
- OpenAI Evals repo: https://github.com/openai/evals

MFH/Meta imported eval surfaces:

- Source reconciliation: compare plan, status, cascade log, git state, and memory before treating project state as current.
- Closure reality check: completed/shipped milestones require ledger evidence, not only a plan marker.
- Claim ledger: public/product claims must be tagged as North Star, category, internal substrate, or externally user-validated.
- Operator-boundary audit: technical decisions stay agent-owned and decision-logged; product/taste/irreversible decisions escalate.

## Default Routing

| Situation | Role flow |
| --- | --- |
| New vague idea | Orchestrator -> Researcher -> Architect -> GStack review |
| Large implementation | Orchestrator -> GSD phase plan -> Implementer -> Eval |
| Bug/failure | Orchestrator -> Security if risky -> Implementer under systematic debugging -> Eval |
| Research brief | Researcher -> Architect -> Memory Librarian |
| Skill candidate | Memory Librarian -> Eval -> Security -> Owner approval |
| Automation candidate | Memory Librarian -> Security -> Eval dry run -> Owner approval |
| Completion claim | Eval -> Orchestrator -> progress/decision update |
| Closure or release claim | Eval -> MFH gate -> Security -> Owner approval if irreversible |
| Cross-project learning | Researcher -> Meta raw/wiki/decision update -> Memory Librarian |
