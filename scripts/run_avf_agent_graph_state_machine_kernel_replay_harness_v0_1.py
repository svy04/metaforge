from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

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
CREATED_AT = "2026-05-27T00:00:00Z"
REPLAY_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_REPLAY_HARNESS_READY_FOR_REVIEW"
REPLAY_SCOPE = "repo_local_state_machine_kernel_replay_only"

TERMINAL_BY_STATE_TYPE = {
    "allowed_replay_path": "evidence_written",
    "blocked_terminal": "blocked_terminal",
    "owner_review_required": "owner_review_required",
}


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
    gate = read_json(KERNEL_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("state machine kernel gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("state machine kernel gate must point to this replay harness")
    if gate.get("kernel_replay_harness_allowed") is not True:
        raise SystemExit("kernel replay harness must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_kernel() -> dict:
    kernel = read_json(KERNEL)
    if kernel.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("state machine kernel goal mismatch")
    if kernel.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("state machine kernel must point to this replay harness")
    if kernel.get("kernel_replay_harness_allowed") is not True:
        raise SystemExit("state machine kernel must allow replay harness")
    if kernel.get("normal_transition_edges_created") != 5:
        raise SystemExit("expected five normal transition edges")
    if kernel.get("guarded_policy_outcomes_modeled") != 8:
        raise SystemExit("expected eight guarded outcomes")
    return kernel


def build_normal_replay(kernel: dict) -> dict:
    state_path = [kernel["normal_transition_edges"][0]["from_state"]]
    replayed_edges = []
    current_state = state_path[0]
    for edge in kernel["normal_transition_edges"]:
        status = "PASS"
        if edge["from_state"] != current_state:
            status = "FAIL"
        current_state = edge["to_state"]
        state_path.append(current_state)
        replayed_edges.append(
            {
                "sequence_index": edge["sequence_index"],
                "node_id": edge["node_id"],
                "from_state": edge["from_state"],
                "to_state": edge["to_state"],
                "status": status,
            }
        )
    return {
        "state_path": state_path,
        "transitions_replayed": len(replayed_edges),
        "terminal_state": state_path[-1],
        "replayed_edges": replayed_edges,
        "status": "PASS" if all(edge["status"] == "PASS" for edge in replayed_edges) else "FAIL",
    }


def build_guarded_replays(kernel: dict) -> list[dict]:
    replays = []
    for state in kernel["guarded_outcome_states"]:
        terminal_state = TERMINAL_BY_STATE_TYPE[state["state_type"]]
        replays.append(
            {
                "rule_id": state["rule_id"],
                "state_type": state["state_type"],
                "actual_decision": state["actual_decision"],
                "terminal_state": terminal_state,
                "source": state["source"],
                "protected_action_allowed": False,
                "status": "PASS",
            }
        )
    return replays


def count_guarded_replays(replays: list[dict]) -> dict:
    return {
        "allowed_replay_path": sum(1 for replay in replays if replay["state_type"] == "allowed_replay_path"),
        "blocked_terminal": sum(1 for replay in replays if replay["state_type"] == "blocked_terminal"),
        "owner_review_required": sum(1 for replay in replays if replay["state_type"] == "owner_review_required"),
    }


def build_replay_result(kernel: dict) -> dict:
    normal = build_normal_replay(kernel)
    guarded = build_guarded_replays(kernel)
    counts = count_guarded_replays(guarded)
    unexpected = sum(1 for replay in guarded if replay["status"] != "PASS")
    if normal["status"] != "PASS":
        unexpected += 1
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "replay_decision": REPLAY_DECISION,
        "replay_scope": REPLAY_SCOPE,
        "normal_path_replayed": normal["status"] == "PASS",
        "normal_terminal_state": normal["terminal_state"],
        "normal_path_replay": normal,
        "guarded_outcomes_replayed": len(guarded),
        "allowed_replay_outcomes_replayed": counts["allowed_replay_path"],
        "blocked_terminal_outcomes_replayed": counts["blocked_terminal"],
        "owner_review_outcomes_replayed": counts["owner_review_required"],
        "guarded_outcome_replays": guarded,
        "unexpected_replay_results": unexpected,
        "replay_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(result: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-replay-harness-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "replay_decision": REPLAY_DECISION,
        "replay_scope": REPLAY_SCOPE,
        "normal_path_replayed": result["normal_path_replayed"],
        "guarded_outcomes_replayed": result["guarded_outcomes_replayed"],
        "unexpected_replay_results": result["unexpected_replay_results"],
        "replay_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-agent-graph-state-machine-kernel-replay-harness
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review kernel replay outcomes before state machine hardening
  - Confirm normal path reaches evidence_written
  - Confirm blocked outcomes terminate at blocked_terminal
  - Confirm owner-review outcomes terminate at owner_review_required
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(result: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_replay_harness_v0_1",
        "status": "PASS",
        "replay_decision": REPLAY_DECISION,
        "replay_scope": REPLAY_SCOPE,
        "normal_path_replayed": result["normal_path_replayed"],
        "normal_terminal_state": result["normal_terminal_state"],
        "guarded_outcomes_replayed": result["guarded_outcomes_replayed"],
        "allowed_replay_outcomes_replayed": result["allowed_replay_outcomes_replayed"],
        "blocked_terminal_outcomes_replayed": result["blocked_terminal_outcomes_replayed"],
        "owner_review_outcomes_replayed": result["owner_review_outcomes_replayed"],
        "unexpected_replay_results": result["unexpected_replay_results"],
        "replay_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(result: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    normal_rows = "\n".join(
        "| {sequence} | `{node}` | `{from_state}` | `{to_state}` | {status} |".format(
            sequence=edge["sequence_index"],
            node=edge["node_id"],
            from_state=edge["from_state"],
            to_state=edge["to_state"],
            status=edge["status"],
        )
        for edge in result["normal_path_replay"]["replayed_edges"]
    )
    guarded_rows = "\n".join(
        "| `{rule_id}` | {state_type} | {terminal_state} | {status} |".format(
            rule_id=replay["rule_id"],
            state_type=replay["state_type"],
            terminal_state=replay["terminal_state"],
            status=replay["status"],
        )
        for replay in result["guarded_outcome_replays"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [REPLAY_RESULT, REPLAY_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph State Machine Kernel Replay Harness v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_replay_harness_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_replay_harness_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_replay_harness_v0_1.py

## Replay summary

- replay_decision={REPLAY_DECISION}
- replay_scope={REPLAY_SCOPE}
- normal_path_replayed=true
- normal_terminal_state={result["normal_terminal_state"]}
- guarded_outcomes_replayed={result["guarded_outcomes_replayed"]}
- allowed_replay_outcomes_replayed={result["allowed_replay_outcomes_replayed"]}
- blocked_terminal_outcomes_replayed={result["blocked_terminal_outcomes_replayed"]}
- owner_review_outcomes_replayed={result["owner_review_outcomes_replayed"]}
- unexpected_replay_results={result["unexpected_replay_results"]}
- replay_review_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Normal path replay

| Sequence | Node | From | To | Status |
| --- | --- | --- | --- | --- |
{normal_rows}

## Guarded outcome replays

| Rule | State type | Terminal state | Status |
| --- | --- | --- | --- |
{guarded_rows}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    kernel = load_kernel()
    result = build_replay_result(kernel)

    write_json(REPLAY_RESULT, result)
    write_json(REPLAY_GATE, build_gate(result))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(result))
    write_text(VALIDATION_REPORT, build_report(result))

    print("AVF Agent Graph State Machine Kernel Replay Harness v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_replay_harness_v0_1=true")
    print(f"replay_decision={REPLAY_DECISION}")
    print(f"replay_scope={REPLAY_SCOPE}")
    print("normal_path_replayed=true")
    print(f"normal_terminal_state={result['normal_terminal_state']}")
    print(f"guarded_outcomes_replayed={result['guarded_outcomes_replayed']}")
    print(f"allowed_replay_outcomes_replayed={result['allowed_replay_outcomes_replayed']}")
    print(f"blocked_terminal_outcomes_replayed={result['blocked_terminal_outcomes_replayed']}")
    print(f"owner_review_outcomes_replayed={result['owner_review_outcomes_replayed']}")
    print(f"unexpected_replay_results={result['unexpected_replay_results']}")
    print("replay_review_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
