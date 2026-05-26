from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_product_quality_missing_inputs_triage_v0_1.py"
MISSING_INPUTS_PLAN = CAPABILITIES / "primary_source_product_quality_missing_inputs_plan.json"
MISSING_INPUTS_GATE = CAPABILITIES / "primary_source_product_quality_missing_inputs_plan_gate.json"
MISSING_INPUTS_NEXT_ACTION = CAPABILITIES / "primary_source_product_quality_missing_inputs_plan_next_action.yml"
TRIAGE = CAPABILITIES / "primary_source_product_quality_missing_inputs_triage.json"
TRIAGE_GATE = CAPABILITIES / "primary_source_product_quality_missing_inputs_triage_gate.json"
TRIAGE_REPORT = CAPABILITIES / "primary_source_product_quality_missing_inputs_triage_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_product_quality_missing_inputs_triage_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_product_quality_missing_inputs_triage_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_PRODUCT_QUALITY_MISSING_INPUTS_TRIAGE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_product_quality_missing_inputs_triage_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_product_quality_missing_inputs_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_adoption_evidence_gate_links_v0_1"
TRIAGE_DECISION = "PRODUCT_QUALITY_MISSING_INPUTS_TRIAGED_TO_CLAIM_BOUNDARY_EXEMPTIONS"
TRIAGE_STATUS = "triage_complete_no_sources_attached"
CLOSED_GAP_ID = "gap-product-quality-reports-missing-primary-source-inputs"

EXPECTED_COUNTS = {
    "closure_target_count": 35,
    "triaged_target_count": 35,
    "attach_existing_evidence_count": 0,
    "claim_boundary_exemption_count": 35,
    "slice_closed_gap_count": 1,
    "gaps_closed_count": 3,
    "remaining_gap_count": 1,
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
    MISSING_INPUTS_PLAN,
    MISSING_INPUTS_GATE,
    MISSING_INPUTS_NEXT_ACTION,
    TRIAGE,
    TRIAGE_GATE,
    TRIAGE_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_product_quality_missing_inputs_triage_v0_1=true",
    f"triage_decision={TRIAGE_DECISION}",
    f"triage_status={TRIAGE_STATUS}",
    "closure_target_count=35",
    "triaged_target_count=35",
    "attach_existing_evidence_count=0",
    "claim_boundary_exemption_count=35",
    "slice_closed_gap_count=1",
    "gaps_closed_count=3",
    "remaining_gap_count=1",
    "product_quality_missing_inputs_gap_closed=true",
    CLOSED_GAP_ID,
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
    "action_id: link-adoption-candidates-to-evidence-gates",
    "owner_approval_required_before_execution: false",
    "Create repo-local adoption evidence gate links for build-vs-buy, license, security, supply-chain, and owner approval gates",
    "Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Primary-Source Product-Quality Missing Inputs Triage v0.1 validation")
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


def require_previous_plan() -> None:
    for label, record in [
        ("missing-input plan", read_json(MISSING_INPUTS_PLAN)),
        ("missing-input gate", read_json(MISSING_INPUTS_GATE)),
    ]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            fail(f"{label} goal_id mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            fail(f"{label} must point to this triage goal")
        if record.get("closure_target_count") != EXPECTED_COUNTS["closure_target_count"]:
            fail(f"{label} closure target count mismatch")
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        MISSING_INPUTS_NEXT_ACTION,
        [
            "action_id: triage-product-quality-primary-source-missing-inputs",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )


def require_triage_record(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "triage_decision": TRIAGE_DECISION,
        "triage_status": TRIAGE_STATUS,
        "closed_gap_id": CLOSED_GAP_ID,
        "product_quality_missing_inputs_gap_closed": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    triage_targets = record.get("triage_targets")
    if not isinstance(triage_targets, list) or len(triage_targets) != EXPECTED_COUNTS["triaged_target_count"]:
        fail(f"{label} triage target count mismatch")
    for target in triage_targets:
        if target.get("triage_lane") != "claim_boundary_exemption":
            fail(f"{label} target lane must be claim_boundary_exemption")
        if target.get("source_attachment_performed") is not False:
            fail(f"{label} source attachment must not be performed")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate() -> None:
    gate = read_json(TRIAGE_GATE)
    if gate.get("gate_id") != "avf-primary-source-product-quality-missing-inputs-triage-gate-v0-1":
        fail("triage gate id mismatch")
    if gate.get("status") != "PASS":
        fail("triage gate status must be PASS")
    require_triage_record(gate, "triage gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_product_quality_missing_inputs_triage_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_triage_record(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_plan()
    require_triage_record(read_json(TRIAGE), "triage")
    require_gate()
    require_text_markers(TRIAGE_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Product-Quality Missing Inputs Triage v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_product_quality_missing_inputs_triage_v0_1=true")
    print(f"triage_decision={TRIAGE_DECISION}")
    print(f"triage_status={TRIAGE_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("product_quality_missing_inputs_gap_closed=true")
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
