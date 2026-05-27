from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1.py"
MUTATION_PACK_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_gate.json"
MUTATION_PACK_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_next_action.yml"
MUTATION_RUNNER_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_result.json"
MUTATION_RUNNER_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_gate.json"
MUTATION_RUNNER_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_report.md"
MUTATION_RUNNER_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_RUNNER_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
RUNNER_DECISION = "EXECUTE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_RUNNER"
RUNNER_STATUS = "adapter_contract_validation_harness_fixture_mutation_runner_executed_ready_for_review"

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "mutation_fixture_count": 5,
    "reviewed_mutation_fixture_count": 5,
    "mutation_runner_result_count": 5,
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
    "ready_for_adapter_contract_validation_harness_fixture_mutation_runner_review_count": 1,
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
    MUTATION_PACK_REVIEW_GATE,
    MUTATION_PACK_REVIEW_NEXT_ACTION,
    MUTATION_RUNNER_RESULT,
    MUTATION_RUNNER_GATE,
    MUTATION_RUNNER_REPORT,
    MUTATION_RUNNER_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"runner_decision={RUNNER_DECISION}",
    f"runner_status={RUNNER_STATUS}",
    "mutation_runner_result_count=5",
    "mutation_fixture_actual_invalid_count=5",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-runner",
    "owner_approval_required_before_execution: false",
    "Review the repo-local mutation runner results and confirm all reviewed mutation fixtures remain invalid",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Runner v0.1 validation")
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


def validate_instance(schema: dict, instance: Any) -> tuple[bool, list[str]]:
    if not isinstance(instance, dict):
        return False, ["malformed_fixture_record:mutated_instance"]
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


def require_previous_review() -> dict:
    review = read_json(MUTATION_PACK_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("fixture mutation pack review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("fixture mutation pack review gate must point to this mutation runner goal")
    if review.get("ready_for_adapter_contract_validation_harness_fixture_mutation_runner_count") != 1:
        fail("fixture mutation pack review must be ready for mutation runner")
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
        if review.get(key) != value:
            fail(f"fixture mutation pack review {key} mismatch")
    for uri in review.get("mutation_fixture_uris", []):
        if not (ROOT / uri).is_file():
            fail(f"mutation fixture file missing: {uri}")
    require_false_flags(review.get("claim_boundary", {}), "fixture mutation pack review claim boundary")
    require_text_markers(
        MUTATION_PACK_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-runner",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def expected_runner_results(review: dict) -> list[dict]:
    results = []
    reviewed_by_id = {
        item["mutation_fixture_id"]: item
        for item in review.get("reviewed_mutation_fixture_validation_results", [])
    }
    for uri in review.get("mutation_fixture_uris", []):
        fixture = read_json(ROOT / uri)
        schema = read_json(ROOT / fixture["target_schema_uri"])
        actual_valid, failure_reasons = validate_instance(schema, fixture["mutated_instance"])
        reviewed = reviewed_by_id.get(fixture["mutation_fixture_id"])
        if not reviewed:
            fail(f"missing reviewed mutation result for {fixture['mutation_fixture_id']}")
        result = {
            "mutation_fixture_id": fixture["mutation_fixture_id"],
            "area_id": fixture["area_id"],
            "mutation_fixture_uri": uri,
            "target_schema_id": fixture["target_schema_id"],
            "target_schema_uri": fixture["target_schema_uri"],
            "expected_valid": fixture["expected_valid"],
            "actual_valid": actual_valid,
            "failure_reasons": failure_reasons,
            "validation_result_matched_expected": actual_valid == fixture["expected_valid"],
            "reviewed_result_matched": failure_reasons == reviewed.get("failure_reasons"),
            "runner_status": "mutation_fixture_executed_through_repo_local_no_install_harness",
            "provider_neutral": True,
            "dependency_free": True,
            "candidate_tool_import_allowed": False,
            "dependency_install_allowed": False,
            "external_fetch_allowed": False,
            "runtime_integration_allowed": False,
        }
        results.append(result)
    return results


def require_runner_result(result: dict) -> None:
    if result.get("expected_valid") is not False:
        fail(f"mutation runner result {result.get('mutation_fixture_id')} must expect invalid")
    if result.get("actual_valid") is not False:
        fail(f"mutation runner result {result.get('mutation_fixture_id')} must remain invalid")
    if result.get("validation_result_matched_expected") is not True:
        fail(f"mutation runner result {result.get('mutation_fixture_id')} must match expected")
    if result.get("reviewed_result_matched") is not True:
        fail(f"mutation runner result {result.get('mutation_fixture_id')} must match reviewed failure reasons")
    if not result.get("failure_reasons"):
        fail(f"mutation runner result {result.get('mutation_fixture_id')} must include failure reasons")
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if result.get(key) != value:
            fail(f"mutation runner result {result.get('mutation_fixture_id')} {key} mismatch")


def require_runner_record(record: dict, label: str, review: dict, expected_results: list[dict]) -> None:
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
    if record.get("mutation_fixture_uris") != review.get("mutation_fixture_uris"):
        fail(f"{label} mutation fixture uri mismatch")
    if record.get("reviewed_blocked_actions") != review.get("reviewed_blocked_actions"):
        fail(f"{label} reviewed blocked actions mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("adapter_contract_validation_harness_fixture_mutation_pack_review_gate") != MUTATION_PACK_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input mutation pack review gate uri mismatch")
    results = record.get("mutation_runner_results", [])
    if results != expected_results:
        fail(f"{label} mutation runner results mismatch")
    for result in results:
        require_runner_result(result)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(review: dict, expected_results: list[dict]) -> None:
    gate = read_json(MUTATION_RUNNER_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-runner-gate-v0-1":
        fail("fixture mutation runner gate id mismatch")
    if gate.get("status") != "PASS":
        fail("fixture mutation runner gate status must be PASS")
    require_runner_record(gate, "fixture mutation runner gate", review, expected_results)


def require_validation_result(review: dict, expected_results: list[dict]) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_runner_record(result, "validation result", review, expected_results)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review = require_previous_review()
    expected_results = expected_runner_results(review)
    require_runner_record(read_json(MUTATION_RUNNER_RESULT), "fixture mutation runner result", review, expected_results)
    require_gate(review, expected_results)
    require_text_markers(MUTATION_RUNNER_REPORT, REPORT_MARKERS)
    require_text_markers(MUTATION_RUNNER_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review, expected_results)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Runner v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"runner_decision={RUNNER_DECISION}")
    print(f"runner_status={RUNNER_STATUS}")
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
