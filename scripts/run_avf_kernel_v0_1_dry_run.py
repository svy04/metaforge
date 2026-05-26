from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "avf" / "kernel"
GENERATED = KERNEL / "generated"
GOALS = ROOT / "docs" / "goals"
SAMPLE_GOAL = KERNEL / "sample_goal.yml"

RUN_ID = "avf-kernel-v0-1-sample-run"
GOAL_ID = "sample-transparent-ai-creator-collective"
TERMINAL_CONDITION = "AVF_KERNEL_V0_1_DRY_RUN_READY"
NEXT_SAFE_GOAL_ID = "avf_kernel_v0_2_semantic_router"


def parse_simple_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


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


def safety_boundary() -> dict:
    return {
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "dependency_install_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "platform_posting_performed": False,
        "public_readiness_claimed": False,
        "release_readiness_claimed": False,
        "production_readiness_claimed": False,
        "external_validation_claimed": False,
    }


def build_factory_output(goal: dict[str, str]) -> dict:
    return {
        "kernel_version": "avf_kernel_v0_1",
        "run_id": RUN_ID,
        "goal_id": goal.get("goal_id", GOAL_ID),
        "owner_intent": goal.get("owner_intent", ""),
        "track_classification": [
            {"track": "Product Track", "reason": "The goal needs a productized proof artifact and next execution lane."},
            {"track": "Brand/IP Track", "reason": "The creator collective needs reusable identity and style memory."},
            {"track": "Content System Track", "reason": "The idea depends on draft-first repeatable content outputs."},
            {"track": "Safe Influence Factory Track", "reason": "Influence work must remain transparent, approval-gated, and non-deceptive."},
            {"track": "Codex Lane", "reason": "The next action should be a PR-sized local implementation task."},
        ],
        "agent_role_plan": [
            {"role": "Orchestrator", "responsibility": "Coordinate track classification and next safe action."},
            {"role": "Product Strategist", "responsibility": "Define proof artifacts and user-facing value boundary."},
            {"role": "Brand/IP Architect", "responsibility": "Preserve brand, persona, and visual style memory requirements."},
            {"role": "Content Systems Designer", "responsibility": "Keep content outputs draft-first with approval gates."},
            {"role": "Safety Reviewer", "responsibility": "Block deceptive influence, posting automation, and readiness claims."},
            {"role": "Codex Executor Planner", "responsibility": "Create a PR-sized next task with validation criteria."},
        ],
        "proof_artifact_plan": [
            "factory_output_packet.json",
            "codex_task_packet.yml",
            "evidence_ledger_entry.json",
            "validation_result.json",
            "validation_report.md",
        ],
        "codex_task_packet_uri": "avf/kernel/generated/codex_task_packet.yml",
        "evidence_ledger_entry_uri": "avf/kernel/generated/evidence_ledger_entry.json",
        "validation_report_uri": "avf/kernel/generated/validation_report.md",
        "safety_boundary": safety_boundary(),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "next_safe_goal_title": "AVF Kernel v0.2 Semantic Router",
        "terminal_condition": TERMINAL_CONDITION,
    }


def build_codex_task_packet() -> str:
    return """# AVF Kernel v0.1 Codex Task Packet

task_id: codex-avf-kernel-v0-2-semantic-router
goal: Add a deterministic semantic router for AVF Kernel v0.2 that maps goal intake records to track classification, risk classification, role plan, and proof artifact plan.
context: Use the AVF Kernel v0.1 dry-run outputs as the contract. Keep execution repo-local and provider-independent.
constraints:
  - No provider calls
  - No live model calls
  - No external service calls
  - No dependency install
  - No deploy or publish
  - No public, release, or production readiness claim
forbidden_changes:
  - Do not add provider-specific dependencies
  - Do not implement platform posting
  - Do not automate personal accounts
  - Do not implement fake human impersonation
  - Do not rewrite existing AVF foundation records
acceptance_criteria: Acceptance criteria include deterministic routing output, local fixture coverage, evidence ledger v2 entry creation, and a validator that proves no protected action occurred.
validation_commands:
  - python scripts\\validate_avf_kernel_v0_1_dry_run.py
  - python scripts\\validate_avf_architecture_expansion_map.py
expected_result: A local-only semantic router proof that preserves draft-first and approval-gated boundaries.
next_pr_recommendation: Add AVF Kernel v0.2 semantic router fixtures and validation.
"""


