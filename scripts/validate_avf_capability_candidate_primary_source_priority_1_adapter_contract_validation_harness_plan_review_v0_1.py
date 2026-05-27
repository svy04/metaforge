from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1.py"
HARNESS_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_gate.json"
HARNESS_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_runner_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_PLAN_REVIEWED"
REVIEW_STATUS = "adapter_contract_validation_harness_plan_validated_ready_for_no_install_runner"

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "reviewed_validation_fixture_count": 8,
    "harness_responsibility_count": 6,
    "reviewed_harness_responsibility_count": 6,
    "planned_harness_step_count": 6,
    "reviewed_planned_harness_step_count": 6,
    "input_contract_count": 2,
    "output_contract_count": 2,
    "blocked_action_count": 10,
    "reviewed_blocked_action_count": 10,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_contract_validation_harness_runner_count": 1,
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
    HARNESS_PLAN_GATE,
    HARNESS_PLAN_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    REVIEW_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "source_schema_artifact_count=4",
    "reviewed_validation_fixture_count=8",
    "harness_responsibility_count=6",
    "reviewed_harness_responsibility_count=6",
    "planned_harness_step_count=6",
    "reviewed_planned_harness_step_count=6",
    "input_contract_count=2",
    "output_contract_count=2",
    "blocked_action_count=10",
    "reviewed_blocked_action_count=10",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "review_blocker_count=0",
    "ready_for_adapter_contract_validation_harness_runner_count=1",
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
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-runner",
    "owner_approval_required_before_execution: false",
    "Create the repo-local no-install adapter contract validation harness runner",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Plan Review v0.1 validation")
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


def require_previous_harness_plan() -> dict:
    plan = read_json(HARNESS_PLAN_GATE)
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("adapter contract validation harness plan gate goal_id mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("adapter contract validation harness plan gate must point to this review goal")
    if plan.get("ready_for_adapter_contract_validation_harness_plan_review_count") != 1:
        fail("adapter contract validation harness plan must be ready for review")
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
    }.items():
        if plan.get(key) != value:
            fail(f"adapter contract validation harness plan {key} mismatch")
    for key, value in {
        "source_schema_artifact_count": 4,
        "reviewed_validation_fixture_count": 8,
        "harness_responsibility_count": 6,
        "planned_harness_step_count": 6,
        "input_contract_count": 2,
        "output_contract_count": 2,
        "blocked_action_count": 10,
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
    }.items():
        if plan.get(key) != value:
            fail(f"adapter contract validation harness plan {key} mismatch")
    require_false_flags(plan.get("claim_boundary", {}), "adapter contract validation harness plan claim boundary")
    require_text_markers(
        HARNESS_PLAN_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return plan


def require_reviewed_responsibility(item: dict, source_by_id: dict[str, dict]) -> None:
    responsibility_id = item.get("responsibility_id", "<missing>")
    if responsibility_id not in source_by_id:
        fail(f"reviewed harness responsibility {responsibility_id} missing matching source responsibility")
    source = source_by_id[responsibility_id]
    for key, value in source.items():
        if item.get(key) != value:
            fail(f"reviewed harness responsibility {responsibility_id} changed source field {key}")
    if item.get("review_status") != "reviewed_no_install_harness_responsibility":
        fail(f"reviewed harness responsibility {responsibility_id} review_status mismatch")
    if item.get("harness_responsibility_contract_validated") is not True:
        fail(f"reviewed harness responsibility {responsibility_id} contract validation flag mismatch")


def require_reviewed_step(item: dict, source_by_id: dict[str, dict]) -> None:
    step_id = item.get("step_id", "<missing>")
    if step_id not in source_by_id:
        fail(f"reviewed harness step {step_id} missing matching source step")
    source = source_by_id[step_id]
    for key, value in source.items():
        if item.get(key) != value:
            fail(f"reviewed harness step {step_id} changed source field {key}")
    if item.get("review_status") != "reviewed_deterministic_no_runtime_step":
        fail(f"reviewed harness step {step_id} review_status mismatch")
    if item.get("step_contract_validated") is not True:
        fail(f"reviewed harness step {step_id} contract validation flag mismatch")


def require_review_record(record: dict, label: str, plan: dict) -> None:
    expected = {
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
    if input_uris.get("adapter_contract_validation_harness_plan_gate") != HARNESS_PLAN_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input harness plan gate uri mismatch")

    if record.get("source_schema_artifacts") != plan.get("source_schema_artifacts"):
        fail(f"{label} source schema artifacts mismatch")
    if record.get("reviewed_validation_fixtures") != plan.get("reviewed_validation_fixtures"):
        fail(f"{label} reviewed validation fixtures mismatch")
    if record.get("input_contracts") != plan.get("input_contracts"):
        fail(f"{label} input contracts mismatch")
    if record.get("output_contracts") != plan.get("output_contracts"):
        fail(f"{label} output contracts mismatch")
    if record.get("reviewed_blocked_actions") != plan.get("blocked_actions"):
        fail(f"{label} reviewed blocked actions mismatch")

    reviewed_responsibilities = record.get("reviewed_harness_responsibilities", [])
    if len(reviewed_responsibilities) != EXPECTED_COUNTS["reviewed_harness_responsibility_count"]:
        fail(f"{label} reviewed harness responsibility count mismatch")
    responsibility_by_id = {
        item["responsibility_id"]: item
        for item in plan.get("harness_responsibilities", [])
    }
    for item in reviewed_responsibilities:
        require_reviewed_responsibility(item, responsibility_by_id)

    reviewed_steps = record.get("reviewed_planned_harness_steps", [])
    if len(reviewed_steps) != EXPECTED_COUNTS["reviewed_planned_harness_step_count"]:
        fail(f"{label} reviewed planned harness step count mismatch")
    step_by_id = {
        item["step_id"]: item
        for item in plan.get("planned_harness_steps", [])
    }
    for item in reviewed_steps:
        require_reviewed_step(item, step_by_id)

    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(plan: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-plan-review-gate-v0-1":
        fail("adapter contract validation harness plan review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("adapter contract validation harness plan review gate status must be PASS")
    require_review_record(gate, "adapter contract validation harness plan review gate", plan)


def require_validation_result(plan: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", plan)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    plan = require_previous_harness_plan()
    require_review_record(read_json(REVIEW_GATE), "adapter contract validation harness plan review", plan)
    require_gate(plan)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(REVIEW_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(plan)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Plan Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("provider_neutral=true")
    print("dependency_free=true")
    print("candidate_tool_import_allowed=false")
    print("runtime_integration_allowed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
