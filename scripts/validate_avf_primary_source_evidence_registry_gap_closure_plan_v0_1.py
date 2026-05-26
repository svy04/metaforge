from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_evidence_registry_gap_closure_plan_v0_1.py"
GAP_REVIEW = CAPABILITIES / "primary_source_evidence_registry_gap_review.json"
GAP_REVIEW_GATE = CAPABILITIES / "primary_source_evidence_registry_gap_review_gate.json"
GAP_REVIEW_NEXT_ACTION = CAPABILITIES / "primary_source_evidence_registry_gap_review_next_action.yml"
CLOSURE_PLAN = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan.json"
CLOSURE_GATE = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_gate.json"
NAMESPACE_MAP_PLAN = CAPABILITIES / "primary_source_namespace_mapping_plan.json"
CLOSURE_BACKLOG = CAPABILITIES / "primary_source_evidence_registry_gap_closure_backlog.yml"
CLOSURE_REPORT = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_EVIDENCE_REGISTRY_GAP_CLOSURE_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_evidence_registry_gap_closure_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_evidence_registry_gap_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_evidence_registry_namespace_map_v0_1"
CLOSURE_DECISION = "PRIMARY_SOURCE_EVIDENCE_REGISTRY_GAP_CLOSURE_PLAN_CREATED_REPO_LOCAL"
CLOSURE_STATUS = "closure_plan_ready_no_gaps_closed_yet"

GAP_IDS = [
    "gap-product-quality-reports-missing-primary-source-inputs",
    "gap-avf-ledger-to-manual-record-namespace-map",
    "gap-content-safety-policy-sources-missing-manual-records",
    "gap-adoption-evidence-gates-not-yet-linked-to-registry",
]

CLOSURE_STEP_IDS = [
    "step-bound-or-attach-product-quality-primary-source-inputs",
    "step-create-avf-ledger-manual-record-namespace-map",
    "step-add-content-safety-policy-manual-source-records",
    "step-link-adoption-candidates-to-evidence-gates",
]

EXPECTED_COUNTS = {
    "gap_count": 4,
    "closure_step_count": 4,
    "reports_missing_primary_source_inputs_count": 35,
    "content_safety_policy_sources_missing_manual_records_count": 2,
    "namespace_mapping_required_count": 7,
    "adoption_gate_requirement_count": 5,
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
    GAP_REVIEW,
    GAP_REVIEW_GATE,
    GAP_REVIEW_NEXT_ACTION,
    CLOSURE_PLAN,
    CLOSURE_GATE,
    NAMESPACE_MAP_PLAN,
    CLOSURE_BACKLOG,
    CLOSURE_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_evidence_registry_gap_closure_plan_v0_1=true",
    f"closure_decision={CLOSURE_DECISION}",
    f"closure_status={CLOSURE_STATUS}",
    "gap_count=4",
    "closure_step_count=4",
    "reports_missing_primary_source_inputs_count=35",
    "content_safety_policy_sources_missing_manual_records_count=2",
    "namespace_mapping_required_count=7",
    "adoption_gate_requirement_count=5",
    "gaps_closed_count=0",
    "step-bound-or-attach-product-quality-primary-source-inputs",
    "step-create-avf-ledger-manual-record-namespace-map",
    "step-add-content-safety-policy-manual-source-records",
    "step-link-adoption-candidates-to-evidence-gates",
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
    "action_id: create-primary-source-namespace-map",
    "owner_approval_required_before_execution: false",
    "Create deterministic repo-local mapping between AVF ledger source ids and manual source record target ids",
    "Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Primary-Source Evidence Registry Gap Closure Plan v0.1 validation")
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


def require_previous_gap_review() -> None:
    review = read_json(GAP_REVIEW)
    gate = read_json(GAP_REVIEW_GATE)
    for label, record in [("gap review", review), ("gap review gate", gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            fail(f"{label} goal_id mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            fail(f"{label} must point to this closure plan goal")
        if record.get("gap_ids") != GAP_IDS:
            fail(f"{label} gap ids mismatch")
        if record.get("gap_count") != EXPECTED_COUNTS["gap_count"]:
            fail(f"{label} gap count mismatch")
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        GAP_REVIEW_NEXT_ACTION,
        [
            "action_id: create-primary-source-evidence-registry-gap-closure-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )


def require_closure_record(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "closure_decision": CLOSURE_DECISION,
        "closure_status": CLOSURE_STATUS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "gaps_closed_count": 0,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("gap_ids") != GAP_IDS:
        fail(f"{label} gap ids mismatch")
    if record.get("closure_step_ids") != CLOSURE_STEP_IDS:
        fail(f"{label} closure step ids mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_namespace_map_plan() -> None:
    plan = read_json(NAMESPACE_MAP_PLAN)
    if plan.get("goal_id") != THIS_GOAL_ID:
        fail("namespace map plan goal_id mismatch")
    if plan.get("namespace_mapping_required_count") != EXPECTED_COUNTS["namespace_mapping_required_count"]:
        fail("namespace map required count mismatch")
    mappings = plan.get("mapping_plan")
    if not isinstance(mappings, list) or len(mappings) != EXPECTED_COUNTS["namespace_mapping_required_count"]:
        fail("namespace map plan must contain seven mapping records")
    for mapping in mappings:
        if mapping.get("mapping_status") != "planned_not_applied":
            fail("namespace mapping status must stay planned_not_applied")
    require_false_flags(plan.get("claim_boundary", {}), "namespace map plan claim boundary")


def require_closure_gate() -> None:
    gate = read_json(CLOSURE_GATE)
    if gate.get("gate_id") != "avf-primary-source-evidence-registry-gap-closure-plan-gate-v0-1":
        fail("closure gate id mismatch")
    if gate.get("status") != "PASS":
        fail("closure gate status must be PASS")
    require_closure_record(gate, "closure gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_evidence_registry_gap_closure_plan_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_closure_record(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_gap_review()
    require_closure_record(read_json(CLOSURE_PLAN), "closure plan")
    require_closure_gate()
    require_namespace_map_plan()
    require_text_markers(CLOSURE_BACKLOG, CLOSURE_STEP_IDS)
    require_text_markers(CLOSURE_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Evidence Registry Gap Closure Plan v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_evidence_registry_gap_closure_plan_v0_1=true")
    print(f"closure_decision={CLOSURE_DECISION}")
    print(f"closure_status={CLOSURE_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("gaps_closed_count=0")
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
