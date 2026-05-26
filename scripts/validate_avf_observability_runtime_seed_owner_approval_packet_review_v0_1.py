from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_observability_runtime_seed_owner_approval_packet_review_v0_1.py"
OWNER_APPROVAL_PACKET = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet.json"
OWNER_APPROVAL_GATE = OBS_GENERATED / "observability_runtime_seed_owner_approval_gate.json"
OWNER_APPROVAL_NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_next_action.yml"
REVIEW = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_review.json"
REVIEW_GATE = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_review_gate.json"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_review_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_APPROVAL_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_approval_completion_guide_v0_1"
REVIEW_DECISION = "OWNER_APPROVAL_PACKET_REVIEWED_APPROVAL_NOT_PROVIDED_INTEGRATION_BLOCKED"
REVIEW_STATUS = "blocked_missing_owner_approval_record"
APPROVAL_SCOPE = "future_runtime_observability_integration_only"

REQUIRED_APPROVAL_ACTIONS = [
    "collector_start",
    "telemetry_export",
    "runtime_backend_integration",
    "dependency_adoption",
]

REQUIRED_OWNER_FIELDS = [
    "owner_name",
    "reviewed_packet_id",
    "approval_decision",
    "approved_actions",
    "approval_valid_after_review",
    "approval_notes",
    "reviewed_at",
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
    OWNER_APPROVAL_PACKET,
    OWNER_APPROVAL_GATE,
    OWNER_APPROVAL_NEXT_ACTION,
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
    '"owner_approval_required": true',
    '"owner_approval_record_present": false',
    '"collector_start_allowed": false',
    '"telemetry_export_allowed": false',
    '"runtime_integration_allowed": false',
    '"dependency_adoption_allowed": false',
    '"missing_required_owner_fields_count": 7',
    f'"next_safe_goal_id": "{NEXT_SAFE_GOAL_ID}"',
]

NEXT_ACTION_MARKERS = [
    "action_id: create-observability-runtime-seed-owner-approval-completion-guide",
    "owner_approval_record_present: false",
    "review_status: blocked_missing_owner_approval_record",
    "Do not start collectors, export telemetry, integrate runtime backends, install dependencies, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "observability_runtime_seed_owner_approval_packet_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "owner_approval_required=true",
    "owner_approval_record_present=false",
    "collector_start_allowed=false",
    "telemetry_export_allowed=false",
    "runtime_integration_allowed=false",
    "dependency_adoption_allowed=false",
    "missing_required_owner_fields_count=7",
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


def fail(message: str) -> None:
    print("AVF Observability Runtime Seed Owner Approval Packet Review v0.1 validation")
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


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{rel(path)} missing markers:\n" + "\n".join(missing))


def require_previous_packet_inputs() -> None:
    packet = read_json(OWNER_APPROVAL_PACKET)
    gate = read_json(OWNER_APPROVAL_GATE)
    if packet.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("owner approval packet goal mismatch")
    if packet.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("owner approval packet must point to this review goal")
    if packet.get("approval_status") != "not_approved_owner_input_required":
        fail("owner approval packet status mismatch")
    if packet.get("approval_scope") != APPROVAL_SCOPE:
        fail("owner approval packet scope mismatch")
    if packet.get("integration_actions_requiring_owner_approval") != REQUIRED_APPROVAL_ACTIONS:
        fail("owner approval packet action list mismatch")
    template = packet.get("approval_record_template", {})
    if sorted(template) != sorted(REQUIRED_OWNER_FIELDS):
        fail("owner approval record template fields mismatch")
    if template.get("approval_decision") != "pending":
        fail("owner approval record template decision must remain pending")
    if template.get("approved_actions") != []:
        fail("owner approval record template must not preapprove actions")
    if template.get("approval_valid_after_review") is not False:
        fail("owner approval record template must not be valid before review")
    require_false_flags(packet.get("claim_boundary", {}), "owner approval packet")

    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("owner approval gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("owner approval gate must point to this review goal")
    if gate.get("owner_approval_record_present") is not False:
        fail("owner approval gate must not contain approval record")
    for key in ["collector_start_allowed", "telemetry_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            fail(f"owner approval gate {key} must remain false")
    require_false_flags(gate.get("claim_boundary", {}), "owner approval gate")

    require_text_markers(
        OWNER_APPROVAL_NEXT_ACTION,
        [
            "action_id: review-observability-runtime-seed-owner-approval-packet",
            "owner_approval_record_present: false",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )


def require_review_record(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "owner_approval_required": True,
        "owner_approval_record_present": False,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("actions_requiring_owner_approval") != REQUIRED_APPROVAL_ACTIONS:
        fail(f"{label} approval action list mismatch")
    if record.get("missing_required_owner_fields") != REQUIRED_OWNER_FIELDS:
        fail(f"{label} missing owner fields mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-observability-runtime-seed-owner-approval-packet-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate must be PASS")
    require_review_record(gate, "review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_observability_runtime_seed_owner_approval_packet_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    require_review_record(result, "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_packet_inputs()
    require_text_markers(REVIEW, REVIEW_MARKERS)
    require_review_record(read_json(REVIEW), "review record")
    require_review_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Observability Runtime Seed Owner Approval Packet Review v0.1 validation")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_approval_packet_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    print("owner_approval_required=true")
    print("owner_approval_record_present=false")
    print("collector_start_allowed=false")
    print("telemetry_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print(f"missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    for flag in FALSE_FLAGS:
        print(f"{flag}=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
