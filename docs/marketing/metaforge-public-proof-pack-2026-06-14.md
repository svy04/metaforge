# Metaforge Public Proof Pack

Date: 2026-06-14
Status: public-facing, proof-bounded marketing aid

## One-Line Position

Metaforge is a Meta/MFH/Orchestra operating system that turns owner intent into evidence-gated agent work, with OpenClaude as the local CLI runtime and Mimesis Engineering as the source-first improvement loop.

## Short Pitch

Metaforge is not another coding-agent wrapper. It is an operating layer for governed agent execution:

- **Meta** keeps operating memory, source ledgers, decisions, and boundaries.
- **MFH** blocks closure until claims have evidence.
- **Orchestra** routes work across scouts, planners, skeptics, implementers, reviewers, and human gates.
- **OpenClaude** supplies the local CLI, provider routes, MCP/tool surfaces, and Claude/Codex credential paths.
- **Mimesis Engineering** imports the load-bearing structure of proven products, papers, patents, standards, and repositories, then keeps only what survives local verification.

## Current Proof Level

The current public proof level is:

```text
local no-provider product-quality evidence + public repository/profile positioning + proof-bounded source ledgers
```

This means Metaforge can currently market:

- the Meta/MFH/Orchestra architecture as the project direction;
- the OpenClaude runtime as the local CLI substrate;
- Mimesis Engineering as an active operating frame;
- local product-quality gates and evidence reports;
- GitHub profile/repo surfaces that link to current public repos;
- claim boundaries that prevent unsupported release, production, compliance, external-validation, or superiority claims.

This does not yet prove hosted deployment, public adoption, production readiness, external validation, compliance, autonomous reliability, or benchmark superiority.

## Metaforge Proof Tour

Use this tour when turning the architecture into public copy:

1. **Goal Kernel** turns owner intent into `CG-*.md` goals with scope, success criteria, validation commands, rollback, evidence, and MFH/Meta fields.
2. **Meta** keeps authority sources, decision-ledger links, raw source records, and memory/wiki boundaries attached to the goal.
3. **MFH** blocks premature closure: `scripts/validate-goals.ts` rejects `validated` or `closed` states without passing command evidence, and `scripts/validate-goal-traces.ts` grades the ordered closure trace.
4. **Orchestra** is the runtime-wired layer where current `src/services/orchestra/` behavior and product-quality reports support routing claims.
5. **Mimesis Engineering** absorbs proven structures from trace, policy, eval, risk, OSS, paper, patent, and standards sources.
6. **OpenClaude** remains the CLI/runtime substrate for terminal tools, provider routes, MCP, slash commands, streaming, and credential surfaces.

