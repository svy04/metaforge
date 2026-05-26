from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_primary_source_evidence_owner_authorization_completion_guide_v0_1.py"
REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_review_gate.json"
COMPLETION_GUIDE = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_completion_guide.md"
COMPLETION_GUIDE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_completion_guide_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_completion_guide_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_completion_guide_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_AUTHORIZATION_COMPLETION_GUIDE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_completion_guide_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_input_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1"
GUIDE_DECISION = "GUIDE_READY_EXECUTION_STILL_BLOCKED"

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
    REVIEW_GATE,
    COMPLETION_GUIDE,
    COMPLETION_GUIDE_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

GUIDE_MARKERS = [
    "# AVF Primary-Source Evidence Owner Authorization Completion Guide v0.1",
    "goal_id: avf_capability_primary_source_evidence_owner_authorization_completion_guide_v0_1",
    "owner_authorization_granted: false",
    "collection_execution_allowed: false",
    "source_records_executable: 0",
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
    "manual_owner_collection",
    "pro_manual_collection",
    "codex_assisted_link_opening",
    "automated_collection",
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
    "task_id: avf-capability-primary-source-evidence-owner-filled-authorization-packet-template-v0-1",
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
    "capability_primary_source_evidence_owner_authorization_completion_guide_v0_1=true",
    "owner_authorization_completion_guide_created=true",
    "owner_authorization_completion_guide_gate_created=true",
    "authorization_fields_documented=11",
    "collection_modes_documented=4",
    "source_records_reviewed=35",
    "source_records_executable=0",
    "collection_execution_allowed=false",
    "owner_authorization_granted=false",
    f"guide_decision={GUIDE_DECISION}",
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
    print("AVF Capability Primary-Source Evidence Owner Authorization Completion Guide v0.1 validation")
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


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("review gate must point to this completion guide goal")
    if gate.get("authorization_input_review_passed") is not False:
        fail("review gate must not pass authorization input review")
    if gate.get("owner_authorization_granted") is not False:
        fail("review gate must not grant owner authorization")
    if gate.get("collection_execution_allowed") is not False:
        fail("review gate must keep collection execution blocked")
    if gate.get("authorization_fields_required") != AUTHORIZATION_FIELDS:
        fail("review gate authorization fields mismatch")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        fail("review gate source record review count mismatch")
    if counts.get("source_records_executable") != 0:
        fail("review gate must not make source records executable")
    require_false_flags(gate.get("claim_boundary", {}), "review gate")


def require_completion_guide_gate() -> None:
    gate = read_json(COMPLETION_GUIDE_GATE)
    expected = {
        "gate_id": "avf-capability-primary-source-evidence-owner-authorization-completion-guide-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "owner_authorization_granted": False,
        "collection_execution_allowed": False,
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"completion guide gate {key} mismatch")

    if gate.get("authorization_fields_documented") != AUTHORIZATION_FIELDS:
        fail("completion guide gate documented fields mismatch")
    if gate.get("collection_modes_documented") != COLLECTION_MODES:
        fail("completion guide gate collection modes mismatch")

    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        fail("completion guide gate source record review count mismatch")
    if counts.get("source_records_executable") != 0:
        fail("completion guide gate must not make source records executable")
    require_false_flags(gate.get("claim_boundary", {}), "completion guide gate")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("validator_id") != "validate_avf_capability_primary_source_evidence_owner_authorization_completion_guide_v0_1":
        fail("validation result validator_id mismatch")
    if validation.get("status") != "PASS":
        fail("validation result must be PASS")
    if validation.get("guide_decision") != GUIDE_DECISION:
        fail("validation result guide decision mismatch")
    if validation.get("source_records_executable") != 0:
        fail("validation result must not make source records executable")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_review_gate()
    require_text_markers(COMPLETION_GUIDE, GUIDE_MARKERS)
    require_completion_guide_gate()
    require_text_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Primary-Source Evidence Owner Authorization Completion Guide v0.1 validation")
    print("RESULT: PASS")
    print("capability_primary_source_evidence_owner_authorization_completion_guide_v0_1=true")
    print("owner_authorization_completion_guide_created=true")
    print("owner_authorization_completion_guide_gate_created=true")
    print("authorization_fields_documented=11")
    print("collection_modes_documented=4")
    print("source_records_reviewed=35")
    print("source_records_executable=0")
    print("collection_execution_allowed=false")
    print("owner_authorization_granted=false")
    print(f"guide_decision={GUIDE_DECISION}")
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
