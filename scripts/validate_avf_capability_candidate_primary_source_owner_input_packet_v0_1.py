from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_owner_input_packet_v0_1.py"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_gate.json"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_next_action.yml"
INPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet.yml"
INPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_gate.json"
INPUT_PACKET_REPORT = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_report.md"
NEXT_OWNER_ACTION = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_OWNER_INPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_review_v0_1"
PACKET_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_OWNER_INPUT_PACKET_CREATED_REPO_LOCAL"
PACKET_STATUS = "waiting_for_owner_filled_primary_source_evidence"

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

ALLOWED_SOURCE_KINDS = [
    "official_docs",
    "original_repository",
    "paper",
    "benchmark",
    "standard",
    "patent",
    "maintained_implementation",
    "local_repo_evidence",
]

EXPECTED_COUNTS = {
    "candidate_input_section_count": 7,
    "fillable_source_record_slot_count": 16,
    "required_source_field_count": 12,
    "filled_record_supplied_count": 0,
    "accepted_records": 0,
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
    REVIEW_GATE,
    REVIEW_NEXT_ACTION,
    INPUT_PACKET,
    INPUT_PACKET_GATE,
    INPUT_PACKET_REPORT,
    NEXT_OWNER_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

INPUT_PACKET_MARKERS = [
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"packet_decision: {PACKET_DECISION}",
    f"packet_status: {PACKET_STATUS}",
    "owner_input_required: true",
    "owner_supplied_only: true",
    "source_collection_execution_allowed: false",
    "candidate_input_sections:",
    "cap-k8s-workflow-argo",
    "cap-general-orchestration-kestra-prefect-airflow",
    "cap-evidence-lineage-dagster",
    "cap-rag-document-pipeline-haystack",
    "cap-llm-observability-langfuse-phoenix",
    "cap-eval-redteam-promptfoo-ragas",
    "cap-coding-executor-openhands-sweagent",
    "src-argo-workflows-official-docs",
    "src-airflow-official-docs",
    "src-ragas-paper-or-benchmark-record",
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
    "Do not ask Codex to fetch URLs",
    "external_fetch_performed: false",
    "protected_action_executed: false",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_OWNER_MARKERS = [
    "action_id: owner-fill-capability-candidate-primary-source-input-packet",
    "owner_input_required: true",
    "Fill all required source fields for each selected source target",
    "Do not ask Codex to fetch URLs",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_owner_input_packet_v0_1=true",
    "owner_input_packet_created=true",
    "owner_input_packet_gate_created=true",
    f"packet_decision={PACKET_DECISION}",
    f"packet_status={PACKET_STATUS}",
    "candidate_input_section_count=7",
    "fillable_source_record_slot_count=16",
    "required_source_field_count=12",
    "filled_record_supplied_count=0",
    "accepted_records=0",
    "source_collection_execution_allowed=false",
    "external_fetch_performed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "dependency_install_performed=false",
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
    print("AVF Capability Candidate Primary-Source Owner Input Packet v0.1 validation")
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


def require_previous_review_gate() -> dict:
    gate = read_json(REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("review gate must point to this owner input packet goal")
    if gate.get("review_blocker_count") != 0:
        fail("review gate must have zero blockers")
    if gate.get("ready_for_owner_input_packet_count") != EXPECTED_COUNTS["candidate_input_section_count"]:
        fail("review gate ready count mismatch")
    if gate.get("source_contents_acquired_count") != 0:
        fail("review gate must show no source contents acquired")
    if gate.get("external_fetch_performed_count") != 0:
        fail("review gate external fetch count must be 0")
    require_false_flags(gate.get("claim_boundary", {}), "review gate claim boundary")
    require_text_markers(
        REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-owner-input-packet",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_input_packet_gate(review_gate: dict) -> None:
    gate = read_json(INPUT_PACKET_GATE)
    expected = {
        "gate_id": "avf-capability-candidate-primary-source-owner-input-packet-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "packet_decision": PACKET_DECISION,
        "packet_status": PACKET_STATUS,
        "owner_input_required": True,
        "owner_supplied_only": True,
        "source_collection_execution_allowed": False,
        "accepted_records": 0,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"owner input packet gate {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if gate.get(key) != value:
            fail(f"owner input packet gate {key} mismatch")
    if gate.get("required_source_fields") != REQUIRED_SOURCE_FIELDS:
        fail("owner input packet gate required source fields mismatch")
    if gate.get("allowed_source_kinds") != ALLOWED_SOURCE_KINDS:
        fail("owner input packet gate allowed source kinds mismatch")
    if gate.get("source_required_candidate_ids") != review_gate.get("source_required_candidate_ids"):
        fail("owner input packet gate candidate ids mismatch")
    sections = gate.get("candidate_input_sections")
    if not isinstance(sections, list) or len(sections) != EXPECTED_COUNTS["candidate_input_section_count"]:
        fail("owner input packet gate candidate section count mismatch")
    if sum(len(section.get("source_input_slots", [])) for section in sections) != EXPECTED_COUNTS["fillable_source_record_slot_count"]:
        fail("owner input packet gate source slot count mismatch")
    for section in sections:
        if section.get("filled_record_supplied_count") != 0:
            fail("owner input packet gate section must start with no filled records")
        for slot in section.get("source_input_slots", []):
            if slot.get("source_input_status") != "waiting_for_owner_input":
                fail("source input slot status mismatch")
            if slot.get("source_contents_acquired") is not False:
                fail("source input slot must not contain acquired contents")
            if slot.get("external_fetch_performed") is not False:
                fail("source input slot must not fetch externally")
    require_false_flags(gate.get("claim_boundary", {}), "owner input packet gate")


def require_validation_result(review_gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_owner_input_packet_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    if result.get("packet_decision") != PACKET_DECISION:
        fail("validation result packet decision mismatch")
    if result.get("packet_status") != PACKET_STATUS:
        fail("validation result packet status mismatch")
    if result.get("source_required_candidate_ids") != review_gate.get("source_required_candidate_ids"):
        fail("validation result candidate ids mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if result.get(key) != value:
            fail(f"validation result {key} mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review_gate = require_previous_review_gate()
    require_text_markers(INPUT_PACKET, INPUT_PACKET_MARKERS)
    require_input_packet_gate(review_gate)
    require_text_markers(INPUT_PACKET_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_OWNER_ACTION, NEXT_OWNER_MARKERS)
    require_validation_result(review_gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Owner Input Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_owner_input_packet_v0_1=true")
    print("owner_input_packet_created=true")
    print("owner_input_packet_gate_created=true")
    print(f"packet_decision={PACKET_DECISION}")
    print(f"packet_status={PACKET_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("source_collection_execution_allowed=false")
    print("external_fetch_performed=false")
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
