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

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1.py"
BEHAVIOR_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_result.json"
BEHAVIOR_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_BEHAVIOR_EXPANSION_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_BEHAVIOR_EXPANSION_REVIEWED"
REVIEW_STATUS = "adapter_behavior_expansion_reviewed_ready_for_runtime_integration_preflight"

EXPECTED_COUNTS = {
    "adapter_module_count": 4,
    "behavior_requirement_count": 6,
    "reviewed_behavior_requirement_count": 6,
    "behavior_test_count": 6,
    "behavior_test_pass_count": 6,
    "behavior_test_fail_count": 0,
    "regression_test_count": 6,
    "scaffold_test_count": 4,
    "review_blocker_count": 0,
    "ready_for_adapter_behavior_expansion_review_count": 1,
    "ready_for_runtime_integration_preflight_count": 1,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
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
    BEHAVIOR_RESULT,
    BEHAVIOR_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    REVIEW_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "behavior_requirement_count=6",
    "reviewed_behavior_requirement_count=6",
    "behavior_test_count=6",
    "behavior_test_pass_count=6",
    "behavior_test_fail_count=0",
    "regression_test_count=6",
    "scaffold_test_count=4",
    "review_blocker_count=0",
    "ready_for_runtime_integration_preflight_count=1",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
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
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-runtime-integration-preflight",
    "owner_approval_required_before_execution: false",
    "Create a repo-local runtime integration preflight without integrating runtime systems",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Review v0.1 validation")
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


def require_behavior_result() -> dict:
    source = read_json(BEHAVIOR_RESULT)
    if source.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("behavior expansion result goal_id mismatch")
    if source.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("behavior expansion result must point to this review goal")
    if source.get("ready_for_adapter_behavior_expansion_review_count") != 1:
        fail("behavior expansion result must be ready for review")
    for key, value in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "behavior_blocker_count": 0,
    }.items():
        if source.get(key) != value:
            fail(f"behavior expansion result {key} mismatch")
    require_false_flags(source.get("claim_boundary", {}), "behavior expansion result claim boundary")
    require_text_markers(
        BEHAVIOR_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-adapter-behavior-expansion",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return source


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
    if input_uris.get("adapter_behavior_expansion_result") != BEHAVIOR_RESULT.relative_to(ROOT).as_posix():
        fail(f"{label} behavior result input uri mismatch")
    if record.get("reviewed_behavior_requirements") != source.get("reviewed_behavior_requirements"):
        fail(f"{label} reviewed behavior requirements mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(source: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", source)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    source = require_behavior_result()
    run_test_file(BEHAVIOR_TEST_FILE, "LOCAL_ADAPTER_BEHAVIOR_EXPANSION_RESULT=PASS")
    run_test_file(REGRESSION_TEST_FILE, "LOCAL_ADAPTER_REGRESSION_PACK_RESULT=PASS")
    run_test_file(SCAFFOLD_TEST_FILE, "LOCAL_ADAPTER_SCAFFOLD_TESTS_RESULT=PASS")
    require_review_record(read_json(REVIEW_GATE), "review gate", source)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(REVIEW_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(source)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1=true")
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
