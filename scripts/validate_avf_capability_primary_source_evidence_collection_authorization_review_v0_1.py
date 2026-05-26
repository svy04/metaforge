from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_primary_source_evidence_collection_authorization_review_v0_1.py"
RUN_PLAN = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan.yml"
RUN_PLAN_GATE = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_collection_authorization_review_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_collection_authorization_review_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_collection_authorization_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_COLLECTION_AUTHORIZATION_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_collection_authorization_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_run_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_input_packet_v0_1"
REVIEW_DECISION = "BLOCKED_AUTHORIZATION_FIELDS_MISSING"
RUN_PLAN_DECISION = "PLAN_READY_EXECUTION_BLOCKED_PENDING_EXPLICIT_AUTHORIZATION"

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

REQUIRED_FILES = [
    RUNNER,
    RUN_PLAN,
    RUN_PLAN_GATE,
    REVIEW_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

NEXT_TASK_MARKERS = [
    "task_id: avf-capability-primary-source-evidence-owner-authorization-input-packet-v0-1",
    "No collection execution from this packet",
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
    "capability_primary_source_evidence_collection_authorization_review_v0_1=true",
    "collection_authorization_review_gate_created=true",
    "authorization_fields_reviewed=11",
    "authorization_fields_present=0",
    "missing_authorization_fields=11",
    "source_records_reviewed=35",
    "source_records_executable=0",
    "collection_execution_allowed=false",
    "authorization_review_passed=false",
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
    print("AVF Capability Primary-Source Evidence Collection Authorization Review v0.1 validation")
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


def require_run_plan_gate() -> None:
    gate = read_json(RUN_PLAN_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("run plan gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("run plan gate must point to this authorization review goal")
    if gate.get("run_plan_decision") != RUN_PLAN_DECISION:
        fail("run plan gate decision mismatch")
    if gate.get("authorization_present") is not False:
        fail("run plan gate authorization_present must remain false")
    if gate.get("collection_execution_allowed") is not False:
        fail("run plan gate must keep collection execution blocked")
    if gate.get("authorization_fields_required") != AUTHORIZATION_FIELDS:
        fail("run plan gate authorization fields mismatch")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_planned") != 35:
        fail("run plan gate source record count mismatch")
    if counts.get("source_records_executable") != 0:
        fail("run plan gate must not make source records executable")
    require_false_flags(gate.get("claim_boundary", {}), "run plan gate")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    expected = {
        "gate_id": "avf-capability-primary-source-evidence-collection-authorization-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "authorization_review_passed": False,
        "collection_execution_allowed": False,
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"authorization review gate {key} mismatch")

    if gate.get("authorization_fields_reviewed") != AUTHORIZATION_FIELDS:
        fail("authorization review gate reviewed fields mismatch")
    if gate.get("missing_authorization_fields") != AUTHORIZATION_FIELDS:
        fail("authorization review gate missing fields mismatch")
    if gate.get("authorization_fields_present") != 0:
        fail("authorization review gate must not report present fields")
    require_false_flags(gate.get("claim_boundary", {}), "authorization review gate")

    counts = gate.get("source_entry_counts", {})
    expected_counts = {
        "source_records_reviewed": 35,
        "source_records_executable": 0,
        "trusted_source_records": 0,
        "ingested_source_records": 0,
        "integrated_source_records": 0,
    }
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            fail(f"authorization review count {key} mismatch")

    mode_reviews = gate.get("mode_reviews", [])
    if len(mode_reviews) != 4:
        fail("authorization review gate must include four mode reviews")
    for mode in mode_reviews:
        if mode.get("review_status") != "blocked_missing_authorization":
            fail(f"{mode.get('mode_id')} mode review status mismatch")
        if mode.get("execution_allowed") is not False:
            fail(f"{mode.get('mode_id')} execution must remain false")

    task_reviews = gate.get("source_task_reviews", [])
    if len(task_reviews) != 35:
        fail("authorization review gate must include 35 source task reviews")
    for task in task_reviews:
        if task.get("review_status") != "blocked_missing_authorization":
            fail(f"{task.get('source_slot_id')} review status mismatch")
        for key in [
            "collection_execution_allowed",
            "trusted_source",
            "accepted_for_ingestion",
            "accepted_for_integration",
            "integration_allowed_from_record",
        ]:
            if task.get(key) is not False:
                fail(f"{task.get('source_slot_id')} {key} must be false")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("validator_id") != "validate_avf_capability_primary_source_evidence_collection_authorization_review_v0_1":
        fail("validation result validator_id mismatch")
    if validation.get("status") != "PASS":
        fail("validation result must be PASS")
    if validation.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
    if validation.get("authorization_review_passed") is not False:
        fail("validation result authorization review must not pass")
    if validation.get("source_records_executable") != 0:
        fail("validation result must not make source records executable")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_run_plan_gate()
    require_review_gate()
    require_text_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Primary-Source Evidence Collection Authorization Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_primary_source_evidence_collection_authorization_review_v0_1=true")
    print("collection_authorization_review_gate_created=true")
    print("authorization_fields_reviewed=11")
    print("authorization_fields_present=0")
    print("missing_authorization_fields=11")
    print("source_records_reviewed=35")
    print("source_records_executable=0")
    print("collection_execution_allowed=false")
    print("authorization_review_passed=false")
    print("integration_decision=blocked")
    print(f"review_decision={REVIEW_DECISION}")
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
