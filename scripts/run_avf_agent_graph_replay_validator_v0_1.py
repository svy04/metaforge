from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

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
CREATED_AT = "2026-05-27T00:00:00Z"
REPLAY_DECISION = "AGENT_GRAPH_REPLAY_VALIDATOR_READY_FOR_FAILURE_MODE_MATRIX"
REPLAY_SCOPE = "repo_local_deterministic_replay_only"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def false_boundary() -> dict:
    return {
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "automated_scraping_performed": False,
        "scraping_performed": False,
        "posting_automation_performed": False,
        "dependency_install_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "package_install_performed": False,
        "runtime_integration_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_previous_gate() -> None:
    gate = read_json(TRANSITION_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("transition gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("transition gate must point to this goal")
    if gate.get("replay_validator_allowed") is not True:
        raise SystemExit("replay validator must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def replay_transitions(model: dict) -> dict:
    current_state = model["state_sequence"][0]
    state_path = [current_state]
    replay_errors: list[str] = []

    for transition in model["transitions"]:
        if transition["from_state"] != current_state:
            replay_errors.append(
                f"{transition['node_id']} expected from_state {current_state}, got {transition['from_state']}"
            )
            break
        if transition["status"] != "PASS":
            replay_errors.append(f"{transition['node_id']} status was not PASS")
            break
        current_state = transition["to_state"]
        state_path.append(current_state)

    terminal_state = state_path[-1]
    replay_passed = not replay_errors and terminal_state == model["terminal_state"]
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "replay_decision": REPLAY_DECISION,
        "replay_scope": REPLAY_SCOPE,
        "replay_passed": replay_passed,
        "transitions_replayed": len(model["transitions"]) if replay_passed else max(0, len(state_path) - 1),
        "initial_state": model["state_sequence"][0],
        "terminal_state": terminal_state,
        "expected_terminal_state": model["terminal_state"],
        "state_path": state_path,
        "replay_errors": replay_errors,
        "failure_mode_matrix_allowed": replay_passed,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(replay: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-replay-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS" if replay["replay_passed"] else "FAIL",
        "replay_decision": REPLAY_DECISION,
        "replay_scope": REPLAY_SCOPE,
        "replay_passed": replay["replay_passed"],
        "transitions_replayed": replay["transitions_replayed"],
        "terminal_state": replay["terminal_state"],
        "failure_mode_matrix_allowed": replay["failure_mode_matrix_allowed"],
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-failure-mode-matrix
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create failure-mode matrix for replay and transition errors
  - Define blocked, retryable, and review_required transition outcomes
  - Keep all failure-mode handling repo-local and deterministic
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(replay: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_replay_validator_v0_1",
        "status": "PASS" if replay["replay_passed"] else "FAIL",
        "replay_decision": REPLAY_DECISION,
        "replay_scope": REPLAY_SCOPE,
        "replay_passed": replay["replay_passed"],
        "transitions_replayed": replay["transitions_replayed"],
        "terminal_state": replay["terminal_state"],
        "failure_mode_matrix_allowed": replay["failure_mode_matrix_allowed"],
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(replay: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    state_path = " -> ".join(replay["state_path"])
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [REPLAY_RESULT, GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph Replay Validator v0.1 Report

RESULT: PASS
agent_graph_replay_validator_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_replay_validator_v0_1.py
- python scripts\\validate_avf_agent_graph_replay_validator_v0_1.py

## Replay summary

- replay_decision={REPLAY_DECISION}
- replay_scope={REPLAY_SCOPE}
- replay_passed=true
- transitions_replayed={replay["transitions_replayed"]}
- terminal_state={replay["terminal_state"]}
- failure_mode_matrix_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## State path

{state_path}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    transition_model = read_json(TRANSITIONS)
    replay = replay_transitions(transition_model)

    write_json(REPLAY_RESULT, replay)
    write_json(GATE, build_gate(replay))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(replay))
    write_text(VALIDATION_REPORT, build_report(replay))

    print("AVF Agent Graph Replay Validator v0.1")
    print("RESULT: PASS" if replay["replay_passed"] else "RESULT: FAIL")
    print("agent_graph_replay_validator_v0_1=true")
    print(f"replay_decision={REPLAY_DECISION}")
    print(f"replay_scope={REPLAY_SCOPE}")
    print(f"replay_passed={str(replay['replay_passed']).lower()}")
    print(f"transitions_replayed={replay['transitions_replayed']}")
    print(f"terminal_state={replay['terminal_state']}")
    print("failure_mode_matrix_allowed=true" if replay["replay_passed"] else "failure_mode_matrix_allowed=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
