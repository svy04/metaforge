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
   - Checked Knip candidate gate for dead exports.
   - dependency-cruiser for circular dependencies and topology rules.
   - jscpd for duplicate code shapes.
   - Lumin Repo Lens as a community reference for topology and clone cues, with
     manual false-positive review.

8. Existing positives should be kept proof-bounded.
   - CodeQL configuration in CI is a useful source-controlled security signal.
   - Source-controlled configuration is not the same as inspected hosted
     execution evidence.

## Current Response

The first response slice extracts tiny shared helper surfaces from
community/public and origin/license product-quality scripts, refreshes the local
duplication audit report, and wires the audit into `product:quality` as a
ratchet. Future helper-clone increases above the current baseline now fail the
local gate, and a checked Knip candidate gate records dead-export/type/duplicate
export candidates without autofix or deletion claims. Public setup docs also
avoid pinning stale OpenAI model examples. This converts the clone-pressure,
dead-export, and stale-public-doc feedback into measured code movement without
claiming that all duplication, dead exports, or wiring gaps are resolved.

Boundary: this snapshot is not production readiness, release readiness,
external validation, hosted workflow proof, or autonomous reliability evidence.

## Late Follow-Up Signals

An additional community thread on 2026-06-15 reinforced the same
public-readiness priorities and added two sharper trust signals:

- Early readers check commit/star history and provenance before trying the
  tool; the public surface should explain the private-to-public transition
  without implying a fully original CLI implementation.
- The OpenClaude/Codex/Claude Code comparison should not become the product
  thesis. Public copy should make clear that OpenClaude is the runtime
  substrate, while the differentiating work is Meta, MFH, Orchestra, and the
  drift/improvement loop above the CLI.
- Claude Code-derived ancestry remains a legal/provenance risk that needs
  explicit review before stronger promotion. If the substrate risk becomes too
  high, evaluate a cleaner open CLI substrate rather than over-marketing the
  fork.
- Reviewers again flagged AGENTS.md/local-path hygiene, dead-code-like
  Metaforge or AVF wiring, marker-only audits, duplicate product scripts, and
  the need to keep Korean docs current.
- The positive signal remains the workflow shape: generate evidence, verify it,
  record versions, and keep CodeQL in CI. The next work should turn that shape
  into behavioral tests and smaller security/refactor patches.

## Third-Wave Follow-Up Signals

A later community thread on 2026-06-16 sharpened the same
feedback into two immediate hardening requirements:

- AGENTS.md quality gates should not pass because required words appear
  somewhere in the file. Repository purpose and verification standards need
  structure-aware checks, and `--check` mode should not rewrite generated
  evidence.
- Public `docs/goals/*.md` artifacts carry strong local status language such as
  `status: PROVEN` and `*_READY`. Those artifacts need explicit top-of-file
  repo-local/historical boundaries before they are included in public claim
  boundary scans.

Current response in this slice: `product-agent-instructions-quality` now has a
fixture-tested analyzer, import-safe entrypoint, and no-write `--check` mode.
`product-public-claim-boundary` now includes `docs/goals/*.md` and classifies
goal-artifact status language as blocked only when a same-file top boundary is
present. Older goal artifacts with strong local status language now carry an
explicit historical local artifact boundary.

## 2026-06-18 Restated Feedback Packet

The same community thread was restated as an active operating input. The durable
signal remains stronger than the casual language of the thread:

- The private-to-public transition needs a plain provenance story. Commit/star
  history questions are trust questions, so public copy should distinguish
  original Metaforge work from adapted CLI substrate work.
- OpenClaude should remain OpenClaude runtime substrate. The product thesis is
  Metaforge as Meta + MFH + Orchestra OS, especially Meta/MFH/drift evidence and
  Orchestra routing/review/promotion.
- Public AGENTS.md and README surfaces must not expose local folder names,
  stale model locks, private memory text, pasted agent-instruction dumps, or raw
  runtime traces.
- Marker-only audits are useful scaffolding but weak proof. The next stronger
  evidence should prioritize behavioral happy paths, edge cases, and side-effect
  guards.
- Static-analysis recommendations are preserved as backlog inputs: Knip or
  fallow for unused exports, dependency-cruiser for cycles/topology, jscpd for
  duplicate shapes, and topology tools with manual false-positive review.
- Metaforge, AVF, influence-factory, and Mimesis surfaces should not be marketed
  as runtime-active modules without import paths, runtime traces, tests, or
  source-controlled proof reports.
- Korean docs should stay current because early public feedback arrived from a
  Korean audience.

Boundary: this restated feedback is product input and local no-provider public
hygiene evidence. It is not production readiness, hosted workflow proof,
external validation, benchmark superiority, or legal clearance.
