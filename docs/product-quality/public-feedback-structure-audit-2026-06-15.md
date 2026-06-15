# Public Feedback Structure Audit - 2026-06-15

Generated after public/community feedback on the Metaforge/OpenClaude repository.

## Claim Boundary

- This is a local, no-autofix structure audit.
- It records evidence for follow-up refactoring; it does not prove the repo is
  clean, production-ready, externally validated, or legally risk-free.
- Knip findings are candidates only. This repo contains generated files,
  compatibility exports, tests, provider surfaces, and CLI entrypoints that can
  create false positives.
- No auto-fix command was run.

## Primary Tool Sources

| Tool | Primary source | Use in this audit |
| --- | --- | --- |
| Knip | <https://knip.dev/> and <https://github.com/webpro-nl/knip> | Candidate unused exports, types, files, and dependencies. |
| dependency-cruiser | <https://github.com/sverweij/dependency-cruiser> | Not run in this pass; recommended next for circular dependency and topology rules. |
| jscpd | <https://jscpd.dev/> and <https://github.com/kucherenko/jscpd> | Product-script clone detection. |
| Lumin Repo Lens | <https://github.com/annyeong844/lumin-repo-lens> | Not installed in this pass; community-recommended topology and clone-cue lens. |

## Community Feedback Converted To Checks

| Feedback | Current response |
| --- | --- |
| AGENTS.md looked like a huge private rule dump. | AGENTS.md was reduced to public-facing repo guidance and now has a line-count/public-memory gate. |
| Local folder names hurt trust. | `verify:privacy` now includes public repo readiness, and `public-artifact-hygiene` scans `README.ko.md` too. |
| README should support Korean readers. | Added `README.ko.md` and linked it from `README.md`. |
| Marker-only checks are not enough. | Recorded as backlog: add happy-path, edge-case, and side-effect tests per product gate. |
| Product scripts look heavily cloned. | Confirmed with local heuristic counts and jscpd; `product:script-duplication-audit` now has baseline caps and is wired into `product:quality`. |
| Dead exports may exist. | Confirmed as knip candidates only; manual review required before deletion. |

## Local Heuristic Counts

Command:

```text
node local product-script helper-count scan
```

Observed:

| Signal | Count |
| --- | ---: |
| `scripts/product-*.ts` files | 87 |
| files containing `function check(` | 80 |
| files containing `function sha256(` | 54 |
| files containing `function readText(` | 43 |
| files containing `function writeMarkdown(` | 50 |
| files containing `type Check =` | 54 |

Interpretation: the feedback about helper cloning is directionally correct.
This does not mean all copies should be mechanically extracted in one pass.
Product-quality scripts intentionally duplicate some local context; refactoring
should start with stable helpers that do not weaken report readability or claim
boundaries.

## jscpd Evidence

Command:

```text
bunx jscpd scripts --pattern "**/product-*.ts" --format typescript --min-lines 20 --min-tokens 120 --reporters json --reporters console --output <temp> --no-tips
```

Tool version:

```text
cpd 5.0.9
```

Summary:

| Metric | Value |
| --- | ---: |
| files analyzed | 87 |
| clones found | 30 |
| duplicated lines | 858 |
| duplicated line percentage | 2.26% |
| duplicated tokens | 5,338 |
| duplicated token percentage | 2.25% |

Top clone pairs:

| Pair | Lines | Tokens |
| --- | ---: | ---: |
| `product-community-intake-quality.ts` <-> `product-community-profile-quality.ts` | 25 | 152 |
| `product-ide-extension-host-smoke.ts` <-> `product-ide-extension-workbench-smoke.ts` | 45 | 159 |
| `product-ide-extension-host-smoke.ts` <-> `product-ide-extension-workbench-smoke.ts` | 74 | 374 |
| `product-ide-extension-rendered-workbench-screenshot.ts` <-> `product-ide-extension-webview-render-smoke.ts` | 37 | 144 |
| `product-ide-extension-runtime-smoke.ts` <-> `product-ide-extension-webview-interaction-smoke.ts` | 25 | 126 |
| `product-license-boundary-authorization.ts` <-> `product-lockfile-sbom-quality.ts` | 21 | 129 |
| `product-license-boundary-authorization.ts` <-> `product-source-license-metadata-quality.ts` | 21 | 129 |
| `product-license-boundary-authorization.ts` <-> `product-third-party-license-quality.ts` | 21 | 129 |
| `product-oss-baseline-drift-closure.ts` <-> `product-oss-safe-backlog-closure.ts` | 22 | 142 |
| `product-oss-eval-quality-gate-checklist.ts` <-> `product-oss-terminal-workflow-evidence.ts` | 52 | 162 |
| `product-oss-ide-or-editor-surface-evidence.ts` <-> `product-oss-privacy-no-phone-home-evidence.ts` | 29 | 184 |
| `product-oss-onboarding-docs-evidence.ts` <-> `product-oss-provider-breadth-evidence.ts` | 26 | 191 |

## Knip Candidate Evidence

Command:

```text
bunx knip --exports --reporter json --no-exit-code --no-progress > <temp>/knip-exports.json
```

Tool version:

```text
6.16.1
```

Summary:

| Signal | Count |
| --- | ---: |
| files with candidate issues | 657 |
| candidate unused exports | 1,462 |
| candidate unused types | 492 |
| duplicate export candidates | 12 |

First candidate files:

| File | Export candidates | Type candidates |
| --- | ---: | ---: |
| `src/commands.ts` | 2 | 0 |
| `src/services/api/providerConfig.ts` | 7 | 1 |
| `src/utils/providerProfile.ts` | 4 | 0 |
| `scripts/provider-discovery.ts` | 4 | 0 |
| `src/utils/config.ts` | 14 | 7 |
| `src/utils/geminiCredentials.ts` | 2 | 1 |
| `src/utils/githubModelsCredentials.ts` | 2 | 1 |
| `src/utils/providerValidation.ts` | 1 | 0 |
| `src/utils/providerDiscovery.ts` | 4 | 0 |
| `src/bridge/sessionRunner.ts` | 1 | 1 |
| `src/constants/prompts.ts` | 5 | 0 |
| `src/state/AppState.tsx` | 2 | 3 |

Interpretation: run a narrower Knip config before deleting anything. The first
pass likely includes entrypoint, generated, test-only, and compatibility exports.

## Recommended Next Refactor Order

1. Continue extracting tiny product-quality report helpers only after
   representative scripts are covered by behavior tests. The first ratchet now
   blocks increases in duplicate `check`, `readText`, and `sha256Text` helper
   occurrences.
2. Start with sibling duplicate pairs, especially IDE extension smoke scripts
   and OSS evidence scripts.
3. Add happy-path, edge-case, and side-effect assertions to each product gate
   before removing repeated local checks.
4. Add a checked Knip config with explicit entrypoints, generated files, and
   test-only exports before treating unused-export candidates as blockers.
5. Run dependency-cruiser separately for circular dependency and layer-boundary
   evidence.
