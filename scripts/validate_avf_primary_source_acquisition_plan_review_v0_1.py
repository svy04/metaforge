from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_acquisition_plan_review_v0_1.py"
PLAN_GATE = CAPABILITIES / "primary_source_acquisition_plan_gate.json"
CLAIM_MAP = CAPABILITIES / "primary_source_acquisition_claim_map.json"
REVIEW_GATE = CAPABILITIES / "primary_source_acquisition_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "primary_source_acquisition_plan_review_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_acquisition_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_acquisition_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_ACQUISITION_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_acquisition_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_acquisition_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_record_skeletons_v0_1"
PLAN_DECISION = "PRIMARY_SOURCE_ACQUISITION_PLAN_READY"
REVIEW_DECISION = "PRIMARY_SOURCE_ACQUISITION_PLAN_REVIEWED_EXECUTION_BLOCKED"

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

SOURCE_TARGET_IDS = [
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
]

REQUIRED_FILES = [
    RUNNER,
    PLAN_GATE,
    CLAIM_MAP,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REVIEW_REPORT_MARKERS = [
    f"review_decision={REVIEW_DECISION}",
    "plan_reviewed=true",
    "planned_source_targets=7",
    "claim_mappings=7",
    "all_targets_mapped=true",
    "all_targets_planned_not_acquired=true",
    "execution_remains_blocked=true",
    "external_fetch_performed=false",
    "scraping_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-primary-source-record-skeletons",
    "owner_approval_required_before_execution: true",
    "Create blank evidence record skeletons for each planned source target",
    "Do not fetch, scrape, clone, install, or call providers",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_acquisition_plan_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    "plan_reviewed=true",
    "planned_source_targets=7",
    "claim_mappings=7",
    "all_targets_mapped=true",
    "all_targets_planned_not_acquired=true",
    "execution_remains_blocked=true",
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
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Primary-Source Acquisition Plan Review v0.1 validation")
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


def require_plan_gate() -> None:
    gate = read_json(PLAN_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("plan gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("plan gate must point to this review goal")
    if gate.get("plan_decision") != PLAN_DECISION:
        fail("plan gate decision mismatch")
    if gate.get("planned_source_target_ids") != SOURCE_TARGET_IDS:
        fail("plan gate source target ids mismatch")
    if gate.get("planned_source_targets_count") != len(SOURCE_TARGET_IDS):
        fail("plan gate planned target count mismatch")
    if gate.get("claim_mappings_count") != len(SOURCE_TARGET_IDS):
        fail("plan gate claim mapping count mismatch")
    if gate.get("acquisition_execution_allowed") is not False:
        fail("plan gate must keep acquisition execution blocked")
    require_false_flags(gate.get("claim_boundary", {}), "plan gate")


def require_claim_map() -> None:
    claim_map = read_json(CLAIM_MAP)
    if claim_map.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("claim map goal_id mismatch")
    mappings = claim_map.get("claim_mappings")
    if not isinstance(mappings, list) or len(mappings) != len(SOURCE_TARGET_IDS):
        fail("claim map must contain seven mappings")
    ids = [mapping.get("source_target_id") for mapping in mappings]
    if ids != SOURCE_TARGET_IDS:
        fail("claim map source ids mismatch")
    for mapping in mappings:
        if mapping.get("evidence_record_status") != "planned_not_acquired":
            fail("all mappings must remain planned_not_acquired")
        if mapping.get("external_fetch_performed") is not False:
            fail("claim mapping external_fetch_performed must be false")
        if mapping.get("source_collection_execution_allowed") is not False:
            fail("claim mapping source collection must remain blocked")
    require_false_flags(claim_map.get("claim_boundary", {}), "claim map")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    expected = {
        "gate_id": "avf-primary-source-acquisition-plan-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "plan_reviewed": True,
        "planned_source_targets": len(SOURCE_TARGET_IDS),
        "claim_mappings": len(SOURCE_TARGET_IDS),
        "all_targets_mapped": True,
        "all_targets_planned_not_acquired": True,
        "execution_remains_blocked": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"review gate {key} mismatch")
    if gate.get("reviewed_source_target_ids") != SOURCE_TARGET_IDS:
        fail("review gate reviewed source target ids mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_acquisition_plan_review_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
    if result.get("execution_remains_blocked") is not True:
        fail("validation result must keep execution blocked")
    if result.get("planned_source_targets") != len(SOURCE_TARGET_IDS):
        fail("validation result planned source count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_plan_gate()
    require_claim_map()
    require_review_gate()
    require_text_markers(REVIEW_REPORT, REVIEW_REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Acquisition Plan Review v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_acquisition_plan_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print("plan_reviewed=true")
    print("planned_source_targets=7")
    print("claim_mappings=7")
    print("all_targets_mapped=true")
    print("all_targets_planned_not_acquired=true")
    print("execution_remains_blocked=true")
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
