from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_evidence_registry_namespace_map_v0_1.py"
CLOSURE_PLAN = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan.json"
CLOSURE_GATE = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_gate.json"
NAMESPACE_MAP_PLAN = CAPABILITIES / "primary_source_namespace_mapping_plan.json"
CLOSURE_NEXT_ACTION = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_next_action.yml"
NAMESPACE_MAP = CAPABILITIES / "primary_source_namespace_map.json"
NAMESPACE_GATE = CAPABILITIES / "primary_source_namespace_map_gate.json"
NAMESPACE_REPORT = CAPABILITIES / "primary_source_namespace_map_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_namespace_map_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_namespace_map_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_EVIDENCE_REGISTRY_NAMESPACE_MAP_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_evidence_registry_namespace_map_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_evidence_registry_gap_closure_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_content_safety_manual_records_v0_1"
MAP_DECISION = "PRIMARY_SOURCE_NAMESPACE_MAP_CREATED_REPO_LOCAL"
MAP_STATUS = "namespace_gap_closed_repo_local"
CLOSED_GAP_ID = "gap-avf-ledger-to-manual-record-namespace-map"

EXPECTED_COUNTS = {
    "mapping_count": 7,
    "direct_equivalent_count": 4,
    "manual_record_without_avf_ledger_source_count": 2,
    "same_identifier_count": 1,
    "gaps_closed_count": 1,
    "remaining_gap_count": 3,
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
    CLOSURE_PLAN,
    CLOSURE_GATE,
    NAMESPACE_MAP_PLAN,
    CLOSURE_NEXT_ACTION,
    NAMESPACE_MAP,
    NAMESPACE_GATE,
    NAMESPACE_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_evidence_registry_namespace_map_v0_1=true",
    f"map_decision={MAP_DECISION}",
    f"map_status={MAP_STATUS}",
    "mapping_count=7",
    "direct_equivalent_count=4",
    "manual_record_without_avf_ledger_source_count=2",
    "same_identifier_count=1",
    "namespace_gap_closed=true",
    "gaps_closed_count=1",
    "remaining_gap_count=3",
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
    "action_id: create-content-safety-primary-source-manual-records",
    "owner_approval_required_before_execution: false",
    "Create repo-local manual source records for FTC endorsement and AI claims policy sources",
    "Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Primary-Source Evidence Registry Namespace Map v0.1 validation")
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


def require_previous_closure_plan() -> None:
    for label, record in [
        ("closure plan", read_json(CLOSURE_PLAN)),
        ("closure gate", read_json(CLOSURE_GATE)),
    ]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            fail(f"{label} goal_id mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            fail(f"{label} must point to this namespace map goal")
        if record.get("namespace_mapping_required_count") != EXPECTED_COUNTS["mapping_count"]:
            fail(f"{label} namespace mapping required count mismatch")
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        CLOSURE_NEXT_ACTION,
        [
            "action_id: create-primary-source-namespace-map",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    plan = read_json(NAMESPACE_MAP_PLAN)
    mappings = plan.get("mapping_plan")
    if not isinstance(mappings, list) or len(mappings) != EXPECTED_COUNTS["mapping_count"]:
        fail("namespace map plan mapping count mismatch")
    for mapping in mappings:
        if mapping.get("mapping_status") != "planned_not_applied":
            fail("namespace map plan must remain planned_not_applied")


def require_namespace_record(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "map_decision": MAP_DECISION,
        "map_status": MAP_STATUS,
        "closed_gap_id": CLOSED_GAP_ID,
        "namespace_gap_closed": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    mappings = record.get("mappings")
    if not isinstance(mappings, list) or len(mappings) != EXPECTED_COUNTS["mapping_count"]:
        fail(f"{label} mappings count mismatch")
    for mapping in mappings:
        if mapping.get("mapping_status") != "applied_repo_local":
            fail(f"{label} mapping status must be applied_repo_local")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_namespace_gate() -> None:
    gate = read_json(NAMESPACE_GATE)
    if gate.get("gate_id") != "avf-primary-source-namespace-map-gate-v0-1":
        fail("namespace gate id mismatch")
    if gate.get("status") != "PASS":
        fail("namespace gate status must be PASS")
    require_namespace_record(gate, "namespace gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_evidence_registry_namespace_map_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_namespace_record(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_closure_plan()
    require_namespace_record(read_json(NAMESPACE_MAP), "namespace map")
    require_namespace_gate()
    require_text_markers(NAMESPACE_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Evidence Registry Namespace Map v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_evidence_registry_namespace_map_v0_1=true")
    print(f"map_decision={MAP_DECISION}")
    print(f"map_status={MAP_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("namespace_gap_closed=true")
    print(f"closed_gap_id={CLOSED_GAP_ID}")
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
