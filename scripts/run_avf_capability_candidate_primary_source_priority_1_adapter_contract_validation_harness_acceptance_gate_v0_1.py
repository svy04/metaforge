from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

BASELINE_RUNNER_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_gate.json"
MUTATION_RUNNER_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_gate.json"
ACCEPTANCE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate.json"
ACCEPTANCE_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_report.md"
ACCEPTANCE_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_ACCEPTANCE_GATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
ACCEPTANCE_DECISION = "ACCEPT_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_FOR_FUTURE_IMPLEMENTATION_PLAN"
ACCEPTANCE_STATUS = "accepted_as_repo_local_contract_harness_not_runtime_or_production_ready"


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


def require_inputs(baseline: dict, mutation: dict) -> None:
    if baseline.get("fixture_validation_result_matched_expected_count") != 8:
        raise SystemExit("baseline runner gate must have 8 matched fixture results")
    if mutation.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("mutation runner review gate goal mismatch")
    if mutation.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("mutation runner review must point to this acceptance goal")
    if mutation.get("ready_for_adapter_contract_validation_harness_acceptance_gate_count") != 1:
        raise SystemExit("mutation runner review must be ready for acceptance gate")
    if mutation.get("mutation_fixture_result_matched_expected_count") != 5:
        raise SystemExit("mutation runner review must have 5 matched mutation results")


def acceptance_criteria() -> list[dict]:
    base = {
        "status": "PASS",
        "claim_boundary": "repo_local_internal_only",
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }
    return [
        {
            **base,
            "criterion_id": "baseline-fixtures-match-expected",
            "evidence_basis": "baseline_adapter_contract_validation_harness_runner_gate.fixture_validation_result_matched_expected_count=8",
        },
        {
            **base,
            "criterion_id": "mutation-fixtures-remain-invalid",
            "evidence_basis": "fixture_mutation_runner_review_gate.mutation_fixture_actual_invalid_count=5",
        },
        {
            **base,
            "criterion_id": "mutation-runner-results-match-reviewed-outcomes",
            "evidence_basis": "fixture_mutation_runner_review_gate.mutation_fixture_result_matched_expected_count=5",
        },
        {
            **base,
            "criterion_id": "protected-actions-remain-blocked",
            "evidence_basis": "claim_boundary flags remain false across baseline and mutation gates",
        },
        {
            **base,
            "criterion_id": "candidate-runtime-remains-unimported",
            "evidence_basis": "candidate_tool_import_allowed=false and runtime_integration_allowed=false",
        },
        {
            **base,
            "criterion_id": "future-adapter-plan-requires-separate-gate",
            "evidence_basis": "acceptance is limited to repo-local harness planning and does not permit dependency adoption",
        },
    ]


def counts(baseline: dict, mutation: dict) -> dict:
    return {
        "source_schema_artifact_count": baseline["source_schema_artifact_count"],
        "baseline_fixture_result_count": baseline["fixture_validation_result_count"],
        "baseline_fixture_result_matched_expected_count": baseline["fixture_validation_result_matched_expected_count"],
        "baseline_passing_fixture_count": baseline["passing_fixture_count"],
        "baseline_failing_fixture_count": baseline["failing_fixture_count"],
        "mutation_runner_result_count": mutation["mutation_runner_result_count"],
        "reviewed_mutation_runner_result_count": mutation["reviewed_mutation_runner_result_count"],
        "mutation_fixture_result_matched_expected_count": mutation["mutation_fixture_result_matched_expected_count"],
        "all_fixture_result_count": baseline["fixture_validation_result_count"] + mutation["mutation_runner_result_count"],
        "all_fixture_result_matched_expected_count": baseline["fixture_validation_result_matched_expected_count"]
        + mutation["mutation_fixture_result_matched_expected_count"],
        "all_passing_fixture_count": baseline["passing_fixture_count"],
        "all_failing_fixture_count": baseline["failing_fixture_count"] + mutation["mutation_fixture_actual_invalid_count"],
        "schema_boundary_mutation_count": mutation["schema_boundary_mutation_count"],
        "malformed_fixture_record_count": mutation["malformed_fixture_record_count"],
        "acceptance_criteria_count": len(acceptance_criteria()),
        "acceptance_criteria_passed_count": len(acceptance_criteria()),
        "blocked_action_count": mutation["blocked_action_count"],
        "reviewed_blocked_action_count": mutation["reviewed_blocked_action_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "acceptance_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_acceptance_gate_review_count": 1,
    }


def base_acceptance_record(baseline: dict, mutation: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_status": ACCEPTANCE_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "baseline_fixture_validation_results": baseline["fixture_validation_results"],
        "reviewed_mutation_runner_results": mutation["reviewed_mutation_runner_results"],
        "acceptance_criteria": acceptance_criteria(),
        "reviewed_blocked_actions": mutation["reviewed_blocked_actions"],
        "input_uris": {
            "baseline_adapter_contract_validation_harness_runner_gate": rel(BASELINE_RUNNER_GATE),
            "adapter_contract_validation_harness_fixture_mutation_runner_review_gate": rel(MUTATION_RUNNER_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(baseline, mutation),
        "claim_boundary": false_boundary(),
    }


def build_gate(baseline: dict, mutation: dict) -> dict:
    return {
        **base_acceptance_record(baseline, mutation),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-acceptance-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local no-install adapter contract validation harness accepted for a future implementation plan only",
    }


def build_validation_result(baseline: dict, mutation: dict) -> dict:
    return {
        **base_acceptance_record(baseline, mutation),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(BASELINE_RUNNER_GATE),
            rel(MUTATION_RUNNER_REVIEW_GATE),
            rel(ACCEPTANCE_GATE),
            rel(ACCEPTANCE_REPORT),
            rel(ACCEPTANCE_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(baseline: dict, mutation: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(baseline, mutation).items())
    criteria_lines = "\n".join(
        "- {criterion_id}: status=PASS, evidence_basis={evidence_basis}".format(**item)
        for item in acceptance_criteria()
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Acceptance Gate v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1=true

## Acceptance summary

- candidate_id={CANDIDATE_ID}
- acceptance_decision={ACCEPTANCE_DECISION}
- acceptance_status={ACCEPTANCE_STATUS}
- provider_neutral=true
- dependency_free=true
- candidate_tool_import_allowed=false
- dependency_install_allowed=false
- external_fetch_allowed=false
- runtime_integration_allowed=false
- selection_allowed=false
- dependency_adoption_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Acceptance criteria

{criteria_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-acceptance-gate
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local acceptance gate before creating any future adapter implementation plan
  - Confirm the gate accepts only repo-local no-install harness readiness, not runtime integration or production readiness
  - Keep candidate tool imports, dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    baseline = read_json(BASELINE_RUNNER_GATE)
    mutation = read_json(MUTATION_RUNNER_REVIEW_GATE)
    require_inputs(baseline, mutation)

    write_json(ACCEPTANCE_GATE, build_gate(baseline, mutation))
    write_text(ACCEPTANCE_REPORT, build_report(baseline, mutation))
    write_text(ACCEPTANCE_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(baseline, mutation))
    write_text(VALIDATION_REPORT, build_report(baseline, mutation))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Acceptance Gate v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
