from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1.py"
AUTHORIZATION_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_gate.json"
AUTHORIZATION_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_next_action.yml"
EVIDENCE_COLLECTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection.json"
EVIDENCE_COLLECTION_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_gate.json"
EVIDENCE_COLLECTION_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_OWNER_APPROVED_MANUAL_EVIDENCE_COLLECTION_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_quality_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
COLLECTION_STATUS = "owner_approved_manual_primary_source_evidence_captured"
COLLECTION_MODE = "manual_assistant_primary_source_review"

EXPECTED_COUNTS = {
    "source_target_count": 7,
    "evidence_record_count": 7,
    "captured_evidence_record_count": 7,
    "empty_evidence_record_count": 0,
    "owner_approval_recorded_count": 1,
    "manual_source_review_performed_count": 7,
    "repo_automation_source_fetch_performed_count": 0,
    "oss_clone_performed_count": 0,
    "dependency_install_performed_count": 0,
    "runtime_integration_performed_count": 0,
    "review_blocker_count": 0,
    "ready_for_manual_evidence_quality_review_count": 1,
}

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
    "runtime_export_performed",
    "collector_started",
    "telemetry_export_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    AUTHORIZATION_REVIEW_GATE,
    AUTHORIZATION_REVIEW_NEXT_ACTION,
    EVIDENCE_COLLECTION,
    EVIDENCE_COLLECTION_GATE,
    EVIDENCE_COLLECTION_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"collection_status={COLLECTION_STATUS}",
    f"collection_mode={COLLECTION_MODE}",
    "owner_approval_recorded=true",
    "external_source_lookup_performed_by_assistant=true",
    "repo_automation_source_fetch_performed=false",
    "source_target_count=7",
    "evidence_record_count=7",
    "captured_evidence_record_count=7",
    "empty_evidence_record_count=0",
    "owner_approval_recorded_count=1",
    "manual_source_review_performed_count=7",
    "repo_automation_source_fetch_performed_count=0",
    "oss_clone_performed_count=0",
    "dependency_install_performed_count=0",
    "runtime_integration_performed_count=0",
    "ready_for_manual_evidence_quality_review_count=1",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "dependency_install_performed=false",
    "runtime_integration_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-priority-1-manual-evidence-quality",
    "owner_approval_required_before_execution: false",
    "Review captured evidence for locator quality, claim boundaries, and adoption safety",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Owner-Approved Manual Evidence Collection v0.1 validation")
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


def require_previous_authorization_review() -> dict:
    review = read_json(AUTHORIZATION_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("authorization review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("authorization review gate must point to this collection goal")
    if review.get("owner_approval_required_before_next_goal") is not True:
        fail("authorization review must require owner approval before this goal")
    if review.get("evidence_capture_authorized") is not False:
        fail("authorization review must not pre-authorize evidence capture")
    if review.get("owner_approval_required_before_next_goal_count") != 1:
        fail("authorization review owner approval count mismatch")
    require_false_flags(review.get("claim_boundary", {}), "authorization review claim boundary")
    require_text_markers(
        AUTHORIZATION_REVIEW_NEXT_ACTION,
        [
            "action_id: owner-approved-manual-evidence-collection-for-capability-candidate-primary-source-priority-1",
            "owner_approval_required_before_execution: true",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_evidence_record(item: dict, request_by_id: dict[str, dict]) -> None:
    record_id = item.get("evidence_record_id", "<missing>")
    request_id = item.get("authorization_request_id", "<missing>")
    if request_id not in request_by_id:
        fail(f"evidence record {record_id} missing matching authorization request")
    request = request_by_id[request_id]
    for key in [
        "source_target_id",
        "candidate_id",
        "source_kind",
        "source_uri",
        "claim_to_extract",
        "capture_scope",
        "adoption_boundary",
    ]:
        if item.get(key) != request.get(key):
            fail(f"evidence record {record_id} {key} mismatch")
    if item.get("capture_status") != "captured_from_owner_approved_manual_review":
        fail(f"evidence record {record_id} capture_status mismatch")
    if item.get("owner_approval_recorded") is not True:
        fail(f"evidence record {record_id} must record owner approval")
    if item.get("manual_source_review_performed") is not True:
        fail(f"evidence record {record_id} must record manual source review")
    if item.get("repo_automation_source_fetch_performed") is not False:
        fail(f"evidence record {record_id} repo automation source fetch must be false")
    for field_name in [
        "exact_locator",
        "evidence_summary",
        "license_or_terms_note",
        "security_or_supply_chain_note",
        "claim_boundary_note",
    ]:
        if not item.get(field_name):
            fail(f"evidence record {record_id} {field_name} must be filled")
    for flag in [
        "source_fetch_performed",
        "external_fetch_performed",
        "oss_clone_performed",
        "dependency_install_performed",
        "runtime_integration_performed",
    ]:
        if item.get(flag) is not False:
            fail(f"evidence record {record_id} {flag} must be false")


def require_collection_record(record: dict, label: str, authorization_review: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "collection_status": COLLECTION_STATUS,
        "collection_mode": COLLECTION_MODE,
        "owner_approval_recorded": True,
        "owner_approval_reference": "current_thread_owner_delegation",
        "external_source_lookup_performed_by_assistant": True,
        "repo_automation_source_fetch_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("authorization_packet_review_gate") != AUTHORIZATION_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input authorization review gate uri mismatch")

    evidence_records = record.get("evidence_records", [])
    if len(evidence_records) != EXPECTED_COUNTS["evidence_record_count"]:
        fail(f"{label} evidence record count mismatch")
    request_by_id = {
        item["authorization_request_id"]: item
        for item in authorization_review.get("reviewed_authorization_requests", [])
    }
    for item in evidence_records:
        require_evidence_record(item, request_by_id)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(authorization_review: dict) -> None:
    gate = read_json(EVIDENCE_COLLECTION_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-owner-approved-manual-evidence-collection-gate-v0-1":
        fail("manual evidence collection gate id mismatch")
    if gate.get("status") != "PASS":
        fail("manual evidence collection gate status must be PASS")
    require_collection_record(gate, "manual evidence collection gate", authorization_review)


def require_validation_result(authorization_review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_collection_record(result, "validation result", authorization_review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    authorization_review = require_previous_authorization_review()
    collection = read_json(EVIDENCE_COLLECTION)
    require_collection_record(collection, "manual evidence collection", authorization_review)
    require_gate(authorization_review)
    require_text_markers(EVIDENCE_COLLECTION_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(authorization_review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Owner-Approved Manual Evidence Collection v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"collection_status={COLLECTION_STATUS}")
    print(f"collection_mode={COLLECTION_MODE}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("owner_approval_recorded=true")
    print("external_source_lookup_performed_by_assistant=true")
    print("repo_automation_source_fetch_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
