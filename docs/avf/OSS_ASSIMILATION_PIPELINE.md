# OSS Assimilation Pipeline

## Purpose

OSS assimilation is not copy-paste adoption. It is a governed acquisition path for turning a missing capability into a reviewed integration task.

## Pipeline

```text
Need Detection
-> Candidate Search
-> Candidate Scoring
-> License Gate
-> Security Gate
-> Integration Mode Decision
-> Codex Task Packet
-> Validation
-> Capability Registry Update
```

## License Gate

- MIT, Apache, BSD: preferred candidates.
- GPL, AGPL: separate owner/legal review required.
- Unknown license: blocked.
- License mismatch with AVF distribution intent: blocked.

## Security Gate

Review before integration:

- install hooks
- postinstall scripts
- network behavior
- secret handling
- known vulnerabilities
- dependency tree
- maintainer trust signals
- suspicious obfuscation

## Tooling Notes

- MCP can become the future tool integration protocol.
- LangGraph can become a future stateful agent runtime adapter.
- Temporal can become a future durable workflow backend.
- This pipeline does not install LangGraph, Temporal, LiteLLM, MCP, or any runtime dependency.

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
