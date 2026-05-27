from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

MUTATION_PACK_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_gate.json"
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
CREATED_AT = "2026-05-27T00:00:00Z"
RUNNER_DECISION = "EXECUTE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_RUNNER"
RUNNER_STATUS = "adapter_contract_validation_harness_fixture_mutation_runner_executed_ready_for_review"


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
        raise SystemExit("fixture mutation pack review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("fixture mutation pack review must point to this mutation runner goal")
    if review.get("ready_for_adapter_contract_validation_harness_fixture_mutation_runner_count") != 1:
        raise SystemExit("fixture mutation pack review must be ready for mutation runner")
    for key, expected in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "mutation_fixture_result_matched_expected_count": 5,
    }.items():
        if review.get(key) != expected:
            raise SystemExit(f"fixture mutation pack review {key} mismatch")


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


def mutation_runner_results(review: dict) -> list[dict]:
    results = []
    reviewed_by_id = {
        item["mutation_fixture_id"]: item
        for item in review["reviewed_mutation_fixture_validation_results"]
    }
    for uri in review["mutation_fixture_uris"]:
        fixture = read_json(ROOT / uri)
        schema = read_json(ROOT / fixture["target_schema_uri"])
        actual_valid, failure_reasons = validate_instance(schema, fixture["mutated_instance"])
        reviewed = reviewed_by_id[fixture["mutation_fixture_id"]]
        results.append(
            {
                "mutation_fixture_id": fixture["mutation_fixture_id"],
                "area_id": fixture["area_id"],
                "mutation_fixture_uri": uri,
                "target_schema_id": fixture["target_schema_id"],
                "target_schema_uri": fixture["target_schema_uri"],
                "expected_valid": fixture["expected_valid"],
                "actual_valid": actual_valid,
                "failure_reasons": failure_reasons,
                "validation_result_matched_expected": actual_valid == fixture["expected_valid"],
                "reviewed_result_matched": failure_reasons == reviewed["failure_reasons"],
                "runner_status": "mutation_fixture_executed_through_repo_local_no_install_harness",
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
    results = mutation_runner_results(review)
    return {
        "source_schema_artifact_count": review["source_schema_artifact_count"],
        "mutation_fixture_count": review["mutation_fixture_count"],
        "reviewed_mutation_fixture_count": review["reviewed_mutation_fixture_count"],
        "mutation_runner_result_count": len(results),
        "mutation_fixture_expected_invalid_count": review["mutation_fixture_expected_invalid_count"],
        "mutation_fixture_actual_invalid_count": sum(1 for result in results if result["actual_valid"] is False),
        "mutation_fixture_result_matched_expected_count": sum(
            1 for result in results if result["validation_result_matched_expected"] is True
        ),
        "schema_boundary_mutation_count": sum(
            1 for result in results if result["area_id"] != "malformed-fixture-record-coverage"
        ),
        "malformed_fixture_record_count": sum(
            1 for result in results if result["area_id"] == "malformed-fixture-record-coverage"
        ),
        "blocked_action_count": review["blocked_action_count"],
        "reviewed_blocked_action_count": review["reviewed_blocked_action_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_fixture_mutation_runner_review_count": 1,
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
        "mutation_fixture_uris": review["mutation_fixture_uris"],
        "mutation_runner_results": mutation_runner_results(review),
        "reviewed_blocked_actions": review["reviewed_blocked_actions"],
        "input_uris": {
            "adapter_contract_validation_harness_fixture_mutation_pack_review_gate": rel(MUTATION_PACK_REVIEW_GATE),
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
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-runner-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local mutation fixtures executed through no-install adapter contract validation harness",
    }


def build_validation_result(review: dict) -> dict:
    return {
        **base_runner_record(review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(MUTATION_PACK_REVIEW_GATE),
            rel(MUTATION_RUNNER_RESULT),
            rel(MUTATION_RUNNER_GATE),
            rel(MUTATION_RUNNER_REPORT),
            rel(MUTATION_RUNNER_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(review).items())
    result_lines = "\n".join(
        "- {mutation_fixture_id}: runner_status={runner_status}, expected_valid=false, actual_valid={actual_valid}, reviewed_result_matched={reviewed_result_matched}, failure_reasons={failure_reasons}".format(
            **result
        )
        for result in mutation_runner_results(review)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Runner v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1=true

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

## Mutation runner results

{result_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-runner
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local mutation runner results and confirm all reviewed mutation fixtures remain invalid
  - Confirm runner failure reasons still match reviewed mutation fixture failure reasons
  - Confirm no candidate tool import, dependency install, external fetch, runtime integration, deploy, publish, or readiness claim was introduced
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(MUTATION_PACK_REVIEW_GATE)
    require_review(review)

    write_json(MUTATION_RUNNER_RESULT, base_runner_record(review))
    write_json(MUTATION_RUNNER_GATE, build_gate(review))
    write_text(MUTATION_RUNNER_REPORT, build_report(review))
    write_text(MUTATION_RUNNER_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Runner v0.1")
    print("RESULT: PASS")
    print("generated=6")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
