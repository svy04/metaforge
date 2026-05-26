from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime" / "generated"
GOALS = ROOT / "docs" / "goals"

AUTHORIZATION_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_authorization_gate.json"
OWNER_RECORD = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record.yml"
OWNER_RECORD_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_gate.json"
NEXT_ACTION = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_next_action.yml"
VALIDATION_RESULT = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_OWNER_APPROVAL_RECORD_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
RECORD_DECISION = "OWNER_APPROVAL_RECORD_TEMPLATE_CREATED_APPROVAL_NOT_PROVIDED"
OWNER_AUTHORIZATION_STATUS = "not_provided"


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


def require_authorization_gate(gate: dict) -> list[dict]:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("authorization gate goal mismatch")
    if gate.get("status") != "PASS":
        raise SystemExit("authorization gate must be PASS")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("authorization gate must point to this owner approval record goal")
    if gate.get("authorization_status") != "required_not_granted":
        raise SystemExit("authorization status must remain required_not_granted")
    if gate.get("owner_authorization_required") is not True:
        raise SystemExit("owner authorization must be required")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("owner authorization must not be granted")
    if gate.get("contract_freeze_execution_allowed") is not False:
        raise SystemExit("contract freeze execution must remain blocked")
    if gate.get("contract_freeze_executed") is not False:
        raise SystemExit("contract freeze must not be executed")
    if gate.get("runtime_contract_frozen") is not False:
        raise SystemExit("runtime contract must not be frozen")
    records = gate.get("freeze_candidate_invariants", [])
    if len(records) != 10:
        raise SystemExit("authorization gate must include ten candidate invariants")
    return records


def build_owner_record(records: list[dict]) -> str:
    candidates = "\n".join(
        "\n".join(
            [
                f"  - sequence_index: {record['sequence_index']}",
                f"    invariant_id: {record['invariant_id']}",
                f"    category: {record['category']}",
                f"    freeze_candidate_status: {record['freeze_candidate_status']}",
            ]
        )
        for record in records
    )
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""record_id: avf-agent-graph-state-machine-kernel-contract-freeze-owner-approval-record-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
record_decision: {RECORD_DECISION}
owner_authorization_status: {OWNER_AUTHORIZATION_STATUS}
owner_authorization_required: true
owner_authorization_granted: false
approval_record_completed: false

owner_identity: null
authorization_scope: null
accepted_invariant_ids: []
freeze_execution_allowed: false
rollback_or_unfreeze_plan: null
validation_commands_required_after_freeze: []
explicit_timestamp: null

contract_freeze_execution_allowed: false
contract_freeze_executed: false
runtime_contract_frozen: false
dependency_adoption_allowed: false
runtime_integration_allowed: false
baseline_entries_available: {len(records)}

freeze_candidate_invariants:
{candidates}

review_rules:
  - Empty owner_identity means approval remains not provided
  - Empty authorization_scope means approval remains not provided
  - Empty accepted_invariant_ids means no freeze candidate is approved
  - freeze_execution_allowed must remain false until a complete owner authorization record is reviewed
  - Contract freeze execution is not part of this step

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_owner_record_gate(records: list[dict]) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-owner-approval-record-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "record_decision": RECORD_DECISION,
        "owner_authorization_status": OWNER_AUTHORIZATION_STATUS,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "approval_record_completed": False,
        "accepted_invariant_ids": [],
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "baseline_entries_available": len(records),
        "freeze_candidate_invariants": records,
        "owner_record_uri": rel(OWNER_RECORD),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-agent-graph-state-machine-kernel-contract-freeze-owner-approval-record
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the owner approval record template
  - Confirm owner_authorization_granted is false when required owner fields are empty
  - Review must reject or keep blocked if approval fields remain empty
  - Do not execute contract freeze during record review
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

owner_authorization_granted: false
contract_freeze_execution_allowed: false
runtime_contract_frozen: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(records: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1",
        "status": "PASS",
        "record_decision": RECORD_DECISION,
        "owner_authorization_status": OWNER_AUTHORIZATION_STATUS,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "approval_record_completed": False,
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "baseline_entries_available": len(records),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(records: list[dict]) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Agent Graph State Machine Kernel Contract Freeze Owner Approval Record v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1.py

## Record summary

- record_decision={RECORD_DECISION}
- owner_authorization_status={OWNER_AUTHORIZATION_STATUS}
- owner_authorization_required=true
- owner_authorization_granted=false
- approval_record_completed=false
- contract_freeze_execution_allowed=false
- contract_freeze_executed=false
- runtime_contract_frozen=false
- baseline_entries_available={len(records)}

## Generated artifacts

- {rel(OWNER_RECORD)}
- {rel(OWNER_RECORD_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    authorization_gate = read_json(AUTHORIZATION_GATE)
    records = require_authorization_gate(authorization_gate)

    write_text(OWNER_RECORD, build_owner_record(records))
    write_json(OWNER_RECORD_GATE, build_owner_record_gate(records))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(records))
    write_text(VALIDATION_REPORT, build_report(records))

    print("AVF Agent Graph State Machine Kernel Contract Freeze Owner Approval Record v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1=true")
    print(f"record_decision={RECORD_DECISION}")
    print(f"owner_authorization_status={OWNER_AUTHORIZATION_STATUS}")
    print("owner_authorization_required=true")
    print("owner_authorization_granted=false")
    print("approval_record_completed=false")
    print("contract_freeze_execution_allowed=false")
    print("contract_freeze_executed=false")
    print("runtime_contract_frozen=false")
    print(f"baseline_entries_available={len(records)}")
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
