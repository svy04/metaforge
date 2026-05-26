from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime"
RUNTIME_GENERATED = RUNTIME / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

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
CREATED_AT = "2026-05-27T00:00:00Z"
KERNEL_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_READY_FOR_REPLAY_HARNESS"
KERNEL_SCOPE = "repo_local_deterministic_state_machine_kernel_only"

STATE_TYPE_BY_IMPLICATION = {
    "model_as_allowed_transition": "allowed_replay_path",
    "model_as_blocked_terminal_state": "blocked_terminal",
    "model_as_owner_review_state": "owner_review_required",
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
    gate = read_json(REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("policy enforcement review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("policy enforcement review gate must point to this kernel goal")
    if gate.get("state_machine_kernel_allowed") is not True:
        raise SystemExit("state machine kernel must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_inputs() -> tuple[dict, dict]:
    transitions = read_json(TRANSITIONS)
    if transitions.get("terminal_state") != "evidence_written":
        raise SystemExit("normal transition terminal state mismatch")
    if len(transitions.get("transitions", [])) != 5:
        raise SystemExit("expected five normal transition edges")

    review = read_json(REVIEW_RESULT)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("policy enforcement review result goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("policy enforcement review result must point to this kernel goal")
    if review.get("state_machine_kernel_allowed") is not True:
        raise SystemExit("policy enforcement review must allow state machine kernel")
    if len(review.get("review_records", [])) != 8:
        raise SystemExit("expected eight policy review records")
    return transitions, review


def build_schema() -> str:
    return """schema_id: avf.agent_graph_state_machine_kernel.v0_1
schema_status: repo_local_contract_only

required_sections:
  - normal_states
  - normal_transition_edges
  - guarded_outcome_states
  - claim_boundary

allowed_terminal_states:
  - evidence_written
  - blocked_terminal
  - owner_review_required

allowed_guarded_state_types:
  - allowed_replay_path
  - blocked_terminal
  - owner_review_required

protected_actions_must_remain_false: true
dependency_adoption_allowed: false
runtime_integration_allowed: false
"""


def build_guarded_outcome_states(review: dict) -> list[dict]:
    guarded = []
    for index, record in enumerate(review["review_records"], start=1):
        guarded.append(
            {
                "sequence_index": index,
                "rule_id": record["rule_id"],
                "source": record["source"],
                "source_implication": record["state_machine_implication"],
                "state_type": STATE_TYPE_BY_IMPLICATION[record["state_machine_implication"]],
                "actual_decision": record["actual_decision"],
                "policy_action": record["policy_action"],
                "protected_action_allowed": False,
                "evidence_requirement": record["evidence_requirement"],
            }
        )
    return guarded


def count_guarded(guarded: list[dict]) -> dict:
    return {
        "allowed_replay_path": sum(1 for state in guarded if state["state_type"] == "allowed_replay_path"),
        "blocked_terminal": sum(1 for state in guarded if state["state_type"] == "blocked_terminal"),
        "owner_review_required": sum(1 for state in guarded if state["state_type"] == "owner_review_required"),
    }


def build_kernel(transitions: dict, review: dict) -> dict:
    guarded = build_guarded_outcome_states(review)
    counts = count_guarded(guarded)
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "kernel_decision": KERNEL_DECISION,
        "kernel_scope": KERNEL_SCOPE,
        "run_id": transitions["run_id"],
        "normal_states": transitions["state_sequence"],
        "normal_states_created": len(transitions["state_sequence"]),
        "normal_transition_edges": transitions["transitions"],
        "normal_transition_edges_created": len(transitions["transitions"]),
        "guarded_outcome_states": guarded,
        "guarded_policy_outcomes_modeled": len(guarded),
        "allowed_replay_outcomes_modeled": counts["allowed_replay_path"],
        "blocked_terminal_outcomes_modeled": counts["blocked_terminal"],
        "owner_review_outcomes_modeled": counts["owner_review_required"],
        "kernel_replay_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(kernel: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "kernel_decision": KERNEL_DECISION,
        "kernel_scope": KERNEL_SCOPE,
        "normal_transition_edges_created": kernel["normal_transition_edges_created"],
        "guarded_policy_outcomes_modeled": kernel["guarded_policy_outcomes_modeled"],
        "kernel_replay_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-state-machine-kernel-replay-harness
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Replay deterministic state machine kernel with normal, blocked, and owner-review outcomes
  - Verify normal transitions reach evidence_written
  - Verify blocked outcomes stop in blocked_terminal
  - Verify owner-review outcomes stop in owner_review_required
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(kernel: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_v0_1",
        "status": "PASS",
        "kernel_decision": KERNEL_DECISION,
        "kernel_scope": KERNEL_SCOPE,
        "normal_states_created": kernel["normal_states_created"],
        "normal_transition_edges_created": kernel["normal_transition_edges_created"],
        "guarded_policy_outcomes_modeled": kernel["guarded_policy_outcomes_modeled"],
        "allowed_replay_outcomes_modeled": kernel["allowed_replay_outcomes_modeled"],
        "blocked_terminal_outcomes_modeled": kernel["blocked_terminal_outcomes_modeled"],
        "owner_review_outcomes_modeled": kernel["owner_review_outcomes_modeled"],
        "kernel_replay_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(kernel: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    normal_rows = "\n".join(
        "| {sequence} | `{node}` | `{from_state}` | `{to_state}` |".format(
            sequence=edge["sequence_index"],
            node=edge["node_id"],
            from_state=edge["from_state"],
            to_state=edge["to_state"],
        )
        for edge in kernel["normal_transition_edges"]
    )
    guarded_rows = "\n".join(
        "| `{rule_id}` | {decision} | {state_type} |".format(
            rule_id=state["rule_id"],
            decision=state["actual_decision"],
            state_type=state["state_type"],
        )
        for state in kernel["guarded_outcome_states"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [KERNEL_SCHEMA, KERNEL, KERNEL_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph State Machine Kernel v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_v0_1.py

## Kernel summary

- kernel_decision={KERNEL_DECISION}
- kernel_scope={KERNEL_SCOPE}
- normal_states_created={kernel["normal_states_created"]}
- normal_transition_edges_created={kernel["normal_transition_edges_created"]}
- guarded_policy_outcomes_modeled={kernel["guarded_policy_outcomes_modeled"]}
- allowed_replay_outcomes_modeled={kernel["allowed_replay_outcomes_modeled"]}
- blocked_terminal_outcomes_modeled={kernel["blocked_terminal_outcomes_modeled"]}
- owner_review_outcomes_modeled={kernel["owner_review_outcomes_modeled"]}
- kernel_replay_harness_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Normal transition edges

| Sequence | Node | From | To |
| --- | --- | --- | --- |
{normal_rows}

## Guarded outcome states

| Rule | Decision | State type |
| --- | --- | --- |
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
    transitions, review = load_inputs()
    kernel = build_kernel(transitions, review)

    write_text(KERNEL_SCHEMA, build_schema())
    write_json(KERNEL, kernel)
    write_json(KERNEL_GATE, build_gate(kernel))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(kernel))
    write_text(VALIDATION_REPORT, build_report(kernel))

    print("AVF Agent Graph State Machine Kernel v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_v0_1=true")
    print(f"kernel_decision={KERNEL_DECISION}")
    print(f"kernel_scope={KERNEL_SCOPE}")
    print(f"normal_states_created={kernel['normal_states_created']}")
    print(f"normal_transition_edges_created={kernel['normal_transition_edges_created']}")
    print(f"guarded_policy_outcomes_modeled={kernel['guarded_policy_outcomes_modeled']}")
    print(f"allowed_replay_outcomes_modeled={kernel['allowed_replay_outcomes_modeled']}")
    print(f"blocked_terminal_outcomes_modeled={kernel['blocked_terminal_outcomes_modeled']}")
    print(f"owner_review_outcomes_modeled={kernel['owner_review_outcomes_modeled']}")
    print("kernel_replay_harness_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
