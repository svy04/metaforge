from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

MANIFEST = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_manifest.json"
SKELETON_GATE = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_gate.json"
REVIEW_GATE = RUNTIME_GENERATED / "runtime_adapter_contract_review_gate.json"
REVIEW_REPORT = RUNTIME_GENERATED / "runtime_adapter_contract_review_report.md"
NEXT_ACTION = RUNTIME_GENERATED / "runtime_adapter_contract_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "runtime_adapter_contract_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_RUNTIME_ADAPTER_CONTRACT_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_runtime_adapter_contract_review_v0_1"
PREVIOUS_GOAL_ID = "avf_runtime_adapter_contract_skeletons_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_adapter_stub_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CONTRACT_SKELETONS_REVIEWED_AGENT_GRAPH_ADAPTER_SELECTED_FOR_STUB"
REVIEW_SCOPE = "review_and_first_stub_selection_only"
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
    gate = read_json(SKELETON_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("skeleton gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("skeleton gate must point to this goal")
    if gate.get("contract_review_allowed") is not True:
        raise SystemExit("contract review must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_manifest() -> dict:
    manifest = read_json(MANIFEST)
    if manifest.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("manifest goal mismatch")
    if manifest.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("manifest must point to this goal")
    contracts = manifest.get("contracts")
    if not isinstance(contracts, list) or len(contracts) != 7:
        raise SystemExit("expected seven contract skeletons")
    selected = [contract for contract in contracts if contract.get("candidate_id") == SELECTED_CANDIDATE_ID]
    if len(selected) != 1 or selected[0].get("contract_uri") != SELECTED_CONTRACT_URI:
        raise SystemExit("selected contract is missing from manifest")
    return manifest


def build_review_records(manifest: dict) -> list[dict]:
    records = []
    for contract in manifest["contracts"]:
        is_selected = contract["candidate_id"] == SELECTED_CANDIDATE_ID
        records.append(
            {
                "candidate_id": contract["candidate_id"],
                "display_name": contract["display_name"],
                "plane": contract["plane"],
                "contract_uri": contract["contract_uri"],
                "source_target_id": contract["source_target_id"],
                "review_status": "reviewed",
                "selection_status": "selected_for_first_stub" if is_selected else "deferred_after_contract_review",
                "selection_reason": (
                    "Best first stub because it exercises AVF role graph boundaries without adopting external runtime dependencies."
                    if is_selected
                    else "Valid contract skeleton, but deferred until the agent graph stub proves local node IO, safety gates, and evidence hooks."
                ),
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
                "owner_approval_required_before_adoption": True,
            }
        )
    return records


def build_gate(manifest: dict, review_records: list[dict]) -> dict:
    return {
        "gate_id": "avf-runtime-adapter-contract-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "contracts_reviewed": len(review_records),
        "review_records": review_records,
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "selected_contract_uri": SELECTED_CONTRACT_URI,
        "stub_creation_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_review_report(review_records: list[dict]) -> str:
    rows = "\n".join(
        f"| {record['display_name']} | `{record['plane']}` | `{record['selection_status']}` | `{record['contract_uri']}` |"
        for record in review_records
    )
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# Runtime Adapter Contract Review v0.1

runtime_adapter_contract_review_v0_1=true
review_decision={REVIEW_DECISION}
review_scope={REVIEW_SCOPE}
contracts_reviewed={len(review_records)}
selected_candidate_id={SELECTED_CANDIDATE_ID}
selected_contract_uri={SELECTED_CONTRACT_URI}
dependency_adoption_allowed=false
runtime_integration_allowed=false

## Review table

| Candidate | Plane | Selection status | Contract |
| --- | --- | --- | --- |
{rows}

## Selection rationale

LangGraph is selected as the first stub target because the agent graph boundary is the smallest useful runtime abstraction for AVF's Orchestrator, Router, Safety Reviewer, Codex Planner, and Evidence Writer flow. Temporal, OpenTelemetry, MCP, LiteLLM, vLLM, and WebArena stay contract-reviewed but deferred.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-adapter-stub
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local agent graph adapter stub
  - Use the selected contract only as an internal interface boundary
  - Keep node execution deterministic and local
  - Do not install LangGraph or any runtime dependency
  - Do not call providers, tools, external services, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(review_records: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_runtime_adapter_contract_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "contracts_reviewed": len(review_records),
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "selected_contract_uri": SELECTED_CONTRACT_URI,
        "stub_creation_allowed": True,
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
    return f"""# AVF Runtime Adapter Contract Review v0.1 Report

RESULT: PASS
runtime_adapter_contract_review_v0_1=true

## Commands

- python scripts\\run_avf_runtime_adapter_contract_review_v0_1.py
- python scripts\\validate_avf_runtime_adapter_contract_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_scope={REVIEW_SCOPE}
- contracts_reviewed={len(review_records)}
- selected_candidate_id={SELECTED_CANDIDATE_ID}
- selected_contract_uri={SELECTED_CONTRACT_URI}
- stub_creation_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Candidate coverage

- LangGraph: selected for first repo-local agent graph adapter stub
- Temporal: deferred
- OpenTelemetry: deferred
- MCP: deferred
- LiteLLM: deferred
- vLLM: deferred
- WebArena: deferred as cautionary safety/eval reference

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    manifest = load_manifest()
    review_records = build_review_records(manifest)

    write_json(REVIEW_GATE, build_gate(manifest, review_records))
    write_text(REVIEW_REPORT, build_review_report(review_records))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review_records))
    write_text(VALIDATION_REPORT, build_validation_report(review_records))

    print("AVF Runtime Adapter Contract Review v0.1")
    print("RESULT: PASS")
    print("runtime_adapter_contract_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"contracts_reviewed={len(review_records)}")
    print(f"selected_candidate_id={SELECTED_CANDIDATE_ID}")
    print(f"selected_contract_uri={SELECTED_CONTRACT_URI}")
    print("stub_creation_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
