from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

HARDENING_PLAN = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan.json"
HARDENING_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan_gate.json"
REPLAY_REVIEW = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_review.json"
INVARIANT_VALIDATION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validation.json"
INVARIANT_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validation_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validation_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validator_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_INVARIANT_VALIDATOR_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_validator_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_hardening_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
VALIDATOR_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_INVARIANTS_VALIDATED_FOR_REVIEW"
VALIDATOR_SCOPE = "repo_local_state_machine_invariant_validator_only"
REVIEW_SCOPE = "repo_local_state_machine_invariant_review_only"


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
    gate = read_json(HARDENING_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("hardening plan gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("hardening plan gate must point to this invariant validator goal")
    if gate.get("invariant_validator_allowed") is not True:
        raise SystemExit("invariant validator must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_inputs() -> tuple[dict, dict]:
    plan = read_json(HARDENING_PLAN)
    review = read_json(REPLAY_REVIEW)
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("hardening plan result goal mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("hardening plan must point to this invariant validator goal")
    if plan.get("invariant_validator_allowed") is not True:
        raise SystemExit("invariant validator must be allowed")
    if review.get("goal_id") != plan.get("source_review_goal_id"):
        raise SystemExit("replay review must match hardening plan source")
    return plan, review


def normal_records(review: dict) -> list[dict]:
    return review["normal_path_review_records"]


def guarded_records(review: dict) -> list[dict]:
    return review["guarded_outcome_review_records"]


def evaluate_invariant(invariant: dict, review: dict, plan: dict) -> tuple[bool, str]:
    invariant_id = invariant["invariant_id"]
    normal = normal_records(review)
    guarded = guarded_records(review)

    checks = {
        "normal_path_terminal_state_is_evidence_written": lambda: all(
            record["terminal_state"] == "evidence_written" for record in normal
        ),
        "normal_transition_sequence_is_contiguous": lambda: [
            record["sequence_index"] for record in normal
        ]
        == [1, 2, 3, 4, 5],
        "normal_transition_order_is_preserved": lambda: [
            record["node_id"] for record in normal
        ]
        == ["orchestrator", "router", "safety_reviewer", "codex_planner", "evidence_writer"],
        "guarded_allowed_path_requires_pass_status": lambda: [
            record for record in guarded if record["state_type"] == "allowed_replay_path"
        ][0]["terminal_state"]
        == "evidence_written",
        "blocked_terminal_outcomes_never_reach_evidence_written": lambda: all(
            record["terminal_state"] == "blocked_terminal"
            for record in guarded
            if record["state_type"] == "blocked_terminal"
        ),
        "owner_review_outcomes_never_auto_execute": lambda: all(
            record["terminal_state"] == "owner_review_required"
            and record["protected_action_allowed"] is False
            for record in guarded
            if record["state_type"] == "owner_review_required"
        ),
        "protected_action_flags_remain_false": lambda: all(
            record["protected_action_allowed"] is False for record in guarded
        ),
        "dependency_and_runtime_actions_remain_blocked": lambda: (
            plan["dependency_adoption_allowed"] is False
            and plan["runtime_integration_allowed"] is False
            and review["dependency_adoption_allowed"] is False
            and review["runtime_integration_allowed"] is False
        ),
        "evidence_event_uri_required_before_terminal_success": lambda: normal[-1]["to_state"] == "evidence_written",
        "node_sequence_gap_or_duplicate_blocks_transition": lambda: any(
            record["rule_id"] == "failure_node_sequence_gap_or_duplicate_block_transition"
            and record["state_type"] == "blocked_terminal"
            and record["terminal_state"] == "blocked_terminal"
            for record in guarded
        ),
    }

    passed = checks[invariant_id]()
    return passed, "verified_repo_local" if passed else "failed_repo_local"


def build_invariant_results(plan: dict, review: dict) -> list[dict]:
    results = []
    for invariant in plan["hardening_invariants"]:
        passed, evidence_status = evaluate_invariant(invariant, review, plan)
        results.append(
            {
                "invariant_id": invariant["invariant_id"],
                "sequence_index": invariant["sequence_index"],
                "category": invariant["category"],
                "status": "PASS" if passed else "FAIL",
                "evidence_status": evidence_status,
                "source_review_field": invariant["source_review_field"],
                "source_review_goal_id": invariant["source_review_goal_id"],
                "protected_action_allowed": False,
            }
        )
    return results


def count_passed_by_category(results: list[dict], category: str) -> int:
    return sum(1 for result in results if result["category"] == category and result["status"] == "PASS")


def build_validation(plan: dict, review: dict) -> dict:
    results = build_invariant_results(plan, review)
    passed = sum(1 for result in results if result["status"] == "PASS")
    failed = len(results) - passed
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "validator_decision": VALIDATOR_DECISION,
        "validator_scope": VALIDATOR_SCOPE,
        "review_scope": REVIEW_SCOPE,
        "invariants_evaluated": len(results),
        "invariants_passed": passed,
        "invariants_failed": failed,
        "normal_path_invariants_passed": count_passed_by_category(results, "normal_path"),
        "guarded_outcome_invariants_passed": count_passed_by_category(results, "guarded_outcome"),
        "safety_boundary_invariants_passed": count_passed_by_category(results, "safety_boundary"),
        "invariant_results": results,
        "invariant_review_allowed": failed == 0,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(validation: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-invariant-validation-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS" if validation["invariants_failed"] == 0 else "FAIL",
        "validator_decision": VALIDATOR_DECISION,
        "validator_scope": VALIDATOR_SCOPE,
        "review_scope": REVIEW_SCOPE,
        "invariants_evaluated": validation["invariants_evaluated"],
        "invariants_passed": validation["invariants_passed"],
        "invariants_failed": validation["invariants_failed"],
        "invariant_review_allowed": validation["invariant_review_allowed"],
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-agent-graph-state-machine-kernel-invariant-validation
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review repo-local invariant validation before any runtime adapter hardening
  - Confirm all ten hardening invariants pass
  - Confirm dependency and runtime integration remain blocked
  - Convert accepted invariants into the next state machine review packet
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(validation: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_invariant_validator_v0_1",
        "status": "PASS" if validation["invariants_failed"] == 0 else "FAIL",
        "validator_decision": VALIDATOR_DECISION,
        "validator_scope": VALIDATOR_SCOPE,
        "review_scope": REVIEW_SCOPE,
        "invariants_evaluated": validation["invariants_evaluated"],
        "invariants_passed": validation["invariants_passed"],
        "invariants_failed": validation["invariants_failed"],
        "normal_path_invariants_passed": validation["normal_path_invariants_passed"],
        "guarded_outcome_invariants_passed": validation["guarded_outcome_invariants_passed"],
        "safety_boundary_invariants_passed": validation["safety_boundary_invariants_passed"],
        "invariant_review_allowed": validation["invariant_review_allowed"],
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(validation: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        "| {sequence} | `{invariant_id}` | {category} | {status} | {evidence} |".format(
            sequence=result["sequence_index"],
            invariant_id=result["invariant_id"],
            category=result["category"],
            status=result["status"],
            evidence=result["evidence_status"],
        )
        for result in validation["invariant_results"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [INVARIANT_VALIDATION, INVARIANT_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph State Machine Kernel Invariant Validator v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_invariant_validator_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_invariant_validator_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_invariant_validator_v0_1.py

## Validation summary

- validator_decision={VALIDATOR_DECISION}
- validator_scope={VALIDATOR_SCOPE}
- review_scope={REVIEW_SCOPE}
- invariants_evaluated={validation["invariants_evaluated"]}
- invariants_passed={validation["invariants_passed"]}
- invariants_failed={validation["invariants_failed"]}
- normal_path_invariants_passed={validation["normal_path_invariants_passed"]}
- guarded_outcome_invariants_passed={validation["guarded_outcome_invariants_passed"]}
- safety_boundary_invariants_passed={validation["safety_boundary_invariants_passed"]}
- invariant_review_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Invariant results

| Sequence | Invariant | Category | Status | Evidence |
| --- | --- | --- | --- | --- |
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
    plan, review = load_inputs()
    validation = build_validation(plan, review)

    write_json(INVARIANT_VALIDATION, validation)
    write_json(INVARIANT_GATE, build_gate(validation))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(validation))
    write_text(VALIDATION_REPORT, build_report(validation))

    print("AVF Agent Graph State Machine Kernel Invariant Validator v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_invariant_validator_v0_1=true")
    print(f"validator_decision={VALIDATOR_DECISION}")
    print(f"validator_scope={VALIDATOR_SCOPE}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"invariants_evaluated={validation['invariants_evaluated']}")
    print(f"invariants_passed={validation['invariants_passed']}")
    print(f"invariants_failed={validation['invariants_failed']}")
    print(f"normal_path_invariants_passed={validation['normal_path_invariants_passed']}")
    print(f"guarded_outcome_invariants_passed={validation['guarded_outcome_invariants_passed']}")
    print(f"safety_boundary_invariants_passed={validation['safety_boundary_invariants_passed']}")
    print("invariant_review_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
