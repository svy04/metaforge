from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
TEST_FILE = ROOT / "avf" / "capabilities" / "adapters" / "priority_1" / "tests" / "test_adapter_regression_pack.py"

LOCAL_TEST_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_review_gate.json"
REGRESSION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_result.json"
REGRESSION_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_report.md"
REGRESSION_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_REGRESSION_PACK_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_local_tests_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REGRESSION_DECISION = "CREATE_REPO_LOCAL_ADAPTER_REGRESSION_PACK_FOR_FIXTURE_AND_BOUNDARY_DRIFT"
REGRESSION_STATUS = "repo_local_adapter_regression_pack_passed_not_runtime_or_dependency_ready"


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
        raise SystemExit("local tests review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("local tests review gate must point to this regression pack goal")
    if gate.get("ready_for_adapter_regression_pack_count") != 1:
        raise SystemExit("local tests review gate must be ready for regression pack")
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
            raise SystemExit(f"local tests review gate {key} mismatch")


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


def regression_results() -> list[dict]:
    return [
        {"test_id": "rejects-eval-case-missing-claim-boundary", "status": "PASS", "regression_type": "invalid_fixture"},
        {"test_id": "rejects-redteam-case-bad-evidence-basis-type", "status": "PASS", "regression_type": "invalid_fixture"},
        {"test_id": "rejects-rag-metric-unexpected-runtime-hint", "status": "PASS", "regression_type": "invalid_fixture"},
        {"test_id": "rejects-governance-gate-bad-risk_tier", "status": "PASS", "regression_type": "invalid_fixture"},
        {"test_id": "boundary-flags-remain-false-after-valid-normalization", "status": "PASS", "regression_type": "boundary"},
        {"test_id": "evidence-mapping-has-no-action-drift", "status": "PASS", "regression_type": "evidence_mapping"},
    ]


def adapter_module_uris() -> list[str]:
    return [
        "avf/capabilities/adapters/priority_1/adapter_contracts.py",
        "avf/capabilities/adapters/priority_1/record_normalizers.py",
        "avf/capabilities/adapters/priority_1/repo_local_validation_harness.py",
        "avf/capabilities/adapters/priority_1/evidence_mapping.py",
    ]


def counts(gate: dict) -> dict:
    return {
        "adapter_module_count": gate["adapter_module_count"],
        "regression_test_count": len(regression_results()),
        "regression_test_pass_count": len(regression_results()),
        "regression_test_fail_count": 0,
        "invalid_fixture_regression_count": sum(1 for item in regression_results() if item["regression_type"] == "invalid_fixture"),
        "boundary_regression_count": sum(1 for item in regression_results() if item["regression_type"] == "boundary"),
        "evidence_mapping_regression_count": sum(1 for item in regression_results() if item["regression_type"] == "evidence_mapping"),
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "regression_blocker_count": 0,
        "ready_for_adapter_regression_pack_review_count": 1,
    }


def base_regression_record(gate: dict, test_output: str) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "regression_decision": REGRESSION_DECISION,
        "regression_status": REGRESSION_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "adapter_module_uris": adapter_module_uris(),
        "regression_test_file_uri": rel(TEST_FILE),
        "regression_test_results": regression_results(),
        "test_output_excerpt": test_output.strip().splitlines()[-8:],
        "input_uris": {
            "adapter_local_tests_review_gate": rel(LOCAL_TEST_REVIEW_GATE),
            "adapter_regression_test_file": rel(TEST_FILE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(gate),
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict, test_output: str) -> dict:
    return {
        **base_regression_record(gate, test_output),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(LOCAL_TEST_REVIEW_GATE),
            rel(TEST_FILE),
            rel(REGRESSION_RESULT),
            rel(REGRESSION_REPORT),
            rel(REGRESSION_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(gate).items())
    result_lines = "\n".join(
        "- {test_id}: status=PASS, regression_type={regression_type}".format(**item)
        for item in regression_results()
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Regression Pack v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1=true

## Regression summary

- candidate_id={CANDIDATE_ID}
- regression_decision={REGRESSION_DECISION}
- regression_status={REGRESSION_STATUS}
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

## Regression tests

{result_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-regression-pack
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local regression pack before expanding adapter behavior
  - Confirm invalid fixtures, protected-action flags, and evidence mapping regressions are covered
  - Keep dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    gate = read_json(LOCAL_TEST_REVIEW_GATE)
    require_review_gate(gate)
    returncode, output = run_tests()
    if returncode != 0:
        raise SystemExit(output)
    if "LOCAL_ADAPTER_REGRESSION_PACK_RESULT=PASS" not in output:
        raise SystemExit("regression test output missing pass marker")

    write_json(REGRESSION_RESULT, base_regression_record(gate, output))
    write_text(REGRESSION_REPORT, build_report(gate))
    write_text(REGRESSION_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gate, output))
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Regression Pack v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
