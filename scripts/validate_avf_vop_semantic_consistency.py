from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "avf" / "kernel" / "v0_2" / "generated"
GOALS = ROOT / "docs" / "goals"

VOP = GENERATED / "venture_operation_packet.json"
EVIDENCE = GENERATED / "evidence_ledger.v2.entry.json"
SEMANTIC_REPORT = GENERATED / "semantic_consistency_report.json"
SEMANTIC_GOAL_REPORT = GOALS / "AVF_VOP_SEMANTIC_CONSISTENCY_VALIDATION_REPORT.md"
RUNNER = ROOT / "scripts" / "run_avf_vop_semantic_consistency.py"

EXPECTED_REQUIRED_CELLS = {
    "product-cell",
    "content-cell",
    "code-cell",
    "evidence-cell",
    "safety-cell",
}
NEXT_SAFE_GOAL_ID = "avf_factory_cell_production_pack_v0_1"
CURRENT_VOP_NEXT_GOAL_ID = "avf_vop_semantic_consistency_validator"

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
    "vop_semantic_consistency_validated=true",
    "market_to_strategy_consistency=true",
    "strategy_to_factory_consistency=true",
    "factory_to_artifact_consistency=true",
    "artifact_to_evidence_consistency=true",
    "capability_to_codex_consistency=true",
    "evidence_to_adaptation_consistency=true",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF VOP semantic consistency validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lower_join(value) -> str:
    if isinstance(value, str):
        return value.lower()
    if isinstance(value, list):
        return " ".join(lower_join(item) for item in value)
    if isinstance(value, dict):
        return " ".join(lower_join(item) for item in value.values())
    return ""


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_report_check(report: dict, check_name: str) -> None:
    check = report.get("checks", {}).get(check_name, {})
    if check.get("status") != "PASS":
        fail(f"semantic report check did not pass: {check_name}")


def require_market_to_strategy(packet: dict) -> None:
    market = packet["market_intelligence_packet"]
    strategy = packet["strategy_hypothesis_packet"]
    market_text = lower_join([market.get("pain_points", []), market.get("observed_signals", [])])
    strategy_text = lower_join([
        strategy.get("thesis", ""),
        strategy.get("user_pain", ""),
        strategy.get("product_angle", ""),
        strategy.get("content_angle", ""),
    ])
    required_shared_terms = {"proof", "evidence", "chat"}
    shared = {term for term in required_shared_terms if term in market_text and term in strategy_text}
    if len(shared) < 2:
        fail("market pain signals are not reflected in the strategy hypothesis")


def require_strategy_to_factory(packet: dict) -> None:
    strategy = packet["strategy_hypothesis_packet"]
    formation = packet["factory_formation_packet"]
    required_cell_ids = {cell["cell_id"] for cell in formation.get("required_cells", [])}
    missing = sorted(EXPECTED_REQUIRED_CELLS - required_cell_ids)
    if missing:
        fail("required factory cells missing:\n" + "\n".join(missing))
    for field in ["product_angle", "content_angle", "distribution_angle"]:
        if not strategy.get(field):
            fail(f"strategy hypothesis missing factory-driving field: {field}")
    if "safety-cell" not in required_cell_ids:
        fail("strategy-to-factory consistency requires a safety-cell")


def require_factory_to_artifacts(packet: dict, semantic_report: dict) -> None:
    artifacts = packet["production_plan_packet"].get("artifacts", [])
    artifacts_by_cell = {}
    for artifact in artifacts:
        artifacts_by_cell.setdefault(artifact.get("producing_cell"), []).append(artifact)

    gap_cells = {
        gap.get("cell_id")
        for gap in semantic_report.get("cell_output_gaps", [])
        if gap.get("status") == "explicit_gap"
        and gap.get("next_safe_goal") == NEXT_SAFE_GOAL_ID
    }
    for cell_id in EXPECTED_REQUIRED_CELLS:
        if cell_id in artifacts_by_cell:
            continue
        if cell_id in gap_cells:
            continue
        fail(f"required cell has neither generated artifact nor explicit next-goal gap: {cell_id}")


