from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_source_evidence_evaluation_packet_v0_1.py"
OWNER_SUPPLIED_EVIDENCE_PACKET = CAPABILITIES / "capability_owner_supplied_source_evidence_packet.json"
OWNER_SUPPLIED_EVIDENCE_GATE = CAPABILITIES / "capability_owner_supplied_source_evidence_preflight_gate.json"
SOURCE_EVIDENCE_EVALUATION_PACKET = CAPABILITIES / "capability_source_evidence_evaluation_packet.json"
SOURCE_EVIDENCE_EVALUATION_GATE = CAPABILITIES / "capability_source_evidence_evaluation_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_source_evidence_evaluation_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_source_evidence_evaluation_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_SOURCE_EVIDENCE_EVALUATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_source_evidence_evaluation_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_source_evidence_fixture_template_v0_1"

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

REQUIRED_FILES = [
    RUNNER,
    OWNER_SUPPLIED_EVIDENCE_PACKET,
    OWNER_SUPPLIED_EVIDENCE_GATE,
    SOURCE_EVIDENCE_EVALUATION_PACKET,
    SOURCE_EVIDENCE_EVALUATION_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_EVALUATION_CATEGORIES = {
    "authenticity",
    "license",
    "security",
    "maintenance",
    "architecture_fit",
    "supply_chain_risk",
}

REQUIRED_EVIDENCE_EVALUATION_FIELDS = {
    "evidence_record_id",
    "source_slot_id",
    "candidate_id",
    "slot_type",
    "target_uri",
    "evaluation_status",
    "acceptance_decision",
    "rejection_reasons",
    "evaluation_criteria",
    "evidence_trusted",
    "evidence_verified",
    "accepted_for_integration",
    "claim_boundary",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_source_evidence_evaluation_packet_v0_1=true",
    "source_evidence_evaluation_packet_created=true",
    "source_evidence_evaluation_gate_created=true",
    "evaluation_criteria_created=true",
    "no_evidence_accepted_by_default=true",
    "integration_remains_blocked=true",
    "protected_action_executed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "provider_calls_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Source Evidence Evaluation Packet v0.1 validation")
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


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def flatten_owner_evidence_records(packet: dict) -> list[dict]:
    records = []
    for candidate in packet.get("candidate_owner_supplied_evidence_records", []):
        records.extend(candidate.get("owner_supplied_evidence_records", []))
    return records


def require_inputs() -> dict:
    packet = read_json(OWNER_SUPPLIED_EVIDENCE_PACKET)
    gate = read_json(OWNER_SUPPLIED_EVIDENCE_GATE)
    if packet.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("owner-supplied evidence packet must point to source evidence evaluation as next safe goal")
    if gate.get("gate_decision") != "BLOCKED_PENDING_SOURCE_EVIDENCE_EVALUATION":
        fail("owner-supplied evidence gate must remain blocked before source evidence evaluation")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("owner-supplied evidence gate must point to source evidence evaluation as next safe goal")
    return packet


def require_evaluation_record(record: dict) -> None:
    missing = sorted(REQUIRED_EVIDENCE_EVALUATION_FIELDS - set(record))
    if missing:
        fail(f"{record.get('evidence_record_id', '<unknown>')} missing evaluation fields:\n" + "\n".join(missing))
    if record.get("evaluation_status") != "blocked_missing_owner_supplied_evidence":
        fail(f"{record.get('evidence_record_id')} evaluation status must block missing owner evidence")
    if record.get("acceptance_decision") != "not_accepted":
        fail(f"{record.get('evidence_record_id')} must not be accepted")
    required_reasons = {
        "owner_supplied_evidence_uri_missing",
        "owner_supplied_excerpt_or_notes_missing",
        "source_snapshot_hash_missing",
        "reviewer_missing",
    }
    reasons = set(record.get("rejection_reasons", []))
    missing_reasons = sorted(required_reasons - reasons)
    if missing_reasons:
        fail(f"{record.get('evidence_record_id')} missing rejection reasons:\n" + "\n".join(missing_reasons))
    categories = {criterion.get("category") for criterion in record.get("evaluation_criteria", [])}
    missing_categories = sorted(REQUIRED_EVALUATION_CATEGORIES - categories)
    if missing_categories:
        fail(f"{record.get('evidence_record_id')} missing evaluation categories:\n" + "\n".join(missing_categories))
    for criterion in record.get("evaluation_criteria", []):
        if criterion.get("status") != "not_evaluable_without_owner_supplied_evidence":
            fail(f"{record.get('evidence_record_id')} criterion {criterion.get('category')} must be not evaluable")
        if criterion.get("passed") is not False:
            fail(f"{record.get('evidence_record_id')} criterion {criterion.get('category')} must not pass")
    if record.get("evidence_trusted") is not False:
        fail(f"{record.get('evidence_record_id')} evidence_trusted must be false")
    if record.get("evidence_verified") is not False:
        fail(f"{record.get('evidence_record_id')} evidence_verified must be false")
    if record.get("accepted_for_integration") is not False:
        fail(f"{record.get('evidence_record_id')} accepted_for_integration must be false")
    require_false_flags(record.get("claim_boundary", {}), f"{record.get('evidence_record_id')} claim boundary")


def require_evaluation_packet(owner_packet: dict) -> None:
    packet = read_json(SOURCE_EVIDENCE_EVALUATION_PACKET)
    if packet.get("status") != "PASS":
        fail("source evidence evaluation packet status must be PASS")
    if packet.get("goal_id") != THIS_GOAL_ID:
        fail("source evidence evaluation packet goal_id mismatch")
    if packet.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("source evidence evaluation packet next safe goal mismatch")
    if packet.get("evaluation_mode") != "criteria_only_owner_evidence_not_accepted_by_default":
        fail("source evidence evaluation mode mismatch")
    require_false_flags(packet.get("claim_boundary", {}), "source evidence evaluation packet claim boundary")

    owner_candidates = {
        record["candidate_id"]: record
        for record in owner_packet.get("candidate_owner_supplied_evidence_records", [])
    }
    evaluation_candidates = packet.get("candidate_evaluation_records", [])
    if {record.get("candidate_id") for record in evaluation_candidates} != set(owner_candidates):
        fail("source evidence evaluation candidates must match owner-supplied evidence packet")
    expected_evidence_count = len(flatten_owner_evidence_records(owner_packet))
    observed_evidence_count = sum(
        len(record.get("evidence_evaluation_records", []))
        for record in evaluation_candidates
    )
    if observed_evidence_count != expected_evidence_count:
        fail("source evidence evaluation record count must match owner-supplied evidence records")

    for candidate in evaluation_candidates:
        source_candidate = owner_candidates[candidate["candidate_id"]]
        source_count = len(source_candidate.get("owner_supplied_evidence_records", []))
        if candidate.get("candidate_evaluation_status") != "blocked_insufficient_owner_supplied_evidence":
            fail(f"{candidate.get('candidate_id')} evaluation status must remain blocked")
        if candidate.get("integration_decision") != "blocked":
            fail(f"{candidate.get('candidate_id')} integration decision must remain blocked")
        if candidate.get("accepted_evidence_count") != 0:
            fail(f"{candidate.get('candidate_id')} accepted evidence count must be zero")
        if candidate.get("pending_or_rejected_evidence_count") != source_count:
            fail(f"{candidate.get('candidate_id')} pending/rejected evidence count mismatch")
        require_false_flags(candidate.get("claim_boundary", {}), f"{candidate.get('candidate_id')} claim boundary")
        for record in candidate.get("evidence_evaluation_records", []):
            require_evaluation_record(record)

    contract = packet.get("evaluation_contract", {})
    if contract.get("accept_evidence_by_default") is not False:
        fail("accept_evidence_by_default must be false")
    if contract.get("allow_integration_without_all_required_categories_passing") is not False:
        fail("integration must require all evaluation categories to pass")
    if set(contract.get("required_categories", [])) != REQUIRED_EVALUATION_CATEGORIES:
        fail("evaluation contract required categories mismatch")


def require_evaluation_gate() -> None:
    gate = read_json(SOURCE_EVIDENCE_EVALUATION_GATE)
    if gate.get("status") != "PASS":
        fail("source evidence evaluation gate status must be PASS")
    if gate.get("gate_decision") != "BLOCKED_NO_ACCEPTED_SOURCE_EVIDENCE":
        fail("source evidence evaluation gate must block with no accepted evidence")
    if gate.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("source evidence evaluation gate next safe goal mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "source evidence evaluation gate")
    required_blockers = {
        "no_accepted_owner_supplied_source_evidence",
        "authenticity_not_passed",
        "license_not_passed",
        "security_not_passed",
        "maintenance_not_passed",
        "architecture_fit_not_passed",
        "supply_chain_risk_not_passed",
        "integration_not_approved",
    }
    blockers = set(gate.get("blocking_requirements", []))
    missing = sorted(required_blockers - blockers)
    if missing:
        fail("source evidence evaluation gate missing blockers:\n" + "\n".join(missing))


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("source evidence evaluation validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("source evidence evaluation validation next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "source evidence evaluation validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    owner_packet = require_inputs()
    require_evaluation_packet(owner_packet)
    require_evaluation_gate()
    require_validation_result()
    require_markers(NEXT_CODEX_TASK, ["task_id: avf-capability-source-evidence-fixture-template-v0-1", "forbidden_changes:", "validation_commands:", f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}"])
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Source Evidence Evaluation Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_source_evidence_evaluation_packet_v0_1=true")
    print("source_evidence_evaluation_packet_created=true")
    print("source_evidence_evaluation_gate_created=true")
    print("evaluation_criteria_created=true")
    print("no_evidence_accepted_by_default=true")
    print("integration_remains_blocked=true")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("provider_calls_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
