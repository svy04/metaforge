# Next Goals

Status: active

Run these as the next three executable Codex `/goal` commands.

## 1. Goal Kernel MVP With MFH/Meta Gates

```text
/goal Implement the Autonomous Goal OS Goal Kernel MVP with MFH/Meta governed-code gates.

Read first:
- AGENTS.md
- docs/PROJECT_SPEC.md
- docs/GOAL_SCHEMA.md
- docs/MFH_META_SYNTHESIS.md
- docs/ROADMAP.md
- docs/EVALS.md
- package.json

Objective:
Create a machine-checkable goal registry for the Autonomous Goal OS without changing provider/auth/runtime behavior, and include Meta operator-boundary fields plus MFH claim/evidence-gate fields.

Deliverables:
- Create docs/goals/README.md.
- Create docs/goals/CG-001-goal-kernel-mvp.md using the schema in docs/GOAL_SCHEMA.md.
- Add scripts/validate-goals.ts or the smallest repo-native validator that checks required goal fields.
- Add a package.json script if appropriate, such as "goals:validate".
- Update docs/PROGRESS_LOG.md and docs/DECISION_LOG.md.

Requirements:
- Validate id, level, parent, objective, non-goals, success criteria, validation commands, checkpoints, pause conditions, rollback strategy, research requirements, governed-code claim level, claim boundary, authority sources, and MFH/Meta gate flags.
- Keep the validator docs-focused and narrow.
- Do not add external dependencies unless already present or clearly necessary.
- Do not create automations.

Validation:
- Run the new goal validator.
- Run bun run build.
- Run focused tests if code touches shared runtime.

Stopping condition:
Stop only when one real goal file validates, MFH/Meta gate fields are checked, failures are documented, and the next goal candidate is recorded.
```

## 2. Meta-Style Primary-Source Research Ledger

```text
/goal Implement the Autonomous Goal OS primary-source research ledger using the Meta raw/wiki/decision pattern.

Read first:
- AGENTS.md
- docs/RESEARCH_PIPELINE.md
- docs/PROJECT_SPEC.md
- docs/MFH_META_SYNTHESIS.md
- docs/DECISION_LOG.md
- docs/GOAL_SCHEMA.md

Objective:
Make research claims auditable by adding a reusable research brief format and one completed brief that connects Goal OS prior art to the local MFH/Meta governed-code work.

Deliverables:
- Create docs/research/README.md.
- Create docs/research/templates/primary-source-brief.md.
- Create docs/research/goal-os-governed-code-prior-art-2026-05-10.md or current-date equivalent.
- Update docs/DECISION_LOG.md with any decisions changed by research.
- Update docs/PROGRESS_LOG.md.

Requirements:
- Use primary sources only as final evidence: local code, official docs, original repos, papers, standards, patents.
- Include rejected blog-only sources if any were encountered.
- Cover at least local MFH/Meta authority docs, AGENTS.md, Agent Skills, MCP, OpenAI agent evals/trace grading, W3C PROV, NIST AI RMF, OWASP LLM Top 10, ReAct, Reflexion, and USPTO Patent Public Search.
- Map each finding to a requirement, eval, guardrail, or decision.

Validation:
- Run a docs consistency check that confirms every source URL appears in the source ledger.
- Run bun run build if repo sanity check is desired.

Stopping condition:
Stop only when the research brief exists, each major claim has a source or decision-log entry, and follow-up implementation goals are proposed.
```

## 3. Eval Flywheel, Source Reconciliation, And Automation Candidates

```text
/goal Build the first Autonomous Goal OS eval flywheel with MFH-style source reconciliation and automation-candidate report.

Read first:
- AGENTS.md
- docs/EVALS.md
- docs/SECURITY_AND_GUARDRAILS.md
- docs/MFH_META_SYNTHESIS.md
- docs/ROADMAP.md
- docs/AGENT_REGISTRY.md
- scripts/orchestra-experiment-runner.ts
- src/services/orchestra/experimentMetrics.ts

Objective:
Turn the planning package into a repeatable eval loop, record current MFH/Meta source-reconciliation status, and identify safe read-only automation candidates without creating automations yet.

Deliverables:
- Create docs/evals/README.md.
- Create docs/evals/autonomous-goal-os-minimal-checklist.md.
- Create docs/reports/automation-candidates-2026-05-10.md or current-date equivalent.
- Create docs/reports/mfh-meta-source-reconciliation-2026-05-10.md or current-date equivalent.
- Run scripts/orchestra-experiment-runner.ts and record whether the run used mock or real tasks.
- Update docs/PROGRESS_LOG.md and docs/DECISION_LOG.md.

Requirements:
- Include eval levels L0-L5 from docs/EVALS.md.
- Include EVAL-008 through EVAL-010 from docs/EVALS.md.
- Include a table of candidate automations with tier, trigger, schedule, permissions, output path, pause condition, and required approvals.
- Mark all automations as proposed only; do not schedule or create them.
- If a candidate needs external calls, mark it blocked until owner approval.

Validation:
- Run bun run scripts/orchestra-experiment-runner.ts.
- From <private-workspace>\scripts\source_reconciler.py and record pass/drift without editing that workspace.
- Run bun run build.
- If tests are practical, run focused Orchestra tests for experimentMetrics and promotion gates.

Stopping condition:
Stop only when the eval checklist and automation-candidate report exist, evidence is recorded, and no live automation has been created.
```
