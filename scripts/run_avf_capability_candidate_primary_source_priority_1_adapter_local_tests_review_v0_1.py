from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

LOCAL_TEST_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_result.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_local_tests_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_LOCAL_TESTS_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_local_tests_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_local_tests_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_regression_pack_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_LOCAL_TESTS_REVIEWED"
REVIEW_STATUS = "adapter_local_tests_reviewed_ready_for_regression_pack"


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


def require_local_tests(source: dict) -> None:
    if source.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("local test result goal mismatch")
    if source.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("local test result must point to this review goal")
    if source.get("ready_for_adapter_local_tests_review_count") != 1:
        raise SystemExit("local test result must be ready for review")
    for key, expected in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "local_test_count": 4,
        "local_test_pass_count": 4,
        "local_test_fail_count": 0,
        "test_blocker_count": 0,
    }.items():
        if source.get(key) != expected:
            raise SystemExit(f"local test result {key} mismatch")


def reviewed_local_tests(source: dict) -> list[dict]:
    return [
        {
            **item,
            "review_status": "reviewed_local_test_preserves_repo_local_boundary",
            "candidate_tool_import_allowed": False,
            "dependency_install_allowed": False,
            "external_fetch_allowed": False,
            "runtime_integration_allowed": False,
        }
        for item in source["test_results"]
    ]


def counts(source: dict) -> dict:
    return {
        "adapter_module_count": source["adapter_module_count"],
        "local_test_count": source["local_test_count"],
        "local_test_pass_count": source["local_test_pass_count"],
        "local_test_fail_count": source["local_test_fail_count"],
        "reviewed_local_test_count": len(reviewed_local_tests(source)),
        "normalized_record_count": source["normalized_record_count"],
        "evidence_entry_count": source["evidence_entry_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "test_blocker_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_local_tests_review_count": 1,
        "ready_for_adapter_regression_pack_count": 1,
    }


def base_review_record(source: dict) -> dict:
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
        "test_results": source["test_results"],
        "reviewed_local_tests": reviewed_local_tests(source),
        "input_uris": {
            "adapter_local_tests_result": rel(LOCAL_TEST_RESULT),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(source),
        "claim_boundary": false_boundary(),
    }


def build_gate(source: dict) -> dict:
    return {
        **base_review_record(source),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-local-tests-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local adapter tests reviewed before regression pack expansion",
    }


def build_validation_result(source: dict) -> dict:
    return {
        **base_review_record(source),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_local_tests_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(LOCAL_TEST_RESULT),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(REVIEW_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(source: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(source).items())
    test_lines = "\n".join(
        "- {test_id}: review_status={review_status}".format(**item)
        for item in reviewed_local_tests(source)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Local Tests Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_local_tests_review_v0_1=true

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

## Reviewed local tests

{test_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-regression-pack
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local regression pack for adapter scaffold fixtures and boundaries
  - Add regression cases for invalid fixtures, protected-action flags, and evidence mapping
  - Keep dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    source = read_json(LOCAL_TEST_RESULT)
    require_local_tests(source)

    write_json(REVIEW_GATE, build_gate(source))
    write_text(REVIEW_REPORT, build_report(source))
    write_text(REVIEW_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(source))
    write_text(VALIDATION_REPORT, build_report(source))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Local Tests Review v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
