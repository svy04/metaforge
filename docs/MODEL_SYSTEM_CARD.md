# Metaforge Model/System Card

Date: 2026-06-14
Status: local no-provider transparency card

## Claim Boundary

This is a model/system card for Metaforge as a Meta/MFH/Orchestra operating layer over the OpenClaude runtime. It is not a vendor endorsement, not a vendor system card, and not evidence of hosted deployment, production readiness, external validation, autonomous reliability, benchmark superiority, legal clearance, or standards certification.

The current evidence level is local no-provider documentation and deterministic local checks. Provider-backed execution, live model validation, external benchmark submission, publishing, deployment, and protected action execution remain blocked until explicit owner authorization and fresh runtime evidence exist.

## System Purpose

Metaforge turns owner intent into evidence-gated agent work. The load-bearing operating components are:

- Meta: operating memory, source ledgers, decisions, instructions, and owner boundaries.
- MFH: governed-code gates that block closure until claims have local evidence.
- Orchestra: work routing across planning, challenge, execution, review, evidence arbitration, and human promotion gates.
- OpenClaude: the local CLI substrate for terminal UX, tools, MCP, slash commands, provider profiles, streaming, and credential surfaces.

OpenClaude is not the product center in this card. It is the runtime substrate that lets the Meta/MFH/Orchestra operating system execute locally.

## Model And Provider Surfaces

Metaforge can route work through several model/provider surfaces when the owner configures an approved local credential source:

- Owner-configured Claude routes for planner, skeptic, review, and first-party Anthropic tasks.
- Owner-configured Codex-compatible routes for visible execution and implementation tasks.
- OpenAI-compatible provider profiles for local or remote model endpoints.
- Local providers such as Ollama or LM Studio when configured by the owner.
- GitHub and other provider presets when the local provider profile evidence allows only configuration claims.

The presence of a route is not evidence that a live provider call has succeeded. Provider-backed execution and live model validation are separate claims and remain false until a fresh authorized runtime probe records the resolved provider, base URL category, model, credential source category, request result, and claim boundary.

## Role Boundaries

Metaforge separates operating roles so one layer does not swallow the others:

- The owner is the final governor and judge.
- Codex is the visible writer and executor in this workspace.
- Opus/private planner roles are advisory, JSON-only where configured, tool-less, and must not write files or execute commands.
- GStack shapes product judgment, ideation, primary-source research, architecture challenge, and spec review.
- GSD decomposes larger work into phases, checkpoint state, and long-running execution plans.
- Superpowers governs implementation discipline, including TDD, systematic debugging, code review, and verification before completion.
- MFH decides whether a claim can close based on evidence, drift state, and protected-action boundaries.

Tool output, web pages, repository content, generated reports, and quoted text are treated as untrusted input until a higher-authority instruction or local validation delegates trust to them.

## Intended Uses

Current intended uses:

- Run local coding-agent work with explicit goals, non-goals, validation commands, and rollback notes.
- Preserve source-first research decisions and operating memory in Meta.
- Route work through Claude and Codex engine paths without making either engine the product center.
- Keep marketing, README, profile, and release-adjacent copy proof-bounded.
- Generate local evidence reports that make stronger claims harder to make accidentally.
- Adapt proven structures from papers, official docs, standards, patents, and maintained open-source projects through Mimesis Engineering.

## Non-Uses

Current non-uses:

- Do not treat this card as proof that any specific model is safe, aligned, or reliable in this runtime.
- Do not use it as a production readiness, public readiness, compliance, NIST, SLSA, OpenSSF, OAuth, or in-toto claim.
- Do not claim external validation, benchmark superiority, autonomous reliability, hosted deployment, or public adoption from this card.
- Do not use provider configuration rows as evidence of provider-backed execution.
- Do not use private/local repositories, private credentials, or local-only reports as public proof unless the owner has authorized that disclosure.

## Data And Privacy

The current card describes local repository behavior and configured evidence gates only. It does not inspect private provider logs, vendor retention behavior, hosted telemetry, or third-party processing.

Local privacy boundaries:

