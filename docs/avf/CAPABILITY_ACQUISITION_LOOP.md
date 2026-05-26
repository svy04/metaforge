# Capability Acquisition Loop

## Role

The Capability Acquisition Loop lets AVF identify missing factory capabilities and produce safe acquisition plans without unapproved cloning, dependency installation, provider calls, or external execution.

## Loop

1. Capability Gap Detection
2. Build vs Buy vs Adopt Decision
3. OSS Candidate Discovery
4. Fit Evaluation
5. Risk Review
6. Integration Mode Decision
7. Codex PR-sized Task
8. Local Validation
9. Capability Registry Update

## Candidate Evaluation Criteria

- feature fit
- license
- maintenance activity
- issue response quality
- dependency risk
- security history
- API stability
- architecture fit
- local-first compatibility
- data boundary fit

## Integration Modes

- reference only
- adapter
- subprocess
- MCP server
- library dependency
- fork
- rewrite from concept

## Source Notes

Model Context Protocol is a future candidate for tool integration boundaries. LiteLLM is a future candidate for provider-independent LLM gateway boundaries. Neither is installed or called in this design pass.

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
