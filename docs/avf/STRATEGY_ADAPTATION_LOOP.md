# Strategy Adaptation Loop

## Role

The Strategy Adaptation Loop turns evidence into strategy changes. It prevents AVF from being a content generator with no learning loop.

## Decision Types

- KEEP: evidence supports the current hypothesis; invest more.
- REFINE: adjust target, message, channel, feature, or format.
- PIVOT: change market, product angle, positioning, or production line.
- KILL: evidence is weak or negative; stop investment.

## Input Evidence

- local validator result
- Codex PR result
- test result
- owner review
- future approved content performance
- future approved user feedback
- GitHub issue and PR feedback
- future approved landing page conversion

## Output

```yaml
strategy_adaptation_decision:
  hypothesis_id:
  decision:
  evidence_summary:
  confidence:
  next_action:
  kill_or_continue_reason:
```

## Web Agent Caution

WebArena is a reminder that autonomous web agents remain brittle on realistic web tasks. AVF should therefore move through sandboxed autonomy, approval-gated action, and bounded operation instead of unrestricted web action.

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
