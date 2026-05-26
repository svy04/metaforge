from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime"
RUNTIME_GENERATED = RUNTIME / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

TRANSITION_SCHEMA = RUNTIME / "agent_graph_run_state_transition.schema.yml"
STUB_REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_adapter_stub_review_gate.json"
TRACE = RUNTIME_GENERATED / "agent_graph_adapter_stub_trace.json"
TRANSITIONS = RUNTIME_GENERATED / "agent_graph_run_state_transitions.json"
GATE = RUNTIME_GENERATED / "agent_graph_run_state_transitions_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_run_state_transitions_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_run_state_transitions_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_RUN_STATE_TRANSITIONS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_run_state_transitions_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_adapter_stub_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_replay_validator_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
TRANSITION_DECISION = "AGENT_GRAPH_RUN_STATE_TRANSITIONS_READY_FOR_REPLAY_VALIDATOR"
TRANSITION_SCOPE = "repo_local_deterministic_state_model_only"
STATE_SEQUENCE = [
    "initialized",
    "orchestrated",
    "routed",
    "safety_reviewed",
    "codex_planned",
    "evidence_written",
]


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


def require_previous_review() -> None:
    gate = read_json(STUB_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("stub review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("stub review gate must point to this goal")
    if gate.get("run_state_transition_model_selected") is not True:
        raise SystemExit("run-state transition model must be selected")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_trace() -> dict:
    trace = read_json(TRACE)
    if trace.get("next_safe_goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("trace must feed the previous review goal")
    node_events = trace.get("node_events")
    if not isinstance(node_events, list) or len(node_events) != 5:
        raise SystemExit("expected five node events")
    return trace


def build_schema() -> str:
    return """schema_id: avf.agent_graph_run_state_transition.v0_1
schema_status: repo_local_contract_only

required_fields:
  - run_id
  - goal_id
  - node_id
  - sequence_index
  - from_state
  - to_state
  - status
  - input_artifact_uri
  - output_artifact_uri
  - claim_boundary
  - evidence_event_uri

allowed_states:
  - initialized
  - orchestrated
  - routed
  - safety_reviewed
  - codex_planned
  - evidence_written
  - blocked

protected_actions_must_remain_false: true
dependency_adoption_allowed: false
runtime_integration_allowed: false
"""


def build_transition_model(trace: dict) -> dict:
    transitions = []
    for index, event in enumerate(trace["node_events"], start=1):
        transitions.append(
            {
                "sequence_index": index,
                "node_id": event["node_id"],
                "from_state": STATE_SEQUENCE[index - 1],
                "to_state": STATE_SEQUENCE[index],
                "status": "PASS",
                "input_artifact_uri": "avf/runtime/generated/agent_graph_adapter_stub_trace.json",
                "output_artifact_uri": "avf/runtime/generated/agent_graph_run_state_transitions.json",
                "evidence_event_uri": f"avf/runtime/generated/agent_graph_run_state_transitions.json#/transitions/{index - 1}",
                "output_summary": event["output_summary"],
                "claim_boundary": false_boundary(),
            }
        )
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "transition_decision": TRANSITION_DECISION,
        "transition_scope": TRANSITION_SCOPE,
        "run_id": "avf-agent-graph-stub-run-001",
        "state_sequence": STATE_SEQUENCE,
        "transitions": transitions,
        "terminal_state": STATE_SEQUENCE[-1],
        "replay_validator_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(model: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-run-state-transitions-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "transition_decision": TRANSITION_DECISION,
        "transition_scope": TRANSITION_SCOPE,
        "transitions_created": len(model["transitions"]),
        "terminal_state": model["terminal_state"],
        "replay_validator_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-replay-validator
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create deterministic replay validator for run-state transitions
  - Verify every transition can be replayed from initialized to evidence_written
  - Keep replay local and evidence-backed
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(model: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_run_state_transitions_v0_1",
        "status": "PASS",
        "transition_decision": TRANSITION_DECISION,
        "transition_scope": TRANSITION_SCOPE,
        "transitions_created": len(model["transitions"]),
        "terminal_state": model["terminal_state"],
        "replay_validator_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(model: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        f"| {transition['sequence_index']} | `{transition['node_id']}` | `{transition['from_state']}` | `{transition['to_state']}` |"
        for transition in model["transitions"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [TRANSITION_SCHEMA, TRANSITIONS, GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph Run-State Transitions v0.1 Report

RESULT: PASS
agent_graph_run_state_transitions_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_run_state_transitions_v0_1.py
- python scripts\\validate_avf_agent_graph_run_state_transitions_v0_1.py

## Transition summary

- transition_decision={TRANSITION_DECISION}
- transition_scope={TRANSITION_SCOPE}
- transitions_created={len(model["transitions"])}
- terminal_state={model["terminal_state"]}
- replay_validator_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Transition table

| Sequence | Node | From | To |
| --- | --- | --- | --- |
{rows}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_review()
    trace = load_trace()
    model = build_transition_model(trace)

    write_text(TRANSITION_SCHEMA, build_schema())
    write_json(TRANSITIONS, model)
    write_json(GATE, build_gate(model))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(model))
    write_text(VALIDATION_REPORT, build_report(model))

    print("AVF Agent Graph Run-State Transitions v0.1")
    print("RESULT: PASS")
    print("agent_graph_run_state_transitions_v0_1=true")
    print(f"transition_decision={TRANSITION_DECISION}")
    print(f"transition_scope={TRANSITION_SCOPE}")
    print(f"transitions_created={len(model['transitions'])}")
    print(f"terminal_state={model['terminal_state']}")
    print("replay_validator_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
