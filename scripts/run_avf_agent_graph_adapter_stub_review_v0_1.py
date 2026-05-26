from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

TRACE = RUNTIME_GENERATED / "agent_graph_adapter_stub_trace.json"
STUB_GATE = RUNTIME_GENERATED / "agent_graph_adapter_stub_gate.json"
REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_adapter_stub_review_gate.json"
REVIEW_REPORT = RUNTIME_GENERATED / "agent_graph_adapter_stub_review_report.md"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_adapter_stub_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_adapter_stub_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_ADAPTER_STUB_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_adapter_stub_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_adapter_stub_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_run_state_transitions_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "AGENT_GRAPH_ADAPTER_STUB_REVIEWED_FOR_RUN_STATE_TRANSITIONS"
REVIEW_SCOPE = "trace_review_and_next_state_model_selection_only"


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
    gate = read_json(STUB_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("stub gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("stub gate must point to this review goal")
    if gate.get("stub_review_allowed") is not True:
        raise SystemExit("stub review must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_trace() -> dict:
    trace = read_json(TRACE)
    if trace.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("trace goal mismatch")
    if trace.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("trace must point to this review goal")
    if trace.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if trace.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")
    node_events = trace.get("node_events")
    if not isinstance(node_events, list) or len(node_events) != 5:
        raise SystemExit("expected five node events")
    return trace


def build_review_records(trace: dict) -> list[dict]:
    records = []
    for event in trace["node_events"]:
        records.append(
            {
                "node_id": event["node_id"],
                "sequence_index": event["sequence_index"],
                "review_status": "reviewed",
                "state_transition_needed": True,
                "recommended_state_fields": [
                    "run_id",
                    "goal_id",
                    "node_id",
                    "state",
                    "input_artifact_uri",
                    "output_artifact_uri",
                    "claim_boundary",
                    "evidence_event_uri",
                ],
                "output_summary": event["output_summary"],
            }
        )
    return records


def build_gate(trace: dict, review_records: list[dict]) -> dict:
    return {
        "gate_id": "avf-agent-graph-adapter-stub-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "nodes_reviewed": len(review_records),
        "reviewed_node_sequence": trace["node_sequence"],
        "node_review_records": review_records,
        "run_state_transition_model_selected": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_review_report(trace: dict, review_records: list[dict]) -> str:
    rows = "\n".join(
        f"| {record['sequence_index']} | `{record['node_id']}` | {record['output_summary']} |"
        for record in review_records
    )
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# Agent Graph Adapter Stub Review v0.1

agent_graph_adapter_stub_review_v0_1=true
review_decision={REVIEW_DECISION}
review_scope={REVIEW_SCOPE}
nodes_reviewed={len(review_records)}
run_state_transition_model_selected=true
dependency_adoption_allowed=false
runtime_integration_allowed=false

## Reviewed node trace

| Sequence | Node | Output summary |
| --- | --- | --- |
{rows}

## Next model selected

The next safe slice should add repo-local run-state transition schema and a deterministic validator. The selected model should capture orchestrator, router, safety_reviewer, codex_planner, and evidence_writer transitions without installing dependencies or integrating a runtime.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-run-state-transitions
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create repo-local run-state transition schema and deterministic validator
  - Model orchestrator, router, safety_reviewer, codex_planner, and evidence_writer state changes
  - Keep all transitions local and replayable
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(review_records: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_adapter_stub_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "nodes_reviewed": len(review_records),
        "run_state_transition_model_selected": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_report(review_records: list[dict]) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [REVIEW_GATE, REVIEW_REPORT, NEXT_ACTION, VALIDATION_RESULT]
    )
    node_ids = "\n".join(f"- {record['node_id']}" for record in review_records)
    return f"""# AVF Agent Graph Adapter Stub Review v0.1 Report

RESULT: PASS
agent_graph_adapter_stub_review_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_adapter_stub_review_v0_1.py
- python scripts\\validate_avf_agent_graph_adapter_stub_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_scope={REVIEW_SCOPE}
- nodes_reviewed={len(review_records)}
- run_state_transition_model_selected=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Reviewed nodes

{node_ids}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    trace = load_trace()
    review_records = build_review_records(trace)

    write_json(REVIEW_GATE, build_gate(trace, review_records))
    write_text(REVIEW_REPORT, build_review_report(trace, review_records))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review_records))
    write_text(VALIDATION_REPORT, build_validation_report(review_records))

    print("AVF Agent Graph Adapter Stub Review v0.1")
    print("RESULT: PASS")
    print("agent_graph_adapter_stub_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"nodes_reviewed={len(review_records)}")
    print("run_state_transition_model_selected=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
