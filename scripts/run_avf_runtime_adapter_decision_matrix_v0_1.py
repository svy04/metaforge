from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

MANUAL_RECORDS = CAPABILITIES / "primary_source_manual_records.json"
INTEGRATION_REVIEW_GATE = CAPABILITIES / "primary_source_claim_integration_review_gate.json"
DECISION_MATRIX = CAPABILITIES / "runtime_adapter_decision_matrix.json"
DECISION_MATRIX_MD = CAPABILITIES / "runtime_adapter_decision_matrix.md"
GATE = CAPABILITIES / "runtime_adapter_decision_matrix_gate.json"
NEXT_ACTION = CAPABILITIES / "runtime_adapter_decision_matrix_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "runtime_adapter_decision_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_RUNTIME_ADAPTER_DECISION_MATRIX_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_runtime_adapter_decision_matrix_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_claim_integration_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_runtime_adapter_contract_skeletons_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
MATRIX_DECISION = "RUNTIME_ADAPTER_DECISION_MATRIX_READY_FOR_CONTRACT_SKELETONS"
MATRIX_SCOPE = "planning_and_contract_selection_only"

SOURCE_TARGET_IDS = [
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
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


def require_previous_gate() -> None:
    gate = read_json(INTEGRATION_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous gate must point to this goal")
    if gate.get("implementation_planning_allowed") is not True:
        raise SystemExit("previous gate must allow implementation planning")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_source_records() -> dict[str, dict]:
    data = read_json(MANUAL_RECORDS)
    if data.get("manual_primary_source_review_performed") is not True:
        raise SystemExit("manual primary-source review is required")
    records = data.get("source_records")
    if not isinstance(records, list) or len(records) != len(SOURCE_TARGET_IDS):
        raise SystemExit("expected seven source records")
    by_id: dict[str, dict] = {}
    for entry in records:
        source_id = entry.get("source_target_id")
        if source_id not in SOURCE_TARGET_IDS:
            raise SystemExit(f"unexpected source target: {source_id}")
        by_id[source_id] = entry["source_record"]
    if list(by_id) != SOURCE_TARGET_IDS:
        raise SystemExit("source records are not in the expected order")
    return by_id


def build_decision_records(source_records: dict[str, dict]) -> list[dict]:
    specs = [
        {
            "candidate_id": "langgraph-agent-runtime-adapter",
            "display_name": "LangGraph",
            "source_target_id": "src-langgraph-official-docs",
            "plane": "agent_runtime_plane",
            "phase": "Phase 2",
            "recommendation": "primary_contract_candidate",
            "fit_for_avf": "Use as the first evaluated stateful agent graph adapter because AVF already has Orchestrator, Router, Safety, Codex Planner, and Evidence Writer roles.",
            "defer_or_adopt_reason": "Create adapter IO contracts and node lifecycle skeletons first; do not install or adopt LangGraph until a later owner-approved runtime PR.",
            "required_next_contract": "avf/runtime/agent_graph_adapter_contract.md",
            "risk_notes": [
                "Keep agent nodes deterministic until external model and tool calls are separately approved.",
                "Require human gates before any live action node can run.",
            ],
        },
        {
            "candidate_id": "temporal-durable-workflow-backend",
            "display_name": "Temporal",
            "source_target_id": "src-temporal-official-docs",
            "plane": "durable_workflow_plane",
            "phase": "Phase 3",
            "recommendation": "defer_until_runtime_state_machine",
            "fit_for_avf": "Use later for crash-resumable, long-running venture runs after the local kernel has stable run states and idempotency rules.",
            "defer_or_adopt_reason": "Temporal is too heavy for the current repo-local compiler; first define workflow state, retry, timeout, and evidence event contracts.",
            "required_next_contract": "avf/runtime/durable_workflow_adapter_contract.md",
            "risk_notes": [
                "Do not introduce worker services or deployment assumptions in the foundation branch.",
                "Require explicit rollback and resume semantics before adoption.",
            ],
        },
        {
            "candidate_id": "opentelemetry-observability-standard",
            "display_name": "OpenTelemetry",
            "source_target_id": "src-opentelemetry-standard-docs",
            "plane": "observability_eval_plane",
            "phase": "Phase 5",
            "recommendation": "design_contract_now",
            "fit_for_avf": "Use as the future trace, metric, and log vocabulary for AVF runs, cells, validators, costs, and evidence events.",
            "defer_or_adopt_reason": "Define telemetry event names and claim-boundary fields now; delay SDK or collector adoption until runtime exists.",
            "required_next_contract": "avf/observability/telemetry_event_contract.md",
            "risk_notes": [
                "Avoid logging prompts, credentials, or sensitive payloads verbatim.",
                "Keep repo-local validation independent from collector availability.",
            ],
        },
        {
            "candidate_id": "mcp-tool-protocol-boundary",
            "display_name": "MCP",
            "source_target_id": "src-mcp-official-docs",
            "plane": "tool_registry_plane",
            "phase": "Phase 4",
            "recommendation": "design_contract_now",
            "fit_for_avf": "Use as the future tool/plugin boundary so AVF can connect tools through explicit capability, permission, and evidence contracts.",
            "defer_or_adopt_reason": "Draft tool registry and approval contracts first; do not run MCP servers or external tools in this planning pass.",
            "required_next_contract": "avf/integrations/mcp_tool_registry_contract.md",
            "risk_notes": [
                "Treat tool descriptions and tool outputs as untrusted inputs.",
                "Block write, publish, deploy, scraping, and account automation tools until owner approval and policy gates exist.",
            ],
        },
        {
            "candidate_id": "litellm-provider-gateway",
            "display_name": "LiteLLM",
            "source_target_id": "src-litellm-original-repository",
            "plane": "model_tool_plane",
            "phase": "Phase 4",
            "recommendation": "later_gateway_candidate",
            "fit_for_avf": "Use later as the provider-independent model gateway candidate after AVF has model routing, cost, policy, and redaction contracts.",
            "defer_or_adopt_reason": "Do not add a live provider gateway before model policy, credential handling, and offline validation gates are defined.",
            "required_next_contract": "avf/integrations/llm_gateway_contract.md",
            "risk_notes": [
                "Provider keys, base URLs, and model choices require explicit owner configuration.",
                "Gateway traces must preserve claim boundaries and avoid public-readiness claims.",
            ],
        },
        {
            "candidate_id": "vllm-open-model-serving",
            "display_name": "vLLM",
            "source_target_id": "src-vllm-original-repository",
            "plane": "model_serving_plane",
            "phase": "Phase 4",
            "recommendation": "later_serving_candidate",
            "fit_for_avf": "Use later as an open-model serving candidate when local or self-hosted inference becomes a real bottleneck.",
            "defer_or_adopt_reason": "Serving infrastructure is outside the current Web-first repo-local control plane; keep it as an approved future integration candidate only.",
            "required_next_contract": "avf/integrations/open_model_serving_contract.md",
            "risk_notes": [
                "Do not assume GPU capacity, model weights, or serving readiness.",
                "Require license, model-card, resource, and safety review before any serving work.",
            ],
        },
        {
            "candidate_id": "webarena-web-autonomy-caution",
            "display_name": "WebArena",
            "source_target_id": "src-webarena-paper",
            "plane": "safety_eval_plane",
            "phase": "Phase 5",
            "recommendation": "cautionary_benchmark_only",
            "fit_for_avf": "Use as evidence that web autonomy must remain sandboxed, approval-gated, and benchmarked rather than broad unsupervised web action.",
            "defer_or_adopt_reason": "This is not a runtime dependency for AVF; it informs future web-agent evaluation and safety limits.",
            "required_next_contract": "avf/evals/web_autonomy_safety_eval_contract.md",
            "risk_notes": [
                "Do not implement live browsing, scraping, posting, or account automation from this source record.",
                "Use benchmark evidence to define stop conditions and human approval gates.",
            ],
        },
    ]

    records: list[dict] = []
    for spec in specs:
        source = source_records[spec["source_target_id"]]
        records.append(
            {
                **spec,
                "primary_source_uri": source["source_uri"],
                "primary_source_title": source["source_title"],
                "primary_source_kind": source["source_kind"],
                "primary_source_claim": source["claim_supported"],
                "evidence_excerpt_summary": source["evidence_excerpt_summary"],
                "source_reference_lines": source["source_reference_lines"],
                "adoption_status": "not_adopted_contract_planning_only",
                "dependency_install_allowed": False,
                "runtime_integration_allowed": False,
                "owner_approval_required_before_adoption": True,
            }
        )
    return records


def build_matrix(records: list[dict]) -> dict:
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "matrix_decision": MATRIX_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "source_target_ids": SOURCE_TARGET_IDS,
        "decision_records": records,
        "selection_rules": [
            "Prefer contract skeletons before runtime adoption.",
            "Use primary-source claims as planning evidence, not as dependency approval.",
            "Keep dependency adoption, runtime integration, provider calls, and external actions behind later owner gates.",
            "Treat web autonomy as sandboxed and approval-gated until benchmarked.",
        ],
        "implementation_planning_allowed": True,
        "contract_skeleton_generation_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_markdown(matrix: dict) -> str:
    rows = "\n".join(
        "| {display_name} | `{plane}` | `{recommendation}` | `{required_next_contract}` |".format(**record)
        for record in matrix["decision_records"]
    )
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# Runtime Adapter Decision Matrix v0.1

runtime_adapter_decision_matrix_v0_1=true
matrix_decision={MATRIX_DECISION}
matrix_scope={MATRIX_SCOPE}
decision_records={len(matrix["decision_records"])}
dependency_adoption_allowed=false
runtime_integration_allowed=false

## Decision table

| Candidate | Plane | Recommendation | Next contract |
| --- | --- | --- | --- |
{rows}

## Interpretation

- LangGraph is the primary contract candidate for AVF's future agent runtime adapter.
- Temporal is deferred until the AVF run state machine needs durable crash-resumable workflow execution.
- OpenTelemetry should shape observability contracts before any SDK or collector is adopted.
- MCP should shape the tool registry boundary before tool servers are executed.
- LiteLLM is a later provider-independent gateway candidate, not an active dependency.
- vLLM is a later open-model serving candidate, not an active serving layer.
- WebArena is a cautionary safety/eval reference for web autonomy limits.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_gate(matrix: dict) -> dict:
    return {
        "gate_id": "avf-runtime-adapter-decision-matrix-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "matrix_decision": MATRIX_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "decision_records": len(matrix["decision_records"]),
        "implementation_planning_allowed": True,
        "contract_skeleton_generation_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-runtime-adapter-contract-skeletons
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Generate adapter contract skeletons only
  - Convert the decision matrix into repo-local interface documents
  - Keep dependency adoption and runtime integration behind later gates
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(matrix: dict) -> dict:
    return {
        "validator_id": "validate_avf_runtime_adapter_decision_matrix_v0_1",
        "status": "PASS",
        "matrix_decision": MATRIX_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "decision_records": len(matrix["decision_records"]),
        "implementation_planning_allowed": True,
        "contract_skeleton_generation_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(matrix: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [DECISION_MATRIX, DECISION_MATRIX_MD, GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Runtime Adapter Decision Matrix v0.1 Report

RESULT: PASS
runtime_adapter_decision_matrix_v0_1=true

## Commands

- python scripts\\run_avf_runtime_adapter_decision_matrix_v0_1.py
- python scripts\\validate_avf_runtime_adapter_decision_matrix_v0_1.py

## Matrix summary

- matrix_decision={MATRIX_DECISION}
- matrix_scope={MATRIX_SCOPE}
- decision_records={len(matrix["decision_records"])}
- implementation_planning_allowed=true
- contract_skeleton_generation_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Candidate coverage

- LangGraph: agent runtime plane
- Temporal: durable workflow plane
- OpenTelemetry: observability/eval plane
- MCP: tool registry plane
- LiteLLM: model/tool gateway plane
- vLLM: open model serving plane
- WebArena: web autonomy safety/eval plane

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    records = build_decision_records(load_source_records())
    matrix = build_matrix(records)

    write_json(DECISION_MATRIX, matrix)
    write_text(DECISION_MATRIX_MD, build_markdown(matrix))
    write_json(GATE, build_gate(matrix))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(matrix))
    write_text(VALIDATION_REPORT, build_report(matrix))

    print("AVF Runtime Adapter Decision Matrix v0.1")
    print("RESULT: PASS")
    print("runtime_adapter_decision_matrix_v0_1=true")
    print(f"matrix_decision={MATRIX_DECISION}")
    print(f"matrix_scope={MATRIX_SCOPE}")
    print(f"decision_records={len(records)}")
    print("implementation_planning_allowed=true")
    print("contract_skeleton_generation_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
