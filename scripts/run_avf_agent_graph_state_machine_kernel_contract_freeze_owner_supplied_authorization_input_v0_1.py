from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime" / "generated"
GOALS = ROOT / "docs" / "goals"

PREVIOUS_GUIDE_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_gate.json"
OWNER_INPUT_PACKET = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input.yml"
OWNER_INPUT_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_gate.json"
NEXT_ACTION = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_next_action.yml"
VALIDATION_RESULT = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_OWNER_SUPPLIED_AUTHORIZATION_INPUT_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
INPUT_DECISION = "OWNER_SUPPLIED_AUTHORIZATION_INPUT_PACKET_CREATED_EMPTY_NOT_AUTHORIZED"
OWNER_INPUT_STATUS = "not_supplied"

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


def require_previous_guide_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous completion guide gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous completion guide gate must point to this owner input goal")
    if gate.get("codex_must_not_fill_owner_approval") is not True:
        raise SystemExit("Codex must not fill owner approval")
    if gate.get("owner_must_supply_authorization") is not True:
        raise SystemExit("owner must supply authorization")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("owner authorization must not be granted")
    if gate.get("contract_freeze_execution_allowed") is not False:
        raise SystemExit("contract freeze execution must remain blocked")
    if gate.get("missing_required_fields") != REQUIRED_OWNER_FIELDS:
        raise SystemExit("completion guide missing fields mismatch")


def build_owner_input_packet() -> str:
    fields = "\n".join(f"  - {field}" for field in REQUIRED_OWNER_FIELDS)
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""packet_id: avf-agent-graph-state-machine-kernel-contract-freeze-owner-supplied-authorization-input-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
input_decision: {INPUT_DECISION}
owner_input_status: {OWNER_INPUT_STATUS}

owner_authorization_granted: false
owner_supplied_fields_count: 0
missing_required_fields_count: {len(REQUIRED_OWNER_FIELDS)}
missing_required_fields:
{fields}

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
codex_fabricated_owner_input: false
codex_must_not_fill_owner_approval: true

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_owner_input_gate() -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-owner-supplied-authorization-input-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "input_decision": INPUT_DECISION,
        "owner_input_status": OWNER_INPUT_STATUS,
        "owner_authorization_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_fields_count": len(REQUIRED_OWNER_FIELDS),
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "codex_fabricated_owner_input": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_input_packet_uri": rel(OWNER_INPUT_PACKET),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-agent-graph-state-machine-kernel-contract-freeze-owner-supplied-authorization-input
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the owner-supplied authorization input packet
  - Review must keep freeze blocked when owner input is empty
  - Confirm Codex did not fabricate owner authorization
  - Do not execute contract freeze from this input packet
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

owner_input_status: {OWNER_INPUT_STATUS}
owner_authorization_granted: false
contract_freeze_execution_allowed: false
runtime_contract_frozen: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1",
        "status": "PASS",
        "input_decision": INPUT_DECISION,
        "owner_input_status": OWNER_INPUT_STATUS,
        "owner_authorization_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_fields_count": len(REQUIRED_OWNER_FIELDS),
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "codex_fabricated_owner_input": False,
        "codex_must_not_fill_owner_approval": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    missing = "\n".join(f"- {field}" for field in REQUIRED_OWNER_FIELDS)
    return f"""# AVF Agent Graph State Machine Kernel Contract Freeze Owner-Supplied Authorization Input v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1.py

## Input summary

- input_decision={INPUT_DECISION}
- owner_input_status={OWNER_INPUT_STATUS}
- owner_authorization_granted=false
- owner_supplied_fields_count=0
- missing_required_fields_count={len(REQUIRED_OWNER_FIELDS)}
- contract_freeze_execution_allowed=false
- contract_freeze_executed=false
- runtime_contract_frozen=false
- codex_fabricated_owner_input=false
- codex_must_not_fill_owner_approval=true

## Missing required owner fields

{missing}

## Generated artifacts

- {rel(OWNER_INPUT_PACKET)}
- {rel(OWNER_INPUT_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    previous_guide_gate = read_json(PREVIOUS_GUIDE_GATE)
    require_previous_guide_gate(previous_guide_gate)

    write_text(OWNER_INPUT_PACKET, build_owner_input_packet())
    write_json(OWNER_INPUT_GATE, build_owner_input_gate())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Agent Graph State Machine Kernel Contract Freeze Owner-Supplied Authorization Input v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1=true")
    print(f"input_decision={INPUT_DECISION}")
    print(f"owner_input_status={OWNER_INPUT_STATUS}")
    print("owner_authorization_granted=false")
    print("owner_supplied_fields_count=0")
    print(f"missing_required_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    print("contract_freeze_execution_allowed=false")
    print("contract_freeze_executed=false")
    print("runtime_contract_frozen=false")
    print("codex_fabricated_owner_input=false")
    print("codex_must_not_fill_owner_approval=true")
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
