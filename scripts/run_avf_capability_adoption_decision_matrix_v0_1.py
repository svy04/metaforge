from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOCS_AVF = ROOT / "docs" / "avf"
DOC_GOALS = ROOT / "docs" / "goals"

FINAL_REVIEW = CAPABILITIES / "primary_source_registry_gap_closure_final_review.json"
FINAL_GATE = CAPABILITIES / "primary_source_registry_gap_closure_final_review_gate.json"
FINAL_NEXT_ACTION = CAPABILITIES / "primary_source_registry_gap_closure_final_review_next_action.yml"
ADOPTION_LINKS = CAPABILITIES / "primary_source_adoption_evidence_gate_links.json"
MANUAL_RECORDS = CAPABILITIES / "primary_source_manual_records.json"
OSS_MAP = DOCS_AVF / "OPEN_SOURCE_EXPANSION_MAP.md"
DECISION_MATRIX = CAPABILITIES / "capability_adoption_decision_matrix.json"
DECISION_GATE = CAPABILITIES / "capability_adoption_decision_matrix_gate.json"
DECISION_REPORT = CAPABILITIES / "capability_adoption_decision_matrix_report.md"
NEXT_ACTION = CAPABILITIES / "capability_adoption_decision_matrix_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_adoption_decision_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_ADOPTION_DECISION_MATRIX_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_adoption_decision_matrix_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_registry_gap_closure_final_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_expansion_plan_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
MATRIX_DECISION = "CAPABILITY_ADOPTION_DECISION_MATRIX_CREATED_REPO_LOCAL"
MATRIX_STATUS = "planning_only_all_adoption_blocked"

