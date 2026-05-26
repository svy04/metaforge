from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_owner_primary_source_evidence_population_packet_v0_1.py"
POPULATION_GATE = CAPABILITIES / "capability_primary_source_evidence_population_gate.json"
OWNER_POPULATION_PACKET = CAPABILITIES / "capability_owner_primary_source_evidence_population_packet.yml"
OWNER_POPULATION_GATE = CAPABILITIES / "capability_owner_primary_source_evidence_population_packet_gate.json"
OWNER_POPULATION_PRO_PROMPT = CAPABILITIES / "capability_owner_primary_source_evidence_population_pro_prompt.md"
VALIDATION_RESULT = CAPABILITIES / "capability_owner_primary_source_evidence_population_packet_v0_1.validation_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_owner_primary_source_evidence_population_next_codex_task_packet.yml"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_OWNER_PRIMARY_SOURCE_EVIDENCE_POPULATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_owner_primary_source_evidence_population_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_population_gate_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_owner_filled_primary_source_evidence_review_v0_1"

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "automated_scraping_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_EVIDENCE_FIELDS = [
    "source_uri",
    "source_type",
    "quoted_excerpt",
    "source_snapshot_hash",
    "license_note",
    "security_note",
    "maintenance_note",
    "architecture_fit_note",
    "supply_chain_note",
    "reviewer",
    "reviewed_at",
]

SOURCE_FAMILIES = [
    "official_docs",
    "official_repository",
    "license_file",
    "security_advisory",
    "maintenance_signal",
    "architecture_spec",
    "supply_chain_standard",
    "paper",
    "patent",
    "standard",
]

REQUIRED_FILES = [
    RUNNER,
    POPULATION_GATE,
    OWNER_POPULATION_PACKET,
    OWNER_POPULATION_GATE,
    OWNER_POPULATION_PRO_PROMPT,
    VALIDATION_RESULT,
    NEXT_CODEX_TASK,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    f"goal_id: {THIS_GOAL_ID}",
    "packet_mode: owner_or_pro_primary_source_evidence_population",
    "population_source: owner_or_pro_supplied_primary_sources_only",
    "evidence_records_to_populate: 35",
    "records_completed_by_default: 0",
    "records_accepted_by_default: 0",
    "integration_allowed_from_packet: false",
    "manual_or_pro_input_required: true",
    "automated_scraping_allowed: false",
    "external_fetch_allowed_by_packet: false",
    "oss_clone_allowed_by_packet: false",
    "dependency_install_allowed_by_packet: false",
    "runtime_integration_allowed_by_packet: false",
    "release_ready: false",
    "production_ready: false",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

PROMPT_MARKERS = [
    "PRO Prompt",
    "Do not claim release readiness",
    "Do not claim production readiness",
    "Use primary/original sources only",
    "Return populated evidence records only",
    "source_snapshot_hash",
    "license_note",
    "security_note",
    "maintenance_note",
    "architecture_fit_note",
    "supply_chain_note",
]

NEXT_TASK_MARKERS = [
    "task_id: avf-capability-owner-filled-primary-source-evidence-review-v0-1",
    "No provider calls",
    "No live model calls",
    "No automated scraping",
    "No OSS clone",
    "No package install",
    "No runtime integration",
    "No deploy",
    "No publish",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_owner_primary_source_evidence_population_packet_v0_1=true",
    "owner_primary_source_evidence_population_packet_created=true",
    "owner_primary_source_evidence_population_gate_created=true",
    "pro_prompt_created=true",
    "source_families_listed=true",
    "required_evidence_fields_listed=true",
    "source_slots_to_populate=35",
    "records_completed_by_default=0",
    "records_accepted_by_default=0",
    "integration_decision=blocked",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Owner Primary-Source Evidence Population Packet v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_previous_population_gate() -> None:
    gate = read_json(POPULATION_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous population gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous population gate must point to this owner/PRO population packet goal")
    if gate.get("workspace_records_reviewed") != 35:
        fail("previous population gate must review 35 workspace records")
    if gate.get("accepted_source_records") != 0:
        fail("previous population gate must not accept source records")
    if gate.get("integration_decision") != "blocked":
        fail("previous population gate must keep integration blocked")
    require_false_flags(gate.get("claim_boundary", {}), "previous population gate")


def require_owner_population_packet() -> None:
    packet = read(OWNER_POPULATION_PACKET)
    require_markers(OWNER_POPULATION_PACKET, PACKET_MARKERS)
    for family in SOURCE_FAMILIES:
        if f"  - {family}" not in packet:
            fail(f"owner population packet missing source family {family}")
    for field in REQUIRED_EVIDENCE_FIELDS:
        if f"  - {field}" not in packet:
            fail(f"owner population packet missing required evidence field {field}")
    if packet.count("source_slot_id:") != 35:
        fail("owner population packet must include 35 source slot references")
    if packet.count("record_status: awaiting_owner_or_pro_population") != 35:
        fail("owner population packet must keep all records awaiting owner/PRO population")
    if packet.count("accepted_for_ingestion: false") != 35:
        fail("owner population packet must block ingestion for all records by default")
    if packet.count("integration_allowed_from_record: false") != 35:
        fail("owner population packet must block integration for all records by default")


def require_owner_population_gate() -> None:
    gate = read_json(OWNER_POPULATION_GATE)
    expected = {
        "gate_id": "avf-capability-owner-primary-source-evidence-population-packet-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "gate_decision": "PACKET_READY_AWAITING_OWNER_OR_PRO_POPULATION",
        "integration_decision": "blocked",
        "source_slots_to_populate": 35,
        "records_completed_by_default": 0,
        "records_accepted_by_default": 0,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"owner population gate {key} mismatch")
    if gate.get("required_evidence_fields") != REQUIRED_EVIDENCE_FIELDS:
        fail("owner population gate required evidence fields mismatch")
    if gate.get("source_families") != SOURCE_FAMILIES:
        fail("owner population gate source families mismatch")
    if gate.get("manual_or_pro_input_required") is not True:
        fail("owner population gate must require manual/PRO input")
    if gate.get("automated_research_allowed") is not False:
        fail("owner population gate must not allow automated research")
    require_false_flags(gate.get("claim_boundary", {}), "owner population gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_owner_primary_source_evidence_population_packet_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("source_slots_to_populate") != 35:
        fail("validation result source slot count mismatch")
    if result.get("records_completed_by_default") != 0:
        fail("validation result must keep completed records at zero")
    if result.get("records_accepted_by_default") != 0:
        fail("validation result must keep accepted records at zero")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_population_gate()
    require_owner_population_packet()
    require_owner_population_gate()
    require_validation_result()
    require_markers(OWNER_POPULATION_PRO_PROMPT, PROMPT_MARKERS)
    require_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Owner Primary-Source Evidence Population Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_owner_primary_source_evidence_population_packet_v0_1=true")
    print("owner_primary_source_evidence_population_packet_created=true")
    print("owner_primary_source_evidence_population_gate_created=true")
    print("pro_prompt_created=true")
    print("source_families_listed=true")
    print("required_evidence_fields_listed=true")
    print("source_slots_to_populate=35")
    print("records_completed_by_default=0")
    print("records_accepted_by_default=0")
    print("integration_decision=blocked")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("automated_scraping_performed=false")
    print("scraping_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
