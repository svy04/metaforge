from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1.py"
SOURCE_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_gate.json"
SOURCE_PACKET_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_CODEX_PRIMARY_SOURCE_OUTPUT_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_codex_primary_source_output_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_packet_v0_1"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_CODEX_OUTPUT_PACKET_REVIEWED_UNACCEPTED"
REVIEW_STATUS = "codex_primary_source_records_review_passed_ready_for_acceptance_decision"

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "source_record_count": 16,
    "required_source_field_count": 12,
    "reviewed_source_record_count": 16,
    "review_blocker_count": 0,
    "accepted_records": 0,
    "ready_for_acceptance_decision_count": 1,
    "assistant_web_primary_source_research_performed_count": 1,
    "gpt_pro_output_supplied_count": 0,
    "codex_script_external_fetch_performed_count": 0,
    "dependency_install_performed_count": 0,
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

REQUIRED_SOURCE_FIELDS = [
    "source_id",
    "source_title",
    "source_kind",
    "source_uri",
    "source_version_or_date",
    "source_owner_or_publisher",
    "license_or_rights_note",
    "claim_supported",
    "evidence_excerpt_summary",
    "verification_notes",
    "source_reference_lines",
    "retrieval_method",
]

ALLOWED_SOURCE_KINDS = {
    "official_docs",
    "original_repository",
    "paper",
}

REQUIRED_FILES = [
    RUNNER,
    SOURCE_PACKET_GATE,
    SOURCE_PACKET_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "records_source=codex_assistant_primary_source_web_research",
    "source_records_reviewed=true",
    "all_required_source_fields_present=true",
    "source_kind_rights_claim_reference_retrieval_checked=true",
    "candidate_count=7",
    "source_record_count=16",
    "required_source_field_count=12",
    "reviewed_source_record_count=16",
    "review_blocker_count=0",
    "accepted_records=0",
    "ready_for_acceptance_decision_count=1",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-acceptance-decision-packet",
    "owner_approval_required_before_execution: false",
    "Create an acceptance decision packet for the reviewed Codex primary-source records",
    "Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Codex Output Packet Review v0.1 validation")
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


def require_source_record_fields(source: dict, label: str) -> None:
    source_id = source.get("source_id", "<missing>")
    for field in REQUIRED_SOURCE_FIELDS:
        if not source.get(field):
            fail(f"{label} {source_id} missing {field}")
    if source.get("source_kind") not in ALLOWED_SOURCE_KINDS:
        fail(f"{label} {source_id} source kind not allowed")
    if source.get("retrieval_method") != "codex_assistant_web_open_primary_source_current_turn":
        fail(f"{label} {source_id} retrieval method mismatch")
    if "turn" not in source.get("source_reference_lines", "") or " L" not in source.get("source_reference_lines", ""):
        fail(f"{label} {source_id} must include turn/line references")
    boundary_notes = source.get("verification_notes", "").lower()
    boundary_markers = [
        "not approved",
        "required",
        "no clone performed",
        "not an adoption approval",
        "no offensive use enabled",
    ]
    if not any(marker in boundary_notes for marker in boundary_markers):
        fail(f"{label} {source_id} verification notes must preserve non-adoption boundary")


def require_source_packet_gate() -> dict:
    gate = read_json(SOURCE_PACKET_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("source packet gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("source packet gate must point to this review goal")
    if gate.get("records_source") != "codex_assistant_primary_source_web_research":
        fail("source packet gate records source mismatch")
    if gate.get("gpt_pro_output_supplied") is not False:
        fail("source packet gate must not claim GPT Pro output")
    if gate.get("codex_script_external_fetch_performed") is not False:
        fail("source packet gate must not claim script external fetch")
    if gate.get("accepted_records") != 0:
        fail("source packet gate must have zero accepted records")
    for key, value in EXPECTED_COUNTS.items():
        if key in gate and gate.get(key) != value:
            fail(f"source packet gate {key} mismatch")
    records = gate.get("source_records", [])
    if len(records) != EXPECTED_COUNTS["source_record_count"]:
        fail("source packet gate source record count mismatch")
    for source in records:
        if source.get("acceptance_status") != "unreviewed":
            fail("source packet gate records must remain unreviewed before review")
        if source.get("filled_record_supplied") is not True:
            fail("source packet gate records must be supplied")
        require_source_record_fields(source, "source packet gate")
    require_false_flags(gate.get("claim_boundary", {}), "source packet gate claim boundary")
    require_text_markers(
        SOURCE_PACKET_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-codex-primary-source-output-packet",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_review_record(record: dict, label: str, source_gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "records_source": "codex_assistant_primary_source_web_research",
        "source_records_reviewed": True,
        "all_required_source_fields_present": True,
        "source_kind_rights_claim_reference_retrieval_checked": True,
        "accepted_records": 0,
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
    if record.get("source_required_candidate_ids") != source_gate.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    reviewed_records = record.get("reviewed_source_records", [])
    if len(reviewed_records) != EXPECTED_COUNTS["source_record_count"]:
        fail(f"{label} reviewed source record count mismatch")
    for source in reviewed_records:
        if source.get("review_status") != "reviewed_unaccepted":
            fail(f"{label} source review status mismatch")
        if source.get("acceptance_status") != "unreviewed":
            fail(f"{label} source acceptance status must remain unreviewed")
        require_source_record_fields(source, label)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(source_gate: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-codex-output-packet-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", source_gate)


def require_validation_result(source_gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", source_gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    source_gate = require_source_packet_gate()
    require_gate(source_gate)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(source_gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Codex Output Packet Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    print("records_source=codex_assistant_primary_source_web_research")
    print("source_records_reviewed=true")
    print("all_required_source_fields_present=true")
    print("source_kind_rights_claim_reference_retrieval_checked=true")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
