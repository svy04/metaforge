# Product Quality Gate

This gate is the first durable productization control for the goal: make OpenClaude a verifiable high-quality product against the leading related GitHub projects.

## Gate Command

```powershell
bun run product:quality
```

## Gate Checks

The gate validates:

- repo-wide TypeScript diagnostics are freshly classified in a health report;
- the TypeScript health report records a diagnostic budget and the current diagnostic count must not exceed that ratchet budget;
- primary-source OSS learning and absorption entries exist;
- the competitive baseline exists and contains exactly 10 ranked projects;
- OSS baseline refresh fixtures perform an explicit GitHub REST Search/Repository metadata refresh, write the fresh 2026-05-21 top-10 reference set, record newly discovered high-star related candidates and excluded non-product candidates, allow only a validated same-day cached refresh when GitHub API rate-limit is exhausted, and block superiority/public comparison claims;
- OSS baseline freshness fixtures verify top-10 ranks, star ordering, GitHub source URLs, license assertions, source-report provenance, and current snapshot freshness while blocking superiority/public comparison claims unless separate claim authorization exists;
- OSS source review fixtures inspect the refreshed top-10 candidates through GitHub README/root source surfaces, classify source-supported versus metadata-only candidates, preserve GitHub REST rate-limit evidence, and keep public comparison, superiority, release, production, external-validation, and autonomous-reliability claims blocked;
- OSS architecture target fixtures convert the source-reviewed top-10 evidence into a local no-provider architecture absorption target queue, prioritizing 9 source-supported candidates, deferring 1 metadata-only candidate, covering core product-quality axes, and keeping public comparison, superiority, release, production, external-validation, and autonomous-reliability claims blocked;
- OSS architecture gap review fixtures map the architecture target queue to current OpenClaude evidence, safe internal actions, explicit protected gaps, and claim blockers before any implementation-pattern absorption;
- OSS axis architecture review fixtures convert the 3 high-priority source-supported targets into per-axis local review records, safe internal backlog items, protected boundaries, and hash-addressed JSONL before implementation-pattern absorption;
- OSS safe backlog plan fixtures convert the 47 high-priority safe internal backlog items into source-bound, axis-bound, protected-boundary-preserving next internal evidence-gate candidates before any implementation or claim expansion;
- OSS safe backlog closure fixtures verify the 9 planned internal evidence-gate candidates are all closed by existing local no-provider evidence gates, write source-hash-addressed closure JSONL, and keep superiority, readiness, provider/live/external, and protected-action claims blocked;
- OSS baseline drift closure fixtures verify fresh GitHub top-10 additions and removals are propagated through source review, architecture targets, gap review, axis review, safe backlog planning, and safe backlog closure before any benchmark planning is considered current;
- OSS benchmark comparison matrix fixtures bind the current top-10 baseline to every required product axis, creating 100 project-axis benchmarkability rows while keeping comparison, superiority, readiness, provider/live/external, and protected-action claims blocked;
- OSS comparison readiness index fixtures rank the comparison matrix by axis and project into 20 priority records, identify the next safe internal evidence work, and keep the first real protected-action boundary explicit;
- OSS IDE/editor surface evidence fixtures convert the highest-priority `ide_or_editor_surface` comparison axis into hash-bound VS Code extension surface, manifest, mock-host, real-host, workbench, webview, screenshot, interaction, and startup-boundary evidence while keeping VS Code CLI/PATH/install-state repair, extension availability, public comparison, superiority, release, production, external-validation, and autonomous-reliability claims blocked;
- OSS eval and quality gate checklist fixtures convert the `eval_and_quality_gates` backlog into explicit public benchmark, leaderboard, superiority, readiness, and external-validation claim rejection rules before any protected benchmark execution;
- OSS terminal workflow evidence fixtures convert the `terminal_workflow` backlog into hash-bound first-run, failure-recovery, doctor-handoff, command-hash, and no-provider boundary evidence before any non-synthetic session or external benchmark claim;
- OSS onboarding docs evidence fixtures convert the `onboarding_docs` backlog into hash-bound onboarding smoke, documentation link integrity, and community profile evidence before any non-synthetic first-run or cross-platform onboarding claim;
- OSS runtime doctoring evidence fixtures convert the `runtime_doctoring` backlog into hash-bound runtime-doctor and VS Code startup diagnostic evidence before any repair, reinstall, dependency install, provider probe, or external diagnostic action;
- OSS security and permissions evidence fixtures convert the `security_and_permissions` backlog into hash-bound permission regression, OpenSSF/SLSA posture, and dependency-governance evidence before any hosted Scorecard, hosted CodeQL, hosted branch-protection, or public security posture claim;
- OSS tool-loop reliability evidence fixtures convert the `tool_loop_reliability` backlog into hash-bound prompted tool-loop, disposable code-editing, interrupted-tool recovery, protected-action denial, trace schema, portability, and redaction-policy evidence before any real product repo mutation, provider-backed execution, external benchmark, or autonomous reliability claim;
- OSS provider-breadth evidence fixtures convert the `provider_breadth` backlog into hash-bound provider capability, failure-mode, runtime-doctor, fallback, and live-authorization boundary evidence before any provider call, live model call, live provider validation, compatibility claim, model-behavior claim, external validation, or autonomous reliability claim;
- OSS privacy/no-phone-home evidence fixtures convert the `privacy_and_no_phone_home` backlog into hash-bound build-output banned-pattern scanning, no-telemetry fixture, privacy-settings surface, and public-claim-boundary evidence before any public privacy, external telemetry-comparison, release, production, external-validation, or superiority claim;
- OSS release hygiene evidence fixtures convert the `release_hygiene` backlog into hash-bound artifact reproducibility, SBOM-shaped inventory, license-boundary, git/release boundary, signed-provenance, publish/deploy, and readiness-claim blockers before any commit, push, publish, deploy, launch, signed provenance, legal/NOTICE/REUSE decision, or release/public/production claim;
- every baseline project has stars, license metadata, and a primary GitHub source URL;
- the baseline contains all required product axes;
- `package.json` exposes the core validation commands;
- the product docs preserve the claim boundary;
- the local project has README, security, eval, roadmap, and onboarding surfaces needed for productization.
- the runtime builds and reports its version through `bun run smoke`;
- golden-path terminal transcripts verify local `--version` and `--help` behavior without provider, live model, or external calls;
- terminal failure recovery transcripts verify a bounded local CLI failure, help recovery, doctor handoff, and version recovery as hash-only no-provider transcript evidence without provider, live model, external, dependency-install, or protected-action calls;
- onboarding smoke fixtures verify README quick-start links, Windows/macOS/Linux setup docs, install/start/provider/troubleshooting/update/uninstall guidance, and local no-provider `--version`, `--help`, and `doctor --help` commands while blocking unsupported cross-platform runtime and readiness claims;
- documentation link integrity fixtures verify local README/quick-start/product-quality relative links, align the README VS Code extension path to the canonical `packages/openclaude-vscode` product surface, and block external link fetching or release/readiness claims;
- primary-source registry fixtures inventory the `primarySourceInputs` already recorded across product-quality reports, classify source kinds, reject blog-summary and secondary-source domains, write `reports/openclaude-primary-source-registry.jsonl`, and block external source fetching, provider/live/external calls, and readiness claims;
- agent instructions quality fixtures absorb OpenHands repository-agent guidance by verifying `AGENTS.md` contains a concise repository purpose, setup/verification commands, repository structure, CI/workflow evidence, GStack/GSD/Superpowers boundaries, primary-source research rules, verification standards, and protected-boundary language without provider, live model, or external calls;
- community intake quality fixtures absorb GitHub issue/PR template guidance by verifying structured bug reports, feature requests, PR evidence checklists, blank-issue blocking, security-policy presence, secret redaction language, protected-action boundaries, and release/readiness claim blocking without GitHub API, provider, live model, or external calls;
- community profile quality fixtures absorb GitHub healthy-contribution guidance by verifying README links, CONTRIBUTING, SUPPORT, CODE_OF_CONDUCT, SECURITY, LICENSE, validation expectations, support routing, secret redaction language, code-of-conduct enforcement, security response scope, and derivative-code license boundaries without GitHub API, provider, live model, or external calls;
- maintainer ownership quality fixtures absorb GitHub CODEOWNERS and protected-branch guidance by verifying `.github/CODEOWNERS` location, size, syntax, default ownership, protected surface ownership, product-quality/report ownership, and hosted-enforcement claim blocking without GitHub API, provider, live model, or external calls;
- dependency governance quality fixtures absorb GitHub Dependency Review, Dependabot, Bun lockfile, and OpenSSF pinned-dependency guidance by verifying `packageManager`, `bun.lock`, direct dependency inventory, dependency-review workflow SHA pinning, Dependabot npm/GitHub Actions coverage, frozen install wiring, and hosted vulnerability/review claim blocking without running installs, audits, GitHub APIs, providers, live models, or external calls;
- lockfile SBOM quality fixtures absorb Bun lockfile, CycloneDX, SPDX, and GitHub Dependency Graph SBOM guidance by verifying the local `bun.lock` package inventory, transitive dependency relationships, SHA-512 integrity metadata, and `reports/openclaude-lockfile-sbom-inventory.jsonl` without running installs, audits, hosted SBOM exports, GitHub APIs, providers, live models, or external calls, and without claiming official SPDX/CycloneDX compliance;
- third-party license quality fixtures absorb SPDX License List, npm package metadata, and GitHub licensing guidance by verifying root `LICENSE`, installed package license fields, direct dependency metadata coverage, license-file/NOTICE-file gap classification, and `reports/openclaude-third-party-license-inventory.jsonl` without running installs, npm/GitHub lookups, legal review, NOTICE generation, provider calls, live model calls, or external calls, and without claiming license compliance or third-party NOTICE readiness;
- source license metadata quality fixtures absorb REUSE/SPDX source-file metadata guidance by verifying the current root derived-code/modification-license boundary, scanning source/product files for `SPDX-License-Identifier`, classifying missing file-level metadata and absent REUSE compliance artifacts, and writing `reports/openclaude-source-license-metadata-inventory.jsonl` without running REUSE tooling, generating SPDX documents, performing legal review, or claiming REUSE/source-license compliance or source-metadata readiness;
- license boundary authorization fixtures absorb GitHub licensing, npm license metadata, SPDX, and REUSE guidance by converting third-party and source-license inventories into `docs/product-quality/license-boundary-authorization-request.md` and `reports/openclaude-license-boundary-authorization-items.jsonl`, with every legal/NOTICE/REUSE/source-metadata/release-claim authorization defaulting to false and without running legal review, NOTICE generation, REUSE tooling, source-file rewrites, dependency installs, npm/GitHub lookups, provider calls, live model calls, external calls, or readiness/compliance claims;
- provider compatibility fixtures verify direct provider flags, profile preset defaults, local-provider key requirements, product-description provider coverage, and classified provider-surface drift without provider, live model, or external calls;
- permission regression fixtures verify protected permission surfaces, targeted permission/security tests, bypass-mode gating, sandbox trust boundaries, plugin hook hardening, WebFetch SSRF guarding, swarm permission path hardening, permission-rule validation, and auto-classifier transcript bounds without provider, live model, or external calls;
- runtime doctor regression fixtures verify local JSON/stdout and `--out` report paths with provider modes explicitly disabled and no provider, live model, or external calls;
- provider capability matrix fixtures convert provider compatibility, runtime doctor, and OSS axis-review backlog evidence into 21 per-surface capability rows plus 5 explicit failure-mode rows while keeping provider-backed execution, provider compatibility, release, production, public, external-validation, and autonomous-reliability claims blocked;
- Git release hygiene fixtures classify repo-root availability, package publication surfaces, and the commit/push boundary without committing, pushing, publishing, deploying, or launching;
- IDE extension surface fixtures classify VS Code extension manifest availability without packaging, installing, publishing, deploying, or claiming extension availability;
- IDE extension scope fixtures convert the current IDE surface status into a primary-source-backed VS Code manifest scope, including required manifest fields, commands, views, configuration keys, activation events, and validation required before any availability claim;
- IDE extension manifest smoke fixtures verify `packages/openclaude-vscode/package.json`, `packages/openclaude-vscode/dist/extension.js`, manifest contribution alignment, and local `npm pack --dry-run --json --ignore-scripts` output without installing, publishing, deploying, launching, or claiming extension availability;
- IDE extension runtime smoke fixtures verify `activate()`, `deactivate()`, command registration, command handler execution, and bounded local messages through a mock VS Code extension host without installing, publishing, deploying, launching, or claiming extension availability;
- IDE extension host smoke fixtures verify the scoped VS Code extension inside a real local Extension Development Host using `--extensionDevelopmentPath` and `--extensionTestsPath`, proving activation plus all manifest command handlers execute without install, publish, deploy, product launch, provider calls, live model calls, external calls, or extension availability claims;
- IDE extension workbench smoke fixtures verify the scoped VS Code extension registers contributed Tree Views, attaches TreeDataProviders, reveals a first item in each view through the TreeView API, executes every TreeItem command in the real Extension Development Host, and keeps install, publish, deploy, product launch, provider calls, live model calls, external calls, and extension availability claims blocked;
- VS Code update boundary fixtures classify local real-host startup state by importing the host/workbench smoke reports, checking the local VS Code update sentinel and CodeSetup processes, and blocking process termination, reinstall, extension availability, release, and production-readiness claims unless explicit owner action exists;
- IDE extension webview render smoke fixtures verify the scoped Control Center WebviewView contribution, activation event, `registerWebviewViewProvider` registration, strict no-script CSP, VS Code theme tokens, accessible command action markers, and no-network HTML through a mock webview host without installing, publishing, deploying, launching, or claiming extension availability;
- IDE extension rendered workbench screenshot fixtures render a bounded local PNG/SVG Control Center workbench-panel artifact from the verified WebviewView contract, record dimensions, nonblank channel evidence, SHA-256 hashes, command action coverage, and keep install, publish, deploy, launch, provider calls, live model calls, external calls, and extension availability claims blocked;
- IDE extension webview interaction smoke fixtures verify native command buttons, list-region semantics, keyboard activation model, manifest-order focus order, registered command alignment, mock-host command execution, bounded local messages, and source-report consistency without installing, publishing, deploying, launching, or claiming extension availability;
- release artifact file-list fixtures verify local `npm pack --dry-run --json --ignore-scripts` output, expected package files, bounded file count, and forbidden package-file exclusions without publishing, deploying, launching, committing, or pushing;
- release artifact provenance fixtures compute local package-file SHA-256 hashes and a package.json SBOM-style component inventory without publishing, deploying, launching, committing, pushing, provider calls, live model calls, or external calls;
- release artifact reproducibility fixtures run local `npm pack --json --ignore-scripts` twice in a temporary directory, compare package file lists plus tarball hashes, and remove temporary tarballs without publishing, deploying, launching, committing, or pushing;
- trace-graded agent replay eval fixtures grade existing local product-quality evidence across CLI surface, permission boundaries, runtime doctoring, Git/release boundary, IDE extension surface/runtime smoke, and release artifact hygiene without provider, live model, or external calls;
- source-controlled check fixtures verify that `.github/workflows/pr-checks.yml` runs `bun run product:quality` on pull requests and main pushes, pins GitHub Actions by SHA, and keeps release/publish/deploy/launch actions out of the PR workflow;
- OpenSSF/SLSA security posture fixtures verify `SECURITY.md`, Dependabot coverage for npm/pip/GitHub Actions, PR and release workflow token permissions, SHA-pinned workflow actions, absent `pull_request_target`, local CodeQL SAST workflow configuration with extended queries, frozen dependency installs, npm provenance configuration, release environment gating, and Docker package permission scope without running external Scorecard, hosted CI, hosted CodeQL analysis, registry attestation verification, publishing, deploying, launching, or making release/readiness/external claims;
- real session capture fixtures execute a broader local no-provider CLI command session covering `dist/cli.mjs --version`, `--help`, `doctor --help`, `auto-mode --help`, `auto-mode defaults`, `agents --help`, and `agents --setting-sources user,project,local`, write a sanitized JSONL trace, record command-output hashes instead of raw stdout, and prove the operator authorization remains bounded to local no-provider CLI capture;
- prompted tool-loop capture fixtures record a local operator prompt hash, execute bounded local no-provider CLI introspection commands as tool steps, write a sanitized JSONL trace, and keep non-synthetic user-session claims blocked;
- code-editing trace capture fixtures mutate only a disposable `_fixtures/product-code-editing-trace` source file, record exploration/implementation/verification trace events, verify three deterministic fixture unit cases, and keep production repo mutation, provider calls, external calls, and reliability/readiness claims blocked;
- multi-file code-editing trace capture fixtures mutate only disposable `_fixtures/product-multi-file-code-editing-trace` source files, record multi-file exploration/implementation/verification trace events, verify four deterministic checkout cases, and keep production repo mutation, provider calls, external calls, and reliability/readiness claims blocked;
- regression-cycle code-editing trace capture fixtures mutate only disposable `_fixtures/product-regression-cycle-code-editing-trace` source files, record a plausible wrong patch, failed regression check, repaired patch, and passing regression check, and keep production repo mutation, provider calls, external calls, and reliability/readiness claims blocked;
- tool-interruption recovery trace fixtures mutate only disposable `_fixtures/product-tool-interruption-recovery-trace` files, record an interrupted tool observation, invariant violation, bounded reread recovery, recovered summary, and final verification trace, and keep protected repo mutation, provider calls, external calls, and reliability/readiness claims blocked;
- protected-action denial trace fixtures mutate only disposable `_fixtures/product-protected-action-denial-trace` files, record a protected action request, policy denial, safe alternative summary, and final verification trace, and keep protected repo mutation, provider calls, external calls, VS Code/PATH/install-state mutation, and reliability/readiness claims blocked;
- real session trace eval fixtures grade existing local `reports/orchestra-*.jsonl` artifacts and a no-provider user/planner/executor trajectory fixture for JSONL parseability, required event fields, started-to-terminal status transitions, trace-kind coverage, query-source diversity, success/failure representation, coverage-gap classification, credential-pattern absence, and raw request-id omission from summaries without provider, live model, or external calls;
- trace schema contract fixtures validate every local `reports/orchestra-*.jsonl` event against a portable v1 trace contract, preserve hashes from `product:real-trace-evals`, classify OpenTelemetry-style `eventName`/trace context and SWE-agent-style action triplet gaps without protected action, and keep stronger interoperability/readiness claims blocked;
- trace portability export fixtures write `reports/openclaude-portable-trace-events.jsonl` as a source-hash-addressed portable view of every local trace event, preserving source trace path/hash/line/event hash while filling portable `eventName`, `traceId`/`spanId`, and action-observation fields without rewriting historical raw traces or expanding claims;
- trace capture redaction policy fixtures scan local trace files, require summary-only publishable fields, forbid raw credentials/provider payloads, define an explicit operator capture workflow, and record that non-synthetic capture has not been performed by this gate;
- benchmark readiness fixtures map local product-quality evidence into a SWE-bench/OpenHands-style task manifest and readiness matrix, preserving task IDs, source evidence hashes, trajectory/replay/reproducibility dimensions, unresolved gaps, and the external benchmark run boundary without provider, live model, external, Docker, or remote-runtime calls;
- external benchmark boundary fixtures convert the benchmark readiness matrix into a protected-action authorization map, default every external benchmark/protected-action authorization to false, and write the owner authorization request required before external datasets, containers, providers, live models, remote runtimes, hosted CI, public claims, or readiness claims can be used;
- local benchmark harness fixtures replay the benchmark task manifest as a local no-provider JSONL result set, verify every source-evidence hash, classify environment-blocked tasks without hiding them, and keep external benchmark result claims blocked;
- benchmark efficiency metrics fixtures convert local benchmark replay results into Vexp/SWE-bench-style cost, token, turn, duration, and resolution fields, classify those fields as unmeasured gaps in no-provider mode, and block external comparison or cost-efficiency claims;
- benchmark submission readiness fixtures convert SWE-bench-style submission expectations into an auditable local asset matrix, preserving predictions, metadata, README, trajectory, log, patch, report/test-output, efficiency, and verification-instruction gaps while keeping official external submission, leaderboard, release, public, production, external-validation, and autonomous-reliability claims blocked;
- benchmark policy compliance fixtures absorb the current SWE-bench experiments submission policy boundary, classify open-research publication, research affiliation, open-source methods, peer-review, official asset, and leaderboard PR requirements, and block official eligibility, leaderboard, public, release, production, external-validation, and autonomous-reliability claims from local readiness evidence;
- Terminal-Bench readiness fixtures map Harbor/Terminal-Bench-style task instruction, Docker environment, verifier, oracle solution, trajectory, result/reward, review/audit, official run, and leaderboard-submission expectations to current OpenClaude local evidence while keeping Harbor install, Docker/container execution, providers, live models, external services, leaderboard claims, and readiness claims blocked;
- VS Code startup diagnostics fixtures preserve current real Extension Development Host startup state as local evidence by reading host/workbench smoke reports, isolated VS Code logs, sentinel candidates, CodeSetup process listings, and Workspace Trust isolation arguments, while blocking process termination, update-state deletion, reinstall, dependency install, availability claims, and readiness claims;
- trajectory process-quality fixtures classify local trace phase labels and waste signals using SWE-agent/AgentLens/AgentRx/Aider-style process evidence patterns, so pass/fail summaries cannot hide missing verification, retry loops, temporal disorder, or raw trace exposure;
- verification report consistency fixtures check that the current product-quality verification report no longer carries stale TypeScript blocker wording after the repo-wide typecheck reached zero diagnostics, while preserving the VS Code updater, no-git-root, and external benchmark protected-action blockers;
- quality blocker taxonomy fixtures classify either a clear VS Code host/workbench/replay state or the known VS Code updater-dependent host, workbench, and replay failure groups, so a future unexpected failure cannot hide inside the existing blocker envelope;
- public claim boundary fixtures scan README/package/community/security/quick-start/product-quality public surfaces for unauthorized positive launch, publish, release, production, public, external-validation, provider-backed, live-model, autonomous-reliability, and top-10 superiority claims while preserving explicit blocked-context wording;
- protected-action authorization packet fixtures consolidate VS Code/PATH/install-state repair, real Git commit/push, release execution, signed provenance, legal/NOTICE/REUSE, provider/live model validation, external benchmark execution/submission, and public/release/production/external/autonomous claim boundaries into explicit default-false owner decision items without executing protected actions;
- product evidence manifest fixtures write `reports/openclaude-product-evidence-manifest.jsonl` as a source-hash-addressed evidence package for product-quality reports, benchmark artifacts, workflow files, package source metadata, OSS IDE/editor evidence, the protected-action authorization packet, and the quality gate itself, following SLSA/in-toto-style subject/materials discipline without generating signed provenance or external attestation claims;
- the build output passes `bun run verify:privacy`.

