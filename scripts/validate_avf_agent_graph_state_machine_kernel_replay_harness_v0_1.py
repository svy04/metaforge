from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_replay_harness_v0_1.py"
KERNEL = RUNTIME_GENERATED / "agent_graph_state_machine_kernel.json"
KERNEL_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_gate.json"
REPLAY_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_harness_result.json"
REPLAY_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_harness_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_harness_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_harness_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_REPLAY_HARNESS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_replay_harness_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_replay_review_v0_1"
REPLAY_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_REPLAY_HARNESS_READY_FOR_REVIEW"
REPLAY_SCOPE = "repo_local_state_machine_kernel_replay_only"

NORMAL_STATE_PATH = [
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
    KERNEL,
    KERNEL_GATE,
    REPLAY_RESULT,
    REPLAY_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_state_machine_kernel_replay_harness_v0_1=true",
    f"replay_decision={REPLAY_DECISION}",
    f"replay_scope={REPLAY_SCOPE}",
    "normal_path_replayed=true",
    "normal_terminal_state=evidence_written",
    "guarded_outcomes_replayed=8",
    "allowed_replay_outcomes_replayed=1",
    "blocked_terminal_outcomes_replayed=5",
    "owner_review_outcomes_replayed=2",
    "unexpected_replay_results=0",
    "replay_review_allowed=true",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-agent-graph-state-machine-kernel-replay-harness",
    "owner_approval_required_before_execution: true",
    "Review kernel replay outcomes before state machine hardening",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph State Machine Kernel Replay Harness v0.1 validation")
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


def require_kernel_inputs() -> dict:
    kernel = read_json(KERNEL)
    expected = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "kernel_decision": "AGENT_GRAPH_STATE_MACHINE_KERNEL_READY_FOR_REPLAY_HARNESS",
        "normal_states_created": 6,
        "normal_transition_edges_created": 5,
        "guarded_policy_outcomes_modeled": 8,
        "allowed_replay_outcomes_modeled": 1,
        "blocked_terminal_outcomes_modeled": 5,
        "owner_review_outcomes_modeled": 2,
        "kernel_replay_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected.items():
        if kernel.get(key) != value:
            fail(f"kernel {key} mismatch")
    if kernel.get("normal_states") != NORMAL_STATE_PATH:
        fail("kernel normal state path mismatch")
    if len(kernel.get("normal_transition_edges", [])) != 5:
        fail("kernel must contain five normal transition edges")
    if len(kernel.get("guarded_outcome_states", [])) != 8:
        fail("kernel must contain eight guarded outcome states")
    require_false_flags(kernel.get("claim_boundary", {}), "kernel")

    gate = read_json(KERNEL_GATE)
    expected_gate = {
        "goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "next_safe_goal_id": THIS_GOAL_ID,
        "kernel_replay_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_gate.items():
        if gate.get(key) != value:
            fail(f"kernel gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "kernel gate")
    return kernel


def require_replay_result(kernel: dict) -> None:
    replay = read_json(REPLAY_RESULT)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "replay_decision": REPLAY_DECISION,
        "replay_scope": REPLAY_SCOPE,
        "normal_path_replayed": True,
        "normal_terminal_state": "evidence_written",
        "guarded_outcomes_replayed": 8,
        "allowed_replay_outcomes_replayed": 1,
        "blocked_terminal_outcomes_replayed": 5,
        "owner_review_outcomes_replayed": 2,
        "unexpected_replay_results": 0,
        "replay_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if replay.get(key) != value:
            fail(f"replay result {key} mismatch")
    normal = replay.get("normal_path_replay")
    if normal.get("state_path") != NORMAL_STATE_PATH:
        fail("normal replay state path mismatch")
    if normal.get("terminal_state") != "evidence_written":
        fail("normal replay terminal state mismatch")
    if normal.get("status") != "PASS":
        fail("normal replay must pass")
    guarded = replay.get("guarded_outcome_replays")
    if not isinstance(guarded, list) or len(guarded) != 8:
        fail("must replay eight guarded outcomes")
    kernel_rules = {state["rule_id"]: state for state in kernel["guarded_outcome_states"]}
    expected_terminal = {
        "allowed_replay_path": "evidence_written",
        "blocked_terminal": "blocked_terminal",
        "owner_review_required": "owner_review_required",
    }
    counts = {
        "allowed_replay_path": 0,
        "blocked_terminal": 0,
        "owner_review_required": 0,
    }
    for replayed in guarded:
        rule_id = replayed.get("rule_id")
        if rule_id not in kernel_rules:
            fail(f"unknown guarded replay rule: {rule_id}")
        state_type = replayed.get("state_type")
        if state_type != kernel_rules[rule_id]["state_type"]:
            fail(f"guarded replay state type mismatch: {rule_id}")
        if replayed.get("terminal_state") != expected_terminal[state_type]:
            fail(f"guarded replay terminal state mismatch: {rule_id}")
        if replayed.get("status") != "PASS":
            fail(f"guarded replay must pass: {rule_id}")
        if replayed.get("protected_action_allowed") is not False:
            fail(f"guarded replay must not allow protected action: {rule_id}")
        counts[state_type] += 1
    if counts != {
        "allowed_replay_path": 1,
        "blocked_terminal": 5,
        "owner_review_required": 2,
    }:
        fail(f"guarded replay counts mismatch: {counts}")
    require_false_flags(replay.get("claim_boundary", {}), "replay result")


def require_replay_gate() -> None:
    gate = read_json(REPLAY_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-replay-harness-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "replay_decision": REPLAY_DECISION,
        "replay_scope": REPLAY_SCOPE,
        "replay_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"replay gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "replay gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_state_machine_kernel_replay_harness_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("replay_decision") != REPLAY_DECISION:
        fail("validation result replay decision mismatch")
    if result.get("unexpected_replay_results") != 0:
        fail("validation result must have zero unexpected replay results")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    kernel = require_kernel_inputs()
    require_replay_result(kernel)
    require_replay_gate()
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

    print("AVF Agent Graph State Machine Kernel Replay Harness v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_replay_harness_v0_1=true")
    print(f"replay_decision={REPLAY_DECISION}")
    print(f"replay_scope={REPLAY_SCOPE}")
    print("normal_path_replayed=true")
    print("normal_terminal_state=evidence_written")
    print("guarded_outcomes_replayed=8")
    print("allowed_replay_outcomes_replayed=1")
    print("blocked_terminal_outcomes_replayed=5")
    print("owner_review_outcomes_replayed=2")
    print("unexpected_replay_results=0")
    print("replay_review_allowed=true")
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
