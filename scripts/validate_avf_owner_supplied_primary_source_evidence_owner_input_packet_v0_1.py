from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_owner_supplied_primary_source_evidence_owner_input_packet_v0_1.py"
FILLED_RECORD_REVIEW_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_filled_record_review_gate.json"
INPUT_PACKET = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet.yml"
INPUT_PACKET_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_gate.json"
NEXT_OWNER_ACTION = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OWNER_SUPPLIED_PRIMARY_SOURCE_EVIDENCE_OWNER_INPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_owner_input_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_filled_record_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_owner_supplied_primary_source_evidence_owner_input_packet_review_v0_1"
PREVIOUS_REVIEW_DECISION = "OWNER_FILLED_SOURCE_RECORD_REJECTED_EMPTY_TEMPLATE"
PACKET_DECISION = "OWNER_INPUT_PACKET_READY_FOR_OWNER_SUPPLIED_SOURCE_RECORD"

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
]

ALLOWED_SOURCE_KINDS = [
    "official_docs",
    "original_repository",
    "paper",
    "patent",
    "standard",
    "maintained_implementation",
    "local_repo_evidence",
]

REQUIRED_FILES = [
    RUNNER,
    FILLED_RECORD_REVIEW_GATE,
    INPUT_PACKET,
    INPUT_PACKET_GATE,
    NEXT_OWNER_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

INPUT_PACKET_MARKERS = [
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    "packet_status: waiting_for_owner_input",
    "owner_input_required: true",
    "owner_supplied_only: true",
    "filled_record_supplied: false",
    "fields_completed: 0",
    "accepted_records: 0",
    "source_collection_execution_allowed: false",
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
    "official_docs",
    "original_repository",
    "paper",
    "patent",
    "standard",
    "maintained_implementation",
    "local_repo_evidence",
    "Do not ask Codex to fetch the URL",
    "external_fetch_performed: false",
    "protected_action_executed: false",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_OWNER_MARKERS = [
    "action_id: owner-paste-primary-source-evidence-record-into-input-packet",
    "owner_input_required: true",
    "Paste exactly one completed source record into the input packet",
    "Do not ask Codex to fetch the URL",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "owner_supplied_primary_source_evidence_owner_input_packet_v0_1=true",
    "owner_input_packet_created=true",
    "owner_input_packet_gate_created=true",
    "packet_status=waiting_for_owner_input",
    "owner_input_required=true",
    "filled_record_supplied=false",
    "fields_completed=0",
    "accepted_records=0",
    "source_collection_execution_allowed=false",
    "external_fetch_performed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "dependency_install_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Owner-Supplied Primary-Source Evidence Owner Input Packet v0.1 validation")
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


def require_filled_record_review_gate() -> None:
    gate = read_json(FILLED_RECORD_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("filled-record review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("filled-record review gate must point to this owner input packet goal")
    if gate.get("review_decision") != PREVIOUS_REVIEW_DECISION:
        fail("filled-record review gate decision mismatch")
    if gate.get("filled_record_supplied") is not False:
        fail("filled-record review gate must prove no owner-filled record exists yet")
    if gate.get("fields_completed") != 0:
        fail("filled-record review gate must show zero completed fields")
    if gate.get("accepted_records") != 0:
        fail("filled-record review gate must not accept records")
    if gate.get("source_collection_execution_allowed") is not False:
        fail("filled-record review gate must keep source collection blocked")
    require_false_flags(gate.get("claim_boundary", {}), "filled-record review gate")


def require_input_packet_gate() -> None:
    gate = read_json(INPUT_PACKET_GATE)
    expected = {
        "gate_id": "avf-owner-supplied-primary-source-evidence-owner-input-packet-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "packet_decision": PACKET_DECISION,
        "packet_status": "waiting_for_owner_input",
        "owner_input_required": True,
        "owner_supplied_only": True,
        "filled_record_supplied": False,
        "required_source_fields_count": len(REQUIRED_SOURCE_FIELDS),
        "fields_completed": 0,
        "accepted_records": 0,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"owner input packet gate {key} mismatch")
    if gate.get("required_source_fields") != REQUIRED_SOURCE_FIELDS:
        fail("owner input packet gate required fields mismatch")
    if gate.get("allowed_source_kinds") != ALLOWED_SOURCE_KINDS:
        fail("owner input packet gate allowed source kinds mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "owner input packet gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_owner_supplied_primary_source_evidence_owner_input_packet_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("packet_decision") != PACKET_DECISION:
        fail("validation result packet decision mismatch")
    if result.get("owner_input_required") is not True:
        fail("validation result must require owner input")
    if result.get("filled_record_supplied") is not False:
        fail("validation result must keep filled_record_supplied=false")
    if result.get("accepted_records") != 0:
        fail("validation result accepted_records must remain 0")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_filled_record_review_gate()
    require_text_markers(INPUT_PACKET, INPUT_PACKET_MARKERS)
    require_input_packet_gate()
    require_text_markers(NEXT_OWNER_ACTION, NEXT_OWNER_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Owner-Supplied Primary-Source Evidence Owner Input Packet v0.1 validation")
    print("RESULT: PASS")
    print("owner_supplied_primary_source_evidence_owner_input_packet_v0_1=true")
    print("owner_input_packet_created=true")
    print("owner_input_packet_gate_created=true")
    print("packet_status=waiting_for_owner_input")
    print("owner_input_required=true")
    print("filled_record_supplied=false")
    print("fields_completed=0")
    print("accepted_records=0")
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
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
