from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_owner_input_packet_review_v0_1.py"
INPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet.yml"
INPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_gate.json"
INPUT_PACKET_NEXT_OWNER_ACTION = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_next_owner_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_OWNER_INPUT_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_pro_prompt_v0_1"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_OWNER_INPUT_PACKET_REVIEWED_REPO_LOCAL"
REVIEW_STATUS = "owner_input_packet_review_passed_ready_for_pro_prompt"

EXPECTED_COUNTS = {
    "candidate_input_section_count": 7,
    "fillable_source_record_slot_count": 16,
    "required_source_field_count": 12,
    "owner_input_packet_review_blocker_count": 0,
    "ready_for_pro_prompt_count": 1,
    "source_contents_acquired_count": 0,
    "external_fetch_performed_count": 0,
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
    INPUT_PACKET,
    INPUT_PACKET_GATE,
    INPUT_PACKET_NEXT_OWNER_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_owner_input_packet_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "candidate_input_section_count=7",
    "fillable_source_record_slot_count=16",
    "required_source_field_count=12",
    "owner_input_packet_review_blocker_count=0",
    "ready_for_pro_prompt_count=1",
    "source_contents_acquired_count=0",
    "external_fetch_performed_count=0",
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
    "action_id: create-capability-candidate-primary-source-pro-prompt",
    "owner_approval_required_before_execution: false",
    "Create a GPT Pro prompt for manually filling primary-source evidence",
    "Do not fetch external sources inside Codex, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Owner Input Packet Review v0.1 validation")
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


def require_previous_input_packet() -> dict:
    gate = read_json(INPUT_PACKET_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("input packet gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("input packet gate must point to this review goal")
    for key, value in EXPECTED_COUNTS.items():
        if key in gate and key not in {"owner_input_packet_review_blocker_count", "ready_for_pro_prompt_count"}:
            if gate.get(key) != value:
                fail(f"input packet gate {key} mismatch")
    if gate.get("owner_input_required") is not True:
        fail("input packet gate must require owner input")
    if gate.get("source_collection_execution_allowed") is not False:
        fail("input packet gate must keep source collection disabled")
    if gate.get("accepted_records") != 0:
        fail("input packet gate must have zero accepted records")
    require_false_flags(gate.get("claim_boundary", {}), "input packet gate claim boundary")
    require_text_markers(
        INPUT_PACKET_NEXT_OWNER_ACTION,
        [
            "action_id: owner-fill-capability-candidate-primary-source-input-packet",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_review_record(record: dict, label: str, input_gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("source_required_candidate_ids") != input_gate.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    if record.get("reviewed_artifact_uri") != INPUT_PACKET.relative_to(ROOT).as_posix():
        fail(f"{label} reviewed artifact uri mismatch")
    if record.get("source_collection_execution_allowed") is not False:
        fail(f"{label} must keep source collection disabled")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(input_gate: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-owner-input-packet-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", input_gate)


def require_validation_result(input_gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_owner_input_packet_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", input_gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    input_gate = require_previous_input_packet()
    require_gate(input_gate)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(input_gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Owner Input Packet Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_owner_input_packet_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
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
