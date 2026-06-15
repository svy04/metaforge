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

## Remaining Work

The feedback still identifies real follow-up work:

- Run a dedicated duplicate-helper audit over `scripts/product-*.ts`.
- Evaluate Knip or Fallow for dead exports, dependency-cruiser for cycles, and
  jscpd for duplicate shapes before broad refactors.
- Upgrade the weakest product-quality gates from marker presence to behavioral
  happy-path, edge-case, and side-effect checks.
- Keep Korean documentation maintained alongside the English README when the
  audience is Korean.

Boundary: this triage proves the current public-surface checks passed locally.
It does not prove production readiness, external validation, release readiness,
or autonomous reliability.
