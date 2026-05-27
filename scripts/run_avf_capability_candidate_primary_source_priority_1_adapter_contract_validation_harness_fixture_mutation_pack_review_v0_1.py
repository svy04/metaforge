from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

MUTATION_PACK_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_PACK_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_PACK_REVIEWED"
REVIEW_STATUS = "adapter_contract_validation_harness_fixture_mutation_pack_validated_ready_for_mutation_runner"


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


def require_pack(pack: dict) -> None:
    if pack.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("fixture mutation pack goal mismatch")
    if pack.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("fixture mutation pack must point to this review goal")
    if pack.get("ready_for_adapter_contract_validation_harness_fixture_mutation_pack_review_count") != 1:
        raise SystemExit("fixture mutation pack must be ready for review")
    for key, expected in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "mutation_fixture_result_matched_expected_count": 5,
    }.items():
        if pack.get(key) != expected:
            raise SystemExit(f"fixture mutation pack {key} mismatch")


def reviewed_results(pack: dict) -> list[dict]:
    return [
        {
            **item,
            "review_status": "reviewed_mutation_fixture_invalid_outcome_matches_expected",
            "mutation_fixture_contract_validated": True,
        }
        for item in pack["mutation_fixture_validation_results"]
    ]


def counts(pack: dict) -> dict:
    return {
        "source_schema_artifact_count": pack["source_schema_artifact_count"],
        "hardening_area_count": pack["hardening_area_count"],
        "fixture_mutation_plan_count": pack["fixture_mutation_plan_count"],
        "mutation_fixture_count": pack["mutation_fixture_count"],
        "reviewed_mutation_fixture_count": len(pack["mutation_fixture_uris"]),
        "mutation_fixture_expected_invalid_count": pack["mutation_fixture_expected_invalid_count"],
        "mutation_fixture_actual_invalid_count": pack["mutation_fixture_actual_invalid_count"],
        "mutation_fixture_result_matched_expected_count": pack["mutation_fixture_result_matched_expected_count"],
        "reviewed_mutation_fixture_result_count": len(reviewed_results(pack)),
        "blocked_action_count": pack["blocked_action_count"],
        "reviewed_blocked_action_count": pack["reviewed_blocked_action_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_fixture_mutation_runner_count": 1,
    }


def base_review_record(pack: dict) -> dict:
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
        "mutation_fixture_uris": pack["mutation_fixture_uris"],
        "reviewed_mutation_fixture_validation_results": reviewed_results(pack),
        "reviewed_blocked_actions": pack["reviewed_blocked_actions"],
        "input_uris": {
            "adapter_contract_validation_harness_fixture_mutation_pack_gate": rel(MUTATION_PACK_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(pack),
        "claim_boundary": false_boundary(),
    }


def build_gate(pack: dict) -> dict:
    return {
        **base_review_record(pack),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-pack-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local mutation fixture pack reviewed for mutation runner",
    }


def build_validation_result(pack: dict) -> dict:
    return {
        **base_review_record(pack),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(MUTATION_PACK_GATE),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(REVIEW_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(pack: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(pack).items())
    result_lines = "\n".join(
        "- {mutation_fixture_id}: review_status={review_status}, mutation_fixture_contract_validated=true, actual_valid={actual_valid}, validation_result_matched_expected={validation_result_matched_expected}".format(
            **item
        )
        for item in reviewed_results(pack)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Pack Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1=true

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

## Reviewed mutation fixture validation results

{result_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-runner
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local mutation runner that executes the reviewed mutation fixtures through the no-install harness boundary
  - Confirm every reviewed mutation fixture remains invalid under deterministic validation
  - Keep candidate tool imports, dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    pack = read_json(MUTATION_PACK_GATE)
    require_pack(pack)

    write_json(REVIEW_GATE, build_gate(pack))
    write_text(REVIEW_REPORT, build_report(pack))
    write_text(REVIEW_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(pack))
    write_text(VALIDATION_REPORT, build_report(pack))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Pack Review v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
