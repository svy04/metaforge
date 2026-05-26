from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

INVARIANT_REVIEW = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_review.json"
INVARIANT_REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_review_gate.json"
CONTRACT_FREEZE_PLAN = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_plan.json"
CONTRACT_FREEZE_PLAN_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_plan_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_plan_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_PLAN_READY_FOR_REVIEW"
PLAN_SCOPE = "repo_local_state_machine_contract_freeze_plan_only"
CONTRACT_REVIEW_SCOPE = "repo_local_state_machine_contract_freeze_review_only"
CONTRACT_STATUS = "planned_not_frozen"


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
    gate = read_json(INVARIANT_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("invariant review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("invariant review gate must point to this contract freeze plan goal")
    if gate.get("contract_freeze_plan_allowed") is not True:
        raise SystemExit("contract freeze plan must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_invariant_review() -> dict:
    review = read_json(INVARIANT_REVIEW)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("invariant review result goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("invariant review result must point to this contract freeze plan goal")
    if review.get("invariants_rejected") != 0:
        raise SystemExit("invariant review must have zero rejections before freeze planning")
    if review.get("contract_freeze_plan_allowed") is not True:
        raise SystemExit("contract freeze plan must be allowed")
    if review.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if review.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")
    records = review.get("invariant_review_records")
    if not isinstance(records, list) or len(records) != 10:
        raise SystemExit("expected ten invariant review records")
    return review


def build_contract_entries(review: dict) -> list[dict]:
    entries = []
    for record in review["invariant_review_records"]:
        entries.append(
            {
                "invariant_id": record["invariant_id"],
                "sequence_index": record["sequence_index"],
                "category": record["category"],
                "freeze_status": "candidate_planned",
                "source_review_status": record["review_status"],
                "source_contract_implication": record["contract_implication"],
                "source_evidence_status": record["evidence_status"],
                "source_review_goal_id": record["source_review_goal_id"],
                "protected_action_allowed": False,
            }
        )
    return entries


def category_counts(entries: list[dict]) -> dict:
    counts = {"normal_path": 0, "guarded_outcome": 0, "safety_boundary": 0}
    for entry in entries:
        counts[entry["category"]] += 1
    return counts


def build_plan(review: dict) -> dict:
    entries = build_contract_entries(review)
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "plan_decision": PLAN_DECISION,
        "plan_scope": PLAN_SCOPE,
        "contract_review_scope": CONTRACT_REVIEW_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "invariants_planned_for_freeze": len(entries),
        "contract_entries_created": len(entries),
        "contract_entry_category_counts": category_counts(entries),
        "contract_entries": entries,
        "baseline_manifest_created": True,
        "contract_review_allowed": True,
        "contract_freeze_executed": False,
        "owner_approval_required_before_freeze": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(plan: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-plan-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS" if plan["contract_review_allowed"] else "FAIL",
        "plan_decision": PLAN_DECISION,
        "plan_scope": PLAN_SCOPE,
        "contract_review_scope": CONTRACT_REVIEW_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "invariants_planned_for_freeze": plan["invariants_planned_for_freeze"],
        "contract_entries_created": plan["contract_entries_created"],
        "contract_review_allowed": plan["contract_review_allowed"],
        "contract_freeze_executed": False,
        "owner_approval_required_before_freeze": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-agent-graph-state-machine-kernel-contract-freeze-plan
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review repo-local contract freeze plan before freezing any runtime contract
  - Confirm ten candidate invariants remain valid contract boundaries
  - Keep actual contract freeze blocked until review passes
  - Keep dependency adoption and runtime integration blocked
  - Do not freeze contracts, install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(plan: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_freeze_plan_v0_1",
        "status": "PASS" if plan["contract_review_allowed"] else "FAIL",
        "plan_decision": PLAN_DECISION,
        "plan_scope": PLAN_SCOPE,
        "contract_review_scope": CONTRACT_REVIEW_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "invariants_planned_for_freeze": plan["invariants_planned_for_freeze"],
        "contract_entries_created": plan["contract_entries_created"],
        "contract_review_allowed": plan["contract_review_allowed"],
        "contract_freeze_executed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(plan: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        "| {sequence} | `{invariant_id}` | {category} | {status} | {source_status} |".format(
            sequence=entry["sequence_index"],
            invariant_id=entry["invariant_id"],
            category=entry["category"],
            status=entry["freeze_status"],
            source_status=entry["source_review_status"],
        )
        for entry in plan["contract_entries"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [CONTRACT_FREEZE_PLAN, CONTRACT_FREEZE_PLAN_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph State Machine Kernel Contract Freeze Plan v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_freeze_plan_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_contract_freeze_plan_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_contract_freeze_plan_v0_1.py

## Plan summary

- plan_decision={PLAN_DECISION}
- plan_scope={PLAN_SCOPE}
- contract_review_scope={CONTRACT_REVIEW_SCOPE}
- contract_status={CONTRACT_STATUS}
- invariants_planned_for_freeze={plan["invariants_planned_for_freeze"]}
- contract_entries_created={plan["contract_entries_created"]}
- contract_review_allowed=true
- contract_freeze_executed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Contract entries

| Sequence | Invariant | Category | Freeze status | Source review status |
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
    review = load_invariant_review()
    plan = build_plan(review)

    write_json(CONTRACT_FREEZE_PLAN, plan)
    write_json(CONTRACT_FREEZE_PLAN_GATE, build_gate(plan))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plan))
    write_text(VALIDATION_REPORT, build_report(plan))

    print("AVF Agent Graph State Machine Kernel Contract Freeze Plan v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_freeze_plan_v0_1=true")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_scope={PLAN_SCOPE}")
    print(f"contract_review_scope={CONTRACT_REVIEW_SCOPE}")
    print(f"contract_status={CONTRACT_STATUS}")
    print(f"invariants_planned_for_freeze={plan['invariants_planned_for_freeze']}")
    print(f"contract_entries_created={plan['contract_entries_created']}")
    print("contract_review_allowed=true")
    print("contract_freeze_executed=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