## Required Core Commands

- `bun run build`
- `bun test`
- `bun run typecheck`
- `bun run smoke`
- `bun run verify:privacy`
- `bun run doctor:runtime`
- `bun run hardening:strict`
- `bun run product:typecheck-health`
- `bun run product:oss-baseline-refresh`
- `bun run product:oss-baseline-freshness`
- `bun run product:oss-source-review`
- `bun run product:oss-architecture-targets`
- `bun run product:oss-architecture-gap-review`
- `bun run product:oss-axis-architecture-review`
- `bun run product:oss-safe-backlog-plan`
- `bun run product:oss-safe-backlog-closure`
- `bun run product:oss-baseline-drift-closure`
- `bun run product:oss-benchmark-comparison-matrix`
- `bun run product:oss-comparison-readiness-index`
- `bun run product:oss-ide-or-editor-surface-evidence`
- `bun run product:oss-eval-quality-gate-checklist`
- `bun run product:oss-terminal-workflow-evidence`
- `bun run product:oss-onboarding-docs-evidence`
- `bun run product:oss-runtime-doctoring-evidence`
- `bun run product:oss-security-permissions-evidence`
- `bun run product:oss-tool-loop-reliability-evidence`
- `bun run product:oss-provider-breadth-evidence`
- `bun run product:oss-privacy-no-phone-home-evidence`
- `bun run product:oss-release-hygiene-evidence`
- `bun run product:golden-transcripts`
- `bun run product:terminal-failure-recovery-transcripts`
- `bun run product:onboarding-smoke`
- `bun run product:doc-link-integrity`
- `bun run product:primary-source-registry`
- `bun run product:agent-instructions-quality`
- `bun run product:community-intake-quality`
- `bun run product:community-profile-quality`
- `bun run product:maintainer-ownership-quality`
- `bun run product:dependency-governance-quality`
- `bun run product:lockfile-sbom-quality`
- `bun run product:third-party-license-quality`
- `bun run product:source-license-metadata-quality`
- `bun run product:license-boundary-authorization`
- `bun run product:provider-compatibility`
- `bun run product:permission-regression`
- `bun run product:runtime-doctor`
- `bun run product:provider-capability-matrix`
- `bun run product:git-release-hygiene`
- `bun run product:ide-extension-surface`
- `bun run product:ide-extension-scope`
- `bun run product:ide-extension-manifest-smoke`
- `bun run product:ide-extension-runtime-smoke`
- `bun run product:ide-extension-host-smoke`
- `bun run product:ide-extension-workbench-smoke`
- `bun run product:vscode-update-boundary`
- `bun run product:vscode-startup-diagnostics`
- `bun run product:ide-extension-webview-render-smoke`
- `bun run product:ide-extension-rendered-workbench-screenshot`
- `bun run product:ide-extension-webview-interaction-smoke`
- `bun run product:release-artifact`
- `bun run product:release-provenance`
- `bun run product:release-reproducibility`
- `bun run product:agent-replay-evals`
- `bun run product:source-controlled-checks`
- `bun run product:openssf-security-posture`
- `bun run product:real-session-capture`
- `bun run product:prompted-tool-loop-capture`
- `bun run product:code-editing-trace-capture`
- `bun run product:multi-file-code-editing-trace-capture`
- `bun run product:regression-cycle-code-editing-trace-capture`
- `bun run product:tool-interruption-recovery-trace`
- `bun run product:protected-action-denial-trace`
- `bun run product:real-trace-evals`
- `bun run product:trace-schema-contract`
- `bun run product:trace-portability-export`
- `bun run product:trace-redaction-policy`
- `bun run product:benchmark-readiness`
- `bun run product:external-benchmark-boundary`
- `bun run product:local-benchmark-harness`
- `bun run product:benchmark-efficiency-metrics`
- `bun run product:benchmark-submission-readiness`
- `bun run product:benchmark-policy-compliance`
- `bun run product:terminal-bench-readiness`
- `bun run product:trajectory-process-quality`
- `bun run product:verification-report-consistency`
- `bun run product:quality-blocker-taxonomy`
- `bun run product:public-claim-boundary`
- `bun run product:protected-action-authorization-packet`
- `bun run product:evidence-manifest`
- `bun run product:quality`

