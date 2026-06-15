# Metaforge Agent Workflow

## Repository Orientation

### Repository Purpose

Metaforge is the public Meta/MFH/Orchestra OS product surface in this checkout.
OpenClaude is the local CLI runtime Metaforge currently rides on: terminal UX,
tools, MCP, provider profiles, Claude/Codex routes, local no-provider evidence,
claim-bounded benchmark readiness, and protected-action gates.

OpenClaude runtime is therefore a substrate, not the main public claim. The
durable product claim should center Meta for operating memory, MFH for
evidence-gated closure, and Orchestra for multi-agent routing, critique, review,
and promotion.

### Setup And Verification Commands

- Install dependencies with the existing lockfile, then run `bun run build`.
- Use `bun run typecheck --pretty false` for repo-wide TypeScript verification.
- Use `bun run product:quality` for the full local product-quality gate. If it
  stops at a protected environment boundary, read the generated reports instead
  of turning the blocker into a readiness claim.
- Use `bun run verify:privacy` before any completion, release-adjacent, or
  public-surface claim.

### Repository Structure

- `src/`: OpenClaude CLI, orchestration, provider, tool, UI, and runtime code.
- `scripts/`: deterministic verification, product-quality, trace,
  benchmark-readiness, and release-hygiene harnesses.
- `docs/`: product specs, goal docs, evidence reports, quality gates, and
  claim-boundary records.
- `reports/`: generated JSONL traces, portable evidence, benchmark manifests,
  and local benchmark results.
- `packages/openclaude-vscode/`: scoped VS Code extension surface and local
  extension evidence target.
- `.github/`: PR, security, dependency, and release-adjacent workflow evidence.

### CI And Workflow Evidence

`.github/workflows/pr-checks.yml` is the source-controlled quality signal and
must keep `bun run product:quality` wired without publish/deploy/launch actions.
CodeQL and Dependabot configuration are evidence inputs, not hosted execution
claims unless a real GitHub run is inspected.

## Standing Research Rule

When planning, ideating, reviewing architecture, or choosing implementation
approaches, prefer primary sources: original project repos, official docs,
papers, patents, standards, and validated open-source implementations. Blogs
only as pointers to primary sources.

Blogs only as pointers; do not use summaries as final evidence.

Keep the user's final goal fixed, but improve the path as evidence appears.

## Workflow Stack

This repo can use three workflow systems, but they must stay separated:

- **GStack**: product judgment, architecture challenge, design review, QA
  review, security review, and final spec shaping.
- **GSD**: milestone/phase decomposition, context-rot control, `.planning/`
  state, and large multi-step execution.
- **Superpowers**: TDD, systematic debugging, code review, and
  verification-before-completion inside concrete implementation work.

Do not let one layer swallow the others. GStack defines judgment, GSD tracks
phases, and Superpowers governs implementation discipline.

For public documentation, keep this stack easy to understand. Avoid dumping
private session memory, stale model choices, local machine paths, or
conversation-specific rules into AGENTS.md.

## Verification Standard

Do not claim installation, implementation, or completion from file presence
alone. Verify by running the relevant command, loader check, test, version probe,
or live inspection. Report any unverified part plainly.

Changed-file TypeScript diagnostics should be clean even if broad typecheck
findings are unrelated and already documented. Treat unrelated failures as
out-of-scope only after they are named.

## Public Claim Boundaries

- Public repo polish is not production readiness.
- Workflow badges show configured automation health only.
- Local proof artifacts are not external validation.
- Benchmarks are readiness surfaces only after the benchmark command, input,
  output, and claim boundary are recorded.
- Protected actions, credential changes, public deploys, and destructive
  filesystem operations need explicit authorization.

## Autonomous Goal OS Planning Package

When work concerns Meta, MFH, Orchestra OS, autonomous goals, research loops,
eval loops, or long-running agent execution, treat these docs as operating
source:

- `docs/PROJECT_SPEC.md`
- `docs/MFH_META_SYNTHESIS.md`
- `docs/GOAL_SCHEMA.md`
- `docs/AGENT_REGISTRY.md`
- `docs/RESEARCH_PIPELINE.md`
- `docs/EVALS.md`
- `docs/SECURITY_AND_GUARDRAILS.md`
- `docs/ROADMAP.md`
- `docs/DECISION_LOG.md`
- `docs/PROGRESS_LOG.md`
- `docs/NEXT_GOALS.md`

The goal hierarchy is:

North Star Goal -> Program Goals -> Sprint Goals -> Codex Goals -> Atomic Tasks.

Codex goals must include success criteria, non-goals, validation commands,
checkpoints, pause conditions, rollback strategy, research requirements, claim
boundaries, and MFH/Meta gate requirements before implementation begins.

## Public Readiness Backlog

Community feedback is tracked in:

- `docs/product-quality/public-feedback-snapshot-2026-06-15.md`
- `docs/product-quality/public-feedback-triage-2026-06-15.md`

Keep this public AGENTS.md concise: no private memory dumps, local paths, stale
model locks, raw runtime logs, or internal-only rule transcripts. Stronger
marketing waits for behavioral happy-path, edge-case, and side-effect evidence.
