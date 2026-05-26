from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_observability_runtime_seed_owner_approval_completion_guide_v0_1.py"
PREVIOUS_REVIEW_GATE = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_review_gate.json"
COMPLETION_GUIDE = OBS_GENERATED / "observability_runtime_seed_owner_approval_record_completion_guide.md"
COMPLETION_GUIDE_GATE = OBS_GENERATED / "observability_runtime_seed_owner_approval_record_completion_guide_gate.json"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_approval_record_completion_guide_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_approval_record_completion_guide_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_APPROVAL_COMPLETION_GUIDE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_approval_completion_guide_v0_1"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_v0_1"
GUIDE_DECISION = "OWNER_APPROVAL_COMPLETION_GUIDE_CREATED_NO_RUNTIME_AUTHORIZATION_GRANTED"
PREVIOUS_REVIEW_STATUS = "blocked_missing_owner_approval_record"

REQUIRED_OWNER_FIELDS = [
    "owner_name",
    "reviewed_packet_id",
    "approval_decision",
    "approved_actions",
    "approval_valid_after_review",
    "approval_notes",
    "reviewed_at",
]

REQUIRED_APPROVAL_ACTIONS = [
    "collector_start",
    "telemetry_export",
    "runtime_backend_integration",
    "dependency_adoption",
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
    PREVIOUS_REVIEW_GATE,
    COMPLETION_GUIDE,
    COMPLETION_GUIDE_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

GUIDE_MARKERS = [
    "# AVF Observability Runtime Seed Owner Approval Record Completion Guide v0.1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"guide_decision: {GUIDE_DECISION}",
    "owner_approval_record_present: false",
    "collector_start_allowed: false",
    "telemetry_export_allowed: false",
    "runtime_integration_allowed: false",
    "dependency_adoption_allowed: false",
    "codex_must_not_fill_owner_approval: true",
    "owner_must_supply_approval: true",
    "missing_required_owner_fields_count: 7",
    "owner_name",
    "reviewed_packet_id",
    "approval_decision",
    "approved_actions",
    "approval_valid_after_review",
    "approval_notes",
    "reviewed_at",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: collect-observability-runtime-seed-owner-supplied-approval-input",
    "owner_approval_record_present: false",
    "Codex must not fabricate owner approval",
    "Keep all runtime actions blocked until owner input exists and is separately reviewed",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "observability_runtime_seed_owner_approval_completion_guide_v0_1=true",
    f"guide_decision={GUIDE_DECISION}",
    "owner_approval_record_present=false",
    "collector_start_allowed=false",
    "telemetry_export_allowed=false",
    "runtime_integration_allowed=false",
    "dependency_adoption_allowed=false",
    "codex_must_not_fill_owner_approval=true",
    "owner_must_supply_approval=true",
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
    print("AVF Observability Runtime Seed Owner Approval Completion Guide v0.1 validation")
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


def require_previous_review_gate() -> None:
    gate = read_json(PREVIOUS_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous review gate must point to this completion guide goal")
    if gate.get("review_status") != PREVIOUS_REVIEW_STATUS:
        fail("previous review gate status mismatch")
    if gate.get("owner_approval_record_present") is not False:
        fail("previous review gate must not contain owner approval record")
    for key in ["collector_start_allowed", "telemetry_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            fail(f"previous review gate {key} must remain false")
    if gate.get("missing_required_owner_fields") != REQUIRED_OWNER_FIELDS:
        fail("previous review gate missing owner fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "previous review gate")


def require_guide_gate() -> None:
    gate = read_json(COMPLETION_GUIDE_GATE)
    expected = {
        "gate_id": "avf-observability-runtime-seed-owner-approval-completion-guide-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "owner_approval_record_present": False,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"completion guide gate {key} mismatch")
    if gate.get("required_owner_fields") != REQUIRED_OWNER_FIELDS:
        fail("completion guide gate required owner fields mismatch")
    if gate.get("actions_requiring_owner_approval") != REQUIRED_APPROVAL_ACTIONS:
        fail("completion guide gate approval action list mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "completion guide gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_observability_runtime_seed_owner_approval_completion_guide_v0_1",
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "owner_approval_record_present": False,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
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

    require_previous_review_gate()
    require_text_markers(COMPLETION_GUIDE, GUIDE_MARKERS)
    require_guide_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Observability Runtime Seed Owner Approval Completion Guide v0.1 validation")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_approval_completion_guide_v0_1=true")
    print(f"guide_decision={GUIDE_DECISION}")
    print("owner_approval_record_present=false")
    print("collector_start_allowed=false")
    print("telemetry_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print("codex_must_not_fill_owner_approval=true")
    print("owner_must_supply_approval=true")
    print(f"missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    for flag in FALSE_FLAGS:
        print(f"{flag}=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
