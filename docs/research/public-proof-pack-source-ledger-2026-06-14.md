# Research Ledger: Public Proof Pack Inputs

Date accessed: 2026-06-14
Status: source ledger for Metaforge public marketing proof pack

## Question

How should Metaforge make a public marketing surface that is strong, discoverable, and credible without claiming production readiness, external validation, compliance, or benchmark superiority?

## Local Sources

| Source | Finding | Use |
| --- | --- | --- |
| `README.md` | Metaforge is already positioned as Meta/MFH/Orchestra OS on top of the OpenClaude runtime. | Keep marketing centered on Metaforge, not OpenClaude alone. |
| `docs/MIMESIS_ENGINEERING.md` | Mimesis is defined as structure extraction plus evidence gating. | Use as improvement-loop explanation. |
| `docs/profile/github-profile-refresh-evidence-2026-06-14.md` | Profile rewrite used current public repos and avoided private/inaccessible proof. | Use as current profile evidence. |
| `docs/product-quality/public-claim-boundary-report.md` | Local no-provider scan blocks unsupported public claims on configured surfaces. | Use as claim-boundary evidence. |
| `docs/product-quality/product-evidence-manifest.md` | Local evidence package can hash-bind reports and artifacts. | Use as proof-pack pattern without signed-attestation claims. |
| `<private-workspace>\CLAIMS.md` | Fresh local claim pack says verification is marketing, proof boundaries should stay visible, and source permission governs claims. | Use as the tone and maxims for public proof-pack copy. |
| `<private-mimesis-workbench>\mimesis-plugin\experts\frontier-visual-designer\MODULE.md` | Fresh local expert module asks whether structure still proves the proposition after copy is removed. | Use as a public-surface design test. |

## Primary Sources

| Source | URL | Pattern to absorb | Boundary |
| --- | --- | --- | --- |
| GitHub profile README docs | https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme | Profile README is a public repository README rendered on the profile when repository and README conditions are met. | Profile presence is not usage, quality, or adoption proof. |
| GitHub README docs | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes | A README should explain what the project does, why it is useful, how to start, where to get help, and who maintains it. | README structure is marketing clarity, not production proof. |
| GitHub repository topics docs | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics | Topics help people find and classify projects by purpose, subject, affinity, and language. | Topics are discoverability metadata, not validation. |
| OpenSSF Scorecard | https://github.com/ossf/scorecard | Security posture becomes stronger when checks are explicit and repeatable. | Do not claim a Scorecard result without actually running Scorecard. |
| NIST AI Risk Management Framework | https://www.nist.gov/itl/ai-risk-management-framework | Public AI risk language should stay attached to concrete govern/map/measure/manage-style controls and evidence. | Framework-inspired control language is not NIST compliance. |
| Model Cards for Model Reporting | https://arxiv.org/abs/1810.03993 | Public AI/system reports should disclose intended use, evaluation procedures, and limitations. | This source supports transparency structure, not model-performance claims. |
| Datasheets for Datasets | https://arxiv.org/abs/1803.09010 | Public proof artifacts should document motivation, composition, operating characteristics, tests, and recommended use. | This source supports documentation structure, not dataset certification. |
| in-toto Attestation Framework | https://github.com/in-toto/attestation | Evidence can be structured as verifiable claims about how software is produced. | Metaforge proof packs are not signed attestations unless an attestation flow is actually implemented. |
| OpenSSF OSPS Baseline | https://baseline.openssf.org/versions/2026-02-19.html | Security maturity can be expressed as controls by level and category. | No OSPS conformance claim without a control-by-control assessment. |
| US11163858B2 client software attestation | https://patents.google.com/patent/US11163858B2/en | Treat pass/fail attestation as a behavior gate instead of trusting self-report. | Patent publication is prior-art vocabulary only; no legal clearance or implementation-equivalence claim. |

## Decision Impact

1. Add a public proof pack that separates what can be said from what cannot be said.
2. Link the proof pack from README so marketing copy points to evidence.
3. Add the proof pack to local link/claim scans so it stays bounded.
4. Use GitHub topics to improve repo discoverability while avoiding validation claims.
5. Treat open PRs and visible remote branches as public staging surfaces that must not be used for marketing unless they pass the same hygiene and claim-boundary checks as `main`.
