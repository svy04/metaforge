# Metaforge Agent Workflow

## Repository Orientation

### Repository Purpose

Metaforge is the public Meta/MFH/Orchestra OS surface in this checkout.
OpenClaude runtime is the local CLI substrate Metaforge currently rides on:
terminal UX, tools, MCP, provider profiles, Claude/Codex routes, local
no-provider evidence, benchmark-readiness boundaries, and protected-action
gates.

The durable public claim centers:

- **Meta**: operating memory and state.
- **MFH**: evidence-gated closure.
- **Orchestra**: multi-agent routing, critique, review, and promotion.

OpenClaude is useful runtime infrastructure, not the main public thesis.

## Verification Commands

- Install with the existing lockfile, then run `bun run build`.
- Use `bun run typecheck --pretty false` for repo-wide TypeScript checks.
- Use `bun run product:quality` for the full local product-quality gate.
- Use `bun run verify:privacy` before completion, release-adjacent, or
  public-surface claims.

If a gate reaches a protected environment boundary, read the generated report
and keep the boundary explicit instead of turning it into a readiness claim.

## Repository Map

`src/` holds runtime code; `scripts/` holds deterministic gates; `docs/` and
`reports/` hold evidence and claim boundaries; `packages/openclaude-vscode/`
holds the scoped extension surface; `.github/` holds workflow evidence.

## CI Evidence

`.github/workflows/pr-checks.yml` is the source-controlled quality signal and
keeps `bun run product:quality` wired without publish, deploy, or launch
actions. CodeQL and Dependabot configuration are evidence inputs, not hosted
execution claims unless a real GitHub run is inspected.

## Research Rule

For planning, architecture, and implementation choices, prefer primary sources:
original project repos, official docs, papers, patents, standards, and
maintained open-source implementations. Blogs only as pointers; they are routing
aids, not final evidence. Keep the final goal fixed while improving the route as
evidence appears.

## Workflow Stack

Use the stack as compact operating boundaries, not a rule pile:

- **GStack**: product, architecture, design, QA, and security judgment.
- **GSD**: phases, checkpoints, and long-running execution state.
- **Superpowers**: TDD, debugging, code review, and verification discipline.

Keep detailed role contracts in `docs/AGENT_REGISTRY.md`.

## Verification Standard

Do not claim installation, implementation, or completion from file presence
alone. Verify by running the relevant command, loader check, test, version
probe, live inspection, or current GitHub run.

Changed-file TypeScript diagnostics should be clean even if unrelated broad
typecheck findings are documented elsewhere. Name unrelated failures before
treating them as out of scope.

## Public Claim Boundaries

- Public repo polish is not production readiness.
- Workflow badges show configured automation health only.
- Local proof artifacts are not external validation.
- Benchmarks need command, input, output, and claim-boundary evidence before
  public readiness wording.
- Do not describe the OpenClaude CLI substrate as fully original, blanket MIT,
  or redistribution-cleared; route origin/license questions to `README.md` and `LICENSE`.
- Protected actions, credential changes, public deploys, and destructive
  filesystem operations require explicit authorization.

## Autonomous Goal OS Docs

When work concerns Meta, MFH, Orchestra OS, autonomous goals, research loops,
eval loops, or long-running agent execution, treat the main operating docs as
source: `docs/PROJECT_SPEC.md`, `docs/MFH_META_SYNTHESIS.md`,
`docs/GOAL_SCHEMA.md`, `docs/AGENT_REGISTRY.md`,
`docs/RESEARCH_PIPELINE.md`, `docs/EVALS.md`,
`docs/SECURITY_AND_GUARDRAILS.md`, `docs/ROADMAP.md`,
`docs/DECISION_LOG.md`, `docs/PROGRESS_LOG.md`, and `docs/NEXT_GOALS.md`.

Use this hierarchy: North Star Goal -> Program Goals -> Sprint Goals -> Codex
Goals -> Atomic Tasks.

## Public Feedback Backlog

Community feedback is tracked in:

- `docs/product-quality/public-feedback-snapshot-2026-06-15.md`
- `docs/product-quality/public-feedback-triage-2026-06-15.md`
- `docs/product-quality/public-feedback-snapshot-2026-06-19.md`
- `docs/product-quality/public-feedback-triage-2026-06-19.md`

Keep this public AGENTS.md concise: no private memory dumps, local paths, stale
model locks, raw runtime logs, or internal-only rule transcripts. Stronger
marketing waits for behavioral happy-path, edge-case, and side-effect evidence.
