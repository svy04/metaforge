# Public Feedback Triage - 2026-06-15

Status: local no-provider triage, not an external validation claim.

This note records a public-surface review pass after community feedback called
out three trust risks:

1. AGENTS.md can look like a private memory dump if it exposes local paths,
   stale model locks, duplicate rules, or personal workflow traces.
2. Public README copy should center Metaforge as Meta + MFH + Orchestra OS,
   with OpenClaude framed as the CLI/runtime substrate rather than the thesis.
3. Current evidence gates must keep moving beyond file-existence and
   marker-only checks toward behavioral happy paths, edge cases, and
   side-effect checks.

## Current Verification

Commands run on 2026-06-15:

```bash
bun run product:agent-instructions-quality
bun run product:public-artifact-hygiene
bun run product:public-repo-readiness
bun run verify:privacy
bun run product:community-intake-quality
git grep -n -E "<local-user-path-pattern>|<private-korean-local-path>|<stale-model-lock-pattern>" -- AGENTS.md README.md README.ko.md
```

Observed result:

- `product:agent-instructions-quality` passed.
- `product:public-artifact-hygiene` passed in check mode over 431 files with
  `files_changed=0`.
- `product:public-repo-readiness` passed 5/5 tests.
- `verify:privacy` passed no-phone-home, public artifact hygiene, and public
  repo readiness checks.
- `product:community-intake-quality` passed.
- The targeted public-surface grep returned no matches for local user paths,
  stale model-lock wording, or the private Korean local path.

## Decision

No AGENTS.md rewrite is required in this slice. The current AGENTS.md is already
public-facing and concise enough for the existing gate:

- repository purpose is explicit
- setup and verification commands are explicit
- GStack, GSD, and Superpowers boundaries remain separated
- primary-source research and verification-before-claim rules remain explicit
- private memory dumps, stale public model-lock lines, and local user paths are
  absent

## Follow-Up Audit Added

The duplicate-helper concern now has a local no-provider audit command:

```bash
bun run product:script-duplication-audit
```

The report lives in `docs/product-quality/script-duplication-audit-report.md`
and `docs/product-quality/script-duplication-audit-report.json`. It records
refactor candidates only; it does not claim that helper duplication has been
removed.

## Remaining Work

The feedback still identifies real follow-up work:

- Use the duplicate-helper audit to extract the smallest safe shared helper
  cluster, starting with the community/public hygiene scripts.
- Evaluate Knip or Fallow for dead exports, dependency-cruiser for cycles, and
  jscpd for duplicate shapes before broad refactors.
- Upgrade the weakest product-quality gates from marker presence to behavioral
  happy-path, edge-case, and side-effect checks.
- Keep Korean documentation maintained alongside the English README when the
  audience is Korean.

Boundary: this triage proves the current public-surface checks passed locally.
It does not prove production readiness, external validation, release readiness,
or autonomous reliability.

## Owner-Provided Community Feedback Snapshot

Additional public-community feedback was recorded on 2026-06-15 as follow-up
product input. The raw comment thread is not copied verbatim into the public
quality docs; the durable signals are:

- Provenance and trust need clearer handling: the repo should say plainly when
  the CLI surface is forked/adapted and should not imply a fully original CLI
  implementation.
- AGENTS.md must stay public-facing: no local folder names, stale model locks,
  duplicate private rules, or internal memory traces.
- Public marketing should center Metaforge as Meta + MFH + Orchestra OS, with
  OpenClaude described as a runtime substrate.
- The audit workflow is directionally strong, but file-existence, marker, and
  hardcoded-flag checks need behavioral happy-path, edge-case, and side-effect
  tests before stronger public claims.
- Product-quality scripts show clone pressure; repeated `check`, `readText`,
  hashing, and markdown/report helpers should be extracted in small verified
  slices rather than by broad mechanical rewrite.
- Metaforge, AVF, and influence-factory surfaces need wiring evidence before
  they are marketed as active modules.
- Recommended static-analysis lanes: Knip or Fallow for dead exports,
  dependency-cruiser for cycles/topology, jscpd for duplicate shapes, and
  Lumin Repo Lens as a topology reference with manual false-positive review.
- CodeQL being present in CI is a positive signal, but source-controlled
  configuration is not the same as inspected hosted execution evidence.

Current response in this slice: extract one tiny shared helper surface from the
community/public quality scripts, re-run the affected scripts, and refresh the
duplication audit report so the feedback turns into measured code movement.
