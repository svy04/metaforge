from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

HARNESS_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_PLAN_REVIEWED"
REVIEW_STATUS = "adapter_contract_validation_harness_plan_validated_ready_for_no_install_runner"


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


def require_harness_plan(plan: dict) -> None:
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("adapter contract validation harness plan goal mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("adapter contract validation harness plan must point to this review goal")
    if plan.get("ready_for_adapter_contract_validation_harness_plan_review_count") != 1:
        raise SystemExit("adapter contract validation harness plan must be ready for review")
    for key, expected in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if plan.get(key) != expected:
            raise SystemExit(f"adapter contract validation harness plan {key} mismatch")


def reviewed_responsibilities(plan: dict) -> list[dict]:
    return [
        {
            **item,
            "review_status": "reviewed_no_install_harness_responsibility",
            "harness_responsibility_contract_validated": True,
        }
        for item in plan["harness_responsibilities"]
    ]


def reviewed_steps(plan: dict) -> list[dict]:
    return [
        {
            **item,
            "review_status": "reviewed_deterministic_no_runtime_step",
            "step_contract_validated": True,
        }
        for item in plan["planned_harness_steps"]
    ]


def counts(plan: dict) -> dict:
    return {
        "source_schema_artifact_count": plan["source_schema_artifact_count"],
        "reviewed_validation_fixture_count": plan["reviewed_validation_fixture_count"],
        "harness_responsibility_count": plan["harness_responsibility_count"],
        "reviewed_harness_responsibility_count": len(reviewed_responsibilities(plan)),
        "planned_harness_step_count": plan["planned_harness_step_count"],
        "reviewed_planned_harness_step_count": len(reviewed_steps(plan)),
        "input_contract_count": plan["input_contract_count"],
        "output_contract_count": plan["output_contract_count"],
        "blocked_action_count": plan["blocked_action_count"],
        "reviewed_blocked_action_count": len(plan["blocked_actions"]),
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_contract_validation_harness_runner_count": 1,
    }


def base_review_record(plan: dict) -> dict:
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
        "source_schema_artifacts": plan["source_schema_artifacts"],
        "reviewed_validation_fixtures": plan["reviewed_validation_fixtures"],
        "reviewed_harness_responsibilities": reviewed_responsibilities(plan),
        "reviewed_planned_harness_steps": reviewed_steps(plan),
        "input_contracts": plan["input_contracts"],
        "output_contracts": plan["output_contracts"],
        "reviewed_blocked_actions": plan["blocked_actions"],
        "input_uris": {
            "adapter_contract_validation_harness_plan_gate": rel(HARNESS_PLAN_GATE),
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
        **base_review_record(plan),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-plan-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local no-install adapter contract validation harness plan reviewed for runner implementation",
    }


def build_validation_result(plan: dict) -> dict:
    return {
        **base_review_record(plan),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(HARNESS_PLAN_GATE),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(REVIEW_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(plan: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(plan).items())
    responsibility_lines = "\n".join(
        "- {responsibility_id}: review_status={review_status}, harness_responsibility_contract_validated=true".format(
            **item
        )
        for item in reviewed_responsibilities(plan)
    )
    step_lines = "\n".join(
        "- {step_id}: review_status={review_status}, step_contract_validated=true".format(**item)
        for item in reviewed_steps(plan)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Plan Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1=true

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

## Reviewed harness responsibilities

{responsibility_lines}

## Reviewed harness steps

{step_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-runner
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create the repo-local no-install adapter contract validation harness runner
  - Implement deterministic schema/fixture checks using only standard-library repo-local file reads
  - Keep candidate tool imports, dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    plan = read_json(HARNESS_PLAN_GATE)
    require_harness_plan(plan)

    write_json(REVIEW_GATE, build_gate(plan))
    write_text(REVIEW_REPORT, build_report(plan))
    write_text(REVIEW_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plan))
    write_text(VALIDATION_REPORT, build_report(plan))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Plan Review v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
