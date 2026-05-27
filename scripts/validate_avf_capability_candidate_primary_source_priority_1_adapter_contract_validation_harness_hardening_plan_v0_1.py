from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1.py"
RUNNER_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_review_gate.json"
RUNNER_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_review_next_action.yml"
HARDENING_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_gate.json"
HARDENING_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_report.md"
HARDENING_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_HARDENING_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PLAN_DECISION = "CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_HARDENING_PLAN"
PLAN_STATUS = "adapter_contract_validation_harness_hardening_plan_created_ready_for_fixture_mutation_pack"

HARDENING_AREAS = {
    "missing-required-field-coverage",
    "type-mismatch-coverage",
    "enum-mismatch-coverage",
    "additional-property-coverage",
    "malformed-fixture-record-coverage",
}

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "reviewed_validation_fixture_count": 8,
    "reviewed_fixture_validation_result_count": 8,
    "existing_passing_fixture_count": 4,
    "existing_failing_fixture_count": 4,
    "reviewed_failure_reason_count": 4,
    "hardening_area_count": 5,
    "fixture_mutation_plan_count": 5,
    "blocked_action_count": 10,
    "reviewed_blocked_action_count": 10,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_contract_validation_harness_fixture_mutation_pack_count": 1,
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
    RUNNER_REVIEW_GATE,
    RUNNER_REVIEW_NEXT_ACTION,
    HARDENING_PLAN_GATE,
    HARDENING_PLAN_REPORT,
    HARDENING_PLAN_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"plan_decision={PLAN_DECISION}",
    f"plan_status={PLAN_STATUS}",
    "hardening_area_count=5",
    "fixture_mutation_plan_count=5",
    "reviewed_failure_reason_count=4",
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
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-pack",
    "owner_approval_required_before_execution: false",
    "Create repo-local mutation fixtures that prove the harness fails when schema boundaries are violated",
    "Keep candidate tool imports, dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Hardening Plan v0.1 validation")
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


def require_previous_review() -> dict:
    review = read_json(RUNNER_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("adapter contract validation harness runner review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("adapter contract validation harness runner review gate must point to this hardening plan goal")
    if review.get("ready_for_adapter_contract_validation_harness_hardening_plan_count") != 1:
        fail("adapter contract validation harness runner review must be ready for hardening plan")
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "review_blocker_count": 0,
    }.items():
        if review.get(key) != value:
            fail(f"adapter contract validation harness runner review {key} mismatch")
    if len(review.get("reviewed_fixture_validation_results", [])) != 8:
        fail("adapter contract validation harness runner review must include 8 reviewed fixture results")
    failing = [item for item in review["reviewed_fixture_validation_results"] if item.get("actual_valid") is False]
    if len(failing) != EXPECTED_COUNTS["existing_failing_fixture_count"]:
        fail("adapter contract validation harness runner review failing fixture count mismatch")
    require_false_flags(review.get("claim_boundary", {}), "adapter contract validation harness runner review claim boundary")
    require_text_markers(
        RUNNER_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-hardening-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_hardening_area(area: dict) -> None:
    area_id = area.get("area_id")
    if area_id not in HARDENING_AREAS:
        fail(f"unknown hardening area {area_id}")
    for key in [
        "reason",
        "current_coverage",
        "proposed_negative_fixture_family",
        "validator_expectation",
    ]:
        if not area.get(key):
            fail(f"hardening area {area_id} missing {key}")
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if area.get(key) != value:
            fail(f"hardening area {area_id} {key} mismatch")


def require_mutation_plan(item: dict) -> None:
    area_id = item.get("area_id")
    if area_id not in HARDENING_AREAS:
        fail(f"fixture mutation plan unknown area {area_id}")
    for key in [
        "mutation_family_id",
        "target_schema_id",
        "expected_result",
        "expected_failure_reason_prefix",
        "next_fixture_status",
    ]:
        if not item.get(key):
            fail(f"fixture mutation plan {area_id} missing {key}")
    if item.get("expected_result") != "invalid":
        fail(f"fixture mutation plan {area_id} must expect invalid")
    for key, value in {
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if item.get(key) != value:
            fail(f"fixture mutation plan {area_id} {key} mismatch")


def require_plan_record(record: dict, label: str, review: dict) -> None:
    expected = {
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
    if input_uris.get("adapter_contract_validation_harness_runner_review_gate") != RUNNER_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input runner review gate uri mismatch")
    if record.get("reviewed_blocked_actions") != review.get("reviewed_blocked_actions"):
        fail(f"{label} reviewed blocked actions mismatch")
    areas = record.get("hardening_areas", [])
    if {area.get("area_id") for area in areas} != HARDENING_AREAS:
        fail(f"{label} hardening area ids mismatch")
    for area in areas:
        require_hardening_area(area)
    mutation_plan = record.get("fixture_mutation_plan", [])
    if {item.get("area_id") for item in mutation_plan} != HARDENING_AREAS:
        fail(f"{label} fixture mutation plan ids mismatch")
    for item in mutation_plan:
        require_mutation_plan(item)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(review: dict) -> None:
    gate = read_json(HARDENING_PLAN_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-hardening-plan-gate-v0-1":
        fail("adapter contract validation harness hardening plan gate id mismatch")
    if gate.get("status") != "PASS":
        fail("adapter contract validation harness hardening plan gate status must be PASS")
    require_plan_record(gate, "adapter contract validation harness hardening plan gate", review)


def require_validation_result(review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_plan_record(result, "validation result", review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review = require_previous_review()
    require_plan_record(read_json(HARDENING_PLAN_GATE), "adapter contract validation harness hardening plan", review)
    require_gate(review)
    require_text_markers(HARDENING_PLAN_REPORT, REPORT_MARKERS)
    require_text_markers(HARDENING_PLAN_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Hardening Plan v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_hardening_plan_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_status={PLAN_STATUS}")
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