Current proof route: [README proof tour](../../README.md#metaforge-proof-tour), [goal trace validation report](../product-quality/goal-trace-validation-report.md), and `bun run goals:validate`.

## Wiring Evidence Map

Use this map before turning architecture language into public copy.
The generated [Public claim evidence map](../product-quality/public-claim-boundary-report.md#public-claim-evidence-map) is the source-bound version: it binds each public symbol to allowed claims, explicit non-claims, local evidence paths, and unresolved gaps.

| Surface | Evidence class | Public wording allowed | Boundary |
| --- | --- | --- | --- |
| OpenClaude terminal UX, tools, MCP, slash commands, provider routes, streaming, and credential surfaces | Runtime import | "OpenClaude is the local CLI runtime substrate Metaforge rides on." | Do not make OpenClaude the main public thesis or call this a Metaforge release artifact. |
| Orchestra routing and planner/skeptic/reviewer roles where tied to current `src/` behavior | Runtime import | "Orchestra is the runtime-wired layer in this package today." | Do not imply every named operating layer is a runtime module. |
| Meta, MFH, Goal Kernel, evidence gates, claim-boundary rules, schemas, and reports | Governance/docs/gates | "Meta/MFH are governance, schema, and evidence-gate surfaces." | Do not describe Meta or MFH as separate default runtime imports in this checkout. |
| Mimesis Engineering source-first loop, source ledgers, and absorbed patterns | Governance/docs/gates | "Mimesis Engineering is the source-first improvement loop." | Public proof is docs/source ledgers plus local verification, not external validation. |
| Local no-provider gates, product-quality reports, privacy scans, proof pack, and profile refresh evidence | Local no-provider proof boundary | "Local gates currently bound what the public surface may claim." | Local proof is not hosted deployment, adoption, production readiness, or benchmark evidence. |
| AVF Influence Factory, generated operator runs, and `avf/` plus validator artifacts | Manual artifact lane | "AVF Influence Factory is a repo-local manual artifact lane." | It is not a default CLI runtime import or CI execution path; generated outputs stay ignored. |

## Evidence Cards

| Claim | Current evidence | What it proves | What it does not prove |
| --- | --- | --- | --- |
| Metaforge is centered on Meta/MFH/Orchestra, not OpenClaude alone. | [README.md](../../README.md), [docs/PROJECT_SPEC.md](../PROJECT_SPEC.md), [docs/MFH_META_SYNTHESIS.md](../MFH_META_SYNTHESIS.md), [docs/AGENT_REGISTRY.md](../AGENT_REGISTRY.md) | Current repository positioning and operating architecture. | Runtime completeness or external adoption. |
| Goal Kernel closure now has local trace-policy evidence. | [goal trace validation report](../product-quality/goal-trace-validation-report.md), [CG-001 trace fixture](../goals/traces/CG-001-goal-kernel-mvp.trace.json), command: `bun run goals:validate` | A current goal trace is checked for loaded, checkpoint, validation, claim-review, validated ordering and no provider/live/external/protected side effects. | It is not live provider execution, external validation, production readiness, or autonomous reliability. |
| Mimesis Engineering is an active improvement loop. | [docs/MIMESIS_ENGINEERING.md](../MIMESIS_ENGINEERING.md), [source ledger](../research/mimesis-engineering-source-ledger-2026-06-14.md), [public proof-pack source ledger](../research/public-proof-pack-source-ledger-2026-06-14.md) | Current method, source-first operating rules, and absorbed source patterns. | Does not prove that Mimesis always improves output or is externally validated. |
| Public profile was refreshed from current repo evidence. | [GitHub profile refresh evidence](../profile/github-profile-refresh-evidence-2026-06-14.md), [svy04 profile](https://github.com/svy04) | The profile surface was rebuilt around current public repos and claim boundaries. | It does not prove that unpublished pre-public artifacts are public or stable. |
| Public claims are scanned locally. | [public claim boundary report](../product-quality/public-claim-boundary-report.md), command: `bun run product:public-claim-boundary` | Configured public surfaces contain no detected unauthorized positive readiness/superiority claims. | It does not fetch external pages or certify marketing truth. |
| Remote GitHub public surfaces are audited. | [GitHub remote surface audit report](../product-quality/github-remote-surface-audit-report.md), command: `bun run product:github-remote-surface-audit` | Remote branches and same-repo open PR heads are inventoried and scanned for configured local-path, token-shaped, and browser-capture blockers. | It is not a full-history secret-scanning alert review or credential-validity certification. |
| Privacy boundaries are checked locally. | command: `bun run verify:privacy` | Built CLI bundle is scanned for configured phone-home patterns. | It does not prove third-party provider behavior or hosted privacy. |
| Evidence can be packaged as a local manifest. | [product evidence manifest](../product-quality/product-evidence-manifest.md), command: `bun run product:evidence-manifest` | Local reports/artifacts/workflows can be hash-bound into a manifest. | It is not a signed in-toto/SLSA attestation. |
| Community surface has local quality evidence. | [community profile quality report](../product-quality/community-profile-quality-report.md), command: `bun run product:community-profile-quality` | Core community files and README links are present locally. | It is not a hosted GitHub community-profile certification. |
| Local docs links are checked. | [doc link integrity report](../product-quality/doc-link-integrity-report.md), command: `bun run product:doc-link-integrity` | Configured repository-local Markdown links resolve. | It does not verify all external URLs. |

## Remote GitHub Surface Card

Marketing does not start only at `README.md`. The public surface includes the default branch, profile README, open PRs, visible branches, workflow badges, and proof routes.

| Surface | Current operating rule | Evidence to check before reuse | Boundary |
| --- | --- | --- | --- |
| Default repo branch | Treat `main` as the canonical public story. | `git status -sb`, `git grep` for local/private patterns, `bun run product:public-artifact-hygiene`, `bun run product:public-claim-boundary` | A clean local checkout is not proof that every remote branch is clean. |
| GitHub profile | Treat the profile README as a routing surface, not a broad validation claim. | Profile README workflow, live link check, claim-boundary phrases, current public repo links | A profile README does not prove adoption, production readiness, or external validation. |
| Open PRs | Treat open PRs as public staging surfaces. | `gh pr list`, `gh pr checks <number>`, and branch-scoped public-artifact scans when the PR changes public copy or generated reports | A PR body or green local run is not a merge/readiness claim. |
| Visible branches | Keep stale public branches out of the proof path. | `git ls-remote --heads origin` plus branch-targeted scans for local paths, unpublished workbench names, and token-shaped strings | Branch presence is not proof that the branch should be marketed. |
| Proof routes | Link only artifacts that carry explicit claim boundaries. | Source ledger, proof pack, model/system card, public claim boundary report | Public proof routes remain bounded unless external validation actually happens. |

Reusable public line:

```text
Metaforge markets only what the current GitHub surface can prove: default-branch docs, profile routes, open PR state, local no-provider gates, and explicit non-claims.
```

Do not reuse copy from a branch, PR, generated report, or unpublished workbench unless it passes the same public-surface scan as `main`.

## Source Absorption

| Source class | Source | Absorbed structure | Boundary |
| --- | --- | --- | --- |
| Official product docs | [GitHub profile README docs](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme) | A profile README is a public repo README rendered on the profile when naming, visibility, and root `README.md` conditions hold. | A profile README is a profile surface, not adoption proof. |
| Official product docs | [GitHub README docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | A repository README should help people understand what the project does, why it is useful, how to start, where to get help, and who maintains it. | README clarity is not proof of product readiness. |
| Official product docs | [GitHub repository topics docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) | Topics improve discoverability by classifying repos by purpose, subject, affinity, or language. | Topics do not prove quality or usage. |
| Open-source project | [OpenSSF Scorecard](https://github.com/ossf/scorecard) | Security/quality posture should be expressed as explicit checks with scores, risks, and remediation. | A local report is not an OpenSSF Scorecard result unless Scorecard is actually run. |
| Official product docs | [GitHub REST Pull Requests API](https://docs.github.com/en/rest/pulls/pulls) | Open PR heads are public review surfaces and should be inventoried before claiming a repo is clean. | PR metadata scanning is not proof that every fork or historical object is clean. |
| Official tool docs | [Git `ls-remote`](https://git-scm.com/docs/git-ls-remote) | Remote branch refs should be listed by ref name and object ID instead of inferred from the local default branch. | Remote ref inventory is not full-history secret scanning. |
| Official product docs | [GitHub Secret Scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning) | Secret hygiene claims should distinguish local tree scans from hosted full-history secret scanning and alert status. | No GitHub alert status claim is made by the local audit. |
| Tool docs | [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer) | Browser traces, network logs, videos, screenshots, and DOM snapshots are data-bearing artifacts. | Blocking accidental artifacts is not a statement that all browser evidence is publishable. |
| Security reference | [OWASP Full Path Disclosure](https://owasp.org/www-community/attacks/Full_Path_Disclosure) | Absolute local paths should be treated as privacy/security disclosures on public surfaces. | Path-disclosure scanning is not a complete security audit. |
| Standard | [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | Risk language should be tied to govern/map/measure/manage-style controls and evidence, not broad safety claims. | NIST alignment language is not a compliance claim. |
| Open-source standard | [OpenTelemetry](https://opentelemetry.io/) | Ordered trace-style evidence can preserve event sequence and boundary metadata before stronger observability claims. | The Goal Kernel trace gate is not an OpenTelemetry compliance claim. |
| Open-source project | [Open Policy Agent](https://www.openpolicyagent.org/docs) | Structured policy decisions are stronger than prose-only closure claims. | Metaforge does not embed OPA in this slice. |
| Official product docs | [OpenAI Agent Evals](https://developers.openai.com/api/docs/guides/agent-evals) and [Trace Grading](https://developers.openai.com/api/docs/guides/trace-grading) | Agent workflow quality should be evaluated through traces, graders, datasets, and repeatable evals. | Local trace validation is not an OpenAI hosted eval run. |
| Paper | [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) | Public AI surfaces should disclose intended use, evaluation procedure, and limits. | Metaforge is not publishing a trained model card from this document. |
| Paper | [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) | Proof packets should expose motivation, composition, operating characteristics, test results, and recommended uses. | This does not certify datasets or benchmarks. |
| Standard / OSS spec | [in-toto Attestation Framework](https://github.com/in-toto/attestation) | Evidence should be structured as verifiable claims about software production. | This pack is unsigned and local unless real attestations are generated. |
| Standard | [OpenSSF OSPS Baseline](https://baseline.openssf.org/versions/2026-02-19.html) | Security maturity can be expressed as controls organized by category and level. | No OSPS conformance claim is made. |
| Patent publication | [US11163858B2 client software attestation](https://patents.google.com/patent/US11163858B2/en) | Gate behavior on pass/fail attestation instead of trusting self-report. | Patent reference is prior-art vocabulary only, not legal clearance or implementation equivalence. |

## Copy Blocks

### Operating Maxims

- Verification is the marketing.
- Put the proof boundary on the same screen as the claim.
- Claim only what the source and the local gate allow.
- If copy is removed, the structure should still prove the point.

### GitHub Profile Line

Building **Metaforge**: a Meta/MFH/Orchestra OS for evidence-gated agent work, with OpenClaude as runtime substrate and Mimesis Engineering as the source-first loop.

### Repo Description

Meta/MFH/Orchestra OS with evidence gates, Mimesis Engineering loops, and OpenClaude runtime substrate for Claude/Codex routes.

### Short Social Post

Metaforge is my attempt to stop treating agent output as magic. Meta keeps memory, Orchestra routes work, MFH forces evidence, and the Goal Kernel now has a local trace-policy gate before stronger claims survive.

### Conservative CTA

Start with the README, then read the proof pack and claim-boundary reports before trusting the story.

## Do Not Say Yet

- Do not say Metaforge is production-ready.
- Do not say it is externally validated.
- Do not claim SLSA, OSPS, NIST, OAuth, or in-toto compliance.
- Do not claim hosted deployment or public adoption.
- Do not claim autonomous reliability.
- Do not claim it beats other agent systems.
- Do not market unpublished workbench repositories as public proof.

## Verification Routine

Before reusing this copy outside the repository:

1. Keep this proof pack in the configured public-claim and link-integrity scans.
2. Keep GitHub topics aligned with the public repo purpose.
3. Re-run local no-provider gates.
4. Run `bun run product:github-remote-surface-audit` before claiming the GitHub surface is clean.
5. Read back the remote README/profile surfaces after push.
6. Only then reuse the copy blocks above.
