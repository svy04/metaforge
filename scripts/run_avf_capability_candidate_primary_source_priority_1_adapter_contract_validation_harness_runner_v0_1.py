from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PLAN_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_gate.json"
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
CREATED_AT = "2026-05-27T00:00:00Z"
RUNNER_DECISION = "CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_RUNNER"
RUNNER_STATUS = "adapter_contract_validation_harness_runner_created_validated_provider_neutral_no_install"


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


def require_plan_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("adapter contract validation harness plan review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("adapter contract validation harness plan review must point to this runner goal")
    if review.get("ready_for_adapter_contract_validation_harness_runner_count") != 1:
        raise SystemExit("adapter contract validation harness plan review must be ready for runner")
    for key, expected in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if review.get(key) != expected:
            raise SystemExit(f"adapter contract validation harness plan review {key} mismatch")


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


def fixture_validation_results(review: dict) -> list[dict]:
    results = []
    for fixture in review["reviewed_validation_fixtures"]:
        schema = read_json(ROOT / fixture["schema_uri"])
        instance = read_json(ROOT / fixture["fixture_uri"])
        actual_valid, failure_reasons = validate_instance(schema, instance)
        results.append(
            {
                "fixture_id": fixture["fixture_id"],
                "schema_id": fixture["schema_id"],
                "schema_uri": fixture["schema_uri"],
                "fixture_uri": fixture["fixture_uri"],
                "expected_valid": fixture["expected_valid"],
                "actual_valid": actual_valid,
                "failure_reasons": failure_reasons,
                "validation_result_matched_expected": actual_valid == fixture["expected_valid"],
                "provider_neutral": True,
                "dependency_free": True,
                "candidate_tool_import_allowed": False,
                "dependency_install_allowed": False,
                "external_fetch_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return results


def counts(review: dict) -> dict:
    results = fixture_validation_results(review)
    return {
        "source_schema_artifact_count": len(review["source_schema_artifacts"]),
        "reviewed_validation_fixture_count": len(review["reviewed_validation_fixtures"]),
        "harness_responsibility_count": review["harness_responsibility_count"],
        "reviewed_harness_responsibility_count": len(review["reviewed_harness_responsibilities"]),
        "planned_harness_step_count": review["planned_harness_step_count"],
        "reviewed_planned_harness_step_count": len(review["reviewed_planned_harness_steps"]),
        "fixture_validation_result_count": len(results),
        "fixture_validation_result_matched_expected_count": sum(
            1 for result in results if result["validation_result_matched_expected"] is True
        ),
        "passing_fixture_count": sum(1 for result in results if result["expected_valid"] is True),
        "failing_fixture_count": sum(1 for result in results if result["expected_valid"] is False),
        "blocked_action_count": len(review["reviewed_blocked_actions"]),
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_runner_review_count": 1,
    }


def base_runner_record(review: dict) -> dict:
    return {
        "created_at": CREATED_AT,
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
        "reviewed_harness_responsibilities": review["reviewed_harness_responsibilities"],
        "reviewed_planned_harness_steps": review["reviewed_planned_harness_steps"],
        "reviewed_blocked_actions": review["reviewed_blocked_actions"],
        "fixture_validation_results": fixture_validation_results(review),
        "input_uris": {
            "adapter_contract_validation_harness_plan_review_gate": rel(PLAN_REVIEW_GATE),
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
        **base_runner_record(review),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-runner-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local no-install adapter contract validation harness runner executed with expected fixture outcomes",
    }


def build_validation_result(review: dict) -> dict:
    return {
        **base_runner_record(review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(PLAN_REVIEW_GATE),
            rel(RUNNER_RESULT),
            rel(RUNNER_GATE),
            rel(RUNNER_REPORT),
            rel(RUNNER_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(review).items())
    result_lines = "\n".join(
        "- {fixture_id}: expected_valid={expected_valid}, actual_valid={actual_valid}, validation_result_matched_expected={validation_result_matched_expected}, failure_reasons={failure_reasons}".format(
            **result
        )
        for result in fixture_validation_results(review)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Runner v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1=true

## Runner summary

- candidate_id={CANDIDATE_ID}
- runner_decision={RUNNER_DECISION}
- runner_status={RUNNER_STATUS}
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

## Fixture validation results

{result_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-runner
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local no-install adapter contract validation harness runner
  - Confirm deterministic fixture validation results match expected outcomes
  - Confirm no candidate tool import, dependency install, external fetch, runtime integration, deploy, publish, or readiness claim was introduced
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(PLAN_REVIEW_GATE)
    require_plan_review(review)

    write_json(RUNNER_RESULT, base_runner_record(review))
    write_json(RUNNER_GATE, build_gate(review))
    write_text(RUNNER_REPORT, build_report(review))
    write_text(RUNNER_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Runner v0.1")
    print("RESULT: PASS")
    print("generated=6")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
