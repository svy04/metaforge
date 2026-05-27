from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1.py"
RECOMMENDATION_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_gate.json"
RECOMMENDATION_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_next_action.yml"
ADAPTER_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan.json"
ADAPTER_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_gate.json"
ADAPTER_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_NO_INSTALL_ADAPTER_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PLAN_DECISION = "CREATE_NO_INSTALL_ADAPTER_PLAN_ONLY"
PLAN_STATUS = "no_install_adapter_contract_plan_created"

EXPECTED_COUNTS = {
    "adapter_component_count": 5,
    "contract_boundary_count": 6,
    "blocked_action_count": 8,
    "dependency_install_allowed_count": 0,
    "oss_clone_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "ready_for_no_install_adapter_plan_review_count": 1,
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
    RECOMMENDATION_GATE,
    RECOMMENDATION_NEXT_ACTION,
    ADAPTER_PLAN,
    ADAPTER_PLAN_GATE,
    ADAPTER_PLAN_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"plan_decision={PLAN_DECISION}",
    f"plan_status={PLAN_STATUS}",
    "dependency_install_allowed=false",
    "oss_clone_allowed=false",
    "runtime_integration_allowed=false",
    "adapter_component_count=5",
    "contract_boundary_count=6",
    "blocked_action_count=8",
    "dependency_install_allowed_count=0",
    "oss_clone_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "ready_for_no_install_adapter_plan_review_count=1",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "dependency_install_performed=false",
    "runtime_integration_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-priority-1-no-install-adapter-plan",
    "owner_approval_required_before_execution: false",
    "Review the no-install adapter plan for contract safety",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 No-Install Adapter Plan v0.1 validation")
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


def require_previous_recommendation() -> dict:
    recommendation = read_json(RECOMMENDATION_GATE)
    if recommendation.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("recommendation gate goal_id mismatch")
    if recommendation.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("recommendation gate must point to this adapter plan goal")
    if recommendation.get("ready_for_no_install_adapter_plan_count") != 1:
        fail("recommendation must be ready for no-install adapter plan")
    if recommendation.get("dependency_install_allowed") is not False:
        fail("recommendation must not allow dependency install")
    if recommendation.get("runtime_integration_allowed") is not False:
        fail("recommendation must not allow runtime integration")
    require_false_flags(recommendation.get("claim_boundary", {}), "recommendation claim boundary")
    require_text_markers(
        RECOMMENDATION_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-no-install-adapter-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return recommendation


def require_plan_record(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "plan_decision": PLAN_DECISION,
        "plan_status": PLAN_STATUS,
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
    if input_uris.get("evidence_backed_recommendation_gate") != RECOMMENDATION_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input recommendation gate uri mismatch")
    if len(record.get("adapter_components", [])) != EXPECTED_COUNTS["adapter_component_count"]:
        fail(f"{label} adapter component count mismatch")
    if len(record.get("contract_boundaries", [])) != EXPECTED_COUNTS["contract_boundary_count"]:
        fail(f"{label} contract boundary count mismatch")
    if len(record.get("blocked_actions", [])) != EXPECTED_COUNTS["blocked_action_count"]:
        fail(f"{label} blocked action count mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate() -> None:
    gate = read_json(ADAPTER_PLAN_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-no-install-adapter-plan-gate-v0-1":
        fail("adapter plan gate id mismatch")
    if gate.get("status") != "PASS":
        fail("adapter plan gate status must be PASS")
    require_plan_record(gate, "adapter plan gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_plan_record(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_recommendation()
    plan = read_json(ADAPTER_PLAN)
    require_plan_record(plan, "adapter plan")
    require_gate()
    require_text_markers(ADAPTER_PLAN_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 No-Install Adapter Plan v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_status={PLAN_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
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
