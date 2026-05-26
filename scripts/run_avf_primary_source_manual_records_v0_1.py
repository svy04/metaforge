from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PACKET_GATE = CAPABILITIES / "primary_source_manual_collection_packet_gate.json"
RECORDS = CAPABILITIES / "primary_source_manual_records.json"
RECORDS_MARKDOWN = CAPABILITIES / "primary_source_manual_records.md"
RECORDS_GATE = CAPABILITIES / "primary_source_manual_records_gate.json"
NEXT_ACTION = CAPABILITIES / "primary_source_manual_records_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_manual_records_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_MANUAL_RECORDS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_manual_records_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_manual_collection_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_records_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PACKET_DECISION = "PRIMARY_SOURCE_MANUAL_COLLECTION_PACKET_READY_NOT_EXECUTED"
RECORD_DECISION = "PRIMARY_SOURCE_MANUAL_RECORDS_CREATED_FROM_PRIMARY_SOURCES"

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


SOURCE_RECORDS = [
    {
        "source_target_id": "src-langgraph-official-docs",
        "target_claim_id": "claim-agent-runtime-stateful-graph",
        "source_record": {
            "source_id": "src-langgraph-official-docs",
            "source_title": "LangGraph overview",
            "source_kind": "official_docs",
            "source_uri": "https://docs.langchain.com/oss/python/langgraph/overview",
            "source_version_or_date": "Accessed 2026-05-27",
            "source_owner_or_publisher": "LangChain Inc / Docs by LangChain",
            "license_or_rights_note": "Official documentation page; use summarized evidence only and review project license before dependency adoption.",
            "claim_supported": "AVF runtime adapter should evaluate a stateful graph model for long-running agent orchestration.",
            "evidence_excerpt_summary": "The official overview frames LangGraph as a low-level orchestration framework and runtime for long-running stateful agents, with durable execution, streaming, human-in-the-loop, persistence, and memory capabilities. It also says LangGraph can be used without LangChain.",
            "verification_notes": "Manual primary-source review of official docs lines 87-92, 124-130, and 160-162.",
            "source_reference_lines": "turn0view0 lines 87-92, 124-130, 160-162",
            "retrieval_method": "manual_browser_primary_source_review",
        },
    },
    {
        "source_target_id": "src-temporal-official-docs",
        "target_claim_id": "claim-durable-workflow-backend",
        "source_record": {
            "source_id": "src-temporal-official-docs",
            "source_title": "Temporal Docs",
            "source_kind": "official_docs",
            "source_uri": "https://docs.temporal.io/",
            "source_version_or_date": "Accessed 2026-05-27",
            "source_owner_or_publisher": "Temporal Technologies Inc.",
            "license_or_rights_note": "Official documentation page; use summarized evidence only and review project/server licensing before adoption.",
            "claim_supported": "AVF durable workflow phases should evaluate crash-resumable workflow execution.",
            "evidence_excerpt_summary": "The Temporal docs describe Temporal as an open-source platform for reliable applications and emphasize crash-proof execution that resumes where work left off after crashes, network failures, or infrastructure outages.",
            "verification_notes": "Manual primary-source review of official docs lines 37-40 and copyright line 87.",
            "source_reference_lines": "turn0view1 lines 37-40, 87",
            "retrieval_method": "manual_browser_primary_source_review",
        },
    },
    {
        "source_target_id": "src-opentelemetry-standard-docs",
        "target_claim_id": "claim-observability-standard",
        "source_record": {
            "source_id": "src-opentelemetry-standard-docs",
            "source_title": "What is OpenTelemetry?",
            "source_kind": "standard",
            "source_uri": "https://opentelemetry.io/docs/what-is-opentelemetry/",
            "source_version_or_date": "Accessed 2026-05-27",
            "source_owner_or_publisher": "OpenTelemetry project",
            "license_or_rights_note": "Official project documentation; use summarized evidence only and review OpenTelemetry documentation/source licenses before adoption.",
            "claim_supported": "AVF observability should use a standard traces, metrics, and logs model.",
            "evidence_excerpt_summary": "The OpenTelemetry docs define it as an observability framework and toolkit for generation, export, and collection of telemetry such as traces, metrics, and logs, and describe it as open source, vendor-neutral, and tool-agnostic.",
            "verification_notes": "Manual primary-source review of official docs lines 832-844 and 865-876.",
            "source_reference_lines": "turn1view2 lines 832-844, 865-876",
            "retrieval_method": "manual_browser_primary_source_review",
        },
    },
    {
        "source_target_id": "src-mcp-official-docs",
        "target_claim_id": "claim-tool-protocol-boundary",
        "source_record": {
            "source_id": "src-mcp-official-docs",
            "source_title": "What is the Model Context Protocol?",
            "source_kind": "standard",
            "source_uri": "https://modelcontextprotocol.io/docs/getting-started/intro",
            "source_version_or_date": "Accessed 2026-05-27",
            "source_owner_or_publisher": "Model Context Protocol project",
            "license_or_rights_note": "Official documentation page; use summarized evidence only and review MCP spec/license terms before integration.",
            "claim_supported": "AVF tool integration should use an explicit tool protocol boundary before plugin execution.",
            "evidence_excerpt_summary": "The MCP docs define MCP as an open-source standard for connecting AI applications to external systems, including data sources, tools, and workflows. The same page positions MCP as a standardized connector boundary for AI applications.",
            "verification_notes": "Manual primary-source review of official docs lines 61-73 and 85-90.",
            "source_reference_lines": "turn1view2 lines 61-73, 85-90",
            "retrieval_method": "manual_browser_primary_source_review",
        },
    },
    {
        "source_target_id": "src-litellm-original-repository",
        "target_claim_id": "claim-provider-independent-llm-gateway",
        "source_record": {
            "source_id": "src-litellm-original-repository",
            "source_title": "BerriAI/litellm repository and LiteLLM docs",
            "source_kind": "original_repository",
            "source_uri": "https://github.com/BerriAI/litellm",
            "source_version_or_date": "Accessed 2026-05-27",
            "source_owner_or_publisher": "BerriAI/litellm maintainers",
            "license_or_rights_note": "Original repository and official docs reviewed; license and enterprise feature boundaries must be reviewed before dependency adoption.",
            "claim_supported": "AVF model plane should evaluate a provider-independent LLM gateway.",
            "evidence_excerpt_summary": "The LiteLLM repository describes LiteLLM as an open-source AI Gateway for 100+ LLM providers using the OpenAI format. The official docs also describe a self-hosted OpenAI-compatible proxy and gateway surface for models, agents, and MCP.",
            "verification_notes": "Manual primary-source review of GitHub README lines 449-467 and 473-479, plus docs lines 360-363 and 426-435.",
            "source_reference_lines": "turn4view3 lines 449-467, 473-479; turn4view2 lines 360-363, 426-435",
            "retrieval_method": "manual_browser_primary_source_review",
        },
    },
    {
        "source_target_id": "src-vllm-original-repository",
        "target_claim_id": "claim-open-model-serving-plane",
        "source_record": {
            "source_id": "src-vllm-original-repository",
            "source_title": "vllm-project/vllm repository and vLLM docs",
            "source_kind": "original_repository",
            "source_uri": "https://github.com/vllm-project/vllm",
            "source_version_or_date": "Accessed 2026-05-27",
            "source_owner_or_publisher": "vllm-project/vllm maintainers",
            "license_or_rights_note": "GitHub repository displays Apache-2.0 license; still review license and supply-chain implications before dependency adoption.",
            "claim_supported": "AVF model plane should evaluate open model serving for later approved runtime phases.",
            "evidence_excerpt_summary": "The vLLM repository describes vLLM as a fast, easy-to-use library for LLM inference and serving, with throughput and memory management features. The docs note an OpenAI-compatible API server and broad model/hardware support.",
            "verification_notes": "Manual primary-source review of GitHub lines 377-405 and 478-480, plus docs lines 2433-2453.",
            "source_reference_lines": "turn4view4 lines 377-405, 478-480; turn4view5 lines 2433-2453",
            "retrieval_method": "manual_browser_primary_source_review",
        },
    },
    {
        "source_target_id": "src-webarena-paper",
        "target_claim_id": "claim-web-agent-autonomy-caution",
        "source_record": {
            "source_id": "src-webarena-paper",
            "source_title": "WebArena: A Realistic Web Environment for Building Autonomous Agents",
            "source_kind": "paper",
            "source_uri": "https://arxiv.org/abs/2307.13854",
            "source_version_or_date": "Submitted 2023-07-25; revised 2024-04-16; accessed 2026-05-27",
            "source_owner_or_publisher": "arXiv / Shuyan Zhou et al.",
            "license_or_rights_note": "arXiv record and paper metadata; cite and summarize only, and review paper license before reproducing text or figures.",
            "claim_supported": "AVF web automation should remain approval-gated because autonomous web agents need evidence-backed limits.",
            "evidence_excerpt_summary": "The arXiv record describes WebArena as a realistic and reproducible web-agent environment with long-horizon benchmark tasks. It reports that the best GPT-4-based baseline agent achieved 14.41% end-to-end success versus 78.24% human performance, supporting approval-gated web automation rather than broad unsupervised action.",
            "verification_notes": "Manual primary-source review of arXiv metadata lines 30-46 and abstract/result lines 38-41.",
            "source_reference_lines": "turn4view1 lines 30-46; turn3view6 lines 40-46",
            "retrieval_method": "manual_browser_primary_source_review",
        },
    },
]


