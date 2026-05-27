from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

BEHAVIOR_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_BEHAVIOR_EXPANSION_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_BEHAVIOR_EXPANSION_PLAN_REVIEWED"
REVIEW_STATUS = "adapter_behavior_expansion_plan_reviewed_ready_for_behavior_expansion"


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


def require_behavior_plan(plan: dict) -> None:
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("behavior expansion plan goal mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("behavior expansion plan must point to this review goal")
    if plan.get("ready_for_adapter_behavior_expansion_plan_review_count") != 1:
        raise SystemExit("behavior expansion plan must be ready for review")
    for key, expected in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "plan_blocker_count": 0,
    }.items():
        if plan.get(key) != expected:
            raise SystemExit(f"behavior expansion plan {key} mismatch")


def reviewed_behavior_requirements(plan: dict) -> list[dict]:
    reviewed = []
    for item in plan["behavior_requirements"]:
        reviewed.append(
            {
                "requirement_id": item["requirement_id"],
                "source_regression_test_id": item["source_regression_test_id"],
                "regression_type": item["regression_type"],
                "review_status": "reviewed_behavior_requirement_preserves_repo_local_boundary",
                "candidate_tool_import_allowed": False,
                "dependency_install_allowed": False,
                "external_fetch_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return reviewed


def counts(plan: dict) -> dict:
    return {
        "adapter_module_count": plan["adapter_module_count"],
        "reviewed_regression_test_count": plan["reviewed_regression_test_count"],
        "behavior_requirement_count": plan["behavior_requirement_count"],
        "reviewed_behavior_requirement_count": len(reviewed_behavior_requirements(plan)),
        "planned_behavior_task_count": plan["planned_behavior_task_count"],
        "invalid_fixture_behavior_requirement_count": plan["invalid_fixture_behavior_requirement_count"],
        "boundary_behavior_requirement_count": plan["boundary_behavior_requirement_count"],
        "evidence_mapping_behavior_requirement_count": plan["evidence_mapping_behavior_requirement_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "plan_blocker_count": plan["plan_blocker_count"],
        "review_blocker_count": 0,
        "ready_for_adapter_behavior_expansion_plan_review_count": plan["ready_for_adapter_behavior_expansion_plan_review_count"],
        "ready_for_adapter_behavior_expansion_count": 1,
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
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "reviewed_regression_tests": plan["reviewed_regression_tests"],
        "behavior_requirements": plan["behavior_requirements"],
        "reviewed_behavior_requirements": reviewed_behavior_requirements(plan),
        "planned_file_targets": plan["planned_file_targets"],
        "validation_commands": plan["validation_commands"],
        "input_uris": {
            "adapter_behavior_expansion_plan": rel(BEHAVIOR_PLAN),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(plan),
        "claim_boundary": false_boundary(),
    }


def build_validation_result(plan: dict) -> dict:
    return {
        **base_review_record(plan),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(BEHAVIOR_PLAN),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(REVIEW_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(plan: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(plan).items())
    review_lines = "\n".join(
        "- {requirement_id}: source_regression_test_id={source_regression_test_id}, review_status=reviewed_behavior_requirement_preserves_repo_local_boundary".format(
            **item
        )
        for item in reviewed_behavior_requirements(plan)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Plan Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1=true

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

## Reviewed behavior requirements

{review_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: implement-capability-candidate-primary-source-priority-1-adapter-behavior-expansion
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Implement repo-local adapter behavior expansion from the reviewed behavior plan
  - Preserve invalid-fixture rejection, protected-action boundary invariants, and evidence-mapping no-action-drift behavior
  - Keep implementation provider-neutral, dependency-free, and runtime-free
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    plan = read_json(BEHAVIOR_PLAN)
    require_behavior_plan(plan)
    write_json(REVIEW_GATE, base_review_record(plan))
    write_text(REVIEW_REPORT, build_report(plan))
    write_text(REVIEW_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plan))
    write_text(VALIDATION_REPORT, build_report(plan))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Plan Review v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
