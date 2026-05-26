from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1.py"
AUTHORIZATION_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_authorization_gate.json"
OWNER_RECORD = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record.yml"
OWNER_RECORD_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_gate.json"
NEXT_ACTION = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_next_action.yml"
VALIDATION_RESULT = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_OWNER_APPROVAL_RECORD_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_v0_1"
RECORD_DECISION = "OWNER_APPROVAL_RECORD_TEMPLATE_CREATED_APPROVAL_NOT_PROVIDED"
OWNER_AUTHORIZATION_STATUS = "not_provided"

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "automated_scraping_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    AUTHORIZATION_GATE,
    OWNER_RECORD,
    OWNER_RECORD_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

OWNER_RECORD_MARKERS = [
    "record_id: avf-agent-graph-state-machine-kernel-contract-freeze-owner-approval-record-v0-1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"record_decision: {RECORD_DECISION}",
    f"owner_authorization_status: {OWNER_AUTHORIZATION_STATUS}",
    "owner_authorization_required: true",
    "owner_authorization_granted: false",
    "approval_record_completed: false",
    "contract_freeze_execution_allowed: false",
    "contract_freeze_executed: false",
    "runtime_contract_frozen: false",
    "baseline_entries_available: 10",
    "accepted_invariant_ids: []",
    "protected_action_executed: false",
    "runtime_integration_performed: false",
    "release_ready: false",
    "production_ready: false",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-agent-graph-state-machine-kernel-contract-freeze-owner-approval-record",
    "owner_approval_required_before_execution: true",
    "owner_authorization_granted: false",
    "contract_freeze_execution_allowed: false",
    "Review must reject or keep blocked if approval fields remain empty",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1=true",
    f"record_decision={RECORD_DECISION}",
    f"owner_authorization_status={OWNER_AUTHORIZATION_STATUS}",
    "owner_authorization_required=true",
    "owner_authorization_granted=false",
    "approval_record_completed=false",
    "contract_freeze_execution_allowed=false",
    "contract_freeze_executed=false",
    "runtime_contract_frozen=false",
    "baseline_entries_available=10",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph State Machine Kernel Contract Freeze Owner Approval Record v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_authorization_gate() -> None:
    gate = read_json(AUTHORIZATION_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("authorization gate goal_id mismatch")
    if gate.get("status") != "PASS":
        fail("authorization gate must be PASS")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("authorization gate must point to this owner approval record goal")
    if gate.get("authorization_status") != "required_not_granted":
        fail("authorization gate status must remain required_not_granted")
    if gate.get("owner_authorization_required") is not True:
        fail("authorization gate must require owner authorization")
    if gate.get("owner_authorization_granted") is not False:
        fail("authorization gate must not grant owner authorization")
    if gate.get("contract_freeze_execution_allowed") is not False:
        fail("authorization gate must block freeze execution")
    if gate.get("contract_freeze_executed") is not False:
        fail("authorization gate must not execute freeze")
    if gate.get("runtime_contract_frozen") is not False:
        fail("authorization gate must not freeze runtime contract")
    if len(gate.get("freeze_candidate_invariants", [])) != 10:
        fail("authorization gate must provide ten freeze candidate invariants")
    require_false_flags(gate.get("claim_boundary", {}), "authorization gate claim boundary")


def require_owner_record_gate() -> None:
    gate = read_json(OWNER_RECORD_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-owner-approval-record-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "record_decision": RECORD_DECISION,
        "owner_authorization_status": OWNER_AUTHORIZATION_STATUS,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "approval_record_completed": False,
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "baseline_entries_available": 10,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"owner record gate {key} mismatch")
    if gate.get("accepted_invariant_ids") != []:
        fail("owner record gate accepted invariant ids must remain empty")
    if len(gate.get("freeze_candidate_invariants", [])) != 10:
        fail("owner record gate must include ten candidate invariants")
    require_false_flags(gate.get("claim_boundary", {}), "owner record gate claim boundary")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
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
        "baseline_entries_available": 10,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            fail(f"validation result {key} mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result claim boundary")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_authorization_gate()
    require_text_markers(OWNER_RECORD, OWNER_RECORD_MARKERS)
    require_owner_record_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Agent Graph State Machine Kernel Contract Freeze Owner Approval Record v0.1 validation")
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
    print("baseline_entries_available=10")
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
