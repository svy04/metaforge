from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_acceptance_decision_packet_v0_1.py"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_gate.json"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_next_action.yml"
DECISION_PACKET = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet.json"
DECISION_GATE = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet_gate.json"
DECISION_REPORT = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ACCEPTANCE_DECISION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_review_v0_1"
ACCEPTANCE_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ACCEPTED_FOR_EVIDENCE_ONLY"
DECISION_STATUS = "primary_source_records_accepted_for_evidence_only_no_adoption"

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

REQUIRED_DECISION_FIELDS = [
    "source_id",
    "candidate_id",
    "source_kind",
    "source_uri",
    "claim_supported",
    "decision",
    "evidence_acceptance_status",
    "adoption_status",
    "acceptance_reason",
    "license_review_required_before_adoption",
    "security_review_required_before_adoption",
    "dependency_install_allowed",
    "runtime_integration_allowed",
]

REQUIRED_FILES = [
    RUNNER,
    REVIEW_GATE,
    REVIEW_NEXT_ACTION,
    DECISION_PACKET,
    DECISION_GATE,
    DECISION_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_acceptance_decision_packet_v0_1=true",
    f"acceptance_decision={ACCEPTANCE_DECISION}",
    f"decision_status={DECISION_STATUS}",
    "evidence_accepted_record_count=16",
    "evidence_rejected_record_count=0",
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
    "action_id: review-capability-candidate-primary-source-acceptance-decision-packet",
    "owner_approval_required_before_execution: false",
    "Review the evidence-only acceptance decision packet",
    "Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Acceptance Decision Packet v0.1 validation")
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


def require_review_gate() -> dict:
    gate = read_json(REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("review gate must point to this acceptance decision goal")
    if gate.get("reviewed_source_record_count") != EXPECTED_COUNTS["reviewed_source_record_count"]:
        fail("review gate reviewed source count mismatch")
    if gate.get("accepted_records") != 0:
        fail("review gate must not pre-accept records")
    if gate.get("dependency_adoption_allowed") is not False:
        fail("review gate dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        fail("review gate runtime integration must remain blocked")
    for source in gate.get("reviewed_source_records", []):
        if source.get("review_status") != "reviewed_unaccepted":
            fail(f"review gate {source.get('source_id')} review status mismatch")
        if source.get("acceptance_status") != "unreviewed":
            fail(f"review gate {source.get('source_id')} acceptance status must remain unreviewed")
    require_false_flags(gate.get("claim_boundary", {}), "review gate claim boundary")
    require_text_markers(
        REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-acceptance-decision-packet",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_decision_record(record: dict, label: str) -> None:
    for field in REQUIRED_DECISION_FIELDS:
        if record.get(field) in (None, ""):
            fail(f"{label} decision record missing {field}")
    if record.get("decision") != "accept_for_evidence_only":
        fail(f"{label} decision must be accept_for_evidence_only")
    if record.get("evidence_acceptance_status") != "accepted_for_internal_design_evidence_only":
        fail(f"{label} evidence acceptance status mismatch")
    if record.get("adoption_status") != "not_adopted":
        fail(f"{label} adoption status must remain not_adopted")
    if record.get("license_review_required_before_adoption") is not True:
        fail(f"{label} license review must be required before adoption")
    if record.get("security_review_required_before_adoption") is not True:
        fail(f"{label} security review must be required before adoption")
    if record.get("dependency_install_allowed") is not False:
        fail(f"{label} dependency install must remain blocked")
    if record.get("runtime_integration_allowed") is not False:
        fail(f"{label} runtime integration must remain blocked")
    if "evidence reference only" not in record.get("acceptance_reason", ""):
        fail(f"{label} acceptance reason must preserve evidence-only boundary")


def require_packet(packet: dict, label: str, review_gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "decision_status": DECISION_STATUS,
        "records_source": "codex_assistant_primary_source_web_research",
        "evidence_acceptance_scope": "internal_design_evidence_only",
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if packet.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if packet.get(key) != value:
            fail(f"{label} {key} mismatch")
    if packet.get("source_required_candidate_ids") != review_gate.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    decisions = packet.get("source_acceptance_decisions", [])
    reviewed = review_gate.get("reviewed_source_records", [])
    if len(decisions) != len(reviewed):
        fail(f"{label} source decision count mismatch")
    reviewed_by_id = {source["source_id"]: source for source in reviewed}
    for decision in decisions:
        source_id = decision.get("source_id")
        if source_id not in reviewed_by_id:
            fail(f"{label} unexpected source decision {source_id}")
        source = reviewed_by_id[source_id]
        for copied in ["candidate_id", "source_kind", "source_uri", "claim_supported"]:
            if decision.get(copied) != source.get(copied):
                fail(f"{label} {source_id} copied {copied} mismatch")
        require_decision_record(decision, f"{label} {source_id}")
    require_false_flags(packet.get("claim_boundary", {}), f"{label} claim boundary")


def require_decision_packet(review_gate: dict) -> None:
    packet = read_json(DECISION_PACKET)
    if packet.get("packet_id") != "avf-capability-candidate-primary-source-acceptance-decision-packet-v0-1":
        fail("decision packet id mismatch")
    require_packet(packet, "decision packet", review_gate)


def require_decision_gate(review_gate: dict) -> None:
    gate = read_json(DECISION_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-acceptance-decision-packet-gate-v0-1":
        fail("decision gate id mismatch")
    if gate.get("status") != "PASS":
        fail("decision gate status must be PASS")
    require_packet(gate, "decision gate", review_gate)


def require_validation_result(review_gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_acceptance_decision_packet_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_packet(result, "validation result", review_gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review_gate = require_review_gate()
    require_decision_packet(review_gate)
    require_decision_gate(review_gate)
    require_text_markers(DECISION_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review_gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Acceptance Decision Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_acceptance_decision_packet_v0_1=true")
    print(f"acceptance_decision={ACCEPTANCE_DECISION}")
    print(f"decision_status={DECISION_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
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
