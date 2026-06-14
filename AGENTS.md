# Metaforge Agent Workflow

## Repository Orientation

### Repository Purpose

Metaforge is a local-first operating system for governed agent execution.
The product center is **Meta + MFH + Orchestra OS**:

- **Meta**: operator constitution, durable memory, decision records, and claim boundaries.
- **MFH**: governed-code operating gate for validation, closure evidence, and promotion control.
- **Orchestra OS**: multi-agent planning, dissent, shadow work, review, and human promotion loops.
- **OpenClaude runtime**: the host adapter/substrate that exposes Claude, Codex, OAuth, tools, and local CLI routes.

Do not frame OpenClaude as the primary product. It is the runtime layer that carries the Meta/MFH/Orchestra system.

## Setup And Verification

- Install dependencies with the package manager lockfile already in the repository.
- Use `bun run build` for the CLI bundle.
- Use `bun run typecheck --pretty false` for repo-wide TypeScript verification.
- Use `bun run product:quality` for the full local product-quality gate.
- Use `bun run verify:privacy` before public-release or release-adjacent claims.

If a command stops at a protected environment boundary, read the generated product-quality reports and report the boundary plainly. Do not convert a boundary into a readiness claim.

## Repository Structure

- `src/`: runtime, orchestration, provider, tool, UI, and CLI code.
- `scripts/`: deterministic local verification, product-quality, trace, benchmark-readiness, and release-hygiene harnesses.
- `docs/`: product specs, goal-system docs, evidence reports, quality gates, and claim-boundary records.
- `reports/`: generated portable evidence and local benchmark artifacts. Do not commit raw private traces.
- `packages/openclaude-vscode/`: scoped VS Code extension surface and local extension evidence target.
- `.github/`: source-controlled PR, security, dependency, and release-adjacent workflow evidence.

## Standing Research Rule

When planning, ideating, reviewing architecture, or choosing implementation approaches, prefer primary sources:

- original project repositories
- official documentation
- papers
- patents
- standards
- validated open-source implementations

Use blogs only as pointers to original sources. Keep the user's final goal fixed, but improve the path as evidence appears.

## Agent Stack

Use three complementary workflow systems without collapsing their roles:

- **GStack**: ideation, product judgment, architecture challenge, design review, QA review, security review, and final spec shaping.
- **GSD**: phase decomposition, context-rot control, long-running implementation plans, `.planning/` state, and large multi-step execution.
- **Superpowers**: TDD, systematic debugging, code review, subagent-driven development, and verification before completion.

Routing:

1. Rough ideas, product decisions, unclear scope: start with GStack.
2. Large implementation work: feed the approved GStack/spec output into GSD.
3. Concrete coding, debugging, and verification: use Superpowers.

Conflict resolution:

1. GStack defines the spec and high-level judgment.
2. GSD turns the spec into phases and keeps state fresh.
3. Superpowers governs implementation discipline inside each concrete task.

## Autonomous Goal OS Source Package

When work concerns Meta, MFH, Orchestra OS, autonomous goals, research loops, eval loops, or long-running agent execution, treat the planning package in `docs/` as the operating source:

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

`North Star Goal -> Program Goals -> Sprint Goals -> Codex Goals -> Atomic Tasks`

Codex goal work must include success criteria, non-goals, validation commands, checkpoints, pause conditions, rollback strategy, research requirements, claim boundaries, and MFH/Meta gate requirements before implementation begins.

## Verification Standard

Do not claim installation, implementation, release readiness, production readiness, autonomous reliability, or external validation from file presence alone.

Require at least one relevant executed command, loader check, test, version probe, or generated evidence report. When verification is partial, say exactly what was and was not verified.

Verify by running the relevant command, not by checking file presence.

## Public Hygiene

Do not commit:

- local absolute paths
- private workspace names
- raw terminal transcripts
- raw model traces
- access tokens
- API keys
- OAuth material
- generated session logs
- machine-specific plugin paths

Use placeholders such as `<workspace>`, `<repo>`, `<config-dir>`, and `<private-harness-root>` in public docs.

Generated local probes belong outside Git or in ignored files. If a trace is needed as evidence, commit a redacted summary with command, date, result, and claim boundary instead of the raw transcript.
