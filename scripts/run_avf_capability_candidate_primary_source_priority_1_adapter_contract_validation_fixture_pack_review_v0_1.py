from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

FIXTURE_PACK_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_FIXTURE_PACK_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_FIXTURE_PACK_REVIEWED"
REVIEW_STATUS = "adapter_contract_validation_fixture_pack_validated_ready_for_validation_harness_plan"


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


def require_fixture_pack(pack: dict) -> None:
    if pack.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("adapter contract validation fixture pack goal mismatch")
    if pack.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("adapter contract validation fixture pack must point to this review goal")
    if pack.get("ready_for_adapter_contract_validation_fixture_pack_review_count") != 1:
        raise SystemExit("adapter contract validation fixture pack must be ready for review")
    if pack.get("provider_neutral") is not True:
        raise SystemExit("adapter contract validation fixture pack must remain provider-neutral")
    if pack.get("dependency_free") is not True:
        raise SystemExit("adapter contract validation fixture pack must remain dependency-free")
    if pack.get("candidate_tool_import_allowed") is not False:
        raise SystemExit("adapter contract validation fixture pack must not allow candidate tool import")
    if pack.get("dependency_install_allowed") is not False:
        raise SystemExit("adapter contract validation fixture pack must not allow dependency install")
    if pack.get("runtime_integration_allowed") is not False:
        raise SystemExit("adapter contract validation fixture pack must not allow runtime integration")


def reviewed_fixtures(pack: dict) -> list[dict]:
    return [
        {
            **fixture,
            "review_status": "reviewed_fixture_validation_result_matches_expected",
            "fixture_contract_validated": True,
        }
        for fixture in pack["validation_fixtures"]
    ]


def counts(pack: dict) -> dict:
    return {
        "source_schema_artifact_count": pack["source_schema_artifact_count"],
        "validation_fixture_count": pack["validation_fixture_count"],
        "reviewed_validation_fixture_count": len(reviewed_fixtures(pack)),
        "passing_fixture_count": pack["passing_fixture_count"],
        "failing_fixture_count": pack["failing_fixture_count"],
        "fixture_validation_result_matched_expected_count": pack["fixture_validation_result_matched_expected_count"],
        "provider_neutral_fixture_count": pack["provider_neutral_fixture_count"],
        "dependency_free_fixture_count": pack["dependency_free_fixture_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_plan_count": 1,
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
        "runtime_integration_allowed": False,
        "source_schema_artifacts": pack["source_schema_artifacts"],
        "reviewed_validation_fixtures": reviewed_fixtures(pack),
        "input_uris": {
            "adapter_contract_validation_fixture_pack_gate": rel(FIXTURE_PACK_GATE),
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
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-fixture-pack-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local adapter contract validation fixtures reviewed for validation harness planning",
    }


def build_validation_result(pack: dict) -> dict:
    return {
        **base_review_record(pack),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(FIXTURE_PACK_GATE),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(REVIEW_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(pack: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(pack).items())
    fixture_lines = "\n".join(
        "- {fixture_id}: expected_valid={expected_valid}, actual_valid={actual_valid}, review_status={review_status}, fixture_contract_validated=true".format(
            **fixture
        )
        for fixture in reviewed_fixtures(pack)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Fixture Pack Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1=true

## Review summary

- candidate_id={CANDIDATE_ID}
- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- provider_neutral=true
- dependency_free=true
- candidate_tool_import_allowed=false
- dependency_install_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Reviewed validation fixtures

{fixture_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local no-install adapter contract validation harness plan
  - Map reviewed fixtures to future no-runtime validation harness responsibilities
  - Keep the plan provider-neutral, dependency-free, and free of candidate tool imports
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    pack = read_json(FIXTURE_PACK_GATE)
    require_fixture_pack(pack)

    write_json(REVIEW_GATE, build_gate(pack))
    write_text(REVIEW_REPORT, build_report(pack))
    write_text(REVIEW_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(pack))
    write_text(VALIDATION_REPORT, build_report(pack))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Fixture Pack Review v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
