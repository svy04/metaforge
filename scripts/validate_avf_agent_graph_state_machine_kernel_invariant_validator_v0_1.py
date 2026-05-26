from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_invariant_validator_v0_1.py"
HARDENING_PLAN = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan.json"
HARDENING_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan_gate.json"
REPLAY_REVIEW = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_review.json"
INVARIANT_VALIDATION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validation.json"
INVARIANT_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validation_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validation_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_invariant_validator_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_INVARIANT_VALIDATOR_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_validator_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_hardening_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_review_v0_1"
VALIDATOR_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_INVARIANTS_VALIDATED_FOR_REVIEW"
VALIDATOR_SCOPE = "repo_local_state_machine_invariant_validator_only"
REVIEW_SCOPE = "repo_local_state_machine_invariant_review_only"

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

EXPECTED_INVARIANTS = [
    "normal_path_terminal_state_is_evidence_written",
    "normal_transition_sequence_is_contiguous",
    "normal_transition_order_is_preserved",
    "guarded_allowed_path_requires_pass_status",
    "blocked_terminal_outcomes_never_reach_evidence_written",
    "owner_review_outcomes_never_auto_execute",
    "protected_action_flags_remain_false",
    "dependency_and_runtime_actions_remain_blocked",
    "evidence_event_uri_required_before_terminal_success",
    "node_sequence_gap_or_duplicate_blocks_transition",
]

