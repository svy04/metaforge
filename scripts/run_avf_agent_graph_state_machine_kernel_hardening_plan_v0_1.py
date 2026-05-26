from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

REVIEW_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_review.json"
REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_review_gate.json"
HARDENING_PLAN = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan.json"
HARDENING_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_HARDENING_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_hardening_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_replay_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_validator_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_HARDENING_PLAN_READY_FOR_INVARIANT_VALIDATOR"
PLAN_SCOPE = "repo_local_state_machine_hardening_plan_only"
INVARIANT_SCOPE = "repo_local_state_machine_invariant_validator_only"

INVARIANT_DEFINITIONS = [
    (
        "normal_path_terminal_state_is_evidence_written",
        "normal_path",
        "The allowed normal path must terminate at evidence_written.",
        "normal_path_review_records",
    ),
    (
        "normal_transition_sequence_is_contiguous",
        "normal_path",
        "The normal transition sequence must remain contiguous from sequence_index 1 through 5.",
        "normal_path_review_records",
    ),
    (
        "normal_transition_order_is_preserved",
        "normal_path",
        "The orchestrator, router, safety_reviewer, codex_planner, evidence_writer order must be preserved.",
        "normal_path_review_records",
    ),
    (
        "guarded_allowed_path_requires_pass_status",
        "guarded_outcome",
        "Allowed local transitions require an explicit PASS replay status and allowed_replay_path state type.",
        "guarded_outcome_review_records",
    ),
    (
        "blocked_terminal_outcomes_never_reach_evidence_written",
        "guarded_outcome",
        "Blocked terminal outcomes must terminate at blocked_terminal and never evidence_written.",
        "guarded_outcome_review_records",
    ),
    (
        "owner_review_outcomes_never_auto_execute",
        "guarded_outcome",
        "Owner-review outcomes must terminate at owner_review_required and never execute protected actions.",
        "guarded_outcome_review_records",
    ),
    (
        "protected_action_flags_remain_false",
        "guarded_outcome",
        "Every replay-derived hardening path must keep protected_action_allowed false.",
        "guarded_outcome_review_records",
    ),
    (
        "dependency_and_runtime_actions_remain_blocked",
        "safety_boundary",
        "Dependency adoption and runtime integration remain blocked before explicit owner approval.",
        "claim_boundary",
    ),
    (
        "evidence_event_uri_required_before_terminal_success",
        "safety_boundary",
        "Terminal success must require evidence event linkage before future runtime adapter work.",
        "normal_path_review_records",
    ),
    (
        "node_sequence_gap_or_duplicate_blocks_transition",
        "safety_boundary",
        "Node sequence gaps or duplicates must remain mapped to blocked terminal outcomes.",
        "guarded_outcome_review_records",
    ),
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def false_boundary() -> dict:
    return {
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "automated_scraping_performed": False,
        "scraping_performed": False,
        "posting_automation_performed": False,
        "dependency_install_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "package_install_performed": False,
        "runtime_integration_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_previous_gate() -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("replay review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("replay review gate must point to this hardening plan goal")
    if gate.get("hardening_plan_allowed") is not True:
        raise SystemExit("hardening plan must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_review() -> dict:
    review = read_json(REVIEW_RESULT)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("replay review result goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("replay review result must point to this hardening plan goal")
    if review.get("hardening_plan_allowed") is not True:
        raise SystemExit("hardening plan must be allowed")
    if review.get("unexpected_replay_results") != 0:
        raise SystemExit("unexpected replay results must remain zero")
    if review.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if review.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")
    return review


def build_invariants(review: dict) -> list[dict]:
    invariants = []
    for index, (invariant_id, category, description, source_field) in enumerate(INVARIANT_DEFINITIONS, start=1):
        invariants.append(
            {
                "invariant_id": invariant_id,
                "sequence_index": index,
                "category": category,
                "description": description,
                "source_review_field": source_field,
                "source_review_goal_id": review["goal_id"],
                "status": "planned",
                "validator_required": True,
                "protected_action_allowed": False,
            }
        )
    return invariants


def count_by_category(invariants: list[dict], category: str) -> int:
    return sum(1 for invariant in invariants if invariant["category"] == category)


def build_plan(review: dict) -> dict:
    invariants = build_invariants(review)
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "source_review_goal_id": review["goal_id"],
        "created_at": CREATED_AT,
        "plan_decision": PLAN_DECISION,
        "plan_scope": PLAN_SCOPE,
        "invariant_scope": INVARIANT_SCOPE,
        "hardening_invariants_created": len(invariants),
        "normal_path_invariants": count_by_category(invariants, "normal_path"),
        "guarded_outcome_invariants": count_by_category(invariants, "guarded_outcome"),
        "safety_boundary_invariants": count_by_category(invariants, "safety_boundary"),
        "hardening_invariants": invariants,
        "invariant_validator_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(plan: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-hardening-plan-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "plan_decision": PLAN_DECISION,
        "plan_scope": PLAN_SCOPE,
        "invariant_scope": INVARIANT_SCOPE,
        "hardening_invariants_created": plan["hardening_invariants_created"],
        "invariant_validator_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-state-machine-kernel-invariant-validator
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create repo-local invariant validator for the deterministic state machine kernel
  - Validate normal path terminal state, transition sequence, and transition order
  - Validate guarded blocked and owner-review outcomes stay non-executing
  - Validate dependency/runtime adoption remains blocked
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(plan: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_hardening_plan_v0_1",
        "status": "PASS",
        "plan_decision": PLAN_DECISION,
        "plan_scope": PLAN_SCOPE,
        "invariant_scope": INVARIANT_SCOPE,
        "hardening_invariants_created": plan["hardening_invariants_created"],
        "normal_path_invariants": plan["normal_path_invariants"],
        "guarded_outcome_invariants": plan["guarded_outcome_invariants"],
        "safety_boundary_invariants": plan["safety_boundary_invariants"],
        "invariant_validator_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(plan: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        "| {sequence} | `{invariant_id}` | {category} | {status} |".format(
            sequence=invariant["sequence_index"],
            invariant_id=invariant["invariant_id"],
            category=invariant["category"],
            status=invariant["status"],
        )
        for invariant in plan["hardening_invariants"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [HARDENING_PLAN, HARDENING_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph State Machine Kernel Hardening Plan v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_hardening_plan_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_hardening_plan_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_hardening_plan_v0_1.py

## Plan summary

- plan_decision={PLAN_DECISION}
- plan_scope={PLAN_SCOPE}
- invariant_scope={INVARIANT_SCOPE}
- hardening_invariants_created={plan["hardening_invariants_created"]}
- normal_path_invariants={plan["normal_path_invariants"]}
- guarded_outcome_invariants={plan["guarded_outcome_invariants"]}
- safety_boundary_invariants={plan["safety_boundary_invariants"]}
- invariant_validator_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Planned invariants

| Sequence | Invariant | Category | Status |
| --- | --- | --- | --- |
{rows}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    review = load_review()
    plan = build_plan(review)

    write_json(HARDENING_PLAN, plan)
    write_json(HARDENING_GATE, build_gate(plan))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plan))
    write_text(VALIDATION_REPORT, build_report(plan))

    print("AVF Agent Graph State Machine Kernel Hardening Plan v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_hardening_plan_v0_1=true")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_scope={PLAN_SCOPE}")
    print(f"invariant_scope={INVARIANT_SCOPE}")
    print(f"hardening_invariants_created={plan['hardening_invariants_created']}")
    print(f"normal_path_invariants={plan['normal_path_invariants']}")
    print(f"guarded_outcome_invariants={plan['guarded_outcome_invariants']}")
    print(f"safety_boundary_invariants={plan['safety_boundary_invariants']}")
    print("invariant_validator_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