def require_artifact_to_evidence(packet: dict) -> None:
    for artifact in packet["production_plan_packet"].get("artifacts", []):
        if not artifact.get("artifact_id") or not artifact.get("artifact_uri"):
            fail("production artifact missing id or uri")
        if not artifact.get("validation_method"):
            fail(f"production artifact missing validation method: {artifact.get('artifact_id')}")
        require_false_flags(artifact.get("claim_boundary", {}), f"artifact {artifact.get('artifact_id')} claim_boundary")
    evidence = read_json(EVIDENCE)
    if evidence.get("artifact_hash") != sha256(VOP):
        fail("evidence ledger v2 artifact_hash does not match current Venture Operation Packet")
    if evidence.get("artifact_uri") != "avf/kernel/v0_2/generated/venture_operation_packet.json":
        fail("evidence ledger v2 artifact_uri does not point to the Venture Operation Packet")
    require_false_flags(evidence.get("claim_boundary", {}), "evidence ledger v2 claim_boundary")


def require_capability_to_codex(packet: dict, semantic_report: dict) -> None:
    gap_ids = {gap.get("gap_id") for gap in packet["capability_acquisition_packet"].get("capability_gaps", [])}
    task_ids = {task.get("task_id") for task in packet["codex_execution_packet"].get("pr_sized_tasks", [])}
    if "gap-vop-semantic-consistency" not in gap_ids:
        fail("capability gaps do not include semantic consistency validator gap")
    if "codex-avf-vop-semantic-consistency-validator" not in task_ids:
        fail("Codex execution packet does not include semantic consistency task")
    links = semantic_report.get("capability_to_codex_links", [])
    if not any(link.get("gap_id") == "gap-factory-cell-production" and link.get("next_safe_goal") == NEXT_SAFE_GOAL_ID for link in links):
        fail("factory cell production gap is not mapped to the next safe goal")


def require_evidence_to_adaptation(packet: dict, semantic_report: dict) -> None:
    decision = packet["evidence_learning_packet"].get("adaptation_decision_candidate", {})
    if decision.get("next_safe_goal") != CURRENT_VOP_NEXT_GOAL_ID:
        fail("VOP adaptation decision does not point to current semantic validator goal")
    if semantic_report.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("semantic report does not point to Factory Cell Production Pack v0.1 as the next safe goal")


def require_safety(packet: dict, semantic_report: dict) -> None:
    require_false_flags(packet.get("claim_boundary", {}), "VOP claim_boundary")
    require_false_flags(packet["safety_governance_packet"].get("protected_action_flags", {}), "safety governance flags")
    require_false_flags(semantic_report.get("claim_boundary", {}), "semantic report claim_boundary")
    for channel in packet["influence_distribution_packet"].get("channel_strategy", []):
        if channel.get("approval_required") is not True:
            fail("distribution channel must remain approval-gated")
        if channel.get("posting_performed") is not False:
            fail("distribution channel posting_performed must be false")
    for gap in packet["capability_acquisition_packet"].get("capability_gaps", []):
        if gap.get("dependency_install_allowed") is not False:
            fail("capability gap dependency_install_allowed must be false")
        if gap.get("external_fetch_performed") is not False:
            fail("capability gap external_fetch_performed must be false")


def main() -> None:
    required_files = [VOP, EVIDENCE, SEMANTIC_REPORT, SEMANTIC_GOAL_REPORT, RUNNER]
    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    packet = read_json(VOP)
    semantic_report = read_json(SEMANTIC_REPORT)
    if semantic_report.get("status") != "PASS":
        fail("semantic consistency report status must be PASS")

    for check_name in [
        "market_to_strategy_consistency",
        "strategy_to_factory_consistency",
        "factory_to_artifact_consistency",
        "artifact_to_evidence_consistency",
        "capability_to_codex_consistency",
        "evidence_to_adaptation_consistency",
    ]:
        require_report_check(semantic_report, check_name)

    require_market_to_strategy(packet)
    require_strategy_to_factory(packet)
    require_factory_to_artifacts(packet, semantic_report)
    require_artifact_to_evidence(packet)
    require_capability_to_codex(packet, semantic_report)
    require_evidence_to_adaptation(packet, semantic_report)
    require_safety(packet, semantic_report)
    require_markers(SEMANTIC_GOAL_REPORT, REPORT_MARKERS)

    print("AVF VOP semantic consistency validation")
    print("RESULT: PASS")
    print("vop_semantic_consistency_validated=true")
    print("market_to_strategy_consistency=true")
    print("strategy_to_factory_consistency=true")
    print("factory_to_artifact_consistency=true")
    print("artifact_to_evidence_consistency=true")
    print("capability_to_codex_consistency=true")
    print("evidence_to_adaptation_consistency=true")
    print("protected_action_executed=false")
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
