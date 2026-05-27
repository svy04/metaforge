from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1.py"
SCHEMA_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_review_gate.json"
SCHEMA_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_review_next_action.yml"

FIXTURE_PACK = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack.json"
FIXTURE_PACK_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_gate.json"
FIXTURE_PACK_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_report.md"
FIXTURE_PACK_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_FIXTURE_PACK_V0_1_REPORT.md"

EVAL_CASE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_eval_case_contract.schema.json"
REDTEAM_CASE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_redteam_case_contract.schema.json"
RAG_METRIC_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_rag_metric_contract.schema.json"
GOVERNANCE_GATE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_governance_gate_contract.schema.json"

FIXTURE_FILES = [
    CAPABILITIES / "capability_candidate_primary_source_priority_1_eval_case_contract.valid.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_eval_case_contract.invalid.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_redteam_case_contract.valid.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_redteam_case_contract.invalid.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_rag_metric_contract.valid.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_rag_metric_contract.invalid.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_governance_gate_contract.valid.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_governance_gate_contract.invalid.fixture.json",
]

SCHEMA_FILES = [
    EVAL_CASE_SCHEMA,
    REDTEAM_CASE_SCHEMA,
    RAG_METRIC_SCHEMA,
    GOVERNANCE_GATE_SCHEMA,
]

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PACK_DECISION = "CREATE_REPO_LOCAL_ADAPTER_CONTRACT_VALIDATION_FIXTURE_PACK"
PACK_STATUS = "adapter_contract_validation_fixture_pack_created_provider_neutral_dependency_free"

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "validation_fixture_count": 8,
    "passing_fixture_count": 4,
    "failing_fixture_count": 4,
    "fixture_validation_result_matched_expected_count": 8,
    "provider_neutral_fixture_count": 8,
    "dependency_free_fixture_count": 8,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_contract_validation_fixture_pack_review_count": 1,
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
    SCHEMA_REVIEW_GATE,
    SCHEMA_REVIEW_NEXT_ACTION,
    *SCHEMA_FILES,
    *FIXTURE_FILES,
    FIXTURE_PACK,
    FIXTURE_PACK_GATE,
    FIXTURE_PACK_REPORT,
    FIXTURE_PACK_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"pack_decision={PACK_DECISION}",
    f"pack_status={PACK_STATUS}",
    "source_schema_artifact_count=4",
    "validation_fixture_count=8",
    "passing_fixture_count=4",
    "failing_fixture_count=4",
    "fixture_validation_result_matched_expected_count=8",
    "provider_neutral_fixture_count=8",
    "dependency_free_fixture_count=8",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "review_blocker_count=0",
    "ready_for_adapter_contract_validation_fixture_pack_review_count=1",
    "provider_neutral=true",
    "dependency_free=true",
    "candidate_tool_import_allowed=false",
    "dependency_install_allowed=false",
    "runtime_integration_allowed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-fixture-pack",
    "owner_approval_required_before_execution: false",
    "Review repo-local adapter contract validation fixtures",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Fixture Pack v0.1 validation")
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


