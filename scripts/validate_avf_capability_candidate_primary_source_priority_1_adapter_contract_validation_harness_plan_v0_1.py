from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1.py"
FIXTURE_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_gate.json"
FIXTURE_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_next_action.yml"
HARNESS_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan.json"
HARNESS_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_gate.json"
HARNESS_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_report.md"
HARNESS_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PLAN_DECISION = "CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_CONTRACT_VALIDATION_HARNESS_PLAN"
PLAN_STATUS = "adapter_contract_validation_harness_plan_created_provider_neutral_no_install"

EXPECTED_COUNTS = {
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
    "review_blocker_count": 0,
    "ready_for_adapter_contract_validation_harness_plan_review_count": 1,
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
    FIXTURE_REVIEW_GATE,
    FIXTURE_REVIEW_NEXT_ACTION,
    HARNESS_PLAN,
    HARNESS_PLAN_GATE,
    HARNESS_PLAN_REPORT,
    HARNESS_PLAN_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"plan_decision={PLAN_DECISION}",
    f"plan_status={PLAN_STATUS}",
    "source_schema_artifact_count=4",
    "reviewed_validation_fixture_count=8",
    "harness_responsibility_count=6",
    "planned_harness_step_count=6",
    "input_contract_count=2",
    "output_contract_count=2",
    "blocked_action_count=10",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "review_blocker_count=0",
    "ready_for_adapter_contract_validation_harness_plan_review_count=1",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-plan",
    "owner_approval_required_before_execution: false",
    "Review the repo-local no-install adapter contract validation harness plan",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Plan v0.1 validation")
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


def require_previous_fixture_review() -> dict:
    review = read_json(FIXTURE_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("adapter contract validation fixture pack review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("adapter contract validation fixture pack review gate must point to this harness plan goal")
    if review.get("ready_for_adapter_contract_validation_harness_plan_count") != 1:
        fail("adapter contract validation fixture pack review must be ready for harness plan")
    if review.get("provider_neutral") is not True:
        fail("adapter contract validation fixture pack review must remain provider-neutral")
    if review.get("dependency_free") is not True:
        fail("adapter contract validation fixture pack review must remain dependency-free")
    if review.get("candidate_tool_import_allowed") is not False:
        fail("adapter contract validation fixture pack review must not allow candidate tool import")
    if review.get("dependency_install_allowed") is not False:
        fail("adapter contract validation fixture pack review must not allow dependency install")
    if review.get("runtime_integration_allowed") is not False:
        fail("adapter contract validation fixture pack review must not allow runtime integration")
    require_false_flags(review.get("claim_boundary", {}), "adapter contract validation fixture pack review claim boundary")
    require_text_markers(
        FIXTURE_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_harness_plan_record(record: dict, label: str, review: dict) -> None:
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
    if input_uris.get("adapter_contract_validation_fixture_pack_review_gate") != FIXTURE_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input fixture review gate uri mismatch")

    if record.get("source_schema_artifacts") != review.get("source_schema_artifacts"):
        fail(f"{label} source schema artifacts mismatch")
    if record.get("reviewed_validation_fixtures") != review.get("reviewed_validation_fixtures"):
        fail(f"{label} reviewed validation fixtures mismatch")

    responsibilities = record.get("harness_responsibilities", [])
    if len(responsibilities) != EXPECTED_COUNTS["harness_responsibility_count"]:
        fail(f"{label} harness responsibility count mismatch")
    for item in responsibilities:
        if item.get("provider_neutral") is not True:
            fail(f"{label} responsibility {item.get('responsibility_id')} must be provider-neutral")
        if item.get("dependency_free") is not True:
            fail(f"{label} responsibility {item.get('responsibility_id')} must be dependency-free")
        if item.get("candidate_tool_import_allowed") is not False:
            fail(f"{label} responsibility {item.get('responsibility_id')} must not allow candidate tool import")
        if item.get("runtime_integration_allowed") is not False:
            fail(f"{label} responsibility {item.get('responsibility_id')} must not allow runtime integration")

    planned_steps = record.get("planned_harness_steps", [])
    if len(planned_steps) != EXPECTED_COUNTS["planned_harness_step_count"]:
        fail(f"{label} planned harness step count mismatch")
    blocked_actions = record.get("blocked_actions", [])
    if len(blocked_actions) != EXPECTED_COUNTS["blocked_action_count"]:
        fail(f"{label} blocked action count mismatch")
    required_blocked = {
        "dependency_install",
        "oss_clone",
        "candidate_tool_import",
        "runtime_integration",
        "provider_call",
        "live_model_call",
        "external_fetch",
        "deploy",
        "publish",
        "readiness_claim",
    }
    if set(blocked_actions) != required_blocked:
        fail(f"{label} blocked actions mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(review: dict) -> None:
    gate = read_json(HARNESS_PLAN_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-plan-gate-v0-1":
        fail("adapter contract validation harness plan gate id mismatch")
    if gate.get("status") != "PASS":
        fail("adapter contract validation harness plan gate status must be PASS")
    require_harness_plan_record(gate, "adapter contract validation harness plan gate", review)


def require_validation_result(review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_harness_plan_record(result, "validation result", review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review = require_previous_fixture_review()
    require_harness_plan_record(read_json(HARNESS_PLAN), "adapter contract validation harness plan", review)
    require_gate(review)
    require_text_markers(HARNESS_PLAN_REPORT, REPORT_MARKERS)
    require_text_markers(HARNESS_PLAN_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Plan v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_status={PLAN_STATUS}")
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
