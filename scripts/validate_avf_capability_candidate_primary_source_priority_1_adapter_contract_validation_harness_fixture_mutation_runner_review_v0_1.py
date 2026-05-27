from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1.py"
MUTATION_RUNNER_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_gate.json"
MUTATION_RUNNER_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_RUNNER_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_RUNNER_REVIEWED"
REVIEW_STATUS = "adapter_contract_validation_harness_fixture_mutation_runner_validated_ready_for_acceptance_gate"

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "mutation_fixture_count": 5,
    "reviewed_mutation_fixture_count": 5,
    "mutation_runner_result_count": 5,
    "reviewed_mutation_runner_result_count": 5,
    "mutation_fixture_expected_invalid_count": 5,
    "mutation_fixture_actual_invalid_count": 5,
    "mutation_fixture_result_matched_expected_count": 5,
    "schema_boundary_mutation_count": 4,
    "malformed_fixture_record_count": 1,
    "blocked_action_count": 10,
    "reviewed_blocked_action_count": 10,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_contract_validation_harness_acceptance_gate_count": 1,
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
    MUTATION_RUNNER_GATE,
    MUTATION_RUNNER_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    REVIEW_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "mutation_runner_result_count=5",
    "reviewed_mutation_runner_result_count=5",
    "mutation_fixture_result_matched_expected_count=5",
    "schema_boundary_mutation_count=4",
    "malformed_fixture_record_count=1",
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
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-acceptance-gate",
    "owner_approval_required_before_execution: false",
    "Create a repo-local acceptance gate that consolidates schema fixtures, mutation runner results, and protected action boundaries",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Runner Review v0.1 validation")
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


def require_previous_runner() -> dict:
    runner = read_json(MUTATION_RUNNER_GATE)
    if runner.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("fixture mutation runner gate goal_id mismatch")
    if runner.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("fixture mutation runner gate must point to this review goal")
    if runner.get("ready_for_adapter_contract_validation_harness_fixture_mutation_runner_review_count") != 1:
        fail("fixture mutation runner must be ready for review")
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "mutation_fixture_result_matched_expected_count": 5,
        "review_blocker_count": 0,
    }.items():
        if runner.get(key) != value:
            fail(f"fixture mutation runner {key} mismatch")
    if len(runner.get("mutation_runner_results", [])) != EXPECTED_COUNTS["mutation_runner_result_count"]:
        fail("fixture mutation runner result count mismatch")
    for item in runner["mutation_runner_results"]:
        if item.get("expected_valid") is not False or item.get("actual_valid") is not False:
            fail(f"mutation runner result {item.get('mutation_fixture_id')} must be invalid")
        if item.get("validation_result_matched_expected") is not True:
            fail(f"mutation runner result {item.get('mutation_fixture_id')} must match expected")
        if item.get("reviewed_result_matched") is not True:
            fail(f"mutation runner result {item.get('mutation_fixture_id')} must match reviewed result")
        if not item.get("failure_reasons"):
            fail(f"mutation runner result {item.get('mutation_fixture_id')} must include failure reasons")
    require_false_flags(runner.get("claim_boundary", {}), "fixture mutation runner claim boundary")
    require_text_markers(
        MUTATION_RUNNER_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-runner",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return runner


def require_reviewed_result(item: dict, source_by_id: dict[str, dict]) -> None:
    result_id = item.get("mutation_fixture_id", "<missing>")
    if result_id not in source_by_id:
        fail(f"reviewed mutation runner result {result_id} missing matching source result")
    source = source_by_id[result_id]
    for key, value in source.items():
        if item.get(key) != value:
            fail(f"reviewed mutation runner result {result_id} changed source field {key}")
    if item.get("review_status") != "reviewed_mutation_runner_result_matches_reviewed_fixture_outcome":
        fail(f"reviewed mutation runner result {result_id} review_status mismatch")
    if item.get("mutation_runner_result_contract_validated") is not True:
        fail(f"reviewed mutation runner result {result_id} contract validation flag mismatch")


def require_review_record(record: dict, label: str, runner: dict) -> None:
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
    if record.get("mutation_fixture_uris") != runner.get("mutation_fixture_uris"):
        fail(f"{label} mutation fixture uri mismatch")
    if record.get("reviewed_blocked_actions") != runner.get("reviewed_blocked_actions"):
        fail(f"{label} reviewed blocked actions mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("adapter_contract_validation_harness_fixture_mutation_runner_gate") != MUTATION_RUNNER_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input mutation runner gate uri mismatch")
    source_by_id = {
        item["mutation_fixture_id"]: item
        for item in runner.get("mutation_runner_results", [])
    }
    reviewed = record.get("reviewed_mutation_runner_results", [])
    if len(reviewed) != EXPECTED_COUNTS["reviewed_mutation_runner_result_count"]:
        fail(f"{label} reviewed mutation runner result count mismatch")
    for item in reviewed:
        require_reviewed_result(item, source_by_id)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(runner: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-runner-review-gate-v0-1":
        fail("fixture mutation runner review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("fixture mutation runner review gate status must be PASS")
    require_review_record(gate, "fixture mutation runner review gate", runner)


def require_validation_result(runner: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", runner)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    runner = require_previous_runner()
    require_review_record(read_json(REVIEW_GATE), "fixture mutation runner review", runner)
    require_gate(runner)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(REVIEW_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(runner)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Runner Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1=true")
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
