from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_v0_1.py"
OWNER_INPUT_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_gate.json"
REVIEW = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review.json"
REVIEW_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_gate.json"
NEXT_ACTION = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_next_action.yml"
VALIDATION_RESULT = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_OWNER_SUPPLIED_AUTHORIZATION_INPUT_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_completion_retry_v0_1"
REVIEW_DECISION = "OWNER_SUPPLIED_AUTHORIZATION_INPUT_REVIEWED_EMPTY_FREEZE_BLOCKED"
REVIEW_STATUS = "blocked_owner_input_not_supplied"

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
    OWNER_INPUT_GATE,
    REVIEW,
    REVIEW_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REVIEW_MARKERS = [
    f'"goal_id": "{THIS_GOAL_ID}"',
    f'"previous_goal_id": "{PREVIOUS_GOAL_ID}"',
    f'"review_decision": "{REVIEW_DECISION}"',
    f'"review_status": "{REVIEW_STATUS}"',
    '"owner_input_status": "not_supplied"',
    '"owner_authorization_granted": false',
    '"owner_supplied_fields_count": 0',
    '"missing_required_fields_count": 7',
    '"contract_freeze_execution_allowed": false',
    '"contract_freeze_executed": false',
    '"runtime_contract_frozen": false',
    '"codex_fabricated_owner_input": false',
    f'"next_safe_goal_id": "{NEXT_SAFE_GOAL_ID}"',
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-state-machine-kernel-contract-freeze-owner-supplied-authorization-completion-retry",
    "owner_approval_required_before_execution: true",
    "review_status: blocked_owner_input_not_supplied",
    "owner_authorization_granted: false",
    "contract_freeze_execution_allowed: false",
    "Do not execute contract freeze from this blocked input review",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "owner_input_status=not_supplied",
    "owner_authorization_granted=false",
    "owner_supplied_fields_count=0",
    "missing_required_fields_count=7",
    "contract_freeze_execution_allowed=false",
    "contract_freeze_executed=false",
    "runtime_contract_frozen=false",
    "codex_fabricated_owner_input=false",
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
    print("AVF Agent Graph State Machine Kernel Contract Freeze Owner-Supplied Authorization Input Review v0.1 validation")
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


def require_owner_input_gate() -> None:
    gate = read_json(OWNER_INPUT_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("owner input gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("owner input gate must point to this input review goal")
    if gate.get("owner_input_status") != "not_supplied":
        fail("owner input status must be not_supplied")
    if gate.get("owner_authorization_granted") is not False:
        fail("owner input gate must not grant authorization")
    if gate.get("owner_supplied_fields_count") != 0:
        fail("owner supplied fields count must be zero")
    if gate.get("missing_required_fields") != REQUIRED_OWNER_FIELDS:
        fail("owner input gate missing fields mismatch")
    if gate.get("codex_fabricated_owner_input") is not False:
        fail("Codex fabricated owner input must be false")
    if gate.get("contract_freeze_execution_allowed") is not False:
        fail("owner input gate must keep freeze blocked")
    require_false_flags(gate.get("claim_boundary", {}), "owner input gate claim boundary")


def require_review_record(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "owner_input_status": "not_supplied",
        "owner_authorization_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_fields_count": len(REQUIRED_OWNER_FIELDS),
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "codex_fabricated_owner_input": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("missing_required_fields") != REQUIRED_OWNER_FIELDS:
        fail(f"{label} missing required fields mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-agent-graph-state-machine-kernel-contract-freeze-owner-supplied-authorization-input-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate must be PASS")
    require_review_record(gate, "review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    require_review_record(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_owner_input_gate()
    require_text_markers(REVIEW, REVIEW_MARKERS)
    require_review_record(read_json(REVIEW), "review record")
    require_review_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Agent Graph State Machine Kernel Contract Freeze Owner-Supplied Authorization Input Review v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    print("owner_input_status=not_supplied")
    print("owner_authorization_granted=false")
    print("owner_supplied_fields_count=0")
    print(f"missing_required_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    print("contract_freeze_execution_allowed=false")
    print("contract_freeze_executed=false")
    print("runtime_contract_frozen=false")
    print("codex_fabricated_owner_input=false")
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
