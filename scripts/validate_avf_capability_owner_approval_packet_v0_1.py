from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_owner_approval_packet_v0_1.py"
SOURCE_MATRIX = CAPABILITIES / "capability_source_verification_matrix.json"
SOURCE_PREFLIGHT_GATE = CAPABILITIES / "capability_source_verification_preflight_gate.json"
REVIEW_DOSSIER = CAPABILITIES / "capability_review_dossier.json"
OWNER_APPROVAL_PACKET = CAPABILITIES / "capability_owner_approval_packet.json"
OWNER_APPROVAL_GATE = CAPABILITIES / "capability_owner_approval_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_owner_approval_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_owner_approval_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_OWNER_APPROVAL_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_owner_approval_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_manual_source_review_packet_v0_1"

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
    SOURCE_MATRIX,
    SOURCE_PREFLIGHT_GATE,
    REVIEW_DOSSIER,
    OWNER_APPROVAL_PACKET,
    OWNER_APPROVAL_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_REVIEW_FLAGS = [
    "source_verification_completed",
    "license_review_completed",
    "security_review_completed",
    "maintenance_review_completed",
    "architecture_fit_review_completed",
    "sandbox_plan_approved",
    "rollback_plan_approved",
]

REQUIRED_PERMISSION_FLAGS = [
    "external_fetch_allowed",
    "oss_clone_allowed",
    "dependency_install_allowed",
    "package_install_allowed",
    "runtime_integration_allowed",
    "provider_activation_allowed",
    "deployment_allowed",
    "publication_allowed",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_owner_approval_packet_v0_1=true",
    "owner_approval_packet_created=true",
    "owner_approval_gate_created=true",
    "all_candidates_blocked_by_default=true",
    "approval_fields_explicit_and_unset=true",
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
    print("AVF Capability Owner Approval Packet v0.1 validation")
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


def require_source_inputs() -> tuple[dict, dict]:
    matrix = read_json(SOURCE_MATRIX)
    gate = read_json(SOURCE_PREFLIGHT_GATE)
    if matrix.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("source verification matrix must point to owner approval as next safe goal")
    if gate.get("gate_decision") != "BLOCKED_PENDING_SOURCE_VERIFICATION_AND_OWNER_APPROVAL":
        fail("source preflight gate must remain blocked before owner approval packet")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("source preflight gate must point to owner approval as next safe goal")
    return matrix, gate


def require_approval_record(record: dict) -> None:
    candidate_id = record.get("candidate_id", "<unknown>")
    if record.get("block_status") != "blocked_pending_source_verification_and_owner_approval":
        fail(f"{candidate_id} must remain blocked")
    if record.get("integration_decision") != "not_approved":
        fail(f"{candidate_id} integration decision must remain not_approved")
    if record.get("owner_approval_status") != "unset":
        fail(f"{candidate_id} owner approval status must be unset")
    for field in ["owner_approver", "owner_approved_at", "approval_signature", "approval_scope", "approval_rationale"]:
        if record.get(field) is not None:
            fail(f"{candidate_id} {field} must remain null")
    for flag in REQUIRED_REVIEW_FLAGS:
        if record.get(flag) is not False:
            fail(f"{candidate_id} {flag} must be false")
    for flag in REQUIRED_PERMISSION_FLAGS:
        if record.get(flag) is not False:
            fail(f"{candidate_id} {flag} must be false")
    if record.get("source_slot_count", 0) < 7:
        fail(f"{candidate_id} must preserve source slot count")
    if "approve_for_manual_review_only" not in record.get("allowed_owner_decisions", []):
        fail(f"{candidate_id} missing manual-review-only owner decision option")
    require_false_flags(record.get("claim_boundary", {}), f"{candidate_id} claim boundary")


def require_owner_approval_packet(matrix: dict) -> None:
    packet = read_json(OWNER_APPROVAL_PACKET)
    if packet.get("status") != "PASS":
        fail("owner approval packet status must be PASS")
    if packet.get("goal_id") != THIS_GOAL_ID:
        fail("owner approval packet goal_id mismatch")
    if packet.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("owner approval packet next safe goal mismatch")
    if packet.get("approval_mode") != "explicit_owner_approval_required":
        fail("owner approval packet approval mode mismatch")
    if packet.get("default_decision") != "blocked":
        fail("owner approval packet default decision must be blocked")
    require_false_flags(packet.get("claim_boundary", {}), "owner approval packet claim boundary")

    expected_ids = {row["candidate_id"] for row in matrix.get("candidate_source_rows", [])}
    records = packet.get("candidate_approval_records", [])
    if len(records) != len(expected_ids):
        fail("owner approval packet must include exactly the source matrix candidates")
    record_ids = {record.get("candidate_id") for record in records}
    missing = sorted(expected_ids - record_ids)
    if missing:
        fail("owner approval packet missing candidates:\n" + "\n".join(missing))
    for record in records:
        require_approval_record(record)

    required_fields = {
        "candidate_id",
        "owner_approval_status",
        "owner_approver",
        "owner_approved_at",
        "approval_signature",
        "approval_scope",
        "approval_rationale",
        "source_verification_completed",
        "license_review_completed",
        "security_review_completed",
        "maintenance_review_completed",
        "architecture_fit_review_completed",
        "sandbox_plan_approved",
        "rollback_plan_approved",
    }
    missing_fields = sorted(required_fields - set(packet.get("required_owner_decision_fields", [])))
    if missing_fields:
        fail("owner approval packet missing required owner decision fields:\n" + "\n".join(missing_fields))


def require_owner_approval_gate() -> None:
    gate = read_json(OWNER_APPROVAL_GATE)
    if gate.get("status") != "PASS":
        fail("owner approval gate status must be PASS")
    if gate.get("gate_decision") != "BLOCKED_PENDING_EXPLICIT_OWNER_APPROVAL":
        fail("owner approval gate must remain blocked")
    if gate.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("owner approval gate next safe goal mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "owner approval gate")
    required_blockers = {
        "source_verification_not_completed",
        "license_review_not_completed",
        "security_review_not_completed",
        "maintenance_review_not_completed",
        "architecture_fit_review_not_completed",
        "sandbox_plan_not_approved",
        "rollback_plan_not_approved",
        "owner_approval_unset",
    }
    blockers = set(gate.get("blocking_requirements", []))
    missing = sorted(required_blockers - blockers)
    if missing:
        fail("owner approval gate missing blockers:\n" + "\n".join(missing))


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("owner approval validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("owner approval validation next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "owner approval validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    matrix, _ = require_source_inputs()
    require_owner_approval_packet(matrix)
    require_owner_approval_gate()
    require_validation_result()
    require_markers(NEXT_CODEX_TASK, ["task_id: avf-capability-manual-source-review-packet-v0-1", "forbidden_changes:", "validation_commands:", f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}"])
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Owner Approval Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_owner_approval_packet_v0_1=true")
    print("owner_approval_packet_created=true")
    print("owner_approval_gate_created=true")
    print("all_candidates_blocked_by_default=true")
    print("approval_fields_explicit_and_unset=true")
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
