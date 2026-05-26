from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
EVIDENCE = ROOT / "avf" / "cells" / "evidence" / "generated"
PRODUCT_QUALITY = ROOT / "docs" / "product-quality"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_evidence_registry_gap_review_v0_1.py"
PREVIOUS_OBS_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2_gate.json"
PRODUCT_REGISTRY = PRODUCT_QUALITY / "primary-source-registry-report.json"
AVF_LEDGER = EVIDENCE / "primary_source_ledger.json"
MANUAL_RECORDS = CAPABILITIES / "primary_source_manual_records.json"
GAP_REVIEW = CAPABILITIES / "primary_source_evidence_registry_gap_review.json"
GAP_GATE = CAPABILITIES / "primary_source_evidence_registry_gap_review_gate.json"
GAP_REPORT = CAPABILITIES / "primary_source_evidence_registry_gap_review_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_evidence_registry_gap_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_evidence_registry_gap_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_EVIDENCE_REGISTRY_GAP_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_evidence_registry_gap_review_v0_1"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2"
NEXT_SAFE_GOAL_ID = "avf_primary_source_evidence_registry_gap_closure_plan_v0_1"
REVIEW_DECISION = "PRIMARY_SOURCE_EVIDENCE_REGISTRY_GAPS_REVIEWED_REPO_LOCAL"
REVIEW_STATUS = "gaps_found_closure_plan_required"

EXPECTED_COUNTS = {
    "primary_source_entry_count": 153,
    "unique_source_url_count": 84,
    "reports_with_primary_source_inputs_count": 49,
    "reports_missing_primary_source_inputs_count": 35,
    "avf_ledger_source_count": 9,
    "manual_source_record_count": 7,
    "content_safety_policy_sources_missing_manual_records_count": 2,
    "gap_count": 4,
}

GAP_IDS = [
    "gap-product-quality-reports-missing-primary-source-inputs",
    "gap-avf-ledger-to-manual-record-namespace-map",
    "gap-content-safety-policy-sources-missing-manual-records",
    "gap-adoption-evidence-gates-not-yet-linked-to-registry",
]

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

SOURCE_INPUT_FALSE_FLAGS = [
    flag
    for flag in FALSE_FLAGS
    if flag
    not in {
        "runtime_export_performed",
        "collector_started",
        "telemetry_export_performed",
    }
]

REQUIRED_FILES = [
    RUNNER,
    PREVIOUS_OBS_GATE,
    PRODUCT_REGISTRY,
    AVF_LEDGER,
    MANUAL_RECORDS,
    GAP_REVIEW,
    GAP_GATE,
    GAP_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_evidence_registry_gap_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "primary_source_entry_count=153",
    "unique_source_url_count=84",
    "reports_with_primary_source_inputs_count=49",
    "reports_missing_primary_source_inputs_count=35",
    "avf_ledger_source_count=9",
    "manual_source_record_count=7",
    "content_safety_policy_sources_missing_manual_records_count=2",
    "gap_count=4",
    "gap-product-quality-reports-missing-primary-source-inputs",
    "gap-avf-ledger-to-manual-record-namespace-map",
    "gap-content-safety-policy-sources-missing-manual-records",
    "gap-adoption-evidence-gates-not-yet-linked-to-registry",
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
    "runtime_export_performed=false",
    "collector_started=false",
    "telemetry_export_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

GAP_REPORT_MARKERS = [
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "primary_source_entry_count=153",
    "reports_missing_primary_source_inputs_count=35",
    "content_safety_policy_sources_missing_manual_records_count=2",
    "gap_count=4",
    "No external fetch, provider call, live model call, scraping, dependency install, OSS clone, runtime integration, deploy, publish, or readiness claim was performed.",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-primary-source-evidence-registry-gap-closure-plan",
    "owner_approval_required_before_execution: false",
    "Close repo-local registry gaps with deterministic mapping and owner-supplied/manual primary-source records",
    "Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Primary-Source Evidence Registry Gap Review v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str, flags: list[str] | None = None) -> None:
    for flag in flags or FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_previous_observability_gate() -> None:
    gate = read_json(PREVIOUS_OBS_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous observability gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous observability gate must point to this registry gap review goal")
    if gate.get("runtime_approval_wait_state") is not True:
        fail("previous observability gate must place runtime approval in wait state")
    if gate.get("switch_to_non_protected_work") is not True:
        fail("previous observability gate must switch to non-protected work")
    require_false_flags(gate.get("claim_boundary", {}), "previous observability gate claim boundary")


def require_source_inputs() -> None:
    product = read_json(PRODUCT_REGISTRY)
    if product.get("primarySourceEntryCount") != EXPECTED_COUNTS["primary_source_entry_count"]:
        fail("product registry primary source entry count mismatch")
    if product.get("uniqueSourceUrlCount") != EXPECTED_COUNTS["unique_source_url_count"]:
        fail("product registry unique source url count mismatch")
    if len(product.get("reportsWithPrimarySourceInputs", [])) != EXPECTED_COUNTS["reports_with_primary_source_inputs_count"]:
        fail("product registry reports-with count mismatch")
    if len(product.get("reportsMissingPrimarySourceInputs", [])) != EXPECTED_COUNTS["reports_missing_primary_source_inputs_count"]:
        fail("product registry reports-missing count mismatch")
    if product.get("externalSourceFetchPerformed") is not False:
        fail("product registry must record no external source fetch")

    ledger = read_json(AVF_LEDGER)
    if len(ledger.get("sources", [])) != EXPECTED_COUNTS["avf_ledger_source_count"]:
        fail("AVF ledger source count mismatch")
    if ledger.get("automation_fetch_performed") is not False:
        fail("AVF ledger must record no automation fetch")

    manual = read_json(MANUAL_RECORDS)
    if len(manual.get("source_records", [])) != EXPECTED_COUNTS["manual_source_record_count"]:
        fail("manual source record count mismatch")
    if manual.get("source_contents_acquired") is not True:
        fail("manual source records must record source contents acquired")
    require_false_flags(manual.get("claim_boundary", {}), "manual source records claim boundary", SOURCE_INPUT_FALSE_FLAGS)


def require_gap_record(record: dict, label: str) -> None:
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
    if record.get("gap_ids") != GAP_IDS:
        fail(f"{label} gap ids mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gap_gate() -> None:
    gate = read_json(GAP_GATE)
    if gate.get("gate_id") != "avf-primary-source-evidence-registry-gap-review-gate-v0-1":
        fail("gap gate id mismatch")
    if gate.get("status") != "PASS":
        fail("gap gate status must be PASS")
    require_gap_record(gate, "gap gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_evidence_registry_gap_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_gap_record(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_observability_gate()
    require_source_inputs()
    require_gap_record(read_json(GAP_REVIEW), "gap review")
    require_gap_gate()
    require_text_markers(GAP_REPORT, GAP_REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Evidence Registry Gap Review v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_evidence_registry_gap_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
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