REQUIRED_FILES = [
    RUNNER,
    HARDENING_PLAN,
    HARDENING_GATE,
    REPLAY_REVIEW,
    INVARIANT_VALIDATION,
    INVARIANT_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_state_machine_kernel_invariant_validator_v0_1=true",
    f"validator_decision={VALIDATOR_DECISION}",
    f"validator_scope={VALIDATOR_SCOPE}",
    f"review_scope={REVIEW_SCOPE}",
    "invariants_evaluated=10",
    "invariants_passed=10",
    "invariants_failed=0",
    "normal_path_invariants_passed=3",
    "guarded_outcome_invariants_passed=4",
    "safety_boundary_invariants_passed=3",
    "invariant_review_allowed=true",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-agent-graph-state-machine-kernel-invariant-validation",
    "owner_approval_required_before_execution: true",
    "Review repo-local invariant validation before any runtime adapter hardening",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph State Machine Kernel Invariant Validator v0.1 validation")
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


def require_hardening_inputs() -> dict:
    plan = read_json(HARDENING_PLAN)
    expected = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "plan_decision": "AGENT_GRAPH_STATE_MACHINE_KERNEL_HARDENING_PLAN_READY_FOR_INVARIANT_VALIDATOR",
        "plan_scope": "repo_local_state_machine_hardening_plan_only",
        "invariant_scope": VALIDATOR_SCOPE,
        "hardening_invariants_created": 10,
        "normal_path_invariants": 3,
        "guarded_outcome_invariants": 4,
        "safety_boundary_invariants": 3,
        "invariant_validator_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected.items():
        if plan.get(key) != value:
            fail(f"hardening plan {key} mismatch")
    invariants = plan.get("hardening_invariants")
    if not isinstance(invariants, list) or len(invariants) != 10:
        fail("hardening plan must contain ten invariants")
    invariant_ids = [invariant.get("invariant_id") for invariant in invariants]
    if invariant_ids != EXPECTED_INVARIANTS:
        fail(f"hardening invariant ids mismatch: {invariant_ids}")
    require_false_flags(plan.get("claim_boundary", {}), "hardening plan")

    gate = read_json(HARDENING_GATE)
    expected_gate = {
        "goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "next_safe_goal_id": THIS_GOAL_ID,
        "invariant_validator_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_gate.items():
        if gate.get(key) != value:
            fail(f"hardening gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "hardening gate")
    return plan


def require_replay_review() -> dict:
    review = read_json(REPLAY_REVIEW)
    expected = {
        "goal_id": "avf_agent_graph_state_machine_kernel_replay_review_v0_1",
        "next_safe_goal_id": PREVIOUS_GOAL_ID,
        "normal_path_reviewed": True,
        "normal_transition_edges_reviewed": 5,
        "guarded_outcomes_reviewed": 8,
        "allowed_replay_outcomes_reviewed": 1,
        "blocked_terminal_outcomes_reviewed": 5,
        "owner_review_outcomes_reviewed": 2,
        "unexpected_replay_results": 0,
        "hardening_plan_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected.items():
        if review.get(key) != value:
            fail(f"replay review {key} mismatch")
    if len(review.get("normal_path_review_records", [])) != 5:
        fail("replay review must contain five normal path records")
    if len(review.get("guarded_outcome_review_records", [])) != 8:
        fail("replay review must contain eight guarded outcome records")
    require_false_flags(review.get("claim_boundary", {}), "replay review")
    return review


def require_invariant_validation(plan: dict) -> None:
    validation = read_json(INVARIANT_VALIDATION)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "validator_decision": VALIDATOR_DECISION,
        "validator_scope": VALIDATOR_SCOPE,
        "review_scope": REVIEW_SCOPE,
        "invariants_evaluated": 10,
        "invariants_passed": 10,
        "invariants_failed": 0,
        "normal_path_invariants_passed": 3,
        "guarded_outcome_invariants_passed": 4,
        "safety_boundary_invariants_passed": 3,
        "invariant_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if validation.get(key) != value:
            fail(f"invariant validation {key} mismatch")
    results = validation.get("invariant_results")
    if not isinstance(results, list) or len(results) != 10:
        fail("invariant validation must contain ten results")
    result_ids = [result.get("invariant_id") for result in results]
    if result_ids != EXPECTED_INVARIANTS:
        fail(f"invariant result ids mismatch: {result_ids}")
    plan_categories = {
        invariant["invariant_id"]: invariant["category"]
        for invariant in plan["hardening_invariants"]
    }
    for result in results:
        invariant_id = result.get("invariant_id")
        if result.get("status") != "PASS":
            fail(f"invariant must pass: {invariant_id}")
        if result.get("category") != plan_categories[invariant_id]:
            fail(f"invariant category mismatch: {invariant_id}")
        if result.get("evidence_status") != "verified_repo_local":
            fail(f"invariant evidence status mismatch: {invariant_id}")
        if result.get("protected_action_allowed") is not False:
            fail(f"invariant must not allow protected action: {invariant_id}")
    require_false_flags(validation.get("claim_boundary", {}), "invariant validation")


def require_invariant_gate() -> None:
    gate = read_json(INVARIANT_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-invariant-validation-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "validator_decision": VALIDATOR_DECISION,
        "validator_scope": VALIDATOR_SCOPE,
        "review_scope": REVIEW_SCOPE,
        "invariants_evaluated": 10,
        "invariants_passed": 10,
        "invariants_failed": 0,
        "invariant_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"invariant gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "invariant gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_state_machine_kernel_invariant_validator_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("validator_decision") != VALIDATOR_DECISION:
        fail("validation result validator decision mismatch")
    if result.get("invariant_review_allowed") is not True:
        fail("validation result must allow invariant review")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    plan = require_hardening_inputs()
    require_replay_review()
    require_invariant_validation(plan)
    require_invariant_gate()
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

    print("AVF Agent Graph State Machine Kernel Invariant Validator v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_invariant_validator_v0_1=true")
    print(f"validator_decision={VALIDATOR_DECISION}")
    print(f"validator_scope={VALIDATOR_SCOPE}")
    print(f"review_scope={REVIEW_SCOPE}")
    print("invariants_evaluated=10")
    print("invariants_passed=10")
    print("invariants_failed=0")
    print("normal_path_invariants_passed=3")
    print("guarded_outcome_invariants_passed=4")
    print("safety_boundary_invariants_passed=3")
    print("invariant_review_allowed=true")
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
