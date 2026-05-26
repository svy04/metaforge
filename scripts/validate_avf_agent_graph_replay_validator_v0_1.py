from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_replay_validator_v0_1.py"
TRANSITIONS = RUNTIME_GENERATED / "agent_graph_run_state_transitions.json"
TRANSITION_GATE = RUNTIME_GENERATED / "agent_graph_run_state_transitions_gate.json"
REPLAY_RESULT = RUNTIME_GENERATED / "agent_graph_replay_result.json"
GATE = RUNTIME_GENERATED / "agent_graph_replay_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_replay_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_replay_validator_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_REPLAY_VALIDATOR_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_replay_validator_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_run_state_transitions_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_failure_mode_matrix_v0_1"
REPLAY_DECISION = "AGENT_GRAPH_REPLAY_VALIDATOR_READY_FOR_FAILURE_MODE_MATRIX"
REPLAY_SCOPE = "repo_local_deterministic_replay_only"
EXPECTED_STATE_PATH = [
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
    TRANSITIONS,
    TRANSITION_GATE,
    REPLAY_RESULT,
    GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_replay_validator_v0_1=true",
    f"replay_decision={REPLAY_DECISION}",
    f"replay_scope={REPLAY_SCOPE}",
    "replay_passed=true",
    "transitions_replayed=5",
    "terminal_state=evidence_written",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-failure-mode-matrix",
    "owner_approval_required_before_execution: true",
    "Create failure-mode matrix for replay and transition errors",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph Replay Validator v0.1 validation")
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


def require_previous_transitions() -> None:
    transition_gate = read_json(TRANSITION_GATE)
    if transition_gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("transition gate goal mismatch")
    if transition_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("transition gate must point to this replay goal")
    if transition_gate.get("replay_validator_allowed") is not True:
        fail("replay validator must be allowed")
    require_false_flags(transition_gate.get("claim_boundary", {}), "transition gate")

    transitions = read_json(TRANSITIONS)
    if transitions.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("transition model goal mismatch")
    if transitions.get("state_sequence") != EXPECTED_STATE_PATH:
        fail("state sequence mismatch")
    require_false_flags(transitions.get("claim_boundary", {}), "transition model")


def require_replay_result() -> None:
    replay = read_json(REPLAY_RESULT)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "replay_decision": REPLAY_DECISION,
        "replay_scope": REPLAY_SCOPE,
        "replay_passed": True,
        "transitions_replayed": 5,
        "initial_state": "initialized",
        "terminal_state": "evidence_written",
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if replay.get(key) != value:
            fail(f"replay result {key} mismatch")
    if replay.get("state_path") != EXPECTED_STATE_PATH:
        fail("replay state path mismatch")
    if replay.get("replay_errors") != []:
        fail("replay_errors must be empty")
    require_false_flags(replay.get("claim_boundary", {}), "replay result")


def require_gate() -> None:
    gate = read_json(GATE)
    expected = {
        "gate_id": "avf-agent-graph-replay-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "replay_decision": REPLAY_DECISION,
        "replay_scope": REPLAY_SCOPE,
        "replay_passed": True,
        "failure_mode_matrix_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_replay_validator_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("replay_decision") != REPLAY_DECISION:
        fail("validation result decision mismatch")
    if result.get("replay_passed") is not True:
        fail("validation result replay must pass")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_transitions()
    require_replay_result()
    require_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, TEXT_MARKERS + [
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
    ])

    print("AVF Agent Graph Replay Validator v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_replay_validator_v0_1=true")
    print(f"replay_decision={REPLAY_DECISION}")
    print(f"replay_scope={REPLAY_SCOPE}")
    print("replay_passed=true")
    print("transitions_replayed=5")
    print("terminal_state=evidence_written")
    print("failure_mode_matrix_allowed=true")
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
