from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_scaffold.py"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_local_tests_v0_1.py"
SCAFFOLD_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_review_gate.json"
SCAFFOLD_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_review_next_action.yml"
LOCAL_TEST_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_result.json"
LOCAL_TEST_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_report.md"
LOCAL_TEST_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_LOCAL_TESTS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_local_tests_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_local_tests_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
TEST_DECISION = "CREATE_EXECUTABLE_REPO_LOCAL_ADAPTER_SCAFFOLD_TESTS"
TEST_STATUS = "repo_local_adapter_scaffold_tests_passed_not_runtime_or_dependency_ready"

EXPECTED_COUNTS = {
    "adapter_module_count": 4,
    "local_test_count": 4,
    "local_test_pass_count": 4,
    "local_test_fail_count": 0,
    "normalized_record_count": 4,
    "evidence_entry_count": 4,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "test_blocker_count": 0,
    "ready_for_adapter_local_tests_review_count": 1,
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
    SCAFFOLD_REVIEW_GATE,
    SCAFFOLD_REVIEW_NEXT_ACTION,
    LOCAL_TEST_RESULT,
    LOCAL_TEST_REPORT,
    LOCAL_TEST_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_local_tests_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"test_decision={TEST_DECISION}",
    f"test_status={TEST_STATUS}",
    "adapter_module_count=4",
    "local_test_count=4",
    "local_test_pass_count=4",
    "local_test_fail_count=0",
    "normalized_record_count=4",
    "evidence_entry_count=4",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "test_blocker_count=0",
    "ready_for_adapter_local_tests_review_count=1",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-local-tests",
    "owner_approval_required_before_execution: false",
    "Review executable repo-local adapter tests before broadening the adapter scaffold",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Local Tests v0.1 validation")
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


def require_scaffold_review_gate() -> dict:
    gate = read_json(SCAFFOLD_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("scaffold review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("scaffold review gate must point to this local tests goal")
    if gate.get("ready_for_adapter_local_tests_count") != 1:
        fail("scaffold review gate must be ready for local tests")
    for key, value in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "review_blocker_count": 0,
    }.items():
        if gate.get(key) != value:
            fail(f"scaffold review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "scaffold review gate claim boundary")
    require_text_markers(
        SCAFFOLD_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-local-tests",
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
        fail("local test file execution failed:\n" + result.stdout)
    for marker in ["LOCAL_ADAPTER_SCAFFOLD_TESTS_RESULT=PASS", "LOCAL_ADAPTER_SCAFFOLD_TEST_COUNT=4"]:
        if marker not in result.stdout:
            fail(f"local test file output missing {marker}")


def require_test_record(record: dict, label: str, gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "test_decision": TEST_DECISION,
        "test_status": TEST_STATUS,
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
    if input_uris.get("adapter_scaffold_review_gate") != SCAFFOLD_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} scaffold review gate input uri mismatch")
    if input_uris.get("adapter_scaffold_test_file") != TEST_FILE.relative_to(ROOT).as_posix():
        fail(f"{label} test file input uri mismatch")
    if record.get("adapter_module_uris") != gate.get("adapter_module_uris"):
        fail(f"{label} adapter module uris mismatch")
    if len(record.get("test_results", [])) != EXPECTED_COUNTS["local_test_count"]:
        fail(f"{label} test result count mismatch")
    for item in record.get("test_results", []):
        if item.get("status") != "PASS":
            fail(f"{label} test result {item.get('test_id')} must pass")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_local_tests_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_test_record(result, "validation result", gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    gate = require_scaffold_review_gate()
    require_test_file_executes()
    require_test_record(read_json(LOCAL_TEST_RESULT), "local test result", gate)
    require_text_markers(LOCAL_TEST_REPORT, REPORT_MARKERS)
    require_text_markers(LOCAL_TEST_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Local Tests v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_local_tests_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"test_decision={TEST_DECISION}")
    print(f"test_status={TEST_STATUS}")
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
