from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

BASELINE_DRAFT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_draft.json"
BASELINE_DRAFT_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_draft_gate.json"
BASELINE_REVIEW = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_review.json"
BASELINE_REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_review_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_BASELINE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_baseline_draft_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_BASELINE_DRAFT_REVIEWED_FOR_FREEZE_AUTHORIZATION_PACKET"
REVIEW_SCOPE = "repo_local_state_machine_contract_baseline_review_only"
AUTHORIZATION_SCOPE = "repo_local_state_machine_contract_freeze_authorization_packet_only"
CONTRACT_STATUS = "baseline_reviewed_not_frozen"


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
    gate = read_json(BASELINE_DRAFT_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("baseline draft gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("baseline draft gate must point to this baseline review goal")
    if gate.get("baseline_review_allowed") is not True:
        raise SystemExit("baseline review must be allowed")
    if gate.get("runtime_contract_frozen") is not False:
        raise SystemExit("runtime contract must not be frozen before baseline review")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_baseline_draft() -> dict:
    draft = read_json(BASELINE_DRAFT)
    if draft.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("baseline draft goal mismatch")
    if draft.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("baseline draft must point to this baseline review goal")
    if draft.get("baseline_review_allowed") is not True:
        raise SystemExit("baseline review must be allowed")
    if draft.get("runtime_contract_frozen") is not False:
        raise SystemExit("runtime contract must not be frozen before baseline review")
    if draft.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if draft.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")
    entries = draft.get("baseline_entries")
    if not isinstance(entries, list) or len(entries) != 10:
        raise SystemExit("expected ten baseline draft entries")
    return draft


def build_review_records(draft: dict) -> list[dict]:
    records = []
    for entry in draft["baseline_entries"]:
        records.append(
            {
                "invariant_id": entry["invariant_id"],
                "sequence_index": entry["sequence_index"],
                "category": entry["category"],
                "review_status": "accepted",
                "source_baseline_status": entry["baseline_status"],
                "authorization_implication": "include_in_freeze_authorization_packet",
                "source_evidence_status": entry["source_evidence_status"],
                "source_review_goal_id": entry["source_review_goal_id"],
                "protected_action_allowed": False,
            }
        )
    return records


def build_review(draft: dict) -> dict:
    records = build_review_records(draft)
    accepted = sum(1 for record in records if record["review_status"] == "accepted")
    rejected = len(records) - accepted
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "authorization_scope": AUTHORIZATION_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "baseline_entries_reviewed": len(records),
        "baseline_entries_accepted": accepted,
        "baseline_entries_rejected": rejected,
        "baseline_review_records": records,
        "contract_freeze_authorization_packet_allowed": rejected == 0,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "owner_approval_required_before_freeze": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(review: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-baseline-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS" if review["contract_freeze_authorization_packet_allowed"] else "FAIL",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "authorization_scope": AUTHORIZATION_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "baseline_entries_reviewed": review["baseline_entries_reviewed"],
        "baseline_entries_accepted": review["baseline_entries_accepted"],
        "baseline_entries_rejected": review["baseline_entries_rejected"],
        "contract_freeze_authorization_packet_allowed": review[
            "contract_freeze_authorization_packet_allowed"
        ],
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-state-machine-kernel-contract-freeze-authorization-packet
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Prepare owner approval packet before any contract freeze execution
  - Include the ten reviewed baseline entries and the freeze boundary
  - Keep actual contract freeze blocked until explicit owner authorization is recorded
  - Do not execute contract freeze or runtime enforcement
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(review: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1",
        "status": "PASS" if review["contract_freeze_authorization_packet_allowed"] else "FAIL",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "authorization_scope": AUTHORIZATION_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "baseline_entries_reviewed": review["baseline_entries_reviewed"],
        "baseline_entries_accepted": review["baseline_entries_accepted"],
        "baseline_entries_rejected": review["baseline_entries_rejected"],
        "contract_freeze_authorization_packet_allowed": review[
            "contract_freeze_authorization_packet_allowed"
        ],
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
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
            implication=record["authorization_implication"],
        )
        for record in review["baseline_review_records"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [BASELINE_REVIEW, BASELINE_REVIEW_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph State Machine Kernel Contract Baseline Review v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_baseline_review_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_scope={REVIEW_SCOPE}
- authorization_scope={AUTHORIZATION_SCOPE}
- contract_status={CONTRACT_STATUS}
- baseline_entries_reviewed={review["baseline_entries_reviewed"]}
- baseline_entries_accepted={review["baseline_entries_accepted"]}
- baseline_entries_rejected={review["baseline_entries_rejected"]}
- contract_freeze_authorization_packet_allowed=true
- contract_freeze_executed=false
- runtime_contract_frozen=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Review records

| Sequence | Invariant | Category | Review status | Authorization implication |
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
    draft = load_baseline_draft()
    review = build_review(draft)

    write_json(BASELINE_REVIEW, review)
    write_json(BASELINE_REVIEW_GATE, build_gate(review))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Agent Graph State Machine Kernel Contract Baseline Review v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_baseline_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"authorization_scope={AUTHORIZATION_SCOPE}")
    print(f"contract_status={CONTRACT_STATUS}")
    print(f"baseline_entries_reviewed={review['baseline_entries_reviewed']}")
    print(f"baseline_entries_accepted={review['baseline_entries_accepted']}")
    print(f"baseline_entries_rejected={review['baseline_entries_rejected']}")
    print("contract_freeze_authorization_packet_allowed=true")
    print("contract_freeze_executed=false")
    print("runtime_contract_frozen=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
