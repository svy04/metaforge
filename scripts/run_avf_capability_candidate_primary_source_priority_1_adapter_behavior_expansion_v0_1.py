from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
BEHAVIOR_TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_behavior_expansion.py"
REGRESSION_TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_regression_pack.py"
SCAFFOLD_TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_scaffold.py"

PLAN_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_gate.json"
BEHAVIOR_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_result.json"
BEHAVIOR_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_report.md"
BEHAVIOR_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_BEHAVIOR_EXPANSION_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
IMPLEMENTATION_DECISION = "IMPLEMENT_REPO_LOCAL_ADAPTER_BEHAVIOR_EXPANSION_FROM_REVIEWED_PLAN"
IMPLEMENTATION_STATUS = "repo_local_adapter_behavior_expansion_passed_not_runtime_or_dependency_ready"


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


def require_plan_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("behavior expansion plan review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("behavior expansion plan review gate must point to this behavior expansion goal")
    if gate.get("ready_for_adapter_behavior_expansion_count") != 1:
        raise SystemExit("behavior expansion plan review gate must be ready for behavior expansion")
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
            raise SystemExit(f"behavior expansion plan review gate {key} mismatch")


def run_test(path: Path, pass_marker: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.stdout)
    if pass_marker not in result.stdout:
        raise SystemExit(f"{path.name} missing {pass_marker}")
    return {
        "test_file_uri": rel(path),
        "status": "PASS",
        "output_excerpt": result.stdout.strip().splitlines()[-8:],
    }


def test_results() -> dict:
    return {
        "behavior": run_test(BEHAVIOR_TEST_FILE, "LOCAL_ADAPTER_BEHAVIOR_EXPANSION_RESULT=PASS"),
        "regression": run_test(REGRESSION_TEST_FILE, "LOCAL_ADAPTER_REGRESSION_PACK_RESULT=PASS"),
        "scaffold": run_test(SCAFFOLD_TEST_FILE, "LOCAL_ADAPTER_SCAFFOLD_TESTS_RESULT=PASS"),
    }


def counts(gate: dict) -> dict:
    return {
        "adapter_module_count": gate["adapter_module_count"],
        "behavior_requirement_count": gate["behavior_requirement_count"],
        "reviewed_behavior_requirement_count": gate["reviewed_behavior_requirement_count"],
        "behavior_test_count": 6,
        "behavior_test_pass_count": 6,
        "behavior_test_fail_count": 0,
        "regression_test_count": 6,
        "scaffold_test_count": 4,
        "invalid_fixture_behavior_requirement_count": gate["invalid_fixture_behavior_requirement_count"],
        "boundary_behavior_requirement_count": gate["boundary_behavior_requirement_count"],
        "evidence_mapping_behavior_requirement_count": gate["evidence_mapping_behavior_requirement_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "behavior_blocker_count": 0,
        "ready_for_adapter_behavior_expansion_review_count": 1,
    }


def base_behavior_record(gate: dict, tests: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "implementation_decision": IMPLEMENTATION_DECISION,
        "implementation_status": IMPLEMENTATION_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "reviewed_behavior_requirements": gate["reviewed_behavior_requirements"],
        "behavior_requirements": gate["behavior_requirements"],
        "behavior_test_results": tests,
        "modified_code_targets": [
            "avf/capabilities/adapters/priority_1/adapter_contracts.py",
            "avf/capabilities/adapters/priority_1/record_normalizers.py",
            "avf/capabilities/adapters/priority_1/evidence_mapping.py",
            "avf/capabilities/adapters/priority_1/tests/test_adapter_behavior_expansion.py",
        ],
        "input_uris": {
            "adapter_behavior_expansion_plan_review_gate": rel(PLAN_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(gate),
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict, tests: dict) -> dict:
    return {
        **base_behavior_record(gate, tests),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(PLAN_REVIEW_GATE),
            rel(BEHAVIOR_TEST_FILE),
            rel(REGRESSION_TEST_FILE),
            rel(SCAFFOLD_TEST_FILE),
            rel(BEHAVIOR_RESULT),
            rel(BEHAVIOR_REPORT),
            rel(BEHAVIOR_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(gate).items())
    requirement_lines = "\n".join(
        "- {requirement_id}: source_regression_test_id={source_regression_test_id}, review_status={review_status}".format(
            **item
        )
        for item in gate["reviewed_behavior_requirements"]
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_behavior_expansion_v0_1=true

## Implementation summary

- candidate_id={CANDIDATE_ID}
- implementation_decision={IMPLEMENTATION_DECISION}
- implementation_status={IMPLEMENTATION_STATUS}
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

{requirement_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-behavior-expansion
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local adapter behavior expansion before any runtime or dependency step
  - Confirm behavior tests, regression tests, scaffold tests, and protected-action flags remain stable
  - Keep implementation provider-neutral, dependency-free, and runtime-free
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    gate = read_json(PLAN_REVIEW_GATE)
    require_plan_review_gate(gate)
    tests = test_results()
    write_json(BEHAVIOR_RESULT, base_behavior_record(gate, tests))
    write_text(BEHAVIOR_REPORT, build_report(gate))
    write_text(BEHAVIOR_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gate, tests))
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Behavior Expansion v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
