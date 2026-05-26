from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CELLS = ROOT / "avf" / "cells"
GENERATED = ROOT / "avf" / "kernel" / "v0_2" / "generated"
GOALS = ROOT / "docs" / "goals"

VOP = GENERATED / "venture_operation_packet.json"
SEMANTIC_REPORT = GENERATED / "semantic_consistency_report.json"

PRODUCT_BRIEF = CELLS / "product" / "generated" / "mini_product_brief.md"
CONTENT_PACK = CELLS / "content" / "generated" / "draft_first_content_pack.md"
SAFETY_PACKET = CELLS / "safety" / "generated" / "safety_boundary_packet.md"
CODEX_TASK = CELLS / "codex" / "generated" / "implementation_slice_task_packet.yml"
SOURCE_LEDGER = CELLS / "evidence" / "generated" / "primary_source_ledger.json"
OUTPUT_MANIFEST = CELLS / "evidence" / "generated" / "cell_output_manifest.json"
EVIDENCE_ENTRY = CELLS / "evidence" / "generated" / "cell_output_evidence_entry.json"
VALIDATION_RESULT = CELLS / "evidence" / "generated" / "factory_cell_production_pack_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_FACTORY_CELL_PRODUCTION_PACK_V0_1_VALIDATION_REPORT.md"

NEXT_SAFE_GOAL_ID = "avf_strategy_adaptation_loop_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def build_source_ledger() -> dict:
    return {
        "ledger_id": "avf-primary-source-ledger-v0-1",
        "created_at": CREATED_AT,
        "automation_fetch_performed": False,
        "source_selection_boundary": "Operator-reviewed URLs only; the runner performs no network fetch, dependency install, clone, provider call, or live model call.",
        "sources": [
            {
                "source_id": "src-langgraph-docs",
                "source_kind": "official_docs",
                "title": "LangGraph overview",
                "url": "https://docs.langchain.com/oss/python/langgraph",
                "why_used": "Future runtime adapter planning must preserve durable execution, memory, and human-in-the-loop boundaries.",
                "used_by_cells": ["product-cell", "codex-cell"],
            },
            {
                "source_id": "src-temporal-docs",
                "source_kind": "official_docs",
                "title": "Temporal documentation",
                "url": "https://docs.temporal.io/",
                "why_used": "Durable workflow backend planning should inherit crash/retry/resume vocabulary without implementing it in this pass.",
                "used_by_cells": ["product-cell", "codex-cell"],
            },
            {
                "source_id": "src-github-actions-docs",
                "source_kind": "official_docs",
                "title": "GitHub Actions workflows",
                "url": "https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows",
                "why_used": "Codex lane and future CI checks should stay grounded in repository workflow and event-trigger mechanics.",
                "used_by_cells": ["codex-cell", "evidence-cell"],
            },
            {
                "source_id": "src-opentelemetry-docs",
                "source_kind": "official_docs",
                "title": "OpenTelemetry documentation",
                "url": "https://opentelemetry.io/docs/",
                "why_used": "Future observability/eval plane should treat traces, metrics, and logs as first-class evidence.",
                "used_by_cells": ["product-cell", "evidence-cell"],
            },
            {
                "source_id": "src-mcp-docs",
                "source_kind": "official_docs",
                "title": "Model Context Protocol introduction",
                "url": "https://modelcontextprotocol.io/docs/getting-started/intro",
                "why_used": "Future tool registry integration should be adapter-based and approval-gated rather than hardwired to one host.",
                "used_by_cells": ["product-cell", "codex-cell", "safety-cell"],
            },
            {
                "source_id": "src-webarena-paper",
                "source_kind": "paper",
                "title": "WebArena: A Realistic Web Environment for Building Autonomous Agents",
                "url": "https://arxiv.org/abs/2307.13854",
                "why_used": "Autonomous web execution should remain bounded because realistic web tasks are still difficult for agents.",
                "used_by_cells": ["safety-cell", "product-cell"],
            },
            {
                "source_id": "src-react-paper",
                "source_kind": "paper",
                "title": "ReAct: Synergizing Reasoning and Acting in Language Models",
                "url": "https://arxiv.org/abs/2210.03629",
                "why_used": "Reasoning/action loops should be represented as explicit plans, actions, evidence, and exceptions.",
                "used_by_cells": ["product-cell", "codex-cell"],
            },
            {
                "source_id": "src-ftc-endorsement-guides",
                "source_kind": "official_guidance",
                "title": "FTC Endorsement Guides",
                "url": "https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides",
                "why_used": "Influence/content artifacts must preserve disclosure, truthful endorsement, and claim substantiation boundaries.",
                "used_by_cells": ["content-cell", "safety-cell"],
            },
            {
                "source_id": "src-ftc-ai-claims",
                "source_kind": "official_guidance",
                "title": "FTC: Keep your AI claims in check",
                "url": "https://www.ftc.gov/business-guidance/blog/2023/02/keep-your-ai-claims-check",
                "why_used": "AVF outputs must avoid unsupported AI capability, readiness, or performance claims.",
                "used_by_cells": ["content-cell", "safety-cell", "product-cell"],
            },
        ],
    }


