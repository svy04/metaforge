from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_owner_filled_primary_source_evidence_review_v0_1.py"
POPULATION_PACKET = CAPABILITIES / "capability_owner_primary_source_evidence_population_packet.yml"
POPULATION_GATE = CAPABILITIES / "capability_owner_primary_source_evidence_population_packet_gate.json"
PRO_PROMPT = CAPABILITIES / "capability_owner_primary_source_evidence_population_pro_prompt.md"
REVIEW_GATE = CAPABILITIES / "capability_owner_filled_primary_source_evidence_review_gate.json"
VALIDATION_RESULT = CAPABILITIES / "capability_owner_filled_primary_source_evidence_review_v0_1.validation_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_owner_filled_primary_source_evidence_review_next_codex_task_packet.yml"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_OWNER_FILLED_PRIMARY_SOURCE_EVIDENCE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_owner_filled_primary_source_evidence_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_owner_primary_source_evidence_population_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_population_retry_v0_1"
REVIEW_DECISION = "BLOCKED_OWNER_OR_PRO_EVIDENCE_NOT_FILLED"

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

CAPTURED_EVIDENCE_FIELDS = [
    "source_uri",
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
    POPULATION_PACKET,
    POPULATION_GATE,
    PRO_PROMPT,
    REVIEW_GATE,
    VALIDATION_RESULT,
    NEXT_CODEX_TASK,
    VALIDATION_REPORT,
]

REQUIRED_GATE_FIELDS = {
    "gate_id",
    "created_at",
    "goal_id",
    "previous_goal_id",
    "status",
    "review_decision",
    "integration_decision",
    "population_packet_uri",
    "source_entry_counts",
    "required_evidence_fields",
    "captured_evidence_fields",
    "source_record_reviews",
    "candidate_review_records",
    "next_safe_goal_id",
    "claim_boundary",
}

NEXT_TASK_MARKERS = [
    "task_id: avf-capability-primary-source-evidence-population-retry-v0-1",
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
    "capability_owner_filled_primary_source_evidence_review_v0_1=true",
    "owner_filled_primary_source_evidence_review_gate_created=true",
    "source_slots_reviewed=35",
    "empty_source_records=35",
    "partial_source_records=0",
    "complete_source_records=0",
    "accepted_source_records=0",
    "integration_decision=blocked",
    f"review_decision={REVIEW_DECISION}",
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
    print("AVF Capability Owner-Filled Primary-Source Evidence Review v0.1 validation")
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


def require_inputs() -> None:
    packet_text = read(POPULATION_PACKET)
    gate = read_json(POPULATION_GATE)
    prompt_text = read(PRO_PROMPT)
    if f"goal_id: {PREVIOUS_GOAL_ID}" not in packet_text:
        fail("population packet goal_id mismatch")
    if f"next_safe_goal_id: {THIS_GOAL_ID}" not in read(CAPABILITIES / "capability_owner_primary_source_evidence_population_next_codex_task_packet.yml"):
        fail("population next task must point to this review goal")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("population gate must point to this review goal")
    if gate.get("source_slots_to_populate") != 35:
        fail("population gate source slot count mismatch")
    if gate.get("records_completed_by_default") != 0:
        fail("population gate must not complete records by default")
    if gate.get("records_accepted_by_default") != 0:
        fail("population gate must not accept records by default")
    if "Return populated evidence records only" not in prompt_text:
        fail("PRO prompt must preserve population-only output instruction")
    require_false_flags(gate.get("claim_boundary", {}), "population gate")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    missing = sorted(REQUIRED_GATE_FIELDS - set(gate))
    if missing:
        fail("review gate missing fields:\n" + "\n".join(missing))
    expected = {
        "gate_id": "avf-capability-owner-filled-primary-source-evidence-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"review gate {key} mismatch")
    if gate.get("required_evidence_fields") != REQUIRED_EVIDENCE_FIELDS:
        fail("review gate required evidence fields mismatch")
    if gate.get("captured_evidence_fields") != CAPTURED_EVIDENCE_FIELDS:
        fail("review gate captured evidence fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "review gate")

    counts = gate.get("source_entry_counts", {})
    expected_counts = {
        "source_slots_reviewed": 35,
        "empty_source_records": 35,
        "partial_source_records": 0,
        "complete_source_records": 0,
        "accepted_source_records": 0,
        "integration_allowed_records": 0,
    }
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            fail(f"review gate count {key} mismatch")

    source_reviews = gate.get("source_record_reviews", [])
    if len(source_reviews) != 35:
        fail("review gate must include 35 source record reviews")
    for review in source_reviews:
        if review.get("review_status") != "empty_record_blocked":
            fail(f"{review.get('source_slot_id')} review status mismatch")
        if review.get("missing_required_fields") != REQUIRED_EVIDENCE_FIELDS:
            fail(f"{review.get('source_slot_id')} missing fields mismatch")
        if review.get("accepted_for_ingestion") is not False:
            fail(f"{review.get('source_slot_id')} must not be accepted for ingestion")
        if review.get("accepted_for_integration") is not False:
            fail(f"{review.get('source_slot_id')} must not be accepted for integration")

    candidate_reviews = gate.get("candidate_review_records", [])
    if not candidate_reviews:
        fail("review gate must include candidate review records")
    for review in candidate_reviews:
        if review.get("candidate_status") != "blocked_no_complete_primary_source_records":
            fail(f"{review.get('candidate_id')} candidate status mismatch")
        if review.get("complete_source_records") != 0:
            fail(f"{review.get('candidate_id')} complete source records must be zero")
        if review.get("integration_proposal_allowed") is not False:
            fail(f"{review.get('candidate_id')} integration proposal must be blocked")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_owner_filled_primary_source_evidence_review_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
    if result.get("source_slots_reviewed") != 35:
        fail("validation result source slot count mismatch")
    if result.get("accepted_source_records") != 0:
        fail("validation result accepted source records must be zero")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_inputs()
    require_review_gate()
    require_validation_result()
    require_text_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Owner-Filled Primary-Source Evidence Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_owner_filled_primary_source_evidence_review_v0_1=true")
    print("owner_filled_primary_source_evidence_review_gate_created=true")
    print("source_slots_reviewed=35")
    print("empty_source_records=35")
    print("partial_source_records=0")
    print("complete_source_records=0")
    print("accepted_source_records=0")
    print("integration_decision=blocked")
    print(f"review_decision={REVIEW_DECISION}")
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
