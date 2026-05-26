from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V02 = ROOT / "avf" / "kernel" / "v0_2"
FIXTURES = V02 / "fixtures"
GENERATED = V02 / "generated"
GOALS = ROOT / "docs" / "goals"

DESIGN_REPORT = GOALS / "AVF_MARKET_TO_FACTORY_DESIGN_VALIDATION_REPORT.md"
VALIDATION_REPORT = GOALS / "AVF_KERNEL_V0_2_VENTURE_OPERATION_PACKET_VALIDATION_REPORT.md"
VOP = GENERATED / "venture_operation_packet.json"
EVIDENCE = GENERATED / "evidence_ledger.v2.entry.json"

REQUIRED_FILES = [
    V02 / "venture_operation_packet.schema.yml",
    V02 / "market_signal.schema.yml",
    V02 / "strategy_hypothesis.schema.yml",
    V02 / "factory_cell_activation.schema.yml",
    V02 / "production_artifact.schema.yml",
    V02 / "capability_gap.schema.yml",
    V02 / "adaptation_decision.schema.yml",
    FIXTURES / "sample_venture_goal.yml",
    FIXTURES / "sample_market_signals.yml",
    FIXTURES / "sample_capability_registry.yml",
    VOP,
    GENERATED / "artifact_manifest.json",
    GENERATED / "codex_task_packet.yml",
    EVIDENCE,
    GENERATED / "validation_result.json",
    GENERATED / "validation_report.md",
    ROOT / "scripts" / "run_avf_kernel_v0_2_venture_operation_packet.py",
    ROOT / "scripts" / "validate_avf_kernel_v0_2_venture_operation_packet.py",
    VALIDATION_REPORT,
]

TOP_LEVEL_FIELDS = [
    "packet_id",
    "schema_version",
    "kernel_version",
    "compiler_mode",
    "created_at",
    "run_id",
    "goal_id",
    "raw_goal",
    "goal_essence",
    "goal_context",
    "market_intelligence_packet",
    "strategy_hypothesis_packet",
    "factory_formation_packet",
    "production_plan_packet",
    "influence_distribution_packet",
    "capability_acquisition_packet",
    "codex_execution_packet",
    "safety_governance_packet",
    "evidence_learning_packet",
    "claim_boundary",
]

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "avf_kernel_v0_2_venture_operation_packet_compiler=true",
    "venture_operation_packet_created=true",
    "market_intelligence_packet_created=true",
    "strategy_hypothesis_packet_created=true",
    "factory_formation_packet_created=true",
    "production_plan_packet_created=true",
    "influence_distribution_packet_created=true",
    "capability_acquisition_packet_created=true",
    "codex_execution_packet_created=true",
    "safety_governance_packet_created=true",
    "evidence_learning_packet_created=true",
    "artifact_manifest_created=true",
    "evidence_ledger_v2_entry_created=true",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
]


