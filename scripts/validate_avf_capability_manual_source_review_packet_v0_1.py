from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_manual_source_review_packet_v0_1.py"
OWNER_APPROVAL_PACKET = CAPABILITIES / "capability_owner_approval_packet.json"
OWNER_APPROVAL_GATE = CAPABILITIES / "capability_owner_approval_preflight_gate.json"
SOURCE_MATRIX = CAPABILITIES / "capability_source_verification_matrix.json"
MANUAL_REVIEW_PACKET = CAPABILITIES / "capability_manual_source_review_packet.json"
MANUAL_REVIEW_GATE = CAPABILITIES / "capability_manual_source_review_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_manual_source_review_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_manual_source_review_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_MANUAL_SOURCE_REVIEW_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_manual_source_review_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_owner_supplied_source_evidence_packet_v0_1"

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
    OWNER_APPROVAL_PACKET,
    OWNER_APPROVAL_GATE,
    SOURCE_MATRIX,
    MANUAL_REVIEW_PACKET,
    MANUAL_REVIEW_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_CAPTURE_FIELDS = {
    "source_slot_id",
    "candidate_id",
    "slot_type",
    "target_uri",
    "evidence_status",
    "verification_status",
    "manual_review_required",
    "reviewer",
    "reviewed_at",
    "owner_supplied_evidence_uri",
    "source_snapshot_hash",
    "license_finding",
    "security_finding",
    "maintenance_finding",
    "architecture_fit_finding",
    "notes",
    "external_fetch_performed",
    "source_marked_verified",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_manual_source_review_packet_v0_1=true",
    "manual_source_review_packet_created=true",
    "manual_review_gate_created=true",
    "source_evidence_capture_fields_created=true",
    "no_source_marked_verified_by_default=true",
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
    print("AVF Capability Manual Source Review Packet v0.1 validation")
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


def require_inputs() -> tuple[dict, dict]:
    approval = read_json(OWNER_APPROVAL_PACKET)
    approval_gate = read_json(OWNER_APPROVAL_GATE)
    if approval.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("owner approval packet must point to manual source review as next safe goal")
    if approval_gate.get("gate_decision") != "BLOCKED_PENDING_EXPLICIT_OWNER_APPROVAL":
        fail("owner approval gate must remain blocked before manual source review packet")
    if approval_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("owner approval gate must point to manual source review as next safe goal")
    matrix = read_json(SOURCE_MATRIX)
    return approval, matrix


def require_capture_record(record: dict) -> None:
    missing = sorted(REQUIRED_CAPTURE_FIELDS - set(record))
    if missing:
        fail(f"{record.get('source_slot_id', '<unknown>')} missing capture fields:\n" + "\n".join(missing))
    if record.get("evidence_status") != "not_collected":
        fail(f"{record.get('source_slot_id')} evidence_status must be not_collected")
    if record.get("verification_status") != "not_verified":
        fail(f"{record.get('source_slot_id')} verification_status must be not_verified")
    if record.get("manual_review_required") is not True:
        fail(f"{record.get('source_slot_id')} manual_review_required must be true")
    for field in [
        "reviewer",
        "reviewed_at",
        "owner_supplied_evidence_uri",
        "source_snapshot_hash",
        "license_finding",
        "security_finding",
        "maintenance_finding",
        "architecture_fit_finding",
        "notes",
    ]:
        if record.get(field) is not None:
            fail(f"{record.get('source_slot_id')} {field} must remain null")
    if record.get("external_fetch_performed") is not False:
        fail(f"{record.get('source_slot_id')} external_fetch_performed must be false")
    if record.get("source_marked_verified") is not False:
        fail(f"{record.get('source_slot_id')} source_marked_verified must be false")
    if not str(record.get("target_uri", "")).startswith("https://"):
        fail(f"{record.get('source_slot_id')} target_uri must be https")


def require_manual_review_packet(approval: dict, matrix: dict) -> None:
    packet = read_json(MANUAL_REVIEW_PACKET)
    if packet.get("status") != "PASS":
        fail("manual source review packet status must be PASS")
    if packet.get("goal_id") != THIS_GOAL_ID:
        fail("manual source review packet goal_id mismatch")
    if packet.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("manual source review packet next safe goal mismatch")
    if packet.get("review_mode") != "manual_owner_supplied_evidence_only":
        fail("manual source review packet review mode mismatch")
    require_false_flags(packet.get("claim_boundary", {}), "manual source review packet claim boundary")

    expected_candidate_ids = {record["candidate_id"] for record in approval.get("candidate_approval_records", [])}
    candidate_records = packet.get("candidate_source_review_records", [])
    if len(candidate_records) != len(expected_candidate_ids):
        fail("manual review packet must include exactly the owner approval candidates")
    if {record.get("candidate_id") for record in candidate_records} != expected_candidate_ids:
        fail("manual review packet candidate IDs must match owner approval packet")

    expected_slot_count = sum(len(row.get("source_slots", [])) for row in matrix.get("candidate_source_rows", []))
    observed_slot_count = sum(len(record.get("source_evidence_capture_records", [])) for record in candidate_records)
    if observed_slot_count != expected_slot_count:
        fail("manual review packet source slot count must match source matrix")
    for candidate_record in candidate_records:
        if candidate_record.get("candidate_review_status") != "not_reviewed":
            fail(f"{candidate_record.get('candidate_id')} must remain not_reviewed")
        if candidate_record.get("integration_decision") != "blocked":
            fail(f"{candidate_record.get('candidate_id')} integration decision must remain blocked")
        if candidate_record.get("owner_approval_status") != "unset":
            fail(f"{candidate_record.get('candidate_id')} owner approval status must remain unset")
        require_false_flags(candidate_record.get("claim_boundary", {}), f"{candidate_record.get('candidate_id')} claim boundary")
        for capture_record in candidate_record.get("source_evidence_capture_records", []):
            require_capture_record(capture_record)


def require_manual_review_gate() -> None:
    gate = read_json(MANUAL_REVIEW_GATE)
    if gate.get("status") != "PASS":
        fail("manual source review gate status must be PASS")
    if gate.get("gate_decision") != "BLOCKED_PENDING_OWNER_SUPPLIED_SOURCE_EVIDENCE":
        fail("manual source review gate must remain blocked")
    if gate.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("manual source review gate next safe goal mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "manual source review gate")
    required_blockers = {
        "owner_supplied_evidence_missing",
        "source_snapshot_hash_missing",
        "manual_reviewer_missing",
        "license_finding_missing",
        "security_finding_missing",
        "maintenance_finding_missing",
        "architecture_fit_finding_missing",
        "integration_not_approved",
    }
    blockers = set(gate.get("blocking_requirements", []))
    missing = sorted(required_blockers - blockers)
    if missing:
        fail("manual source review gate missing blockers:\n" + "\n".join(missing))


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("manual source review validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("manual source review validation next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "manual source review validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    approval, matrix = require_inputs()
    require_manual_review_packet(approval, matrix)
    require_manual_review_gate()
    require_validation_result()
    require_markers(NEXT_CODEX_TASK, ["task_id: avf-capability-owner-supplied-source-evidence-packet-v0-1", "forbidden_changes:", "validation_commands:", f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}"])
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Manual Source Review Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_manual_source_review_packet_v0_1=true")
    print("manual_source_review_packet_created=true")
    print("manual_review_gate_created=true")
    print("source_evidence_capture_fields_created=true")
    print("no_source_marked_verified_by_default=true")
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
