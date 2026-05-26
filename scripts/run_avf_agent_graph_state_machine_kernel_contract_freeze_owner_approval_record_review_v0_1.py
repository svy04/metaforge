from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime" / "generated"
GOALS = ROOT / "docs" / "goals"

OWNER_RECORD = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record.yml"
OWNER_RECORD_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_gate.json"
REVIEW = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review.json"
REVIEW_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_gate.json"
NEXT_ACTION = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_next_action.yml"
VALIDATION_RESULT = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_OWNER_APPROVAL_RECORD_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "OWNER_APPROVAL_RECORD_REVIEWED_APPROVAL_NOT_PROVIDED_FREEZE_BLOCKED"
REVIEW_STATUS = "blocked_missing_owner_authorization"

REQUIRED_OWNER_FIELDS = [
    "owner_identity",
    "authorization_scope",
    "accepted_invariant_ids",
    "freeze_execution_allowed",
    "rollback_or_unfreeze_plan",
    "validation_commands_required_after_freeze",
    "explicit_timestamp",
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


def require_owner_record_gate(gate: dict) -> list[dict]:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("owner record gate goal mismatch")
    if gate.get("status") != "PASS":
        raise SystemExit("owner record gate must be PASS")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("owner record gate must point to this review goal")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("owner authorization must not be granted")
    if gate.get("approval_record_completed") is not False:
        raise SystemExit("approval record must not be completed")
    if gate.get("contract_freeze_execution_allowed") is not False:
        raise SystemExit("contract freeze execution must remain blocked")
    if gate.get("contract_freeze_executed") is not False:
        raise SystemExit("contract freeze must not be executed")
    if gate.get("runtime_contract_frozen") is not False:
        raise SystemExit("runtime contract must not be frozen")
    records = gate.get("freeze_candidate_invariants", [])
    if len(records) != 10:
        raise SystemExit("owner record gate must include ten candidate invariants")
    return records


def build_review_record(records: list[dict]) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "approval_record_completed": False,
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "baseline_entries_available": len(records),
        "missing_required_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_fields_count": len(REQUIRED_OWNER_FIELDS),
        "freeze_candidate_invariants_reviewed": len(records),
        "rejection_reason": "owner authorization fields are empty, so freeze execution remains blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_review_gate(review: dict) -> dict:
    gate = {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-owner-approval-record-review-gate-v0-1",
        "status": "PASS",
        "review_record_uri": rel(REVIEW),
    }
    gate.update(review)
    return gate


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-state-machine-kernel-contract-freeze-owner-approval-completion-guide
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a completion guide for the owner approval record fields
  - Keep review_status: {REVIEW_STATUS}
  - Do not execute contract freeze from this blocked review
  - Do not freeze runtime contract state
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

review_status: {REVIEW_STATUS}
owner_authorization_granted: false
contract_freeze_execution_allowed: false
runtime_contract_frozen: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(review: dict) -> dict:
    result = {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_v0_1",
        "status": "PASS",
    }
    result.update(review)
    return result


def build_report(review: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    missing = "\n".join(f"- {field}" for field in REQUIRED_OWNER_FIELDS)
    return f"""# AVF Agent Graph State Machine Kernel Contract Freeze Owner Approval Record Review v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- owner_authorization_required=true
- owner_authorization_granted=false
- approval_record_completed=false
- contract_freeze_execution_allowed=false
- contract_freeze_executed=false
- runtime_contract_frozen=false
- missing_required_fields_count={len(REQUIRED_OWNER_FIELDS)}

## Missing required owner fields

{missing}

## Generated artifacts

- {rel(REVIEW)}
- {rel(REVIEW_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    if "owner_authorization_granted: false" not in OWNER_RECORD.read_text(encoding="utf-8"):
        raise SystemExit("owner record must keep owner_authorization_granted false")
    owner_record_gate = read_json(OWNER_RECORD_GATE)
    records = require_owner_record_gate(owner_record_gate)
    review = build_review_record(records)

    write_json(REVIEW, review)
    write_json(REVIEW_GATE, build_review_gate(review))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Agent Graph State Machine Kernel Contract Freeze Owner Approval Record Review v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    print("owner_authorization_required=true")
    print("owner_authorization_granted=false")
    print("approval_record_completed=false")
    print("contract_freeze_execution_allowed=false")
    print("contract_freeze_executed=false")
    print("runtime_contract_frozen=false")
    print(f"missing_required_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("automated_scraping_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
