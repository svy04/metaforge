# AVF Platform Roadmap

## Roadmap Boundary

This roadmap describes internal architecture evolution. It does not authorize runtime execution, external calls, provider calls, deployment, publishing, release readiness claims, production readiness claims, or public readiness claims.

State:

- OpenClaude-independent: true
- runtime dependencies installed: false
- external runtime automation implemented: false
- release_ready: false
- production_ready: false

## Platform Planes

| Plane | Responsibility |
| --- | --- |
| Control Plane | Goal OS, roles, routing, safety, policy, evidence contracts |
| Runtime Plane | Local run state, agent nodes, transitions, retries, timeouts, human gates |
| Data Plane | Evidence ledger, artifact provenance, result memory, feedback registry |
| Model/Tool Plane | LLM gateway, tool registry, coding executor lane, provider boundaries |
| Observability/Eval Plane | Validation events, traces, metrics, evals, regression and red-team checks |
| Studio/Product Plane | Goal intake, review queues, memory editor, evidence browser, task packet viewer |

## Phases

### Phase 0: Current Foundation

Repo-local docs, schemas, role catalog, routing rules, runbooks, safety boundaries, Codex lane templates, and foundation validation.

Exit state: FACTORY_FOUNDATION_READY as an internal foundation state only.

### Phase 1: AVF Kernel v0.1

Add typed local goal intake, deterministic router, risk classifier, factory output packet, evidence ledger v2 entry writer, semantic validator, and sample goal fixtures.

Success proof: one sample goal produces a factory output packet, Codex task packet, validation report, and evidence ledger v2 entry locally.

### Phase 2: Agent Runtime Adapter

Define provider-independent node contracts and plan a LangGraph-style adapter. Keep execution local and dry-run until policy and evidence contracts prove stable.

### Phase 3: Durable Workflow Backend

Evaluate Temporal or similar durable workflow systems for resume, retry, timeout, and long-running work. Do not introduce this until Phase 1 and Phase 2 outputs are replayable.

### Phase 4: LLM Gateway And Tool Registry

Plan LiteLLM-style gateway boundaries, MCP-style tool registry contracts, and optional local/open serving boundaries. No provider call is authorized by this roadmap.

### Phase 5: Observability And Evaluation

Add validation event contracts, trace plans, eval harness plans, and quality regression policy. Candidate tools include Langfuse, Phoenix, promptfoo, Ragas, and OpenTelemetry.

### Phase 6: AVF Studio

Design a web product surface for goal intake, agent run review, safety review, human approval queues, Codex task packet review, evidence browsing, Brand/IP memory editing, and experiment registry review.

### Phase 7: Plugin And Cell Marketplace

Define how product cells, brand/IP cells, content cells, infra cells, growth cells, and tool adapters can be added safely without crossing protected-action boundaries.

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

## Next Safe Goal

Implement AVF Kernel v0.1 local dry run. It should transform one sample goal into track classification, role plan, proof artifact plan, Codex task packet, safety boundary, validation report, and evidence ledger v2 entry.

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
