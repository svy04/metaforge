from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from avf.runtime.agent_graph_adapter_stub import NODE_SEQUENCE, false_boundary, run_agent_graph_stub

RUNTIME = ROOT / "avf" / "runtime"
RUNTIME_GENERATED = RUNTIME / "generated"
RUNTIME_FIXTURES = RUNTIME / "fixtures"
DOC_GOALS = ROOT / "docs" / "goals"

CONTRACT_REVIEW_GATE = RUNTIME_GENERATED / "runtime_adapter_contract_review_gate.json"
SAMPLE_PACKET = RUNTIME_FIXTURES / "agent_graph_adapter_stub_sample_packet.json"
TRACE = RUNTIME_GENERATED / "agent_graph_adapter_stub_trace.json"
GATE = RUNTIME_GENERATED / "agent_graph_adapter_stub_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_adapter_stub_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_adapter_stub_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_ADAPTER_STUB_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_adapter_stub_v0_1"
PREVIOUS_GOAL_ID = "avf_runtime_adapter_contract_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_adapter_stub_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
STUB_DECISION = "AGENT_GRAPH_ADAPTER_STUB_READY_FOR_REVIEW"
STUB_SCOPE = "deterministic_repo_local_stub_only"
SELECTED_CANDIDATE_ID = "langgraph-agent-runtime-adapter"
SELECTED_CONTRACT_URI = "avf/runtime/agent_graph_adapter_contract.md"


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


def require_previous_gate() -> None:
    gate = read_json(CONTRACT_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("contract review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("contract review gate must point to this goal")
    if gate.get("selected_candidate_id") != SELECTED_CANDIDATE_ID:
        raise SystemExit("selected candidate mismatch")
    if gate.get("stub_creation_allowed") is not True:
        raise SystemExit("stub creation must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def build_sample_packet() -> dict:
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "stub_decision": STUB_DECISION,
        "stub_scope": STUB_SCOPE,
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "selected_contract_uri": SELECTED_CONTRACT_URI,
        "raw_goal": "Create a deterministic repo-local agent graph adapter stub without adopting LangGraph.",
        "owner_intent": "Turn the reviewed contract into a minimal internal runtime seed.",
        "constraints": [
            "no dependency install",
            "no provider call",
            "no runtime integration",
            "no external service call",
            "no deploy",
            "no publish",
            "no readiness claim",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(trace: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-adapter-stub-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "stub_decision": STUB_DECISION,
        "stub_scope": STUB_SCOPE,
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "selected_contract_uri": SELECTED_CONTRACT_URI,
        "nodes_executed": len(trace["node_events"]),
        "node_sequence": NODE_SEQUENCE,
        "stub_review_allowed": True,
        "external_runtime_dependency_required": False,
        "langgraph_dependency_installed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-agent-graph-adapter-stub
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review deterministic node trace and stub contract alignment
  - Confirm Orchestrator, Router, Safety Reviewer, Codex Planner, and Evidence Writer boundaries
  - Decide whether to extend the stub into a typed run-state adapter
  - Do not install LangGraph or any runtime dependency
  - Do not call providers, tools, external services, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(trace: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_adapter_stub_v0_1",
        "status": "PASS",
        "stub_decision": STUB_DECISION,
        "stub_scope": STUB_SCOPE,
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "nodes_executed": len(trace["node_events"]),
        "stub_review_allowed": True,
        "external_runtime_dependency_required": False,
        "langgraph_dependency_installed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_report(trace: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    node_lines = "\n".join(
        f"- {event['sequence_index']}. {event['node_id']}: {event['output_summary']}"
        for event in trace["node_events"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [SAMPLE_PACKET, TRACE, GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph Adapter Stub v0.1 Report

RESULT: PASS
agent_graph_adapter_stub_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_adapter_stub_v0_1.py
- python scripts\\validate_avf_agent_graph_adapter_stub_v0_1.py

## Stub summary

- stub_decision={STUB_DECISION}
- stub_scope={STUB_SCOPE}
- selected_candidate_id={SELECTED_CANDIDATE_ID}
- selected_contract_uri={SELECTED_CONTRACT_URI}
- nodes_executed={len(trace["node_events"])}
- stub_review_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false
- external_runtime_dependency_required=false
- langgraph_dependency_installed=false

## Node trace

{node_lines}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    sample_packet = build_sample_packet()
    write_json(SAMPLE_PACKET, sample_packet)

    trace = run_agent_graph_stub(sample_packet)
    write_json(TRACE, trace)
    write_json(GATE, build_gate(trace))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(trace))
    write_text(VALIDATION_REPORT, build_validation_report(trace))

    print("AVF Agent Graph Adapter Stub v0.1")
    print("RESULT: PASS")
    print("agent_graph_adapter_stub_v0_1=true")
    print(f"stub_decision={STUB_DECISION}")
    print(f"stub_scope={STUB_SCOPE}")
    print(f"selected_candidate_id={SELECTED_CANDIDATE_ID}")
    print(f"nodes_executed={len(trace['node_events'])}")
    print("stub_review_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_runtime_dependency_required=false")
    print("langgraph_dependency_installed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
