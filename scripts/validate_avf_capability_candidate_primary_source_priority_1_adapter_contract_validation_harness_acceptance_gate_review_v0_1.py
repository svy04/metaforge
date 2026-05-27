from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1.py"
ACCEPTANCE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate.json"
ACCEPTANCE_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_ACCEPTANCE_GATE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
ACCEPTANCE_DECISION = "ACCEPT_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_FOR_FUTURE_IMPLEMENTATION_PLAN"
ACCEPTANCE_STATUS = "accepted_as_repo_local_contract_harness_not_runtime_or_production_ready"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_ACCEPTANCE_GATE_REVIEWED"
REVIEW_STATUS = "adapter_contract_validation_harness_acceptance_gate_reviewed_ready_for_future_adapter_implementation_plan"

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
    "reviewed_acceptance_criteria_count": 6,
    "reviewed_acceptance_criteria_passed_count": 6,
    "review_blocker_count": 0,
    "ready_for_adapter_implementation_plan_count": 1,
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
    ACCEPTANCE_GATE,
    ACCEPTANCE_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    REVIEW_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    f"acceptance_decision={ACCEPTANCE_DECISION}",
    f"acceptance_status={ACCEPTANCE_STATUS}",
    "all_fixture_result_count=13",
    "all_fixture_result_matched_expected_count=13",
    "acceptance_criteria_count=6",
    "acceptance_criteria_passed_count=6",
    "reviewed_acceptance_criteria_count=6",
    "reviewed_acceptance_criteria_passed_count=6",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "review_blocker_count=0",
    "ready_for_adapter_implementation_plan_count=1",
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
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-implementation-plan",
    "owner_approval_required_before_execution: false",
    "Create a repo-local no-install adapter implementation plan from the reviewed acceptance gate",
    "Do not install dependencies, clone OSS, import candidate tools, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Acceptance Gate Review v0.1 validation")
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


def require_previous_acceptance_gate() -> dict:
    gate = read_json(ACCEPTANCE_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("acceptance gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("acceptance gate must point to this review goal")
    if gate.get("ready_for_adapter_contract_validation_harness_acceptance_gate_review_count") != 1:
        fail("acceptance gate must be ready for review")
    for key, value in {
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
        "acceptance_blocker_count": 0,
    }.items():
        if gate.get(key) != value:
            fail(f"acceptance gate {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if key.startswith("reviewed_") or key in {"review_blocker_count", "ready_for_adapter_implementation_plan_count"}:
            continue
        if gate.get(key) != value:
            fail(f"acceptance gate {key} mismatch")
    criteria = gate.get("acceptance_criteria", [])
    if len(criteria) != EXPECTED_COUNTS["acceptance_criteria_count"]:
        fail("acceptance gate criteria count mismatch")
    for criterion in criteria:
        if criterion.get("status") != "PASS":
            fail(f"acceptance criterion {criterion.get('criterion_id')} must pass")
        for key in ["candidate_tool_import_allowed", "dependency_install_allowed", "external_fetch_allowed", "runtime_integration_allowed"]:
            if criterion.get(key) is not False:
                fail(f"acceptance criterion {criterion.get('criterion_id')} must keep {key}=false")
    require_false_flags(gate.get("claim_boundary", {}), "acceptance gate claim boundary")
    require_text_markers(
        ACCEPTANCE_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-acceptance-gate",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_reviewed_criterion(item: dict, source_by_id: dict[str, dict]) -> None:
    criterion_id = item.get("criterion_id", "<missing>")
    if criterion_id not in source_by_id:
        fail(f"reviewed acceptance criterion {criterion_id} missing matching source criterion")
    source = source_by_id[criterion_id]
    for key, value in source.items():
        if item.get(key) != value:
            fail(f"reviewed acceptance criterion {criterion_id} changed source field {key}")
    if item.get("review_status") != "reviewed_acceptance_criterion_matches_gate_outcome":
        fail(f"reviewed acceptance criterion {criterion_id} review_status mismatch")
    if item.get("acceptance_criterion_contract_validated") is not True:
        fail(f"reviewed acceptance criterion {criterion_id} contract validation flag mismatch")


def require_review_record(record: dict, label: str, gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_status": ACCEPTANCE_STATUS,
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
    if input_uris.get("adapter_contract_validation_harness_acceptance_gate") != ACCEPTANCE_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} acceptance gate input uri mismatch")
    if record.get("baseline_fixture_validation_results") != gate.get("baseline_fixture_validation_results"):
        fail(f"{label} baseline fixture results mismatch")
    if record.get("reviewed_mutation_runner_results") != gate.get("reviewed_mutation_runner_results"):
        fail(f"{label} reviewed mutation runner results mismatch")
    if record.get("reviewed_blocked_actions") != gate.get("reviewed_blocked_actions"):
        fail(f"{label} reviewed blocked actions mismatch")
    reviewed_criteria = record.get("reviewed_acceptance_criteria", [])
    if len(reviewed_criteria) != EXPECTED_COUNTS["reviewed_acceptance_criteria_count"]:
        fail(f"{label} reviewed acceptance criteria count mismatch")
    source_by_id = {item["criterion_id"]: item for item in gate.get("acceptance_criteria", [])}
    for item in reviewed_criteria:
        require_reviewed_criterion(item, source_by_id)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(gate: dict) -> None:
    review_gate = read_json(REVIEW_GATE)
    if review_gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-acceptance-gate-review-gate-v0-1":
        fail("review gate id mismatch")
    if review_gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(review_gate, "review gate", gate)


def require_validation_result(gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    gate = require_previous_acceptance_gate()
    require_review_record(read_json(REVIEW_GATE), "review gate record", gate)
    require_gate(gate)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(REVIEW_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Acceptance Gate Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
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
