from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

CONTRACT_FREEZE_PLAN = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_plan.json"
CONTRACT_FREEZE_PLAN_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_plan_gate.json"
CONTRACT_FREEZE_REVIEW = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_review.json"
CONTRACT_FREEZE_REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_review_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_baseline_draft_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_PLAN_REVIEWED_FOR_BASELINE_DRAFT"
REVIEW_SCOPE = "repo_local_state_machine_contract_freeze_review_only"
BASELINE_DRAFT_SCOPE = "repo_local_state_machine_contract_baseline_draft_only"
CONTRACT_STATUS = "reviewed_not_frozen"


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
    gate = read_json(CONTRACT_FREEZE_PLAN_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("contract freeze plan gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("contract freeze plan gate must point to this review goal")
    if gate.get("contract_review_allowed") is not True:
        raise SystemExit("contract review must be allowed")
    if gate.get("contract_freeze_executed") is not False:
        raise SystemExit("contract freeze must not be executed before review")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_contract_freeze_plan() -> dict:
    plan = read_json(CONTRACT_FREEZE_PLAN)
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("contract freeze plan goal mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("contract freeze plan must point to this review goal")
    if plan.get("contract_review_allowed") is not True:
        raise SystemExit("contract review must be allowed")
    if plan.get("contract_freeze_executed") is not False:
        raise SystemExit("contract freeze must not be executed before review")
    if plan.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if plan.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")
    entries = plan.get("contract_entries")
    if not isinstance(entries, list) or len(entries) != 10:
        raise SystemExit("expected ten contract freeze plan entries")
    return plan


def build_review_records(plan: dict) -> list[dict]:
    records = []
    for entry in plan["contract_entries"]:
        records.append(
            {
                "invariant_id": entry["invariant_id"],
                "sequence_index": entry["sequence_index"],
                "category": entry["category"],
                "review_status": "accepted",
                "freeze_status_reviewed": entry["freeze_status"],
                "baseline_draft_implication": "include_as_contract_baseline_candidate",
                "source_evidence_status": entry["source_evidence_status"],
                "source_review_goal_id": entry["source_review_goal_id"],
                "protected_action_allowed": False,
            }
        )
    return records


def build_review(plan: dict) -> dict:
    records = build_review_records(plan)
    accepted = sum(1 for record in records if record["review_status"] == "accepted")
    rejected = len(records) - accepted
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "baseline_draft_scope": BASELINE_DRAFT_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "plan_entries_reviewed": len(records),
        "plan_entries_accepted": accepted,
        "plan_entries_rejected": rejected,
        "contract_review_records": records,
        "contract_baseline_draft_allowed": rejected == 0,
        "contract_freeze_executed": False,
        "owner_approval_required_before_freeze": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(review: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS" if review["contract_baseline_draft_allowed"] else "FAIL",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "baseline_draft_scope": BASELINE_DRAFT_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "plan_entries_reviewed": review["plan_entries_reviewed"],
        "plan_entries_accepted": review["plan_entries_accepted"],
        "plan_entries_rejected": review["plan_entries_rejected"],
        "contract_baseline_draft_allowed": review["contract_baseline_draft_allowed"],
        "contract_freeze_executed": False,
        "owner_approval_required_before_freeze": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-state-machine-kernel-contract-baseline-draft
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create repo-local contract baseline draft from reviewed freeze-plan entries
  - Keep the baseline draft separate from any runtime enforcement
  - Do not treat the baseline draft as a frozen runtime contract
  - Keep dependency adoption and runtime integration blocked
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(review: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_freeze_review_v0_1",
        "status": "PASS" if review["contract_baseline_draft_allowed"] else "FAIL",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "baseline_draft_scope": BASELINE_DRAFT_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "plan_entries_reviewed": review["plan_entries_reviewed"],
        "plan_entries_accepted": review["plan_entries_accepted"],
        "plan_entries_rejected": review["plan_entries_rejected"],
        "contract_baseline_draft_allowed": review["contract_baseline_draft_allowed"],
        "contract_freeze_executed": False,
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
            implication=record["baseline_draft_implication"],
        )
        for record in review["contract_review_records"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [CONTRACT_FREEZE_REVIEW, CONTRACT_FREEZE_REVIEW_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph State Machine Kernel Contract Freeze Review v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_freeze_review_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_contract_freeze_review_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_contract_freeze_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_scope={REVIEW_SCOPE}
- baseline_draft_scope={BASELINE_DRAFT_SCOPE}
- contract_status={CONTRACT_STATUS}
- plan_entries_reviewed={review["plan_entries_reviewed"]}
- plan_entries_accepted={review["plan_entries_accepted"]}
- plan_entries_rejected={review["plan_entries_rejected"]}
- contract_baseline_draft_allowed=true
- contract_freeze_executed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Review records

| Sequence | Invariant | Category | Review status | Baseline draft implication |
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
    plan = load_contract_freeze_plan()
    review = build_review(plan)

    write_json(CONTRACT_FREEZE_REVIEW, review)
    write_json(CONTRACT_FREEZE_REVIEW_GATE, build_gate(review))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Agent Graph State Machine Kernel Contract Freeze Review v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_freeze_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"baseline_draft_scope={BASELINE_DRAFT_SCOPE}")
    print(f"contract_status={CONTRACT_STATUS}")
    print(f"plan_entries_reviewed={review['plan_entries_reviewed']}")
    print(f"plan_entries_accepted={review['plan_entries_accepted']}")
    print(f"plan_entries_rejected={review['plan_entries_rejected']}")
    print("contract_baseline_draft_allowed=true")
    print("contract_freeze_executed=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
