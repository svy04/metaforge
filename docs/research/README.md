# Research Ledger

Status: active

This directory holds Metaforge research artifacts that are safe to publish and reuse. The operating pattern is:

1. Raw/source layer: preserve primary sources, local authority paths, and rejected-source notes.
2. Wiki/brief layer: synthesize what the sources change for Meta, MFH, Orchestra, Goal OS, evals, and guardrails.
3. Decision layer: record plan-changing choices in `docs/DECISION_LOG.md`.

Research is not a decoration pass. A researched claim can enter public proof copy, roadmap language, or Goal OS requirements only when it is backed by one of:

- local repository evidence;
- official documentation;
- original repositories or maintained source code;
- standards or specifications;
- papers or technical reports;
- patent database search routes;
- a validation method;
- a decision-log assumption.

Blog posts, search snippets, community comments, and marketing summaries may route discovery, but they are not final evidence. Private internal notes may inform planning, but they are not public proof paths.

## Current Briefs

- `goal-os-governed-code-prior-art-2026-06-18.md` maps Goal OS governed-code prior art to the local Meta/MFH/Orchestra operating system.
- `mimesis-engineering-source-ledger-2026-06-14.md` records the broader source-first improvement loop.
- `public-proof-pack-source-ledger-2026-06-18.md` records the current public-proof and claim-boundary source absorption.
- `public-proof-pack-source-ledger-2026-06-14.md` records the historical baseline public-proof source absorption.

## Validation

Run:

```powershell
bun run research:validate
```

The validator checks `goal-os-*.md` briefs for required sections, required local and external primary-source anchors, source-to-requirement/eval/guardrail/decision mappings, rejected secondary/blog domains, and explicit claim boundaries.

Generated reports:

- `docs/product-quality/research-brief-validation-report.json`
- `docs/product-quality/research-brief-validation-report.md`

Those reports include HTTPS `primarySourceInputs`, so `bun run product:primary-source-registry` can absorb the research ledger without fetching external sources.
