from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1.py"
PREVIOUS_GUIDE_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_gate.json"
OWNER_INPUT_PACKET = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input.yml"
OWNER_INPUT_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_gate.json"
NEXT_ACTION = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_next_action.yml"
VALIDATION_RESULT = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_OWNER_SUPPLIED_AUTHORIZATION_INPUT_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_v0_1"
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
    PREVIOUS_GUIDE_GATE,
    OWNER_INPUT_PACKET,
    OWNER_INPUT_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    "packet_id: avf-agent-graph-state-machine-kernel-contract-freeze-owner-supplied-authorization-input-v0-1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"input_decision: {INPUT_DECISION}",
    f"owner_input_status: {OWNER_INPUT_STATUS}",
    "owner_authorization_granted: false",
    "owner_supplied_fields_count: 0",
    "missing_required_fields_count: 7",
    "contract_freeze_execution_allowed: false",
    "contract_freeze_executed: false",
    "runtime_contract_frozen: false",
    "codex_fabricated_owner_input: false",
    "codex_must_not_fill_owner_approval: true",
    "owner_identity: null",
    "authorization_scope: null",
    "accepted_invariant_ids: []",
    "freeze_execution_allowed: false",
    "rollback_or_unfreeze_plan: null",
    "validation_commands_required_after_freeze: []",
    "explicit_timestamp: null",
    "protected_action_executed: false",
    "runtime_integration_performed: false",
    "release_ready: false",
    "production_ready: false",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-agent-graph-state-machine-kernel-contract-freeze-owner-supplied-authorization-input",
    "owner_approval_required_before_execution: true",
    "owner_input_status: not_supplied",
    "owner_authorization_granted: false",
    "contract_freeze_execution_allowed: false",
    "Review must keep freeze blocked when owner input is empty",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1=true",
    f"input_decision={INPUT_DECISION}",
    f"owner_input_status={OWNER_INPUT_STATUS}",
    "owner_authorization_granted=false",
    "owner_supplied_fields_count=0",
    "missing_required_fields_count=7",
    "contract_freeze_execution_allowed=false",
    "contract_freeze_executed=false",
    "runtime_contract_frozen=false",
    "codex_fabricated_owner_input=false",
    "codex_must_not_fill_owner_approval=true",
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
    print("AVF Agent Graph State Machine Kernel Contract Freeze Owner-Supplied Authorization Input v0.1 validation")
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


def require_previous_guide_gate() -> None:
    gate = read_json(PREVIOUS_GUIDE_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous completion guide gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous completion guide gate must point to this owner input goal")
    if gate.get("codex_must_not_fill_owner_approval") is not True:
        fail("previous completion guide must forbid Codex-filled owner approval")
    if gate.get("owner_must_supply_authorization") is not True:
        fail("previous completion guide must require owner-supplied authorization")
    if gate.get("owner_authorization_granted") is not False:
        fail("previous completion guide must not grant authorization")
    if gate.get("contract_freeze_execution_allowed") is not False:
        fail("previous completion guide must block freeze execution")
    if gate.get("missing_required_fields") != REQUIRED_OWNER_FIELDS:
        fail("previous completion guide missing fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "previous completion guide claim boundary")


def require_owner_input_gate() -> None:
    gate = read_json(OWNER_INPUT_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-owner-supplied-authorization-input-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "input_decision": INPUT_DECISION,
        "owner_input_status": OWNER_INPUT_STATUS,
        "owner_authorization_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_fields_count": len(REQUIRED_OWNER_FIELDS),
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "codex_fabricated_owner_input": False,
        "codex_must_not_fill_owner_approval": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"owner input gate {key} mismatch")
    if gate.get("missing_required_fields") != REQUIRED_OWNER_FIELDS:
        fail("owner input gate missing required fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "owner input gate claim boundary")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1",
        "status": "PASS",
        "input_decision": INPUT_DECISION,
        "owner_input_status": OWNER_INPUT_STATUS,
        "owner_authorization_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_fields_count": len(REQUIRED_OWNER_FIELDS),
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "codex_fabricated_owner_input": False,
        "codex_must_not_fill_owner_approval": True,
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

    require_previous_guide_gate()
    require_text_markers(OWNER_INPUT_PACKET, PACKET_MARKERS)
    require_owner_input_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Agent Graph State Machine Kernel Contract Freeze Owner-Supplied Authorization Input v0.1 validation")
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
