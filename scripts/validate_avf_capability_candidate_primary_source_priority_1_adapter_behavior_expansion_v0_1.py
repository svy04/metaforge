from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
BEHAVIOR_TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_behavior_expansion.py"
REGRESSION_TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_regression_pack.py"
SCAFFOLD_TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_scaffold.py"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1.py"
PLAN_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_gate.json"
PLAN_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_next_action.yml"
BEHAVIOR_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_result.json"
BEHAVIOR_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_report.md"
BEHAVIOR_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_BEHAVIOR_EXPANSION_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
IMPLEMENTATION_DECISION = "IMPLEMENT_REPO_LOCAL_ADAPTER_BEHAVIOR_EXPANSION_FROM_REVIEWED_PLAN"
IMPLEMENTATION_STATUS = "repo_local_adapter_behavior_expansion_passed_not_runtime_or_dependency_ready"

EXPECTED_COUNTS = {
    "adapter_module_count": 4,
    "behavior_requirement_count": 6,
    "reviewed_behavior_requirement_count": 6,
    "behavior_test_count": 6,
    "behavior_test_pass_count": 6,
    "behavior_test_fail_count": 0,
    "regression_test_count": 6,
    "scaffold_test_count": 4,
    "invalid_fixture_behavior_requirement_count": 4,
    "boundary_behavior_requirement_count": 1,
    "evidence_mapping_behavior_requirement_count": 1,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "behavior_blocker_count": 0,
    "ready_for_adapter_behavior_expansion_review_count": 1,
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
    PLAN_REVIEW_GATE,
    PLAN_REVIEW_NEXT_ACTION,
    BEHAVIOR_TEST_FILE,
    REGRESSION_TEST_FILE,
    SCAFFOLD_TEST_FILE,
    BEHAVIOR_RESULT,
    BEHAVIOR_REPORT,
    BEHAVIOR_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"implementation_decision={IMPLEMENTATION_DECISION}",
    f"implementation_status={IMPLEMENTATION_STATUS}",
    "behavior_requirement_count=6",
    "reviewed_behavior_requirement_count=6",
    "behavior_test_count=6",
    "behavior_test_pass_count=6",
    "behavior_test_fail_count=0",
    "regression_test_count=6",
    "scaffold_test_count=4",
    "invalid_fixture_behavior_requirement_count=4",
    "boundary_behavior_requirement_count=1",
    "evidence_mapping_behavior_requirement_count=1",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "behavior_blocker_count=0",
    "ready_for_adapter_behavior_expansion_review_count=1",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-behavior-expansion",
    "owner_approval_required_before_execution: false",
    "Review the repo-local adapter behavior expansion before any runtime or dependency step",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion v0.1 validation")
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


def run_test_file(path: Path, marker: str) -> None:
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        fail(f"{path.relative_to(ROOT)} execution failed:\n" + result.stdout)
    if marker not in result.stdout:
        fail(f"{path.relative_to(ROOT)} output missing {marker}")


def require_plan_review_gate() -> dict:
    gate = read_json(PLAN_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("behavior expansion plan review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("behavior expansion plan review gate must point to this behavior expansion goal")
    if gate.get("ready_for_adapter_behavior_expansion_count") != 1:
        fail("behavior expansion plan review gate must be ready for behavior expansion")
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
            fail(f"behavior expansion plan review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "behavior expansion plan review gate claim boundary")
    require_text_markers(
        PLAN_REVIEW_NEXT_ACTION,
        [
            "action_id: implement-capability-candidate-primary-source-priority-1-adapter-behavior-expansion",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_behavior_result(record: dict, label: str, source: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "implementation_decision": IMPLEMENTATION_DECISION,
        "implementation_status": IMPLEMENTATION_STATUS,
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
    if input_uris.get("adapter_behavior_expansion_plan_review_gate") != PLAN_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} behavior expansion plan review gate input uri mismatch")
    if record.get("reviewed_behavior_requirements") != source.get("reviewed_behavior_requirements"):
        fail(f"{label} reviewed behavior requirements mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(source: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_behavior_result(result, "validation result", source)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    source = require_plan_review_gate()
    run_test_file(BEHAVIOR_TEST_FILE, "LOCAL_ADAPTER_BEHAVIOR_EXPANSION_RESULT=PASS")
    run_test_file(REGRESSION_TEST_FILE, "LOCAL_ADAPTER_REGRESSION_PACK_RESULT=PASS")
    run_test_file(SCAFFOLD_TEST_FILE, "LOCAL_ADAPTER_SCAFFOLD_TESTS_RESULT=PASS")
    require_behavior_result(read_json(BEHAVIOR_RESULT), "behavior expansion result", source)
    require_text_markers(BEHAVIOR_REPORT, REPORT_MARKERS)
    require_text_markers(BEHAVIOR_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(source)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"implementation_decision={IMPLEMENTATION_DECISION}")
    print(f"implementation_status={IMPLEMENTATION_STATUS}")
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
