from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1.py"
PLAN_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_gate.json"
PLAN_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_next_action.yml"
RUNNER_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_result.json"
RUNNER_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_gate.json"
RUNNER_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_report.md"
RUNNER_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_RUNNER_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
RUNNER_DECISION = "CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_RUNNER"
RUNNER_STATUS = "adapter_contract_validation_harness_runner_created_validated_provider_neutral_no_install"

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "reviewed_validation_fixture_count": 8,
    "harness_responsibility_count": 6,
    "reviewed_harness_responsibility_count": 6,
    "planned_harness_step_count": 6,
    "reviewed_planned_harness_step_count": 6,
    "fixture_validation_result_count": 8,
    "fixture_validation_result_matched_expected_count": 8,
    "passing_fixture_count": 4,
    "failing_fixture_count": 4,
    "blocked_action_count": 10,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_contract_validation_harness_runner_review_count": 1,
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
    RUNNER_RESULT,
    RUNNER_GATE,
    RUNNER_REPORT,
    RUNNER_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"runner_decision={RUNNER_DECISION}",
    f"runner_status={RUNNER_STATUS}",
    "source_schema_artifact_count=4",
    "reviewed_validation_fixture_count=8",
    "harness_responsibility_count=6",
    "reviewed_harness_responsibility_count=6",
    "planned_harness_step_count=6",
    "reviewed_planned_harness_step_count=6",
    "fixture_validation_result_count=8",
    "fixture_validation_result_matched_expected_count=8",
    "passing_fixture_count=4",
    "failing_fixture_count=4",
    "blocked_action_count=10",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "review_blocker_count=0",
    "ready_for_adapter_contract_validation_harness_runner_review_count=1",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-runner",
    "owner_approval_required_before_execution: false",
    "Review the repo-local no-install adapter contract validation harness runner",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Runner v0.1 validation")
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


def require_previous_plan_review() -> dict:
    review = read_json(PLAN_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("adapter contract validation harness plan review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("adapter contract validation harness plan review gate must point to this runner goal")
    if review.get("ready_for_adapter_contract_validation_harness_runner_count") != 1:
        fail("adapter contract validation harness plan review must be ready for runner")
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if review.get(key) != value:
            fail(f"adapter contract validation harness plan review {key} mismatch")
    require_false_flags(review.get("claim_boundary", {}), "adapter contract validation harness plan review claim boundary")
    require_text_markers(
        PLAN_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-runner",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def validate_instance(schema: dict, instance: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    missing = [key for key in required if key not in instance]
    if missing:
        reasons.append("missing_required:" + ",".join(missing))
    if schema.get("additionalProperties") is False:
        extras = [key for key in instance if key not in properties]
        if extras:
            reasons.append("additional_properties:" + ",".join(extras))
    for key, value in instance.items():
        property_schema = properties.get(key, {})
        expected_type = property_schema.get("type")
        if expected_type == "string" and not isinstance(value, str):
            reasons.append(f"type_mismatch:{key}:string")
        if expected_type == "array" and not isinstance(value, list):
            reasons.append(f"type_mismatch:{key}:array")
        if "enum" in property_schema and value not in property_schema["enum"]:
            reasons.append(f"enum_mismatch:{key}")
    return not reasons, reasons


def require_fixture_result(item: dict) -> None:
    fixture_id = item.get("fixture_id", "<missing>")
    schema_uri = item.get("schema_uri")
    fixture_uri = item.get("fixture_uri")
    if not schema_uri or not fixture_uri:
        fail(f"fixture result {fixture_id} missing schema_uri or fixture_uri")
    schema = read_json(ROOT / schema_uri)
    instance = read_json(ROOT / fixture_uri)
    actual_valid, reasons = validate_instance(schema, instance)
    if item.get("actual_valid") != actual_valid:
        fail(f"fixture result {fixture_id} actual_valid mismatch")
    if item.get("failure_reasons") != reasons:
        fail(f"fixture result {fixture_id} failure_reasons mismatch")
    if item.get("validation_result_matched_expected") is not True:
        fail(f"fixture result {fixture_id} must match expected")
    if item.get("expected_valid") is not actual_valid and item.get("expected_valid") is not False:
        fail(f"fixture result {fixture_id} expected_valid invalid")
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if item.get(key) != value:
            fail(f"fixture result {fixture_id} {key} mismatch")


def require_runner_record(record: dict, label: str, review: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "runner_decision": RUNNER_DECISION,
        "runner_status": RUNNER_STATUS,
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
    if input_uris.get("adapter_contract_validation_harness_plan_review_gate") != PLAN_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input harness plan review gate uri mismatch")
    if record.get("reviewed_harness_responsibilities") != review.get("reviewed_harness_responsibilities"):
        fail(f"{label} reviewed harness responsibilities mismatch")
    if record.get("reviewed_planned_harness_steps") != review.get("reviewed_planned_harness_steps"):
        fail(f"{label} reviewed planned harness steps mismatch")
    if record.get("reviewed_blocked_actions") != review.get("reviewed_blocked_actions"):
        fail(f"{label} reviewed blocked actions mismatch")

    fixture_results = record.get("fixture_validation_results", [])
    if len(fixture_results) != EXPECTED_COUNTS["fixture_validation_result_count"]:
        fail(f"{label} fixture validation result count mismatch")
    for item in fixture_results:
        require_fixture_result(item)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(review: dict) -> None:
    gate = read_json(RUNNER_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-runner-gate-v0-1":
        fail("adapter contract validation harness runner gate id mismatch")
    if gate.get("status") != "PASS":
        fail("adapter contract validation harness runner gate status must be PASS")
    require_runner_record(gate, "adapter contract validation harness runner gate", review)


def require_validation_result(review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_runner_record(result, "validation result", review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review = require_previous_plan_review()
    require_runner_record(read_json(RUNNER_RESULT), "adapter contract validation harness runner result", review)
    require_gate(review)
    require_text_markers(RUNNER_REPORT, REPORT_MARKERS)
    require_text_markers(RUNNER_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Runner v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"runner_decision={RUNNER_DECISION}")
    print(f"runner_status={RUNNER_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("provider_neutral=true")
    print("dependency_free=true")
    print("candidate_tool_import_allowed=false")
    print("runtime_integration_allowed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
