from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1.py"
BASELINE_RUNNER_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_gate.json"
MUTATION_RUNNER_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_gate.json"
MUTATION_RUNNER_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_next_action.yml"
ACCEPTANCE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate.json"
ACCEPTANCE_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_report.md"
ACCEPTANCE_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_ACCEPTANCE_GATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
ACCEPTANCE_DECISION = "ACCEPT_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_FOR_FUTURE_IMPLEMENTATION_PLAN"
ACCEPTANCE_STATUS = "accepted_as_repo_local_contract_harness_not_runtime_or_production_ready"

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "baseline_fixture_result_count": 8,
    "baseline_fixture_result_matched_expected_count": 8,
    "baseline_passing_fixture_count": 4,
    "baseline_failing_fixture_count": 4,
    "mutation_runner_result_count": 5,
    "reviewed_mutation_runner_result_count": 5,
    "mutation_fixture_result_matched_expected_count": 5,
    "all_fixture_result_count": 13,
    "all_fixture_result_matched_expected_count": 13,
    "all_passing_fixture_count": 4,
    "all_failing_fixture_count": 9,
    "schema_boundary_mutation_count": 4,
    "malformed_fixture_record_count": 1,
    "acceptance_criteria_count": 6,
    "acceptance_criteria_passed_count": 6,
    "blocked_action_count": 10,
    "reviewed_blocked_action_count": 10,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "acceptance_blocker_count": 0,
    "ready_for_adapter_contract_validation_harness_acceptance_gate_review_count": 1,
}

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "automated_scraping_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "runtime_export_performed",
    "collector_started",
    "telemetry_export_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    BASELINE_RUNNER_GATE,
    MUTATION_RUNNER_REVIEW_GATE,
    MUTATION_RUNNER_REVIEW_NEXT_ACTION,
    ACCEPTANCE_GATE,
    ACCEPTANCE_REPORT,
    ACCEPTANCE_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"acceptance_decision={ACCEPTANCE_DECISION}",
    f"acceptance_status={ACCEPTANCE_STATUS}",
    "baseline_fixture_result_count=8",
    "mutation_runner_result_count=5",
    "all_fixture_result_count=13",
    "all_fixture_result_matched_expected_count=13",
    "acceptance_criteria_count=6",
    "acceptance_criteria_passed_count=6",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "provider_neutral=true",
    "dependency_free=true",
    "candidate_tool_import_allowed=false",
    "dependency_install_allowed=false",
    "external_fetch_allowed=false",
    "runtime_integration_allowed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-acceptance-gate",
    "owner_approval_required_before_execution: false",
    "Review the repo-local acceptance gate before creating any future adapter implementation plan",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Acceptance Gate v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_inputs() -> tuple[dict, dict]:
    baseline = read_json(BASELINE_RUNNER_GATE)
    mutation = read_json(MUTATION_RUNNER_REVIEW_GATE)
    if baseline.get("goal_id") != "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1":
        fail("baseline runner gate goal_id mismatch")
    if baseline.get("fixture_validation_result_matched_expected_count") != 8:
        fail("baseline runner gate must have 8 matched fixture results")
    if mutation.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("mutation runner review gate goal_id mismatch")
    if mutation.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("mutation runner review gate must point to this acceptance gate goal")
    if mutation.get("ready_for_adapter_contract_validation_harness_acceptance_gate_count") != 1:
        fail("mutation runner review gate must be ready for acceptance gate")
    if mutation.get("mutation_fixture_result_matched_expected_count") != 5:
        fail("mutation runner review gate must have 5 matched mutation results")
    for record, label in [(baseline, "baseline runner gate"), (mutation, "mutation runner review gate")]:
        for key, value in {
            "provider_neutral": True,
            "dependency_free": True,
            "candidate_tool_import_allowed": False,
            "dependency_install_allowed": False,
            "external_fetch_allowed": False,
            "runtime_integration_allowed": False,
        }.items():
            if record.get(key) != value:
                fail(f"{label} {key} mismatch")
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        MUTATION_RUNNER_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-acceptance-gate",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return baseline, mutation


def require_acceptance_criterion(item: dict) -> None:
    for key in ["criterion_id", "evidence_basis", "status", "claim_boundary"]:
        if not item.get(key):
            fail(f"acceptance criterion missing {key}")
    if item.get("status") != "PASS":
        fail(f"acceptance criterion {item.get('criterion_id')} must pass")
    if item.get("candidate_tool_import_allowed") is not False:
        fail(f"acceptance criterion {item.get('criterion_id')} must block candidate tool import")
    if item.get("dependency_install_allowed") is not False:
        fail(f"acceptance criterion {item.get('criterion_id')} must block dependency install")
    if item.get("external_fetch_allowed") is not False:
        fail(f"acceptance criterion {item.get('criterion_id')} must block external fetch")
    if item.get("runtime_integration_allowed") is not False:
        fail(f"acceptance criterion {item.get('criterion_id')} must block runtime integration")


def require_acceptance_record(record: dict, label: str, baseline: dict, mutation: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_status": ACCEPTANCE_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("baseline_adapter_contract_validation_harness_runner_gate") != BASELINE_RUNNER_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} baseline runner input uri mismatch")
    if input_uris.get("adapter_contract_validation_harness_fixture_mutation_runner_review_gate") != MUTATION_RUNNER_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} mutation runner review input uri mismatch")
    if record.get("baseline_fixture_validation_results") != baseline.get("fixture_validation_results"):
        fail(f"{label} baseline fixture results mismatch")
    if record.get("reviewed_mutation_runner_results") != mutation.get("reviewed_mutation_runner_results"):
        fail(f"{label} reviewed mutation runner results mismatch")
    if record.get("reviewed_blocked_actions") != mutation.get("reviewed_blocked_actions"):
        fail(f"{label} reviewed blocked actions mismatch")
    criteria = record.get("acceptance_criteria", [])
    if len(criteria) != EXPECTED_COUNTS["acceptance_criteria_count"]:
        fail(f"{label} acceptance criteria count mismatch")
    for item in criteria:
        require_acceptance_criterion(item)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(baseline: dict, mutation: dict) -> None:
    gate = read_json(ACCEPTANCE_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-acceptance-gate-v0-1":
        fail("acceptance gate id mismatch")
    if gate.get("status") != "PASS":
        fail("acceptance gate status must be PASS")
    require_acceptance_record(gate, "acceptance gate", baseline, mutation)


def require_validation_result(baseline: dict, mutation: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_acceptance_record(result, "validation result", baseline, mutation)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    baseline, mutation = require_inputs()
    require_acceptance_record(read_json(ACCEPTANCE_GATE), "acceptance gate record", baseline, mutation)
    require_gate(baseline, mutation)
    require_text_markers(ACCEPTANCE_REPORT, REPORT_MARKERS)
    require_text_markers(ACCEPTANCE_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(baseline, mutation)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Acceptance Gate v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"acceptance_decision={ACCEPTANCE_DECISION}")
    print(f"acceptance_status={ACCEPTANCE_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("provider_neutral=true")
    print("dependency_free=true")
    print("candidate_tool_import_allowed=false")
    print("dependency_install_allowed=false")
    print("external_fetch_allowed=false")
    print("runtime_integration_allowed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
