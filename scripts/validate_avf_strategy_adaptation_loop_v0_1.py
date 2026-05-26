from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRATEGY = ROOT / "avf" / "strategy" / "generated"
CELLS = ROOT / "avf" / "cells"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_strategy_adaptation_loop_v0_1.py"
DECISION_PACKET = STRATEGY / "strategy_adaptation_decision_packet.json"
SOURCE_LEDGER = CELLS / "evidence" / "generated" / "primary_source_ledger.json"
STRATEGY_SOURCE_LEDGER = STRATEGY / "strategy_source_ledger.json"
CELL_MANIFEST = CELLS / "evidence" / "generated" / "cell_output_manifest.json"
CELL_EVIDENCE = CELLS / "evidence" / "generated" / "cell_output_evidence_entry.json"
VALIDATION_RESULT = STRATEGY / "strategy_adaptation_loop_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_STRATEGY_ADAPTATION_LOOP_V0_1_VALIDATION_REPORT.md"

NEXT_SAFE_GOAL_ID = "avf_capability_acquisition_loop_v0_1"
VALID_DECISIONS = {"keep", "refine", "pivot", "kill", "insufficient_evidence"}

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
    DECISION_PACKET,
    SOURCE_LEDGER,
    STRATEGY_SOURCE_LEDGER,
    CELL_MANIFEST,
    CELL_EVIDENCE,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_SOURCE_IDS = {
    "src-reflexion-paper",
    "src-self-refine-paper",
    "src-voyager-paper",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "strategy_adaptation_loop_v0_1=true",
    "decision_packet_created=true",
    "decision_is_evidence_bound=true",
    "cell_manifest_referenced=true",
    "source_ledger_updated=true",
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


def fail(message: str) -> None:
    print("AVF Strategy Adaptation Loop v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_source_ledger() -> None:
    ledger = read_json(STRATEGY_SOURCE_LEDGER)
    ids = {entry.get("source_id") for entry in ledger.get("sources", [])}
    missing = sorted(REQUIRED_SOURCE_IDS - ids)
    if missing:
        fail("source ledger missing adaptation source ids:\n" + "\n".join(missing))
    if ledger.get("automation_fetch_performed") is not False:
        fail("strategy source ledger automation_fetch_performed must be false")


def require_decision_packet() -> None:
    packet = read_json(DECISION_PACKET)
    if packet.get("status") != "PASS":
        fail("decision packet status must be PASS")
    if packet.get("decision") not in VALID_DECISIONS:
        fail("decision packet has invalid decision")
    if packet.get("decision") != "refine":
        fail("v0.1 local evidence should produce a refine decision")
    if packet.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("decision packet next safe goal mismatch")
    if packet.get("cell_output_manifest_hash") != sha256(CELL_MANIFEST):
        fail("decision packet cell_output_manifest_hash mismatch")
    if packet.get("cell_output_evidence_hash") != sha256(CELL_EVIDENCE):
        fail("decision packet cell_output_evidence_hash mismatch")
    if not packet.get("evidence_basis"):
        fail("decision packet missing evidence_basis")
    if not packet.get("decision_threshold"):
        fail("decision packet missing decision_threshold")
    if not packet.get("source_refs"):
        fail("decision packet missing source_refs")
    for required in REQUIRED_SOURCE_IDS:
        if required not in packet["source_refs"]:
            fail(f"decision packet missing source ref: {required}")
    require_false_flags(packet.get("claim_boundary", {}), "decision packet claim boundary")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("strategy adaptation validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("strategy adaptation validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "strategy adaptation validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    manifest = read_json(CELL_MANIFEST)
    if manifest.get("next_safe_goal_id") != "avf_strategy_adaptation_loop_v0_1":
        fail("cell output manifest does not authorize strategy adaptation as next safe goal")

    evidence = read_json(CELL_EVIDENCE)
    if evidence.get("next_safe_goal") != "avf_strategy_adaptation_loop_v0_1":
        fail("cell output evidence does not authorize strategy adaptation as next safe goal")

    require_source_ledger()
    require_decision_packet()
    require_validation_result()
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Strategy Adaptation Loop v0.1 validation")
    print("RESULT: PASS")
    print("strategy_adaptation_loop_v0_1=true")
    print("decision_packet_created=true")
    print("decision_is_evidence_bound=true")
    print("cell_manifest_referenced=true")
    print("source_ledger_updated=true")
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