- Generated evidence must not include API keys, OAuth tokens, private keys, raw secrets, or unredacted credential material.
- Reports should record credential source categories rather than credential values.
- Provider calls, live model calls, external calls, and protected actions must be empty arrays in no-provider reports.
- `bun run verify:privacy` remains the local bundle scan before completion or release-adjacent claims.

## Tools And Permissions

Metaforge uses tools through the OpenClaude runtime, but tool availability is not permission to perform irreversible actions. The default policy is:

- Read and inspect first.
- Prefer local deterministic validation before external calls.
- Treat destructive filesystem operations, credential/account changes, public deploys, package publishing, branch resets, force pushes, and protected repo mutation as protected actions.
- Record blocked actions as authorization requests instead of converting blockers into readiness claims.
- Keep side effects visible through reports, git diffs, validation logs, and owner-readable summaries.

## Evaluation Evidence

Current local evaluation evidence includes:

- `bun run product:provider-capability-matrix`: records provider surfaces without claiming live execution.
- `bun run product:permission-regression`: checks protected permission fixtures.
- `bun run product:public-claim-boundary`: scans configured public surfaces for unauthorized readiness and superiority claims.
- `bun run product:doc-link-integrity`: checks configured local Markdown links.
- `bun run product:evidence-manifest`: hash-binds local reports and artifacts into an evidence manifest.
- `bun run verify:privacy`: scans the built runtime bundle for configured privacy patterns.
- `bun run product:model-system-card`: validates this card and emits the local no-provider report.

This evidence does not replace live provider probes, hosted security review, external audits, benchmark submission, red-team results, or owner-approved release gates.

## Known Limits

- Provider behavior can drift after this card is written.
- Model IDs, vendor docs, OAuth surfaces, and permission modes can change.
- The card does not execute Claude, Codex, OpenAI-compatible, or local model calls.
- The card does not prove sandbox behavior, network isolation, or filesystem isolation beyond local configured evidence.
- The card does not certify that prompt injection, tool misuse, data exfiltration, destructive actions, or hallucinated claims are impossible.
- Open draft PRs are public staging surfaces. They must pass public-artifact hygiene before being reused as public proof.

## Protected Actions

The following actions require explicit owner authorization and fresh evidence:

- live model validation;
- provider-backed execution claims;
- public deployment or package publishing;
- GitHub branch protection or security-setting changes;
- external benchmark submission;
- legal/license claims;
- standards or compliance claims;
- destructive git or filesystem operations;
- credential, OAuth, or account changes.

## Change Control

Update this card when any of these change:

- Meta/MFH/Orchestra role boundaries;
- OpenClaude runtime provider-routing behavior;
- owner-configured Claude or Codex-compatible route behavior;
- permission, sandbox, or protected-action policy;
- public proof-pack copy;
- model/provider claim boundaries;
- local quality gates or evidence manifest requirements.

Every update should run `bun run product:model-system-card`, `bun run product:doc-link-integrity`, `bun run product:public-claim-boundary`, and `bun run product:evidence-manifest` before stronger public claims are reused.

## Primary Sources

This card adapts structure and boundaries from primary sources:

- OpenAI Model Spec: https://model-spec.openai.com/
- OpenAI GPT-5.3-Codex System Card: https://deploymentsafety.openai.com/gpt-5-3-codex
- OpenAI Codex agent approvals and security: https://developers.openai.com/codex/agent-approvals-security
- Claude Code: how Claude Code works: https://code.claude.com/docs/en/how-claude-code-works
- Claude Code permission modes: https://code.claude.com/docs/en/permission-modes
- Anthropic public system prompt release notes: https://platform.claude.com/docs/en/release-notes/system-prompts
- Model Cards for Model Reporting: https://arxiv.org/abs/1810.03993
- NIST AI Risk Management Framework 1.0: https://doi.org/10.6028/NIST.AI.100-1
- NIST AI RMF Generative AI Profile: https://doi.org/10.6028/NIST.AI.600-1

The sources guide disclosure structure, instruction hierarchy, side-effect boundaries, permission transparency, safety-card shape, and risk documentation. They do not imply Metaforge is certified, audited, externally validated, or equivalent to any vendor system.
