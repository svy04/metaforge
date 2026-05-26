from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1.py"
PREVIOUS_REVIEW = RUNTIME / "agent_graph_state_machine_kernel_contract_baseline_review.json"
PREVIOUS_REVIEW_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_baseline_review_gate.json"
AUTHORIZATION_PACKET = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_authorization_packet.yml"
AUTHORIZATION_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_authorization_gate.json"
NEXT_ACTION = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_authorization_next_action.yml"
VALIDATION_RESULT = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_AUTHORIZATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1"
AUTHORIZATION_DECISION = "CONTRACT_FREEZE_AUTHORIZATION_PACKET_READY_OWNER_APPROVAL_REQUIRED"
AUTHORIZATION_STATUS = "required_not_granted"

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
    PREVIOUS_REVIEW,
    PREVIOUS_REVIEW_GATE,
    AUTHORIZATION_PACKET,
    AUTHORIZATION_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    "packet_id: avf-agent-graph-state-machine-kernel-contract-freeze-authorization-packet-v0-1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"authorization_decision: {AUTHORIZATION_DECISION}",
    f"authorization_status: {AUTHORIZATION_STATUS}",
    "owner_authorization_required: true",
    "owner_authorization_granted: false",
    "contract_freeze_execution_allowed: false",
    "contract_freeze_executed: false",
    "runtime_contract_frozen: false",
    "dependency_adoption_allowed: false",
    "runtime_integration_allowed: false",
    "baseline_entries_included: 10",
    "protected_action_executed: false",
    "runtime_integration_performed: false",
    "release_ready: false",
    "production_ready: false",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-state-machine-kernel-contract-freeze-owner-approval-record",
    "owner_approval_required_before_execution: true",
    "contract_freeze_execution_allowed: false",
    "runtime_contract_frozen: false",
    "Do not execute the contract freeze until explicit owner authorization is recorded",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1=true",
    f"authorization_decision={AUTHORIZATION_DECISION}",
    f"authorization_status={AUTHORIZATION_STATUS}",
    "owner_authorization_required=true",
    "owner_authorization_granted=false",
    "contract_freeze_execution_allowed=false",
    "contract_freeze_executed=false",
    "runtime_contract_frozen=false",
    "baseline_entries_included=10",
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
    print("AVF Agent Graph State Machine Kernel Contract Freeze Authorization Packet v0.1 validation")
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


def require_previous_review() -> None:
    review = read_json(PREVIOUS_REVIEW)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous review goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous review must point to this authorization packet goal")
    if review.get("contract_status") != "baseline_reviewed_not_frozen":
        fail("previous review contract status mismatch")
    if review.get("baseline_entries_reviewed") != 10:
        fail("previous review baseline entries reviewed mismatch")
    if review.get("baseline_entries_accepted") != 10:
        fail("previous review baseline entries accepted mismatch")
    if review.get("baseline_entries_rejected") != 0:
        fail("previous review baseline entries rejected mismatch")
    if review.get("contract_freeze_authorization_packet_allowed") is not True:
        fail("previous review must allow authorization packet creation")
    if review.get("contract_freeze_executed") is not False:
        fail("previous review must not execute contract freeze")
    if review.get("runtime_contract_frozen") is not False:
        fail("previous review must not freeze runtime contract")
    records = review.get("baseline_review_records", [])
    if len(records) != 10:
        fail("previous review must carry ten baseline review records")
    if any(record.get("review_status") != "accepted" for record in records):
        fail("all baseline review records must be accepted")
    require_false_flags(review.get("claim_boundary", {}), "previous review claim boundary")


def require_previous_review_gate() -> None:
    gate = read_json(PREVIOUS_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous review gate goal_id mismatch")
    if gate.get("status") != "PASS":
        fail("previous review gate must be PASS")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous review gate must point to this authorization packet goal")
    if gate.get("contract_status") != "baseline_reviewed_not_frozen":
        fail("previous review gate contract status mismatch")
    if gate.get("contract_freeze_authorization_packet_allowed") is not True:
        fail("previous review gate must allow authorization packet creation")
    if gate.get("contract_freeze_executed") is not False:
        fail("previous review gate must not execute contract freeze")
    if gate.get("runtime_contract_frozen") is not False:
        fail("previous review gate must not freeze runtime contract")
    require_false_flags(gate.get("claim_boundary", {}), "previous review gate claim boundary")


def require_authorization_gate() -> None:
    gate = read_json(AUTHORIZATION_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-authorization-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "authorization_decision": AUTHORIZATION_DECISION,
        "authorization_status": AUTHORIZATION_STATUS,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "baseline_entries_included": 10,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"authorization gate {key} mismatch")
    if len(gate.get("freeze_candidate_invariants", [])) != 10:
        fail("authorization gate must include ten freeze candidate invariants")
    require_false_flags(gate.get("claim_boundary", {}), "authorization gate claim boundary")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1",
        "status": "PASS",
        "authorization_decision": AUTHORIZATION_DECISION,
        "authorization_status": AUTHORIZATION_STATUS,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "baseline_entries_included": 10,
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

    require_previous_review()
    require_previous_review_gate()
    require_text_markers(AUTHORIZATION_PACKET, PACKET_MARKERS)
    require_authorization_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Agent Graph State Machine Kernel Contract Freeze Authorization Packet v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1=true")
    print(f"authorization_decision={AUTHORIZATION_DECISION}")
    print(f"authorization_status={AUTHORIZATION_STATUS}")
    print("owner_authorization_required=true")
    print("owner_authorization_granted=false")
    print("contract_freeze_execution_allowed=false")
    print("contract_freeze_executed=false")
    print("runtime_contract_frozen=false")
    print("baseline_entries_included=10")
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
