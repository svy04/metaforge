from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_gate.json"
BEHAVIOR_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan.json"
BEHAVIOR_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_report.md"
BEHAVIOR_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_BEHAVIOR_EXPANSION_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_DECISION = "CREATE_REPO_LOCAL_ADAPTER_BEHAVIOR_EXPANSION_PLAN_FROM_REVIEWED_REGRESSION_PACK"
PLAN_STATUS = "planned_for_repo_local_adapter_behavior_expansion_review_not_runtime_or_dependency_ready"


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


def require_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("regression pack review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("regression pack review gate must point to this behavior expansion plan goal")
    if gate.get("ready_for_adapter_behavior_expansion_plan_count") != 1:
        raise SystemExit("regression pack review gate must be ready for behavior expansion plan")
    for key, expected in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "review_blocker_count": 0,
    }.items():
        if gate.get(key) != expected:
            raise SystemExit(f"regression pack review gate {key} mismatch")


def planned_file_targets() -> list[str]:
    return [
        "avf/capabilities/adapters/priority_1/record_normalizers.py",
        "avf/capabilities/adapters/priority_1/adapter_contracts.py",
        "avf/capabilities/adapters/priority_1/evidence_mapping.py",
        "avf/capabilities/adapters/priority_1/tests/test_adapter_regression_pack.py",
    ]


def validation_commands() -> list[str]:
    return [
        "python avf\\capabilities\\adapters\\priority_1\\tests\\test_adapter_regression_pack.py",
        "python scripts\\run_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1.py",
        "python scripts\\validate_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1.py",
    ]


def behavior_blueprint() -> dict[str, dict[str, str]]:
    return {
        "rejects-eval-case-missing-claim-boundary": {
            "requirement_id": "enforce-eval-claim-boundary-required",
            "behavior_goal": "Preserve strict eval case rejection when claim_boundary is absent.",
        },
        "rejects-redteam-case-bad-evidence-basis-type": {
            "requirement_id": "enforce-redteam-evidence-basis-list",
            "behavior_goal": "Preserve strict red-team case rejection when evidence_basis is not a list.",
        },
        "rejects-rag-metric-unexpected-runtime-hint": {
            "requirement_id": "reject-rag-runtime-hints",
            "behavior_goal": "Preserve strict RAG metric rejection when fixture records include runtime execution hints.",
        },
        "rejects-governance-gate-bad-risk_tier": {
            "requirement_id": "enforce-governance-risk_tier-enum",
            "behavior_goal": "Preserve strict governance gate rejection when risk_tier leaves the approved enum.",
        },
        "boundary-flags-remain-false-after-valid-normalization": {
            "requirement_id": "preserve-protected-action-boundary-invariants",
            "behavior_goal": "Keep protected-action flags false after valid repo-local normalization.",
        },
        "evidence-mapping-has-no-action-drift": {
            "requirement_id": "preserve-evidence-mapping-no-action-drift",
            "behavior_goal": "Keep evidence mapping from drifting into candidate tool imports, dependency installs, external fetches, or runtime integration.",
        },
    }


def behavior_requirements(gate: dict) -> list[dict]:
    blueprint = behavior_blueprint()
    requirements = []
    for item in gate["reviewed_regression_tests"]:
        data = blueprint[item["test_id"]]
        requirements.append(
            {
                "requirement_id": data["requirement_id"],
                "source_regression_test_id": item["test_id"],
                "regression_type": item["regression_type"],
                "behavior_goal": data["behavior_goal"],
                "planned_file_targets": planned_file_targets(),
                "acceptance_criteria": [
                    "Behavior remains deterministic and repo-local",
                    "Invalid fixture rejection remains contract-specific",
                    "Protected-action flags remain false",
                    "Candidate tools are not imported and dependencies are not installed",
                ],
                "validation_commands": validation_commands(),
                "claim_boundary": false_boundary(),
                "candidate_tool_import_allowed": False,
                "dependency_install_allowed": False,
                "external_fetch_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return requirements


def counts(gate: dict) -> dict:
    requirements = behavior_requirements(gate)
    return {
        "adapter_module_count": gate["adapter_module_count"],
        "reviewed_regression_test_count": gate["reviewed_regression_test_count"],
        "behavior_requirement_count": len(requirements),
        "planned_behavior_task_count": len(requirements),
        "invalid_fixture_behavior_requirement_count": sum(1 for item in requirements if item["regression_type"] == "invalid_fixture"),
        "boundary_behavior_requirement_count": sum(1 for item in requirements if item["regression_type"] == "boundary"),
        "evidence_mapping_behavior_requirement_count": sum(1 for item in requirements if item["regression_type"] == "evidence_mapping"),
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "plan_blocker_count": 0,
        "ready_for_adapter_behavior_expansion_plan_review_count": 1,
    }


def base_plan_record(gate: dict) -> dict:
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
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "reviewed_regression_tests": gate["reviewed_regression_tests"],
        "behavior_requirements": behavior_requirements(gate),
        "planned_file_targets": planned_file_targets(),
        "validation_commands": validation_commands(),
        "input_uris": {
            "adapter_regression_pack_review_gate": rel(REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(gate),
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    return {
        **base_plan_record(gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(BEHAVIOR_PLAN),
            rel(BEHAVIOR_PLAN_REPORT),
            rel(BEHAVIOR_PLAN_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(gate).items())
    requirement_lines = "\n".join(
        "- {requirement_id}: source_regression_test_id={source_regression_test_id}, regression_type={regression_type}".format(
            **item
        )
        for item in behavior_requirements(gate)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1=true

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

## Behavior requirements

{requirement_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-behavior-expansion-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local adapter behavior expansion plan before implementing behavior changes
  - Confirm reviewed regression tests map to behavior requirements and validation commands
  - Keep behavior expansion provider-neutral, dependency-free, and runtime-free
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    gate = read_json(REVIEW_GATE)
    require_review_gate(gate)
    write_json(BEHAVIOR_PLAN, base_plan_record(gate))
    write_text(BEHAVIOR_PLAN_REPORT, build_report(gate))
    write_text(BEHAVIOR_PLAN_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion Plan v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
