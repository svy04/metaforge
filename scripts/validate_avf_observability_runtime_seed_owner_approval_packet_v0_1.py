from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_observability_runtime_seed_owner_approval_packet_v0_1.py"
ACCEPTANCE_GATE = OBS_GENERATED / "observability_runtime_seed_acceptance_gate.json"
ACCEPTANCE_NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_acceptance_next_action.yml"
OWNER_APPROVAL_PACKET = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet.json"
OWNER_APPROVAL_GATE = OBS_GENERATED / "observability_runtime_seed_owner_approval_gate.json"
OWNER_APPROVAL_GUIDE = OBS_GENERATED / "observability_runtime_seed_owner_approval_completion_guide.md"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_APPROVAL_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_acceptance_gate_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_review_v0_1"
APPROVAL_STATUS = "not_approved_owner_input_required"
APPROVAL_SCOPE = "future_runtime_observability_integration_only"

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

REQUIRED_FILES = [
    RUNNER,
    ACCEPTANCE_GATE,
    ACCEPTANCE_NEXT_ACTION,
    OWNER_APPROVAL_PACKET,
    OWNER_APPROVAL_GATE,
    OWNER_APPROVAL_GUIDE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_PACKET_FIELDS = {
    "packet_id",
    "created_at",
    "goal_id",
    "previous_goal_id",
    "approval_status",
    "approval_scope",
    "required_owner_decision",
    "integration_actions_requiring_owner_approval",
    "blocked_until_owner_approval",
    "allowed_without_owner_approval",
    "approval_record_template",
    "next_safe_goal_id",
    "claim_boundary",
}

REQUIRED_APPROVAL_ACTIONS = [
    "collector_start",
    "telemetry_export",
    "runtime_backend_integration",
    "dependency_adoption",
]

ALLOWED_WITHOUT_APPROVAL = [
    "repo_local_documentation",
    "repo_local_validation",
    "repo_local_approval_packet_review",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "observability_runtime_seed_owner_approval_packet_v0_1=true",
    f"approval_status={APPROVAL_STATUS}",
    f"approval_scope={APPROVAL_SCOPE}",
    "owner_approval_record_present=false",
    "collector_start_allowed=false",
    "telemetry_export_allowed=false",
    "runtime_integration_allowed=false",
    "dependency_adoption_allowed=false",
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
    "runtime_export_performed=false",
    "collector_started=false",
    "telemetry_export_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-observability-runtime-seed-owner-approval-packet",
    "owner_approval_record_present: false",
    "Do not treat this packet as approval",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Observability Runtime Seed Owner Approval Packet v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{rel(path)} missing markers:\n" + "\n".join(missing))


def require_previous_acceptance_gate() -> None:
    gate = read_json(ACCEPTANCE_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("acceptance gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("acceptance gate must point to this owner approval packet goal")
    if gate.get("acceptance_decision") != "ACCEPT_REPO_LOCAL_OBSERVABILITY_SEED_ONLY":
        fail("acceptance gate decision mismatch")
    if gate.get("owner_approval_required_before_runtime_integration") is not True:
        fail("acceptance gate must require owner approval before runtime integration")
    for key in ["runtime_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            fail(f"acceptance gate {key} must remain false")
    require_false_flags(gate.get("claim_boundary", {}), "acceptance gate")
    require_markers(
        ACCEPTANCE_NEXT_ACTION,
        [
            "action_id: create-observability-runtime-seed-owner-approval-packet",
            "owner_approval_required_before_runtime_integration: true",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )


def require_owner_approval_packet() -> None:
    packet = read_json(OWNER_APPROVAL_PACKET)
    missing = sorted(REQUIRED_PACKET_FIELDS - set(packet))
    if missing:
        fail("owner approval packet missing fields:\n" + "\n".join(missing))
    expected = {
        "packet_id": "avf-observability-runtime-seed-owner-approval-packet-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "required_owner_decision": "explicit_owner_approval_required_before_runtime_integration",
        "blocked_until_owner_approval": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if packet.get(key) != value:
            fail(f"owner approval packet {key} mismatch")
    if packet.get("integration_actions_requiring_owner_approval") != REQUIRED_APPROVAL_ACTIONS:
        fail("owner approval action list mismatch")
    if packet.get("allowed_without_owner_approval") != ALLOWED_WITHOUT_APPROVAL:
        fail("allowed-without-approval list mismatch")
    template = packet.get("approval_record_template", {})
    if template.get("owner_name") != "<required>":
        fail("approval template must require owner_name")
    if template.get("approval_decision") != "pending":
        fail("approval template decision must remain pending")
    if template.get("approved_actions") != []:
        fail("approval template must not pre-approve any action")
    if template.get("approval_valid_after_review") is not False:
        fail("approval template must not be valid before review")
    require_false_flags(packet.get("claim_boundary", {}), "owner approval packet")


def require_owner_approval_gate() -> None:
    gate = read_json(OWNER_APPROVAL_GATE)
    expected = {
        "gate_id": "avf-observability-runtime-seed-owner-approval-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "owner_approval_packet_created": True,
        "owner_approval_record_present": False,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"owner approval gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "owner approval gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_observability_runtime_seed_owner_approval_packet_v0_1",
        "status": "PASS",
        "goal_id": THIS_GOAL_ID,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "owner_approval_record_present": False,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            fail(f"validation result {key} mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_acceptance_gate()
    require_owner_approval_packet()
    require_owner_approval_gate()
    require_validation_result()
    require_markers(OWNER_APPROVAL_GUIDE, REPORT_MARKERS)
    require_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Observability Runtime Seed Owner Approval Packet v0.1 validation")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_approval_packet_v0_1=true")
    print(f"approval_status={APPROVAL_STATUS}")
    print(f"approval_scope={APPROVAL_SCOPE}")
    print("owner_approval_record_present=false")
    print("collector_start_allowed=false")
    print("telemetry_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    for flag in FALSE_FLAGS:
        print(f"{flag}=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
