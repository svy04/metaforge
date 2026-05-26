from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_hardening_plan_v0_1.py"
REVIEW_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_review.json"
REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_review_gate.json"
HARDENING_PLAN = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan.json"
HARDENING_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_hardening_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_HARDENING_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_hardening_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_replay_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_invariant_validator_v0_1"
PLAN_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_HARDENING_PLAN_READY_FOR_INVARIANT_VALIDATOR"
PLAN_SCOPE = "repo_local_state_machine_hardening_plan_only"
INVARIANT_SCOPE = "repo_local_state_machine_invariant_validator_only"

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
    REVIEW_RESULT,
    REVIEW_GATE,
    HARDENING_PLAN,
    HARDENING_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
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

TEXT_MARKERS = [
    "agent_graph_state_machine_kernel_hardening_plan_v0_1=true",
    f"plan_decision={PLAN_DECISION}",
    f"plan_scope={PLAN_SCOPE}",
    f"invariant_scope={INVARIANT_SCOPE}",
    "hardening_invariants_created=10",
    "normal_path_invariants=3",
    "guarded_outcome_invariants=4",
    "safety_boundary_invariants=3",
    "invariant_validator_allowed=true",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-state-machine-kernel-invariant-validator",
    "owner_approval_required_before_execution: true",
    "Create repo-local invariant validator for the deterministic state machine kernel",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph State Machine Kernel Hardening Plan v0.1 validation")
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


def require_review_inputs() -> dict:
    review = read_json(REVIEW_RESULT)
    expected = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "review_decision": "AGENT_GRAPH_STATE_MACHINE_KERNEL_REPLAY_REVIEWED_FOR_HARDENING_PLAN",
        "review_scope": "repo_local_state_machine_kernel_replay_review_only",
        "hardening_scope": PLAN_SCOPE,
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
            fail(f"replay review result {key} mismatch")
    normal_records = review.get("normal_path_review_records")
    if not isinstance(normal_records, list) or len(normal_records) != 5:
        fail("replay review must contain five normal path records")
    guarded_records = review.get("guarded_outcome_review_records")
    if not isinstance(guarded_records, list) or len(guarded_records) != 8:
        fail("replay review must contain eight guarded records")
    require_false_flags(review.get("claim_boundary", {}), "replay review result")

    gate = read_json(REVIEW_GATE)
    expected_gate = {
        "goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "next_safe_goal_id": THIS_GOAL_ID,
        "hardening_plan_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_gate.items():
        if gate.get(key) != value:
            fail(f"replay review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "replay review gate")
    return review


def require_hardening_plan(review: dict) -> None:
    plan = read_json(HARDENING_PLAN)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "plan_decision": PLAN_DECISION,
        "plan_scope": PLAN_SCOPE,
        "invariant_scope": INVARIANT_SCOPE,
        "hardening_invariants_created": 10,
        "normal_path_invariants": 3,
        "guarded_outcome_invariants": 4,
        "safety_boundary_invariants": 3,
        "invariant_validator_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
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
    for invariant in invariants:
        if invariant.get("status") != "planned":
            fail(f"invariant must be planned: {invariant.get('invariant_id')}")
        if invariant.get("validator_required") is not True:
            fail(f"invariant must require validator: {invariant.get('invariant_id')}")
        if invariant.get("protected_action_allowed") is not False:
            fail(f"invariant must not allow protected action: {invariant.get('invariant_id')}")
    if plan.get("source_review_goal_id") != review.get("goal_id"):
        fail("hardening plan source review goal mismatch")
    require_false_flags(plan.get("claim_boundary", {}), "hardening plan")


def require_hardening_gate() -> None:
    gate = read_json(HARDENING_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-hardening-plan-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "plan_decision": PLAN_DECISION,
        "plan_scope": PLAN_SCOPE,
        "invariant_scope": INVARIANT_SCOPE,
        "hardening_invariants_created": 10,
        "invariant_validator_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"hardening gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "hardening gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_state_machine_kernel_hardening_plan_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("plan_decision") != PLAN_DECISION:
        fail("validation result plan decision mismatch")
    if result.get("invariant_validator_allowed") is not True:
        fail("validation result must allow invariant validator")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review = require_review_inputs()
    require_hardening_plan(review)
    require_hardening_gate()
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

    print("AVF Agent Graph State Machine Kernel Hardening Plan v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_hardening_plan_v0_1=true")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_scope={PLAN_SCOPE}")
    print(f"invariant_scope={INVARIANT_SCOPE}")
    print("hardening_invariants_created=10")
    print("normal_path_invariants=3")
    print("guarded_outcome_invariants=4")
    print("safety_boundary_invariants=3")
    print("invariant_validator_allowed=true")
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
