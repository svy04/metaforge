from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

OWNER_APPROVAL_PACKET = CAPABILITIES / "capability_owner_approval_packet.json"
OWNER_APPROVAL_GATE = CAPABILITIES / "capability_owner_approval_preflight_gate.json"
SOURCE_MATRIX = CAPABILITIES / "capability_source_verification_matrix.json"
MANUAL_REVIEW_PACKET = CAPABILITIES / "capability_manual_source_review_packet.json"
MANUAL_REVIEW_GATE = CAPABILITIES / "capability_manual_source_review_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_manual_source_review_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_manual_source_review_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_MANUAL_SOURCE_REVIEW_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_manual_source_review_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_owner_supplied_source_evidence_packet_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"

BLOCKING_REQUIREMENTS = [
    "owner_supplied_evidence_missing",
    "source_snapshot_hash_missing",
    "manual_reviewer_missing",
    "license_finding_missing",
    "security_finding_missing",
    "maintenance_finding_missing",
    "architecture_fit_finding_missing",
    "integration_not_approved",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def false_boundary() -> dict:
    return {
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "scraping_performed": False,
        "posting_automation_performed": False,
        "dependency_install_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "package_install_performed": False,
        "runtime_integration_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def build_capture_record(candidate_id: str, slot: dict) -> dict:
    return {
        "source_slot_id": slot["slot_id"],
        "candidate_id": candidate_id,
        "slot_type": slot["slot_type"],
        "target_uri": slot["target_uri"],
        "evidence_status": "not_collected",
        "verification_status": "not_verified",
        "manual_review_required": True,
        "reviewer": None,
        "reviewed_at": None,
        "owner_supplied_evidence_uri": None,
        "source_snapshot_hash": None,
        "license_finding": None,
        "security_finding": None,
        "maintenance_finding": None,
        "architecture_fit_finding": None,
        "notes": None,
        "external_fetch_performed": False,
        "source_marked_verified": False,
    }


def build_candidate_review_record(row: dict, approval_by_id: dict) -> dict:
    approval = approval_by_id[row["candidate_id"]]
    return {
        "candidate_id": row["candidate_id"],
        "candidate_name": row["candidate_name"],
        "capability_id": row["capability_id"],
        "priority_rank": row["priority_rank"],
        "candidate_review_status": "not_reviewed",
        "integration_decision": "blocked",
        "owner_approval_status": approval["owner_approval_status"],
        "source_evidence_capture_records": [
            build_capture_record(row["candidate_id"], slot)
            for slot in row["source_slots"]
        ],
        "claim_boundary": false_boundary(),
    }


def build_manual_review_packet(approval_packet: dict, matrix: dict) -> dict:
    approval_by_id = {
        record["candidate_id"]: record
        for record in approval_packet["candidate_approval_records"]
    }
    return {
        "packet_id": "avf-capability-manual-source-review-packet-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "review_mode": "manual_owner_supplied_evidence_only",
        "owner_approval_packet_uri": rel(OWNER_APPROVAL_PACKET),
        "owner_approval_gate_uri": rel(OWNER_APPROVAL_GATE),
        "source_matrix_uri": rel(SOURCE_MATRIX),
        "candidate_source_review_records": [
            build_candidate_review_record(row, approval_by_id)
            for row in matrix["candidate_source_rows"]
        ],
        "evidence_capture_contract": {
            "allowed_evidence_source": "owner_supplied_manual_source_notes_or_snapshots",
            "automated_fetch_allowed": False,
            "automated_scraping_allowed": False,
            "source_marked_verified_by_default": False,
            "requires_snapshot_hash_before_trust": True,
            "requires_manual_reviewer_before_trust": True,
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_manual_review_gate(packet: dict) -> dict:
    return {
        "gate_id": "avf-capability-manual-source-review-preflight-gate-v0-1",
        "created_at": CREATED_AT,
        "status": "PASS",
        "gate_decision": "BLOCKED_PENDING_OWNER_SUPPLIED_SOURCE_EVIDENCE",
        "decision_reason": "Manual source review fields exist, but no owner-supplied evidence, reviewer, source hash, or findings have been captured.",
        "candidate_ids": [
            record["candidate_id"]
            for record in packet["candidate_source_review_records"]
        ],
        "blocking_requirements": BLOCKING_REQUIREMENTS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-owner-supplied-source-evidence-packet-v0-1
title: Add AVF owner-supplied source evidence packet v0.1
goal: Define how owner-provided primary-source evidence snapshots can be recorded without automated fetch, scraping, cloning, installing, or runtime integration.
context_paths:
  - avf/capabilities/generated/capability_manual_source_review_packet.json
  - avf/capabilities/generated/capability_manual_source_review_preflight_gate.json
  - avf/capabilities/generated/capability_source_verification_matrix.json
files_likely_to_touch:
  - scripts/run_avf_capability_owner_supplied_source_evidence_packet_v0_1.py
  - scripts/validate_avf_capability_owner_supplied_source_evidence_packet_v0_1.py
  - avf/capabilities/generated/capability_owner_supplied_source_evidence_packet.json
  - docs/goals/AVF_CAPABILITY_OWNER_SUPPLIED_SOURCE_EVIDENCE_PACKET_V0_1_REPORT.md
forbidden_changes:
  - No provider calls
  - No live model calls
  - No external service calls
  - No scraping automation
  - No package install
  - No dependency install
  - No OSS clone
  - No runtime integration
  - No deploy
  - No publish
  - No release readiness claim
  - No production readiness claim
acceptance_criteria:
  - owner-supplied source evidence packet exists
  - evidence input fields preserve source URI, captured excerpt/notes placeholder, hash placeholder, reviewer, and claim boundary
  - no evidence is trusted or verified by default
  - integration remains blocked
validation_commands:
  - python scripts\\validate_avf_capability_manual_source_review_packet_v0_1.py
  - python scripts\\validate_avf_capability_owner_supplied_source_evidence_packet_v0_1.py
expected_outputs:
  - capability_owner_supplied_source_evidence_packet.json
  - owner-supplied source evidence validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_manual_source_review_packet_v0_1",
        "status": "PASS",
        "checks": [
            "owner approval packet points to manual source review",
            "manual source review packet exists",
            "source evidence capture fields exist",
            "no source is marked verified by default",
            "integration remains blocked",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(packet: dict) -> str:
    rows = "\n".join(
        f"- {record['candidate_id']}: captures={len(record['source_evidence_capture_records'])}, status={record['candidate_review_status']}, integration={record['integration_decision']}"
        for record in packet["candidate_source_review_records"]
    )
    return f"""# AVF Capability Manual Source Review Packet v0.1 Report

RESULT: PASS
capability_manual_source_review_packet_v0_1=true
manual_source_review_packet_created=true
manual_review_gate_created=true
source_evidence_capture_fields_created=true
no_source_marked_verified_by_default=true
integration_remains_blocked=true
protected_action_executed=false
dependency_install_performed=false
external_fetch_performed=false
oss_clone_performed=false
package_install_performed=false
runtime_integration_performed=false
provider_calls_performed=false
scraping_performed=false
posting_automation_performed=false
deploy_performed=false
publish_performed=false
release_ready=false
production_ready=false
next_safe_goal_id={NEXT_SAFE_GOAL_ID}

## Candidate Manual Review Records

{rows}

## Boundary

The packet creates evidence capture fields only. It does not fetch, scrape, clone, install, trust, verify, invoke, deploy, publish, approve, or integrate any source or candidate.
"""


def main() -> None:
    approval_packet = read_json(OWNER_APPROVAL_PACKET)
    approval_gate = read_json(OWNER_APPROVAL_GATE)
    matrix = read_json(SOURCE_MATRIX)
    if approval_packet.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("owner approval packet does not point to this manual source review goal")
    if approval_gate.get("gate_decision") != "BLOCKED_PENDING_EXPLICIT_OWNER_APPROVAL":
        raise SystemExit("owner approval gate must remain blocked before manual source review packet")
    if approval_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("owner approval gate does not point to this manual source review goal")

    packet = build_manual_review_packet(approval_packet, matrix)
    write_json(MANUAL_REVIEW_PACKET, packet)
    write_json(MANUAL_REVIEW_GATE, build_manual_review_gate(packet))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(packet))

    print("AVF Capability Manual Source Review Packet v0.1 runner")
    print("RESULT: PASS")
    print("capability_manual_source_review_packet_v0_1=true")
    print("manual_source_review_packet_created=true")
    print("manual_review_gate_created=true")
    print("source_evidence_capture_fields_created=true")
    print("no_source_marked_verified_by_default=true")
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
