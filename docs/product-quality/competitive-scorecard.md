# Metaforge Competitive Evidence Scorecard

Snapshot date: 2026-05-21

This scorecard turns the user's top-level objective into a verifiable product gate. It does not claim Metaforge is already better than the top related projects. It defines the evidence Metaforge must keep producing before any stronger product claim is allowed. OpenClaude is the runtime substrate beneath the Meta/MFH/Orchestra operating layer, not the public product thesis.

## Top 10 Reference Set

The reference set is stored in `docs/product-quality/oss-top10-baseline-2026-05-21.json` and bounded by `bun run product:oss-baseline-refresh`, `bun run product:oss-baseline-freshness`, `bun run product:oss-source-review`, `bun run product:oss-architecture-targets`, and `bun run product:oss-architecture-gap-review`. The refresh uses GitHub REST metadata as current discovery evidence, the source review inspects README/root source surfaces and classifies 9 source-supported candidates plus 1 metadata-only candidate, the architecture-target queue maps those candidates to local no-provider absorption axes, and the gap review maps target axes to Metaforge/OpenClaude evidence plus protected blockers. This scorecard still treats the result as internal planning evidence until separate public-comparison and superiority-claim authorization exists.

| Rank | Project | Primary source | Stars at snapshot | Product signal |
| --- | --- | --- | ---: | --- |
| 1 | ultraworkers/claw-code | https://github.com/ultraworkers/claw-code | 192126 | Rust/Codex-compatible agentic coding candidate discovered by fresh GitHub search |
| 2 | anomalyco/opencode | https://github.com/anomalyco/opencode | 163314 | open-source coding agent |
| 3 | anthropics/claude-code | https://github.com/anthropics/claude-code | 125358 | terminal agentic coding tool |
| 4 | google-gemini/gemini-cli | https://github.com/google-gemini/gemini-cli | 104409 | terminal AI agent |
| 5 | openai/codex | https://github.com/openai/codex | 84266 | lightweight terminal coding agent |
| 6 | OpenHands/OpenHands | https://github.com/OpenHands/OpenHands | 74327 | AI-driven development platform |
| 7 | openinterpreter/open-interpreter | https://github.com/openinterpreter/open-interpreter | 63595 | natural language computer interface |
| 8 | cline/cline | https://github.com/cline/cline | 62127 | SDK, IDE extension, and CLI assistant |
| 9 | warpdotdev/warp | https://github.com/warpdotdev/warp | 59372 | agentic development environment born out of the terminal |
| 10 | ruvnet/ruflo | https://github.com/ruvnet/ruflo | 53696 | Claude/Codex-oriented agent orchestration candidate |

## Metaforge Product Thesis

Metaforge should compete by being the verifiable Meta/MFH/Orchestra operating layer for agent work:

- one workflow across cloud, local, OpenAI-compatible, Codex, Gemini, Ollama, Atomic Chat, and enterprise backends through the OpenClaude runtime substrate;
- explicit provider profiles and runtime doctoring;
- privacy gate through no-phone-home build verification;
- goal, research, and eval documents that make agentic work auditable;
- IDE/editor launch surface work must remain evidence-bound and must not claim VS Code extension availability until manifest/package smoke, local runtime smoke, and real Extension Development Host smoke all exist.

## Required Evidence Axes

