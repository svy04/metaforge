from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2.py"
PREVIOUS_REVIEW_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_review_v0_2_gate.json"
RETRY_PACKET = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2.yml"
RETRY_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2_gate.json"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_SUPPLIED_APPROVAL_COMPLETION_RETRY_V0_2_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_review_v0_2"
NEXT_SAFE_GOAL_ID = "avf_primary_source_evidence_registry_gap_review_v0_1"
RETRY_DECISION = "OWNER_APPROVAL_COMPLETION_RETRY_V0_2_CREATED_RUNTIME_WAIT_STATE_NON_PROTECTED_NEXT"
RETRY_STATUS = "awaiting_owner_supplied_approval_runtime_blocked"

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
    PREVIOUS_REVIEW_GATE,
    RETRY_PACKET,
    RETRY_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    "packet_id: avf-observability-runtime-seed-owner-supplied-approval-completion-retry-v0-2",
    "schema_version: 0.2",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"retry_decision: {RETRY_DECISION}",
    f"retry_status: {RETRY_STATUS}",
    "owner_approval_granted: false",
    "owner_supplied_fields_count: 0",
    "missing_required_owner_fields_count: 7",
    "runtime_approval_wait_state: true",
    "switch_to_non_protected_work: true",
    "collector_start_allowed: false",
    "telemetry_export_allowed: false",
    "runtime_integration_allowed: false",
    "dependency_adoption_allowed: false",
    "codex_must_not_fill_owner_approval: true",
    "owner_must_supply_approval: true",
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
    "action_id: review-primary-source-evidence-registry-gap",
    "runtime_approval_wait_state: true",
    "switch_to_non_protected_work: true",
    "owner_approval_required_before_runtime_execution: true",
    "owner_approval_granted: false",
    "collector_start_allowed: false",
    "telemetry_export_allowed: false",
    "runtime_integration_allowed: false",
    "dependency_adoption_allowed: false",
    "Continue with repo-local primary-source evidence registry gap review",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2=true",
    f"retry_decision={RETRY_DECISION}",
    f"retry_status={RETRY_STATUS}",
    "owner_approval_granted=false",
    "owner_supplied_fields_count=0",
    "missing_required_owner_fields_count=7",
    "runtime_approval_wait_state=true",
    "switch_to_non_protected_work=true",
    "collector_start_allowed=false",
    "telemetry_export_allowed=false",
    "runtime_integration_allowed=false",
    "dependency_adoption_allowed=false",
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
    print("AVF Observability Runtime Seed Owner-Supplied Approval Completion Retry v0.2 validation")
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


def require_previous_review_gate() -> None:
    gate = read_json(PREVIOUS_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous review gate must point to this completion retry goal")
    if gate.get("review_status") != "blocked_owner_approval_input_not_supplied":
        fail("previous review gate must remain blocked_owner_approval_input_not_supplied")
    if gate.get("owner_approval_record_present") is not False:
        fail("previous review gate must not contain approval")
    if gate.get("owner_approval_granted") is not False:
        fail("previous review gate must not grant approval")
    if gate.get("owner_supplied_fields_count") != 0:
        fail("previous review gate owner supplied fields must be zero")
    if gate.get("missing_required_owner_fields") != REQUIRED_OWNER_FIELDS:
        fail("previous review gate missing fields mismatch")
    if gate.get("codex_fabricated_owner_approval") is not False:
        fail("previous review gate must record no fabricated owner approval")
    for key in ["collector_start_allowed", "telemetry_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            fail(f"previous review gate {key} must be false")
    require_false_flags(gate.get("claim_boundary", {}), "previous review gate claim boundary")


def require_retry_gate() -> None:
    gate = read_json(RETRY_GATE)
    expected = {
        "gate_id": "avf-observability-runtime-seed-owner-supplied-approval-completion-retry-v0-2-gate",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "retry_decision": RETRY_DECISION,
        "retry_status": RETRY_STATUS,
        "owner_approval_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "runtime_approval_wait_state": True,
        "switch_to_non_protected_work": True,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"retry gate {key} mismatch")
    if gate.get("missing_required_owner_fields") != REQUIRED_OWNER_FIELDS:
        fail("retry gate missing fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "retry gate claim boundary")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2",
        "status": "PASS",
        "retry_decision": RETRY_DECISION,
        "retry_status": RETRY_STATUS,
        "owner_approval_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "runtime_approval_wait_state": True,
        "switch_to_non_protected_work": True,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
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

    require_previous_review_gate()
    require_text_markers(RETRY_PACKET, PACKET_MARKERS)
    require_retry_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Observability Runtime Seed Owner-Supplied Approval Completion Retry v0.2 validation")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2=true")
    print(f"retry_decision={RETRY_DECISION}")
    print(f"retry_status={RETRY_STATUS}")
    print("owner_approval_granted=false")
    print("owner_supplied_fields_count=0")
    print(f"missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    print("runtime_approval_wait_state=true")
    print("switch_to_non_protected_work=true")
    print("collector_start_allowed=false")
    print("telemetry_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
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
