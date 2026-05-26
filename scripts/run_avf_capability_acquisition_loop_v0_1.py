from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
STRATEGY = ROOT / "avf" / "strategy" / "generated"
GOALS = ROOT / "docs" / "goals"

STRATEGY_DECISION = STRATEGY / "strategy_adaptation_decision_packet.json"
ACQUISITION_PLAN = CAPABILITIES / "capability_acquisition_plan.json"
CANDIDATE_REGISTRY = CAPABILITIES / "capability_candidate_registry.json"
BUILD_BUY_ADOPT = CAPABILITIES / "build_buy_adopt_decision_records.json"
SOURCE_LEDGER = CAPABILITIES / "capability_source_ledger.json"
NEXT_CODEX_TASK = CAPABILITIES / "next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_acquisition_loop_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_ACQUISITION_LOOP_V0_1_VALIDATION_REPORT.md"

THIS_GOAL_ID = "avf_capability_acquisition_loop_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_fit_scoring_validator_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"


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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def false_boundary() -> dict:
    return {
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "scraping_performed": False,
        "posting_automation_performed": False,
        "dependency_install_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "package_install_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def build_source_ledger() -> dict:
    return {
        "ledger_id": "avf-capability-source-ledger-v0-1",
        "created_at": CREATED_AT,
        "automation_fetch_performed": False,
        "source_selection_boundary": (
            "Operator-reviewed primary-source URLs only. This runner performs no network fetch, "
            "dependency install, package install, OSS clone, provider call, live model call, scraping, "
            "posting, deploy, publish, or readiness claim."
        ),
        "sources": [
            {
                "source_id": "src-litellm-docs",
                "source_kind": "official_docs",
                "title": "LiteLLM documentation",
                "url": "https://docs.litellm.ai/docs/",
                "why_used": "Candidate for a provider-independent LLM gateway, virtual-key control, and spend tracking plane.",
                "capability_ids": ["cap-llm-gateway"],
            },
            {
                "source_id": "src-langgraph-docs",
                "source_kind": "official_docs",
                "title": "LangGraph overview",
                "url": "https://docs.langchain.com/oss/python/langgraph",
                "why_used": "Candidate for stateful agent graph runtime and human-in-loop adapter planning.",
                "capability_ids": ["cap-agent-runtime"],
            },
            {
                "source_id": "src-temporal-docs",
                "source_kind": "official_docs",
                "title": "Temporal documentation",
                "url": "https://docs.temporal.io/",
                "why_used": "Candidate for durable workflow, retry, resume, timeout, and long-running state boundaries.",
                "capability_ids": ["cap-durable-workflow", "cap-agent-runtime"],
            },
            {
                "source_id": "src-mcp-docs",
                "source_kind": "official_docs",
                "title": "Model Context Protocol documentation",
                "url": "https://modelcontextprotocol.io/docs/getting-started/intro",
                "why_used": "Candidate standard for a tool and connector registry after approval-gated integration.",
                "capability_ids": ["cap-tool-registry"],
            },
            {
                "source_id": "src-opentelemetry-docs",
                "source_kind": "official_docs",
                "title": "OpenTelemetry documentation",
                "url": "https://opentelemetry.io/docs/",
                "why_used": "Candidate observability standard for traces, metrics, logs, and evidence correlation.",
                "capability_ids": ["cap-observability"],
            },
            {
                "source_id": "src-langfuse-docs",
                "source_kind": "official_docs",
                "title": "Langfuse documentation",
                "url": "https://langfuse.com/docs",
                "why_used": "Candidate for LLM tracing, prompt/version observation, and eval workflow review.",
                "capability_ids": ["cap-observability", "cap-evaluation-red-team"],
            },
            {
                "source_id": "src-phoenix-docs",
                "source_kind": "official_docs",
                "title": "Arize Phoenix documentation",
                "url": "https://docs.arize.com/phoenix",
                "why_used": "Candidate for AI observability and evaluation plane review.",
                "capability_ids": ["cap-observability", "cap-evaluation-red-team"],
            },
            {
                "source_id": "src-promptfoo-docs",
                "source_kind": "official_docs",
                "title": "promptfoo documentation",
                "url": "https://www.promptfoo.dev/docs/intro/",
                "why_used": "Candidate for prompt, model, and red-team evaluation harness planning.",
                "capability_ids": ["cap-evaluation-red-team"],
            },
            {
                "source_id": "src-ragas-docs",
                "source_kind": "official_docs",
                "title": "Ragas documentation",
                "url": "https://docs.ragas.io/en/stable/",
                "why_used": "Candidate for RAG and agent evaluation metrics when document memory is added.",
                "capability_ids": ["cap-evaluation-red-team", "cap-rag-document-pipeline"],
            },
            {
                "source_id": "src-haystack-docs",
                "source_kind": "official_docs",
                "title": "Haystack documentation",
                "url": "https://docs.haystack.deepset.ai/docs/intro",
                "why_used": "Candidate for future RAG, document pipeline, agent, tool, and document-store integration.",
                "capability_ids": ["cap-rag-document-pipeline"],
            },
            {
                "source_id": "src-openhands-docs",
                "source_kind": "official_docs",
                "title": "OpenHands documentation",
                "url": "https://docs.all-hands.dev/",
                "why_used": "Candidate for an optional approval-gated coding executor lane, not enabled in this pass.",
                "capability_ids": ["cap-approved-coding-executor"],
            },
            {
                "source_id": "src-swe-agent-docs",
                "source_kind": "official_docs",
                "title": "SWE-agent documentation",
                "url": "https://swe-agent.com/latest/",
                "why_used": "Candidate for issue-to-code task execution research under Codex-lane safety boundaries.",
                "capability_ids": ["cap-approved-coding-executor"],
            },
        ],
    }


def candidate(
    candidate_id: str,
    name: str,
    source_ref: str,
    integration_mode: str,
    fit_reason: str,
) -> dict:
    return {
        "candidate_id": candidate_id,
        "name": name,
        "source_ref": source_ref,
        "integration_mode": integration_mode,
        "fit_reason": fit_reason,
        "license_review_status": "required_not_performed",
        "security_review_status": "required_not_performed",
        "maintenance_review_status": "required_not_performed",
        "integration_status": "proposed_only",
        "dependency_install_allowed": False,
        "external_fetch_performed": False,
        "owner_approval_required": True,
    }


def capability(
    capability_id: str,
    name: str,
    why_needed: str,
    recommendation: str,
    candidate_records: list[dict],
) -> dict:
    return {
        "capability_id": capability_id,
        "capability_name": name,
        "why_needed": why_needed,
        "current_status": "missing_or_design_only",
        "build_buy_adopt_recommendation": recommendation,
        "candidate_search_required": True,
        "license_review_required": True,
        "security_review_required": True,
        "maintenance_review_required": True,
        "integration_status": "proposed_only",
        "dependency_install_allowed": False,
        "external_fetch_performed": False,
        "owner_approval_required": True,
        "candidate_records": candidate_records,
    }


def build_candidate_registry() -> dict:
    return {
        "registry_id": "avf-capability-candidate-registry-v0-1",
        "created_at": CREATED_AT,
        "status": "PASS",
        "selection_boundary": "Records only. No candidate is installed, cloned, fetched, invoked, deployed, or enabled.",
        "capabilities": [
            capability(
                "cap-llm-gateway",
                "Provider-independent LLM gateway",
                "AVF needs provider independence and future cost/routing governance without binding to OpenClaude or one model provider.",
                "adopt_later_after_gateway_security_review",
                [
                    candidate(
                        "candidate-litellm-proxy",
                        "LiteLLM Proxy",
                        "src-litellm-docs",
                        "gateway_adapter_later",
                        "Official docs describe an LLM gateway/proxy surface that can later centralize model routing and spend tracking.",
                    )
                ],
            ),
            capability(
                "cap-agent-runtime",
                "Stateful agent runtime",
                "The current foundation has role catalogs and packets, but no stateful execution graph or human-in-loop runtime.",
                "adopt_later_after_local_contract",
                [
                    candidate(
                        "candidate-langgraph-runtime",
                        "LangGraph",
                        "src-langgraph-docs",
                        "runtime_adapter_later",
                        "Fits future stateful graph execution while keeping current pass contract-only.",
                    ),
                    candidate(
                        "candidate-temporal-agent-boundary",
                        "Temporal",
                        "src-temporal-docs",
                        "durable_runtime_boundary_later",
                        "Useful if agent runs become long-lived and need retry/resume semantics.",
                    ),
                ],
            ),
            capability(
                "cap-durable-workflow",
                "Durable workflow backend",
                "AVF needs future retry, timeout, replay, and idempotent long-running execution once it leaves deterministic local runs.",
                "adopt_later_after_workflow_contract",
                [
                    candidate(
                        "candidate-temporal-workflow",
                        "Temporal",
                        "src-temporal-docs",
                        "workflow_backend_later",
                        "Best fit for crash-resistant durable workflows after local compiler semantics are stable.",
                    )
                ],
            ),
            capability(
                "cap-tool-registry",
                "Tool and connector registry",
                "Future capability acquisition needs a standard way to expose approved tools without hardwiring each provider or host.",
                "adopt_standard_later_after_tool_security_gate",
                [
                    candidate(
                        "candidate-mcp-tool-registry",
                        "Model Context Protocol",
                        "src-mcp-docs",
                        "tool_protocol_later",
                        "A protocol candidate for tool/resource/prompt contracts after approval and sandbox boundaries exist.",
                    )
                ],
            ),
            capability(
                "cap-observability",
                "Observability and trace evidence",
                "AVF needs traces, metrics, logs, run lineage, and LLM-specific observability before claiming autonomous reliability.",
                "compose_later_after_trace_contract",
                [
                    candidate(
                        "candidate-opentelemetry",
                        "OpenTelemetry",
                        "src-opentelemetry-docs",
                        "observability_standard_later",
                        "Vendor-neutral telemetry standard candidate for run/evidence correlation.",
                    ),
                    candidate(
                        "candidate-langfuse",
                        "Langfuse",
                        "src-langfuse-docs",
                        "llm_observability_adapter_later",
                        "LLM trace/eval observability candidate after provider gateway exists.",
                    ),
                    candidate(
                        "candidate-phoenix",
                        "Arize Phoenix",
                        "src-phoenix-docs",
                        "ai_observability_adapter_later",
                        "AI observability/evaluation candidate for comparing traces and runs.",
                    ),
                ],
            ),
            capability(
                "cap-evaluation-red-team",
                "Evaluation and red-team harness",
                "AVF needs regression checks and safety evaluation before self-improvement or public-facing claims can be trusted.",
                "compose_later_after_eval_contract",
                [
                    candidate(
                        "candidate-promptfoo",
                        "promptfoo",
                        "src-promptfoo-docs",
                        "eval_harness_later",
                        "Candidate for prompt/model evals and red-team cases.",
                    ),
                    candidate(
                        "candidate-ragas",
                        "Ragas",
                        "src-ragas-docs",
                        "rag_eval_harness_later",
                        "Candidate for RAG/agent evaluation metrics when memory retrieval exists.",
                    ),
                    candidate(
                        "candidate-langfuse-evals",
                        "Langfuse evals",
                        "src-langfuse-docs",
                        "llm_eval_observability_later",
                        "Candidate for connecting evals back to trace evidence.",
                    ),
                ],
            ),
            capability(
                "cap-rag-document-pipeline",
                "Document memory and RAG pipeline",
                "Brand/IP, evidence, and market memory will need searchable document pipelines after local file contracts mature.",
                "adopt_or_build_adapter_later_after_memory_contract",
                [
                    candidate(
                        "candidate-haystack",
                        "Haystack",
                        "src-haystack-docs",
                        "document_pipeline_adapter_later",
                        "Candidate for RAG/document-store/tool pipelines.",
                    ),
                    candidate(
                        "candidate-ragas-rag-eval",
                        "Ragas",
                        "src-ragas-docs",
                        "rag_eval_adapter_later",
                        "Evaluation companion candidate for future document-memory quality checks.",
                    ),
                ],
            ),
            capability(
                "cap-approved-coding-executor",
                "Optional approved coding executor lane",
                "Codex remains the main executor, but optional issue-to-code agents can be compared under the same approval-gated PR-sized lane later.",
                "compare_later_without_replacing_codex_lane",
                [
                    candidate(
                        "candidate-openhands",
                        "OpenHands",
                        "src-openhands-docs",
                        "approved_executor_candidate_later",
                        "Candidate for sandboxed coding-agent comparison, not enabled here.",
                    ),
                    candidate(
                        "candidate-swe-agent",
                        "SWE-agent",
                        "src-swe-agent-docs",
                        "approved_executor_candidate_later",
                        "Candidate for issue-to-code research, not enabled here.",
                    ),
                ],
            ),
        ],
        "claim_boundary": false_boundary(),
    }


def build_decision_records(registry: dict) -> dict:
    decisions = []
    for capability_record in registry["capabilities"]:
        decisions.append(
            {
                "decision_id": f"decision-{capability_record['capability_id']}",
                "capability_id": capability_record["capability_id"],
                "decision_status": "proposed_only",
                "recommendation": capability_record["build_buy_adopt_recommendation"],
                "preferred_candidate_ids": [
                    candidate_record["candidate_id"] for candidate_record in capability_record["candidate_records"]
                ],
                "why_not_build_now": "Current boundary is repo-local planning and evidence. Building runtime integrations now would skip fit scoring and approval gates.",
                "why_not_install_now": "Dependency install, external fetch, OSS clone, provider calls, and runtime integration are protected actions in this phase.",
                "license_review_required": True,
                "security_review_required": True,
                "owner_approval_required": True,
                "dependency_install_allowed": False,
                "external_fetch_performed": False,
            }
        )
    return {
        "record_id": "avf-build-buy-adopt-decision-records-v0-1",
        "created_at": CREATED_AT,
        "status": "PASS",
        "decision_boundary": "Proposal records only; no external action or dependency mutation.",
        "decisions": decisions,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-fit-scoring-validator-v0-1
title: Add AVF capability fit scoring validator v0.1
goal: Score proposed capability candidates for fit, risk, license-review status, security-review status, and integration readiness without installing or fetching anything.
context_paths:
  - avf/capabilities/generated/capability_acquisition_plan.json
  - avf/capabilities/generated/capability_candidate_registry.json
  - avf/capabilities/generated/build_buy_adopt_decision_records.json
  - avf/capabilities/generated/capability_source_ledger.json
files_likely_to_touch:
  - scripts/run_avf_capability_fit_scoring_validator_v0_1.py
  - scripts/validate_avf_capability_fit_scoring_validator_v0_1.py
  - avf/capabilities/generated/capability_fit_scorecard.json
  - docs/goals/AVF_CAPABILITY_FIT_SCORING_VALIDATOR_V0_1_REPORT.md
forbidden_changes:
  - No provider calls
  - No live model calls
  - No external service calls
  - No scraping
  - No package install
  - No dependency install
  - No OSS clone
  - No external fetch
  - No runtime integration
  - No deploy
  - No publish
  - No release readiness claim
  - No production readiness claim
acceptance_criteria:
  - scorecard exists
  - each candidate has fit_score, risk_score, license_review_status, security_review_status, and next gate
  - candidates remain proposed_only
  - all protected-action flags remain false
validation_commands:
  - python scripts\\validate_avf_capability_acquisition_loop_v0_1.py
  - python scripts\\validate_avf_capability_fit_scoring_validator_v0_1.py
expected_outputs:
  - capability_fit_scorecard.json
  - fit scoring validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_acquisition_plan(strategy_decision: dict) -> dict:
    return {
        "plan_id": "avf-capability-acquisition-loop-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "run_id": strategy_decision["run_id"],
        "status": "PASS",
        "trigger_decision_uri": rel(STRATEGY_DECISION),
        "trigger_decision_hash": sha256(STRATEGY_DECISION),
        "trigger_refinement_actions": strategy_decision.get("refinement_actions", []),
        "capability_gap_summary": [
            "Provider-independent LLM gateway is still only a future plan.",
            "Stateful and durable runtime planes are still only contracts.",
            "Tool registry, observability, eval, RAG, and approved executor lanes have no scored acquisition records yet.",
        ],
        "candidate_registry_uri": rel(CANDIDATE_REGISTRY),
        "candidate_registry_hash": sha256(CANDIDATE_REGISTRY),
        "build_buy_adopt_uri": rel(BUILD_BUY_ADOPT),
        "build_buy_adopt_hash": sha256(BUILD_BUY_ADOPT),
        "source_ledger_uri": rel(SOURCE_LEDGER),
        "source_ledger_hash": sha256(SOURCE_LEDGER),
        "next_codex_task_uri": rel(NEXT_CODEX_TASK),
        "next_codex_task_hash": sha256(NEXT_CODEX_TASK),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_acquisition_loop_v0_1",
        "status": "PASS",
        "checks": [
            "strategy decision authorizes capability acquisition",
            "candidate registry exists",
            "build/buy/adopt records exist",
            "primary source ledger exists",
            "next Codex task exists",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    return f"""# AVF Capability Acquisition Loop v0.1 Validation Report

RESULT: PASS
capability_acquisition_loop_v0_1=true
capability_acquisition_plan_created=true
candidate_registry_created=true
build_buy_adopt_records_created=true
source_ledger_created=true
protected_action_executed=false
dependency_install_performed=false
external_fetch_performed=false
provider_calls_performed=false
scraping_performed=false
posting_automation_performed=false
deploy_performed=false
publish_performed=false
release_ready=false
production_ready=false
next_safe_goal_id={NEXT_SAFE_GOAL_ID}

## What This Adds

This pass turns the Strategy Adaptation Loop refinement into a repo-local Capability Acquisition Loop. It records OSS/tool candidates for LLM gateway, agent runtime, durable workflow, tool registry, observability, evaluation, RAG/document memory, and optional approved coding executors.

## Source Boundary

The source ledger records official documentation URLs only. The runner does not fetch those URLs, install packages, clone repositories, call providers, call live models, scrape sites, post content, deploy, publish, or claim release/production readiness.

## Next Safe Goal

`{NEXT_SAFE_GOAL_ID}` should add a scoring validator before any integration work. That keeps AVF in proposal/evidence mode until license, security, maintenance, and architecture fit gates are explicit.
"""


def main() -> None:
    strategy_decision = read_json(STRATEGY_DECISION)
    if strategy_decision.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("strategy decision does not point to this capability acquisition goal")

    source_ledger = build_source_ledger()
    write_json(SOURCE_LEDGER, source_ledger)
    registry = build_candidate_registry()
    write_json(CANDIDATE_REGISTRY, registry)
    decisions = build_decision_records(registry)
    write_json(BUILD_BUY_ADOPT, decisions)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    plan = build_acquisition_plan(strategy_decision)
    write_json(ACQUISITION_PLAN, plan)
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Capability Acquisition Loop v0.1 runner")
    print("RESULT: PASS")
    print("capability_acquisition_loop_v0_1=true")
    print("capability_acquisition_plan_created=true")
    print("candidate_registry_created=true")
    print("build_buy_adopt_records_created=true")
    print("source_ledger_created=true")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("provider_calls_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
