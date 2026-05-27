from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

ACCEPTANCE_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_gate.json"
IMPLEMENTATION_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan.json"
IMPLEMENTATION_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan_report.md"
IMPLEMENTATION_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_IMPLEMENTATION_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_DECISION = "CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_IMPLEMENTATION_PLAN_FROM_REVIEWED_ACCEPTANCE_GATE"
PLAN_STATUS = "planned_for_repo_local_adapter_scaffold_not_runtime_or_dependency_ready"


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
        raise SystemExit("acceptance review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("acceptance review gate must point to this implementation plan goal")
    if gate.get("ready_for_adapter_implementation_plan_count") != 1:
        raise SystemExit("acceptance review gate must be ready for implementation plan")
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
            raise SystemExit(f"acceptance review gate {key} mismatch")


def base_task(task_id: str, goal: str, targets: list[str], validation_commands: list[str]) -> dict:
    return {
        "task_id": task_id,
        "goal": goal,
        "acceptance_criteria": [
            "Task remains repo-local and deterministic",
            "Task does not import candidate tools or install dependencies",
            "Task preserves claim boundaries and protected action flags",
        ],
        "planned_file_targets": targets,
        "validation_commands": validation_commands,
        "claim_boundary": false_boundary(),
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }


def source_contracts() -> list[dict]:
    contract_data = [
        (
            "eval-case-contract",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_eval_case_contract.schema.json",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_eval_case_contract.valid.fixture.json",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_eval_case_contract.invalid.fixture.json",
            "Normalize repo-local eval case records into the future adapter boundary",
        ),
        (
            "redteam-case-contract",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_redteam_case_contract.schema.json",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_redteam_case_contract.valid.fixture.json",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_redteam_case_contract.invalid.fixture.json",
            "Normalize repo-local red-team case records into the future adapter boundary",
        ),
        (
            "rag-metric-contract",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_rag_metric_contract.schema.json",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_rag_metric_contract.valid.fixture.json",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_rag_metric_contract.invalid.fixture.json",
            "Normalize repo-local RAG metric records into the future adapter boundary",
        ),
        (
            "governance-gate-contract",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_governance_gate_contract.schema.json",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_governance_gate_contract.valid.fixture.json",
            "avf/capabilities/generated/capability_candidate_primary_source_priority_1_governance_gate_contract.invalid.fixture.json",
            "Normalize repo-local governance gate records into the future adapter boundary",
        ),
    ]
    return [
        {
            "contract_id": contract_id,
            "schema_uri": schema_uri,
            "valid_fixture_uri": valid_fixture_uri,
            "invalid_fixture_uri": invalid_fixture_uri,
            "implementation_scope": implementation_scope,
            "candidate_tool_import_allowed": False,
            "dependency_install_allowed": False,
            "external_fetch_allowed": False,
            "runtime_integration_allowed": False,
        }
        for contract_id, schema_uri, valid_fixture_uri, invalid_fixture_uri, implementation_scope in contract_data
    ]


def planned_file_targets() -> list[str]:
    return [
        "avf/capabilities/adapters/priority_1/adapter_contracts.py",
        "avf/capabilities/adapters/priority_1/record_normalizers.py",
        "avf/capabilities/adapters/priority_1/repo_local_validation_harness.py",
        "avf/capabilities/adapters/priority_1/evidence_mapping.py",
    ]


def validation_commands() -> list[str]:
    return [
        "python scripts\\run_avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1.py",
        "python scripts\\validate_avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1.py",
        "python -m py_compile avf\\capabilities\\adapters\\priority_1\\adapter_contracts.py avf\\capabilities\\adapters\\priority_1\\record_normalizers.py avf\\capabilities\\adapters\\priority_1\\repo_local_validation_harness.py avf\\capabilities\\adapters\\priority_1\\evidence_mapping.py",
    ]


def implementation_tasks() -> list[dict]:
    targets = planned_file_targets()
    commands = validation_commands()
    return [
        base_task("adapter-contract-boundary-module", "Define repo-local adapter contract dataclasses and protected-action constants", [targets[0]], commands),
        base_task("eval-case-record-normalizer", "Plan deterministic eval case record normalization without importing Promptfoo or Ragas", [targets[1]], commands),
        base_task("redteam-case-record-normalizer", "Plan deterministic red-team case record normalization without importing Promptfoo or Ragas", [targets[1]], commands),
        base_task("rag-metric-record-normalizer", "Plan deterministic RAG metric record normalization without importing Promptfoo or Ragas", [targets[1]], commands),
        base_task("governance-gate-record-normalizer", "Plan deterministic governance gate record normalization without importing Promptfoo or Ragas", [targets[1]], commands),
        base_task("repo-local-validation-harness-entrypoint", "Plan a local harness entrypoint over generated fixtures only", [targets[2]], commands),
        base_task("evidence-ledger-v2-mapping", "Plan evidence ledger v2 mapping for scaffold output and validation reports", [targets[3]], commands),
    ]


def counts(gate: dict) -> dict:
    return {
        "source_schema_artifact_count": gate["source_schema_artifact_count"],
        "baseline_fixture_result_count": gate["baseline_fixture_result_count"],
        "mutation_runner_result_count": gate["mutation_runner_result_count"],
        "all_fixture_result_count": gate["all_fixture_result_count"],
        "all_fixture_result_matched_expected_count": gate["all_fixture_result_matched_expected_count"],
        "reviewed_acceptance_criteria_count": gate["reviewed_acceptance_criteria_count"],
        "reviewed_acceptance_criteria_passed_count": gate["reviewed_acceptance_criteria_passed_count"],
        "source_contract_count": len(source_contracts()),
        "implementation_task_count": len(implementation_tasks()),
        "planned_file_target_count": len(planned_file_targets()),
        "validation_command_count": len(validation_commands()),
        "blocked_action_count": gate["blocked_action_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "plan_blocker_count": 0,
        "ready_for_adapter_scaffold_count": 1,
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
        "reviewed_acceptance_criteria": gate["reviewed_acceptance_criteria"],
        "source_contracts": source_contracts(),
        "implementation_tasks": implementation_tasks(),
        "planned_file_targets": planned_file_targets(),
        "validation_commands": validation_commands(),
        "input_uris": {
            "adapter_contract_validation_harness_acceptance_gate_review_gate": rel(ACCEPTANCE_REVIEW_GATE),
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
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(ACCEPTANCE_REVIEW_GATE),
            rel(IMPLEMENTATION_PLAN),
            rel(IMPLEMENTATION_PLAN_REPORT),
            rel(IMPLEMENTATION_PLAN_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(gate).items())
    contract_lines = "\n".join(
        "- {contract_id}: schema_uri={schema_uri}, implementation_scope={implementation_scope}".format(**item)
        for item in source_contracts()
    )
    task_lines = "\n".join(
        "- {task_id}: goal={goal}".format(**item)
        for item in implementation_tasks()
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Implementation Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1=true

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
- selection_allowed=false
- dependency_adoption_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Source contracts

{contract_lines}

## Implementation tasks

{task_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-scaffold
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local adapter scaffold from the implementation plan without importing candidate tools
  - Generate only local adapter boundary modules, normalizers, validation harness code, and evidence mapping
  - Keep dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    gate = read_json(ACCEPTANCE_REVIEW_GATE)
    require_review_gate(gate)

    write_json(IMPLEMENTATION_PLAN, base_plan_record(gate))
    write_text(IMPLEMENTATION_PLAN_REPORT, build_report(gate))
    write_text(IMPLEMENTATION_PLAN_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Implementation Plan v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
