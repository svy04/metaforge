from __future__ import annotations

from copy import deepcopy
from typing import Any


NODE_SEQUENCE = [
    "orchestrator",
    "router",
    "safety_reviewer",
    "codex_planner",
    "evidence_writer",
]


def false_boundary() -> dict[str, bool]:
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


def _event(sequence_index: int, node_id: str, output_summary: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "sequence_index": sequence_index,
        "node_id": node_id,
        "status": "PASS",
        "output_summary": output_summary,
        "payload": payload,
        "claim_boundary": false_boundary(),
    }


def run_agent_graph_stub(packet: dict[str, Any]) -> dict[str, Any]:
    """Run a deterministic, dependency-free AVF agent graph skeleton."""
    working = deepcopy(packet)

    orchestrator_payload = {
        "goal_id": working["goal_id"],
        "goal_essence": "Create a repo-local adapter stub without adopting external runtime dependencies.",
        "selected_candidate_id": working["selected_candidate_id"],
    }

    router_payload = {
        "primary_track": "Runtime & Tooling Engine",
        "secondary_tracks": ["Evidence & Learning Engine", "Governance & Safety Engine"],
        "required_cells": ["runtime_cell", "safety_cell", "codex_planner_cell", "evidence_cell"],
    }

    safety_payload = {
        "risk_tier": "yellow",
        "allowed_creation_level": "Level 2 Local Artifact",
        "blocked_actions": [
            "dependency_install",
            "runtime_integration",
            "provider_call",
            "external_service_call",
            "deploy",
            "publish",
            "readiness_claim",
        ],
        "claim_boundary": false_boundary(),
    }

    codex_payload = {
        "task_id": "avf-agent-graph-adapter-stub-v0-1",
        "scope": "repo-local deterministic adapter stub only",
        "files_likely_to_touch": [
            "avf/runtime/agent_graph_adapter_stub.py",
            "scripts/run_avf_agent_graph_adapter_stub_v0_1.py",
            "scripts/validate_avf_agent_graph_adapter_stub_v0_1.py",
        ],
        "forbidden_changes": [
            "install LangGraph",
            "call providers",
            "start runtime workers",
            "perform external actions",
        ],
    }

    evidence_payload = {
        "evidence_event_type": "local_stub_trace",
        "artifact_uri": "avf/runtime/generated/agent_graph_adapter_stub_trace.json",
        "validation_method": "python scripts\\validate_avf_agent_graph_adapter_stub_v0_1.py",
        "next_safe_goal_id": working["next_safe_goal_id"],
    }

    node_events = [
        _event(1, "orchestrator", "Goal normalized into a local adapter stub run.", orchestrator_payload),
        _event(2, "router", "Runtime, safety, Codex, and evidence cells selected.", router_payload),
        _event(3, "safety_reviewer", "Protected actions blocked and local artifact scope confirmed.", safety_payload),
        _event(4, "codex_planner", "PR-sized deterministic stub task emitted.", codex_payload),
        _event(5, "evidence_writer", "Trace and validation artifact contract emitted.", evidence_payload),
    ]

    return {
        "goal_id": working["goal_id"],
        "previous_goal_id": working["previous_goal_id"],
        "created_at": working["created_at"],
        "stub_decision": working["stub_decision"],
        "stub_scope": working["stub_scope"],
        "selected_candidate_id": working["selected_candidate_id"],
        "selected_contract_uri": working["selected_contract_uri"],
        "external_runtime_dependency_required": False,
        "langgraph_dependency_installed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "node_sequence": NODE_SEQUENCE,
        "node_events": node_events,
        "next_safe_goal_id": working["next_safe_goal_id"],
        "claim_boundary": false_boundary(),
    }
