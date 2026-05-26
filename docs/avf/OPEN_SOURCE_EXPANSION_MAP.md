# AVF Open-Source Expansion Map

## Purpose

This map records candidate upstream systems for expanding AVF without making the AVF domain logic dependent on OpenClaude or any single provider. It is a candidate map only. No dependency is installed here, no provider is called, and no external runtime automation is implemented.

Status:

- OpenClaude-independent: true
- runtime dependencies installed: false
- external runtime automation implemented: false
- release_ready: false
- production_ready: false

## Expansion Map

| AVF need | Candidate | Build-vs-buy recommendation | AVF boundary |
| --- | --- | --- | --- |
| Stateful agent graph | LangGraph | Reuse upstream as an adapter candidate after AVF Kernel v0.1 proves local goal-to-output semantics | Keep AVF node contracts provider-independent |
| Durable workflow and resume | Temporal | Reuse upstream for crash-resistant long-running workflows later | Do not use until local run state contract exists |
| Kubernetes-scale workflow | Argo Workflows | Reuse upstream only if AVF needs containerized parallel jobs | Not part of foundation or Kernel v0.1 |
| General workflow alternatives | Kestra, Prefect, Airflow | Compare as orchestration alternatives; prefer event/manual approval support over batch-only fit | Candidate only |
| Evidence and data lineage | Dagster | Reuse upstream when artifact lineage becomes data-product-like | Do not replace AVF claim boundary logic |
| Provider-independent LLM gateway | LiteLLM | Reuse upstream later for gateway/proxy/cost boundaries | No provider calls in this pass |
| Local/open model serving | Ollama, vLLM | Keep as optional future fallback/serving candidates | No local model runtime in this pass |
| RAG and document pipelines | Haystack | Reuse upstream later for memory/document retrieval pipelines | Brand/IP and evidence memory contracts stay AVF-owned |
| LLM observability | Langfuse, Phoenix | Reuse upstream later for traces, prompt versions, and eval views | No external service integration in this pass |
| Eval and red-team harness | promptfoo, Ragas | Reuse upstream later for regression and quality checks | Safety policy remains AVF-owned |
| Tool protocol | MCP | Reuse upstream later for tool registry boundaries | No tool execution in this pass |
| Telemetry standard | OpenTelemetry | Reuse upstream later for traces, metrics, and logs | Define AVF validation events first |
| Optional coding executor lane | OpenHands, SWE-agent | Evaluate only as approval-gated alternatives to Codex lane | PR-sized, human-approved, no autonomous mutation |

## What AVF Should Build

AVF should build domain logic that upstream workflow tools do not know:

- Goal OS and goal hierarchy
- Product, Infra Product, Brand/IP, Content, Growth, and Safe Influence track taxonomy
- Proof artifact contracts
- Brand/IP memory contract
- Safe Influence Factory policy
- Codex task packet grammar
- Evidence claim boundary
- Approval-gated operating model
- Goal-to-task transformation logic

## What AVF Should Reuse

AVF should reuse upstream systems for generic infrastructure:

- workflow engine
- queue, retry, timeout, and idempotency
- LLM gateway
- local or open model serving
- RAG pipeline
- tracing and observability
- eval and red-team harness
- tool protocol
- artifact storage
- policy enforcement substrate
- auth and RBAC

## Protected-Action Boundary

- deploy: blocked
- publish: blocked
- provider calls: blocked
- live model calls: blocked
- external service calls: blocked
- production readiness claim: blocked
- release readiness claim: blocked
- public readiness claim: blocked
- external validation claim: blocked
- protected_action_executed: false
- provider_calls_performed: false
- deploy_performed: false
- publish_performed: false

## Next Recommendation

Before adopting any runtime dependency, implement AVF Kernel v0.1 as a local dry run:

sample goal -> factory output packet -> Codex task packet -> validation report -> evidence ledger v2 entry.

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
