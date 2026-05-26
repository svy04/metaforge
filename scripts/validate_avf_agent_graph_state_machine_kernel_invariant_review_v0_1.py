from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_invariant_review_v0_1.py"
INVARIANT_VALIDATION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validation.json"
INVARIANT_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validation_gate.json"
INVARIANT_REVIEW = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_review.json"
INVARIANT_REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_review_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_INVARIANT_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_validator_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_plan_v0_1"
REVIEW_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_INVARIANTS_REVIEWED_FOR_CONTRACT_FREEZE_PLAN"
REVIEW_SCOPE = "repo_local_state_machine_invariant_review_only"
CONTRACT_FREEZE_SCOPE = "repo_local_state_machine_contract_freeze_plan_only"

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
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    INVARIANT_VALIDATION,
    INVARIANT_GATE,
    INVARIANT_REVIEW,
    INVARIANT_REVIEW_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_state_machine_kernel_invariant_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_scope={REVIEW_SCOPE}",
    f"contract_freeze_scope={CONTRACT_FREEZE_SCOPE}",
    "invariants_reviewed=10",
    "invariants_accepted=10",
    "invariants_rejected=0",
    "contract_freeze_plan_allowed=true",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-state-machine-kernel-contract-freeze-plan",
    "owner_approval_required_before_execution: true",
    "Create repo-local contract freeze plan for the deterministic state machine kernel",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph State Machine Kernel Invariant Review v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{rel(path)} missing markers:\n" + "\n".join(missing))


def require_invariant_inputs() -> dict:
    validation = read_json(INVARIANT_VALIDATION)
    expected = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "validator_decision": "AGENT_GRAPH_STATE_MACHINE_KERNEL_INVARIANTS_VALIDATED_FOR_REVIEW",
        "validator_scope": "repo_local_state_machine_invariant_validator_only",
        "review_scope": REVIEW_SCOPE,
        "invariants_evaluated": 10,
        "invariants_passed": 10,
        "invariants_failed": 0,
        "invariant_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected.items():
        if validation.get(key) != value:
            fail(f"invariant validation {key} mismatch")
    results = validation.get("invariant_results")
    if not isinstance(results, list) or len(results) != 10:
        fail("invariant validation must contain ten results")
    for result in results:
        if result.get("status") != "PASS":
            fail(f"invariant must be PASS before review: {result.get('invariant_id')}")
        if result.get("evidence_status") != "verified_repo_local":
            fail(f"invariant must have repo-local evidence: {result.get('invariant_id')}")
        if result.get("protected_action_allowed") is not False:
            fail(f"invariant must not allow protected action: {result.get('invariant_id')}")
    require_false_flags(validation.get("claim_boundary", {}), "invariant validation")

    gate = read_json(INVARIANT_GATE)
    expected_gate = {
        "goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "next_safe_goal_id": THIS_GOAL_ID,
        "invariant_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_gate.items():
        if gate.get(key) != value:
            fail(f"invariant gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "invariant gate")
    return validation


def require_invariant_review(validation: dict) -> None:
    review = read_json(INVARIANT_REVIEW)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "contract_freeze_scope": CONTRACT_FREEZE_SCOPE,
        "invariants_reviewed": 10,
        "invariants_accepted": 10,
        "invariants_rejected": 0,
        "contract_freeze_plan_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if review.get(key) != value:
            fail(f"invariant review {key} mismatch")
    records = review.get("invariant_review_records")
    if not isinstance(records, list) or len(records) != 10:
        fail("invariant review must contain ten review records")
    result_ids = [result["invariant_id"] for result in validation["invariant_results"]]
    record_ids = [record.get("invariant_id") for record in records]
    if record_ids != result_ids:
        fail(f"invariant review record ids mismatch: {record_ids}")
    for record in records:
        if record.get("review_status") != "accepted":
            fail(f"invariant review record must be accepted: {record.get('invariant_id')}")
        if record.get("contract_implication") != "freeze_as_state_machine_contract_invariant":
            fail(f"invariant review implication mismatch: {record.get('invariant_id')}")
        if record.get("protected_action_allowed") is not False:
            fail(f"invariant review must not allow protected action: {record.get('invariant_id')}")
    require_false_flags(review.get("claim_boundary", {}), "invariant review")


def require_review_gate() -> None:
    gate = read_json(INVARIANT_REVIEW_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-invariant-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "contract_freeze_scope": CONTRACT_FREEZE_SCOPE,
        "invariants_reviewed": 10,
        "invariants_accepted": 10,
        "invariants_rejected": 0,
        "contract_freeze_plan_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"invariant review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "invariant review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_state_machine_kernel_invariant_review_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
    if result.get("contract_freeze_plan_allowed") is not True:
        fail("validation result must allow contract freeze plan")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    validation = require_invariant_inputs()
    require_invariant_review(validation)
    require_review_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(
        VALIDATION_REPORT,
        TEXT_MARKERS
        + [
            "RESULT: PASS",
            "protected_action_executed=false",
            "provider_calls_performed=false",
            "live_model_calls_performed=false",
            "external_service_calls_performed=false",
            "dependency_install_performed=false",
            "external_fetch_performed=false",
            "oss_clone_performed=false",
            "runtime_integration_performed=false",
            "deploy_performed=false",
            "publish_performed=false",
            "release_ready=false",
            "production_ready=false",
        ],
    )

    print("AVF Agent Graph State Machine Kernel Invariant Review v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_invariant_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"contract_freeze_scope={CONTRACT_FREEZE_SCOPE}")
    print("invariants_reviewed=10")
    print("invariants_accepted=10")
    print("invariants_rejected=0")
    print("contract_freeze_plan_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("automated_scraping_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
