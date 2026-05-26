from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_acquisition_plan_v0_1.py"
APPROVAL_GATE = CAPABILITIES / "primary_source_acquisition_approval_packet_gate.json"
ACQUISITION_PLAN = CAPABILITIES / "primary_source_acquisition_plan.yml"
PLAN_GATE = CAPABILITIES / "primary_source_acquisition_plan_gate.json"
CLAIM_MAP = CAPABILITIES / "primary_source_acquisition_claim_map.json"
NEXT_ACTION = CAPABILITIES / "primary_source_acquisition_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_acquisition_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_ACQUISITION_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_acquisition_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_acquisition_approval_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_acquisition_plan_review_v0_1"
APPROVAL_DECISION = "PRIMARY_SOURCE_ACQUISITION_APPROVAL_PACKET_READY"
PLAN_DECISION = "PRIMARY_SOURCE_ACQUISITION_PLAN_READY"

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

ALLOWED_SOURCE_CATEGORIES = [
    "official_docs",
    "original_repository",
    "paper",
    "patent",
    "standard",
    "maintained_implementation",
    "local_repo_evidence",
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
    APPROVAL_GATE,
    ACQUISITION_PLAN,
    PLAN_GATE,
    CLAIM_MAP,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PLAN_MARKERS = [
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"plan_decision: {PLAN_DECISION}",
    "plan_status: drafted_repo_local_not_executed",
    "acquisition_plan_allowed: true",
    "acquisition_execution_allowed: false",
    "external_fetch_performed: false",
    "scraping_performed: false",
    "oss_clone_performed: false",
    "package_install_performed: false",
    "official_docs",
    "original_repository",
    "paper",
    "standard",
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
    "license_review_status: required_not_performed",
    "security_review_status: required_not_performed",
    "evidence_record_status: planned_not_acquired",
    "Do not fetch, scrape, clone, install, or call providers in this plan.",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-primary-source-acquisition-plan",
    "owner_approval_required_before_execution: true",
    "Review planned source targets before any acquisition execution",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_acquisition_plan_v0_1=true",
    "acquisition_plan_created=true",
    "plan_gate_created=true",
    "claim_map_created=true",
    "planned_source_targets=7",
    "claim_mappings=7",
    "acquisition_execution_allowed=false",
    "external_fetch_performed=false",
    "scraping_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "dependency_install_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Primary-Source Acquisition Plan v0.1 validation")
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


def require_approval_gate() -> None:
    gate = read_json(APPROVAL_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("approval gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("approval gate must point to this acquisition plan goal")
    if gate.get("approval_decision") != APPROVAL_DECISION:
        fail("approval gate decision mismatch")
    if gate.get("acquisition_plan_allowed") is not True:
        fail("approval gate must allow planning")
    if gate.get("acquisition_execution_allowed") is not False:
        fail("approval gate must keep execution blocked")
    require_false_flags(gate.get("claim_boundary", {}), "approval gate")


def require_plan_gate() -> None:
    gate = read_json(PLAN_GATE)
    expected = {
        "gate_id": "avf-primary-source-acquisition-plan-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "plan_decision": PLAN_DECISION,
        "plan_status": "drafted_repo_local_not_executed",
        "acquisition_plan_allowed": True,
        "acquisition_execution_allowed": False,
        "planned_source_targets_count": len(SOURCE_TARGET_IDS),
        "claim_mappings_count": len(SOURCE_TARGET_IDS),
        "owner_approval_required_before_execution": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"plan gate {key} mismatch")
    if gate.get("allowed_source_categories") != ALLOWED_SOURCE_CATEGORIES:
        fail("plan gate allowed source categories mismatch")
    if gate.get("planned_source_target_ids") != SOURCE_TARGET_IDS:
        fail("plan gate source target ids mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "plan gate")


def require_claim_map() -> None:
    claim_map = read_json(CLAIM_MAP)
    if claim_map.get("goal_id") != THIS_GOAL_ID:
        fail("claim map goal_id mismatch")
    if claim_map.get("plan_status") != "drafted_repo_local_not_executed":
        fail("claim map plan status mismatch")
    mappings = claim_map.get("claim_mappings")
    if not isinstance(mappings, list) or len(mappings) != len(SOURCE_TARGET_IDS):
        fail("claim map must contain seven mappings")
    ids = [mapping.get("source_target_id") for mapping in mappings]
    if ids != SOURCE_TARGET_IDS:
        fail("claim map source target ids mismatch")
    for mapping in mappings:
        if mapping.get("evidence_record_status") != "planned_not_acquired":
            fail("claim mapping must remain planned_not_acquired")
        if mapping.get("external_fetch_performed") is not False:
            fail("claim mapping external_fetch_performed must be false")
        if mapping.get("source_collection_execution_allowed") is not False:
            fail("claim mapping source collection must remain blocked")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_acquisition_plan_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("plan_decision") != PLAN_DECISION:
        fail("validation result plan decision mismatch")
    if result.get("planned_source_targets") != len(SOURCE_TARGET_IDS):
        fail("validation result planned source count mismatch")
    if result.get("claim_mappings") != len(SOURCE_TARGET_IDS):
        fail("validation result claim mapping count mismatch")
    if result.get("acquisition_execution_allowed") is not False:
        fail("validation result must keep acquisition execution blocked")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_approval_gate()
    require_text_markers(ACQUISITION_PLAN, PLAN_MARKERS)
    require_plan_gate()
    require_claim_map()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Acquisition Plan v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_acquisition_plan_v0_1=true")
    print("acquisition_plan_created=true")
    print("plan_gate_created=true")
    print("claim_map_created=true")
    print("planned_source_targets=7")
    print("claim_mappings=7")
    print("acquisition_execution_allowed=false")
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
