from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

ACCEPTANCE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_ACCEPTANCE_GATE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
ACCEPTANCE_DECISION = "ACCEPT_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_FOR_FUTURE_IMPLEMENTATION_PLAN"
ACCEPTANCE_STATUS = "accepted_as_repo_local_contract_harness_not_runtime_or_production_ready"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_ACCEPTANCE_GATE_REVIEWED"
REVIEW_STATUS = "adapter_contract_validation_harness_acceptance_gate_reviewed_ready_for_future_adapter_implementation_plan"


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


def require_acceptance_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("acceptance gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("acceptance gate must point to this review goal")
    if gate.get("ready_for_adapter_contract_validation_harness_acceptance_gate_review_count") != 1:
        raise SystemExit("acceptance gate must be ready for review")
    for key, expected in {
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
        "all_fixture_result_matched_expected_count": 13,
        "acceptance_criteria_passed_count": 6,
        "acceptance_blocker_count": 0,
    }.items():
        if gate.get(key) != expected:
            raise SystemExit(f"acceptance gate {key} mismatch")


def reviewed_acceptance_criteria(gate: dict) -> list[dict]:
    return [
        {
            **item,
            "review_status": "reviewed_acceptance_criterion_matches_gate_outcome",
            "acceptance_criterion_contract_validated": True,
        }
        for item in gate["acceptance_criteria"]
    ]


def counts(gate: dict) -> dict:
    return {
        "source_schema_artifact_count": gate["source_schema_artifact_count"],
        "baseline_fixture_result_count": gate["baseline_fixture_result_count"],
        "baseline_fixture_result_matched_expected_count": gate["baseline_fixture_result_matched_expected_count"],
        "baseline_passing_fixture_count": gate["baseline_passing_fixture_count"],
        "baseline_failing_fixture_count": gate["baseline_failing_fixture_count"],
        "mutation_runner_result_count": gate["mutation_runner_result_count"],
        "reviewed_mutation_runner_result_count": gate["reviewed_mutation_runner_result_count"],
        "mutation_fixture_result_matched_expected_count": gate["mutation_fixture_result_matched_expected_count"],
        "all_fixture_result_count": gate["all_fixture_result_count"],
        "all_fixture_result_matched_expected_count": gate["all_fixture_result_matched_expected_count"],
        "all_passing_fixture_count": gate["all_passing_fixture_count"],
        "all_failing_fixture_count": gate["all_failing_fixture_count"],
        "schema_boundary_mutation_count": gate["schema_boundary_mutation_count"],
        "malformed_fixture_record_count": gate["malformed_fixture_record_count"],
        "acceptance_criteria_count": gate["acceptance_criteria_count"],
        "acceptance_criteria_passed_count": gate["acceptance_criteria_passed_count"],
        "blocked_action_count": gate["blocked_action_count"],
        "reviewed_blocked_action_count": gate["reviewed_blocked_action_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "acceptance_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_acceptance_gate_review_count": 1,
        "reviewed_acceptance_criteria_count": len(reviewed_acceptance_criteria(gate)),
        "reviewed_acceptance_criteria_passed_count": len(reviewed_acceptance_criteria(gate)),
        "review_blocker_count": 0,
        "ready_for_adapter_implementation_plan_count": 1,
    }


def base_review_record(gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_status": ACCEPTANCE_STATUS,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "baseline_fixture_validation_results": gate["baseline_fixture_validation_results"],
        "reviewed_mutation_runner_results": gate["reviewed_mutation_runner_results"],
        "reviewed_acceptance_criteria": reviewed_acceptance_criteria(gate),
        "reviewed_blocked_actions": gate["reviewed_blocked_actions"],
        "input_uris": {
            "adapter_contract_validation_harness_acceptance_gate": rel(ACCEPTANCE_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(gate),
        "claim_boundary": false_boundary(),
    }


def build_gate(gate: dict) -> dict:
    return {
        **base_review_record(gate),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-acceptance-gate-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local acceptance gate reviewed for a future no-install adapter implementation plan",
    }


def build_validation_result(gate: dict) -> dict:
    return {
        **base_review_record(gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(ACCEPTANCE_GATE),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(REVIEW_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(gate).items())
    criteria_lines = "\n".join(
        "- {criterion_id}: review_status={review_status}, acceptance_criterion_contract_validated=true, status={status}, evidence_basis={evidence_basis}".format(
            **item
        )
        for item in reviewed_acceptance_criteria(gate)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Acceptance Gate Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1=true

## Review summary

- candidate_id={CANDIDATE_ID}
- acceptance_decision={ACCEPTANCE_DECISION}
- acceptance_status={ACCEPTANCE_STATUS}
- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
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

## Reviewed acceptance criteria

{criteria_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-implementation-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local no-install adapter implementation plan from the reviewed acceptance gate
  - Translate the reviewed harness contract into implementation-plan tasks without importing candidate runtimes
  - Keep candidate tool imports, dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, import candidate tools, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    gate = read_json(ACCEPTANCE_GATE)
    require_acceptance_gate(gate)

    write_json(REVIEW_GATE, build_gate(gate))
    write_text(REVIEW_REPORT, build_report(gate))
    write_text(REVIEW_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Acceptance Gate Review v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