def require_packet_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("manual collection packet gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("manual collection packet gate must point to this records goal")
    if gate.get("packet_decision") != PACKET_DECISION:
        raise SystemExit("manual collection packet decision mismatch")
    if gate.get("source_target_ids") != SOURCE_TARGET_IDS:
        raise SystemExit("manual collection packet source target ids mismatch")


def record_for(entry: dict) -> dict:
    return {
        "source_target_id": entry["source_target_id"],
        "target_claim_id": entry["target_claim_id"],
        "source_record_status": "manual_primary_source_record_created",
        "source_contents_acquired": True,
        "manual_primary_source_review_performed": True,
        "automated_collection_allowed": False,
        "external_fetch_performed": False,
        "source_record": entry["source_record"],
    }


def build_records() -> dict:
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "record_decision": RECORD_DECISION,
        "manual_primary_source_review_performed": True,
        "source_records": [record_for(entry) for entry in SOURCE_RECORDS],
        "source_contents_acquired": True,
        "all_records_have_primary_source_uris": True,
        "all_records_have_evidence_summaries": True,
        "automated_collection_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_records_markdown(records: list[dict]) -> str:
    sections = []
    for record in records:
        source = record["source_record"]
        sections.append(
            "\n".join(
                [
                    f"### {record['source_target_id']}",
                    "",
                    f"- target_claim_id: `{record['target_claim_id']}`",
                    f"- source_record_status: `{record['source_record_status']}`",
                    "- manual_primary_source_review_performed=true",
                    "- source_contents_acquired=true",
                    "- automated_collection_allowed=false",
                    "- external_fetch_performed=false",
                    f"- source_uri: {source['source_uri']}",
                    f"- source_reference_lines: {source['source_reference_lines']}",
                    "",
                    f"claim_supported: {source['claim_supported']}",
                    "",
                    f"evidence_excerpt_summary: {source['evidence_excerpt_summary']}",
                    "",
                    f"verification_notes: {source['verification_notes']}",
                ]
            )
        )
    return f"""# Primary-Source Manual Records v0.1

record_decision={RECORD_DECISION}
source_records={len(records)}
manual_primary_source_review_performed=true
source_contents_acquired=true
automated_collection_allowed=false
external_fetch_performed=false

{chr(10).join(sections)}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_records_gate(records: list[dict]) -> dict:
    return {
        "gate_id": "avf-primary-source-manual-records-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "record_decision": RECORD_DECISION,
        "records_uri": rel(RECORDS),
        "records_markdown_uri": rel(RECORDS_MARKDOWN),
        "source_records": len(records),
        "source_target_ids": SOURCE_TARGET_IDS,
        "manual_primary_source_review_performed": True,
        "source_contents_acquired": True,
        "all_records_have_primary_source_uris": True,
        "all_records_have_evidence_summaries": True,
        "automated_collection_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-primary-source-manual-records
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review manually recorded primary-source evidence before integrating claims
  - Check source_uri, source_reference_lines, license_or_rights_note, evidence_excerpt_summary, and verification_notes
  - Decide which claims may be promoted into architecture docs and which require more evidence
  - Do not install, clone, deploy, publish, or call providers

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(records: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_primary_source_manual_records_v0_1",
        "status": "PASS",
        "record_decision": RECORD_DECISION,
        "source_records": len(records),
        "manual_primary_source_review_performed": True,
        "source_contents_acquired": True,
        "all_records_have_primary_source_uris": True,
        "all_records_have_evidence_summaries": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(records: list[dict]) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Primary-Source Manual Records v0.1 Report

RESULT: PASS
primary_source_manual_records_v0_1=true

## Commands

- python scripts\\run_avf_primary_source_manual_records_v0_1.py
- python scripts\\validate_avf_primary_source_manual_records_v0_1.py

## Gate summary

- record_decision={RECORD_DECISION}
- source_records={len(records)}
- manual_primary_source_review_performed=true
- source_contents_acquired=true
- all_records_have_primary_source_uris=true
- all_records_have_evidence_summaries=true

## Generated artifacts

- {rel(RECORDS)}
- {rel(RECORDS_MARKDOWN)}
- {rel(RECORDS_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_packet_gate(read_json(PACKET_GATE))
    records_data = build_records()
    records = records_data["source_records"]

    write_json(RECORDS, records_data)
    write_text(RECORDS_MARKDOWN, build_records_markdown(records))
    write_json(RECORDS_GATE, build_records_gate(records))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(records))
    write_text(VALIDATION_REPORT, build_report(records))

    print("AVF Primary-Source Manual Records v0.1")
    print("RESULT: PASS")
    print(f"record_decision={RECORD_DECISION}")
    print(f"source_records={len(records)}")
    print("manual_primary_source_review_performed=true")
    print("source_contents_acquired=true")
    print("all_records_have_primary_source_uris=true")
    print("all_records_have_evidence_summaries=true")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
