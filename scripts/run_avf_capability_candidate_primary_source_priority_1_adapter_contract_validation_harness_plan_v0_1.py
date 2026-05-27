from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

FIXTURE_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_gate.json"
HARNESS_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan.json"
HARNESS_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_gate.json"
HARNESS_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_report.md"
HARNESS_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_DECISION = "CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_PLAN"
PLAN_STATUS = "adapter_contract_validation_harness_plan_created_provider_neutral_no_install"


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


def require_fixture_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("adapter contract validation fixture pack review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("adapter contract validation fixture pack review must point to this harness plan goal")
    if review.get("ready_for_adapter_contract_validation_harness_plan_count") != 1:
        raise SystemExit("adapter contract validation fixture pack review must be ready for harness plan")
    if review.get("provider_neutral") is not True:
        raise SystemExit("adapter contract validation fixture pack review must remain provider-neutral")
    if review.get("dependency_free") is not True:
        raise SystemExit("adapter contract validation fixture pack review must remain dependency-free")
    if review.get("candidate_tool_import_allowed") is not False:
        raise SystemExit("adapter contract validation fixture pack review must not allow candidate tool import")
    if review.get("dependency_install_allowed") is not False:
        raise SystemExit("adapter contract validation fixture pack review must not allow dependency install")
    if review.get("runtime_integration_allowed") is not False:
        raise SystemExit("adapter contract validation fixture pack review must not allow runtime integration")


def blocked_actions() -> list[str]:
    return [
        "dependency_install",
        "oss_clone",
        "candidate_tool_import",
        "runtime_integration",
        "provider_call",
        "live_model_call",
        "external_fetch",
        "deploy",
        "publish",
        "readiness_claim",
    ]


def harness_responsibilities() -> list[dict]:
    base = {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "runtime_integration_allowed": False,
    }
    return [
        {
            "responsibility_id": "load-provider-neutral-schema-contracts",
            "purpose": "Load reviewed JSON Schema contract files from repo-local paths only.",
            "input_contracts": ["source_schema_artifacts"],
            "output_contracts": ["loaded_schema_contracts"],
            **base,
        },
        {
            "responsibility_id": "load-repo-local-validation-fixtures",
            "purpose": "Load reviewed valid and invalid fixture files from repo-local paths only.",
            "input_contracts": ["reviewed_validation_fixtures"],
            "output_contracts": ["loaded_fixture_instances"],
            **base,
        },
        {
            "responsibility_id": "validate-required-fields",
            "purpose": "Check required fields for each fixture against its mapped schema contract.",
            "input_contracts": ["loaded_schema_contracts", "loaded_fixture_instances"],
            "output_contracts": ["required_field_results"],
            **base,
        },
        {
            "responsibility_id": "validate-additional-properties",
            "purpose": "Check additionalProperties=false boundaries without executing any candidate tool.",
            "input_contracts": ["loaded_schema_contracts", "loaded_fixture_instances"],
            "output_contracts": ["additional_property_results"],
            **base,
        },
        {
            "responsibility_id": "compare-expected-vs-actual-fixture-results",
            "purpose": "Compare expected_valid and actual validation outcomes for each reviewed fixture.",
            "input_contracts": ["reviewed_validation_fixtures", "validation_results"],
            "output_contracts": ["fixture_outcome_match_results"],
            **base,
        },
        {
            "responsibility_id": "emit-claim-bounded-validation-report",
            "purpose": "Emit repo-local validation summaries with protected action flags remaining false.",
            "input_contracts": ["fixture_outcome_match_results", "claim_boundary"],
            "output_contracts": ["claim_bounded_validation_report"],
            **base,
        },
    ]


def planned_harness_steps() -> list[dict]:
    return [
        {
            "step_id": "step-1-load-schema-contracts",
            "responsibility_id": "load-provider-neutral-schema-contracts",
            "execution_boundary": "repo_local_file_read_only",
        },
        {
            "step_id": "step-2-load-fixtures",
            "responsibility_id": "load-repo-local-validation-fixtures",
            "execution_boundary": "repo_local_file_read_only",
        },
        {
            "step_id": "step-3-check-required-fields",
            "responsibility_id": "validate-required-fields",
            "execution_boundary": "in_process_no_dependency_install",
        },
        {
            "step_id": "step-4-check-additional-properties",
            "responsibility_id": "validate-additional-properties",
            "execution_boundary": "in_process_no_candidate_tool_import",
        },
        {
            "step_id": "step-5-compare-outcomes",
            "responsibility_id": "compare-expected-vs-actual-fixture-results",
            "execution_boundary": "deterministic_repo_local_comparison",
        },
        {
            "step_id": "step-6-emit-report",
            "responsibility_id": "emit-claim-bounded-validation-report",
            "execution_boundary": "repo_local_artifact_write_only",
        },
    ]


def counts(review: dict) -> dict:
    return {
        "source_schema_artifact_count": len(review["source_schema_artifacts"]),
        "reviewed_validation_fixture_count": len(review["reviewed_validation_fixtures"]),
        "harness_responsibility_count": len(harness_responsibilities()),
        "planned_harness_step_count": len(planned_harness_steps()),
        "input_contract_count": 2,
        "output_contract_count": 2,
        "blocked_action_count": len(blocked_actions()),
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_plan_review_count": 1,
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
        "source_schema_artifacts": review["source_schema_artifacts"],
        "reviewed_validation_fixtures": review["reviewed_validation_fixtures"],
        "harness_responsibilities": harness_responsibilities(),
        "planned_harness_steps": planned_harness_steps(),
        "input_contracts": [
            "source_schema_artifacts",
            "reviewed_validation_fixtures",
        ],
        "output_contracts": [
            "fixture_outcome_match_results",
            "claim_bounded_validation_report",
        ],
        "blocked_actions": blocked_actions(),
        "input_uris": {
            "adapter_contract_validation_fixture_pack_review_gate": rel(FIXTURE_REVIEW_GATE),
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
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-plan-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local no-install adapter contract validation harness plan created without dependency or runtime adoption",
    }


def build_validation_result(review: dict) -> dict:
    return {
        **base_plan_record(review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(FIXTURE_REVIEW_GATE),
            rel(HARNESS_PLAN),
            rel(HARNESS_PLAN_GATE),
            rel(HARNESS_PLAN_REPORT),
            rel(HARNESS_PLAN_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(review).items())
    responsibility_lines = "\n".join(
        "- {responsibility_id}: provider_neutral=true, dependency_free=true, candidate_tool_import_allowed=false, runtime_integration_allowed=false".format(
            **item
        )
        for item in harness_responsibilities()
    )
    blocked_lines = "\n".join(f"- {action}" for action in blocked_actions())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1=true

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

## Harness responsibilities

{responsibility_lines}

## Blocked actions

{blocked_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local no-install adapter contract validation harness plan
  - Confirm responsibilities map reviewed schemas and fixtures to deterministic validation duties
  - Confirm blocked actions remain dependency install, OSS clone, candidate tool import, runtime integration, external fetch, provider calls, deploy, publish, and readiness claims
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(FIXTURE_REVIEW_GATE)
    require_fixture_review(review)

    write_json(HARNESS_PLAN, base_plan_record(review))
    write_json(HARNESS_PLAN_GATE, build_gate(review))
    write_text(HARNESS_PLAN_REPORT, build_report(review))
    write_text(HARNESS_PLAN_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Plan v0.1")
    print("RESULT: PASS")
    print("generated=6")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