| Axis | Current Metaforge/OpenClaude evidence | Gap to keep closing |
| --- | --- | --- |
| provider_breadth | README provider matrix and provider launch scripts | Add provider compatibility fixtures with pass/fail examples |
| terminal_workflow | `bin/openclaude`, `dist/cli.mjs`, slash/tool workflow docs | Add scripted golden-path terminal transcript tests |
| tool_loop_reliability | Bun tests under `src/`, orchestration tests, `bun run product:agent-replay-evals`, `bun run product:real-session-capture`, `bun run product:prompted-tool-loop-capture`, `bun run product:code-editing-trace-capture`, `bun run product:multi-file-code-editing-trace-capture`, `bun run product:regression-cycle-code-editing-trace-capture`, `bun run product:real-trace-evals`, `bun run product:trace-schema-contract`, `bun run product:trace-portability-export`, and `bun run product:trace-redaction-policy` over local `reports/orchestra-*.jsonl` traces with trace-kind coverage, query-source diversity, started-to-terminal ordering, terminal outcome coverage, a portable v1 trace schema contract, a source-hash-addressed portable trace JSONL view, verified enriched current generated trace producers, a no-provider user/planner/executor trajectory fixture, an operator-authorized broader local CLI command-session trace, an operator-authorized prompted local tool-loop trace, implementation-bearing single-file, multi-file, and regression-cycle fixture code-editing traces, and summary-only redaction policy | Backfill or replace older historical traces with non-synthetic enriched operator traces before stronger interoperability or reliability claims |
| privacy_and_no_phone_home | `bun run verify:privacy`, `bun run product:release-artifact`, `bun run product:release-provenance`, and `bun run product:release-reproducibility` | Add signed provenance after a real release boundary exists |
| runtime_doctoring | `bun run doctor:runtime`, `bun run product:runtime-doctor` | Extend regression fixtures beyond local no-provider mode |
| eval_and_quality_gates | `docs/EVALS.md`, this product quality gate, trace-graded local replay evals, operator-authorized local CLI capture, operator-authorized prompted local tool-loop capture, implementation-bearing single-file, multi-file, and regression-cycle fixture code-editing trace capture, real local JSONL trace grading with coverage-gap classification, trace schema contract validation, source-hash-addressed portable trace export, trace capture redaction policy, `bun run product:benchmark-readiness`, benchmark task manifest generation, `bun run product:external-benchmark-boundary`, `bun run product:local-benchmark-harness`, `bun run product:benchmark-efficiency-metrics`, Vexp/SWE-bench-style cost/token/turn/duration gap classification, `bun run product:benchmark-submission-readiness`, SWE-bench-style submission asset gap mapping, `bun run product:benchmark-policy-compliance`, SWE-bench policy and eligibility-claim blocking, `bun run product:terminal-bench-readiness`, Terminal-Bench/Harbor task-format and official-run gap mapping, `bun run product:trajectory-process-quality`, `bun run product:verification-report-consistency`, `bun run product:quality-blocker-taxonomy`, `bun run product:primary-source-registry`, `bun run product:evidence-manifest`, `bun run product:openssf-security-posture`, an explicit external benchmark authorization request, and source-controlled PR/push product-quality workflow wiring | Turn future claims into machine-checkable gates backed by non-synthetic real-session traces, approved external benchmark execution, local benchmark replay/process-quality, efficiency-metric, submission-asset, benchmark-policy, and Terminal-Bench readiness results, verification-report consistency, portable trace export, primary-source registry evidence, source-hash-addressed evidence manifest, trace schema contract, known-blocker taxonomy, OpenSSF/SLSA posture evidence, CodeQL SAST configuration, and hosted CI evidence |
| security_and_permissions | `SECURITY.md`, `docs/SECURITY_AND_GUARDRAILS.md`, `.github/dependabot.yml`, `.github/workflows/codeql.yml`, `bun run product:permission-regression`, and `bun run product:openssf-security-posture` for security policy, dependency update coverage, CodeQL SAST workflow coverage, SHA-pinned workflows, scoped workflow permissions, absent `pull_request_target`, frozen installs, npm provenance wiring, release environment gating, and Docker package permission scope | Extend permission fixtures into replayed tool-loop scenarios and add operator-authorized external Scorecard/hosted CodeQL/hosted CI posture evidence when a real GitHub repository boundary is available |
| onboarding_docs | README, Windows/macOS/Linux quick-start docs, `bun run product:onboarding-smoke` evidence for first-run documentation and CLI commands, and `bun run product:doc-link-integrity` evidence for local relative links plus canonical VS Code extension package paths | Add non-synthetic user onboarding session evidence before claiming onboarding completion across all operating systems |
| ide_or_editor_surface | `bun run product:ide-extension-surface` now classifies `extension_manifest_found`, `bun run product:ide-extension-scope` preserves the bounded no-availability decision, `bun run product:ide-extension-manifest-smoke` verifies the scoped VS Code manifest plus local package dry-run, `bun run product:ide-extension-runtime-smoke` verifies activation/command handlers plus Tree View and WebviewView provider registration through a local mock VS Code host, `bun run product:ide-extension-host-smoke` verifies activation plus all manifest command handlers in a real local VS Code Extension Development Host with current-session Workspace Trust isolation, `bun run product:ide-extension-workbench-smoke` verifies contributed Tree Views, TreeDataProviders, item reveal, non-empty view items, and TreeItem command execution in a real local VS Code Extension Development Host with the same isolation, `bun run product:vscode-update-boundary` records the current local updater protected-action boundary state, `bun run product:vscode-startup-diagnostics` preserves sentinel candidates, CodeSetup process evidence, clear update-guard status, and official VS Code Workspace Trust/CLI/test sources, `bun run product:ide-extension-webview-render-smoke` verifies provider-backed Control Center WebviewView HTML with strict no-script CSP, VS Code theme tokens, accessible command action markers, and no network/script surfaces, `bun run product:ide-extension-rendered-workbench-screenshot` records a bounded local PNG/SVG workbench-panel render artifact with dimensions, nonblank evidence, hashes, and command-action coverage, and `bun run product:ide-extension-webview-interaction-smoke` verifies native command buttons, focus order, command registration, command execution, bounded messages, and accessibility semantics without install/publish/deploy/product launch | Add operator-authorized non-synthetic IDE/user session evidence before claiming extension availability |
| release_hygiene | release config, changelog, smoke script, `bun run product:git-release-hygiene`, `bun run product:release-artifact`, `bun run product:release-provenance`, `bun run product:release-reproducibility`, `bun run product:third-party-license-quality`, `bun run product:source-license-metadata-quality`, `bun run product:license-boundary-authorization`, and `bun run product:openssf-security-posture` | Add release-candidate checklist tied to a real Git repo, owner/legal license-boundary decisions, external Scorecard/hosted CodeQL evidence, and signed artifact boundary |

## Claim Boundary

Allowed now:

- Metaforge has a verifiable product-quality gate and a fresh GitHub top-10 reference baseline with refresh, freshness, README/root-source review, exclusion, and provenance checks.
- Metaforge has a concrete path to compete against the leading GitHub coding-agent projects through evidence-gated Meta/MFH/Orchestra work on top of the OpenClaude runtime substrate.

Not allowed now:

- claiming market leadership;
- claiming release readiness;
- claiming production readiness;
- claiming external validation;
- claiming autonomous reliability.

## Learning Loop

The absorption register at `docs/product-quality/open-source-absorption-register.json` records patterns from stronger primary-source projects and the local OpenClaude action for each. This is mandatory because the product goal is not just to compare against top projects once, but to keep learning from them when a better design is found.
