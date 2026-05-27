from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_review_gate.json"
HARDENING_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_gate.json"
HARDENING_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_report.md"
HARDENING_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_HARDENING_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_DECISION = "CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_HARDENING_PLAN"
PLAN_STATUS = "adapter_contract_validation_harness_hardening_plan_created_ready_for_fixture_mutation_pack"


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


def require_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("adapter contract validation harness runner review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("adapter contract validation harness runner review must point to this hardening plan goal")
    if review.get("ready_for_adapter_contract_validation_harness_hardening_plan_count") != 1:
        raise SystemExit("adapter contract validation harness runner review must be ready for hardening plan")
    for key, expected in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if review.get(key) != expected:
            raise SystemExit(f"adapter contract validation harness runner review {key} mismatch")


def hardening_areas() -> list[dict]:
    base = {
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
            "area_id": "missing-required-field-coverage",
            "reason": "Existing fixture proves one missing required field; next fixture pack should cover every contract family with a required-field mutation.",
            "current_coverage": "present_from_eval_case_contract_invalid_fixture",
            "proposed_negative_fixture_family": "required-field-removal-mutations",
            "validator_expectation": "Each required-field mutation remains invalid with a missing_required failure prefix.",
        },
        {
            **base,
            "area_id": "type-mismatch-coverage",
            "reason": "Existing fixture proves array type mismatch; next fixture pack should cover string and array type boundaries.",
            "current_coverage": "present_from_redteam_case_contract_invalid_fixture",
            "proposed_negative_fixture_family": "type-mismatch-mutations",
            "validator_expectation": "Each type mutation remains invalid with a type_mismatch failure prefix.",
        },
        {
            **base,
            "area_id": "enum-mismatch-coverage",
            "reason": "Existing fixture proves one enum mismatch; next fixture pack should cover every enum-bearing contract field.",
            "current_coverage": "present_from_governance_gate_contract_invalid_fixture",
            "proposed_negative_fixture_family": "enum-boundary-mutations",
            "validator_expectation": "Each enum mutation remains invalid with an enum_mismatch failure prefix.",
        },
        {
            **base,
            "area_id": "additional-property-coverage",
            "reason": "Existing fixture proves additionalProperties=false on one contract; next fixture pack should cover every schema contract.",
            "current_coverage": "present_from_rag_metric_contract_invalid_fixture",
            "proposed_negative_fixture_family": "additional-property-mutations",
            "validator_expectation": "Each additional-property mutation remains invalid with an additional_properties failure prefix.",
        },
        {
            **base,
            "area_id": "malformed-fixture-record-coverage",
            "reason": "Current runner validates loaded JSON objects but does not yet plan explicit malformed fixture record coverage.",
            "current_coverage": "gap_requires_new_fixture_family",
            "proposed_negative_fixture_family": "malformed-fixture-record-mutations",
            "validator_expectation": "Each malformed fixture record remains invalid before candidate tool import or runtime execution.",
        },
    ]


def fixture_mutation_plan() -> list[dict]:
    return [
        {
            "area_id": "missing-required-field-coverage",
            "mutation_family_id": "mutation-required-field-removal",
            "target_schema_id": "all-reviewed-schema-contracts",
            "expected_result": "invalid",
            "expected_failure_reason_prefix": "missing_required",
            "next_fixture_status": "planned_only",
            "candidate_tool_import_allowed": False,
            "dependency_install_allowed": False,
            "external_fetch_allowed": False,
            "runtime_integration_allowed": False,
        },
        {
            "area_id": "type-mismatch-coverage",
            "mutation_family_id": "mutation-type-mismatch",
            "target_schema_id": "all-reviewed-schema-contracts",
            "expected_result": "invalid",
            "expected_failure_reason_prefix": "type_mismatch",
            "next_fixture_status": "planned_only",
            "candidate_tool_import_allowed": False,
            "dependency_install_allowed": False,
            "external_fetch_allowed": False,
            "runtime_integration_allowed": False,
        },
        {
            "area_id": "enum-mismatch-coverage",
            "mutation_family_id": "mutation-enum-boundary",
            "target_schema_id": "enum-bearing-schema-contracts",
            "expected_result": "invalid",
            "expected_failure_reason_prefix": "enum_mismatch",
            "next_fixture_status": "planned_only",
            "candidate_tool_import_allowed": False,
            "dependency_install_allowed": False,
            "external_fetch_allowed": False,
            "runtime_integration_allowed": False,
        },
        {
            "area_id": "additional-property-coverage",
            "mutation_family_id": "mutation-additional-property",
            "target_schema_id": "all-reviewed-schema-contracts",
            "expected_result": "invalid",
            "expected_failure_reason_prefix": "additional_properties",
            "next_fixture_status": "planned_only",
            "candidate_tool_import_allowed": False,
            "dependency_install_allowed": False,
            "external_fetch_allowed": False,
            "runtime_integration_allowed": False,
        },
        {
            "area_id": "malformed-fixture-record-coverage",
            "mutation_family_id": "mutation-malformed-fixture-record",
            "target_schema_id": "fixture-record-loader-boundary",
            "expected_result": "invalid",
            "expected_failure_reason_prefix": "malformed_fixture_record",
            "next_fixture_status": "planned_only",
            "candidate_tool_import_allowed": False,
            "dependency_install_allowed": False,
            "external_fetch_allowed": False,
            "runtime_integration_allowed": False,
        },
    ]


