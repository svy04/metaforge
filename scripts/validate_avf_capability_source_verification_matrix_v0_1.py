from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_source_verification_matrix_v0_1.py"
REVIEW_DOSSIER = CAPABILITIES / "capability_review_dossier.json"
INTEGRATION_GATE = CAPABILITIES / "capability_integration_preflight_gate.json"
SOURCE_MATRIX = CAPABILITIES / "capability_source_verification_matrix.json"
SOURCE_PREFLIGHT_GATE = CAPABILITIES / "capability_source_verification_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_source_verification_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_source_verification_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_SOURCE_VERIFICATION_MATRIX_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_source_verification_matrix_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_owner_approval_packet_v0_1"

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
    REVIEW_DOSSIER,
    INTEGRATION_GATE,
    SOURCE_MATRIX,
    SOURCE_PREFLIGHT_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_SLOT_TYPES = {
    "official_docs",
    "official_repository",
    "license_file",
    "security_advisory",
    "maintenance_signal",
    "architecture_spec",
    "supply_chain_standard",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_source_verification_matrix_v0_1=true",
    "source_verification_matrix_created=true",
    "source_preflight_gate_created=true",
    "top_candidate_source_slots_created=true",
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
    print("AVF Capability Source Verification Matrix v0.1 validation")
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


def require_source_matrix(dossier: dict) -> None:
    matrix = read_json(SOURCE_MATRIX)
    if matrix.get("status") != "PASS":
        fail("source verification matrix status must be PASS")
    if matrix.get("goal_id") != THIS_GOAL_ID:
        fail("source verification matrix goal_id mismatch")
    if matrix.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("source verification matrix next safe goal mismatch")
    require_false_flags(matrix.get("claim_boundary", {}), "source verification matrix claim boundary")

    expected_candidate_ids = {candidate["candidate_id"] for candidate in dossier.get("candidate_dossiers", [])}
    rows = matrix.get("candidate_source_rows", [])
    if len(rows) != len(expected_candidate_ids):
        fail("source matrix must include exactly the review dossier candidates")
    row_ids = {row.get("candidate_id") for row in rows}
    missing = sorted(expected_candidate_ids - row_ids)
    if missing:
        fail("source matrix missing candidates:\n" + "\n".join(missing))

    for row in rows:
        slot_types = {slot.get("slot_type") for slot in row.get("source_slots", [])}
        missing_slots = sorted(REQUIRED_SLOT_TYPES - slot_types)
        if missing_slots:
            fail(f"{row.get('candidate_id')} missing source slots:\n" + "\n".join(missing_slots))
        if row.get("integration_recommendation") != "do_not_integrate_yet":
            fail(f"{row.get('candidate_id')} must remain do_not_integrate_yet")
        for slot in row.get("source_slots", []):
            if slot.get("verification_status") != "required_not_performed":
                fail(f"slot must remain required_not_performed: {row.get('candidate_id')} {slot.get('slot_type')}")
            if slot.get("source_fetch_performed") is not False:
                fail(f"slot source_fetch_performed must be false: {row.get('candidate_id')} {slot.get('slot_type')}")
            if slot.get("owner_action_required") is not True:
                fail(f"slot owner_action_required must be true: {row.get('candidate_id')} {slot.get('slot_type')}")
            if not slot.get("target_uri", "").startswith("https://"):
                fail(f"slot target_uri must be https: {row.get('candidate_id')} {slot.get('slot_type')}")


def require_source_preflight_gate() -> None:
    gate = read_json(SOURCE_PREFLIGHT_GATE)
    if gate.get("status") != "PASS":
        fail("source preflight gate status must be PASS")
    if gate.get("gate_decision") != "BLOCKED_PENDING_SOURCE_VERIFICATION_AND_OWNER_APPROVAL":
        fail("source preflight gate must remain blocked")
    if gate.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("source preflight gate next safe goal mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "source preflight gate")
    required_blockers = {
        "official_docs_verification",
        "repository_and_license_verification",
        "security_advisory_review",
        "maintenance_review",
        "architecture_fit_review",
        "owner_approval",
    }
    blockers = set(gate.get("blocking_requirements", []))
    missing = sorted(required_blockers - blockers)
    if missing:
        fail("source preflight gate missing blockers:\n" + "\n".join(missing))


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("source verification validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("source verification validation next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "source verification validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    dossier = read_json(REVIEW_DOSSIER)
    if dossier.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("review dossier does not authorize source verification matrix as next safe goal")
    integration_gate = read_json(INTEGRATION_GATE)
    if integration_gate.get("gate_decision") != "BLOCKED_PENDING_OWNER_REVIEW":
        fail("integration gate must remain blocked before source verification")

    require_source_matrix(dossier)
    require_source_preflight_gate()
    require_validation_result()
    require_markers(NEXT_CODEX_TASK, ["task_id: avf-capability-owner-approval-packet-v0-1", "forbidden_changes:", "validation_commands:", f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}"])
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Source Verification Matrix v0.1 validation")
    print("RESULT: PASS")
    print("capability_source_verification_matrix_v0_1=true")
    print("source_verification_matrix_created=true")
    print("source_preflight_gate_created=true")
    print("top_candidate_source_slots_created=true")
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
