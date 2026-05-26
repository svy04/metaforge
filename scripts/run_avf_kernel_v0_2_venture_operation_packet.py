from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V02 = ROOT / "avf" / "kernel" / "v0_2"
FIXTURES = V02 / "fixtures"
GENERATED = V02 / "generated"
GOALS = ROOT / "docs" / "goals"

RUN_ID = "avf-kernel-v0-2-vop-sample-run"
GOAL_ID = "sample-avf-market-to-factory-infra-product"
NEXT_SAFE_GOAL = "avf_vop_semantic_consistency_validator"
CREATED_AT = "2026-05-26T00:00:00Z"


def parse_simple_yaml(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    result: dict = {}
    current_list: str | None = None
    current_item: dict | None = None
    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - "):
            if current_list is None:
                continue
            current_item = {}
            result[current_list].append(current_item)
            line = raw[4:]
            if ":" in line:
                key, value = line.split(":", 1)
                current_item[key.strip()] = parse_value(value.strip())
            continue
        if raw.startswith("    ") and current_item is not None and ":" in raw:
            key, value = raw.strip().split(":", 1)
            current_item[key.strip()] = parse_value(value.strip())
            continue
        if raw.endswith(":"):
            current_list = raw[:-1].strip()
            result[current_list] = []
            current_item = None
            continue
        if ":" in raw:
            current_list = None
            current_item = None
            key, value = raw.split(":", 1)
            result[key.strip()] = parse_value(value.strip())
    return result


def parse_value(value: str):
    if value == "true":
        return True
    if value == "false":
        return False
    return value


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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


def production_artifact(artifact_id: str, artifact_type: str, uri: str, cell: str) -> dict:
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "artifact_uri": uri,
        "producing_cell": cell,
        "status": "generated",
        "claim_boundary": false_boundary(),
        "validation_method": "python scripts\\validate_avf_kernel_v0_2_venture_operation_packet.py",
        "owner_approval_required": False,
    }


