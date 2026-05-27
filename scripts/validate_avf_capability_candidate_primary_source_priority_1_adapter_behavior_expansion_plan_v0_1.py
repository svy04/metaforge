from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1.py"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_gate.json"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_next_action.yml"
BEHAVIOR_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan.json"
BEHAVIOR_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_report.md"
BEHAVIOR_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_BEHAVIOR_EXPANSION_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PLAN_DECISION = "CREATE_REPO_LOCAL_ADAPTER_BEHAVIOR_EXPANSION_PLAN_FROM_REVIEWED_REGRESSION_PACK"
PLAN_STATUS = "planned_for_repo_local_adapter_behavior_expansion_review_not_runtime_or_dependency_ready"

EXPECTED_COUNTS = {
    "adapter_module_count": 4,
    "reviewed_regression_test_count": 6,
    "behavior_requirement_count": 6,
    "planned_behavior_task_count": 6,
    "invalid_fixture_behavior_requirement_count": 4,
    "boundary_behavior_requirement_count": 1,
    "evidence_mapping_behavior_requirement_count": 1,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "plan_blocker_count": 0,
    "ready_for_adapter_behavior_expansion_plan_review_count": 1,
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
    REVIEW_GATE,
    REVIEW_NEXT_ACTION,
    BEHAVIOR_PLAN,
    BEHAVIOR_PLAN_REPORT,
    BEHAVIOR_PLAN_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

BEHAVIOR_REQUIREMENT_IDS = [
    "enforce-eval-claim-boundary-required",
    "enforce-redteam-evidence-basis-list",
    "reject-rag-runtime-hints",
    "enforce-governance-risk_tier-enum",
    "preserve-protected-action-boundary-invariants",
    "preserve-evidence-mapping-no-action-drift",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"plan_decision={PLAN_DECISION}",
    f"plan_status={PLAN_STATUS}",
    "reviewed_regression_test_count=6",
    "behavior_requirement_count=6",
    "planned_behavior_task_count=6",
    "invalid_fixture_behavior_requirement_count=4",
    "boundary_behavior_requirement_count=1",
    "evidence_mapping_behavior_requirement_count=1",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "plan_blocker_count=0",
    "ready_for_adapter_behavior_expansion_plan_review_count=1",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-behavior-expansion-plan",
    "owner_approval_required_before_execution: false",
    "Review the repo-local adapter behavior expansion plan before implementing behavior changes",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Plan v0.1 validation")
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


def require_review_gate() -> dict:
    gate = read_json(REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("regression pack review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("regression pack review gate must point to this behavior expansion plan goal")
    if gate.get("ready_for_adapter_behavior_expansion_plan_count") != 1:
        fail("regression pack review gate must be ready for behavior expansion plan")
    for key, value in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "review_blocker_count": 0,
    }.items():
        if gate.get(key) != value:
            fail(f"regression pack review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "regression pack review gate claim boundary")
    require_text_markers(
        REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-behavior-expansion-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_behavior_requirement(item: dict) -> None:
    for key in [
        "requirement_id",
        "source_regression_test_id",
        "regression_type",
        "behavior_goal",
        "planned_file_targets",
        "acceptance_criteria",
        "validation_commands",
        "claim_boundary",
    ]:
        if not item.get(key):
            fail(f"behavior requirement missing {key}")
    if item.get("requirement_id") not in BEHAVIOR_REQUIREMENT_IDS:
        fail(f"unexpected behavior requirement {item.get('requirement_id')}")
    for key in ["candidate_tool_import_allowed", "dependency_install_allowed", "external_fetch_allowed", "runtime_integration_allowed"]:
        if item.get(key) is not False:
            fail(f"behavior requirement {item.get('requirement_id')} must keep {key}=false")
    require_false_flags(item.get("claim_boundary", {}), f"behavior requirement {item.get('requirement_id')} claim boundary")


def require_plan_record(record: dict, label: str, gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "plan_decision": PLAN_DECISION,
        "plan_status": PLAN_STATUS,
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
    if input_uris.get("adapter_regression_pack_review_gate") != REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} review gate input uri mismatch")
    if record.get("reviewed_regression_tests") != gate.get("reviewed_regression_tests"):
        fail(f"{label} reviewed regression tests mismatch")
    requirements = record.get("behavior_requirements", [])
    if len(requirements) != EXPECTED_COUNTS["behavior_requirement_count"]:
        fail(f"{label} behavior requirement count mismatch")
    for item in requirements:
        require_behavior_requirement(item)
    if sorted(item["requirement_id"] for item in requirements) != sorted(BEHAVIOR_REQUIREMENT_IDS):
        fail(f"{label} behavior requirement ids mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_plan_record(result, "validation result", gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    gate = require_review_gate()
    require_plan_record(read_json(BEHAVIOR_PLAN), "behavior expansion plan", gate)
    require_text_markers(BEHAVIOR_PLAN_REPORT, REPORT_MARKERS)
    require_text_markers(BEHAVIOR_PLAN_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Plan v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_status={PLAN_STATUS}")
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