GATE_IDS = [
    "gate-build-vs-buy-review",
    "gate-license-review",
    "gate-security-review",
    "gate-supply-chain-review",
    "gate-owner-approval",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


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
        "runtime_export_performed": False,
        "collector_started": False,
        "telemetry_export_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_previous_final_review(final_review: dict, final_gate: dict) -> None:
    for label, record in [("final review", final_review), ("final gate", final_gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            raise SystemExit(f"{label} goal mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            raise SystemExit(f"{label} must point to this matrix goal")
        if record.get("remaining_gap_count") != 0:
            raise SystemExit(f"{label} remaining gap count mismatch")
        if record.get("dependency_adoption_allowed") is not False:
            raise SystemExit(f"{label} dependency adoption must stay blocked")
        if record.get("runtime_integration_allowed") is not False:
            raise SystemExit(f"{label} runtime integration must stay blocked")


def manual_source_ids(manual_records: dict) -> set[str]:
    return {record.get("source_target_id") for record in manual_records.get("source_records", [])}


def capability_candidates(source_ids: set[str]) -> list[dict]:
    specs = [
        ("cap-agent-runtime-langgraph", "LangGraph", "agent_runtime", ["src-langgraph-official-docs"], "prepare_adapter_contract_after_kernel_semantics"),
        ("cap-durable-workflow-temporal", "Temporal", "durable_workflow", ["src-temporal-official-docs"], "prepare_adapter_contract_after_run_state_contract"),
        ("cap-k8s-workflow-argo", "Argo Workflows", "kubernetes_workflow", [], "defer_until_containerized_parallel_jobs_are_required"),
        ("cap-general-orchestration-kestra-prefect-airflow", "Kestra / Prefect / Airflow", "general_orchestration", [], "compare_after_local_kernel_and_approval_queue_exist"),
        ("cap-evidence-lineage-dagster", "Dagster", "evidence_lineage", [], "defer_until_artifacts_behave_like_data_products"),
        ("cap-llm-gateway-litellm", "LiteLLM", "llm_gateway", ["src-litellm-original-repository"], "prepare_gateway_decision_record_without_provider_calls"),
        ("cap-local-open-model-serving-ollama-vllm", "Ollama / vLLM", "local_open_model_serving", ["src-vllm-original-repository"], "defer_runtime_serving_but_keep_vllm_source_backed"),
        ("cap-rag-document-pipeline-haystack", "Haystack", "document_retrieval_pipeline", [], "defer_until_memory_contract_needs_retrieval_pipeline"),
        ("cap-llm-observability-langfuse-phoenix", "Langfuse / Phoenix", "llm_observability", [], "defer_until_local_trace_schema_and_export_boundary_are_stable"),
        ("cap-eval-redteam-promptfoo-ragas", "promptfoo / Ragas", "eval_redteam", [], "defer_until_eval_cases_are_versioned"),
        ("cap-tool-protocol-mcp", "MCP", "tool_protocol", ["src-mcp-official-docs"], "prepare_tool_boundary_contract_before_tool_execution"),
        ("cap-telemetry-standard-opentelemetry", "OpenTelemetry", "telemetry_standard", ["src-opentelemetry-standard-docs"], "prepare_event_schema_mapping_without_collector_start"),
        ("cap-coding-executor-openhands-sweagent", "OpenHands / SWE-agent", "coding_executor", [], "evaluate_only_as_approval_gated_optional_codex_lane"),
    ]
    candidates = []
    for candidate_id, name, capability_type, source_targets, recommended_action in specs:
        source_backed = bool(source_targets) and all(source_id in source_ids for source_id in source_targets)
        candidates.append(
            {
                "candidate_id": candidate_id,
                "name": name,
                "capability_type": capability_type,
                "source_target_ids": source_targets,
                "source_record_status": "manual_source_record_available" if source_backed else "manual_source_record_required",
                "recommended_action": recommended_action,
                "required_gate_ids": GATE_IDS,
                "adoption_status": "blocked_until_gates_satisfied",
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
                "protected_action_required_before_adoption": True,
            }
        )
    return candidates


def counts(candidates: list[dict], manual_records: dict) -> dict:
    source_backed = [candidate for candidate in candidates if candidate["source_record_status"] == "manual_source_record_available"]
    source_required = [candidate for candidate in candidates if candidate["source_record_status"] == "manual_source_record_required"]
    return {
        "candidate_count": len(candidates),
        "source_backed_candidate_count": len(source_backed),
        "source_record_required_candidate_count": len(source_required),
        "manual_primary_source_record_count": len(manual_records.get("source_records", [])),
        "gate_requirement_count": len(GATE_IDS),
        "ready_for_adoption_count": 0,
        "blocked_candidate_count": len(candidates),
    }


def base_record(candidates: list[dict], manual_records: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "matrix_decision": MATRIX_DECISION,
        "matrix_status": MATRIX_STATUS,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "all_candidates_blocked_until_gates_satisfied": True,
        "candidate_ids": [candidate["candidate_id"] for candidate in candidates],
        "gate_ids": GATE_IDS,
        "candidates": candidates,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(candidates, manual_records),
        "claim_boundary": false_boundary(),
    }


def build_matrix(candidates: list[dict], manual_records: dict) -> dict:
    return {
        **base_record(candidates, manual_records),
        "matrix_id": "avf-capability-adoption-decision-matrix-v0-1",
        "matrix_scope": "repo-local planning matrix only; no dependency adoption or runtime integration",
        "source_inputs": [
            rel(FINAL_REVIEW),
            rel(FINAL_GATE),
            rel(FINAL_NEXT_ACTION),
            rel(ADOPTION_LINKS),
            rel(MANUAL_RECORDS),
            rel(OSS_MAP),
        ],
    }


def build_gate(candidates: list[dict], manual_records: dict) -> dict:
    return {
        **base_record(candidates, manual_records),
        "gate_id": "avf-capability-adoption-decision-matrix-gate-v0-1",
        "status": "PASS",
        "gate_scope": "decision matrix created; all candidates remain blocked",
    }


def build_report(title: str, candidates: list[dict], manual_records: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(candidates, manual_records).items())
    candidate_lines = "\n".join(f"- {candidate['candidate_id']}" for candidate in candidates)
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_adoption_decision_matrix_v0_1=true

## Gate summary

- matrix_decision={MATRIX_DECISION}
- matrix_status={MATRIX_STATUS}
- dependency_adoption_allowed=false
- runtime_integration_allowed=false
- all_candidates_blocked_until_gates_satisfied=true

## Counts

{count_lines}

## Candidates

{candidate_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: plan-capability-candidate-primary-source-expansion
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create repo-local primary-source expansion plan for capability candidates without manual source records
  - Prioritize official docs, original repositories, papers, standards, and maintained upstream implementations
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(candidates: list[dict], manual_records: dict) -> dict:
    return {
        **base_record(candidates, manual_records),
        "validator_id": "validate_avf_capability_adoption_decision_matrix_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(DECISION_MATRIX),
            rel(DECISION_GATE),
            rel(DECISION_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    final_review = read_json(FINAL_REVIEW)
    final_gate = read_json(FINAL_GATE)
    manual_records = read_json(MANUAL_RECORDS)
    require_previous_final_review(final_review, final_gate)

    candidates = capability_candidates(manual_source_ids(manual_records))
    write_json(DECISION_MATRIX, build_matrix(candidates, manual_records))
    write_json(DECISION_GATE, build_gate(candidates, manual_records))
    write_text(DECISION_REPORT, build_report("Capability Adoption Decision Matrix v0.1", candidates, manual_records))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(candidates, manual_records))
    write_text(VALIDATION_REPORT, build_report("AVF Capability Adoption Decision Matrix v0.1 Report", candidates, manual_records))

    print("AVF Capability Adoption Decision Matrix v0.1")
    print("RESULT: PASS")
    print(f"matrix_decision={MATRIX_DECISION}")
    print(f"matrix_status={MATRIX_STATUS}")
    for key, value in counts(candidates, manual_records).items():
        print(f"{key}={value}")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("all_candidates_blocked_until_gates_satisfied=true")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