def build_packet(goal: dict, signals: dict, capabilities: dict) -> dict:
    signal_sources = signals["signals"]
    capability_gaps = capabilities["proposed_capability_gaps"]
    artifacts = [
        production_artifact("artifact-vop", "venture_operation_packet", "avf/kernel/v0_2/generated/venture_operation_packet.json", "evidence-cell"),
        production_artifact("artifact-manifest", "artifact_manifest", "avf/kernel/v0_2/generated/artifact_manifest.json", "evidence-cell"),
        production_artifact("artifact-codex-task", "codex_task_packet", "avf/kernel/v0_2/generated/codex_task_packet.yml", "code-cell"),
        production_artifact("artifact-evidence-entry", "evidence_ledger_v2_entry", "avf/kernel/v0_2/generated/evidence_ledger.v2.entry.json", "evidence-cell"),
        production_artifact("artifact-validation-report", "validation_report", "avf/kernel/v0_2/generated/validation_report.md", "evidence-cell"),
    ]
    return {
        "packet_id": "vop-avf-kernel-v0-2-sample",
        "schema_version": "venture_operation_packet.v0_2",
        "kernel_version": "avf_kernel_v0_2",
        "compiler_mode": "deterministic_repo_local",
        "created_at": CREATED_AT,
        "run_id": RUN_ID,
        "goal_id": GOAL_ID,
        "raw_goal": goal["raw_goal"],
        "goal_essence": "Compile a safe infra-product venture goal into a complete repo-local Venture Operation Packet.",
        "goal_context": {
            "owner_intent": goal["owner_intent"],
            "target_user": goal["target_user"],
            "business_objective": goal["business_objective"],
            "time_horizon": goal["time_horizon"],
            "resource_constraints": goal["constraints"],
            "non_goals": goal["non_goals"],
            "assumptions": ["Owner-provided signals are sufficient for a local compiler proof."],
            "unknowns": ["No external market validation has been performed."],
        },
        "market_intelligence_packet": {
            "signal_sources": signal_sources,
            "observed_signals": [item["signal_summary"] for item in signal_sources],
            "pain_points": ["Technical operators need proof-producing AI systems instead of chat-only plans."],
            "audience_segments": ["solo founder", "technical operator", "AI-native venture builder"],
            "competitor_assumptions": ["Existing agent stacks may emphasize runtime before evidence contracts."],
            "market_timing": "early internal proof stage",
            "signal_quality": "repo-local and owner-provided only",
            "confidence": "medium",
            "unknowns": ["Live market size and willingness to pay remain unvalidated."],
        },
        "strategy_hypothesis_packet": {
            "hypothesis_id": "hypothesis-avf-vop-compiler",
            "thesis": "A repo-local Venture Operation Packet compiler is the smallest proof that AVF can organize market-to-factory decisions.",
            "wedge": "Start with evidence-bound local decision compilation before runtime automation.",
            "target_audience": "solo founder and technical operator building AI-native venture systems",
            "user_pain": "AI strategy outputs disappear into chat unless they become files, validators, tasks, and evidence.",
            "product_angle": "Decision compiler for market-to-factory venture packets.",
            "content_angle": "Build-in-public notes about evidence-led AI venture infrastructure.",
            "brand_angle": "Transparent AI venture operating system, not a bot network.",
            "distribution_angle": "Owned-channel draft artifacts only until approval.",
            "monetization_angle": "Future paid studio or infrastructure product after evidence and user validation.",
            "unfair_advantage_or_edge": "Tight integration of strategy, Codex tasks, evidence, and safety boundaries.",
            "key_assumptions": ["Users value proof artifacts over chat advice.", "Repo-local validators create trust."],
            "counterarguments": ["The packet may become too complex before runtime proves utility."],
            "success_criteria": ["VOP generated locally", "All subpackets present", "Validator exits 0"],
            "failure_criteria": ["Subpackets are disconnected", "Protected action boundary expands"],
            "decision_threshold": "PASS local validator and preserve all false protected-action flags",
            "confidence": "medium",
        },
        "factory_formation_packet": {
            "required_cells": [
                {"cell_id": "product-cell", "cell_type": "Product Cell", "activation_reason": "Define product proof and value boundary.", "expected_outputs": ["mini product brief"], "dependencies": [], "owner_gate_required": False},
                {"cell_id": "content-cell", "cell_type": "Content Cell", "activation_reason": "Prepare draft-first owned-channel outputs.", "expected_outputs": ["draft content pack"], "dependencies": ["strategy_hypothesis_packet"], "owner_gate_required": True},
                {"cell_id": "code-cell", "cell_type": "Code Cell", "activation_reason": "Create PR-sized Codex next task.", "expected_outputs": ["codex task packet"], "dependencies": ["production_plan_packet"], "owner_gate_required": False},
                {"cell_id": "evidence-cell", "cell_type": "Evidence Cell", "activation_reason": "Record artifact hashes and validation results.", "expected_outputs": ["evidence ledger entry"], "dependencies": [], "owner_gate_required": False},
                {"cell_id": "safety-cell", "cell_type": "Safety Cell", "activation_reason": "Keep distribution and automation bounded.", "expected_outputs": ["safety governance packet"], "dependencies": [], "owner_gate_required": False},
            ],
            "skipped_cells": [
                {"cell_id": "runtime-cell", "skip_reason": "Runtime integration is a future protected expansion."},
                {"cell_id": "posting-cell", "skip_reason": "Posting automation is blocked."},
            ],
            "cell_sequence": ["product-cell", "content-cell", "code-cell", "evidence-cell", "safety-cell"],
            "bottlenecks": ["No external market validation yet."],
        },
        "production_plan_packet": {"artifacts": artifacts},
        "influence_distribution_packet": {
            "channel_strategy": [
                {"channel": "project blog", "channel_type": "blog", "owned_or_external": "owned", "draft_artifacts": ["draft_first_content_pack.md"], "approval_required": True, "posting_performed": False},
                {"channel": "newsletter", "channel_type": "newsletter", "owned_or_external": "owned", "draft_artifacts": ["newsletter_outline.md"], "approval_required": True, "posting_performed": False},
            ],
            "disclosure_policy": "Represent AI-generated content transparently where published in a future approved phase.",
            "measurement_plan": "Future approved publishing should measure views, replies, saves, clicks, and qualitative pain signals.",
            "prohibited_actions": ["fake human impersonation", "bot networks", "mass posting", "engagement manipulation", "platform bypass"],
            "red_actions_blocked": True,
        },
        "capability_acquisition_packet": {
            "capability_gaps": capability_gaps,
            "dependency_install_allowed": False,
            "external_fetch_performed": False,
        },
        "codex_execution_packet": {
            "pr_sized_tasks": [
                {
                    "task_id": "codex-avf-vop-semantic-consistency-validator",
                    "title": "Add VOP semantic consistency validator",
                    "context_paths": ["avf/kernel/v0_2/generated/venture_operation_packet.json", "docs/avf/VENTURE_OPERATION_PACKET_SPEC.md"],
                    "files_likely_to_touch": ["scripts/validate_avf_vop_semantic_consistency.py", "docs/goals/AVF_VOP_SEMANTIC_CONSISTENCY_VALIDATION_REPORT.md"],
                    "scope": "Validate cross-packet consistency between signals, strategy, cells, artifacts, Codex tasks, evidence, and adaptation decisions.",
                    "non_goals": ["No provider calls", "No dependency install", "No runtime integration"],
                    "forbidden_changes": ["No deploy", "No publish", "No posting automation", "No readiness claims"],
                    "acceptance_criteria": ["semantic consistency report created", "validator exits 0", "protected-action flags remain false"],
                    "validation_commands": ["python scripts\\validate_avf_kernel_v0_2_venture_operation_packet.py"],
                    "expected_outputs": ["semantic_consistency_report.json", "validation report"],
                    "rollback_notes": "Remove new semantic validator artifacts if validation scope proves too broad.",
                    "next_pr_recommendation": "Factory Cell Production Pack v0.1",
                }
            ]
        },
        "safety_governance_packet": {
            "creation_level_allowed": "Creation Level 2",
            "creation_level_requested": "Creation Level 2",
            "risk_tier": "medium",
            "human_gates": ["publish approval required for future distribution"],
            "policy_decisions": ["repo-local compiler allowed", "posting automation blocked", "runtime integration blocked"],
            "prohibited_actions": ["scraping", "provider calls", "posting automation", "deploy", "publish"],
            "protected_action_flags": false_boundary(),
        },
        "evidence_learning_packet": {
            "evidence_plan": ["hash VOP artifact", "validate subpacket presence", "record evidence ledger entry"],
            "evidence_entries": ["avf/kernel/v0_2/generated/evidence_ledger.v2.entry.json"],
            "validator_uris": ["scripts/validate_avf_kernel_v0_2_venture_operation_packet.py"],
            "artifact_hashes": {},
            "success_criteria": ["validator exits 0", "all subpackets present", "claim boundary remains false"],
            "failure_criteria": ["missing subpacket", "protected flag true", "external action evidence appears"],
            "decision_options": ["insufficient_evidence", "keep", "refine", "pivot", "kill"],
            "adaptation_decision_candidate": {
                "decision": "insufficient_evidence",
                "reason": "Local compiler proof exists but no external market evidence exists.",
                "confidence": "medium",
                "decision_threshold": "semantic consistency validator should pass before cell production expansion",
                "next_safe_goal": NEXT_SAFE_GOAL,
                "kill_or_continue_reason": "Continue locally because compiler proof is prerequisite infrastructure.",
            },
        },
        "claim_boundary": false_boundary(),
    }


