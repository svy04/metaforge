from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime"
RUNTIME_GENERATED = RUNTIME / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_run_state_transitions_v0_1.py"
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
TRANSITION_DECISION = "AGENT_GRAPH_RUN_STATE_TRANSITIONS_READY_FOR_REPLAY_VALIDATOR"
TRANSITION_SCOPE = "repo_local_deterministic_state_model_only"
EXPECTED_NODES = [
    "orchestrator",
    "router",
    "safety_reviewer",
    "codex_planner",
    "evidence_writer",
]
EXPECTED_STATES = [
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
    TRANSITION_SCHEMA,
    STUB_REVIEW_GATE,
    TRACE,
    TRANSITIONS,
    GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

SCHEMA_MARKERS = [
    "schema_id: avf.agent_graph_run_state_transition.v0_1",
    "required_fields:",
    "run_id",
    "goal_id",
    "node_id",
    "from_state",
    "to_state",
    "claim_boundary",
    "evidence_event_uri",
    "protected_actions_must_remain_false: true",
]

TEXT_MARKERS = [
    "agent_graph_run_state_transitions_v0_1=true",
    f"transition_decision={TRANSITION_DECISION}",
    f"transition_scope={TRANSITION_SCOPE}",
    "transitions_created=5",
    "terminal_state=evidence_written",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-replay-validator",
    "owner_approval_required_before_execution: true",
    "Create deterministic replay validator for run-state transitions",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph Run-State Transitions v0.1 validation")
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


def require_previous_review() -> None:
    gate = read_json(STUB_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("stub review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("stub review gate must point to this transitions goal")
    if gate.get("run_state_transition_model_selected") is not True:
        fail("run-state model must be selected")
    require_false_flags(gate.get("claim_boundary", {}), "stub review gate")

    trace = read_json(TRACE)
    if trace.get("node_sequence") != EXPECTED_NODES:
        fail("trace node sequence mismatch")
    require_false_flags(trace.get("claim_boundary", {}), "trace")


def require_transitions() -> None:
    data = read_json(TRANSITIONS)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "transition_decision": TRANSITION_DECISION,
        "transition_scope": TRANSITION_SCOPE,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "terminal_state": "evidence_written",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            fail(f"transitions {key} mismatch")
    if data.get("state_sequence") != EXPECTED_STATES:
        fail("state sequence mismatch")
    transitions = data.get("transitions")
    if not isinstance(transitions, list) or len(transitions) != len(EXPECTED_NODES):
        fail("must contain five transitions")
    for idx, (transition, node_id) in enumerate(zip(transitions, EXPECTED_NODES), start=1):
        if transition.get("sequence_index") != idx:
            fail(f"transition index mismatch for {node_id}")
        if transition.get("node_id") != node_id:
            fail(f"transition node mismatch for {node_id}")
        if transition.get("from_state") != EXPECTED_STATES[idx - 1]:
            fail(f"from_state mismatch for {node_id}")
        if transition.get("to_state") != EXPECTED_STATES[idx]:
            fail(f"to_state mismatch for {node_id}")
        if transition.get("status") != "PASS":
            fail(f"transition status mismatch for {node_id}")
        if not transition.get("evidence_event_uri"):
            fail(f"transition missing evidence_event_uri for {node_id}")
        require_false_flags(transition.get("claim_boundary", {}), f"transition {node_id}")
    require_false_flags(data.get("claim_boundary", {}), "transitions")


def require_gate() -> None:
    gate = read_json(GATE)
    expected = {
        "gate_id": "avf-agent-graph-run-state-transitions-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "transition_decision": TRANSITION_DECISION,
        "transition_scope": TRANSITION_SCOPE,
        "transitions_created": len(EXPECTED_NODES),
        "replay_validator_allowed": True,
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
    if result.get("validator_id") != "validate_avf_agent_graph_run_state_transitions_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("transition_decision") != TRANSITION_DECISION:
        fail("validation result decision mismatch")
    if result.get("transitions_created") != len(EXPECTED_NODES):
        fail("validation result transition count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_text_markers(TRANSITION_SCHEMA, SCHEMA_MARKERS)
    require_previous_review()
    require_transitions()
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

    print("AVF Agent Graph Run-State Transitions v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_run_state_transitions_v0_1=true")
    print(f"transition_decision={TRANSITION_DECISION}")
    print(f"transition_scope={TRANSITION_SCOPE}")
    print("transitions_created=5")
    print("terminal_state=evidence_written")
    print("replay_validator_allowed=true")
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
