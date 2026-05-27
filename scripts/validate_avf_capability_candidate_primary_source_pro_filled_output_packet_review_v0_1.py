from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_pro_filled_output_packet_review_v0_1.py"
FILLED_OUTPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet.yml"
FILLED_OUTPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_gate.json"
FILLED_OUTPUT_PACKET_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_FILLED_OUTPUT_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_pro_actual_output_packet_v0_1"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_FILLED_OUTPUT_PACKET_SHELL_REVIEWED_REPO_LOCAL"
REVIEW_STATUS = "filled_output_packet_shell_review_passed_waiting_for_actual_gpt_pro_output"

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "source_target_count": 16,
    "required_source_field_count": 12,
    "empty_source_field_slot_count": 16,
    "review_blocker_count": 0,
    "ready_for_actual_gpt_pro_output_packet_count": 1,
    "filled_record_supplied_count": 0,
    "accepted_records": 0,
    "external_fetch_performed_count": 0,
    "source_contents_acquired_count": 0,
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

REQUIRED_FILES = [
    RUNNER,
    FILLED_OUTPUT_PACKET,
    FILLED_OUTPUT_PACKET_GATE,
    FILLED_OUTPUT_PACKET_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    "records_source: pasted_gpt_pro_yaml_not_supplied",
    "gpt_pro_output_supplied: false",
    "filled_record_supplied_count: 0",
    "accepted_records: 0",
    "acceptance_status: unreviewed",
    "filled_record_supplied: false",
    "source_id:",
    "source_title:",
    "source_kind:",
    "source_uri:",
    "source_version_or_date:",
    "source_owner_or_publisher:",
    "license_or_rights_note:",
    "claim_supported:",
    "evidence_excerpt_summary:",
    "verification_notes:",
    "source_reference_lines:",
    "retrieval_method:",
    "Do not treat empty source fields as accepted primary-source evidence.",
    "external_fetch_performed: false",
    "protected_action_executed: false",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_pro_filled_output_packet_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "records_source=pasted_gpt_pro_yaml_not_supplied",
    "gpt_pro_output_supplied=false",
    "candidate_count=7",
    "source_target_count=16",
    "required_source_field_count=12",
    "empty_source_field_slot_count=16",
    "review_blocker_count=0",
    "ready_for_actual_gpt_pro_output_packet_count=1",
    "filled_record_supplied_count=0",
    "accepted_records=0",
    "external_fetch_performed_count=0",
    "source_contents_acquired_count=0",
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
    "action_id: create-capability-candidate-primary-source-pro-actual-output-packet",
    "owner_approval_required_before_execution: false",
    "Create a repo-local packet from actual pasted GPT Pro primary-source YAML",
    "Keep pasted GPT Pro records unaccepted until a separate evidence-review gate passes",
    "Do not fetch external sources inside Codex, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Pro Filled Output Packet Review v0.1 validation")
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


def require_empty_slots(record: dict, label: str) -> None:
    empty_slot_count = 0
    for section in record.get("candidate_output_sections", []):
        for slot in section.get("source_output_slots", []):
            if slot.get("acceptance_status") != "unreviewed":
                fail(f"{label} slot acceptance status mismatch")
            if slot.get("filled_record_supplied") is not False:
                fail(f"{label} slot must not be filled")
            if slot.get("source_contents_acquired") is not False:
                fail(f"{label} slot must not contain acquired source contents")
            if slot.get("external_fetch_performed") is not False:
                fail(f"{label} slot must not fetch externally")
            source_record = slot.get("source_record", {})
            if not source_record or any(value != "" for value in source_record.values()):
                fail(f"{label} source fields must remain empty before actual GPT Pro output")
            empty_slot_count += 1
    if empty_slot_count != EXPECTED_COUNTS["empty_source_field_slot_count"]:
        fail(f"{label} empty source field slot count mismatch")


def require_previous_filled_output_packet_gate() -> dict:
    gate = read_json(FILLED_OUTPUT_PACKET_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("filled output packet gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("filled output packet gate must point to this review goal")
    if gate.get("records_source") != "pasted_gpt_pro_yaml_not_supplied":
        fail("filled output packet gate records source mismatch")
    if gate.get("gpt_pro_output_supplied") is not False:
        fail("filled output packet gate must not claim GPT Pro output supplied")
    for key, value in EXPECTED_COUNTS.items():
        if key in gate and gate.get(key) != value:
            fail(f"filled output packet gate {key} mismatch")
    require_empty_slots(gate, "filled output packet gate")
    require_false_flags(gate.get("claim_boundary", {}), "filled output packet gate claim boundary")
    require_text_markers(
        FILLED_OUTPUT_PACKET_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-pro-filled-output-packet",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_review_record(record: dict, label: str, filled_output_gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "records_source": "pasted_gpt_pro_yaml_not_supplied",
        "gpt_pro_output_supplied": False,
        "source_collection_execution_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("source_required_candidate_ids") != filled_output_gate.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    if record.get("reviewed_filled_output_packet_uri") != FILLED_OUTPUT_PACKET.relative_to(ROOT).as_posix():
        fail(f"{label} reviewed packet uri mismatch")
    require_empty_slots(record, label)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(filled_output_gate: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-pro-filled-output-packet-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", filled_output_gate)


def require_validation_result(filled_output_gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_pro_filled_output_packet_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", filled_output_gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    filled_output_gate = require_previous_filled_output_packet_gate()
    require_text_markers(FILLED_OUTPUT_PACKET, PACKET_MARKERS)
    require_gate(filled_output_gate)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(filled_output_gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Pro Filled Output Packet Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_pro_filled_output_packet_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    print("records_source=pasted_gpt_pro_yaml_not_supplied")
    print("gpt_pro_output_supplied=false")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("source_collection_execution_allowed=false")
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