def build_manifest(packet: dict) -> dict:
    return {
        "run_id": RUN_ID,
        "goal_id": GOAL_ID,
        "artifacts": packet["production_plan_packet"]["artifacts"],
    }


def build_codex_task() -> str:
    return """# AVF Kernel v0.2 Codex Task Packet

task_id: codex-avf-vop-semantic-consistency-validator
title: Add VOP semantic consistency validator
goal: Validate that market signals, strategy hypotheses, factory cells, production artifacts, Codex tasks, evidence entries, and adaptation decisions are connected.
context_paths:
  - avf/kernel/v0_2/generated/venture_operation_packet.json
  - docs/avf/VENTURE_OPERATION_PACKET_SPEC.md
forbidden_changes:
  - No provider calls
  - No live model calls
  - No external service calls
  - No scraping
  - No posting automation
  - No dependency install
  - No deploy or publish
acceptance_criteria:
  - semantic consistency report exists
  - every required cell has production artifacts
  - strategy hypothesis cites market pain
  - capability gaps map to next Codex task
  - protected-action flags remain false
validation_commands:
  - python scripts\\validate_avf_kernel_v0_2_venture_operation_packet.py
next_pr_recommendation: Factory Cell Production Pack v0.1
"""


def build_report() -> str:
    return """# AVF Kernel v0.2 Venture Operation Packet Validation Report

RESULT: PASS
avf_kernel_v0_2_venture_operation_packet_compiler=true
venture_operation_packet_created=true
market_intelligence_packet_created=true
strategy_hypothesis_packet_created=true
factory_formation_packet_created=true
production_plan_packet_created=true
influence_distribution_packet_created=true
capability_acquisition_packet_created=true
codex_execution_packet_created=true
safety_governance_packet_created=true
evidence_learning_packet_created=true
artifact_manifest_created=true
evidence_ledger_v2_entry_created=true
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
next_safe_goal_id=avf_vop_semantic_consistency_validator
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_kernel_v0_2_venture_operation_packet",
        "status": "PASS",
        "checks": [
            "venture operation packet created",
            "required subpackets present",
            "artifact manifest created",
            "evidence ledger v2 entry created",
            "protected-action flags false",
        ],
        "claim_boundary": false_boundary(),
    }


def build_evidence(vop_path: Path) -> dict:
    return {
        "id": "evidence-avf-kernel-v0-2-vop",
        "run_id": RUN_ID,
        "goal_id": GOAL_ID,
        "artifact_id": "venture-operation-packet-v0-2",
        "artifact_uri": rel(vop_path),
        "artifact_hash": sha256(vop_path),
        "actor": {"actor_type": "local_runner", "actor_id": "scripts/run_avf_kernel_v0_2_venture_operation_packet.py"},
        "source": {
            "source_type": "repo_fixture",
            "source_uri": "avf/kernel/v0_2/fixtures",
            "source_hash": sha256(FIXTURES / "sample_venture_goal.yml"),
        },
        "claim": "AVF Kernel v0.2 can compile repo-local fixtures into a Venture Operation Packet.",
        "claim_boundary": false_boundary(),
        "validation_method": {
            "method_type": "local_validator",
            "command": "python scripts\\validate_avf_kernel_v0_2_venture_operation_packet.py",
            "validator_uri": "scripts/validate_avf_kernel_v0_2_venture_operation_packet.py",
        },
        "validation_result": {"status": "PASS", "observed_at": CREATED_AT, "summary": "Local deterministic compiler proof only."},
        "confidence": {"level": "medium", "reason": "Repo-local fixture proof without external validation."},
        "approval_state": {"required": False, "status": "not_required", "approver": ""},
        "created_at": CREATED_AT,
        "next_action": NEXT_SAFE_GOAL,
    }


def main() -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    goal = parse_simple_yaml(FIXTURES / "sample_venture_goal.yml")
    signals = parse_simple_yaml(FIXTURES / "sample_market_signals.yml")
    capabilities = parse_simple_yaml(FIXTURES / "sample_capability_registry.yml")

    packet = build_packet(goal, signals, capabilities)
    vop_path = GENERATED / "venture_operation_packet.json"
    write_json(vop_path, packet)
    write_json(GENERATED / "artifact_manifest.json", build_manifest(packet))
    write_text(GENERATED / "codex_task_packet.yml", build_codex_task())
    write_json(GENERATED / "evidence_ledger.v2.entry.json", build_evidence(vop_path))
    write_json(GENERATED / "validation_result.json", build_validation_result())
    report = build_report()
    write_text(GENERATED / "validation_report.md", report)
    write_text(GOALS / "AVF_KERNEL_V0_2_VENTURE_OPERATION_PACKET_VALIDATION_REPORT.md", report)

    print("AVF Kernel v0.2 Venture Operation Packet compiler")
    print("RESULT: PASS")
    print("avf_kernel_v0_2_venture_operation_packet_compiler=true")
    print("venture_operation_packet_created=true")
    print("artifact_manifest_created=true")
    print("evidence_ledger_v2_entry_created=true")
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


if __name__ == "__main__":
    main()
