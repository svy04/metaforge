from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_primary_source_evidence_population_retry_v0_1.py"
REVIEW_GATE = CAPABILITIES / "capability_owner_filled_primary_source_evidence_review_gate.json"
RETRY_PACKET = CAPABILITIES / "capability_primary_source_evidence_population_retry_packet.yml"
RETRY_GATE = CAPABILITIES / "capability_primary_source_evidence_population_retry_gate.json"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_population_retry_v0_1.validation_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_population_retry_next_codex_task_packet.yml"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_POPULATION_RETRY_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_population_retry_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_owner_filled_primary_source_evidence_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_retry_review_v0_1"
RETRY_DECISION = "RETRY_PACKET_READY_AWAITING_OWNER_OR_PRO_EVIDENCE"

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

REQUIRED_FILES = [
    RUNNER,
    REVIEW_GATE,
    RETRY_PACKET,
    RETRY_GATE,
    VALIDATION_RESULT,
    NEXT_CODEX_TASK,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    "retry_attempt: 1",
    "retry_reason: previous_review_gate_blocked_empty_records",
    "retry_source_records: 35",
    "empty_records_to_retry: 35",
    "records_accepted_by_default: 0",
    "integration_allowed_from_retry: false",
    "manual_or_pro_input_required: true",
    "external_fetch_allowed_by_packet: false",
    "automated_scraping_allowed: false",
    "oss_clone_allowed_by_packet: false",
    "dependency_install_allowed_by_packet: false",
    "runtime_integration_allowed_by_packet: false",
    "release_ready: false",
    "production_ready: false",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_TASK_MARKERS = [
    "task_id: avf-capability-primary-source-evidence-retry-review-v0-1",
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
    "capability_primary_source_evidence_population_retry_v0_1=true",
    "primary_source_evidence_population_retry_packet_created=true",
    "primary_source_evidence_population_retry_gate_created=true",
    "retry_source_records=35",
    "empty_records_to_retry=35",
    "records_accepted_by_default=0",
    "integration_decision=blocked",
    f"retry_decision={RETRY_DECISION}",
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
    print("AVF Capability Primary-Source Evidence Population Retry v0.1 validation")
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


def require_previous_review_gate() -> dict:
    gate = read_json(REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous review gate must point to this retry goal")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_slots_reviewed") != 35:
        fail("previous review gate must review 35 source slots")
    if counts.get("empty_source_records") != 35:
        fail("previous review gate must expose 35 empty source records")
    if counts.get("accepted_source_records") != 0:
        fail("previous review gate must not accept source records")
    if gate.get("integration_decision") != "blocked":
        fail("previous review gate must keep integration blocked")
    require_false_flags(gate.get("claim_boundary", {}), "previous review gate")
    return gate


def require_retry_packet(previous_gate: dict) -> None:
    packet_text = read(RETRY_PACKET)
    require_markers(RETRY_PACKET, PACKET_MARKERS)
    for field in REQUIRED_EVIDENCE_FIELDS:
        if f"  - {field}" not in packet_text:
            fail(f"retry packet missing required evidence field {field}")
    if packet_text.count("source_slot_id:") != 35:
        fail("retry packet must include 35 source slot ids")
    if packet_text.count("retry_status: awaiting_owner_or_pro_population") != 35:
        fail("retry packet must keep all records awaiting owner/PRO population")
    if packet_text.count("previous_review_status: empty_record_blocked") != 35:
        fail("retry packet must preserve empty blocked status for all records")
    if packet_text.count("accepted_for_ingestion: false") != 35:
        fail("retry packet must block ingestion for all records by default")
    if packet_text.count("integration_allowed_from_record: false") != 35:
        fail("retry packet must block integration for all records by default")

    previous_slots = {review.get("source_slot_id") for review in previous_gate.get("source_record_reviews", [])}
    for slot_id in previous_slots:
        if f"source_slot_id: {slot_id}" not in packet_text:
            fail(f"retry packet missing previous blocked source slot {slot_id}")


def require_retry_gate() -> None:
    gate = read_json(RETRY_GATE)
    expected = {
        "gate_id": "avf-capability-primary-source-evidence-population-retry-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "retry_decision": RETRY_DECISION,
        "integration_decision": "blocked",
        "retry_source_records": 35,
        "empty_records_to_retry": 35,
        "records_accepted_by_default": 0,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"retry gate {key} mismatch")
    if gate.get("required_evidence_fields") != REQUIRED_EVIDENCE_FIELDS:
        fail("retry gate required evidence fields mismatch")
    if gate.get("manual_or_pro_input_required") is not True:
        fail("retry gate must require owner/PRO input")
    require_false_flags(gate.get("claim_boundary", {}), "retry gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_primary_source_evidence_population_retry_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("retry_source_records") != 35:
        fail("validation result retry source record count mismatch")
    if result.get("records_accepted_by_default") != 0:
        fail("validation result must keep accepted records at zero")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    previous_gate = require_previous_review_gate()
    require_retry_packet(previous_gate)
    require_retry_gate()
    require_validation_result()
    require_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Primary-Source Evidence Population Retry v0.1 validation")
    print("RESULT: PASS")
    print("capability_primary_source_evidence_population_retry_v0_1=true")
    print("primary_source_evidence_population_retry_packet_created=true")
    print("primary_source_evidence_population_retry_gate_created=true")
    print("retry_source_records=35")
    print("empty_records_to_retry=35")
    print("records_accepted_by_default=0")
    print("integration_decision=blocked")
    print(f"retry_decision={RETRY_DECISION}")
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
