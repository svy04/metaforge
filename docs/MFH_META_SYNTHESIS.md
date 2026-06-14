# MFH / Meta Synthesis For Autonomous Goal OS

Status: planning update after reading harness-engineering workspace
Date: 2026-05-10

## Local Sources Read

Harness workspace:

- `<private-workspace>\MASTER_SPEC.md`
- `<private-workspace>\NARROW_SPEC.md`
- `<private-workspace>\POSITIONING_BRIEF.md`
- `<private-workspace>\meta\CLAUDE.md`
- `<private-workspace>\meta\SPEC.md`
- `<private-workspace>\meta\decisions\2026-05-05-2388-governed-code-problem-definition.md`
- `<private-workspace>\mfh\README.md`
- `<private-workspace>\mfh\.mfh\spec.md`
- `<private-workspace>\mfh\.mfh\plan.md`
- `<private-workspace>\mfh\.mfh\status.md`
- `<private-workspace>\mfh\.mfh\cascade_log.txt`
- `<private-workspace>\mfh\docs\reports\2026-05-09-candidate-m-closure.md`

Live probe:

```powershell
python meta\scripts\source_reconciler.py
```

Result: exit 1, `DRIFT`; current mfh branch has 9 modified and 3 untracked files, while `.mfh/status.md` says `awaiting user adjudication`.

## Synthesis

The earlier planning package treated `mth` as a provisional Mission-to-Harness layer because the OpenClaude repo had no definition. The harness-engineering workspace clarifies the real component: **MFH**, not `mth`, is the governed-code Operating Gate. Future references should treat `mth` as an unresolved spelling/alias unless the owner defines it separately.

### Meta

Meta is the operator OS and Constitution layer.

It defines:

- the North Star: overcome both AI limits and human operator limits so products can be built without requiring the owner to be a CTO;
- the operator boundary: the human supplies ideas, taste, user sense, and strategic/product decisions, not technical stack or architecture decisions;
- the decision ledger, LLM Wiki substrate, raw immutable source storage, digest, inbox, and file-based agent communication rules;
- the escalation boundary for irreversible actions, credentials, deployment, payment, public communication, and unresolved taste/product choices.

For Autonomous Goal OS, Meta is the **governance memory substrate**: decisions, source ledgers, raw notes, wiki pages, and operator-boundary rules.

### MFH

MFH is governed-code, not no-code and not another coding agent.

It is a Claude Code Operating Gate that turns product intent, risk, verification, and release claims into evidence-backed approval gates. Its own principle is: "measured judgment only; compose existing components; write down what cannot be solved."

For Autonomous Goal OS, MFH is the **control and evidence gate**:

- goal drift, false completion, state integrity, scope drift, content pollution, hallucinated APIs, weak benchmarks, and session-anchor failures are treated as candidate-detected failure modes;
- self-report is not enough; external measurement, ledger entries, closure reports, and source reconciliation are required;
- closure markers are not authoritative unless closure reality and evidence gates agree.

### Orchestra OS

Orchestra OS remains the multi-agent execution and challenge layer in OpenClaude.

Its role is not to replace Meta or MFH:

- Meta governs operator boundaries and long-term memory.
- MFH judges whether execution claims are honest and evidence-backed.
- Orchestra OS routes planner, skeptic, shadow, cross-review, evidence arbiter, promotion store, and human gate behavior.

### Candidate M Import

Candidate M is directly relevant to Autonomous Goal OS. It introduces a three-layer vision anchor:

- project vision;
- topic/program vision;
- today's local objective.

It also introduces a deterministic state-machine framing:

```text
Pending -> Active -> Verifying -> Closed
                    \-> Failed -> Active
```

This should become the default lifecycle for Autonomous Goal OS goals. A goal is not closed just because an agent says it is done; it closes only after verification artifacts, dirty-state attribution, reports, and evidence gates are recorded.

## Updated Architecture

```text
Meta Constitution / Wiki / Decisions
    owns operator boundaries, durable memory, raw sources, decisions
        |
Goal Kernel
    owns hierarchy, schema, checkpoints, pause/rollback, validation commands
        |
Orchestra OS
    owns multi-agent planning, critique, implementation routing, shadow review
        |
MFH Operating Gate
    owns evidence, closure, source reconciliation, claim boundaries
        |
Evals / Reports / Next Goals
    decide revise, pause, close, promote to Skill, propose Automation
```

## Planning Implications

1. Rename the role from provisional `mth` to canonical `mfh` where possible, while leaving a decision-log note for the unresolved original spelling.
2. Treat "governed-code" as the product category for the unified system.
3. Treat "no-use completion" and claim boundaries as first-class planning controls: internal substrate proof is not the same as external user-success validation.
4. Use Meta's raw/wiki/decision pattern as the research and memory model.
5. Use MFH source reconciliation and closure reality checks as examples for future Goal OS evals.
6. Keep the operator out of technical bottlenecks, but keep explicit approval gates for irreversible or product/taste decisions.
7. Do not claim harness-engineering is currently green: the live source reconciler reported drift in the mfh working tree.

## Immediate Changes To OpenClaude Plan

- `docs/PROJECT_SPEC.md`: revise role definitions around Meta, MFH, and Orchestra OS.
- `docs/GOAL_SCHEMA.md`: add MFH-style evidence, claim-boundary, and state-machine fields.
- `docs/AGENT_REGISTRY.md`: add Meta and MFH as governance/evidence systems distinct from agent roles.
- `docs/RESEARCH_PIPELINE.md`: add Meta raw/wiki/decision flow.
- `docs/EVALS.md`: add source reconciliation and closure reality checks.
- `docs/SECURITY_AND_GUARDRAILS.md`: import governed-code approval boundaries.
- `docs/ROADMAP.md` and `docs/NEXT_GOALS.md`: make the next goals integrate actual MFH/Meta evidence instead of starting from a blank Goal OS.
