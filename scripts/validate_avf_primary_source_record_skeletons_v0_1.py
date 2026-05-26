from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_record_skeletons_v0_1.py"
PLAN_REVIEW_GATE = CAPABILITIES / "primary_source_acquisition_plan_review_gate.json"
CLAIM_MAP = CAPABILITIES / "primary_source_acquisition_claim_map.json"
SKELETONS = CAPABILITIES / "primary_source_record_skeletons.json"
SKELETONS_MARKDOWN = CAPABILITIES / "primary_source_record_skeletons.md"
SKELETONS_GATE = CAPABILITIES / "primary_source_record_skeletons_gate.json"
NEXT_ACTION = CAPABILITIES / "primary_source_record_skeletons_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_record_skeletons_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_RECORD_SKELETONS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_record_skeletons_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_acquisition_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_record_skeletons_review_v0_1"
PLAN_REVIEW_DECISION = "PRIMARY_SOURCE_ACQUISITION_PLAN_REVIEWED_EXECUTION_BLOCKED"
SKELETON_DECISION = "PRIMARY_SOURCE_RECORD_SKELETONS_CREATED_NOT_ACQUIRED"

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
    PLAN_REVIEW_GATE,
    CLAIM_MAP,
    SKELETONS,
    SKELETONS_MARKDOWN,
    SKELETONS_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

MARKDOWN_MARKERS = [
    f"decision={SKELETON_DECISION}",
    "skeletons_created=7",
    "skeleton_status=planned_not_acquired",
    "source_contents_acquired=false",
    "external_fetch_performed=false",
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
    "source_uri:",
    "license_or_rights_note:",
    "evidence_excerpt_summary:",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-primary-source-record-skeletons",
    "owner_approval_required_before_execution: true",
    "Review blank source record skeletons before any source acquisition",
    "Do not fetch, scrape, clone, install, or call providers",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_record_skeletons_v0_1=true",
    "skeletons_created=7",
    "required_fields_per_skeleton=10",
    "all_skeletons_planned_not_acquired=true",
    "source_contents_acquired=false",
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
    print("AVF Primary-Source Record Skeletons v0.1 validation")
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


def require_plan_review_gate() -> None:
    gate = read_json(PLAN_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("plan review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("plan review gate must point to this skeleton goal")
    if gate.get("review_decision") != PLAN_REVIEW_DECISION:
        fail("plan review gate decision mismatch")
    if gate.get("reviewed_source_target_ids") != SOURCE_TARGET_IDS:
        fail("plan review gate source target ids mismatch")
    if gate.get("all_targets_planned_not_acquired") is not True:
        fail("plan review gate must keep all targets planned_not_acquired")
    if gate.get("execution_remains_blocked") is not True:
        fail("plan review gate must keep execution blocked")
    require_false_flags(gate.get("claim_boundary", {}), "plan review gate")


def require_skeletons() -> None:
    data = read_json(SKELETONS)
    if data.get("goal_id") != THIS_GOAL_ID:
        fail("skeletons goal_id mismatch")
    if data.get("skeleton_decision") != SKELETON_DECISION:
        fail("skeleton decision mismatch")
    skeletons = data.get("source_record_skeletons")
    if not isinstance(skeletons, list) or len(skeletons) != len(SOURCE_TARGET_IDS):
        fail("skeletons must contain seven records")
    ids = [record.get("source_target_id") for record in skeletons]
    if ids != SOURCE_TARGET_IDS:
        fail("skeleton source target ids mismatch")
    for record in skeletons:
        if record.get("skeleton_status") != "planned_not_acquired":
            fail("skeleton status must remain planned_not_acquired")
        if record.get("source_contents_acquired") is not False:
            fail("skeleton source_contents_acquired must be false")
        if record.get("source_collection_execution_allowed") is not False:
            fail("skeleton source collection must remain blocked")
        if record.get("required_fields") != REQUIRED_SOURCE_FIELDS:
            fail("skeleton required fields mismatch")
        for field in REQUIRED_SOURCE_FIELDS:
            if field not in record.get("source_record", {}):
                fail(f"skeleton missing source_record field {field}")
    require_false_flags(data.get("claim_boundary", {}), "skeletons")


def require_skeleton_gate() -> None:
    gate = read_json(SKELETONS_GATE)
    expected = {
        "gate_id": "avf-primary-source-record-skeletons-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "skeleton_decision": SKELETON_DECISION,
        "skeletons_created": len(SOURCE_TARGET_IDS),
        "required_fields_per_skeleton": len(REQUIRED_SOURCE_FIELDS),
        "all_skeletons_planned_not_acquired": True,
        "source_contents_acquired": False,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"skeleton gate {key} mismatch")
    if gate.get("source_target_ids") != SOURCE_TARGET_IDS:
        fail("skeleton gate source target ids mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "skeleton gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_record_skeletons_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("skeleton_decision") != SKELETON_DECISION:
        fail("validation result skeleton decision mismatch")
    if result.get("skeletons_created") != len(SOURCE_TARGET_IDS):
        fail("validation result skeleton count mismatch")
    if result.get("source_contents_acquired") is not False:
        fail("validation result must keep source contents unacquired")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_plan_review_gate()
    require_skeletons()
    require_text_markers(SKELETONS_MARKDOWN, MARKDOWN_MARKERS)
    require_skeleton_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Record Skeletons v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_record_skeletons_v0_1=true")
    print("skeletons_created=7")
    print("required_fields_per_skeleton=10")
    print("all_skeletons_planned_not_acquired=true")
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
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
