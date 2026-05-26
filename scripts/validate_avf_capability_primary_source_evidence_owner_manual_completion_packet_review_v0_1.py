from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1.py"
PACKET_TEMPLATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template.yml"
PACKET_TEMPLATE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_review_gate.json"
TERMINAL_BOUNDARY = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_review_protected_action_required_boundary.json"
NEXT_OWNER_ACTION = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_review_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_MANUAL_COMPLETION_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1"
TEMPLATE_DECISION = "MANUAL_COMPLETION_PACKET_TEMPLATE_READY_OWNER_INPUT_REQUIRED"
REVIEW_DECISION = "PROTECTED_ACTION_REQUIRED_OWNER_PACKET_STILL_UNFILLED"
TERMINAL_CONDITION = "PROTECTED_ACTION_REQUIRED"

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

AUTHORIZATION_FIELDS = [
    "owner_authorization_statement",
    "authorized_by",
    "authorized_at",
    "authorization_expires_at",
    "authorized_collection_modes",
    "authorized_source_families",
    "authorized_candidate_ids",
    "authorized_source_slot_ids",
    "max_records_to_collect",
    "collection_boundaries",
    "revocation_note",
]

REQUIRED_FILES = [
    RUNNER,
    PACKET_TEMPLATE,
    PACKET_TEMPLATE_GATE,
    REVIEW_GATE,
    TERMINAL_BOUNDARY,
    NEXT_OWNER_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

NEXT_OWNER_ACTION_MARKERS = [
    "action_id: owner-fill-avf-primary-source-evidence-manual-completion-packet",
    "terminal_condition: PROTECTED_ACTION_REQUIRED",
    "owner_input_required: true",
    "Fill all 11 authorization fields",
    "Select at least one collection mode",
    "Do not ask Codex to collect sources until review passes",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "terminal_condition=PROTECTED_ACTION_REQUIRED",
    "capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1=true",
    "owner_manual_completion_packet_review_gate_created=true",
    "protected_action_required_boundary_created=true",
    "owner_input_required=true",
    "manual_completion_packet_completed=false",
    "authorization_fields_reviewed=11",
    "authorization_fields_completed=0",
    "missing_authorization_fields=11",
    "collection_modes_selected=0",
    "source_records_reviewed=35",
    "source_records_executable=0",
    "collection_execution_allowed=false",
    "owner_authorization_granted=false",
    f"review_decision={REVIEW_DECISION}",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
]


def fail(message: str) -> None:
    print("AVF Capability Primary-Source Evidence Owner Manual Completion Packet Review v0.1 validation")
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


def require_packet_template_gate() -> None:
    gate = read_json(PACKET_TEMPLATE_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("packet template gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("packet template gate must point to this packet review goal")
    if gate.get("template_decision") != TEMPLATE_DECISION:
        fail("packet template decision mismatch")
    if gate.get("owner_input_required") is not True:
        fail("packet template gate must require owner input")
    if gate.get("manual_completion_packet_completed") is not False:
        fail("packet template must remain uncompleted")
    if gate.get("authorization_fields_completed") != 0:
        fail("packet template must not complete authorization fields")
    if gate.get("missing_authorization_fields") != AUTHORIZATION_FIELDS:
        fail("packet template missing fields mismatch")
    if gate.get("selected_collection_modes") != []:
        fail("packet template selected collection modes must be empty")
    if gate.get("collection_execution_allowed") is not False:
        fail("packet template must keep collection blocked")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        fail("packet template source record review count mismatch")
    if counts.get("source_records_executable") != 0:
        fail("packet template must not make source records executable")
    require_false_flags(gate.get("claim_boundary", {}), "packet template gate")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    expected = {
        "gate_id": "avf-capability-primary-source-evidence-owner-manual-completion-packet-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "terminal_condition": TERMINAL_CONDITION,
        "review_decision": REVIEW_DECISION,
        "owner_input_required": True,
        "manual_completion_packet_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_reviewed": len(AUTHORIZATION_FIELDS),
        "authorization_fields_completed": 0,
        "missing_authorization_fields_count": len(AUTHORIZATION_FIELDS),
        "collection_modes_selected": 0,
        "collection_execution_allowed": False,
        "integration_decision": "blocked",
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"review gate {key} mismatch")

    if gate.get("missing_authorization_fields") != AUTHORIZATION_FIELDS:
        fail("review gate missing authorization fields mismatch")
    if gate.get("selected_collection_modes") != []:
        fail("review gate selected collection modes must be empty")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        fail("review gate source record review count mismatch")
    if counts.get("source_records_executable") != 0:
        fail("review gate must not make source records executable")
    require_false_flags(gate.get("claim_boundary", {}), "review gate")


def require_terminal_boundary() -> None:
    boundary = read_json(TERMINAL_BOUNDARY)
    if boundary.get("terminal_condition") != TERMINAL_CONDITION:
        fail("terminal boundary condition mismatch")
    if boundary.get("review_decision") != REVIEW_DECISION:
        fail("terminal boundary decision mismatch")
    if boundary.get("owner_input_required") is not True:
        fail("terminal boundary must require owner input")
    if boundary.get("collection_execution_allowed") is not False:
        fail("terminal boundary must keep collection blocked")
    require_false_flags(boundary.get("claim_boundary", {}), "terminal boundary")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("validator_id") != "validate_avf_capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1":
        fail("validation result validator_id mismatch")
    if validation.get("status") != "PASS":
        fail("validation result must be PASS")
    if validation.get("terminal_condition") != TERMINAL_CONDITION:
        fail("validation result terminal condition mismatch")
    if validation.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
    if validation.get("owner_input_required") is not True:
        fail("validation result must require owner input")
    if validation.get("authorization_fields_completed") != 0:
        fail("validation result must not complete fields")
    if validation.get("collection_execution_allowed") is not False:
        fail("validation result must keep collection blocked")
    require_false_flags(validation.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_packet_template_gate()
    require_review_gate()
    require_terminal_boundary()
    require_text_markers(NEXT_OWNER_ACTION, NEXT_OWNER_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Primary-Source Evidence Owner Manual Completion Packet Review v0.1 validation")
    print("RESULT: PASS")
    print("terminal_condition=PROTECTED_ACTION_REQUIRED")
    print("capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1=true")
    print("owner_manual_completion_packet_review_gate_created=true")
    print("protected_action_required_boundary_created=true")
    print("owner_input_required=true")
    print("manual_completion_packet_completed=false")
    print("authorization_fields_reviewed=11")
    print("authorization_fields_completed=0")
    print("missing_authorization_fields=11")
    print("collection_modes_selected=0")
    print("source_records_reviewed=35")
    print("source_records_executable=0")
    print("collection_execution_allowed=false")
    print("owner_authorization_granted=false")
    print(f"review_decision={REVIEW_DECISION}")
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


if __name__ == "__main__":
    main()
