from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime"
RUNTIME_GENERATED = RUNTIME / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_v0_1.py"
KERNEL_SCHEMA = RUNTIME / "agent_graph_state_machine_kernel.schema.yml"
TRANSITIONS = RUNTIME_GENERATED / "agent_graph_run_state_transitions.json"
REVIEW_RESULT = RUNTIME_GENERATED / "agent_graph_policy_enforcement_review.json"
REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_policy_enforcement_review_gate.json"
KERNEL = RUNTIME_GENERATED / "agent_graph_state_machine_kernel.json"
KERNEL_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_policy_enforcement_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_replay_harness_v0_1"
KERNEL_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_READY_FOR_REPLAY_HARNESS"
KERNEL_SCOPE = "repo_local_deterministic_state_machine_kernel_only"

NORMAL_STATES = [
    "initialized",
    "orchestrated",
    "routed",
    "safety_reviewed",
    "codex_planned",
    "evidence_written",
]

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
    KERNEL_SCHEMA,
    TRANSITIONS,
    REVIEW_RESULT,
    REVIEW_GATE,
    KERNEL,
    KERNEL_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_state_machine_kernel_v0_1=true",
    f"kernel_decision={KERNEL_DECISION}",
    f"kernel_scope={KERNEL_SCOPE}",
    "normal_states_created=6",
    "normal_transition_edges_created=5",
    "guarded_policy_outcomes_modeled=8",
    "allowed_replay_outcomes_modeled=1",
    "blocked_terminal_outcomes_modeled=5",
    "owner_review_outcomes_modeled=2",
    "kernel_replay_harness_allowed=true",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-state-machine-kernel-replay-harness",
    "owner_approval_required_before_execution: true",
    "Replay deterministic state machine kernel with normal, blocked, and owner-review outcomes",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph State Machine Kernel v0.1 validation")
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


def require_inputs() -> tuple[dict, dict]:
    transitions = read_json(TRANSITIONS)
    if transitions.get("state_sequence") != NORMAL_STATES:
        fail("normal transition state sequence mismatch")
    if transitions.get("terminal_state") != "evidence_written":
        fail("normal transition terminal state mismatch")
    if len(transitions.get("transitions", [])) != 5:
        fail("normal transition model must contain five edges")
    require_false_flags(transitions.get("claim_boundary", {}), "normal transition model")

    review = read_json(REVIEW_RESULT)
    expected_review = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "review_decision": "AGENT_GRAPH_POLICY_ENFORCEMENT_REVIEWED_FOR_STATE_MACHINE_KERNEL",
        "state_machine_kernel_allowed": True,
        "policy_rules_reviewed": 8,
        "enforcement_evaluations_reviewed": 8,
        "allowed_local_only_decisions_reviewed": 1,
        "blocked_decisions_reviewed": 5,
        "owner_review_required_decisions_reviewed": 2,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_review.items():
        if review.get(key) != value:
            fail(f"policy enforcement review {key} mismatch")
    if len(review.get("review_records", [])) != 8:
        fail("policy enforcement review must contain eight records")
    require_false_flags(review.get("claim_boundary", {}), "policy enforcement review")

    gate = read_json(REVIEW_GATE)
    expected_gate = {
        "goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "next_safe_goal_id": THIS_GOAL_ID,
        "state_machine_kernel_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_gate.items():
        if gate.get(key) != value:
            fail(f"policy enforcement review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "policy enforcement review gate")
    return transitions, review


def require_kernel_schema() -> None:
    require_text_markers(
        KERNEL_SCHEMA,
        [
            "schema_id: avf.agent_graph_state_machine_kernel.v0_1",
            "schema_status: repo_local_contract_only",
            "allowed_terminal_states:",
            "blocked_terminal",
            "owner_review_required",
            "protected_actions_must_remain_false: true",
            "runtime_integration_allowed: false",
        ],
    )


def require_kernel(transitions: dict, review: dict) -> None:
    kernel = read_json(KERNEL)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "kernel_decision": KERNEL_DECISION,
        "kernel_scope": KERNEL_SCOPE,
        "normal_states_created": 6,
        "normal_transition_edges_created": 5,
        "guarded_policy_outcomes_modeled": 8,
        "allowed_replay_outcomes_modeled": 1,
        "blocked_terminal_outcomes_modeled": 5,
        "owner_review_outcomes_modeled": 2,
        "kernel_replay_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if kernel.get(key) != value:
            fail(f"kernel {key} mismatch")
    if kernel.get("normal_states") != NORMAL_STATES:
        fail("kernel normal states mismatch")
    if kernel.get("normal_transition_edges") != transitions.get("transitions"):
        fail("kernel normal transition edges must match transition model")
    guarded = kernel.get("guarded_outcome_states")
    if not isinstance(guarded, list) or len(guarded) != 8:
        fail("kernel must contain eight guarded outcome states")
    review_ids = {record["rule_id"] for record in review["review_records"]}
    outcome_counts = {
        "allowed_replay_path": 0,
        "blocked_terminal": 0,
        "owner_review_required": 0,
    }
    expected_state_by_implication = {
        "model_as_allowed_transition": "allowed_replay_path",
        "model_as_blocked_terminal_state": "blocked_terminal",
        "model_as_owner_review_state": "owner_review_required",
    }
    for state in guarded:
        if state.get("rule_id") not in review_ids:
            fail(f"unknown guarded state rule: {state.get('rule_id')}")
        state_type = state.get("state_type")
        if state_type not in outcome_counts:
            fail(f"unexpected guarded state type: {state_type}")
        if state.get("state_type") != expected_state_by_implication.get(state.get("source_implication")):
            fail(f"guarded state implication mismatch: {state.get('rule_id')}")
        if state.get("protected_action_allowed") is not False:
            fail(f"guarded state must not allow protected action: {state.get('rule_id')}")
        outcome_counts[state_type] += 1
    if outcome_counts != {
        "allowed_replay_path": 1,
        "blocked_terminal": 5,
        "owner_review_required": 2,
    }:
        fail(f"guarded outcome counts mismatch: {outcome_counts}")
    require_false_flags(kernel.get("claim_boundary", {}), "kernel")


def require_kernel_gate() -> None:
    gate = read_json(KERNEL_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "kernel_decision": KERNEL_DECISION,
        "kernel_scope": KERNEL_SCOPE,
        "kernel_replay_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"kernel gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "kernel gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_state_machine_kernel_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("kernel_decision") != KERNEL_DECISION:
        fail("validation result kernel decision mismatch")
    if result.get("kernel_replay_harness_allowed") is not True:
        fail("validation result must allow kernel replay harness")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    transitions, review = require_inputs()
    require_kernel_schema()
    require_kernel(transitions, review)
    require_kernel_gate()
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

    print("AVF Agent Graph State Machine Kernel v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_v0_1=true")
    print(f"kernel_decision={KERNEL_DECISION}")
    print(f"kernel_scope={KERNEL_SCOPE}")
    print("normal_states_created=6")
    print("normal_transition_edges_created=5")
    print("guarded_policy_outcomes_modeled=8")
    print("allowed_replay_outcomes_modeled=1")
    print("blocked_terminal_outcomes_modeled=5")
    print("owner_review_outcomes_modeled=2")
    print("kernel_replay_harness_allowed=true")
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
