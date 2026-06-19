# Metaforge Architecture Map

Generated-by-hand from checked-in local evidence, not from live provider calls.

## Claim Boundary

- This is a public architecture visualization for Metaforge = Meta + MFH + Orchestra OS over the OpenClaude runtime substrate.
- It is derived from current docs, tests, and product-quality reports.
- It is not clean-architecture proof, not production readiness, not external validation, not topology cleanup, and not refactor completion.

## Source Evidence

| Evidence | Current role |
| --- | --- |
| `README.md` and `README.ko.md` | Public thesis, runtime substrate wording, origin/license boundary |
| `docs/PROJECT_SPEC.md` | North Star, operating loop, goal hierarchy |
| `docs/MFH_META_SYNTHESIS.md` | Meta/MFH import boundary and unresolved alias guard |
| `docs/AGENT_REGISTRY.md` | Agent role and Orchestra routing surface |
| `docs/RESEARCH_PIPELINE.md` | Source-first Mimesis loop |
| `docs/EVALS.md` | Eval and trace-grading boundary |
| `docs/SECURITY_AND_GUARDRAILS.md` | Permission, protected action, and safety controls |
| `docs/product-quality/public-claim-boundary-report.md` | Public claim evidence map and non-claims |
| `docs/product-quality/dependency-topology-report.md` | dependency-cruiser topology baseline and known-violation ratchet |
| `docs/product-quality/script-duplication-audit-report.md` | jscpd duplicate-shape ratchet |
| `docs/product-quality/dead-export-candidates-report.md` | Knip dead-export candidate inventory |
| `src/services/orchestra/` | runtime-wired import path for Orchestra surfaces |

## Operating Stack

```mermaid
flowchart TD
  Owner["Human owner"]
  Meta["Meta\noperating memory, source ledgers, decisions"]
  GoalKernel["Goal Kernel\ngoals, success criteria, rollback rules"]
  MFH["MFH\nevidence gate, drift check, claim boundary"]
  Orchestra["Orchestra\nplanner, skeptic, reviewer, arbiter, promotion"]
  Runtime["OpenClaude runtime substrate\nterminal UX, tools, MCP, provider routes"]
  Providers["Claude and Codex OAuth routes\nOpenAI-compatible, Gemini, Ollama, local routes"]
  Mimesis["Mimesis Engineering\nsource-first absorption loop"]
  Reports["Product-quality reports\ntraces, topology, clones, privacy, claims"]
  AVF["AVF Influence Factory\nmanual artifact lane"]

  Owner --> GoalKernel
  Meta --> GoalKernel
  Mimesis --> Meta
  Mimesis --> GoalKernel
  GoalKernel --> Orchestra
  Orchestra --> Runtime
  Runtime --> Providers
  Orchestra --> Reports
  Reports --> MFH
  MFH --> GoalKernel
  MFH --> Owner
  AVF -. "manual artifacts only" .-> Reports
```

## Evidence Closure Loop

```mermaid
flowchart TD
  Intent["Owner intent"]
  Contract["Goal contract\nscope, non-goals, validation commands"]
  Research["Primary-source research\nOSS, docs, papers, patents, standards"]
  Work["Implementation or documentation change"]
  Validation["Validation commands\nbuild, tests, product-quality gates"]
  Evidence["Evidence artifacts\nreports, traces, manifests, proof packs"]
  ClaimGate["MFH claim gate\nallowed claims and explicit non-claims"]
  PublicSurface["Public surface\nREADME, Korean README, profile, proof pack"]
  NextGoals["Next goals\nroadmap, progress, decision log"]

  Intent --> Contract
  Contract --> Research
  Research --> Work
  Work --> Validation
  Validation --> Evidence
  Evidence --> ClaimGate
  ClaimGate --> PublicSurface
  ClaimGate --> NextGoals
  NextGoals --> Contract
```

## Static Analysis Trust Stack

```mermaid
flowchart TD
  Knip["Knip\ndead-export candidates"]
  DepCruiser["dependency-cruiser\ndependency topology ratchet"]
  Jscpd["jscpd\nduplicate-shape ratchet"]
  CG002["CG-002 static-analysis goal"]
  Manifest["Product evidence manifest"]
  PublicClaim["Public claim boundary report"]
  CandidateBoundary["Candidate/baseline/ratchet only\nnot cleanup, topology-clean, refactor-completion, public-readiness, or external-validation proof"]

  Knip --> CG002
  DepCruiser --> CG002
  Jscpd --> CG002
  CG002 --> Manifest
  Manifest --> PublicClaim
  PublicClaim --> CandidateBoundary
```

Current static-analysis counters from checked-in product-quality reports:

### Knip dead-export candidate lane

Source: `docs/product-quality/dead-export-candidates-report.md`

- candidate_file_count: `637`
- candidate_unused_export_count: `1396`
- candidate_unused_type_count: `364`
- candidate_duplicate_export_count: `12`
- triage_record_count: `4`
- deletion_claim_allowed: `false`
- cleanup_completion_claim_allowed: `false`
- public_readiness_claim_allowed: `false`

### dependency-cruiser topology lane

Source: `docs/product-quality/dependency-topology-report.md`

- module_count: `2630`
- dependency_edge_count: `11984`
- circular_dependency_baseline: `1737`
- unresolved_dependency_baseline: `863`
- configured_dependency_cruiser_new_violation_count: `0`

### jscpd duplicate-shape lane

Source: `docs/product-quality/script-duplication-audit-report.md`

- jscpd_clone_count: `17`
- jscpd_duplicated_lines: `439`
- jscpd_duplicated_tokens: `2979`
- jscpd_duplicated_percentage: `1.043871121150874`
- public_readiness_claim_allowed: `false`
- refactor_completion_claim_allowed: `false`

Those counters are ratchet evidence. They are not clean-architecture proof and they do not prove public readiness.

## Primary Source Method

- Mermaid flowcharts are used because Mermaid supports text-defined flowcharts in Markdown-friendly syntax: https://mermaid.js.org/syntax/flowchart.html
- dependency-cruiser is already the local topology source and supports graph-oriented dependency reporting: https://github.com/sverweij/dependency-cruiser
- jscpd is already the local duplicate-shape source: https://github.com/kucherenko/jscpd
- The C4 model's useful constraint here is map-like communication at different abstraction levels, not a claim that this repo has a complete C4 model: https://c4model.com/introduction

## Reading Rule

Treat this page as a navigation map. The evidence lives in the linked reports, tests, scripts, and docs. If this map conflicts with a current generated report, the generated report wins until this map is updated.
