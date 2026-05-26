from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_content_safety_manual_records_v0_1.py"
NAMESPACE_MAP = CAPABILITIES / "primary_source_namespace_map.json"
NAMESPACE_GATE = CAPABILITIES / "primary_source_namespace_map_gate.json"
NAMESPACE_NEXT_ACTION = CAPABILITIES / "primary_source_namespace_map_next_action.yml"
LEDGER = ROOT / "avf" / "cells" / "evidence" / "generated" / "primary_source_ledger.json"
CONTENT_SAFETY_RECORDS = CAPABILITIES / "primary_source_content_safety_manual_records.json"
CONTENT_SAFETY_GATE = CAPABILITIES / "primary_source_content_safety_manual_records_gate.json"
CONTENT_SAFETY_REPORT = CAPABILITIES / "primary_source_content_safety_manual_records_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_content_safety_manual_records_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_content_safety_manual_records_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_CONTENT_SAFETY_MANUAL_RECORDS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_content_safety_manual_records_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_evidence_registry_namespace_map_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_product_quality_missing_inputs_plan_v0_1"
RECORD_DECISION = "CONTENT_SAFETY_PRIMARY_SOURCE_MANUAL_RECORDS_CREATED_FROM_LEDGER"
RECORD_STATUS = "manual_records_created_content_summary_review_required"
CLOSED_GAP_ID = "gap-content-safety-policy-sources-missing-manual-records"

SOURCE_TARGET_IDS = [
    "src-ftc-endorsement-guides",
    "src-ftc-ai-claims",
]

EXPECTED_COUNTS = {
    "content_safety_manual_record_count": 2,
    "source_content_summary_required_count": 2,
    "slice_closed_gap_count": 1,
    "gaps_closed_count": 2,
    "remaining_gap_count": 2,
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
    NAMESPACE_MAP,
    NAMESPACE_GATE,
    NAMESPACE_NEXT_ACTION,
    LEDGER,
    CONTENT_SAFETY_RECORDS,
    CONTENT_SAFETY_GATE,
    CONTENT_SAFETY_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_content_safety_manual_records_v0_1=true",
    f"record_decision={RECORD_DECISION}",
    f"record_status={RECORD_STATUS}",
    "content_safety_manual_record_count=2",
    "source_content_summary_required_count=2",
    "slice_closed_gap_count=1",
    "gaps_closed_count=2",
    "remaining_gap_count=2",
    "content_safety_policy_source_record_gap_closed=true",
    "source_contents_acquired=false",
    "src-ftc-endorsement-guides",
    "src-ftc-ai-claims",
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
    "action_id: create-product-quality-primary-source-missing-inputs-plan",
    "owner_approval_required_before_execution: false",
    "Plan closure for product-quality reports missing primary-source inputs",
    "Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Primary-Source Content Safety Manual Records v0.1 validation")
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


def require_previous_namespace_map() -> None:
    for label, record in [
        ("namespace map", read_json(NAMESPACE_MAP)),
        ("namespace gate", read_json(NAMESPACE_GATE)),
    ]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            fail(f"{label} goal_id mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            fail(f"{label} must point to this content-safety records goal")
        if record.get("namespace_gap_closed") is not True:
            fail(f"{label} must close namespace gap first")
        if record.get("remaining_gap_count") != 3:
            fail(f"{label} remaining gap count mismatch")
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        NAMESPACE_NEXT_ACTION,
        [
            "action_id: create-content-safety-primary-source-manual-records",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )


def require_ledger_inputs() -> None:
    ledger = read_json(LEDGER)
    sources = {source.get("source_id"): source for source in ledger.get("sources", [])}
    missing = [source_id for source_id in SOURCE_TARGET_IDS if source_id not in sources]
    if missing:
        fail("missing content safety ledger sources:\n" + "\n".join(missing))
    for source_id in SOURCE_TARGET_IDS:
        source = sources[source_id]
        if not source.get("url", "").startswith("https://www.ftc.gov/"):
            fail(f"{source_id} must use FTC source URL")
        if "safety-cell" not in source.get("used_by_cells", []):
            fail(f"{source_id} must be used by safety-cell")


def require_records(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "record_decision": RECORD_DECISION,
        "record_status": RECORD_STATUS,
        "closed_gap_id": CLOSED_GAP_ID,
        "content_safety_policy_source_record_gap_closed": True,
        "source_contents_acquired": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("source_target_ids") != SOURCE_TARGET_IDS:
        fail(f"{label} source target ids mismatch")
    records = record.get("source_records")
    if not isinstance(records, list) or len(records) != EXPECTED_COUNTS["content_safety_manual_record_count"]:
        fail(f"{label} source records count mismatch")
    for source_record in records:
        if source_record.get("source_contents_acquired") is not False:
            fail(f"{label} source contents must not be claimed acquired")
        if source_record.get("source_content_summary_required_for_promotion") is not True:
            fail(f"{label} source content summary must be required for promotion")
        if source_record.get("record_status") != "ledger_derived_manual_record_shell":
            fail(f"{label} record status mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate() -> None:
    gate = read_json(CONTENT_SAFETY_GATE)
    if gate.get("gate_id") != "avf-primary-source-content-safety-manual-records-gate-v0-1":
        fail("content safety gate id mismatch")
    if gate.get("status") != "PASS":
        fail("content safety gate status must be PASS")
    require_records(gate, "content safety gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_content_safety_manual_records_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_records(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_namespace_map()
    require_ledger_inputs()
    require_records(read_json(CONTENT_SAFETY_RECORDS), "content safety records")
    require_gate()
    require_text_markers(CONTENT_SAFETY_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Content Safety Manual Records v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_content_safety_manual_records_v0_1=true")
    print(f"record_decision={RECORD_DECISION}")
    print(f"record_status={RECORD_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("content_safety_policy_source_record_gap_closed=true")
    print("source_contents_acquired=false")
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
