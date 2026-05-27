from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1.py"
HARDENING_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_gate.json"
HARDENING_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_next_action.yml"
MUTATION_PACK_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_gate.json"
MUTATION_PACK_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_report.md"
MUTATION_PACK_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_PACK_V0_1_REPORT.md"

MUTATION_FIXTURE_URIS = [
    CAPABILITIES / "capability_candidate_primary_source_priority_1_mutation_required_field_removal.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_mutation_type_mismatch.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_mutation_enum_boundary.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_mutation_additional_property.fixture.json",
    CAPABILITIES / "capability_candidate_primary_source_priority_1_mutation_malformed_fixture_record.fixture.json",
]

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
MUTATION_PACK_DECISION = "CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_PACK"
MUTATION_PACK_STATUS = "adapter_contract_validation_harness_fixture_mutation_pack_created_ready_for_review"

EXPECTED_AREAS = {
    "missing-required-field-coverage": "missing_required",
    "type-mismatch-coverage": "type_mismatch",
    "enum-mismatch-coverage": "enum_mismatch",
    "additional-property-coverage": "additional_properties",
    "malformed-fixture-record-coverage": "malformed_fixture_record",
}

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "hardening_area_count": 5,
    "fixture_mutation_plan_count": 5,
    "mutation_fixture_count": 5,
    "mutation_fixture_expected_invalid_count": 5,
    "mutation_fixture_actual_invalid_count": 5,
    "mutation_fixture_result_matched_expected_count": 5,
    "blocked_action_count": 10,
    "reviewed_blocked_action_count": 10,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_contract_validation_harness_fixture_mutation_pack_review_count": 1,
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
    HARDENING_PLAN_GATE,
    HARDENING_PLAN_NEXT_ACTION,
    MUTATION_PACK_GATE,
    MUTATION_PACK_REPORT,
    MUTATION_PACK_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
    *MUTATION_FIXTURE_URIS,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"mutation_pack_decision={MUTATION_PACK_DECISION}",
    f"mutation_pack_status={MUTATION_PACK_STATUS}",
    "mutation_fixture_count=5",
    "mutation_fixture_expected_invalid_count=5",
    "mutation_fixture_actual_invalid_count=5",
    "mutation_fixture_result_matched_expected_count=5",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-pack",
    "owner_approval_required_before_execution: false",
    "Review repo-local mutation fixtures and their deterministic invalid outcomes",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Pack v0.1 validation")
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


def require_previous_plan() -> dict:
    plan = read_json(HARDENING_PLAN_GATE)
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("adapter contract validation harness hardening plan gate goal_id mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("adapter contract validation harness hardening plan gate must point to this fixture mutation pack goal")
    if plan.get("ready_for_adapter_contract_validation_harness_fixture_mutation_pack_count") != 1:
        fail("adapter contract validation harness hardening plan must be ready for fixture mutation pack")
    if {area.get("area_id") for area in plan.get("hardening_areas", [])} != set(EXPECTED_AREAS):
        fail("adapter contract validation harness hardening plan area ids mismatch")
    require_false_flags(plan.get("claim_boundary", {}), "adapter contract validation harness hardening plan claim boundary")
    require_text_markers(
        HARDENING_PLAN_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-pack",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return plan


def require_mutation_fixture(path: Path) -> dict:
    fixture = read_json(path)
    area_id = fixture.get("area_id")
    if area_id not in EXPECTED_AREAS:
        fail(f"mutation fixture {path.name} area_id mismatch")
    for key in [
        "mutation_fixture_id",
        "mutation_family_id",
        "target_schema_id",
        "target_schema_uri",
        "mutated_instance",
        "expected_valid",
        "expected_failure_reason_prefix",
    ]:
        if key not in fixture:
            fail(f"mutation fixture {path.name} missing {key}")
    if fixture["expected_valid"] is not False:
        fail(f"mutation fixture {path.name} must expect invalid")
    if fixture["expected_failure_reason_prefix"] != EXPECTED_AREAS[area_id]:
        fail(f"mutation fixture {path.name} failure prefix mismatch")
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if fixture.get(key) != value:
            fail(f"mutation fixture {path.name} {key} mismatch")
    schema = read_json(ROOT / fixture["target_schema_uri"])
    actual_valid, failure_reasons = validate_instance(schema, fixture["mutated_instance"])
    if actual_valid is not False:
        fail(f"mutation fixture {path.name} must validate as invalid")
    if not any(reason.startswith(fixture["expected_failure_reason_prefix"]) for reason in failure_reasons):
        fail(f"mutation fixture {path.name} failure reason prefix mismatch: {failure_reasons}")
    return {
        "mutation_fixture_id": fixture["mutation_fixture_id"],
        "area_id": area_id,
        "expected_valid": False,
        "actual_valid": actual_valid,
        "failure_reasons": failure_reasons,
        "validation_result_matched_expected": actual_valid is False,
    }


def require_pack_record(record: dict, label: str, plan: dict, fixture_results: list[dict]) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "mutation_pack_decision": MUTATION_PACK_DECISION,
        "mutation_pack_status": MUTATION_PACK_STATUS,
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
    if input_uris.get("adapter_contract_validation_harness_hardening_plan_gate") != HARDENING_PLAN_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input hardening plan gate uri mismatch")
    expected_uris = [path.relative_to(ROOT).as_posix() for path in MUTATION_FIXTURE_URIS]
    if record.get("mutation_fixture_uris") != expected_uris:
        fail(f"{label} mutation fixture uri mismatch")
    if record.get("reviewed_blocked_actions") != plan.get("reviewed_blocked_actions"):
        fail(f"{label} reviewed blocked actions mismatch")
    if record.get("mutation_fixture_validation_results") != fixture_results:
        fail(f"{label} fixture validation results mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(plan: dict, fixture_results: list[dict]) -> None:
    gate = read_json(MUTATION_PACK_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-pack-gate-v0-1":
        fail("adapter contract validation harness fixture mutation pack gate id mismatch")
    if gate.get("status") != "PASS":
        fail("adapter contract validation harness fixture mutation pack gate status must be PASS")
    require_pack_record(gate, "adapter contract validation harness fixture mutation pack gate", plan, fixture_results)


def require_validation_result(plan: dict, fixture_results: list[dict]) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_pack_record(result, "validation result", plan, fixture_results)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    plan = require_previous_plan()
    fixture_results = [require_mutation_fixture(path) for path in MUTATION_FIXTURE_URIS]
    require_pack_record(read_json(MUTATION_PACK_GATE), "adapter contract validation harness fixture mutation pack", plan, fixture_results)
    require_gate(plan, fixture_results)
    require_text_markers(MUTATION_PACK_REPORT, REPORT_MARKERS)
    require_text_markers(MUTATION_PACK_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(plan, fixture_results)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Pack v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"mutation_pack_decision={MUTATION_PACK_DECISION}")
    print(f"mutation_pack_status={MUTATION_PACK_STATUS}")
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
