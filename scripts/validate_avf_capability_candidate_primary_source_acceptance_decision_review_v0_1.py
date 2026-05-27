from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_acceptance_decision_review_v0_1.py"
DECISION_PACKET = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet.json"
DECISION_GATE = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet_gate.json"
DECISION_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ACCEPTANCE_DECISION_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_v0_1"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ACCEPTANCE_DECISION_REVIEWED"
REVIEW_STATUS = "evidence_only_acceptance_validated_ready_for_claim_mapping"

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "source_record_count": 16,
    "reviewed_source_record_count": 16,
    "evidence_accepted_record_count": 16,
    "evidence_rejected_record_count": 0,
    "dependency_adopted_record_count": 0,
    "runtime_integrated_record_count": 0,
    "records_requiring_license_review_before_adoption": 16,
    "records_requiring_security_review_before_adoption": 16,
    "reviewed_acceptance_decision_count": 16,
    "review_blocker_count": 0,
    "ready_for_claim_mapping_count": 1,
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
    DECISION_PACKET,
    DECISION_GATE,
    DECISION_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_acceptance_decision_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "evidence_only_acceptance_confirmed=true",
    "adoption_boundary_confirmed=true",
    "ready_for_claim_mapping_count=1",
    "evidence_accepted_record_count=16",
    "dependency_adopted_record_count=0",
    "runtime_integrated_record_count=0",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-evidence-claim-map",
    "owner_approval_required_before_execution: false",
    "Map accepted evidence-only primary-source records to capability claims",
    "Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Acceptance Decision Review v0.1 validation")
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


def require_decision_record(record: dict, label: str) -> None:
    source_id = record.get("source_id", "<missing>")
    if record.get("decision") != "accept_for_evidence_only":
        fail(f"{label} {source_id} decision must be accept_for_evidence_only")
    if record.get("evidence_acceptance_status") != "accepted_for_internal_design_evidence_only":
        fail(f"{label} {source_id} evidence status mismatch")
    if record.get("adoption_status") != "not_adopted":
        fail(f"{label} {source_id} adoption status must remain not_adopted")
    if record.get("license_review_required_before_adoption") is not True:
        fail(f"{label} {source_id} license review must be required")
    if record.get("security_review_required_before_adoption") is not True:
        fail(f"{label} {source_id} security review must be required")
    if record.get("dependency_install_allowed") is not False:
        fail(f"{label} {source_id} dependency install must be blocked")
    if record.get("runtime_integration_allowed") is not False:
        fail(f"{label} {source_id} runtime integration must be blocked")
    if "not an adoption" not in record.get("acceptance_reason", ""):
        fail(f"{label} {source_id} must preserve no-adoption reason")


def require_decision_source(packet: dict, label: str) -> None:
    expected = {
        "goal_id": PREVIOUS_GOAL_ID,
        "previous_goal_id": "avf_capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1",
        "acceptance_decision": "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ACCEPTED_FOR_EVIDENCE_ONLY",
        "decision_status": "primary_source_records_accepted_for_evidence_only_no_adoption",
        "records_source": "codex_assistant_primary_source_web_research",
        "evidence_acceptance_scope": "internal_design_evidence_only",
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": THIS_GOAL_ID,
    }
    for key, value in expected.items():
        if packet.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if key in packet and packet.get(key) != value:
            fail(f"{label} {key} mismatch")
    decisions = packet.get("source_acceptance_decisions", [])
    if len(decisions) != EXPECTED_COUNTS["evidence_accepted_record_count"]:
        fail(f"{label} source acceptance decision count mismatch")
    for decision in decisions:
        require_decision_record(decision, label)
    require_false_flags(packet.get("claim_boundary", {}), f"{label} claim boundary")


def require_previous_inputs() -> tuple[dict, dict]:
    packet = read_json(DECISION_PACKET)
    gate = read_json(DECISION_GATE)
    if packet.get("packet_id") != "avf-capability-candidate-primary-source-acceptance-decision-packet-v0-1":
        fail("decision packet id mismatch")
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-acceptance-decision-packet-gate-v0-1":
        fail("decision gate id mismatch")
    if gate.get("status") != "PASS":
        fail("decision gate status must be PASS")
    require_decision_source(packet, "decision packet")
    require_decision_source(gate, "decision gate")
    require_text_markers(
        DECISION_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-acceptance-decision-packet",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return packet, gate


def require_review_record(record: dict, label: str, decision_packet: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "evidence_only_acceptance_confirmed": True,
        "adoption_boundary_confirmed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("source_required_candidate_ids") != decision_packet.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    reviewed = record.get("reviewed_acceptance_decisions", [])
    if len(reviewed) != EXPECTED_COUNTS["reviewed_acceptance_decision_count"]:
        fail(f"{label} reviewed acceptance decision count mismatch")
    decision_by_source = {
        decision["source_id"]: decision
        for decision in decision_packet.get("source_acceptance_decisions", [])
    }
    for item in reviewed:
        source_id = item.get("source_id")
        if source_id not in decision_by_source:
            fail(f"{label} unexpected reviewed decision {source_id}")
        if item.get("review_status") != "reviewed_evidence_only_acceptance_validated":
            fail(f"{label} {source_id} review status mismatch")
        if item.get("claim_mapping_allowed") is not True:
            fail(f"{label} {source_id} claim mapping must be allowed")
        if item.get("dependency_adoption_allowed") is not False:
            fail(f"{label} {source_id} dependency adoption must remain blocked")
        if item.get("runtime_integration_allowed") is not False:
            fail(f"{label} {source_id} runtime integration must remain blocked")
        require_decision_record(decision_by_source[source_id], f"{label} source")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_review_gate(decision_packet: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-acceptance-decision-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", decision_packet)


def require_validation_result(decision_packet: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_acceptance_decision_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", decision_packet)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    decision_packet, _ = require_previous_inputs()
    require_review_gate(decision_packet)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(decision_packet)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Acceptance Decision Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_acceptance_decision_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("evidence_only_acceptance_confirmed=true")
    print("adoption_boundary_confirmed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
