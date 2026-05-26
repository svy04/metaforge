from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_owner_supplied_source_evidence_packet_v0_1.py"
MANUAL_REVIEW_PACKET = CAPABILITIES / "capability_manual_source_review_packet.json"
MANUAL_REVIEW_GATE = CAPABILITIES / "capability_manual_source_review_preflight_gate.json"
OWNER_SUPPLIED_EVIDENCE_PACKET = CAPABILITIES / "capability_owner_supplied_source_evidence_packet.json"
OWNER_SUPPLIED_EVIDENCE_GATE = CAPABILITIES / "capability_owner_supplied_source_evidence_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_owner_supplied_source_evidence_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_owner_supplied_source_evidence_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_OWNER_SUPPLIED_SOURCE_EVIDENCE_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_owner_supplied_source_evidence_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_source_evidence_evaluation_packet_v0_1"

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
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

REQUIRED_FILES = [
    RUNNER,
    MANUAL_REVIEW_PACKET,
    MANUAL_REVIEW_GATE,
    OWNER_SUPPLIED_EVIDENCE_PACKET,
    OWNER_SUPPLIED_EVIDENCE_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_EVIDENCE_FIELDS = {
    "evidence_record_id",
    "source_slot_id",
    "candidate_id",
    "slot_type",
    "target_uri",
    "owner_supplied_evidence_status",
    "owner_supplied_evidence_uri",
    "owner_supplied_excerpt",
    "owner_supplied_notes",
    "source_snapshot_hash",
    "snapshot_hash_algorithm",
    "reviewer",
    "reviewed_at",
    "evidence_trusted",
    "evidence_verified",
    "claim_boundary",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_owner_supplied_source_evidence_packet_v0_1=true",
    "owner_supplied_source_evidence_packet_created=true",
    "owner_supplied_source_evidence_gate_created=true",
    "evidence_input_fields_created=true",
    "no_evidence_trusted_or_verified_by_default=true",
    "integration_remains_blocked=true",
    "protected_action_executed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
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
    print("AVF Capability Owner-Supplied Source Evidence Packet v0.1 validation")
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


def require_inputs() -> dict:
    manual = read_json(MANUAL_REVIEW_PACKET)
    manual_gate = read_json(MANUAL_REVIEW_GATE)
    if manual.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("manual source review packet must point to owner-supplied evidence as next safe goal")
    if manual_gate.get("gate_decision") != "BLOCKED_PENDING_OWNER_SUPPLIED_SOURCE_EVIDENCE":
        fail("manual source review gate must remain blocked before owner-supplied evidence packet")
    if manual_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("manual source review gate must point to owner-supplied evidence as next safe goal")
    return manual


def require_evidence_record(record: dict) -> None:
    missing = sorted(REQUIRED_EVIDENCE_FIELDS - set(record))
    if missing:
        fail(f"{record.get('evidence_record_id', '<unknown>')} missing evidence fields:\n" + "\n".join(missing))
    if record.get("owner_supplied_evidence_status") != "awaiting_owner_input":
        fail(f"{record.get('evidence_record_id')} must await owner input")
    for field in [
        "owner_supplied_evidence_uri",
        "owner_supplied_excerpt",
        "owner_supplied_notes",
        "source_snapshot_hash",
        "reviewer",
        "reviewed_at",
    ]:
        if record.get(field) is not None:
            fail(f"{record.get('evidence_record_id')} {field} must remain null")
    if record.get("snapshot_hash_algorithm") != "sha256_required_before_trust":
        fail(f"{record.get('evidence_record_id')} snapshot hash algorithm marker mismatch")
    if record.get("evidence_trusted") is not False:
        fail(f"{record.get('evidence_record_id')} evidence_trusted must be false")
    if record.get("evidence_verified") is not False:
        fail(f"{record.get('evidence_record_id')} evidence_verified must be false")
    if not str(record.get("target_uri", "")).startswith("https://"):
        fail(f"{record.get('evidence_record_id')} target_uri must be https")
    require_false_flags(record.get("claim_boundary", {}), f"{record.get('evidence_record_id')} claim boundary")


def require_owner_supplied_evidence_packet(manual: dict) -> None:
    packet = read_json(OWNER_SUPPLIED_EVIDENCE_PACKET)
    if packet.get("status") != "PASS":
        fail("owner-supplied evidence packet status must be PASS")
    if packet.get("goal_id") != THIS_GOAL_ID:
        fail("owner-supplied evidence packet goal_id mismatch")
    if packet.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("owner-supplied evidence packet next safe goal mismatch")
    if packet.get("evidence_mode") != "owner_supplied_primary_source_snapshot_placeholders":
        fail("owner-supplied evidence mode mismatch")
    require_false_flags(packet.get("claim_boundary", {}), "owner-supplied evidence packet claim boundary")

    expected_candidate_ids = {record["candidate_id"] for record in manual.get("candidate_source_review_records", [])}
    candidate_records = packet.get("candidate_owner_supplied_evidence_records", [])
    if {record.get("candidate_id") for record in candidate_records} != expected_candidate_ids:
        fail("owner-supplied evidence candidates must match manual source review packet")

    expected_evidence_count = sum(
        len(record.get("source_evidence_capture_records", []))
        for record in manual.get("candidate_source_review_records", [])
    )
    observed_evidence_count = sum(
        len(record.get("owner_supplied_evidence_records", []))
        for record in candidate_records
    )
    if observed_evidence_count != expected_evidence_count:
        fail("owner-supplied evidence record count must match manual source review capture slots")

    for candidate_record in candidate_records:
        if candidate_record.get("candidate_evidence_status") != "awaiting_owner_input":
            fail(f"{candidate_record.get('candidate_id')} candidate evidence status must await owner input")
        if candidate_record.get("integration_decision") != "blocked":
            fail(f"{candidate_record.get('candidate_id')} integration decision must remain blocked")
        if candidate_record.get("source_evidence_verified") is not False:
            fail(f"{candidate_record.get('candidate_id')} source evidence verified must be false")
        require_false_flags(candidate_record.get("claim_boundary", {}), f"{candidate_record.get('candidate_id')} claim boundary")
        for evidence_record in candidate_record.get("owner_supplied_evidence_records", []):
            require_evidence_record(evidence_record)

    contract = packet.get("evidence_input_contract", {})
    if contract.get("automated_fetch_allowed") is not False:
        fail("automated_fetch_allowed must be false")
    if contract.get("automated_scraping_allowed") is not False:
        fail("automated_scraping_allowed must be false")
    if contract.get("evidence_trusted_by_default") is not False:
        fail("evidence_trusted_by_default must be false")
    if contract.get("evidence_verified_by_default") is not False:
        fail("evidence_verified_by_default must be false")


def require_owner_supplied_evidence_gate() -> None:
    gate = read_json(OWNER_SUPPLIED_EVIDENCE_GATE)
    if gate.get("status") != "PASS":
        fail("owner-supplied evidence gate status must be PASS")
    if gate.get("gate_decision") != "BLOCKED_PENDING_SOURCE_EVIDENCE_EVALUATION":
        fail("owner-supplied evidence gate must remain blocked")
    if gate.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("owner-supplied evidence gate next safe goal mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "owner-supplied evidence gate")
    required_blockers = {
        "owner_supplied_evidence_uri_missing",
        "owner_supplied_excerpt_or_notes_missing",
        "source_snapshot_hash_missing",
        "reviewer_missing",
        "evidence_not_evaluated",
        "integration_not_approved",
    }
    blockers = set(gate.get("blocking_requirements", []))
    missing = sorted(required_blockers - blockers)
    if missing:
        fail("owner-supplied evidence gate missing blockers:\n" + "\n".join(missing))


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("owner-supplied evidence validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("owner-supplied evidence validation next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "owner-supplied evidence validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    manual = require_inputs()
    require_owner_supplied_evidence_packet(manual)
    require_owner_supplied_evidence_gate()
    require_validation_result()
    require_markers(NEXT_CODEX_TASK, ["task_id: avf-capability-source-evidence-evaluation-packet-v0-1", "forbidden_changes:", "validation_commands:", f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}"])
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Owner-Supplied Source Evidence Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_owner_supplied_source_evidence_packet_v0_1=true")
    print("owner_supplied_source_evidence_packet_created=true")
    print("owner_supplied_source_evidence_gate_created=true")
    print("evidence_input_fields_created=true")
    print("no_evidence_trusted_or_verified_by_default=true")
    print("integration_remains_blocked=true")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
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
