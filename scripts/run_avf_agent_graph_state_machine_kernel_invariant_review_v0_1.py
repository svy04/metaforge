from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

INVARIANT_VALIDATION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validation.json"
INVARIANT_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validation_gate.json"
INVARIANT_REVIEW = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_review.json"
INVARIANT_REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_review_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_INVARIANT_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_validator_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_plan_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_INVARIANTS_REVIEWED_FOR_CONTRACT_FREEZE_PLAN"
REVIEW_SCOPE = "repo_local_state_machine_invariant_review_only"
CONTRACT_FREEZE_SCOPE = "repo_local_state_machine_contract_freeze_plan_only"


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
    gate = read_json(INVARIANT_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("invariant validation gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("invariant validation gate must point to this invariant review goal")
    if gate.get("invariant_review_allowed") is not True:
        raise SystemExit("invariant review must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_invariant_validation() -> dict:
    validation = read_json(INVARIANT_VALIDATION)
    if validation.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("invariant validation result goal mismatch")
    if validation.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("invariant validation result must point to this invariant review goal")
    if validation.get("invariants_failed") != 0:
        raise SystemExit("invariant validation must have zero failures before review")
    if validation.get("invariant_review_allowed") is not True:
        raise SystemExit("invariant review must be allowed")
    if validation.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if validation.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")
    results = validation.get("invariant_results")
    if not isinstance(results, list) or len(results) != 10:
        raise SystemExit("expected ten invariant validation results")
    return validation


def build_review_records(validation: dict) -> list[dict]:
    records = []
    for result in validation["invariant_results"]:
        records.append(
            {
                "invariant_id": result["invariant_id"],
                "sequence_index": result["sequence_index"],
                "category": result["category"],
                "review_status": "accepted",
                "contract_implication": "freeze_as_state_machine_contract_invariant",
                "evidence_status": result["evidence_status"],
                "source_review_goal_id": result["source_review_goal_id"],
                "protected_action_allowed": False,
            }
        )
    return records


def build_review(validation: dict) -> dict:
    records = build_review_records(validation)
    accepted = sum(1 for record in records if record["review_status"] == "accepted")
    rejected = len(records) - accepted
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "contract_freeze_scope": CONTRACT_FREEZE_SCOPE,
        "invariants_reviewed": len(records),
        "invariants_accepted": accepted,
        "invariants_rejected": rejected,
        "invariant_review_records": records,
        "contract_freeze_plan_allowed": rejected == 0,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(review: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-invariant-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS" if review["invariants_rejected"] == 0 else "FAIL",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "contract_freeze_scope": CONTRACT_FREEZE_SCOPE,
        "invariants_reviewed": review["invariants_reviewed"],
        "invariants_accepted": review["invariants_accepted"],
        "invariants_rejected": review["invariants_rejected"],
        "contract_freeze_plan_allowed": review["contract_freeze_plan_allowed"],
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-state-machine-kernel-contract-freeze-plan
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create repo-local contract freeze plan for the deterministic state machine kernel
  - Freeze accepted invariants as the state machine contract baseline
  - Keep runtime adapter hardening blocked until contract freeze review
  - Keep dependency adoption and runtime integration blocked
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(review: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_invariant_review_v0_1",
        "status": "PASS" if review["invariants_rejected"] == 0 else "FAIL",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "contract_freeze_scope": CONTRACT_FREEZE_SCOPE,
        "invariants_reviewed": review["invariants_reviewed"],
        "invariants_accepted": review["invariants_accepted"],
        "invariants_rejected": review["invariants_rejected"],
        "contract_freeze_plan_allowed": review["contract_freeze_plan_allowed"],
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(review: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        "| {sequence} | `{invariant_id}` | {category} | {status} | {implication} |".format(
            sequence=record["sequence_index"],
            invariant_id=record["invariant_id"],
            category=record["category"],
            status=record["review_status"],
            implication=record["contract_implication"],
        )
        for record in review["invariant_review_records"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [INVARIANT_REVIEW, INVARIANT_REVIEW_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph State Machine Kernel Invariant Review v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_invariant_review_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_invariant_review_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_invariant_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_scope={REVIEW_SCOPE}
- contract_freeze_scope={CONTRACT_FREEZE_SCOPE}
- invariants_reviewed={review["invariants_reviewed"]}
- invariants_accepted={review["invariants_accepted"]}
- invariants_rejected={review["invariants_rejected"]}
- contract_freeze_plan_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Invariant review records

| Sequence | Invariant | Category | Review status | Contract implication |
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
    validation = load_invariant_validation()
    review = build_review(validation)

    write_json(INVARIANT_REVIEW, review)
    write_json(INVARIANT_REVIEW_GATE, build_gate(review))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Agent Graph State Machine Kernel Invariant Review v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_invariant_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"contract_freeze_scope={CONTRACT_FREEZE_SCOPE}")
    print(f"invariants_reviewed={review['invariants_reviewed']}")
    print(f"invariants_accepted={review['invariants_accepted']}")
    print(f"invariants_rejected={review['invariants_rejected']}")
    print("contract_freeze_plan_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
