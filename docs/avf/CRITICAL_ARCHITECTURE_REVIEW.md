# AVF Critical Architecture Review

## Verdict

The current AVF state is a repo-local control-plane foundation. It is useful, portable, and safe as a foundation, but it is not a production runtime.

This review keeps the distinction explicit:

- foundation exists: true
- runtime dependencies installed: false
- external runtime automation implemented: false
- release_ready: false
- production_ready: false
- OpenClaude-independent: true

## Current Strengths

1. Honest boundary language: the foundation does not present internal evidence as launch, release, deployment, external validation, or production readiness.
2. Goal OS direction: North Star, Program, Sprint, Codex Goal, and Atomic Task layers give the factory a real decomposition model.
3. Safety posture: draft-first content, human approval gates, blocked deceptive influence patterns, and protected-action boundaries are already explicit.
4. Role organization: Orchestrator, TPM, Solution Architect, DevRel, Infra Engineer, SRE, Data Analyst, Growth, Brand/IP, Safety, and Codex Executor roles create a usable organization model.
5. Codex lane discipline: PR-sized tasks, narrow files, validation commands, forbidden changes, and next-PR recommendations make execution auditable.

## Current Limitations

### Runtime gap

The current AVF does not have a stateful worker, queue, retry engine, scheduler, durable workflow backend, or agent execution graph. Its roles are durable definitions, not running agents.

### Schema gap

The current schemas are useful for foundation validation but remain shallow. They need versioned typed records with run IDs, artifact IDs, hashes, actor identity, approval state, validation method, confidence, and replay pointers.

### Evidence gap

The v1 evidence ledger records claim boundaries but does not yet create replayable evidence lineage. AVF needs artifact provenance, validation events, actor identity, input and output hashes, and approval decisions.

### Validation gap

Current validation proves file presence, required markers, and protected-action flags. It does not yet prove an end-to-end semantic run from goal intake to factory output packet, Codex task packet, validation report, and evidence ledger entry.

### Governance gap

Risk policy exists as a declared boundary. It is not yet a signed approval model, RBAC layer, policy-as-code decision engine, or execution blocker.

### Product/UI gap

The current AVF can be inspected through files and reports, but it does not yet provide a Studio UI for goal intake, run review, memory editing, approval queues, evidence browsing, or Codex task review.

### Feedback gap

Feedback and experiment registries exist as a foundation, but external user signals, content performance, issue feedback, customer interviews, and analytics events are not yet connected.

## Plane Separation

| Plane | Role | Current state | Required expansion |
| --- | --- | --- | --- |
| Control Plane | Goal OS, roles, routing, safety, evidence contracts | Present as repo-local foundation | Typed policies, versioned schemas, approval states |
| Runtime Plane | Workers, workflow, retries, scheduling, state machines | Missing | Adapter contract, local dry-run runner, durable backend later |
| Data Plane | Evidence DB, artifact store, memory, registry | Weak/file-based | Evidence ledger v2, artifact provenance, optional DB later |
| Model/Tool Plane | LLM gateway, model routing, MCP tools, coding executors | Not implemented | Provider-independent gateway and tool registry later |
| Observability/Eval Plane | Traces, cost, metrics, regression evals, red-team tests | Not implemented | Trace and eval contracts before live integrations |
| Studio/Product Plane | Goal UI, approval UI, evidence browser, memory editor | Missing | AVF Studio information architecture before implementation |

## Missing Capabilities By Priority

P0:
- Goal intake engine
- Schema v2
- Evidence ledger v2
- Semantic validator

P1:
- Runtime state machine
- Workflow backend
- LLM gateway plan
- Human approval UI
- Observability and eval plan

P2:
- Plugin/tool registry
- Multi-tenant and security model
- Artifact registry

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

## Conclusion

AVF should evolve from a document and prompt control plane into a venture operating infrastructure with runtime, evidence, governance, eval, and studio layers. The next safe step is not Kubernetes-scale automation. The next safe step is AVF Kernel v0.1: one local sample goal transformed into a track classification, agent role plan, proof artifact plan, Codex task packet, safety boundary, validation report, and evidence ledger v2 entry.
