import { describe, expect, test } from 'bun:test'

import { buildResearchBriefReport, evaluateResearchBrief } from './validate-research-briefs'

const requiredSources = [
  'AGENTS.md',
  'README.md',
  'docs/RESEARCH_PIPELINE.md',
  'docs/PROJECT_SPEC.md',
  'docs/MFH_META_SYNTHESIS.md',
  'docs/GOAL_SCHEMA.md',
  'docs/EVALS.md',
  'docs/SECURITY_AND_GUARDRAILS.md',
  'docs/DECISION_LOG.md',
  'docs/research/mimesis-engineering-source-ledger-2026-06-14.md',
  'docs/research/public-proof-pack-source-ledger-2026-06-14.md',
  'https://openai.com/index/the-next-evolution-of-the-agents-sdk/',
  'https://agents.md/',
  'https://agentskills.io/',
  'https://modelcontextprotocol.io/docs/getting-started/intro',
  'https://modelcontextprotocol.io/specification/2025-06-18/server/resources',
  'https://modelcontextprotocol.io/specification/2025-06-18/server/prompts',
  'https://modelcontextprotocol.io/specification/2024-11-05/server/tools',
  'https://developers.openai.com/api/docs/guides/agent-evals',
  'https://developers.openai.com/api/docs/guides/trace-grading',
  'https://github.com/openai/evals',
  'https://www.w3.org/TR/prov-overview/',
  'https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10',
  'https://owasp.org/www-project-top-10-for-large-language-model-applications/',
  'https://arxiv.org/abs/2210.03629',
  'https://arxiv.org/abs/2303.11366',
  'https://www.uspto.gov/patents/search/patent-public-search/',
]

function row(source: string, mapTo = 'Requirement: keep research source-backed'): string {
  return `| ${source} | ${source} | official source | Records the load-bearing pattern for this research brief. | ${mapTo} | Local no-provider research evidence only; not production or external validation. |`
}

const validBrief = `# Research Brief: Goal OS governed-code prior art

Date accessed: 2026-06-18

## Question

How should Metaforge import prior art into Goal OS work without letting OpenClaude become the public thesis?

## Decision Needed

Decide whether research claims need a reusable primary-source ledger before they enter roadmap or proof copy.

## Local Authority Sources

The brief uses AGENTS.md and current public docs as local authority.

## Primary Source Ledger

| Source | URL or path | Source class | Finding | Maps to | Boundary |
| --- | --- | --- | --- | --- | --- |
${requiredSources.map((source) => row(source)).join('\n')}

## Findings To Requirements / Evals / Guardrails / Decisions

- Requirement: every major claim maps to a local authority path, official source, original repository, paper, standard, or patent database.
- Eval: the validator rejects missing source coverage and blog-only final evidence.
- Guardrail: OpenClaude remains runtime substrate; Meta/MFH/Orchestra remains the public thesis.
- Decision: research brief validation gates future public proof updates.

## Rejected Sources

- Blog-only or secondary summaries were not used as final evidence.

## Follow-Up Goal Candidates

- Add eval flywheel source reconciliation once this ledger is validated.

## Claim Boundary

This brief is local no-provider research evidence. It is not production readiness, hosted deployment, benchmark superiority, external validation, or autonomous reliability evidence.
`

describe('research brief validator', () => {
  test('accepts a structured primary-source Goal OS research brief', () => {
    const result = evaluateResearchBrief(validBrief, 'docs/research/goal-os-governed-code-prior-art-2026-06-18.md')

    expect(result.ok).toBe(true)
    expect(result.errors).toEqual([])
    expect(result.requiredSourceCoverage.missing).toEqual([])
    expect(result.sourceRowCount).toBe(requiredSources.length)
  })

  test('rejects briefs that omit required primary sources', () => {
    const missingMcpTools = validBrief.replace(row('https://modelcontextprotocol.io/specification/2024-11-05/server/tools'), '')

    const result = evaluateResearchBrief(missingMcpTools)

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('primary source ledger is missing required source: https://modelcontextprotocol.io/specification/2024-11-05/server/tools')
  })

  test('rejects secondary or blog domains in the final source ledger', () => {
    const withBlog = validBrief.replace(
      row('https://agents.md/'),
      row('https://medium.com/example/blog-only-summary'),
    )

    const result = evaluateResearchBrief(withBlog)

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('primary source ledger contains disallowed secondary/blog source: https://medium.com/example/blog-only-summary')
  })

  test('rejects source rows that do not map to a requirement, eval, guardrail, or decision', () => {
    const unmapped = validBrief.replace(
      row('https://agentskills.io/'),
      row('https://agentskills.io/', 'Backlog note only'),
    )

    const result = evaluateResearchBrief(unmapped)

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('primary source ledger row must map to requirement, eval, guardrail, or decision: https://agentskills.io/')
  })

  test('builds a local no-provider report with pass/fail counts and source inputs', () => {
    const invalidBrief = validBrief.replace(row('https://www.w3.org/TR/prov-overview/'), '')
    const report = buildResearchBriefReport([
      { path: 'docs/research/valid.md', markdown: validBrief },
      { path: 'docs/research/invalid.md', markdown: invalidBrief },
    ])

    expect(report.briefFileCount).toBe(2)
    expect(report.validBriefCount).toBe(1)
    expect(report.invalidBriefCount).toBe(1)
    expect(report.providerCallsPerformed).toEqual([])
    expect(report.liveModelCallsPerformed).toEqual([])
    expect(report.externalCallsPerformed).toEqual([])
    expect(report.protectedActionsExecuted).toEqual([])
    expect(report.primarySourceInputs.some((source) => source.sourceUrl === 'https://www.w3.org/TR/prov-overview/')).toBe(true)
  })
})