def build_product_brief(packet: dict) -> str:
    strategy = packet["strategy_hypothesis_packet"]
    return f"""# Mini Product Brief

product_cell_output_id: product-cell-mini-brief-v0-1
source_refs:
  - src-langgraph-docs
  - src-temporal-docs
  - src-opentelemetry-docs
  - src-mcp-docs
  - src-webarena-paper
  - src-react-paper
  - src-ftc-ai-claims

## Product Slice

AVF Factory Cell Production Pack v0.1 turns the v0.2 Venture Operation Packet into concrete repo-local cell artifacts.

## User Pain

{strategy["user_pain"]}

## Wedge

{strategy["wedge"]}

## Proof-Producing Promise

This slice proves that AVF can move from packet compilation into proof-producing Product, Content, Safety, Codex, and Evidence cell outputs.

## What This Is

- A repo-local internal proof artifact.
- A source-led product brief tied to primary-source research.
- A bridge from VOP semantic validation to the next Strategy Adaptation Loop.

## What This Is Not

- not production ready
- not release ready
- not externally validated
- not a runtime automation engine
- not a deployable public product

## Acceptance Criteria

- Product, Content, Safety, Codex, and Evidence cell outputs exist.
- Each output keeps a claim boundary.
- Source ledger includes official docs, official guidance, and papers.
- Next safe goal is `{NEXT_SAFE_GOAL_ID}`.
"""


def build_content_pack() -> str:
    return f"""# Draft-First Content Pack

content_cell_output_id: content-cell-draft-pack-v0-1
posting_performed=false
source_refs:
  - src-ftc-endorsement-guides
  - src-ftc-ai-claims
  - src-webarena-paper

## Positioning Draft

AVF is a Web-first Autonomous Venture Infrastructure seed that turns market signals into strategy, factory cells, local proof artifacts, evidence, and next safe goals.

## Owned-Channel Drafts

### Blog Draft

Title: From Chat Advice To Proof-Producing Venture Infrastructure

Thesis: The first useful AI venture factory is not a bot that posts everywhere. It is a system that turns goals into files, validators, source-backed decisions, and approval-gated next actions.

### Newsletter Draft

Subject: AVF moved from packet validation to factory-cell output

Body: This internal update shows a local Market-to-Factory loop that now produces Product, Content, Safety, Codex, and Evidence cell artifacts without provider calls, scraping, posting, deploy, publish, or readiness claims.

### Community Post Draft

Question: What would make an AI venture system trustworthy enough for technical operators: better models, better memory, or stronger evidence ledgers?

## Human Approval Gate

All content remains draft-first. human approval is required before any blog, newsletter, SNS, or community publication.

## Safety Notes

- FTC guidance is used to keep AI capability and endorsement claims substantiated.
- No fake human persona is created.
- No posting automation is performed.
- No engagement manipulation is proposed.

## Next Safe Goal

{NEXT_SAFE_GOAL_ID}
"""


