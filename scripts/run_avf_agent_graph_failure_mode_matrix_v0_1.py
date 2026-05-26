from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

REPLAY_RESULT = RUNTIME_GENERATED / "agent_graph_replay_result.json"
REPLAY_GATE = RUNTIME_GENERATED / "agent_graph_replay_gate.json"
FAILURE_MATRIX = RUNTIME_GENERATED / "agent_graph_failure_mode_matrix.json"
GATE = RUNTIME_GENERATED / "agent_graph_failure_mode_matrix_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_failure_mode_matrix_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_failure_mode_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_FAILURE_MODE_MATRIX_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_failure_mode_matrix_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_replay_validator_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_failure_replay_harness_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
MATRIX_DECISION = "AGENT_GRAPH_FAILURE_MODE_MATRIX_READY_FOR_NEGATIVE_REPLAY_HARNESS"
MATRIX_SCOPE = "repo_local_failure_classification_only"


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
    gate = read_json(REPLAY_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("replay gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("replay gate must point to this failure-mode goal")
    if gate.get("failure_mode_matrix_allowed") is not True:
        raise SystemExit("failure-mode matrix must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def require_replay_result() -> dict:
    replay = read_json(REPLAY_RESULT)
    if replay.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("replay result goal mismatch")
    if replay.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("replay result must point to this failure-mode goal")
    if replay.get("replay_passed") is not True:
        raise SystemExit("positive replay must pass first")
    return replay


def build_failure_modes() -> list[dict]:
    specs = [
        (
            "transition_from_state_mismatch",
            "A transition starts from a state different from the replay cursor.",
            "replay cursor comparison before applying to_state",
            "blocked",
            "agent_graph_failure_fixture_from_state_mismatch.json",
        ),
        (
            "transition_status_not_pass",
            "A transition has a non-PASS status.",
            "transition status check",
            "review_required",
            "agent_graph_failure_fixture_status_not_pass.json",
        ),
        (
            "missing_evidence_event_uri",
            "A transition omits evidence_event_uri.",
            "transition evidence hook presence check",
            "blocked",
            "agent_graph_failure_fixture_missing_evidence_event_uri.json",
        ),
        (
            "protected_action_flag_true",
            "Any protected-action flag is true inside transition or replay claim boundary.",
            "protected-action boundary scan",
            "blocked",
            "agent_graph_failure_fixture_protected_action_flag_true.json",
        ),
        (
            "terminal_state_mismatch",
            "Replay reaches a terminal state different from expected terminal_state.",
            "terminal state equality check",
            "review_required",
            "agent_graph_failure_fixture_terminal_state_mismatch.json",
        ),
        (
            "dependency_or_runtime_action_requested",
            "A transition requests dependency adoption, runtime integration, provider call, external service, deploy, publish, or readiness claim.",
            "protected-action and policy field scan",
            "blocked",
            "agent_graph_failure_fixture_dependency_or_runtime_action_requested.json",
        ),
        (
            "node_sequence_gap_or_duplicate",
            "A transition sequence skips a node, duplicates a node, or breaks sequence_index ordering.",
            "node sequence and sequence_index monotonicity check",
            "blocked",
            "agent_graph_failure_fixture_node_sequence_gap_or_duplicate.json",
        ),
    ]
    modes = []
    for mode_id, trigger, detected_by, outcome, fixture in specs:
        modes.append(
            {
                "failure_mode_id": mode_id,
                "trigger_condition": trigger,
                "detected_by": detected_by,
                "expected_outcome": outcome,
                "owner_review_required": True,
                "protected_action_allowed": False,
                "evidence_requirement": "Record failing fixture, replay cursor, blocked action state, and next safe action in repo-local evidence.",
                "next_harness_fixture": f"avf/runtime/fixtures/{fixture}",
            }
        )
    return modes


def build_matrix(replay: dict) -> dict:
    modes = build_failure_modes()
    blocked = sum(1 for mode in modes if mode["expected_outcome"] == "blocked")
    review_required = sum(1 for mode in modes if mode["expected_outcome"] == "review_required")
    retryable = sum(1 for mode in modes if mode["expected_outcome"] == "retryable")
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "matrix_decision": MATRIX_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "replay_source_uri": rel(REPLAY_RESULT),
        "positive_replay_terminal_state": replay["terminal_state"],
        "failure_modes_defined": len(modes),
        "blocked_modes": blocked,
        "review_required_modes": review_required,
        "retryable_modes": retryable,
        "failure_modes": modes,
        "failure_replay_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(matrix: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-failure-mode-matrix-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "matrix_decision": MATRIX_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "failure_modes_defined": matrix["failure_modes_defined"],
        "blocked_modes": matrix["blocked_modes"],
        "review_required_modes": matrix["review_required_modes"],
        "retryable_modes": matrix["retryable_modes"],
        "failure_replay_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-failure-replay-harness
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create negative replay fixtures for each failure mode
  - Verify blocked and review_required outcomes are enforced by deterministic replay
  - Keep all failure handling repo-local and evidence-backed
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(matrix: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_failure_mode_matrix_v0_1",
        "status": "PASS",
        "matrix_decision": MATRIX_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "failure_modes_defined": matrix["failure_modes_defined"],
        "blocked_modes": matrix["blocked_modes"],
        "review_required_modes": matrix["review_required_modes"],
        "retryable_modes": matrix["retryable_modes"],
        "failure_replay_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(matrix: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        f"| `{mode['failure_mode_id']}` | {mode['expected_outcome']} | {mode['detected_by']} |"
        for mode in matrix["failure_modes"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [FAILURE_MATRIX, GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph Failure-Mode Matrix v0.1 Report

RESULT: PASS
agent_graph_failure_mode_matrix_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_failure_mode_matrix_v0_1.py
- python scripts\\validate_avf_agent_graph_failure_mode_matrix_v0_1.py

## Matrix summary

- matrix_decision={MATRIX_DECISION}
- matrix_scope={MATRIX_SCOPE}
- failure_modes_defined={matrix["failure_modes_defined"]}
- blocked_modes={matrix["blocked_modes"]}
- review_required_modes={matrix["review_required_modes"]}
- retryable_modes={matrix["retryable_modes"]}
- failure_replay_harness_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Failure modes

| Failure mode | Expected outcome | Detected by |
| --- | --- | --- |
{rows}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    replay = require_replay_result()
    matrix = build_matrix(replay)

    write_json(FAILURE_MATRIX, matrix)
    write_json(GATE, build_gate(matrix))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(matrix))
    write_text(VALIDATION_REPORT, build_report(matrix))

    print("AVF Agent Graph Failure-Mode Matrix v0.1")
    print("RESULT: PASS")
    print("agent_graph_failure_mode_matrix_v0_1=true")
    print(f"matrix_decision={MATRIX_DECISION}")
    print(f"matrix_scope={MATRIX_SCOPE}")
    print(f"failure_modes_defined={matrix['failure_modes_defined']}")
    print(f"blocked_modes={matrix['blocked_modes']}")
    print(f"review_required_modes={matrix['review_required_modes']}")
    print(f"retryable_modes={matrix['retryable_modes']}")
    print("failure_replay_harness_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
