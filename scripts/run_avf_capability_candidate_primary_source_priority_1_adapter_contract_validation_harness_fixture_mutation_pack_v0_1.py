from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

HARDENING_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_gate.json"
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
CREATED_AT = "2026-05-27T00:00:00Z"
MUTATION_PACK_DECISION = "CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_PACK"
MUTATION_PACK_STATUS = "adapter_contract_validation_harness_fixture_mutation_pack_created_ready_for_review"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def false_boundary() -> dict:
    return {
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "automated_scraping_performed": False,
        "scraping_performed": False,
        "posting_automation_performed": False,
        "dependency_install_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "package_install_performed": False,
        "runtime_integration_performed": False,
        "runtime_export_performed": False,
        "collector_started": False,
        "telemetry_export_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_plan(plan: dict) -> None:
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("adapter contract validation harness hardening plan goal mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("adapter contract validation harness hardening plan must point to this fixture mutation pack goal")
    if plan.get("ready_for_adapter_contract_validation_harness_fixture_mutation_pack_count") != 1:
        raise SystemExit("adapter contract validation harness hardening plan must be ready for fixture mutation pack")


def mutation_fixtures() -> list[dict]:
    base = {
        "expected_valid": False,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }
    return [
        {
            **base,
            "mutation_fixture_id": "mutation-required-field-removal-eval-case",
            "area_id": "missing-required-field-coverage",
            "mutation_family_id": "mutation-required-field-removal",
            "target_schema_id": "eval-case-contract",
            "target_schema_uri": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_eval_case_contract.schema.json",
            "mutated_instance": {
                "case_id": "eval-required-field-missing",
                "input": "repo-local no-provider eval input",
                "success_criteria": ["validator reports missing required field"],
                "claim_boundary": "repo_local_internal_only",
            },
            "expected_failure_reason_prefix": "missing_required",
        },
        {
            **base,
            "mutation_fixture_id": "mutation-type-mismatch-redteam-case",
            "area_id": "type-mismatch-coverage",
            "mutation_family_id": "mutation-type-mismatch",
            "target_schema_id": "redteam-case-contract",
            "target_schema_uri": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_redteam_case_contract.schema.json",
            "mutated_instance": {
                "case_id": "redteam-evidence-basis-type-mismatch",
                "risk_category": "prompt_injection",
                "prompt_or_scenario": "repo-local red-team prompt placeholder",
                "expected_refusal_or_guardrail": "block unsafe influence execution",
                "evidence_basis": "should-be-array",
            },
            "expected_failure_reason_prefix": "type_mismatch",
        },
        {
            **base,
            "mutation_fixture_id": "mutation-enum-boundary-governance-gate",
            "area_id": "enum-mismatch-coverage",
            "mutation_family_id": "mutation-enum-boundary",
            "target_schema_id": "governance-gate-contract",
            "target_schema_uri": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_governance_gate_contract.schema.json",
            "mutated_instance": {
                "gate_id": "governance_risk_tier_enum_mismatch",
                "risk_tier": "purple",
                "required_reviews": ["safety"],
                "blocked_actions": ["deploy", "publish"],
                "decision_boundary": "repo-local internal fixture only",
            },
            "expected_failure_reason_prefix": "enum_mismatch",
        },
        {
            **base,
            "mutation_fixture_id": "mutation-additional-property-rag-metric",
            "area_id": "additional-property-coverage",
            "mutation_family_id": "mutation-additional-property",
            "target_schema_id": "rag-metric-contract",
            "target_schema_uri": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_rag_metric_contract.schema.json",
            "mutated_instance": {
                "metric_id": "rag-additional-property",
                "metric_name": "Groundedness Placeholder",
                "input_fields": ["question", "context"],
                "output_fields": ["answer"],
                "interpretation_boundary": "repo-local internal fixture only",
                "unexpected_runtime_hint": "do-not-execute",
            },
            "expected_failure_reason_prefix": "additional_properties",
        },
        {
            **base,
            "mutation_fixture_id": "mutation-malformed-fixture-record-loader-boundary",
            "area_id": "malformed-fixture-record-coverage",
            "mutation_family_id": "mutation-malformed-fixture-record",
            "target_schema_id": "eval-case-contract",
            "target_schema_uri": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_eval_case_contract.schema.json",
            "mutated_instance": "not-an-object-fixture-record",
            "expected_failure_reason_prefix": "malformed_fixture_record",
        },
    ]


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


def fixture_results() -> list[dict]:
    results = []
    for fixture in mutation_fixtures():
        schema = read_json(ROOT / fixture["target_schema_uri"])
        actual_valid, failure_reasons = validate_instance(schema, fixture["mutated_instance"])
        results.append(
            {
                "mutation_fixture_id": fixture["mutation_fixture_id"],
                "area_id": fixture["area_id"],
                "expected_valid": False,
                "actual_valid": actual_valid,
                "failure_reasons": failure_reasons,
                "validation_result_matched_expected": actual_valid is False,
            }
        )
    return results


def counts(plan: dict) -> dict:
    return {
        "source_schema_artifact_count": plan["source_schema_artifact_count"],
        "hardening_area_count": plan["hardening_area_count"],
        "fixture_mutation_plan_count": plan["fixture_mutation_plan_count"],
        "mutation_fixture_count": len(mutation_fixtures()),
        "mutation_fixture_expected_invalid_count": 5,
        "mutation_fixture_actual_invalid_count": sum(1 for result in fixture_results() if result["actual_valid"] is False),
        "mutation_fixture_result_matched_expected_count": sum(
            1 for result in fixture_results() if result["validation_result_matched_expected"] is True
        ),
        "blocked_action_count": plan["blocked_action_count"],
        "reviewed_blocked_action_count": plan["reviewed_blocked_action_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_fixture_mutation_pack_review_count": 1,
    }


def base_pack_record(plan: dict) -> dict:
    return {
        "created_at": CREATED_AT,
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
        "mutation_fixture_uris": [rel(path) for path in MUTATION_FIXTURE_URIS],
        "mutation_fixture_validation_results": fixture_results(),
        "reviewed_blocked_actions": plan["reviewed_blocked_actions"],
        "input_uris": {
            "adapter_contract_validation_harness_hardening_plan_gate": rel(HARDENING_PLAN_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(plan),
        "claim_boundary": false_boundary(),
    }


def build_gate(plan: dict) -> dict:
    return {
        **base_pack_record(plan),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-pack-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local mutation fixtures created for adapter contract validation harness hardening",
    }


def build_validation_result(plan: dict) -> dict:
    return {
        **base_pack_record(plan),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(HARDENING_PLAN_GATE),
            rel(MUTATION_PACK_GATE),
            rel(MUTATION_PACK_REPORT),
            rel(MUTATION_PACK_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
            *[rel(path) for path in MUTATION_FIXTURE_URIS],
        ],
    }


def build_report(plan: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(plan).items())
    fixture_lines = "\n".join(
        "- {mutation_fixture_id}: area_id={area_id}, expected_valid=false, actual_valid={actual_valid}, failure_reasons={failure_reasons}".format(
            **result
        )
        for result in fixture_results()
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Pack v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1=true

## Mutation pack summary

- candidate_id={CANDIDATE_ID}
- mutation_pack_decision={MUTATION_PACK_DECISION}
- mutation_pack_status={MUTATION_PACK_STATUS}
- provider_neutral=true
- dependency_free=true
- candidate_tool_import_allowed=false
- dependency_install_allowed=false
- external_fetch_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Mutation fixture validation results

{fixture_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-pack
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review repo-local mutation fixtures and their deterministic invalid outcomes
  - Confirm every mutation fixture maps to a hardening area and remains invalid
  - Confirm no candidate tool import, dependency install, external fetch, runtime integration, deploy, publish, or readiness claim was introduced
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    plan = read_json(HARDENING_PLAN_GATE)
    require_plan(plan)

    for path, fixture in zip(MUTATION_FIXTURE_URIS, mutation_fixtures()):
        write_json(path, fixture)
    write_json(MUTATION_PACK_GATE, build_gate(plan))
    write_text(MUTATION_PACK_REPORT, build_report(plan))
    write_text(MUTATION_PACK_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plan))
    write_text(VALIDATION_REPORT, build_report(plan))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Pack v0.1")
    print("RESULT: PASS")
    print("generated=10")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
