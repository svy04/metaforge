from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_primary_source_evidence_authorized_collection_packet_v0_1.py"
RETRY_REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_retry_review_gate.json"
RETRY_PACKET = CAPABILITIES / "capability_primary_source_evidence_population_retry_packet.yml"
PRO_PROMPT = CAPABILITIES / "capability_owner_primary_source_evidence_population_pro_prompt.md"
COLLECTION_PACKET = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_packet.yml"
COLLECTION_GATE = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_AUTHORIZED_COLLECTION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_retry_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_run_plan_v0_1"
AUTHORIZATION_DECISION = "BLOCKED_PENDING_EXPLICIT_COLLECTION_AUTHORIZATION"

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

PRIMARY_SOURCE_FAMILIES = [
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

REQUIRED_FILES = [
    RUNNER,
    RETRY_REVIEW_GATE,
    RETRY_PACKET,
    PRO_PROMPT,
    COLLECTION_PACKET,
    COLLECTION_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    "packet_id: avf-capability-primary-source-evidence-authorized-collection-packet-v0-1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"authorization_decision: {AUTHORIZATION_DECISION}",
    "owner_authorization_required: true",
    "owner_authorization_granted: false",
    "collection_authorization_status: not_authorized",
    "manual_owner_collection_allowed: false",
    "pro_manual_collection_allowed: false",
    "codex_assisted_link_opening_allowed: false",
    "automated_collection_allowed: false",
    "automated_scraping_allowed: false",
    "source_records_targeted: 35",
    "source_records_authorized: 0",
    "trusted_sources_by_default: false",
    "ingested_sources_by_default: false",
    "integrated_sources_by_default: false",
    "allowed_source_families_after_explicit_authorization:",
    "authorization_fields_required_before_collection:",
    "collection_modes:",
    "source_collection_records:",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_TASK_MARKERS = [
    "task_id: avf-capability-primary-source-evidence-authorized-collection-run-plan-v0-1",
    "No external collection execution until explicit authorization fields are filled and reviewed",
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
    "capability_primary_source_evidence_authorized_collection_packet_v0_1=true",
    "authorized_collection_packet_created=true",
    "authorized_collection_gate_created=true",
    "source_records_targeted=35",
    "source_records_authorized=0",
    "trusted_sources_by_default=false",
    "ingested_sources_by_default=false",
    "integrated_sources_by_default=false",
    "owner_authorization_required=true",
    "owner_authorization_granted=false",
    "manual_owner_collection_allowed=false",
    "pro_manual_collection_allowed=false",
    "codex_assisted_link_opening_allowed=false",
    "automated_collection_allowed=false",
    "integration_decision=blocked",
    f"authorization_decision={AUTHORIZATION_DECISION}",
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
    print("AVF Capability Primary-Source Evidence Authorized Collection Packet v0.1 validation")
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


def require_previous_retry_review_gate() -> None:
    gate = read_json(RETRY_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("retry review gate goal_id mismatch")
    if gate.get("status") != "PASS":
        fail("retry review gate must be PASS")
    if gate.get("review_decision") != "BLOCKED_RETRY_EVIDENCE_NOT_FILLED":
        fail("retry review gate decision mismatch")
    if gate.get("integration_decision") != "blocked":
        fail("retry review gate must keep integration blocked")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("retry review gate must point to this authorized collection goal")
    counts = gate.get("source_entry_counts", {})
    if counts.get("retry_records_reviewed") != 35:
        fail("retry review gate record count mismatch")
    if counts.get("accepted_retry_records") != 0:
        fail("retry review gate must not accept records")
    require_false_flags(gate.get("claim_boundary", {}), "retry review gate")


def require_collection_gate() -> None:
    gate = read_json(COLLECTION_GATE)
    expected = {
        "gate_id": "avf-capability-primary-source-evidence-authorized-collection-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "authorization_decision": AUTHORIZATION_DECISION,
        "collection_authorization_status": "not_authorized",
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"authorized collection gate {key} mismatch")

    required_bools = {
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "manual_owner_collection_allowed": False,
        "pro_manual_collection_allowed": False,
        "codex_assisted_link_opening_allowed": False,
        "automated_collection_allowed": False,
    }
    for key, value in required_bools.items():
        if gate.get(key) is not value:
            fail(f"authorized collection gate {key} mismatch")

    if gate.get("authorization_fields") != AUTHORIZATION_FIELDS:
        fail("authorized collection gate authorization fields mismatch")
    if gate.get("allowed_source_families_after_explicit_authorization") != PRIMARY_SOURCE_FAMILIES:
        fail("authorized collection gate source families mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "authorized collection gate")

    counts = gate.get("source_entry_counts", {})
    expected_counts = {
        "source_records_targeted": 35,
        "source_records_authorized": 0,
        "trusted_source_records": 0,
        "ingested_source_records": 0,
        "integrated_source_records": 0,
    }
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            fail(f"authorized collection count {key} mismatch")

    collection_modes = gate.get("collection_modes", [])
    if len(collection_modes) != 4:
        fail("authorized collection gate must list four collection modes")
    for mode in collection_modes:
        if mode.get("collection_allowed") is not False:
            fail(f"{mode.get('mode_id')} collection must be blocked")
        if mode.get("authorization_required") is not True:
            fail(f"{mode.get('mode_id')} must require authorization")

    source_records = gate.get("source_collection_records", [])
    if len(source_records) != 35:
        fail("authorized collection gate must include 35 source collection records")
    for record in source_records:
        if record.get("collection_status") != "awaiting_explicit_authorization":
            fail(f"{record.get('source_slot_id')} collection status mismatch")
        for key in [
            "collection_allowed",
            "trusted_source",
            "accepted_for_ingestion",
            "accepted_for_integration",
            "integration_allowed_from_record",
        ]:
            if record.get(key) is not False:
                fail(f"{record.get('source_slot_id')} {key} must be false")

    candidate_records = gate.get("candidate_collection_records", [])
    if not candidate_records:
        fail("authorized collection gate must include candidate collection records")
    for record in candidate_records:
        if record.get("candidate_status") != "blocked_pending_explicit_collection_authorization":
            fail(f"{record.get('candidate_id')} candidate status mismatch")
        if record.get("collection_proposal_allowed") is not False:
            fail(f"{record.get('candidate_id')} collection proposal must remain blocked")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("validator_id") != "validate_avf_capability_primary_source_evidence_authorized_collection_packet_v0_1":
        fail("validation result validator_id mismatch")
    if validation.get("status") != "PASS":
        fail("validation result must be PASS")
    if validation.get("authorization_decision") != AUTHORIZATION_DECISION:
        fail("validation result authorization decision mismatch")
    if validation.get("owner_authorization_granted") is not False:
        fail("validation result owner authorization must remain false")
    if validation.get("source_records_authorized") != 0:
        fail("validation result must not authorize source records")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_retry_review_gate()
    require_text_markers(COLLECTION_PACKET, PACKET_MARKERS + PRIMARY_SOURCE_FAMILIES + AUTHORIZATION_FIELDS)
    require_collection_gate()
    require_text_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Primary-Source Evidence Authorized Collection Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_primary_source_evidence_authorized_collection_packet_v0_1=true")
    print("authorized_collection_packet_created=true")
    print("authorized_collection_gate_created=true")
    print("source_records_targeted=35")
    print("source_records_authorized=0")
    print("trusted_sources_by_default=false")
    print("ingested_sources_by_default=false")
    print("integrated_sources_by_default=false")
    print("owner_authorization_required=true")
    print("owner_authorization_granted=false")
    print("manual_owner_collection_allowed=false")
    print("pro_manual_collection_allowed=false")
    print("codex_assisted_link_opening_allowed=false")
    print("automated_collection_allowed=false")
    print("integration_decision=blocked")
    print(f"authorization_decision={AUTHORIZATION_DECISION}")
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
