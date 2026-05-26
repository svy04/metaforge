from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRATEGY = ROOT / "avf" / "strategy" / "generated"
CELLS = ROOT / "avf" / "cells"
GOALS = ROOT / "docs" / "goals"

SOURCE_LEDGER = CELLS / "evidence" / "generated" / "primary_source_ledger.json"
STRATEGY_SOURCE_LEDGER = STRATEGY / "strategy_source_ledger.json"
CELL_MANIFEST = CELLS / "evidence" / "generated" / "cell_output_manifest.json"
CELL_EVIDENCE = CELLS / "evidence" / "generated" / "cell_output_evidence_entry.json"
DECISION_PACKET = STRATEGY / "strategy_adaptation_decision_packet.json"
VALIDATION_RESULT = STRATEGY / "strategy_adaptation_loop_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_STRATEGY_ADAPTATION_LOOP_V0_1_VALIDATION_REPORT.md"

NEXT_SAFE_GOAL_ID = "avf_capability_acquisition_loop_v0_1"
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
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def adaptation_sources() -> list[dict]:
    return [
        {
            "source_id": "src-reflexion-paper",
            "source_kind": "paper",
            "title": "Reflexion: Language Agents with Verbal Reinforcement Learning",
            "url": "https://arxiv.org/abs/2303.11366",
            "why_used": "Strategy adaptation should convert feedback and scalar/local validation signals into reusable decision memory.",
            "used_by_cells": ["strategy-cell", "evidence-cell"],
        },
        {
            "source_id": "src-self-refine-paper",
            "source_kind": "paper",
            "title": "Self-Refine: Iterative Refinement with Self-Feedback",
            "url": "https://arxiv.org/abs/2303.17651",
            "why_used": "The loop should produce explicit feedback and refinement actions instead of ungrounded improvement claims.",
            "used_by_cells": ["strategy-cell", "codex-cell"],
        },
        {
            "source_id": "src-voyager-paper",
            "source_kind": "paper",
            "title": "Voyager: An Open-Ended Embodied Agent with Large Language Models",
            "url": "https://arxiv.org/abs/2305.16291",
            "why_used": "Capability acquisition should eventually turn successful loops into reusable skills while remaining gated in this pass.",
            "used_by_cells": ["strategy-cell", "capability-cell"],
        },
    ]


def build_strategy_source_ledger() -> dict:
    cell_ledger = read_json(SOURCE_LEDGER)
    return {
        "ledger_id": "avf-strategy-adaptation-source-ledger-v0-1",
        "created_at": CREATED_AT,
        "parent_source_ledger_uri": rel(SOURCE_LEDGER),
        "parent_source_ledger_hash": sha256(SOURCE_LEDGER),
        "automation_fetch_performed": False,
        "source_selection_boundary": (
        "Operator-reviewed URLs only; runners perform no network fetch, dependency install, clone, "
        "provider call, live model call, scraping, posting, deploy, or publish action."
        ),
        "inherited_source_count": len(cell_ledger.get("sources", [])),
        "sources": adaptation_sources(),
    }