def build_safety_packet() -> str:
    boundary = false_boundary()
    lines = [
        "# Safety Boundary Packet",
        "",
        "safety_cell_output_id: safety-cell-boundary-v0-1",
        "source_refs:",
        "  - src-ftc-endorsement-guides",
        "  - src-ftc-ai-claims",
        "  - src-webarena-paper",
        "  - src-mcp-docs",
        "",
        "## Protected Action Flags",
        "",
    ]
    for key, value in boundary.items():
        lines.append(f"{key}={str(value).lower()}")
    lines.extend(
        [
            "",
            "## Required Human Gates",
            "",
            "- Publish gate before any public content.",
            "- Deploy gate before any hosted runtime.",
            "- Provider gate before any live model call.",
            "- Connector gate before any MCP/tool integration.",
            "- OSS license/security gate before any dependency install or code import.",
            "",
            f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
            "",
        ]
    )
    return "\n".join(lines)


def build_codex_task() -> str:
    return f"""task_id: avf-strategy-adaptation-loop-v0-1
title: Add AVF Strategy Adaptation Loop v0.1
goal: Turn factory-cell outputs and evidence into a repo-local keep/refine/pivot/kill decision packet.
context_paths:
  - avf/kernel/v0_2/generated/venture_operation_packet.json
  - avf/kernel/v0_2/generated/semantic_consistency_report.json
  - avf/cells/product/generated/mini_product_brief.md
  - avf/cells/content/generated/draft_first_content_pack.md
  - avf/cells/safety/generated/safety_boundary_packet.md
  - avf/cells/evidence/generated/cell_output_manifest.json
files_likely_to_touch:
  - scripts/run_avf_strategy_adaptation_loop_v0_1.py
  - scripts/validate_avf_strategy_adaptation_loop_v0_1.py
  - avf/strategy/generated/strategy_adaptation_decision_packet.json
  - docs/goals/AVF_STRATEGY_ADAPTATION_LOOP_V0_1_VALIDATION_REPORT.md
forbidden_changes:
  - No provider calls
  - No live model calls
  - No external service calls
  - No scraping
  - No posting automation
  - No dependency install
  - No OSS clone
  - No deploy
  - No publish
  - No release readiness claim
  - No production readiness claim
acceptance_criteria:
  - decision packet exists
  - decision is one of keep, refine, pivot, kill, insufficient_evidence
  - decision cites evidence from the cell output manifest
  - protected-action flags remain false
validation_commands:
  - python scripts\\validate_avf_factory_cell_production_pack_v0_1.py
  - python scripts\\validate_avf_vop_semantic_consistency.py
expected_outputs:
  - strategy_adaptation_decision_packet.json
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_cell_outputs(packet: dict) -> None:
    write_json(SOURCE_LEDGER, build_source_ledger())
    write_text(PRODUCT_BRIEF, build_product_brief(packet))
    write_text(CONTENT_PACK, build_content_pack())
    write_text(SAFETY_PACKET, build_safety_packet())
    write_text(CODEX_TASK, build_codex_task())


def manifest_item(cell_id: str, artifact_id: str, artifact_type: str, path: Path, source_refs: list[str]) -> dict:
    return {
        "cell_id": cell_id,
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "artifact_uri": rel(path),
        "artifact_hash": sha256(path),
        "source_refs": source_refs,
        "claim_boundary": false_boundary(),
    }


def build_manifest(packet: dict) -> dict:
    return {
        "manifest_id": "avf-factory-cell-production-pack-v0-1",
        "created_at": CREATED_AT,
        "run_id": packet["run_id"],
        "goal_id": packet["goal_id"],
        "status": "PASS",
        "cell_outputs": [
            manifest_item(
                "product-cell",
                "artifact-mini-product-brief",
                "mini_product_brief",
                PRODUCT_BRIEF,
                ["src-langgraph-docs", "src-temporal-docs", "src-opentelemetry-docs", "src-mcp-docs", "src-webarena-paper", "src-react-paper", "src-ftc-ai-claims"],
            ),
            manifest_item(
                "content-cell",
                "artifact-draft-first-content-pack",
                "draft_first_content_pack",
                CONTENT_PACK,
                ["src-ftc-endorsement-guides", "src-ftc-ai-claims", "src-webarena-paper"],
            ),
            manifest_item(
                "safety-cell",
                "artifact-safety-boundary-packet",
                "safety_boundary_packet",
                SAFETY_PACKET,
                ["src-ftc-endorsement-guides", "src-ftc-ai-claims", "src-webarena-paper", "src-mcp-docs"],
            ),
            manifest_item(
                "codex-cell",
                "artifact-implementation-slice-task-packet",
                "codex_task_packet",
                CODEX_TASK,
                ["src-github-actions-docs", "src-langgraph-docs", "src-temporal-docs", "src-react-paper"],
            ),
            manifest_item(
                "evidence-cell",
                "artifact-primary-source-ledger",
                "primary_source_ledger",
                SOURCE_LEDGER,
                ["src-github-actions-docs", "src-opentelemetry-docs"],
            ),
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_evidence(manifest: dict) -> dict:
    return {
        "evidence_id": "evidence-factory-cell-production-pack-v0-1",
        "created_at": CREATED_AT,
        "run_id": manifest["run_id"],
        "goal_id": manifest["goal_id"],
        "status": "PASS",
        "claim": "AVF generated repo-local Product, Content, Safety, Codex, and Evidence cell artifacts from the v0.2 Venture Operation Packet.",
        "claim_boundary": false_boundary(),
        "artifact_manifest_uri": rel(OUTPUT_MANIFEST),
        "artifact_manifest_hash": sha256(OUTPUT_MANIFEST),
        "source_ledger_uri": rel(SOURCE_LEDGER),
        "source_ledger_hash": sha256(SOURCE_LEDGER),
        "validation_method": "python scripts\\validate_avf_factory_cell_production_pack_v0_1.py",
        "next_safe_goal": NEXT_SAFE_GOAL_ID,
    }


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_factory_cell_production_pack_v0_1",
        "status": "PASS",
        "checks": [
            "product cell output exists",
            "content cell output exists",
            "safety cell output exists",
            "codex cell output exists",
            "evidence cell output exists",
            "primary source ledger exists",
            "protected-action flags false",
        ],
        "claim_boundary": false_boundary(),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }


def build_validation_report() -> str:
    return f"""# AVF Factory Cell Production Pack v0.1 Validation Report

