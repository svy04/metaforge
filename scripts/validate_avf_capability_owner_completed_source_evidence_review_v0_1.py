from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_owner_completed_source_evidence_review_v0_1.py"
RESEARCH_PACKET = CAPABILITIES / "capability_primary_source_research_packet.yml"
PRO_PROMPT = CAPABILITIES / "capability_primary_source_research_pro_prompt.md"
FIXTURE_TEMPLATE = CAPABILITIES / "capability_source_evidence_fixture_template.yml"
FIXTURE_MANIFEST = CAPABILITIES / "capability_source_evidence_fixture_template_manifest.json"
REVIEW_GATE = CAPABILITIES / "capability_owner_completed_source_evidence_review_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_owner_completed_source_evidence_review_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_owner_completed_source_evidence_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_OWNER_COMPLETED_SOURCE_EVIDENCE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_owner_completed_source_evidence_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_research_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_external_primary_source_research_authorization_packet_v0_1"
REVIEW_DECISION = "BLOCKED_OWNER_EVIDENCE_NOT_COMPLETED"

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

REQUIRED_FIELDS = [
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

REQUIRED_CATEGORIES = [
    "authenticity",
    "license",
    "security",
    "maintenance",
    "architecture_fit",
    "supply_chain_risk",
    "owner_approval",
]

REQUIRED_FILES = [
    RUNNER,
    RESEARCH_PACKET,
    PRO_PROMPT,
    FIXTURE_TEMPLATE,
    FIXTURE_MANIFEST,
    REVIEW_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_GATE_FIELDS = {
    "gate_id",
    "created_at",
    "goal_id",
    "status",
    "reviewed_fixture_uri",
    "research_packet_uri",
    "source_entry_counts",
    "review_decision",
    "integration_decision",
    "owner_approval_present",
    "owner_approval_required",
    "required_fields",
    "required_categories",
    "categories_satisfied",
    "source_record_reviews",
    "candidate_review_records",
    "next_safe_goal_id",
    "claim_boundary",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_owner_completed_source_evidence_review_v0_1=true",
    "owner_completed_source_evidence_review_gate_created=true",
    "source_slots_reviewed=35",
    "completed_source_records=0",
    "accepted_source_records=0",
    "integration_decision=blocked",
    f"review_decision={REVIEW_DECISION}",
    "owner_approval_present=false",
    "protected_action_executed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Owner-Completed Source Evidence Review v0.1 validation")
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


def require_inputs() -> dict:
    manifest = read_json(FIXTURE_MANIFEST)
    if f"goal_id: {PREVIOUS_GOAL_ID}" not in read(RESEARCH_PACKET):
        fail("research packet previous goal_id mismatch")
    if f"next_safe_goal_id: {THIS_GOAL_ID}" not in read(RESEARCH_PACKET):
        fail("research packet must point to this owner-completed evidence review goal")
    if "Do not fetch, scrape, clone, install, integrate, deploy, publish, or automate from this repo." not in read(PRO_PROMPT):
        fail("PRO prompt must preserve protected-action boundary")
    if "Evidence remains untrusted until evaluated by the source evidence ingestion validator." not in read(FIXTURE_TEMPLATE):
        fail("fixture template must preserve untrusted evidence warning")
    return manifest


def require_review_gate(manifest: dict) -> None:
    gate = read_json(REVIEW_GATE)
    missing = sorted(REQUIRED_GATE_FIELDS - set(gate))
    if missing:
        fail("review gate missing fields:\n" + "\n".join(missing))
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    if gate.get("goal_id") != THIS_GOAL_ID:
        fail("review gate goal_id mismatch")
    if gate.get("review_decision") != REVIEW_DECISION:
        fail("review gate decision mismatch")
    if gate.get("integration_decision") != "blocked":
        fail("review gate integration decision must remain blocked")
    if gate.get("owner_approval_present") is not False:
        fail("owner approval must be absent in this review gate")
    if gate.get("owner_approval_required") is not True:
        fail("owner approval must be required")
    if gate.get("required_fields") != REQUIRED_FIELDS:
        fail("review gate required fields mismatch")
    if gate.get("required_categories") != REQUIRED_CATEGORIES:
        fail("review gate required categories mismatch")
    if gate.get("categories_satisfied") != []:
        fail("no categories may be satisfied without completed evidence")
    if gate.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("review gate next safe goal mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "review gate claim boundary")

    entry_count = len(manifest.get("candidate_template_records", []))
    candidate_count = len({entry["candidate_id"] for entry in manifest.get("candidate_template_records", [])})
    counts = gate.get("source_entry_counts", {})
    expected_counts = {
        "source_slots_reviewed": entry_count,
        "completed_source_records": 0,
        "incomplete_source_records": entry_count,
        "accepted_source_records": 0,
        "rejected_source_records": entry_count,
        "candidate_count": candidate_count,
    }
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            fail(f"review gate count {key} mismatch")

    source_reviews = gate.get("source_record_reviews", [])
    if len(source_reviews) != entry_count:
        fail("source record review count must match manifest entries")
    for review in source_reviews:
        if review.get("review_status") != "blocked_missing_required_fields":
            fail(f"{review.get('source_slot_id')} review status mismatch")
        if review.get("accepted_for_evaluation") is not False:
            fail(f"{review.get('source_slot_id')} must not be accepted for evaluation")
        if review.get("accepted_for_integration") is not False:
            fail(f"{review.get('source_slot_id')} must not be accepted for integration")
        if review.get("missing_required_fields") != REQUIRED_FIELDS:
            fail(f"{review.get('source_slot_id')} missing fields mismatch")

    candidate_reviews = gate.get("candidate_review_records", [])
    if len(candidate_reviews) != candidate_count:
        fail("candidate review count mismatch")
    for review in candidate_reviews:
        if review.get("candidate_status") != "blocked_no_completed_source_evidence":
            fail(f"{review.get('candidate_id')} candidate status mismatch")
        if review.get("integration_proposal_allowed") is not False:
            fail(f"{review.get('candidate_id')} integration proposal must be blocked")
        if review.get("owner_approval_required") is not True:
            fail(f"{review.get('candidate_id')} owner approval must be required")
        if review.get("categories_missing") != REQUIRED_CATEGORIES:
            fail(f"{review.get('candidate_id')} missing categories mismatch")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("validator_id") != "validate_avf_capability_owner_completed_source_evidence_review_v0_1":
        fail("validation result validator_id mismatch")
    if validation.get("status") != "PASS":
        fail("validation result status must be PASS")
    if validation.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "validation result claim boundary")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    manifest = require_inputs()
    require_review_gate(manifest)
    require_validation_result()
    require_text_markers(
        NEXT_CODEX_TASK,
        [
            "task_id: avf-capability-external-primary-source-research-authorization-packet-v0-1",
            "No provider calls without explicit owner authorization",
            "No automated scraping",
            "No package install",
            "No dependency install",
            "No OSS clone",
            "No runtime integration",
            f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
        ],
    )
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Owner-Completed Source Evidence Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_owner_completed_source_evidence_review_v0_1=true")
    print("owner_completed_source_evidence_review_gate_created=true")
    print("source_slots_reviewed=35")
    print("completed_source_records=0")
    print("accepted_source_records=0")
    print("integration_decision=blocked")
    print(f"review_decision={REVIEW_DECISION}")
    print("owner_approval_present=false")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
