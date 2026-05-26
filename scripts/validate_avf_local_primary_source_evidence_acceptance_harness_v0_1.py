from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOAL_GENERATED = ROOT / "avf" / "goals" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_local_primary_source_evidence_acceptance_harness_v0_1.py"
MATRIX = GOAL_GENERATED / "active_objective_completion_matrix_v0_1.json"
SCHEMA = CAPABILITIES / "local_primary_source_evidence_acceptance.schema.yml"
SAMPLE = CAPABILITIES / "local_primary_source_evidence_acceptance_sample.yml"
GATE = CAPABILITIES / "local_primary_source_evidence_acceptance_gate.json"
NEXT_OWNER_ACTION = CAPABILITIES / "local_primary_source_evidence_acceptance_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "local_primary_source_evidence_acceptance_harness_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_LOCAL_PRIMARY_SOURCE_EVIDENCE_ACCEPTANCE_HARNESS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_local_primary_source_evidence_acceptance_harness_v0_1"
NEXT_SAFE_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_review_v0_1"
GATE_DECISION = "OWNER_SUPPLIED_SOURCE_RECORD_SCHEMA_READY_EMPTY_SAMPLE_REJECTED"

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
    MATRIX,
    SCHEMA,
    SAMPLE,
    GATE,
    NEXT_OWNER_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

SCHEMA_MARKERS = [
    "schema_id: local_primary_source_evidence_acceptance_v0_1",
    "accepted_collection_mode: owner_supplied_only",
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
    "disallowed_actions:",
    "No source collection execution",
    "No provider calls",
    "No external fetch",
    "No automated scraping",
]

SAMPLE_MARKERS = [
    "sample_id: empty_owner_supplied_primary_source_record",
    "collection_mode: owner_supplied_only",
    "source_id:",
    "source_title:",
    "source_kind:",
    "source_uri:",
    "claim_supported:",
    "evidence_excerpt_summary:",
    "sample_status: incomplete_rejected",
]

NEXT_OWNER_MARKERS = [
    "action_id: owner-fill-local-primary-source-evidence-record",
    "owner_input_required: true",
    "Fill every required source field",
    "Paste only owner-supplied source metadata or excerpts",
    "Do not ask Codex to fetch the URL",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "local_primary_source_evidence_acceptance_harness_v0_1=true",
    "owner_supplied_only=true",
    "required_source_fields=10",
    "accepted_records=0",
    "rejected_records=1",
    "empty_sample_rejected=true",
    "source_collection_execution_allowed=false",
    "external_fetch_performed=false",
    "automated_scraping_performed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
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
    print("AVF Local Primary-Source Evidence Acceptance Harness v0.1 validation")
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


def require_matrix() -> None:
    matrix = read_json(MATRIX)
    if matrix.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("active objective matrix must point to this acceptance harness")
    if matrix.get("objective_completion_proven") is not False:
        fail("active objective matrix must not prove completion")
    if matrix.get("source_collection_terminal_condition") != "PROTECTED_ACTION_REQUIRED":
        fail("active objective matrix must preserve protected source boundary")
    require_false_flags(matrix.get("claim_boundary", {}), "active objective matrix")


def require_gate() -> None:
    gate = read_json(GATE)
    expected = {
        "gate_id": "avf-local-primary-source-evidence-acceptance-harness-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "gate_decision": GATE_DECISION,
        "owner_supplied_only": True,
        "required_source_fields_count": len(REQUIRED_SOURCE_FIELDS),
        "accepted_records": 0,
        "rejected_records": 1,
        "empty_sample_rejected": True,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"acceptance gate {key} mismatch")
    if gate.get("required_source_fields") != REQUIRED_SOURCE_FIELDS:
        fail("acceptance gate required fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "acceptance gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_local_primary_source_evidence_acceptance_harness_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("accepted_records") != 0:
        fail("validation result must not accept empty records")
    if result.get("rejected_records") != 1:
        fail("validation result must reject empty sample")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_matrix()
    require_text_markers(SCHEMA, SCHEMA_MARKERS)
    require_text_markers(SAMPLE, SAMPLE_MARKERS)
    require_gate()
    require_text_markers(NEXT_OWNER_ACTION, NEXT_OWNER_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Local Primary-Source Evidence Acceptance Harness v0.1 validation")
    print("RESULT: PASS")
    print("local_primary_source_evidence_acceptance_harness_v0_1=true")
    print("owner_supplied_only=true")
    print("required_source_fields=10")
    print("accepted_records=0")
    print("rejected_records=1")
    print("empty_sample_rejected=true")
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