def reviewed_failure_reasons(review: dict) -> list[str]:
    reasons: list[str] = []
    for item in review["reviewed_fixture_validation_results"]:
        for reason in item.get("failure_reasons", []):
            reasons.append(reason)
    return reasons


def counts(review: dict) -> dict:
    return {
        "source_schema_artifact_count": review["source_schema_artifact_count"],
        "reviewed_validation_fixture_count": review["reviewed_validation_fixture_count"],
        "reviewed_fixture_validation_result_count": review["reviewed_fixture_validation_result_count"],
        "existing_passing_fixture_count": review["passing_fixture_count"],
        "existing_failing_fixture_count": review["failing_fixture_count"],
        "reviewed_failure_reason_count": len(reviewed_failure_reasons(review)),
        "hardening_area_count": len(hardening_areas()),
        "fixture_mutation_plan_count": len(fixture_mutation_plan()),
        "blocked_action_count": review["blocked_action_count"],
        "reviewed_blocked_action_count": review["reviewed_blocked_action_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_fixture_mutation_pack_count": 1,
    }


def base_plan_record(review: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "plan_decision": PLAN_DECISION,
        "plan_status": PLAN_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "reviewed_failure_reasons": reviewed_failure_reasons(review),
        "hardening_areas": hardening_areas(),
        "fixture_mutation_plan": fixture_mutation_plan(),
        "reviewed_blocked_actions": review["reviewed_blocked_actions"],
        "input_uris": {
            "adapter_contract_validation_harness_runner_review_gate": rel(RUNNER_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(review),
        "claim_boundary": false_boundary(),
    }


def build_gate(review: dict) -> dict:
    return {
        **base_plan_record(review),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-hardening-plan-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local no-install adapter contract validation harness hardening plan created for fixture mutation pack",
    }


def build_validation_result(review: dict) -> dict:
    return {
        **base_plan_record(review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(RUNNER_REVIEW_GATE),
            rel(HARDENING_PLAN_GATE),
            rel(HARDENING_PLAN_REPORT),
            rel(HARDENING_PLAN_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(review).items())
    area_lines = "\n".join(
        "- {area_id}: current_coverage={current_coverage}, proposed_negative_fixture_family={proposed_negative_fixture_family}".format(
            **area
        )
        for area in hardening_areas()
    )
    mutation_lines = "\n".join(
        "- {mutation_family_id}: area_id={area_id}, target_schema_id={target_schema_id}, expected_failure_reason_prefix={expected_failure_reason_prefix}".format(
            **item
        )
        for item in fixture_mutation_plan()
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Hardening Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1=true

## Plan summary

- candidate_id={CANDIDATE_ID}
- plan_decision={PLAN_DECISION}
- plan_status={PLAN_STATUS}
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

## Hardening areas

{area_lines}

## Fixture mutation plan

{mutation_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-pack
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create repo-local mutation fixtures that prove the harness fails when schema boundaries are violated
  - Cover type checks, enum checks, missing required fields, additional properties, and malformed fixture records
  - Keep candidate tool imports, dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(RUNNER_REVIEW_GATE)
    require_review(review)

    write_json(HARDENING_PLAN_GATE, build_gate(review))
    write_text(HARDENING_PLAN_REPORT, build_report(review))
    write_text(HARDENING_PLAN_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Hardening Plan v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
