from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1.py"
ADAPTER_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_gate.json"
ADAPTER_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_NO_INSTALL_ADAPTER_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_NO_INSTALL_ADAPTER_PLAN_REVIEWED"
REVIEW_STATUS = "no_install_adapter_plan_validated_ready_for_adapter_contract_schema_pack"

EXPECTED_COUNTS = {
    "adapter_component_count": 5,
    "reviewed_adapter_component_count": 5,
    "contract_boundary_count": 6,
    "reviewed_contract_boundary_count": 6,
    "blocked_action_count": 8,
    "reviewed_blocked_action_count": 8,
    "dependency_install_allowed_count": 0,
    "oss_clone_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_contract_schema_pack_count": 1,
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
    ADAPTER_PLAN_GATE,
    ADAPTER_PLAN_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "plan_remains_contract_only=true",
    "dependency_install_allowed=false",
    "oss_clone_allowed=false",
    "runtime_integration_allowed=false",
    "adapter_component_count=5",
    "reviewed_adapter_component_count=5",
    "contract_boundary_count=6",
    "reviewed_contract_boundary_count=6",
    "blocked_action_count=8",
    "reviewed_blocked_action_count=8",
    "dependency_install_allowed_count=0",
    "oss_clone_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "ready_for_adapter_contract_schema_pack_count=1",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "dependency_install_performed=false",
    "runtime_integration_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-schema-pack",
    "owner_approval_required_before_execution: false",
    "Create adapter contract schemas without importing candidate tools",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 No-Install Adapter Plan Review v0.1 validation")
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


def require_previous_plan() -> dict:
    plan = read_json(ADAPTER_PLAN_GATE)
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("adapter plan gate goal_id mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("adapter plan gate must point to this review goal")
    if plan.get("ready_for_no_install_adapter_plan_review_count") != 1:
        fail("adapter plan must be ready for review")
    if plan.get("dependency_install_allowed") is not False:
        fail("adapter plan must not allow dependency install")
    if plan.get("oss_clone_allowed") is not False:
        fail("adapter plan must not allow OSS clone")
    if plan.get("runtime_integration_allowed") is not False:
        fail("adapter plan must not allow runtime integration")
    require_false_flags(plan.get("claim_boundary", {}), "adapter plan claim boundary")
    require_text_markers(
        ADAPTER_PLAN_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-no-install-adapter-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return plan


def require_reviewed_component(item: dict, component_by_id: dict[str, dict]) -> None:
    component_id = item.get("component_id", "<missing>")
    if component_id not in component_by_id:
        fail(f"reviewed adapter component {component_id} missing matching input component")
    component = component_by_id[component_id]
    for key, value in component.items():
        if item.get(key) != value:
            fail(f"reviewed adapter component {component_id} changed input field {key}")
    if item.get("review_status") != "reviewed_contract_only_component_validated":
        fail(f"reviewed adapter component {component_id} review_status mismatch")


def require_review_record(record: dict, label: str, plan: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "plan_remains_contract_only": True,
        "dependency_install_allowed": False,
        "oss_clone_allowed": False,
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
    if input_uris.get("no_install_adapter_plan_gate") != ADAPTER_PLAN_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input adapter plan gate uri mismatch")

    reviewed_components = record.get("reviewed_adapter_components", [])
    if len(reviewed_components) != EXPECTED_COUNTS["reviewed_adapter_component_count"]:
        fail(f"{label} reviewed adapter component count mismatch")
    component_by_id = {
        item["component_id"]: item
        for item in plan.get("adapter_components", [])
    }
    for item in reviewed_components:
        require_reviewed_component(item, component_by_id)

    if record.get("reviewed_contract_boundaries") != plan.get("contract_boundaries"):
        fail(f"{label} reviewed contract boundaries mismatch")
    if record.get("reviewed_blocked_actions") != plan.get("blocked_actions"):
        fail(f"{label} reviewed blocked actions mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(plan: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-no-install-adapter-plan-review-gate-v0-1":
        fail("adapter plan review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("adapter plan review gate status must be PASS")
    require_review_record(gate, "adapter plan review gate", plan)


def require_validation_result(plan: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", plan)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    plan = require_previous_plan()
    review = read_json(REVIEW_GATE)
    require_review_record(review, "adapter plan review", plan)
    require_gate(plan)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(plan)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 No-Install Adapter Plan Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("plan_remains_contract_only=true")
    print("dependency_install_allowed=false")
    print("oss_clone_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
