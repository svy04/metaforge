from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1.py"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_review_gate.json"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_review_next_action.yml"
OWNER_INPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet.yml"
OWNER_INPUT_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_gate.json"
OWNER_INPUT_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_RUNTIME_INTEGRATION_OWNER_INPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
OWNER_INPUT_DECISION = "OWNER_INPUT_PACKET_TEMPLATE_READY_UNFILLED_RUNTIME_ACTIONS_BLOCKED"
OWNER_INPUT_STATUS = "owner_input_required_not_supplied_authorization_not_granted"

EXPECTED_COUNTS = {
    "runtime_preflight_check_count": 8,
    "authorization_item_count": 6,
    "owner_input_item_template_count": 6,
    "owner_input_item_completed_count": 0,
    "authorization_item_not_granted_count": 6,
    "protected_action_required_count": 6,
    "owner_input_required_count": 1,
    "sandbox_plan_required_count": 1,
    "license_review_required_count": 1,
    "security_review_required_count": 1,
    "runtime_integration_allowed_count": 0,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "action_allowed_count": 0,
    "owner_input_packet_blocker_count": 0,
    "ready_for_runtime_integration_owner_input_packet_review_count": 1,
}

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
    "runtime_export_performed",
    "collector_started",
    "telemetry_export_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

AUTHORIZATION_ITEM_IDS = [
    "authorize-candidate-tool-import",
    "authorize-dependency-install",
    "authorize-external-source-fetch",
    "authorize-runtime-integration",
    "authorize-runtime-export",
    "authorize-external-service-call",
]

