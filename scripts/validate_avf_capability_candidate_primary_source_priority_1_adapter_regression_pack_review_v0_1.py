from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_regression_pack.py"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1.py"
REGRESSION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_result.json"
REGRESSION_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_REGRESSION_PACK_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_REGRESSION_PACK_REVIEWED"
REVIEW_STATUS = "adapter_regression_pack_reviewed_ready_for_behavior_expansion_plan"

EXPECTED_COUNTS = {
    "adapter_module_count": 4,
    "regression_test_count": 6,
    "regression_test_pass_count": 6,
    "regression_test_fail_count": 0,
    "reviewed_regression_test_count": 6,
    "invalid_fixture_regression_count": 4,
    "boundary_regression_count": 1,
    "evidence_mapping_regression_count": 1,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "regression_blocker_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_regression_pack_review_count": 1,
    "ready_for_adapter_behavior_expansion_plan_count": 1,
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
    TEST_FILE,
    REGRESSION_RESULT,
    REGRESSION_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    REVIEW_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "regression_test_count=6",
    "regression_test_pass_count=6",
    "regression_test_fail_count=0",
    "reviewed_regression_test_count=6",
    "invalid_fixture_regression_count=4",
    "boundary_regression_count=1",
    "evidence_mapping_regression_count=1",
    "review_blocker_count=0",
    "ready_for_adapter_behavior_expansion_plan_count=1",
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
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-behavior-expansion-plan",
    "owner_approval_required_before_execution: false",
    "Create a repo-local adapter behavior expansion plan after regression review",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Regression Pack Review v0.1 validation")
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


def require_regression_result() -> dict:
    result = read_json(REGRESSION_RESULT)
    if result.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("regression result goal_id mismatch")
    if result.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("regression result must point to this review goal")
    if result.get("ready_for_adapter_regression_pack_review_count") != 1:
        fail("regression result must be ready for review")
    for key, value in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "regression_test_count": 6,
        "regression_test_pass_count": 6,
        "regression_test_fail_count": 0,
        "regression_blocker_count": 0,
    }.items():
        if result.get(key) != value:
            fail(f"regression result {key} mismatch")
    require_false_flags(result.get("claim_boundary", {}), "regression result claim boundary")
    require_text_markers(
        REGRESSION_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-adapter-regression-pack",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return result


def require_test_file_executes() -> None:
    result = subprocess.run(
        [sys.executable, str(TEST_FILE)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        fail("regression test file execution failed:\n" + result.stdout)
    if "LOCAL_ADAPTER_REGRESSION_PACK_RESULT=PASS" not in result.stdout:
        fail("regression test file output missing pass marker")


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
    if input_uris.get("adapter_regression_pack_result") != REGRESSION_RESULT.relative_to(ROOT).as_posix():
        fail(f"{label} regression result input uri mismatch")
    if record.get("regression_test_results") != source.get("regression_test_results"):
        fail(f"{label} regression test results mismatch")
    reviewed = record.get("reviewed_regression_tests", [])
    if len(reviewed) != EXPECTED_COUNTS["reviewed_regression_test_count"]:
        fail(f"{label} reviewed regression test count mismatch")
    for item in reviewed:
        if item.get("review_status") != "reviewed_regression_test_preserves_repo_local_boundary":
            fail(f"{label} reviewed regression test status mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(source: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", source)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    source = require_regression_result()
    require_test_file_executes()
    require_review_record(read_json(REVIEW_GATE), "review gate", source)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(REVIEW_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(source)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Regression Pack Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1=true")
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
