from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_regression_pack.py"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1.py"
LOCAL_TEST_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_review_gate.json"
LOCAL_TEST_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_review_next_action.yml"
REGRESSION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_result.json"
REGRESSION_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_report.md"
REGRESSION_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_REGRESSION_PACK_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_local_tests_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REGRESSION_DECISION = "CREATE_REPO_LOCAL_ADAPTER_REGRESSION_PACK_FOR_FIXTURE_AND_BOUNDARY_DRIFT"
REGRESSION_STATUS = "repo_local_adapter_regression_pack_passed_not_runtime_or_dependency_ready"

EXPECTED_COUNTS = {
    "adapter_module_count": 4,
    "regression_test_count": 6,
    "regression_test_pass_count": 6,
    "regression_test_fail_count": 0,
    "invalid_fixture_regression_count": 4,
    "boundary_regression_count": 1,
    "evidence_mapping_regression_count": 1,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "regression_blocker_count": 0,
    "ready_for_adapter_regression_pack_review_count": 1,
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
    LOCAL_TEST_REVIEW_GATE,
    LOCAL_TEST_REVIEW_NEXT_ACTION,
    REGRESSION_RESULT,
    REGRESSION_REPORT,
    REGRESSION_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"regression_decision={REGRESSION_DECISION}",
    f"regression_status={REGRESSION_STATUS}",
    "regression_test_count=6",
    "regression_test_pass_count=6",
    "regression_test_fail_count=0",
    "invalid_fixture_regression_count=4",
    "boundary_regression_count=1",
    "evidence_mapping_regression_count=1",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "regression_blocker_count=0",
    "ready_for_adapter_regression_pack_review_count=1",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-regression-pack",
    "owner_approval_required_before_execution: false",
    "Review the repo-local regression pack before expanding adapter behavior",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Regression Pack v0.1 validation")
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


def require_local_tests_review_gate() -> dict:
    gate = read_json(LOCAL_TEST_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("local tests review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("local tests review gate must point to this regression pack goal")
    if gate.get("ready_for_adapter_regression_pack_count") != 1:
        fail("local tests review gate must be ready for regression pack")
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
            fail(f"local tests review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "local tests review gate claim boundary")
    require_text_markers(
        LOCAL_TEST_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-regression-pack",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


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
    for marker in ["LOCAL_ADAPTER_REGRESSION_PACK_RESULT=PASS", "LOCAL_ADAPTER_REGRESSION_TEST_COUNT=6"]:
        if marker not in result.stdout:
            fail(f"regression test file output missing {marker}")


def adapter_module_uris() -> list[str]:
    return [
        "avf/capabilities/adapters/priority_1/adapter_contracts.py",
        "avf/capabilities/adapters/priority_1/record_normalizers.py",
        "avf/capabilities/adapters/priority_1/repo_local_validation_harness.py",
        "avf/capabilities/adapters/priority_1/evidence_mapping.py",
    ]


def require_regression_record(record: dict, label: str, gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "regression_decision": REGRESSION_DECISION,
        "regression_status": REGRESSION_STATUS,
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
    if input_uris.get("adapter_local_tests_review_gate") != LOCAL_TEST_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} local tests review gate input uri mismatch")
    if input_uris.get("adapter_regression_test_file") != TEST_FILE.relative_to(ROOT).as_posix():
        fail(f"{label} regression test file input uri mismatch")
    if record.get("adapter_module_uris") != adapter_module_uris():
        fail(f"{label} adapter module uris mismatch")
    if len(record.get("regression_test_results", [])) != EXPECTED_COUNTS["regression_test_count"]:
        fail(f"{label} regression test result count mismatch")
    for item in record.get("regression_test_results", []):
        if item.get("status") != "PASS":
            fail(f"{label} regression test result {item.get('test_id')} must pass")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_regression_record(result, "validation result", gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    gate = require_local_tests_review_gate()
    require_test_file_executes()
    require_regression_record(read_json(REGRESSION_RESULT), "regression result", gate)
    require_text_markers(REGRESSION_REPORT, REPORT_MARKERS)
    require_text_markers(REGRESSION_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Regression Pack v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"regression_decision={REGRESSION_DECISION}")
    print(f"regression_status={REGRESSION_STATUS}")
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
