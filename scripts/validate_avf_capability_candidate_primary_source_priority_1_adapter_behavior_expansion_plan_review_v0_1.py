from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1.py"
BEHAVIOR_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan.json"
BEHAVIOR_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_BEHAVIOR_EXPANSION_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_BEHAVIOR_EXPANSION_PLAN_REVIEWED"
REVIEW_STATUS = "adapter_behavior_expansion_plan_reviewed_ready_for_behavior_expansion"

EXPECTED_COUNTS = {
    "adapter_module_count": 4,
    "reviewed_regression_test_count": 6,
    "behavior_requirement_count": 6,
    "reviewed_behavior_requirement_count": 6,
    "planned_behavior_task_count": 6,
    "invalid_fixture_behavior_requirement_count": 4,
    "boundary_behavior_requirement_count": 1,
    "evidence_mapping_behavior_requirement_count": 1,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "plan_blocker_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_behavior_expansion_plan_review_count": 1,
    "ready_for_adapter_behavior_expansion_count": 1,
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
    BEHAVIOR_PLAN,
    BEHAVIOR_PLAN_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    REVIEW_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "reviewed_regression_test_count=6",
    "behavior_requirement_count=6",
    "reviewed_behavior_requirement_count=6",
    "planned_behavior_task_count=6",
    "invalid_fixture_behavior_requirement_count=4",
    "boundary_behavior_requirement_count=1",
    "evidence_mapping_behavior_requirement_count=1",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "plan_blocker_count=0",
    "review_blocker_count=0",
    "ready_for_adapter_behavior_expansion_count=1",
    "provider_neutral=true",
    "dependency_free=true",
    "candidate_tool_import_allowed=false",
    "dependency_install_allowed=false",
    "external_fetch_allowed=false",
    "runtime_integration_allowed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: implement-capability-candidate-primary-source-priority-1-adapter-behavior-expansion",
    "owner_approval_required_before_execution: false",
    "Implement repo-local adapter behavior expansion from the reviewed behavior plan",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Plan Review v0.1 validation")
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


def require_behavior_plan() -> dict:
    plan = read_json(BEHAVIOR_PLAN)
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("behavior expansion plan goal_id mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("behavior expansion plan must point to this review goal")
    if plan.get("ready_for_adapter_behavior_expansion_plan_review_count") != 1:
        fail("behavior expansion plan must be ready for review")
    for key, value in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "plan_blocker_count": 0,
    }.items():
        if plan.get(key) != value:
            fail(f"behavior expansion plan {key} mismatch")
    require_false_flags(plan.get("claim_boundary", {}), "behavior expansion plan claim boundary")
    require_text_markers(
        BEHAVIOR_PLAN_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-adapter-behavior-expansion-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return plan


def require_reviewed_requirement(item: dict) -> None:
    for key in ["requirement_id", "source_regression_test_id", "review_status"]:
        if not item.get(key):
            fail(f"reviewed requirement missing {key}")
    if item.get("review_status") != "reviewed_behavior_requirement_preserves_repo_local_boundary":
        fail(f"reviewed requirement {item.get('requirement_id')} status mismatch")
    for key in ["candidate_tool_import_allowed", "dependency_install_allowed", "external_fetch_allowed", "runtime_integration_allowed"]:
        if item.get(key) is not False:
            fail(f"reviewed requirement {item.get('requirement_id')} must keep {key}=false")


def require_review_record(record: dict, label: str, source: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("adapter_behavior_expansion_plan") != BEHAVIOR_PLAN.relative_to(ROOT).as_posix():
        fail(f"{label} behavior plan input uri mismatch")
    if record.get("behavior_requirements") != source.get("behavior_requirements"):
        fail(f"{label} behavior requirements mismatch")
    reviewed = record.get("reviewed_behavior_requirements", [])
    if len(reviewed) != EXPECTED_COUNTS["reviewed_behavior_requirement_count"]:
        fail(f"{label} reviewed behavior requirement count mismatch")
    for item in reviewed:
        require_reviewed_requirement(item)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(source: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", source)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    source = require_behavior_plan()
    require_review_record(read_json(REVIEW_GATE), "review gate", source)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(REVIEW_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(source)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Plan Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("provider_neutral=true")
    print("dependency_free=true")
    print("candidate_tool_import_allowed=false")
    print("dependency_install_allowed=false")
    print("external_fetch_allowed=false")
    print("runtime_integration_allowed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
