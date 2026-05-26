# Venture Operation Packet Spec

## Purpose

The Venture Operation Packet is the central output object for the Market-to-Factory Loop. It contains the market interpretation, strategy hypothesis, factory cell plan, production plan, distribution boundary, capability gaps, Codex execution tasks, governance boundary, and evidence learning plan.

It replaces the idea that a Venture Proof Packet is the top-level output. A Venture Proof Packet can be one artifact inside the larger operation packet.

## Packet Shape

```yaml
venture_operation_packet:
  run_id:
  goal_id:
  raw_goal:
  goal_essence:

  market_intelligence_packet:
    observed_signals:
    target_market:
    pain_points:
    competitor_assumptions:
    unknowns:

  strategy_hypothesis_packet:
    thesis:
    wedge:
    audience:
    product_angle:
    content_angle:
    monetization_angle:
    failure_modes:

  factory_formation_packet:
    required_cells:
    skipped_cells:
    reason:

  production_plan_packet:
    product_artifacts:
    content_artifacts:
    brand_artifacts:
    code_artifacts:
    media_artifacts:

  influence_distribution_packet:
    owned_channels:
    draft_first_outputs:
    approval_required:
    prohibited_actions:

  capability_acquisition_packet:
    missing_capabilities:
    oss_candidates_required:
    build_vs_buy_decision_needed:
    license_review_required:

  codex_execution_packet:
    pr_sized_tasks:
    forbidden_changes:
    validation_commands:

  safety_governance_packet:
    creation_level:
    human_gate_required:
    red_actions_blocked:
    claim_boundary:

  evidence_learning_packet:
    success_criteria:
    failure_criteria:
    evidence_entries:
    next_decision:

  claim_boundary:
    repo_local_internal_only:
    protected_action_executed:
    provider_calls_performed:
    deploy_performed:
    publish_performed:
    production_ready:
    release_ready:
```

## Required Subpackets

- market_intelligence_packet
- strategy_hypothesis_packet
- factory_formation_packet
- production_plan_packet
- influence_distribution_packet
- capability_acquisition_packet
- codex_execution_packet
- safety_governance_packet
- evidence_learning_packet

## Validation Requirements

- Every packet has a goal_id and run_id.
- Every hypothesis has success and failure criteria.
- Every production item has a claim boundary.
- Every Codex task is PR-sized.
- Every external or public action remains approval-gated.
- Evidence entries use evidence ledger v2.

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