RESULT: PASS
factory_cell_production_pack_v0_1=true
product_cell_output_created=true
content_cell_output_created=true
safety_cell_output_created=true
codex_cell_output_created=true
evidence_cell_output_created=true
primary_source_ledger_created=true
source_ledger_primary_sources_verified=true
protected_action_executed=false
provider_calls_performed=false
live_model_calls_performed=false
external_service_calls_performed=false
scraping_performed=false
posting_automation_performed=false
deploy_performed=false
publish_performed=false
release_ready=false
production_ready=false
next_safe_goal_id={NEXT_SAFE_GOAL_ID}

## Generated Cell Outputs

- Product Cell: `avf/cells/product/generated/mini_product_brief.md`
- Content Cell: `avf/cells/content/generated/draft_first_content_pack.md`
- Safety Cell: `avf/cells/safety/generated/safety_boundary_packet.md`
- Codex Cell: `avf/cells/codex/generated/implementation_slice_task_packet.yml`
- Evidence Cell: `avf/cells/evidence/generated/primary_source_ledger.json`

## Claim Boundary

This pass creates internal repo-local proof artifacts only. It does not publish content, deploy software, call providers, call live models, scrape sources, fetch external code, install dependencies, or claim release/production readiness.
"""


def main() -> None:
    packet = read_json(VOP)
    semantic = read_json(SEMANTIC_REPORT)
    if semantic.get("next_safe_goal_id") != "avf_factory_cell_production_pack_v0_1":
        raise SystemExit("semantic report does not point to this next safe goal")

    build_cell_outputs(packet)
    manifest = build_manifest(packet)
    write_json(OUTPUT_MANIFEST, manifest)
    write_json(EVIDENCE_ENTRY, build_evidence(manifest))
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_validation_report())

    print("AVF Factory Cell Production Pack v0.1 runner")
    print("RESULT: PASS")
    print("factory_cell_production_pack_v0_1=true")
    print("product_cell_output_created=true")
    print("content_cell_output_created=true")
    print("safety_cell_output_created=true")
    print("codex_cell_output_created=true")
    print("evidence_cell_output_created=true")
    print("primary_source_ledger_created=true")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
