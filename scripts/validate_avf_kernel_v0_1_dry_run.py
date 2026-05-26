from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "avf" / "kernel"
GENERATED = KERNEL / "generated"
GOALS = ROOT / "docs" / "goals"

ARCHITECTURE_REPORT = GOALS / "AVF_CRITICAL_ARCHITECTURE_EXPANSION_MAP_VALIDATION_REPORT.md"
VALIDATION_REPORT = GOALS / "AVF_KERNEL_V0_1_DRY_RUN_VALIDATION_REPORT.md"
FACTORY_OUTPUT = GENERATED / "factory_output_packet.json"
EVIDENCE_ENTRY = GENERATED / "evidence_ledger_entry.json"

REQUIRED_FILES = [
    ARCHITECTURE_REPORT,
    KERNEL / "goal_intake.schema.yml",
    KERNEL / "factory_output_packet.schema.yml",
    KERNEL / "router_contract.schema.yml",
    KERNEL / "run_state.schema.yml",
    KERNEL / "validation_result.schema.yml",
    KERNEL / "sample_goal.yml",
    GENERATED / "run_state.json",
    FACTORY_OUTPUT,
    GENERATED / "codex_task_packet.yml",
    EVIDENCE_ENTRY,
    GENERATED / "validation_result.json",
    GENERATED / "validation_report.md",
    ROOT / "scripts" / "run_avf_kernel_v0_1_dry_run.py",
    ROOT / "scripts" / "validate_avf_kernel_v0_1_dry_run.py",
    VALIDATION_REPORT,
]

REQUIRED_TRACKS = {
    "Product Track",
    "Brand/IP Track",
    "Content System Track",
    "Safe Influence Factory Track",
    "Codex Lane",
}

REQUIRED_ROLES = {
    "Orchestrator",
    "Product Strategist",
    "Brand/IP Architect",
    "Content Systems Designer",
    "Safety Reviewer",
    "Codex Executor Planner",
}

REQUIRED_EVIDENCE_FIELDS = {
    "id",
    "run_id",
    "goal_id",
    "artifact_id",
    "artifact_uri",
    "artifact_hash",
    "actor",
    "source",
    "claim",
    "claim_boundary",
    "validation_method",
    "validation_result",
    "confidence",
    "approval_state",
    "created_at",
    "next_action",
}

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "dependency_install_performed",
    "deploy_performed",
    "publish_performed",
    "platform_posting_performed",
    "public_readiness_claimed",
    "release_readiness_claimed",
    "production_readiness_claimed",
    "external_validation_claimed",
]


def fail(message: str) -> None:
    print("AVF Kernel v0.1 dry-run validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_text(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    if "RESULT: PASS" not in read(ARCHITECTURE_REPORT):
        fail("architecture expansion validation report is not PASS")

    require_text(
        KERNEL / "goal_intake.schema.yml",
        ["goal_id", "owner_intent", "target_tracks", "success_proof", "constraints"],
    )
    require_text(
        KERNEL / "factory_output_packet.schema.yml",
        ["run_id", "goal_id", "track_classification", "agent_role_plan", "proof_artifact_plan", "safety_boundary"],
    )
    require_text(
        KERNEL / "router_contract.schema.yml",
        ["deterministic_router", "risk_classifier", "track_classifier"],
    )
    require_text(
        KERNEL / "run_state.schema.yml",
        ["created", "classified", "planned", "validated", "terminal"],
    )
    require_text(
        KERNEL / "validation_result.schema.yml",
        ["validator_id", "status", "checks", "claim_boundary"],
    )

    output = read_json(FACTORY_OUTPUT)
    if output.get("kernel_version") != "avf_kernel_v0_1":
        fail("factory output kernel_version mismatch")
    if output.get("terminal_condition") != "AVF_KERNEL_V0_1_DRY_RUN_READY":
        fail("factory output terminal_condition mismatch")
    if output.get("goal_id") != "sample-transparent-ai-creator-collective":
        fail("factory output goal_id mismatch")
    tracks = {item.get("track") for item in output.get("track_classification", [])}
    if not REQUIRED_TRACKS.issubset(tracks):
        fail("factory output missing required tracks:\n" + "\n".join(sorted(REQUIRED_TRACKS - tracks)))
    roles = {item.get("role") for item in output.get("agent_role_plan", [])}
    if not REQUIRED_ROLES.issubset(roles):
        fail("factory output missing required roles:\n" + "\n".join(sorted(REQUIRED_ROLES - roles)))
    if len(output.get("proof_artifact_plan", [])) < 5:
        fail("factory output proof_artifact_plan is too small")
    for flag in FALSE_FLAGS:
        if output.get("safety_boundary", {}).get(flag) is not False:
            fail(f"factory output safety_boundary {flag} must be false")

    codex_task = read(GENERATED / "codex_task_packet.yml")
    for marker in [
        "task_id: codex-avf-kernel-v0-2-semantic-router",
        "forbidden_changes:",
        "No provider calls",
        "No deploy or publish",
        "Acceptance criteria",
        "python scripts\\validate_avf_kernel_v0_1_dry_run.py",
    ]:
        if marker not in codex_task:
            fail(f"codex task packet missing marker: {marker}")

    evidence = read_json(EVIDENCE_ENTRY)
    if set(evidence.keys()) & REQUIRED_EVIDENCE_FIELDS != REQUIRED_EVIDENCE_FIELDS:
        fail("evidence ledger entry missing required v2 fields")
    if evidence.get("artifact_hash") != sha256(FACTORY_OUTPUT):
        fail("evidence ledger entry artifact_hash does not match factory output packet")
    boundary = evidence.get("claim_boundary", {})
    for flag in ["protected_action_executed", "provider_calls_performed", "deploy_performed", "publish_performed", "release_ready", "production_ready"]:
        if boundary.get(flag) is not False:
            fail(f"evidence claim_boundary {flag} must be false")

    validation = read_json(GENERATED / "validation_result.json")
    if validation.get("status") != "PASS":
        fail("validation_result.json status must be PASS")
    if validation.get("terminal_condition") != "AVF_KERNEL_V0_1_DRY_RUN_READY":
        fail("validation_result.json terminal_condition mismatch")

    report_text = read(VALIDATION_REPORT) + "\n" + read(GENERATED / "validation_report.md")
    for marker in [
        "RESULT: PASS",
        "AVF_KERNEL_V0_1_DRY_RUN_READY",
        "factory_output_packet_created=true",
        "codex_task_packet_created=true",
        "evidence_ledger_v2_entry_created=true",
        "protected_action_executed=false",
        "provider_calls_performed=false",
        "deploy_performed=false",
        "publish_performed=false",
        "release_ready=false",
        "production_ready=false",
        "next_safe_goal_id=avf_kernel_v0_2_semantic_router",
    ]:
        if marker not in report_text:
            fail(f"validation report missing marker: {marker}")

    print("AVF Kernel v0.1 dry-run validation")
    print("RESULT: PASS")
    print("terminal_condition=AVF_KERNEL_V0_1_DRY_RUN_READY")
    print("sample_goal_id=sample-transparent-ai-creator-collective")
    print("factory_output_packet_created=true")
    print("codex_task_packet_created=true")
    print("evidence_ledger_v2_entry_created=true")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print("next_safe_goal_id=avf_kernel_v0_2_semantic_router")


if __name__ == "__main__":
    main()
