from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_observability_runtime_seed_owner_supplied_approval_input_v0_2.py"
PREVIOUS_RETRY_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_gate.json"
OWNER_INPUT_PACKET = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_v0_2.yml"
OWNER_INPUT_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_v0_2_gate.json"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_v0_2_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_v0_2.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_SUPPLIED_APPROVAL_INPUT_V0_2_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_v0_2"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_review_v0_2"
INPUT_DECISION = "OWNER_SUPPLIED_APPROVAL_INPUT_V0_2_CREATED_EMPTY_NOT_AUTHORIZED"
OWNER_INPUT_STATUS = "not_supplied"

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
    PREVIOUS_RETRY_GATE,
    OWNER_INPUT_PACKET,
    OWNER_INPUT_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    "packet_id: avf-observability-runtime-seed-owner-supplied-approval-input-v0-2",
    "schema_version: 0.2",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"input_decision: {INPUT_DECISION}",
    f"owner_input_status: {OWNER_INPUT_STATUS}",
    "owner_approval_record_present: false",
    "owner_approval_granted: false",
    "owner_supplied_fields_count: 0",
    "missing_required_owner_fields_count: 7",
    "collector_start_allowed: false",
    "telemetry_export_allowed: false",
    "runtime_integration_allowed: false",
    "dependency_adoption_allowed: false",
    "codex_fabricated_owner_approval: false",
    "codex_must_not_fill_owner_approval: true",
    "owner_must_supply_approval: true",
    "owner_name: null",
    "reviewed_packet_id: null",
    "approval_decision: null",
    "approved_actions: []",
    "approval_valid_after_review: false",
    "approval_notes: null",
    "reviewed_at: null",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-observability-runtime-seed-owner-supplied-approval-input-v0-2",
    "owner_input_status: not_supplied",
    "owner_approval_record_present: false",
    "collector_start_allowed: false",
    "telemetry_export_allowed: false",
    "runtime_integration_allowed: false",
    "dependency_adoption_allowed: false",
    "Confirm Codex did not fabricate owner approval",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "observability_runtime_seed_owner_supplied_approval_input_v0_2=true",
    f"input_decision={INPUT_DECISION}",
    "owner_input_status=not_supplied",
    "owner_approval_record_present=false",
    "owner_approval_granted=false",
    "owner_supplied_fields_count=0",
    "missing_required_owner_fields_count=7",
    "collector_start_allowed=false",
    "telemetry_export_allowed=false",
    "runtime_integration_allowed=false",
    "dependency_adoption_allowed=false",
    "codex_fabricated_owner_approval=false",
    "codex_must_not_fill_owner_approval=true",
    "owner_must_supply_approval=true",
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
    print("AVF Observability Runtime Seed Owner-Supplied Approval Input v0.2 validation")
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


def require_previous_retry_gate() -> None:
    gate = read_json(PREVIOUS_RETRY_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous retry gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous retry gate must point to this v0.2 owner input goal")
    if gate.get("retry_status") != "awaiting_owner_supplied_approval":
        fail("previous retry gate must be awaiting owner approval")
    if gate.get("owner_approval_granted") is not False:
        fail("previous retry gate must not grant approval")
    if gate.get("owner_supplied_fields_count") != 0:
        fail("previous retry gate owner supplied fields must be zero")
    if gate.get("missing_required_owner_fields") != REQUIRED_OWNER_FIELDS:
        fail("previous retry gate missing fields mismatch")
    if gate.get("codex_must_not_fill_owner_approval") is not True:
        fail("previous retry gate must forbid Codex-filled approval")
    if gate.get("owner_must_supply_approval") is not True:
        fail("previous retry gate must require owner-supplied approval")
    for key in ["collector_start_allowed", "telemetry_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            fail(f"previous retry gate {key} must be false")
    require_false_flags(gate.get("claim_boundary", {}), "previous retry gate claim boundary")


def require_owner_input_gate() -> None:
    gate = read_json(OWNER_INPUT_GATE)
    expected = {
        "gate_id": "avf-observability-runtime-seed-owner-supplied-approval-input-v0-2-gate",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "input_decision": INPUT_DECISION,
        "owner_input_status": OWNER_INPUT_STATUS,
        "owner_approval_record_present": False,
        "owner_approval_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_fabricated_owner_approval": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"owner input gate {key} mismatch")
    if gate.get("missing_required_owner_fields") != REQUIRED_OWNER_FIELDS:
        fail("owner input gate missing fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "owner input gate claim boundary")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_observability_runtime_seed_owner_supplied_approval_input_v0_2",
        "status": "PASS",
        "input_decision": INPUT_DECISION,
        "owner_input_status": OWNER_INPUT_STATUS,
        "owner_approval_record_present": False,
        "owner_approval_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_fabricated_owner_approval": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
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

    require_previous_retry_gate()
    require_text_markers(OWNER_INPUT_PACKET, PACKET_MARKERS)
    require_owner_input_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Observability Runtime Seed Owner-Supplied Approval Input v0.2 validation")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_supplied_approval_input_v0_2=true")
    print(f"input_decision={INPUT_DECISION}")
    print("owner_input_status=not_supplied")
    print("owner_approval_record_present=false")
    print("owner_approval_granted=false")
    print("owner_supplied_fields_count=0")
    print(f"missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    print("collector_start_allowed=false")
    print("telemetry_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print("codex_fabricated_owner_approval=false")
    print("codex_must_not_fill_owner_approval=true")
    print("owner_must_supply_approval=true")
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
    print("runtime_export_performed=false")
    print("collector_started=false")
    print("telemetry_export_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
