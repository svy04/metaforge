from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1.py"
MANUAL_GUIDE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_guide_gate.json"
PACKET_TEMPLATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template.yml"
PACKET_TEMPLATE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_MANUAL_COMPLETION_PACKET_TEMPLATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_guide_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1"
GUIDE_DECISION = "MANUAL_COMPLETION_GUIDE_READY_EXECUTION_STILL_BLOCKED"
TEMPLATE_DECISION = "MANUAL_COMPLETION_PACKET_TEMPLATE_READY_OWNER_INPUT_REQUIRED"

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

AUTHORIZATION_FIELDS = [
    "owner_authorization_statement",
    "authorized_by",
    "authorized_at",
    "authorization_expires_at",
    "authorized_collection_modes",
    "authorized_source_families",
    "authorized_candidate_ids",
    "authorized_source_slot_ids",
    "max_records_to_collect",
    "collection_boundaries",
    "revocation_note",
]

COLLECTION_MODES = [
    "manual_owner_collection",
    "pro_manual_collection",
    "codex_assisted_link_opening",
    "automated_collection",
]

REQUIRED_FILES = [
    RUNNER,
    MANUAL_GUIDE_GATE,
    PACKET_TEMPLATE,
    PACKET_TEMPLATE_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEMPLATE_MARKERS = [
    "packet_id: avf-capability-primary-source-evidence-owner-manual-completion-packet-template-v0-1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"template_decision: {TEMPLATE_DECISION}",
    "owner_input_required: true",
    "manual_completion_packet_completed: false",
    "owner_authorization_granted: false",
    "collection_execution_allowed: false",
    "source_records_reviewed: 35",
    "source_records_executable: 0",
    "owner_authorization_statement:",
    "authorized_by:",
    "authorized_at:",
    "authorization_expires_at:",
    "authorized_collection_modes: []",
    "authorized_source_families: []",
    "authorized_candidate_ids: []",
    "authorized_source_slot_ids: []",
    "max_records_to_collect: 0",
    "collection_boundaries: []",
    "revocation_note:",
    "manual_owner_collection_authorized: false",
    "pro_manual_collection_authorized: false",
    "codex_assisted_link_opening_authorized: false",
    "automated_collection_authorized: false",
    "No source collection execution",
    "No provider calls",
    "No live model calls",
    "No external service calls",
    "No automated scraping",
    "No OSS clone",
    "No package install",
    "No dependency install",
    "No runtime integration",
    "No deploy",
    "No publish",
    "No release readiness claim",
    "No production readiness claim",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_TASK_MARKERS = [
    "task_id: avf-capability-primary-source-evidence-owner-manual-completion-packet-review-v0-1",
    "manual completion packet review",
    "owner-filled packet",
    "No source collection execution",
    "No provider calls",
    "No live model calls",
    "No external service calls",
    "No automated scraping",
    "No OSS clone",
    "No package install",
    "No dependency install",
    "No runtime integration",
    "No deploy",
    "No publish",
    "No release readiness claim",
    "No production readiness claim",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1=true",
    "owner_manual_completion_packet_template_created=true",
    "owner_manual_completion_packet_template_gate_created=true",
    "authorization_fields_templated=11",
    "authorization_fields_completed=0",
    "collection_modes_templated=4",
    "collection_modes_selected=0",
    "owner_input_required=true",
    "manual_completion_packet_completed=false",
    "source_records_reviewed=35",
    "source_records_executable=0",
    "collection_execution_allowed=false",
    "owner_authorization_granted=false",
    f"template_decision={TEMPLATE_DECISION}",
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
    print("AVF Capability Primary-Source Evidence Owner Manual Completion Packet Template v0.1 validation")
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


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_manual_guide_gate() -> None:
    gate = read_json(MANUAL_GUIDE_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("manual guide gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("manual guide gate must point to this packet template goal")
    if gate.get("guide_decision") != GUIDE_DECISION:
        fail("manual guide gate decision mismatch")
    if gate.get("owner_input_required") is not True:
        fail("manual guide gate must require owner input")
    if gate.get("owner_authorization_granted") is not False:
        fail("manual guide gate must not grant owner authorization")
    if gate.get("collection_execution_allowed") is not False:
        fail("manual guide gate must keep collection blocked")
    if gate.get("authorization_fields_documented") != AUTHORIZATION_FIELDS:
        fail("manual guide gate authorization fields mismatch")
    if gate.get("collection_modes_documented") != COLLECTION_MODES:
        fail("manual guide gate collection modes mismatch")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        fail("manual guide gate source record review count mismatch")
    if counts.get("source_records_executable") != 0:
        fail("manual guide gate must not make source records executable")
    require_false_flags(gate.get("claim_boundary", {}), "manual guide gate")


def require_packet_template_gate() -> None:
    gate = read_json(PACKET_TEMPLATE_GATE)
    expected = {
        "gate_id": "avf-capability-primary-source-evidence-owner-manual-completion-packet-template-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "template_decision": TEMPLATE_DECISION,
        "owner_input_required": True,
        "manual_completion_packet_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_templated_count": len(AUTHORIZATION_FIELDS),
        "authorization_fields_completed": 0,
        "collection_modes_templated_count": len(COLLECTION_MODES),
        "collection_modes_selected": 0,
        "collection_execution_allowed": False,
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"packet template gate {key} mismatch")

    if gate.get("authorization_fields_templated") != AUTHORIZATION_FIELDS:
        fail("packet template gate templated fields mismatch")
    if gate.get("missing_authorization_fields") != AUTHORIZATION_FIELDS:
        fail("packet template gate missing fields mismatch")
    if gate.get("collection_modes_templated") != COLLECTION_MODES:
        fail("packet template gate collection modes mismatch")
    if gate.get("selected_collection_modes") != []:
        fail("packet template gate selected collection modes must be empty")

    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        fail("packet template gate source record review count mismatch")
    if counts.get("source_records_executable") != 0:
        fail("packet template gate must not make source records executable")
    require_false_flags(gate.get("claim_boundary", {}), "packet template gate")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("validator_id") != "validate_avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1":
        fail("validation result validator_id mismatch")
    if validation.get("status") != "PASS":
        fail("validation result must be PASS")
    if validation.get("template_decision") != TEMPLATE_DECISION:
        fail("validation result template decision mismatch")
    if validation.get("owner_input_required") is not True:
        fail("validation result must require owner input")
    if validation.get("authorization_fields_completed") != 0:
        fail("validation result must not complete fields")
    if validation.get("collection_modes_selected") != 0:
        fail("validation result must not select modes")
    if validation.get("source_records_executable") != 0:
        fail("validation result must not make source records executable")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_manual_guide_gate()
    require_text_markers(PACKET_TEMPLATE, TEMPLATE_MARKERS)
    require_packet_template_gate()
    require_text_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Primary-Source Evidence Owner Manual Completion Packet Template v0.1 validation")
    print("RESULT: PASS")
    print("capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1=true")
    print("owner_manual_completion_packet_template_created=true")
    print("owner_manual_completion_packet_template_gate_created=true")
    print("authorization_fields_templated=11")
    print("authorization_fields_completed=0")
    print("collection_modes_templated=4")
    print("collection_modes_selected=0")
    print("owner_input_required=true")
    print("manual_completion_packet_completed=false")
    print("source_records_reviewed=35")
    print("source_records_executable=0")
    print("collection_execution_allowed=false")
    print("owner_authorization_granted=false")
    print(f"template_decision={TEMPLATE_DECISION}")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("automated_scraping_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
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
