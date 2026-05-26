# AVF Market-to-Factory Vision

## New Definition

AVF is a Web-first Autonomous Venture Infrastructure.

It is not only a tool that turns an owner idea into a proof artifact. It is a repo-local control-plane seed for a larger operating system that can eventually observe markets, form strategy hypotheses, assemble factory cells, produce product/content/brand/code artifacts, collect evidence, and adapt direction.

Core loop:

```text
Market -> Strategy -> Factory -> Distribution -> Evidence -> Adaptation
```

## Market-to-Factory Loop

1. Market Sensing: observe allowed market signals, owner-provided material, public documentation, community notes, product signals, and repo-local evidence.
2. Strategic Hypothesis: transform signals into audience, wedge, product, content, brand, distribution, and monetization hypotheses.
3. Factory Formation: assemble only the required cells for the goal instead of activating every role by default.
4. Production: create draft-first product specs, Codex task packets, brand/IP memory, content drafts, media prompts, and validation plans.
5. Distribution: prepare owned-channel, approval-gated distribution material without posting automation.
6. Evidence Collection: record validation, feedback, performance, owner review, and failure signals.
7. Adaptation: produce keep/refine/pivot/kill decisions and the next safe action.

## Engines

- Market Intelligence Engine
- Strategy & Hypothesis Engine
- Factory Formation Engine
- Production Engine
- Transparent Influence Engine
- Evidence & Learning Engine
- Capability Acquisition Loop
- Governance & Safety Engine
- Runtime & Tooling Engine

## Source Notes

- web4.ai is treated as a high-level external inspiration for a broader web intelligence vision, not as an implementation dependency.
- Model Context Protocol is an open-source standard for connecting AI applications to external systems, useful later for tool registry design.
- LangGraph is a candidate runtime for long-running stateful agent orchestration.
- Temporal is a candidate durable workflow backend for crash-proof resume behavior.
- LiteLLM is a candidate provider-independent LLM gateway, not used in this design pass.
- WebArena is a cautionary benchmark showing autonomous web agents remain brittle; AVF should use sandboxed autonomy and approval gates before external action.

## Boundary

- repo_local_internal_only
- runtime implementation: blocked
- provider calls: blocked
- live model calls: blocked
- external service calls: blocked
- scraping implementation: blocked
- posting automation: blocked
- deploy: blocked
- publish: blocked
- production readiness claim: blocked
- release readiness claim: blocked
- public readiness claim: blocked
- fake human impersonation: blocked
- engagement manipulation: blocked
- protected_action_executed=false

## Next Safe Goal

Convert Kernel v0.1 from a simple factory output packet into a Venture Operation Packet local compiler.

<!-- BEGIN AVF PRIMARY SOURCE CLAIM INTEGRATION V0.1 -->
## Primary-Source Claim Integration

primary_source_claims_integrated=true
integration_decision=PRIMARY_SOURCE_CLAIMS_INTEGRATED_INTO_DOCS_ONLY
promotion_scope=architecture_docs_and_plans_only
source_claims_integrated=7
runtime_adoption_allowed=false
dependency_adoption_allowed=false

| Source target | Claim id | Primary source | Scope |
| --- | --- | --- | --- |
| `src-langgraph-official-docs` | `claim-agent-runtime-stateful-graph` | https://docs.langchain.com/oss/python/langgraph/overview | `architecture_docs_and_plans_only` |
| `src-temporal-official-docs` | `claim-durable-workflow-backend` | https://docs.temporal.io/ | `architecture_docs_and_plans_only` |
| `src-opentelemetry-standard-docs` | `claim-observability-standard` | https://opentelemetry.io/docs/what-is-opentelemetry/ | `architecture_docs_and_plans_only` |
| `src-mcp-official-docs` | `claim-tool-protocol-boundary` | https://modelcontextprotocol.io/docs/getting-started/intro | `architecture_docs_and_plans_only` |
| `src-litellm-original-repository` | `claim-provider-independent-llm-gateway` | https://github.com/BerriAI/litellm | `architecture_docs_and_plans_only` |
| `src-vllm-original-repository` | `claim-open-model-serving-plane` | https://github.com/vllm-project/vllm | `architecture_docs_and_plans_only` |
| `src-webarena-paper` | `claim-web-agent-autonomy-caution` | https://arxiv.org/abs/2307.13854 | `architecture_docs_and_plans_only` |

Boundary:

- These claims are promoted into architecture docs and planning only.
- They do not authorize dependency adoption, runtime integration, provider calls, deployment, publishing, release readiness, or production readiness.
- Use `avf/capabilities/generated/primary_source_manual_records.json` as the detailed evidence record.

<!-- END AVF PRIMARY SOURCE CLAIM INTEGRATION V0.1 -->
