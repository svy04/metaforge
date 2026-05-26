from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_owner_supplied_primary_source_evidence_record_template_v0_1.py"
COMPLETION_GUIDE_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_completion_guide_gate.json"
TEMPLATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_template.yml"
TEMPLATE_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_template_gate.json"
NEXT_OWNER_ACTION = CAPABILITIES / "owner_supplied_primary_source_evidence_record_template_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "owner_supplied_primary_source_evidence_record_template_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OWNER_SUPPLIED_PRIMARY_SOURCE_EVIDENCE_RECORD_TEMPLATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_template_v0_1"
PREVIOUS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_completion_guide_v0_1"
NEXT_SAFE_GOAL_ID = "avf_owner_supplied_primary_source_evidence_filled_record_review_v0_1"
TEMPLATE_DECISION = "OWNER_SUPPLIED_SOURCE_RECORD_TEMPLATE_READY"
GUIDE_DECISION = "OWNER_SUPPLIED_SOURCE_RECORD_COMPLETION_GUIDE_READY"

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
    COMPLETION_GUIDE_GATE,
    TEMPLATE,
    TEMPLATE_GATE,
    NEXT_OWNER_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEMPLATE_MARKERS = [
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    "template_status: fillable_owner_supplied_template",
    "owner_supplied_only: true",
    "source_collection_execution_allowed: false",
    "fields_completed: 0",
    "accepted_records: 0",
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
    "action_id: owner-complete-primary-source-evidence-record-from-template",
    "owner_input_required: true",
    "Fill the template with owner-supplied source metadata",
    "Do not ask Codex to fetch the URL",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "owner_supplied_primary_source_evidence_record_template_v0_1=true",
    "template_created=true",
    "template_gate_created=true",
    "required_source_fields=10",
    "fields_completed=0",
    "accepted_records=0",
    "owner_supplied_only=true",
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
    print("AVF Owner-Supplied Primary-Source Evidence Record Template v0.1 validation")
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


def require_completion_guide_gate() -> None:
    gate = read_json(COMPLETION_GUIDE_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("completion guide gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("completion guide gate must point to this template goal")
    if gate.get("guide_decision") != GUIDE_DECISION:
        fail("completion guide gate decision mismatch")
    if gate.get("owner_supplied_only") is not True:
        fail("completion guide gate must be owner supplied only")
    if gate.get("required_source_fields_documented") != REQUIRED_SOURCE_FIELDS:
        fail("completion guide gate required fields mismatch")
    if gate.get("allowed_source_kinds") != ALLOWED_SOURCE_KINDS:
        fail("completion guide gate allowed source kinds mismatch")
    if gate.get("source_collection_execution_allowed") is not False:
        fail("completion guide gate must keep source collection blocked")
    require_false_flags(gate.get("claim_boundary", {}), "completion guide gate")


def require_template_gate() -> None:
    gate = read_json(TEMPLATE_GATE)
    expected = {
        "gate_id": "avf-owner-supplied-primary-source-evidence-record-template-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "template_decision": TEMPLATE_DECISION,
        "owner_supplied_only": True,
        "required_source_fields_count": len(REQUIRED_SOURCE_FIELDS),
        "fields_completed": 0,
        "accepted_records": 0,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"template gate {key} mismatch")
    if gate.get("required_source_fields") != REQUIRED_SOURCE_FIELDS:
        fail("template gate required fields mismatch")
    if gate.get("allowed_source_kinds") != ALLOWED_SOURCE_KINDS:
        fail("template gate allowed source kinds mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "template gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_owner_supplied_primary_source_evidence_record_template_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("template_decision") != TEMPLATE_DECISION:
        fail("validation result template decision mismatch")
    if result.get("fields_completed") != 0:
        fail("validation result fields_completed must remain 0")
    if result.get("accepted_records") != 0:
        fail("validation result accepted_records must remain 0")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_completion_guide_gate()
    require_text_markers(TEMPLATE, TEMPLATE_MARKERS)
    require_template_gate()
    require_text_markers(NEXT_OWNER_ACTION, NEXT_OWNER_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Owner-Supplied Primary-Source Evidence Record Template v0.1 validation")
    print("RESULT: PASS")
    print("owner_supplied_primary_source_evidence_record_template_v0_1=true")
    print("template_created=true")
    print("template_gate_created=true")
    print("required_source_fields=10")
    print("fields_completed=0")
    print("accepted_records=0")
    print("owner_supplied_only=true")
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