## Terminal Condition For This Gate

`PRODUCT_QUALITY_GATE_READY` means the project now has a reproducible product-quality gate for the competitive productization baseline, explicit GitHub REST OSS baseline refresh evidence, OSS baseline freshness/provenance, GitHub README/root-source review evidence for the refreshed top-10 candidates, local no-provider OSS architecture absorption target evidence, local no-provider OSS architecture gap review evidence, local no-provider OSS high-priority axis architecture review evidence, local no-provider OSS safe backlog planning evidence, local no-provider OSS IDE/editor surface evidence, local no-provider OSS eval/quality-gate claim-rejection checklist evidence, local no-provider OSS terminal workflow evidence matrix, local no-provider OSS onboarding docs evidence matrix, local no-provider OSS runtime doctoring evidence matrix, local no-provider OSS security and permissions evidence matrix, local no-provider OSS tool-loop reliability evidence matrix, local no-provider OSS provider-breadth evidence matrix, local no-provider OSS privacy/no-phone-home evidence matrix, TypeScript health classification, build smoke, golden-path terminal transcripts, terminal failure recovery transcript evidence, onboarding smoke evidence, documentation link integrity evidence, primary-source registry evidence, agent instructions quality evidence, community intake evidence, community profile quality evidence, maintainer ownership quality evidence, dependency governance quality evidence, lockfile SBOM-shaped package/relationship inventory evidence, third-party license metadata and NOTICE-gap inventory evidence, source-file REUSE/SPDX metadata gap inventory evidence, explicit license-boundary owner/legal authorization request evidence, provider compatibility fixtures, provider capability/failure-mode matrix evidence, permission regression fixtures, runtime doctor regression fixtures, Git release hygiene classification, IDE extension surface classification, IDE extension scope planning, IDE extension manifest/package dry-run smoke evidence, IDE extension mock-host runtime smoke evidence, real VS Code Extension Development Host command smoke evidence, real VS Code Tree View workbench smoke evidence including TreeItem command execution, mock-host VS Code WebviewView render-contract evidence, local rendered Control Center workbench screenshot evidence, local WebviewView command interaction evidence, release artifact file-list verification, release artifact hash/SBOM-style provenance, local release artifact reproducibility checks, trace-graded agent replay evals, source-controlled PR/push product-quality wiring, OpenSSF/SLSA local security posture evidence with configured CodeQL SAST workflow coverage, operator-authorized broader local CLI command-session trace capture, operator-authorized prompted local tool-loop trace capture, implementation-bearing single-file, multi-file, regression-cycle fixture code-editing trace capture, tool-interruption recovery trace capture, and protected-action denial trace capture, real local JSONL trace grading with coverage-gap classification, local trace schema contract validation, source-hash-addressed portable trace export, trace capture redaction policy, SWE-bench/OpenHands-style benchmark readiness mapping, explicit external benchmark protected-action boundary mapping, local benchmark manifest replay results, benchmark efficiency metric gap classification, SWE-bench-style benchmark submission readiness gap mapping, benchmark policy compliance and eligibility-claim blocking, trajectory process-quality classification, verification-report consistency checks, quality blocker taxonomy, public claim boundary scanning, default-false protected-action authorization packet evidence, source-hash-addressed product evidence manifest, and privacy verification. It does not mean the product is finished, REUSE-compliant, license-compliant, NOTICE-ready, externally validated, superior to the top 10 projects, or release-ready.
