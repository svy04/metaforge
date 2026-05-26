from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CELLS = ROOT / "avf" / "cells"
GENERATED = ROOT / "avf" / "kernel" / "v0_2" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_factory_cell_production_pack_v0_1.py"
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

REQUIRED_FILES = [
    RUNNER,
    VOP,
    SEMANTIC_REPORT,
    PRODUCT_BRIEF,
    CONTENT_PACK,
    SAFETY_PACKET,
    CODEX_TASK,
    SOURCE_LEDGER,
    OUTPUT_MANIFEST,
    EVIDENCE_ENTRY,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "factory_cell_production_pack_v0_1=true",
    "product_cell_output_created=true",
    "content_cell_output_created=true",
    "safety_cell_output_created=true",
    "codex_cell_output_created=true",
    "evidence_cell_output_created=true",
    "primary_source_ledger_created=true",
    "source_ledger_primary_sources_verified=true",
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
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

REQUIRED_SOURCE_IDS = {
    "src-langgraph-docs",
    "src-temporal-docs",
    "src-github-actions-docs",
    "src-opentelemetry-docs",
    "src-mcp-docs",
    "src-webarena-paper",
    "src-react-paper",
    "src-ftc-endorsement-guides",
    "src-ftc-ai-claims",
}


def fail(message: str) -> None:
    print("AVF Factory Cell Production Pack v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_primary_sources() -> None:
    ledger = read_json(SOURCE_LEDGER)
    entries = ledger.get("sources", [])
    ids = {entry.get("source_id") for entry in entries}
    missing = sorted(REQUIRED_SOURCE_IDS - ids)
    if missing:
        fail("primary source ledger missing source ids:\n" + "\n".join(missing))
    if ledger.get("automation_fetch_performed") is not False:
        fail("source ledger automation_fetch_performed must be false")
    for entry in entries:
        if entry.get("source_kind") not in {"official_docs", "official_guidance", "paper"}:
            fail(f"source has non-primary source_kind: {entry.get('source_id')}")
        if not entry.get("url", "").startswith("https://"):
            fail(f"source missing https URL: {entry.get('source_id')}")
        if not entry.get("used_by_cells"):
            fail(f"source missing used_by_cells: {entry.get('source_id')}")


def require_manifest() -> None:
    manifest = read_json(OUTPUT_MANIFEST)
    if manifest.get("status") != "PASS":
        fail("cell output manifest status must be PASS")
    required_cells = {"product-cell", "content-cell", "safety-cell", "codex-cell", "evidence-cell"}
    manifest_cells = {item.get("cell_id") for item in manifest.get("cell_outputs", [])}
    missing = sorted(required_cells - manifest_cells)
    if missing:
        fail("cell output manifest missing cells:\n" + "\n".join(missing))
    for item in manifest.get("cell_outputs", []):
        artifact_path = ROOT / item["artifact_uri"]
        if not artifact_path.is_file():
            fail(f"manifest artifact missing: {item['artifact_uri']}")
        if item.get("artifact_hash") != sha256(artifact_path):
            fail(f"manifest artifact hash mismatch: {item['artifact_uri']}")
        require_false_flags(item.get("claim_boundary", {}), f"manifest item {item.get('artifact_id')}")


def require_evidence() -> None:
    evidence = read_json(EVIDENCE_ENTRY)
    if evidence.get("status") != "PASS":
        fail("cell output evidence entry status must be PASS")
    if evidence.get("next_safe_goal") != NEXT_SAFE_GOAL_ID:
        fail("cell output evidence entry next_safe_goal mismatch")
    require_false_flags(evidence.get("claim_boundary", {}), "cell output evidence entry")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    semantic = read_json(SEMANTIC_REPORT)
    if semantic.get("next_safe_goal_id") != "avf_factory_cell_production_pack_v0_1":
        fail("semantic report does not authorize this next safe goal")

    require_primary_sources()
    require_manifest()
    require_evidence()

    require_markers(PRODUCT_BRIEF, ["# Mini Product Brief", "proof-producing", "source_refs:", "not production ready"])
    require_markers(CONTENT_PACK, ["# Draft-First Content Pack", "human approval", "posting_performed=false", "FTC", "source_refs:"])
    require_markers(SAFETY_PACKET, ["# Safety Boundary Packet", "protected_action_executed=false", "release_ready=false", "production_ready=false"])
    require_markers(CODEX_TASK, ["task_id: avf-strategy-adaptation-loop-v0-1", "forbidden_changes:", "validation_commands:", "next_safe_goal_id: avf_strategy_adaptation_loop_v0_1"])
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_false_flags(validation.get("claim_boundary", {}), "validation result claim boundary")

    print("AVF Factory Cell Production Pack v0.1 validation")
    print("RESULT: PASS")
    print("factory_cell_production_pack_v0_1=true")
    print("product_cell_output_created=true")
    print("content_cell_output_created=true")
    print("safety_cell_output_created=true")
    print("codex_cell_output_created=true")
    print("evidence_cell_output_created=true")
    print("primary_source_ledger_created=true")
    print("source_ledger_primary_sources_verified=true")
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
