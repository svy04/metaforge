# AVF Build-Vs-Buy Decision Record

## Decision

AVF should build its domain-specific venture factory logic and reuse upstream infrastructure for generic workflow, runtime, gateway, storage, observability, and evaluation concerns.

This keeps AVF OpenClaude-independent while avoiding a custom infrastructure platform before the domain loop is proven.

State:

- runtime dependencies installed: false
- external runtime automation implemented: false
- release_ready: false
- production_ready: false

## Build in AVF

Use build in AVF for logic that defines what this factory uniquely does:

- Goal OS: North Star -> Program -> Sprint -> Codex Goal -> Atomic Task
- venture track taxonomy for Product, Infra Product, Brand/IP, Content, Growth, Safe Influence, and Codex Lane
- proof artifact contract
- Brand/IP memory contract
- character and style continuity memory
- Safe Influence Factory policy
- draft-first content pipeline boundary
- Codex task packet grammar
- evidence claim boundary
- human approval gate model
- goal-to-output and goal-to-task transformation rules
- final owner decision packet grammar

## Reuse upstream

Use reuse upstream for infrastructure that is already solved better by maintained projects:

- workflow engine
- queue, retry, timeout, and idempotency
- durable execution backend
- LLM gateway
- local/open model serving
- document and RAG pipeline
- tracing and observability
- eval and red-team harness
- tool protocol
- artifact storage
- policy enforcement substrate
- auth, RBAC, and multi-tenant isolation

## Do Not Implement From Scratch

Decision marker: do not implement from scratch for commodity runtime infrastructure.

Do not implement from scratch unless an AVF-specific domain boundary makes an upstream tool unsuitable:

- agent workflow runtime
- crash recovery engine
- Kubernetes job scheduler
- general-purpose queue
- LLM proxy
- vector database
- telemetry collector
- authentication framework
- policy engine

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

## Decision Consequence

The next PR should not add LangGraph, Temporal, LiteLLM, Langfuse, MCP, or any dependency. The next PR should add AVF Kernel v0.1 local dry-run semantics so that runtime candidates have a stable contract to implement later.
