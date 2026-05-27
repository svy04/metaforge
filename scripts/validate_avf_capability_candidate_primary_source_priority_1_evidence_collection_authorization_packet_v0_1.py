from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1.py"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_gate.json"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_next_action.yml"
AUTHORIZATION_PACKET = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet.json"
AUTHORIZATION_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_gate.json"
AUTHORIZATION_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_EVIDENCE_COLLECTION_AUTHORIZATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PACKET_STATUS = "authorization_packet_created_no_evidence_collected"
AUTHORIZATION_STATUS = "pending_owner_approval"
AUTHORIZATION_DECISION = "PRIMARY_SOURCE_EVIDENCE_COLLECTION_REQUIRES_OWNER_APPROVAL"

EXPECTED_COUNTS = {
    "source_target_count": 7,
    "authorization_request_count": 7,
    "owner_approval_required_count": 7,
    "evidence_capture_authorized_count": 0,
    "filled_evidence_record_count": 0,
    "source_fetch_performed_count": 0,
    "oss_clone_performed_count": 0,
    "dependency_install_performed_count": 0,
    "runtime_integration_performed_count": 0,
    "ready_for_authorization_packet_review_count": 1,
}

EMPTY_FIELDS = [
    "exact_locator",
    "evidence_summary",
    "license_or_terms_note",
    "security_or_supply_chain_note",
]

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
    REVIEW_GATE,
    REVIEW_NEXT_ACTION,
    AUTHORIZATION_PACKET,
    AUTHORIZATION_GATE,
    AUTHORIZATION_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"authorization_decision={AUTHORIZATION_DECISION}",
    f"authorization_status={AUTHORIZATION_STATUS}",
    f"packet_status={PACKET_STATUS}",
    "authorization_packet_not_evidence_collection_gate=true",
    "owner_approval_required_before_evidence_collection=true",
    "source_target_count=7",
    "authorization_request_count=7",
    "owner_approval_required_count=7",
    "evidence_capture_authorized_count=0",
    "filled_evidence_record_count=0",
    "source_fetch_performed_count=0",
    "oss_clone_performed_count=0",
    "dependency_install_performed_count=0",
    "runtime_integration_performed_count=0",
    "ready_for_authorization_packet_review_count=1",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "dependency_install_performed=false",
    "runtime_integration_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-priority-1-evidence-collection-authorization-packet",
    "owner_approval_required_before_execution: false",
    "Review the evidence collection authorization packet",
    "Confirm evidence capture remains pending owner approval",
    "Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Evidence Collection Authorization Packet v0.1 validation")
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


def require_previous_review() -> dict:
    review = read_json(REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("manual evidence workspace review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("manual evidence workspace review must point to this authorization packet goal")
    if review.get("ready_for_evidence_collection_authorization_packet_count") != 1:
        fail("manual evidence workspace review must be ready for authorization packet")
    if review.get("manual_workspace_not_evidence_collection_gate") is not True:
        fail("manual evidence workspace review must confirm non-collection boundary")
    if review.get("filled_evidence_record_count") != 0:
        fail("manual evidence workspace review must not contain filled evidence")
    require_false_flags(review.get("claim_boundary", {}), "manual workspace review claim boundary")
    require_text_markers(
        REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-evidence-collection-authorization-packet",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_authorization_request(item: dict, template_by_id: dict[str, dict]) -> None:
    request_id = item.get("authorization_request_id", "<missing>")
    template_id = item.get("evidence_record_template_id", "<missing>")
    if template_id not in template_by_id:
        fail(f"authorization request {request_id} missing matching reviewed template")
    template = template_by_id[template_id]
    for key in [
        "evidence_record_template_id",
        "source_target_id",
        "candidate_id",
        "source_kind",
        "source_uri",
        "capture_scope",
        "claim_to_extract",
        "retrieval_mode",
        "quote_limit_policy",
        "adoption_boundary",
        "capture_status",
    ]:
        if item.get(key) != template.get(key):
            fail(f"authorization request {request_id} {key} mismatch")
    if item.get("authorization_status") != AUTHORIZATION_STATUS:
        fail(f"authorization request {request_id} authorization_status mismatch")
    if item.get("owner_approval_required_before_capture") is not True:
        fail(f"authorization request {request_id} must require owner approval")
    if item.get("evidence_capture_authorized") is not False:
        fail(f"authorization request {request_id} evidence_capture_authorized must be false")
    if item.get("integration_status") != "proposed_authorization_only":
        fail(f"authorization request {request_id} integration_status mismatch")
    for field_name in EMPTY_FIELDS:
        if item.get(field_name) != "":
            fail(f"authorization request {request_id} {field_name} must remain empty")
    for flag in [
        "source_fetch_performed",
        "external_fetch_performed",
        "oss_clone_performed",
        "dependency_install_performed",
        "runtime_integration_performed",
    ]:
        if item.get(flag) is not False:
            fail(f"authorization request {request_id} {flag} must be false")


def require_authorization_record(record: dict, label: str, review: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "authorization_decision": AUTHORIZATION_DECISION,
        "authorization_status": AUTHORIZATION_STATUS,
        "packet_status": PACKET_STATUS,
        "authorization_packet_not_evidence_collection_gate": True,
        "owner_approval_required_before_evidence_collection": True,
        "evidence_capture_authorized": False,
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
    if input_uris.get("manual_evidence_workspace_review_gate") != REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input review gate uri mismatch")

    requests = record.get("authorization_requests", [])
    if len(requests) != EXPECTED_COUNTS["authorization_request_count"]:
        fail(f"{label} authorization request count mismatch")
    template_by_id = {
        item["evidence_record_template_id"]: item
        for item in review.get("reviewed_evidence_record_templates", [])
    }
    for item in requests:
        require_authorization_request(item, template_by_id)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(review: dict) -> None:
    gate = read_json(AUTHORIZATION_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-evidence-collection-authorization-packet-gate-v0-1":
        fail("authorization gate id mismatch")
    if gate.get("status") != "PASS":
        fail("authorization gate status must be PASS")
    require_authorization_record(gate, "authorization gate", review)


def require_validation_result(review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_authorization_record(result, "validation result", review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review = require_previous_review()
    packet = read_json(AUTHORIZATION_PACKET)
    require_authorization_record(packet, "authorization packet", review)
    require_gate(review)
    require_text_markers(AUTHORIZATION_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Evidence Collection Authorization Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"authorization_decision={AUTHORIZATION_DECISION}")
    print(f"authorization_status={AUTHORIZATION_STATUS}")
    print(f"packet_status={PACKET_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("authorization_packet_not_evidence_collection_gate=true")
    print("owner_approval_required_before_evidence_collection=true")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
