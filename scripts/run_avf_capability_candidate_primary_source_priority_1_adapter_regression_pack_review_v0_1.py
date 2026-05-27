from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_regression_pack.py"

REGRESSION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_result.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_REGRESSION_PACK_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_plan_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_REGRESSION_PACK_REVIEWED"
REVIEW_STATUS = "adapter_regression_pack_reviewed_ready_for_behavior_expansion_plan"


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


def require_regression_result(source: dict) -> None:
    expected = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "regression_test_count": 6,
        "regression_test_pass_count": 6,
        "regression_test_fail_count": 0,
        "regression_blocker_count": 0,
        "ready_for_adapter_regression_pack_review_count": 1,
    }
    for key, value in expected.items():
        if source.get(key) != value:
            raise SystemExit(f"regression result {key} mismatch")


def run_tests() -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(TEST_FILE)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode, result.stdout


def reviewed_regression_tests(source: dict) -> list[dict]:
    reviewed = []
    for item in source["regression_test_results"]:
        reviewed.append(
            {
                "test_id": item["test_id"],
                "regression_type": item["regression_type"],
                "source_status": item["status"],
                "review_status": "reviewed_regression_test_preserves_repo_local_boundary",
                "candidate_tool_import_allowed": False,
                "dependency_install_allowed": False,
                "external_fetch_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return reviewed


def counts(source: dict) -> dict:
    return {
        "adapter_module_count": source["adapter_module_count"],
        "regression_test_count": source["regression_test_count"],
        "regression_test_pass_count": source["regression_test_pass_count"],
        "regression_test_fail_count": source["regression_test_fail_count"],
        "reviewed_regression_test_count": len(reviewed_regression_tests(source)),
        "invalid_fixture_regression_count": source["invalid_fixture_regression_count"],
        "boundary_regression_count": source["boundary_regression_count"],
        "evidence_mapping_regression_count": source["evidence_mapping_regression_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "regression_blocker_count": source["regression_blocker_count"],
        "review_blocker_count": 0,
        "ready_for_adapter_regression_pack_review_count": source["ready_for_adapter_regression_pack_review_count"],
        "ready_for_adapter_behavior_expansion_plan_count": 1,
    }


def base_review_record(source: dict, test_output: str) -> dict:
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
        "adapter_module_uris": source["adapter_module_uris"],
        "regression_test_file_uri": source["regression_test_file_uri"],
        "regression_test_results": source["regression_test_results"],
        "reviewed_regression_tests": reviewed_regression_tests(source),
        "test_output_excerpt": test_output.strip().splitlines()[-8:],
        "input_uris": {
            "adapter_regression_pack_result": rel(REGRESSION_RESULT),
            "adapter_regression_test_file": rel(TEST_FILE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(source),
        "claim_boundary": false_boundary(),
    }


def build_validation_result(source: dict, test_output: str) -> dict:
    return {
        **base_review_record(source, test_output),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REGRESSION_RESULT),
            rel(TEST_FILE),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(REVIEW_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(source: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(source).items())
    result_lines = "\n".join(
        "- {test_id}: source_status={status}, review_status=reviewed_regression_test_preserves_repo_local_boundary, regression_type={regression_type}".format(
            **item
        )
        for item in source["regression_test_results"]
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Regression Pack Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1=true

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

## Reviewed regression tests

{result_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-behavior-expansion-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local adapter behavior expansion plan after regression review
  - Map reviewed invalid-fixture, boundary, and evidence-mapping regressions to behavior expansion requirements
  - Keep behavior expansion plan provider-neutral, dependency-free, and runtime-free
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    source = read_json(REGRESSION_RESULT)
    require_regression_result(source)
    returncode, output = run_tests()
    if returncode != 0:
        raise SystemExit(output)
    if "LOCAL_ADAPTER_REGRESSION_PACK_RESULT=PASS" not in output:
        raise SystemExit("regression test output missing pass marker")

    write_json(REVIEW_GATE, base_review_record(source, output))
    write_text(REVIEW_REPORT, build_report(source))
    write_text(REVIEW_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(source, output))
    write_text(VALIDATION_REPORT, build_report(source))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Regression Pack Review v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