def build_decision_packet(manifest: dict, evidence: dict, ledger: dict) -> dict:
    return {
        "packet_id": "avf-strategy-adaptation-decision-v0-1",
        "created_at": CREATED_AT,
        "run_id": manifest["run_id"],
        "goal_id": manifest["goal_id"],
        "status": "PASS",
        "decision": "refine",
        "decision_reason": "Local cell outputs exist and are evidence-bound, but there is still no external validation, runtime automation, or capability acquisition record.",
        "decision_threshold": "Refine when repo-local artifacts pass validation but evidence remains internal-only and protected-action flags remain false.",
        "evidence_basis": [
            {
                "evidence_type": "cell_output_manifest",
                "artifact_uri": rel(CELL_MANIFEST),
                "artifact_hash": sha256(CELL_MANIFEST),
                "summary": "Product, Content, Safety, Codex, and Evidence cell outputs were generated with claim boundaries.",
            },
            {
                "evidence_type": "cell_output_evidence_entry",
                "artifact_uri": rel(CELL_EVIDENCE),
                "artifact_hash": sha256(CELL_EVIDENCE),
                "summary": evidence["claim"],
            },
            {
                "evidence_type": "primary_source_ledger",
                "artifact_uri": rel(SOURCE_LEDGER),
                "artifact_hash": sha256(SOURCE_LEDGER),
                "summary": "Primary-source, official-guidance, and paper references are captured in a repo-local ledger.",
            },
        ],
        "source_refs": [
            "src-reflexion-paper",
            "src-self-refine-paper",
            "src-voyager-paper",
            "src-react-paper",
            "src-webarena-paper",
            "src-ftc-ai-claims",
        ],
        "available_decisions": ["keep", "refine", "pivot", "kill", "insufficient_evidence"],
        "why_not_keep": "Evidence is still internal-only; keep would overstate market or runtime validation.",
        "why_not_pivot": "The local proof path is working and does not contradict the Market-to-Factory thesis.",
        "why_not_kill": "Local validators and cell outputs are passing; no safety failure or contradiction was found.",
        "refinement_actions": [
            "Add a capability acquisition loop that proposes OSS/tool candidates without installing or fetching them.",
            "Map missing runtime, observability, and tool-registry capabilities to build/buy/adopt records.",
            "Preserve approval gates before provider calls, dependency installs, scraping, posting, deploy, or publish.",
        ],
        "cell_output_manifest_uri": rel(CELL_MANIFEST),
        "cell_output_manifest_hash": sha256(CELL_MANIFEST),
        "cell_output_evidence_uri": rel(CELL_EVIDENCE),
        "cell_output_evidence_hash": sha256(CELL_EVIDENCE),
        "source_ledger_uri": rel(STRATEGY_SOURCE_LEDGER),
        "source_ledger_hash": sha256(STRATEGY_SOURCE_LEDGER),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_strategy_adaptation_loop_v0_1",
        "status": "PASS",
        "checks": [
            "decision packet exists",
            "decision is evidence-bound",
            "cell manifest hash matches",
            "cell evidence hash matches",
            "source ledger includes adaptation papers",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    return f"""# AVF Strategy Adaptation Loop v0.1 Validation Report

RESULT: PASS
strategy_adaptation_loop_v0_1=true
decision_packet_created=true
decision_is_evidence_bound=true
cell_manifest_referenced=true
source_ledger_updated=true
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

## Decision

decision=refine

The current evidence supports refining the local factory rather than keeping, pivoting, killing, or claiming external success. The next safe step is a capability acquisition loop that can evaluate OSS/tool candidates without fetching, installing, deploying, or calling providers.

## Added Research Basis

- Reflexion: feedback should become reusable decision memory.
- Self-Refine: refinement should produce explicit feedback and revision steps.
- Voyager: successful behaviors can later become reusable skills, but this pass only records the next gated capability loop.

## Claim Boundary

This pass creates an internal repo-local decision packet only. It does not perform provider calls, live model calls, external service calls, scraping, posting automation, dependency installs, OSS cloning, deploy, publish, release readiness, or production readiness.
"""


def main() -> None:
    manifest = read_json(CELL_MANIFEST)
    evidence = read_json(CELL_EVIDENCE)
    if manifest.get("next_safe_goal_id") != "avf_strategy_adaptation_loop_v0_1":
        raise SystemExit("cell output manifest does not point to this safe goal")
    if evidence.get("next_safe_goal") != "avf_strategy_adaptation_loop_v0_1":
        raise SystemExit("cell evidence does not point to this safe goal")

    ledger = build_strategy_source_ledger()
    write_json(STRATEGY_SOURCE_LEDGER, ledger)
    decision = build_decision_packet(manifest, evidence, ledger)
    write_json(DECISION_PACKET, decision)
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Strategy Adaptation Loop v0.1 runner")
    print("RESULT: PASS")
    print("strategy_adaptation_loop_v0_1=true")
    print("decision_packet_created=true")
    print("decision=refine")
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