def fail(message: str) -> None:
    print("AVF Kernel v0.2 Venture Operation Packet validation")
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


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    if "RESULT: PASS" not in read(DESIGN_REPORT):
        fail("Market-to-Factory design validation report is not PASS")

    require_text(V02 / "venture_operation_packet.schema.yml", TOP_LEVEL_FIELDS)
    require_text(V02 / "market_signal.schema.yml", ["signal_id", "source_type", "collection_mode", "freshness", "rights_boundary", "confidence"])
    require_text(V02 / "strategy_hypothesis.schema.yml", ["hypothesis_id", "success_criteria", "failure_criteria", "decision_threshold"])
    require_text(V02 / "factory_cell_activation.schema.yml", ["cell_id", "cell_type", "activation_reason", "expected_outputs", "owner_gate_required"])
    require_text(V02 / "production_artifact.schema.yml", ["artifact_id", "artifact_type", "artifact_uri", "claim_boundary", "validation_method"])
    require_text(V02 / "capability_gap.schema.yml", ["license_review_required", "security_review_required", "dependency_install_allowed", "external_fetch_performed"])
    require_text(V02 / "adaptation_decision.schema.yml", ["hypothesis_id", "decision", "evidence_summary", "next_safe_goal"])

    packet = read_json(VOP)
    for field in TOP_LEVEL_FIELDS:
        if field not in packet:
            fail(f"venture operation packet missing field: {field}")
    if packet.get("kernel_version") != "avf_kernel_v0_2":
        fail("kernel_version mismatch")
    if packet.get("compiler_mode") != "deterministic_repo_local":
        fail("compiler_mode mismatch")
    if packet.get("goal_id") != "sample-avf-market-to-factory-infra-product":
        fail("goal_id mismatch")

    market = packet["market_intelligence_packet"]
    if len(market.get("signal_sources", [])) < 3:
        fail("market intelligence packet must include at least three signal sources")
    for source in market["signal_sources"]:
        if source.get("collection_mode") not in {"manual_fixture", "repo_local"}:
            fail("market source collection_mode must be manual_fixture or repo_local")
        if source.get("source_type") not in {"owner_provided", "repo_local"}:
            fail("market source source_type must be owner_provided or repo_local")

    strategy = packet["strategy_hypothesis_packet"]
    for field in ["success_criteria", "failure_criteria", "decision_threshold", "counterarguments"]:
        if not strategy.get(field):
            fail(f"strategy hypothesis missing {field}")

    formation = packet["factory_formation_packet"]
    if not formation.get("required_cells") or not formation.get("skipped_cells"):
        fail("factory formation must include required and skipped cells")
    for cell in formation["required_cells"]:
        for field in ["cell_id", "cell_type", "activation_reason", "expected_outputs", "owner_gate_required"]:
            if field not in cell:
                fail(f"required cell missing {field}")

    production = packet["production_plan_packet"]
    artifacts = production.get("artifacts", [])
    if len(artifacts) < 5:
        fail("production plan must include at least five artifacts")
    for artifact in artifacts:
        for field in ["artifact_id", "artifact_type", "artifact_uri", "producing_cell", "status", "claim_boundary", "validation_method", "owner_approval_required"]:
            if field not in artifact:
                fail(f"production artifact missing {field}")

    distribution = packet["influence_distribution_packet"]
    for channel in distribution.get("channel_strategy", []):
        if channel.get("posting_performed") is not False:
            fail("distribution channel posting_performed must be false")
        if channel.get("approval_required") is not True:
            fail("distribution channel approval_required must be true")

    acquisition = packet["capability_acquisition_packet"]
    for gap in acquisition.get("capability_gaps", []):
        if gap.get("integration_status") != "proposed_only":
            fail("capability gap integration_status must be proposed_only")
        if gap.get("dependency_install_allowed") is not False:
            fail("capability gap dependency_install_allowed must be false")
        if gap.get("external_fetch_performed") is not False:
            fail("capability gap external_fetch_performed must be false")

    codex = packet["codex_execution_packet"]
    if not codex.get("pr_sized_tasks"):
        fail("codex execution packet missing pr_sized_tasks")
    for task in codex["pr_sized_tasks"]:
        for field in ["task_id", "title", "context_paths", "scope", "forbidden_changes", "acceptance_criteria", "validation_commands", "next_pr_recommendation"]:
            if field not in task:
                fail(f"codex task missing {field}")

    governance = packet["safety_governance_packet"]
    require_false_flags(governance.get("protected_action_flags", {}), "safety governance protected_action_flags")
    if governance.get("risk_tier") not in {"low", "medium"}:
        fail("risk_tier must remain low or medium for local dry run")

    learning = packet["evidence_learning_packet"]
    decision = learning.get("adaptation_decision_candidate", {})
    if decision.get("decision") not in {"insufficient_evidence", "refine", "keep", "pivot", "kill"}:
        fail("adaptation decision candidate has invalid decision")
    if not decision.get("next_safe_goal"):
        fail("adaptation decision candidate missing next_safe_goal")

    require_false_flags(packet["claim_boundary"], "claim boundary")

    manifest = read_json(GENERATED / "artifact_manifest.json")
    if len(manifest.get("artifacts", [])) < 5:
        fail("artifact manifest must include at least five artifacts")

    evidence = read_json(EVIDENCE)
    if evidence.get("artifact_hash") != sha256(VOP):
        fail("evidence artifact_hash does not match Venture Operation Packet")
    require_false_flags(evidence.get("claim_boundary", {}), "evidence claim boundary")

    validation = read_json(GENERATED / "validation_result.json")
    if validation.get("status") != "PASS":
        fail("validation_result status must be PASS")

    report_text = read(GENERATED / "validation_report.md") + "\n" + read(VALIDATION_REPORT)
    for marker in REPORT_MARKERS:
        if marker not in report_text:
            fail(f"validation report missing marker: {marker}")

    print("AVF Kernel v0.2 Venture Operation Packet validation")
    print("RESULT: PASS")
    print("avf_kernel_v0_2_venture_operation_packet_compiler=true")
    print("venture_operation_packet_created=true")
    print("market_intelligence_packet_created=true")
    print("strategy_hypothesis_packet_created=true")
    print("factory_formation_packet_created=true")
    print("production_plan_packet_created=true")
    print("influence_distribution_packet_created=true")
    print("capability_acquisition_packet_created=true")
    print("codex_execution_packet_created=true")
    print("safety_governance_packet_created=true")
    print("evidence_learning_packet_created=true")
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
