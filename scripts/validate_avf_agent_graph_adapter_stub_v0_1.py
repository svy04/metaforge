from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime"
RUNTIME_GENERATED = RUNTIME / "generated"
RUNTIME_FIXTURES = RUNTIME / "fixtures"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_adapter_stub_v0_1.py"
STUB = RUNTIME / "agent_graph_adapter_stub.py"
SAMPLE_PACKET = RUNTIME_FIXTURES / "agent_graph_adapter_stub_sample_packet.json"
CONTRACT_REVIEW_GATE = RUNTIME_GENERATED / "runtime_adapter_contract_review_gate.json"
TRACE = RUNTIME_GENERATED / "agent_graph_adapter_stub_trace.json"
GATE = RUNTIME_GENERATED / "agent_graph_adapter_stub_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_adapter_stub_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_adapter_stub_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_ADAPTER_STUB_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_adapter_stub_v0_1"
PREVIOUS_GOAL_ID = "avf_runtime_adapter_contract_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_adapter_stub_review_v0_1"
STUB_DECISION = "AGENT_GRAPH_ADAPTER_STUB_READY_FOR_REVIEW"
STUB_SCOPE = "deterministic_repo_local_stub_only"
SELECTED_CANDIDATE_ID = "langgraph-agent-runtime-adapter"
EXPECTED_NODES = [
    "orchestrator",
    "router",
    "safety_reviewer",
    "codex_planner",
    "evidence_writer",
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
    STUB,
    SAMPLE_PACKET,
    CONTRACT_REVIEW_GATE,
    TRACE,
    GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_adapter_stub_v0_1=true",
    f"stub_decision={STUB_DECISION}",
    f"stub_scope={STUB_SCOPE}",
    f"selected_candidate_id={SELECTED_CANDIDATE_ID}",
    "nodes_executed=5",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "external_runtime_dependency_required=false",
    "langgraph_dependency_installed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-agent-graph-adapter-stub",
    "owner_approval_required_before_execution: true",
    "Review deterministic node trace and stub contract alignment",
    "Do not install LangGraph or any runtime dependency",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph Adapter Stub v0.1 validation")
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


def require_contract_review_gate() -> None:
    gate = read_json(CONTRACT_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("contract review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("contract review gate must point to this stub goal")
    if gate.get("selected_candidate_id") != SELECTED_CANDIDATE_ID:
        fail("contract review selected candidate mismatch")
    if gate.get("stub_creation_allowed") is not True:
        fail("stub creation must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        fail("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        fail("runtime integration must remain blocked")
    require_false_flags(gate.get("claim_boundary", {}), "contract review gate")


def require_stub_source() -> None:
    text = read(STUB)
    blocked_imports = ["import langgraph", "from langgraph"]
    for marker in blocked_imports:
        if marker in text.lower():
            fail(f"stub must not contain {marker}")
    for marker in [
        "def run_agent_graph_stub",
        "NODE_SEQUENCE",
        "orchestrator",
        "safety_reviewer",
        "evidence_writer",
    ]:
        if marker not in text:
            fail(f"stub source missing {marker}")


def require_trace() -> None:
    trace = read_json(TRACE)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "stub_decision": STUB_DECISION,
        "stub_scope": STUB_SCOPE,
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "external_runtime_dependency_required": False,
        "langgraph_dependency_installed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if trace.get(key) != value:
            fail(f"trace {key} mismatch")
    if trace.get("node_sequence") != EXPECTED_NODES:
        fail("node sequence mismatch")
    node_events = trace.get("node_events")
    if not isinstance(node_events, list) or len(node_events) != len(EXPECTED_NODES):
        fail("trace must contain five node events")
    for idx, (event, node_id) in enumerate(zip(node_events, EXPECTED_NODES), start=1):
        if event.get("node_id") != node_id:
            fail(f"node event mismatch for {node_id}")
        if event.get("status") != "PASS":
            fail(f"node event status must be PASS for {node_id}")
        if event.get("sequence_index") != idx:
            fail(f"node event sequence mismatch for {node_id}")
        if not event.get("output_summary"):
            fail(f"node event missing output summary for {node_id}")
    require_false_flags(trace.get("claim_boundary", {}), "trace")


def require_gate() -> None:
    gate = read_json(GATE)
    expected = {
        "gate_id": "avf-agent-graph-adapter-stub-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "stub_decision": STUB_DECISION,
        "stub_scope": STUB_SCOPE,
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "nodes_executed": len(EXPECTED_NODES),
        "stub_review_allowed": True,
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
    if result.get("validator_id") != "validate_avf_agent_graph_adapter_stub_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("stub_decision") != STUB_DECISION:
        fail("validation result decision mismatch")
    if result.get("nodes_executed") != len(EXPECTED_NODES):
        fail("validation result node count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_contract_review_gate()
    require_stub_source()
    require_trace()
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

    print("AVF Agent Graph Adapter Stub v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_adapter_stub_v0_1=true")
    print(f"stub_decision={STUB_DECISION}")
    print(f"stub_scope={STUB_SCOPE}")
    print(f"selected_candidate_id={SELECTED_CANDIDATE_ID}")
    print("nodes_executed=5")
    print("stub_review_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_runtime_dependency_required=false")
    print("langgraph_dependency_installed=false")
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
