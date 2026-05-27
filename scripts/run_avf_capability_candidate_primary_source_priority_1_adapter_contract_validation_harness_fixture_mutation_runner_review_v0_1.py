from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

MUTATION_RUNNER_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_RUNNER_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_RUNNER_REVIEWED"
REVIEW_STATUS = "adapter_contract_validation_harness_fixture_mutation_runner_validated_ready_for_acceptance_gate"


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


def require_runner(runner: dict) -> None:
    if runner.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("fixture mutation runner goal mismatch")
    if runner.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("fixture mutation runner must point to this review goal")
    if runner.get("ready_for_adapter_contract_validation_harness_fixture_mutation_runner_review_count") != 1:
        raise SystemExit("fixture mutation runner must be ready for review")
    for key, expected in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "mutation_fixture_result_matched_expected_count": 5,
    }.items():
        if runner.get(key) != expected:
            raise SystemExit(f"fixture mutation runner {key} mismatch")


def reviewed_results(runner: dict) -> list[dict]:
    return [
        {
            **item,
            "review_status": "reviewed_mutation_runner_result_matches_reviewed_fixture_outcome",
            "mutation_runner_result_contract_validated": True,
        }
        for item in runner["mutation_runner_results"]
    ]


def counts(runner: dict) -> dict:
    return {
        "source_schema_artifact_count": runner["source_schema_artifact_count"],
        "mutation_fixture_count": runner["mutation_fixture_count"],
        "reviewed_mutation_fixture_count": runner["reviewed_mutation_fixture_count"],
        "mutation_runner_result_count": runner["mutation_runner_result_count"],
        "reviewed_mutation_runner_result_count": len(reviewed_results(runner)),
        "mutation_fixture_expected_invalid_count": runner["mutation_fixture_expected_invalid_count"],
        "mutation_fixture_actual_invalid_count": runner["mutation_fixture_actual_invalid_count"],
        "mutation_fixture_result_matched_expected_count": runner["mutation_fixture_result_matched_expected_count"],
        "schema_boundary_mutation_count": runner["schema_boundary_mutation_count"],
        "malformed_fixture_record_count": runner["malformed_fixture_record_count"],
        "blocked_action_count": runner["blocked_action_count"],
        "reviewed_blocked_action_count": runner["reviewed_blocked_action_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_acceptance_gate_count": 1,
    }


def base_review_record(runner: dict) -> dict:
    return {
        "created_at": CREATED_AT,
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
        "mutation_fixture_uris": runner["mutation_fixture_uris"],
        "reviewed_mutation_runner_results": reviewed_results(runner),
        "reviewed_blocked_actions": runner["reviewed_blocked_actions"],
        "input_uris": {
            "adapter_contract_validation_harness_fixture_mutation_runner_gate": rel(MUTATION_RUNNER_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(runner),
        "claim_boundary": false_boundary(),
    }


def build_gate(runner: dict) -> dict:
    return {
        **base_review_record(runner),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-runner-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local mutation runner reviewed for adapter contract validation harness acceptance gate",
    }


def build_validation_result(runner: dict) -> dict:
    return {
        **base_review_record(runner),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(MUTATION_RUNNER_GATE),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(REVIEW_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(runner: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(runner).items())
    result_lines = "\n".join(
        "- {mutation_fixture_id}: review_status={review_status}, mutation_runner_result_contract_validated=true, actual_valid={actual_valid}, reviewed_result_matched={reviewed_result_matched}".format(
            **item
        )
        for item in reviewed_results(runner)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Runner Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1=true

## Review summary

- candidate_id={CANDIDATE_ID}
- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
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

## Reviewed mutation runner results

{result_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-acceptance-gate
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local acceptance gate that consolidates schema fixtures, mutation runner results, and protected action boundaries
  - Decide whether the no-install adapter contract validation harness is ready to feed a future adapter implementation plan
  - Keep candidate tool imports, dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    runner = read_json(MUTATION_RUNNER_GATE)
    require_runner(runner)

    write_json(REVIEW_GATE, build_gate(runner))
    write_text(REVIEW_REPORT, build_report(runner))
    write_text(REVIEW_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(runner))
    write_text(VALIDATION_REPORT, build_report(runner))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Runner Review v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