REQUIRED_FILES = [
    RUNNER,
    REVIEW_GATE,
    REVIEW_NEXT_ACTION,
    OWNER_INPUT_PACKET,
    OWNER_INPUT_GATE,
    OWNER_INPUT_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

OWNER_INPUT_PACKET_MARKERS = [
    "packet_id: avf-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-input-packet-v0-1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"owner_input_decision: {OWNER_INPUT_DECISION}",
    f"owner_input_status: {OWNER_INPUT_STATUS}",
    "owner_input_packet_completed: false",
    "owner_authorization_granted: false",
    "runtime_integration_allowed: false",
    "candidate_tool_import_allowed: false",
    "dependency_install_allowed: false",
    "external_fetch_allowed: false",
    "runtime_export_allowed: false",
    "external_service_call_allowed: false",
    "authorization_statement:",
    "authorized_by:",
    "authorized_at:",
    "authorization_expires_at:",
    "sandbox_plan_uri:",
    "license_review_uri:",
    "security_review_uri:",
    "revocation_note:",
    "decision: unfilled",
    "authorization_status: not_granted",
    "action_allowed: false",
    "protected_action_required: true",
    "No candidate tool import",
    "No dependency install",
    "No external fetch",
    "No runtime integration",
    "No runtime export",
    "No external service call",
    "No deploy",
    "No publish",
    "No release readiness claim",
    "No production readiness claim",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1=true",
    "owner_input_packet_template_created=true",
    "owner_input_packet_gate_created=true",
    f"candidate_id={CANDIDATE_ID}",
    f"owner_input_decision={OWNER_INPUT_DECISION}",
    f"owner_input_status={OWNER_INPUT_STATUS}",
    "owner_input_packet_completed=false",
    "owner_authorization_granted=false",
    "runtime_preflight_check_count=8",
    "authorization_item_count=6",
    "owner_input_item_template_count=6",
    "owner_input_item_completed_count=0",
    "authorization_item_not_granted_count=6",
    "protected_action_required_count=6",
    "owner_input_required_count=1",
    "sandbox_plan_required_count=1",
    "license_review_required_count=1",
    "security_review_required_count=1",
    "runtime_integration_allowed_count=0",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "action_allowed_count=0",
    "owner_input_packet_blocker_count=0",
    "ready_for_runtime_integration_owner_input_packet_review_count=1",
    "provider_neutral=true",
    "dependency_free=true",
    "candidate_tool_import_allowed=false",
    "dependency_install_allowed=false",
    "external_fetch_allowed=false",
    "runtime_integration_allowed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-input-packet",
    "owner_approval_required_before_execution: false",
    "Review the unfilled owner input packet template before any runtime authorization can be accepted",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Owner Input Packet v0.1 validation")
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


def require_review_gate() -> dict:
    gate = read_json(REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("review gate must point to this owner input packet goal")
    if gate.get("ready_for_runtime_integration_owner_input_packet_count") != 1:
        fail("review gate must be ready for owner input packet")
    for key, value in {
        "candidate_id": CANDIDATE_ID,
        "owner_authorization_granted": False,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "review_blocker_count": 0,
    }.items():
        if gate.get(key) != value:
            fail(f"review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "review gate claim boundary")
    require_text_markers(
        REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-input-packet",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_owner_input_item(item: dict) -> None:
    item_id = item.get("authorization_item_id", "<missing>")
    if item_id not in AUTHORIZATION_ITEM_IDS:
        fail(f"unexpected owner input authorization item {item_id}")
    expected = {
        "decision": "unfilled",
        "authorization_status": "not_granted",
        "protected_action_required": True,
        "action_allowed": False,
        "owner_authorization_granted": False,
    }
    for key, value in expected.items():
        if item.get(key) != value:
            fail(f"owner input item {item_id} {key} mismatch")
    for key in [
        "authorization_statement",
        "authorized_by",
        "authorized_at",
        "authorization_expires_at",
        "sandbox_plan_uri",
        "license_review_uri",
        "security_review_uri",
        "revocation_note",
    ]:
        if item.get(key) != "":
            fail(f"owner input item {item_id} {key} must be empty")
    if item.get("scope_boundaries") != []:
        fail(f"owner input item {item_id} scope boundaries must be empty")


def require_owner_input_record(record: dict, label: str, source: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "owner_input_decision": OWNER_INPUT_DECISION,
        "owner_input_status": OWNER_INPUT_STATUS,
        "owner_input_packet_completed": False,
        "owner_authorization_granted": False,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "runtime_integration_performed": False,
        "runtime_export_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("adapter_runtime_integration_authorization_packet_review_gate") != REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} review gate input uri mismatch")
    items = record.get("owner_input_authorization_items", [])
    if len(items) != EXPECTED_COUNTS["owner_input_item_template_count"]:
        fail(f"{label} owner input item template count mismatch")
    for item in items:
        require_owner_input_item(item)
    if sorted(item["authorization_item_id"] for item in items) != sorted(AUTHORIZATION_ITEM_IDS):
        fail(f"{label} owner input item ids mismatch")
    if record.get("source_reviewed_authorization_items") != source.get("reviewed_authorization_items"):
        fail(f"{label} source reviewed authorization items mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(source: dict) -> None:
    gate = read_json(OWNER_INPUT_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-input-packet-gate-v0-1":
        fail("owner input gate id mismatch")
    if gate.get("status") != "PASS":
        fail("owner input gate status must be PASS")
    require_owner_input_record(gate, "owner input gate", source)


def require_validation_result(source: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_owner_input_record(result, "validation result", source)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    source = require_review_gate()
    require_text_markers(OWNER_INPUT_PACKET, OWNER_INPUT_PACKET_MARKERS)
    require_gate(source)
    require_text_markers(OWNER_INPUT_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(source)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Owner Input Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1=true")
    print("owner_input_packet_template_created=true")
    print("owner_input_packet_gate_created=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"owner_input_decision={OWNER_INPUT_DECISION}")
    print(f"owner_input_status={OWNER_INPUT_STATUS}")
    print("owner_input_packet_completed=false")
    print("owner_authorization_granted=false")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("provider_neutral=true")
    print("dependency_free=true")
    print("candidate_tool_import_allowed=false")
    print("dependency_install_allowed=false")
    print("external_fetch_allowed=false")
    print("runtime_integration_allowed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
