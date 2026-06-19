# Public Feedback Snapshot - 2026-06-19

Status: public-safe feedback preservation, local/no-provider record only.

The owner supplied another Korean community-feedback packet and asked that it be
saved before continuing. This document preserves durable product signals rather
than copying a raw comment thread, public handles, casual chat, or local/private
machine details back into the repository.

## Durable Feedback Signals

1. Provenance is a trust surface.
   - Commit/star history questions and fork/adaptation questions should be
     answered plainly.
   - Public copy should distinguish original Metaforge work from adapted CLI
     substrate work and avoid implying that the CLI substrate is fully original.

2. The product thesis is Metaforge, not OpenClaude alone.
   - Metaforge should remain framed as Meta + MFH + Orchestra OS.
   - OpenClaude should remain the runtime substrate for terminal UX, tools,
     MCP, provider routes, Claude/Codex routes, and local evidence.

3. Public AGENTS.md and README surfaces must stay distribution-safe.
   - Avoid local folder names, private memory dumps, stale model locks, raw
     runtime traces, copied agent-instruction headers, OAuth-looking material,
     and rule sprawl.
   - Public workflow wording should stay concise enough that readers can judge
     the architecture rather than the private operating ritual.

4. Marker-only audits are not strong enough for stronger claims.
   - File existence, string checks, missing forbidden markers, and hardcoded
     flags are useful scaffolding but weak proof.
   - The next evidence should prioritize behavioral happy paths, edge cases,
     and side-effect guards, especially around MFH closure.

5. Wiring evidence matters.
   - Metaforge, AVF, influence-factory, Mimesis, GStack, GSD, and Superpowers
     language should not imply runtime-active modules without imports, runtime
     traces, tests, or source-controlled reports.

6. Static-analysis recommendations remain backlog inputs.
   - Use Knip or fallow for unused/dead exports.
   - Use dependency-cruiser for cycles and topology.
   - Use jscpd for duplicate shapes.
   - Use topology tools such as `annyeong844/lumin-repo-lens` as heuristic
     review inputs with manual false-positive triage.
   - Keep CodeQL as a positive but bounded configured-analysis signal unless a
     current hosted run is inspected.

7. Korean documentation should stay current.
   - The first public feedback audience is Korean, so public explanation should
     not be English-only when key product framing changes.

## Current Response

This slice records the feedback as a new dated snapshot, updates the public
feedback backlog pointer, and binds MFH public claim evidence directly to the
source-controlled three-file Goal Kernel trace pack and goal-trace validation
report. The pack covers one validated happy path, one rejected missing-evidence
edge case, and one blocked protected-action side-effect case.

Boundary: this snapshot and response are local no-provider product input and
public hygiene evidence. They are not production readiness, hosted workflow
proof, external validation, benchmark superiority, or legal clearance.
Autonomous reliability claims remain blocked.
