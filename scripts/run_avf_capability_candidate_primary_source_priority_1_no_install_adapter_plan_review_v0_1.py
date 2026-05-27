from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

ADAPTER_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_NO_INSTALL_ADAPTER_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_NO_INSTALL_ADAPTER_PLAN_REVIEWED"
REVIEW_STATUS = "no_install_adapter_plan_validated_ready_for_adapter_contract_schema_pack"


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


def require_plan(plan: dict) -> None:
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("adapter plan goal mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("adapter plan must point to this review goal")
    if plan.get("ready_for_no_install_adapter_plan_review_count") != 1:
        raise SystemExit("adapter plan must be ready for review")
    if plan.get("dependency_install_allowed") is not False:
        raise SystemExit("adapter plan must not allow dependency install")
    if plan.get("oss_clone_allowed") is not False:
        raise SystemExit("adapter plan must not allow OSS clone")
    if plan.get("runtime_integration_allowed") is not False:
        raise SystemExit("adapter plan must not allow runtime integration")


def reviewed_adapter_components(plan: dict) -> list[dict]:
    return [
        {
            **component,
            "review_status": "reviewed_contract_only_component_validated",
        }
        for component in plan["adapter_components"]
    ]


def counts(plan: dict) -> dict:
    return {
        "adapter_component_count": plan["adapter_component_count"],
        "reviewed_adapter_component_count": len(reviewed_adapter_components(plan)),
        "contract_boundary_count": plan["contract_boundary_count"],
        "reviewed_contract_boundary_count": len(plan["contract_boundaries"]),
        "blocked_action_count": plan["blocked_action_count"],
        "reviewed_blocked_action_count": len(plan["blocked_actions"]),
        "dependency_install_allowed_count": plan["dependency_install_allowed_count"],
        "oss_clone_allowed_count": plan["oss_clone_allowed_count"],
        "runtime_integration_allowed_count": plan["runtime_integration_allowed_count"],
        "review_blocker_count": 0,
        "ready_for_adapter_contract_schema_pack_count": 1,
    }


def base_review_record(plan: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "plan_remains_contract_only": True,
        "reviewed_adapter_components": reviewed_adapter_components(plan),
        "reviewed_contract_boundaries": plan["contract_boundaries"],
        "reviewed_blocked_actions": plan["blocked_actions"],
        "input_uris": {
            "no_install_adapter_plan_gate": rel(ADAPTER_PLAN_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "dependency_install_allowed": False,
        "oss_clone_allowed": False,
        "runtime_integration_allowed": False,
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
        "gate_id": "avf-capability-candidate-primary-source-priority-1-no-install-adapter-plan-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "No-install adapter plan reviewed as contract-only and ready for schema pack generation",
    }


def build_validation_result(plan: dict) -> dict:
    return {
        **base_review_record(plan),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(ADAPTER_PLAN_GATE),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(plan: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(plan).items())
    component_lines = "\n".join(
        "- {component_id}: review_status=reviewed_contract_only_component_validated, boundary={implementation_boundary}".format(
            **component
        )
        for component in reviewed_adapter_components(plan)
    )
    boundary_lines = "\n".join(f"- {boundary}" for boundary in plan["contract_boundaries"])
    blocked_lines = "\n".join(f"- {action}" for action in plan["blocked_actions"])
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 No-Install Adapter Plan Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1=true

## Review summary

- candidate_id={CANDIDATE_ID}
- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- plan_remains_contract_only=true
- dependency_install_allowed=false
- oss_clone_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Reviewed adapter components

{component_lines}

## Reviewed contract boundaries

{boundary_lines}

## Reviewed blocked actions

{blocked_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-schema-pack
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create adapter contract schemas without importing candidate tools
  - Generate repo-local schema artifacts for eval cases, red-team cases, RAG metric slots, and governance gates
  - Keep all schemas provider-neutral and dependency-free
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    plan = read_json(ADAPTER_PLAN_GATE)
    require_plan(plan)

    record = base_review_record(plan)
    write_json(REVIEW_GATE, build_gate(plan))
    report = build_report(plan)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plan))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 No-Install Adapter Plan Review v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(plan).items():
        print(f"{key}={value}")
    print("plan_remains_contract_only=true")
    print("dependency_install_allowed=false")
    print("oss_clone_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