def require_previous_review() -> dict:
    review = read_json(SCHEMA_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("adapter contract schema pack review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("adapter contract schema pack review gate must point to this fixture pack goal")
    if review.get("ready_for_adapter_contract_validation_fixture_pack_count") != 1:
        fail("adapter contract schema pack review must be ready for validation fixture pack")
    if review.get("provider_neutral") is not True:
        fail("adapter contract schema pack review must remain provider-neutral")
    if review.get("dependency_free") is not True:
        fail("adapter contract schema pack review must remain dependency-free")
    if review.get("candidate_tool_import_allowed") is not False:
        fail("adapter contract schema pack review must not allow candidate tool import")
    if review.get("dependency_install_allowed") is not False:
        fail("adapter contract schema pack review must not allow dependency install")
    if review.get("runtime_integration_allowed") is not False:
        fail("adapter contract schema pack review must not allow runtime integration")
    require_false_flags(review.get("claim_boundary", {}), "adapter contract schema pack review claim boundary")
    require_text_markers(
        SCHEMA_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-fixture-pack",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_schema_file(path: Path) -> dict:
    schema = read_json(path)
    schema_label = path.name
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail(f"{schema_label} $schema mismatch")
    if schema.get("type") != "object":
        fail(f"{schema_label} type must be object")
    if schema.get("additionalProperties") is not False:
        fail(f"{schema_label} additionalProperties must be false")
    if not schema.get("required"):
        fail(f"{schema_label} required fields missing")
    if not schema.get("properties"):
        fail(f"{schema_label} properties missing")
    contract = schema.get("x-avf-contract", {})
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if contract.get(key) != value:
            fail(f"{schema_label} {key} mismatch")
    return schema


def validate_instance(schema: dict, instance: dict[str, Any]) -> bool:
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    if any(key not in instance for key in required):
        return False
    if schema.get("additionalProperties") is False:
        if any(key not in properties for key in instance):
            return False
    for key, value in instance.items():
        property_schema = properties.get(key, {})
        expected_type = property_schema.get("type")
        if expected_type == "string" and not isinstance(value, str):
            return False
        if expected_type == "array" and not isinstance(value, list):
            return False
        if "enum" in property_schema and value not in property_schema["enum"]:
            return False
    return True


def require_fixture_record(record: dict, schema_by_uri: dict[str, dict]) -> None:
    fixture_id = record.get("fixture_id", "<missing>")
    schema_uri = record.get("schema_uri")
    fixture_uri = record.get("fixture_uri")
    if schema_uri not in schema_by_uri:
        fail(f"fixture {fixture_id} schema_uri mismatch")
    fixture_path = ROOT / fixture_uri
    if not fixture_path.is_file():
        fail(f"fixture {fixture_id} fixture_uri missing")
    instance = read_json(fixture_path)
    actual_valid = validate_instance(schema_by_uri[schema_uri], instance)
    if actual_valid != record.get("expected_valid"):
        fail(f"fixture {fixture_id} expected_valid mismatch")
    if record.get("validation_result_matched_expected") is not True:
        fail(f"fixture {fixture_id} validation_result_matched_expected must be true")
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if record.get(key) != value:
            fail(f"fixture {fixture_id} {key} mismatch")


def require_pack_record(record: dict, label: str, review: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "pack_decision": PACK_DECISION,
        "pack_status": PACK_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
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
    if input_uris.get("adapter_contract_schema_pack_review_gate") != SCHEMA_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input schema review gate uri mismatch")

    source_schema_artifacts = record.get("source_schema_artifacts", [])
    if source_schema_artifacts != review.get("reviewed_schema_artifacts"):
        fail(f"{label} source schema artifacts mismatch")

    schema_by_uri = {
        artifact["schema_uri"]: read_json(ROOT / artifact["schema_uri"])
        for artifact in source_schema_artifacts
    }
    fixtures = record.get("validation_fixtures", [])
    if len(fixtures) != EXPECTED_COUNTS["validation_fixture_count"]:
        fail(f"{label} validation fixture count mismatch")
    for fixture in fixtures:
        require_fixture_record(fixture, schema_by_uri)

    expected_true = sum(1 for fixture in fixtures if fixture.get("expected_valid") is True)
    expected_false = sum(1 for fixture in fixtures if fixture.get("expected_valid") is False)
    if expected_true != EXPECTED_COUNTS["passing_fixture_count"]:
        fail(f"{label} passing fixture count mismatch")
    if expected_false != EXPECTED_COUNTS["failing_fixture_count"]:
        fail(f"{label} failing fixture count mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(review: dict) -> None:
    gate = read_json(FIXTURE_PACK_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-fixture-pack-gate-v0-1":
        fail("adapter contract validation fixture pack gate id mismatch")
    if gate.get("status") != "PASS":
        fail("adapter contract validation fixture pack gate status must be PASS")
    require_pack_record(gate, "adapter contract validation fixture pack gate", review)


def require_validation_result(review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_pack_record(result, "validation result", review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review = require_previous_review()
    for path in SCHEMA_FILES:
        require_schema_file(path)
    require_pack_record(read_json(FIXTURE_PACK), "adapter contract validation fixture pack", review)
    require_gate(review)
    require_text_markers(FIXTURE_PACK_REPORT, REPORT_MARKERS)
    require_text_markers(FIXTURE_PACK_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Fixture Pack v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"pack_decision={PACK_DECISION}")
    print(f"pack_status={PACK_STATUS}")
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