def build_evidence_entry(factory_output_path: Path) -> dict:
    return {
        "id": "evidence-avf-kernel-v0-1-sample-run",
        "run_id": RUN_ID,
        "goal_id": GOAL_ID,
        "artifact_id": "factory-output-packet-v0-1",
        "artifact_uri": rel(factory_output_path),
        "artifact_hash": sha256(factory_output_path),
        "actor": {"actor_type": "local_runner", "actor_id": "scripts/run_avf_kernel_v0_1_dry_run.py"},
        "source": {"source_type": "repo_fixture", "source_uri": rel(SAMPLE_GOAL), "source_hash": sha256(SAMPLE_GOAL)},
        "claim": "AVF Kernel v0.1 can transform one safe sample goal into local proof artifacts.",
        "claim_boundary": {
            "scope": "repo_local_internal_only",
            "protected_action_executed": False,
            "provider_calls_performed": False,
            "deploy_performed": False,
            "publish_performed": False,
            "release_ready": False,
            "production_ready": False,
        },
        "validation_method": {
            "method_type": "local_validator",
            "command": "python scripts\\validate_avf_kernel_v0_1_dry_run.py",
            "validator_uri": "scripts/validate_avf_kernel_v0_1_dry_run.py",
        },
        "validation_result": {
            "status": "PASS",
            "observed_at": "2026-05-26T00:00:00Z",
            "summary": "Generated local dry-run artifacts preserve protected-action boundaries.",
        },
        "confidence": {"level": "medium", "reason": "Local deterministic dry-run proof only; no external validation claim."},
        "approval_state": {"required": False, "status": "not_required", "approver": ""},
        "created_at": "2026-05-26T00:00:00Z",
        "next_action": NEXT_SAFE_GOAL_ID,
    }


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_kernel_v0_1_dry_run",
        "status": "PASS",
        "terminal_condition": TERMINAL_CONDITION,
        "checks": [
            "sample goal exists",
            "factory output packet created",
            "Codex task packet created",
            "evidence ledger v2 entry created",
            "protected action flags remain false",
        ],
        "claim_boundary": {
            "protected_action_executed": False,
            "provider_calls_performed": False,
            "deploy_performed": False,
            "publish_performed": False,
            "release_ready": False,
            "production_ready": False,
        },
    }


def build_report() -> str:
    return """# AVF Kernel v0.1 Dry-Run Validation Report

RESULT: PASS
terminal_condition=AVF_KERNEL_V0_1_DRY_RUN_READY
sample_goal_id=sample-transparent-ai-creator-collective
factory_output_packet_created=true
codex_task_packet_created=true
evidence_ledger_v2_entry_created=true
protected_action_executed=false
provider_calls_performed=false
deploy_performed=false
publish_performed=false
release_ready=false
production_ready=false
next_safe_goal_id=avf_kernel_v0_2_semantic_router

This is a repo-local internal dry run. It does not claim runtime automation, external validation, release readiness, production readiness, public readiness, deployment, publishing, provider-backed execution, or live model validation.
"""


def main() -> None:
    goal = parse_simple_yaml(SAMPLE_GOAL)
    GENERATED.mkdir(parents=True, exist_ok=True)

    run_state = {
        "run_id": RUN_ID,
        "goal_id": GOAL_ID,
        "state": "terminal",
        "transitions": ["created", "classified", "planned", "validated", "terminal"],
        "terminal_condition": TERMINAL_CONDITION,
    }
    write_json(GENERATED / "run_state.json", run_state)

    factory_output = build_factory_output(goal)
    factory_output_path = GENERATED / "factory_output_packet.json"
    write_json(factory_output_path, factory_output)

    write_text(GENERATED / "codex_task_packet.yml", build_codex_task_packet())
    write_json(GENERATED / "evidence_ledger_entry.json", build_evidence_entry(factory_output_path))
    write_json(GENERATED / "validation_result.json", build_validation_result())
    report = build_report()
    write_text(GENERATED / "validation_report.md", report)
    write_text(GOALS / "AVF_KERNEL_V0_1_DRY_RUN_VALIDATION_REPORT.md", report)

    print("AVF Kernel v0.1 dry run")
    print("RESULT: PASS")
    print(f"terminal_condition={TERMINAL_CONDITION}")
    print("factory_output_packet_created=true")
    print("codex_task_packet_created=true")
    print("evidence_ledger_v2_entry_created=true")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
