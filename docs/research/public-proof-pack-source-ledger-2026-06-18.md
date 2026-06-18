# Research Ledger: Public Proof Pack Inputs

Date accessed: 2026-06-18
Status: source-first public-proof ledger

## Research Question

How should Metaforge update its public proof pack after adding research and eval
gates, without claiming production readiness, external validation, compliance,
autonomous reliability, or benchmark superiority?

## Sources Used

| Source | Type | Absorbed pattern | Boundary |
| --- | --- | --- | --- |
| [GitHub profile README docs](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme) | Official product docs | Treat the profile README as a public identity and project-routing surface. | It is not adoption, validation, or product-completion proof. |
| [GitHub README docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | Official product docs | README copy should explain what the project does, why it is useful, how to start, where to get help, and who maintains it. | README clarity is not production readiness. |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | Maintained OSS | Open-source posture should be expressed through repeatable checks, findings, and remediation queues. | Metaforge does not claim an OpenSSF Scorecard result in this pack. |
| [in-toto Attestation Framework](https://github.com/in-toto/attestation) | Open-source standard | Bind claims to subjects, predicates, and produced artifacts instead of narrative-only trust. | This pack is unsigned local documentation, not an in-toto attestation. |
| [SLSA Build Provenance](https://slsa.dev/spec/v1.2/build-provenance) | Standard | Separate source revision, generation process, and provenance claims. | No SLSA level, hosted provenance, or build attestation claim is made. |
| [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | Standard | Keep secure-development practice evidence distinct from compliance claims. | No SSDF compliance claim is made. |
| [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) | Paper | Public AI surfaces should state intended use, evaluation procedure, and limits. | Metaforge is not publishing a trained model card. |
| [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) | Paper | Proof packets should preserve motivation, composition, operating characteristics, and recommended uses. | This does not certify datasets or benchmarks. |
| [US11163858B2 client software attestation](https://patents.google.com/patent/US11163858B2/en) | Patent publication | Use pass/fail gate language instead of trusting self-report. | Prior-art vocabulary only, not legal clearance or implementation equivalence. |
| `docs/research/goal-os-governed-code-prior-art-2026-06-18.md` | Local authority | Primary-source research briefs now require source, local precedent, rejected-source, and claim-boundary records. | Local research gate only. |
| `docs/evals/autonomous-goal-os-minimal-checklist.md` | Local authority | Eval levels, automation candidates, side-effect arrays, and owner-side drift are separated before stronger claims. | Local no-provider eval governance only. |
| `docs/reports/mfh-meta-source-reconciliation-2026-06-18.md` | Local authority | Public docs, private harness status, owner-side claims, and blocked claim classes are reconciled explicitly. | Reconciliation report, not external validation. |

## Rejected Shortcuts

| Shortcut | Reason rejected |
| --- | --- |
| Treat workflow badges as proof of product quality | Badges show configured automation status only. |
| Treat a profile refresh as adoption evidence | Profile README is a routing surface, not social proof. |
| Treat local no-provider eval governance as live benchmark evidence | No live provider benchmark or external evaluator was run. |
| Claim standards compliance from standards-inspired structure | The standards informed structure only; no certification or conformance run exists. |
| Link private/local workbench or plugin repos directly | Live unauthenticated checks returned non-public/inaccessible surfaces, so profile/proof copy must use public-safe boundaries only. |

## Public Copy Rule

Use:

```text
Metaforge has local research/eval/proof gates that bind public claims to current
source-controlled evidence and explicit non-claims.
```

Not allowed:

```text
Not allowed: Metaforge is externally validated.
Not allowed: Metaforge is production-ready.
Not allowed: Metaforge is compliant with SLSA, NIST, SSDF, OpenSSF, or in-toto.
Not allowed: Mimesis Engineering universally improves AI output.
Not allowed: Private/local workbench repositories are public proof.
```
