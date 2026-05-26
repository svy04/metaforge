from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_owner_supplied_primary_source_evidence_filled_record_review_v0_1.py"
TEMPLATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_template.yml"
TEMPLATE_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_template_gate.json"
REVIEW_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_filled_record_review_gate.json"
REJECTION_REPORT = CAPABILITIES / "owner_supplied_primary_source_evidence_filled_record_review_rejection_report.md"
NEXT_OWNER_ACTION = CAPABILITIES / "owner_supplied_primary_source_evidence_filled_record_review_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "owner_supplied_primary_source_evidence_filled_record_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OWNER_SUPPLIED_PRIMARY_SOURCE_EVIDENCE_FILLED_RECORD_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_filled_record_review_v0_1"
PREVIOUS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_template_v0_1"
NEXT_SAFE_GOAL_ID = "avf_owner_supplied_primary_source_evidence_owner_input_packet_v0_1"
TEMPLATE_DECISION = "OWNER_SUPPLIED_SOURCE_RECORD_TEMPLATE_READY"
REVIEW_DECISION = "OWNER_FILLED_SOURCE_RECORD_REJECTED_EMPTY_TEMPLATE"

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

REQUIRED_FILES = [
    RUNNER,
    TEMPLATE,
    TEMPLATE_GATE,
    REVIEW_GATE,
    REJECTION_REPORT,
    NEXT_OWNER_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REJECTION_REPORT_MARKERS = [
    f"review_decision={REVIEW_DECISION}",
    "filled_record_supplied=false",
    "fields_reviewed=10",
    "fields_completed=0",
    "missing_required_fields=10",
    "accepted_records=0",
    "rejected_records=1",
    "source_collection_execution_allowed=false",
    "external_fetch_performed=false",
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

NEXT_OWNER_MARKERS = [
    "action_id: owner-supply-primary-source-evidence-record",
    "owner_input_required: true",
    "Paste one completed owner-supplied primary-source evidence record",
    "Do not ask Codex to fetch the URL",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "owner_supplied_primary_source_evidence_filled_record_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    "filled_record_supplied=false",
    "fields_reviewed=10",
    "fields_completed=0",
    "missing_required_fields=10",
    "accepted_records=0",
    "rejected_records=1",
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
    print("AVF Owner-Supplied Primary-Source Evidence Filled Record Review v0.1 validation")
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


def require_template_gate() -> None:
    gate = read_json(TEMPLATE_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("template gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("template gate must point to this filled-record review goal")
    if gate.get("template_decision") != TEMPLATE_DECISION:
        fail("template gate decision mismatch")
    if gate.get("required_source_fields") != REQUIRED_SOURCE_FIELDS:
        fail("template gate required fields mismatch")
    if gate.get("fields_completed") != 0:
        fail("template gate must start with zero completed fields")
    if gate.get("accepted_records") != 0:
        fail("template gate must not accept records")
    if gate.get("source_collection_execution_allowed") is not False:
        fail("template gate must keep source collection blocked")
    require_false_flags(gate.get("claim_boundary", {}), "template gate")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    expected = {
        "gate_id": "avf-owner-supplied-primary-source-evidence-filled-record-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "owner_supplied_only": True,
        "filled_record_supplied": False,
        "fields_reviewed": len(REQUIRED_SOURCE_FIELDS),
        "fields_completed": 0,
        "accepted_records": 0,
        "rejected_records": 1,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"filled-record review gate {key} mismatch")
    if gate.get("missing_required_fields") != REQUIRED_SOURCE_FIELDS:
        fail("filled-record review gate missing fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "filled-record review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_owner_supplied_primary_source_evidence_filled_record_review_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
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

    require_template_gate()
    require_review_gate()
    require_text_markers(REJECTION_REPORT, REJECTION_REPORT_MARKERS)
    require_text_markers(NEXT_OWNER_ACTION, NEXT_OWNER_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Owner-Supplied Primary-Source Evidence Filled Record Review v0.1 validation")
    print("RESULT: PASS")
    print("owner_supplied_primary_source_evidence_filled_record_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print("filled_record_supplied=false")
    print("fields_reviewed=10")
    print("fields_completed=0")
    print("missing_required_fields=10")
    print("accepted_records=0")
    print("rejected_records=1")
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
