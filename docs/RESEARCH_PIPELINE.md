# Research Pipeline

Status: first planning pass

The Autonomous Goal OS uses research as an operating input, not as decoration. Research must change the plan, narrow uncertainty, or identify a reusable implementation.

Harness update: Meta's raw/wiki/decision pattern is the default memory model for research. Raw sources are immutable; wiki/briefs are agent-maintained; decisions record why the plan changed.

## Source Ladder

Use this order when research affects architecture, implementation, safety, product direction, or eval design:

1. Existing local code and docs.
2. Official product docs.
3. Original GitHub repositories and maintained source code.
4. Standards and specifications.
5. Papers and technical reports.
6. Patent databases.
7. Issue trackers, release notes, changelogs.
8. Blog posts only as discovery pointers to the above.

Blog-only summaries are rejected as final evidence unless no primary source exists and the decision log says why.

## Research Workflow

1. State the research question.
2. Search local repo first.
3. Identify primary-source classes needed.
4. Fetch/read primary sources.
5. Extract only claims relevant to the goal.
6. Record source URL/path, date accessed, and reason.
7. Map findings to decisions, requirements, or evals.
8. Mark unsupported claims as assumptions.
9. Update `docs/DECISION_LOG.md` when the plan changes.

## Local-First Rule

Before external research, read:

- `README.md`
- `AGENTS.md`
- `package.json`
- `docs/`
- `.planning/`
- source files matching the domain

For this project, the natural source files include:

- `src/services/orchestra/*.ts`
- `src/skills/loadSkillsDir.ts`
- `src/tools/AgentTool/loadAgentsDir.ts`
- `src/utils/claudemd.ts`
- `src/hooks/useScheduledTasks.ts`
- `src/utils/cronScheduler.ts`
- `src/services/mcp/*.ts`
- `src/commands/orchestra-apply/*`

When the goal touches MFH/Meta/governed-code, use the public synthesis package
in this repository as the public authority:

- `docs/MFH_META_SYNTHESIS.md`
- `docs/PROJECT_SPEC.md`
- `docs/GOAL_SCHEMA.md`
- `docs/EVALS.md`
- `docs/SECURITY_AND_GUARDRAILS.md`
- `docs/DECISION_LOG.md`

Private harness notes may inform internal planning, but they are not public
proof and should not be named as public source paths.

## Meta Raw/Wiki/Decision Flow

Use this flow for durable research:

1. Preserve primary material in a raw/source ledger when the project needs long-term reuse.
2. Write the agent-owned synthesis as a research brief or wiki-style concept page.
3. Link every major claim to a source, validation method, or decision-log assumption.
4. Record plan-changing decisions in `docs/DECISION_LOG.md`.
5. Promote repeated research workflows to Skills only after repeated validated runs.

The raw layer is evidence. The wiki/brief layer is interpretation. The decision log is the authority for why the plan changed.

## Primary-Source Anchors For This Project

| Topic | Source | Why it matters |
| --- | --- | --- |
| Agent runtime primitives | https://openai.com/index/the-next-evolution-of-the-agents-sdk/ | Controlled workspace, instructions, MCP, skills, AGENTS.md, sandbox, checkpointing |
| AGENTS.md | https://agents.md/ | Agent instruction file convention |
| Skills | https://agentskills.io/ | Skill format and progressive disclosure |
| MCP | https://modelcontextprotocol.io/docs/getting-started/intro | Standard integration layer |
| MCP resources | https://modelcontextprotocol.io/specification/2025-06-18/server/resources | Context/resource exposure |
| MCP prompts | https://modelcontextprotocol.io/specification/2025-06-18/server/prompts | Reusable prompt templates |
| MCP tools | https://modelcontextprotocol.io/specification/2024-11-05/server/tools | Model-controlled external actions |
| Agent evals | https://developers.openai.com/api/docs/guides/agent-evals | Reproducible agent-quality checks |
| Trace grading | https://developers.openai.com/api/docs/guides/trace-grading | Workflow-level trace scoring |
| OpenAI Evals | https://github.com/openai/evals | Open-source eval framework |
| AI risk governance | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10 | Governance, risk, trustworthiness anchor |
| LLM security | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Prompt injection, excessive agency, sensitive data risks |
| Provenance | https://www.w3.org/TR/prov-overview/ | Evidence lineage model |
| Reasoning + acting | https://arxiv.org/abs/2210.03629 | Research basis for interleaved reasoning/actions |
| Reflection loop | https://arxiv.org/abs/2303.11366 | Feedback/reflection memory basis |
| Patents/prior art | https://www.uspto.gov/patents/search/patent-public-search/ | Prior-art search requirement |
| Governed-code category | `docs/MFH_META_SYNTHESIS.md` | Public synthesis of the product category and gate import |
| MFH Operating Gate | `docs/GOAL_SCHEMA.md` | Public goal evidence and closure schema |
| Meta Constitution | `docs/SECURITY_AND_GUARDRAILS.md` | Public owner/operator boundary and guardrail model |
| Candidate M closure pattern | `docs/EVALS.md` | Public state-machine and verification gate import |

## Research Artifact Template

```markdown
# Research Brief: <topic>

Question:

Decision needed:

Local sources:
- <path> - finding

Primary external sources:
- <url> - finding

Rejected sources:
- <url> - reason

Findings:
1. <claim> - supported by <source>

Implications:
- Requirement change:
- Eval change:
- Security change:

Open questions:
- <question>

Decision log entries:
- D-000
```

## Rejection Rules

Reject or quarantine:

- Blog posts that do not link to original sources.
- Claims about model/provider capability without official docs or runtime probe.
- Patent claims without patent database link.
- Security claims without standard, official project, or reproducible exploit/eval.
- Open-source claims without repository, license, maintenance signal, and install/run path.

## Research-to-Plan Gate

A researched claim can enter the roadmap only when one of these is true:

- It is backed by a primary source.
- It is backed by local code evidence.
- It has a validation method.
- It is explicitly recorded as an assumption in `docs/DECISION_LOG.md`.
