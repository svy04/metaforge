# Primary-Source Manual Records v0.1

record_decision=PRIMARY_SOURCE_MANUAL_RECORDS_CREATED_FROM_PRIMARY_SOURCES
source_records=7
manual_primary_source_review_performed=true
source_contents_acquired=true
automated_collection_allowed=false
external_fetch_performed=false

### src-langgraph-official-docs

- target_claim_id: `claim-agent-runtime-stateful-graph`
- source_record_status: `manual_primary_source_record_created`
- manual_primary_source_review_performed=true
- source_contents_acquired=true
- automated_collection_allowed=false
- external_fetch_performed=false
- source_uri: https://docs.langchain.com/oss/python/langgraph/overview
- source_reference_lines: turn0view0 lines 87-92, 124-130, 160-162

claim_supported: AVF runtime adapter should evaluate a stateful graph model for long-running agent orchestration.

evidence_excerpt_summary: The official overview frames LangGraph as a low-level orchestration framework and runtime for long-running stateful agents, with durable execution, streaming, human-in-the-loop, persistence, and memory capabilities. It also says LangGraph can be used without LangChain.

verification_notes: Manual primary-source review of official docs lines 87-92, 124-130, and 160-162.
### src-temporal-official-docs

- target_claim_id: `claim-durable-workflow-backend`
- source_record_status: `manual_primary_source_record_created`
- manual_primary_source_review_performed=true
- source_contents_acquired=true
- automated_collection_allowed=false
- external_fetch_performed=false
- source_uri: https://docs.temporal.io/
- source_reference_lines: turn0view1 lines 37-40, 87

claim_supported: AVF durable workflow phases should evaluate crash-resumable workflow execution.

evidence_excerpt_summary: The Temporal docs describe Temporal as an open-source platform for reliable applications and emphasize crash-proof execution that resumes where work left off after crashes, network failures, or infrastructure outages.

verification_notes: Manual primary-source review of official docs lines 37-40 and copyright line 87.
### src-opentelemetry-standard-docs

- target_claim_id: `claim-observability-standard`
- source_record_status: `manual_primary_source_record_created`
- manual_primary_source_review_performed=true
- source_contents_acquired=true
- automated_collection_allowed=false
- external_fetch_performed=false
- source_uri: https://opentelemetry.io/docs/what-is-opentelemetry/
- source_reference_lines: turn1view2 lines 832-844, 865-876

claim_supported: AVF observability should use a standard traces, metrics, and logs model.

evidence_excerpt_summary: The OpenTelemetry docs define it as an observability framework and toolkit for generation, export, and collection of telemetry such as traces, metrics, and logs, and describe it as open source, vendor-neutral, and tool-agnostic.

verification_notes: Manual primary-source review of official docs lines 832-844 and 865-876.
### src-mcp-official-docs

- target_claim_id: `claim-tool-protocol-boundary`
- source_record_status: `manual_primary_source_record_created`
- manual_primary_source_review_performed=true
- source_contents_acquired=true
- automated_collection_allowed=false
- external_fetch_performed=false
- source_uri: https://modelcontextprotocol.io/docs/getting-started/intro
- source_reference_lines: turn1view2 lines 61-73, 85-90

claim_supported: AVF tool integration should use an explicit tool protocol boundary before plugin execution.

evidence_excerpt_summary: The MCP docs define MCP as an open-source standard for connecting AI applications to external systems, including data sources, tools, and workflows. The same page positions MCP as a standardized connector boundary for AI applications.

verification_notes: Manual primary-source review of official docs lines 61-73 and 85-90.
### src-litellm-original-repository

- target_claim_id: `claim-provider-independent-llm-gateway`
- source_record_status: `manual_primary_source_record_created`
- manual_primary_source_review_performed=true
- source_contents_acquired=true
- automated_collection_allowed=false
- external_fetch_performed=false
- source_uri: https://github.com/BerriAI/litellm
- source_reference_lines: turn4view3 lines 449-467, 473-479; turn4view2 lines 360-363, 426-435

claim_supported: AVF model plane should evaluate a provider-independent LLM gateway.

evidence_excerpt_summary: The LiteLLM repository describes LiteLLM as an open-source AI Gateway for 100+ LLM providers using the OpenAI format. The official docs also describe a self-hosted OpenAI-compatible proxy and gateway surface for models, agents, and MCP.

verification_notes: Manual primary-source review of GitHub README lines 449-467 and 473-479, plus docs lines 360-363 and 426-435.
### src-vllm-original-repository

- target_claim_id: `claim-open-model-serving-plane`
- source_record_status: `manual_primary_source_record_created`
- manual_primary_source_review_performed=true
- source_contents_acquired=true
- automated_collection_allowed=false
- external_fetch_performed=false
- source_uri: https://github.com/vllm-project/vllm
- source_reference_lines: turn4view4 lines 377-405, 478-480; turn4view5 lines 2433-2453

claim_supported: AVF model plane should evaluate open model serving for later approved runtime phases.

evidence_excerpt_summary: The vLLM repository describes vLLM as a fast, easy-to-use library for LLM inference and serving, with throughput and memory management features. The docs note an OpenAI-compatible API server and broad model/hardware support.

verification_notes: Manual primary-source review of GitHub lines 377-405 and 478-480, plus docs lines 2433-2453.
### src-webarena-paper

- target_claim_id: `claim-web-agent-autonomy-caution`
- source_record_status: `manual_primary_source_record_created`
- manual_primary_source_review_performed=true
- source_contents_acquired=true
- automated_collection_allowed=false
- external_fetch_performed=false
- source_uri: https://arxiv.org/abs/2307.13854
- source_reference_lines: turn4view1 lines 30-46; turn3view6 lines 40-46

claim_supported: AVF web automation should remain approval-gated because autonomous web agents need evidence-backed limits.

evidence_excerpt_summary: The arXiv record describes WebArena as a realistic and reproducible web-agent environment with long-horizon benchmark tasks. It reports that the best GPT-4-based baseline agent achieved 14.41% end-to-end success versus 78.24% human performance, supporting approval-gated web automation rather than broad unsupervised action.

verification_notes: Manual primary-source review of arXiv metadata lines 30-46 and abstract/result lines 38-41.

## Next safe goal

next_safe_goal_id=avf_primary_source_records_review_v0_1
