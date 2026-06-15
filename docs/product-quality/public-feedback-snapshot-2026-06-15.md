# Public Feedback Snapshot - 2026-06-15

Status: public-safe feedback preservation, local/no-provider record only.

This snapshot preserves the product signals from community feedback received
after Metaforge/OpenClaude was made public. It is intentionally not a verbatim
comment dump: public handles, casual chat, and private/local path details are
omitted or generalized so the repository does not reintroduce the trust risks
that the feedback identified.

## Durable Feedback Signals

1. Provenance should be explicit.
   - The CLI surface should not be marketed as fully original if it is forked,
     adapted, or derived from another CLI.
   - Origin and license boundaries need a plain public explanation before
     heavier marketing.

2. Public AGENTS.md must stay distribution-safe.
   - Avoid private memory dumps, local machine paths, stale model locks,
     duplicated personal workflow rules, and internal-only execution traces.
   - Keep the public file as concise operating guidance; move deeper product
     evidence and process records into `docs/`.

3. The main story is Metaforge, not OpenClaude alone.
   - Metaforge should be framed as Meta + MFH + Orchestra OS.
   - OpenClaude should be described as the local CLI/runtime substrate under
     that operating system.

4. Marker-only audits are not enough.
   - Existing product-quality scripts prove structure and hygiene, but stronger
     public claims require behavioral happy paths, edge cases, and side-effect
     guards.
   - File existence, marker strings, missing forbidden markers, and hardcoded
     false flags should not be mistaken for real runtime proof.

5. Product scripts show clone pressure.
   - Repeated helpers such as `check`, `readText`, hashing helpers, and report
     writers should be extracted in small verified slices.
   - Broad mechanical refactors should be avoided until each slice has focused
     tests and before/after audit evidence.

6. Marketing modules need wiring evidence.
   - Metaforge, AVF, and influence-factory surfaces should not be described as
     active modules unless imports, runtime paths, tests, or proof reports show
     they are actually wired.

7. Recommended analysis lanes.
   - Knip or Fallow for dead exports.
   - dependency-cruiser for circular dependencies and topology rules.
   - jscpd for duplicate code shapes.
   - Lumin Repo Lens as a community reference for topology and clone cues, with
     manual false-positive review.

8. Existing positives should be kept proof-bounded.
   - CodeQL configuration in CI is a useful source-controlled security signal.
   - Source-controlled configuration is not the same as inspected hosted
     execution evidence.

## Current Response

The first response slice extracts a tiny shared helper surface from
community/public product-quality scripts and refreshes the local duplication
audit report. This converts the clone-pressure feedback into measured code
movement without claiming that all duplication, dead exports, or wiring gaps are
resolved.

Boundary: this snapshot is not production readiness, release readiness,
external validation, hosted workflow proof, or autonomous reliability evidence.
