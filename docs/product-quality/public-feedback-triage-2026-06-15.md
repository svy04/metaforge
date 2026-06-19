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
- Use the checked Knip candidate gate, dependency-cruiser topology gate, and
  jscpd duplicate-shape audit before broad refactors.
- Upgrade the weakest product-quality gates from marker presence to behavioral
  happy-path, edge-case, and side-effect checks.
- Keep Korean documentation maintained alongside the English README when the
  audience is Korean.

Boundary: this triage proves the current public-surface checks passed locally.
It does not prove production readiness, external validation, release readiness,
or autonomous reliability.

## Community Feedback Snapshot

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
- Recommended static-analysis lanes: the checked Knip candidate gate for dead
  exports, dependency-cruiser for cycles/topology, jscpd for duplicate shapes,
  and Lumin Repo Lens as a topology reference with manual false-positive
  review.
- CodeQL being present in CI is a positive signal, but source-controlled
  configuration is not the same as inspected hosted execution evidence.
- Later comments also recommended simplifying public workflow language where
  possible: GStack, GSD, and Superpowers may remain separated internally, but
  public docs should avoid making the operating stack look like rule sprawl.
- The latest security/refactor response lane is to start with P0 CodeQL alerts
  and tiny TDD-backed fixes, then use hosted CodeQL feedback before claiming an
  alert class is closed.

## 2026-06-16 Follow-Up Response

The next community-feedback response slice converts two marker-only risks into
fixture-backed gates:

- `product-agent-instructions-quality` is now import-safe and exposes a pure
  analyzer so AGENTS.md hygiene can be tested without rewriting repository
  evidence.
- `--check` mode for that gate no longer writes
  `agent-instructions-quality-report.json` or `.md`.
- The verification-standard check now requires marker text inside the real
  `## Verification Standard` section, not unrelated prose or fenced examples.
- `product-public-claim-boundary` now scans `docs/goals/*.md` and treats
  `status: PROVEN`, `*_READY`, completion-candidate, and beta-candidate wording
  as goal-artifact status language.
- Older goal artifacts with strong local status language now state a historical
  repo-local boundary at the top of the file, so local completion evidence is
  not read as production, release, public-readiness, or external-validation
  proof.

Current response in this slice:

- add a fixture-based regression test proving `public-artifact-hygiene` rejects
  private Codex memory directory placeholders, private agent skill directory
  placeholders, raw private memory headings, and pasted local agent-instruction
  headers;
- remove tracked generated AVF local-run artifacts from the public checkout,
  add a path-portability regression test for tracked files over 240 characters,
  and keep `operator_package_v*` outputs ignored as local review artifacts;
- extract tiny shared helper surfaces from community/public and origin/license
  quality scripts;
- wire `bun run product:script-duplication-audit` into `product:quality`;
- add duplicate-helper baseline caps so future clone growth fails locally;
- make public setup docs avoid stale model pins such as old hardcoded OpenAI or
  local Ollama example model names;
- keep the proof boundary explicit: this is public hygiene and regression
  prevention, not production readiness or external validation.

## 2026-06-18 Goal Kernel Trace-Policy Response

The next response slice moves the Goal Kernel from schema-only evidence toward
behavioral closure evidence:

- `scripts/validate-goals.ts` now rejects future `validated` or `closed` goals
  when required validation commands lack passing `evidence.testResults`.
- `scripts/validate-goals.ts` now checks `evidence.artifacts` paths, so closure
  cannot rest only on named but missing files.
- `scripts/validate-goal-traces.ts` validates source-controlled goal traces for
  `goal.loaded -> checkpoint.completed -> validation.ran -> claim.reviewed ->
  goal.validated` ordering.
- `docs/goals/traces/CG-001-goal-kernel-mvp.trace.json` is the first local
  no-provider Goal Kernel trace fixture.
- `docs/product-quality/goal-trace-validation-report.md` records the trace
  result, source patterns, side-effect arrays, and claim boundary.
- README and README.ko now expose a short `Metaforge Proof Tour` that centers
  Meta/MFH/Orchestra and leaves OpenClaude as runtime substrate.

Blocked context: this is still local no-provider evidence and does not prove production readiness, hosted deployment, external validation, benchmark superiority, or autonomous reliability.

## 2026-06-18 Response: Product Evidence Reframing

The restated feedback packet is now treated as an active backlog input,
not a one-time launch reaction. This response slice keeps the raw thread out of
public docs while preserving the concrete work:

- keep feedback docs as summarized evidence, not raw comment archives;
- keep OpenClaude framed as runtime substrate while Metaforge carries the
  Meta/MFH/Orchestra thesis;
- add regression coverage so product-quality evidence docs cannot drift back to
  OpenClaude-as-product wording;
- preserve the recommended analysis stack, including Knip/fallow,
  dependency-cruiser, jscpd, and manual topology review;
- continue moving weak marker/file-existence checks toward behavioral happy
  paths, edge cases, and side-effect guards;
- keep Korean docs current when public readers are Korean.

Blocked context: this response is public-surface hygiene and local no-provider
evidence alignment. It does not prove production readiness, hosted deployment,
external validation, benchmark superiority, legal clearance, or autonomous
reliability.
