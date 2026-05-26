# Factory Formation Engine

## Role

The Factory Formation Engine selects the smallest useful set of factory cells for a goal.

It does not activate every role by default. It assembles only the required cells based on the Venture Operation Packet.

## Candidate Cells

- Product Cell
- Infra Product Cell
- Brand/IP Cell
- Content Cell
- Growth Cell
- Code Cell
- Evidence Cell
- Safety Cell
- Capability Acquisition Cell

## Output

```yaml
factory_formation_packet:
  required_cells:
  skipped_cells:
  reason:
  cell_inputs:
  cell_outputs:
  handoff_order:
  validation_commands:
```

## Selection Rules

- Use Product Cell when the goal needs PRD, MVP scope, user journey, or product architecture.
- Use Infra Product Cell when the target user is an engineer, platform team, SRE, or developer workflow owner.
- Use Brand/IP Cell when identity, character, visual consistency, or style memory matters.
- Use Content Cell when repeated draft-first production is needed.
- Use Code Cell only when a PR-sized Codex task can be defined.
- Use Safety Cell for all public, influence, automation, or external-action-adjacent goals.

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
