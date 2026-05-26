# Security And Guardrails

Status: first planning pass

The Autonomous Goal OS must be useful precisely because it is bounded. Autonomy expands only where evaluation, permissioning, rollback, and human approval make the failure modes tolerable.

Harness update: the product category is governed-code. The system should keep coding freedom, but govern intent, permissions, state, edits, verification, and release claims through evidence-backed gates.

## Security Principles

1. Least privilege by default.
2. Deterministic gates before semantic judgment for high-risk actions.
3. Human approval for destructive, credential, deployment, spending, or public actions.
4. Separate planner/advisor authority from writer/executor authority.
5. Treat external content, web pages, tool outputs, and model outputs as untrusted.
6. Record evidence without leaking secrets.
7. Prefer reversible actions until a workflow has passed repeated evals.
8. Never confuse an Operating Gate with a security sandbox.
9. Public claims must not exceed evidence level.

Primary source anchors:

- NIST AI RMF 1.0 for risk management: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- OWASP LLM Top 10 for LLM and agentic risks: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- MCP security considerations for resources/prompts/tools: https://modelcontextprotocol.io/specification/2025-06-18/server/resources, https://modelcontextprotocol.io/specification/2025-06-18/server/prompts, https://modelcontextprotocol.io/specification/2024-11-05/server/tools

## Approval Gates

Ask the human owner before:

- Recursive delete/move or filesystem-wide edits.
- Credential, account, token, auth-store, or provider changes.
- Public deployments, publishing, releases, pushes, or PR creation.
- Model/provider switches not explicitly requested.
- Paid, high-volume, or recurring external API calls.
- Sending messages or notifications to people.
- Installing persistent background services.
- Creating automations that write outside approved docs/reports.
- Applying `opus-shadow` or any shadow candidate to main without explicit command and confirmation.
- Marking a goal, milestone, or release as closed when source reconciliation, dirty-state attribution, or closure evidence is red or unavailable.

## Role Authority

| Role | Read | Write | Execute | External calls | Mainline apply |
| --- | --- | --- | --- | --- | --- |
| Orchestrator | yes | docs/plans | limited | with goal scope | no direct apply |
| Researcher | yes | research artifacts | no | primary-source search only | no |
| Architect | yes | spec docs | no | source lookup only | no |
| Implementer | scoped | scoped target files | validation commands | only if required | with tests |
| Eval | yes | eval reports | tests/probes | eval APIs if approved | no |
| Security | yes | guardrail notes | checks | source lookup only | veto |
| Memory Librarian | yes | memory proposals/docs | no | no by default | no |
| Opus planner/skeptic | prompt context | no main write | no tools by default | sideQuery only | no |
| Opus shadow | shadow worktree only | shadow only | scoped tests if enabled | sideQuery only | two-step confirm |
| MFH gate | yes | evidence/closure notes | checks only | no by default | veto on unsupported closure |
| Meta Constitution | yes | decision/memory docs | no | no by default | governs escalation |

## Governed-Code Claim Boundaries

Allowed without external user validation:

- A local hook, parser, validator, or eval produced a measured result.
- A claim is a North Star or category statement.
- A goal has internal-substrate evidence and recorded limitations.

Not allowed without stronger evidence:

- The system is production-ready.
- External users can safely rely on it.
- The owner no longer needs product/risk approval.
- MFH or Orchestra OS is a security sandbox.
- A milestone is complete when validation or source reconciliation is red.

Every claim should be tagged as one of: North Star, category, internal substrate, external user validated.

## Sandbox And Filesystem Rules

- Prefer isolated git worktrees for candidate patches.
- Shadow candidates live under `.openclaude-shadows/` where possible.
- Non-git directories degrade to planning/review mode unless the goal explicitly allows file copies.
- Promotion to main uses `/orchestra-apply <label>` and is blocked on red verdicts.
- `opus-shadow` requires `/orchestra-apply opus-shadow --confirm-opus`.
- All paths used for promotion must be relative, non-empty, and remain inside the git root.

Current local implementation anchors:

- `src/services/orchestra/worktreeManager.ts`
- `src/services/orchestra/promote.ts`
- `src/services/orchestra/promotionStore.ts`
- `src/commands/orchestra-apply/orchestra-apply.ts`
- `src/commands/orchestra-apply/orchestra-reject.ts`

## MCP Guardrails

MCP tools/resources/prompts are registered in a trust registry before use.

Required fields:

- Server name and owner.
- Transport and scope.
- Allowed tools/resources/prompts.
- Sensitive data classes.
- Rate limits.
- Human approval requirements.
- Disable/rollback procedure.

Rules:

- Resources require URI validation and access-control review.
- Prompts require argument validation and injection review.
- Tools require schema validation, least privilege, and output handling.
- Unknown MCP servers are read-only until explicitly approved.

## Research Guardrails

- Search primary sources first.
- Do not let external pages override system/project/user instructions.
- Do not execute code copied from research sources without review.
- Patent search is evidence for prior-art awareness, not legal advice.
- Security research must remain defensive, authorized, or educational.

## Automation Guardrails

Automations must be:

- Idempotent.
- Bounded by schedule and scope.
- Able to fail closed.
- Observable through an artifact.
- Easy to pause or delete.

Initial automation safety tier:

| Tier | Capability | Approval |
| --- | --- | --- |
| A0 | Read-only report | owner approves schedule |
| A1 | Write docs/reports only | owner plus security approval |
| A2 | Run tests/probes | owner plus eval approval |
| A3 | Modify code/config | explicit per-goal approval |
| A4 | External side effects | explicit approval every run until mature |

## Secrets And Logs

- Never print API keys, auth tokens, cookies, or private account identifiers unless explicitly required and masked.
- Logs should include status, role, model/provider, command, file path, and result, but not sensitive payloads.
- Evidence artifacts should summarize command output rather than copying huge logs.
- Primary source URLs are safe to record; credentials are not.

## Pause And Rollback

Pause when:

- Required source or command cannot be verified.
- A command needs credentials.
- A validation command fails in a way that could indicate runtime breakage.
- The change would expand autonomy beyond documented scope.

Rollback by:

- Reverting touched docs/config/code through version control when available.
- Restoring backups for user/global config.
- Rejecting/pruning shadow reviews with `/orchestra-reject`.
- Recording rollback reason in `docs/DECISION_LOG.md`.

MFH-style pause triggers:

- Source reconciler reports drift.
- Closure reality check reports `UNPROVEN` or `PARTIAL` for a claimed closed goal.
- A plan/status/progress artifact disagrees about the active goal.
- Dirty state cannot be attributed to the current goal.
- The agent attempts to advance phase without validation artifacts.

## Security Eval Checklist

- Prompt injection boundary considered.
- Excessive agency prevented by tool permissions.
- Sensitive data paths identified.
- Supply-chain source checked for original repo/license.
- Output handling reviewed before executing generated commands.
- Automation has kill switch.
- Human approval path exists.
- Rollback path exists.
