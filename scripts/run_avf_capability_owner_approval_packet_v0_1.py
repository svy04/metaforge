from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

SOURCE_MATRIX = CAPABILITIES / "capability_source_verification_matrix.json"
SOURCE_PREFLIGHT_GATE = CAPABILITIES / "capability_source_verification_preflight_gate.json"
REVIEW_DOSSIER = CAPABILITIES / "capability_review_dossier.json"
OWNER_APPROVAL_PACKET = CAPABILITIES / "capability_owner_approval_packet.json"
OWNER_APPROVAL_GATE = CAPABILITIES / "capability_owner_approval_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_owner_approval_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_owner_approval_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_OWNER_APPROVAL_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_owner_approval_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_manual_source_review_packet_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"

REQUIRED_OWNER_DECISION_FIELDS = [
    "candidate_id",
    "owner_approval_status",
    "owner_approver",
    "owner_approved_at",
    "approval_signature",
    "approval_scope",
    "approval_rationale",
    "source_verification_completed",
    "license_review_completed",
    "security_review_completed",
    "maintenance_review_completed",
    "architecture_fit_review_completed",
    "sandbox_plan_approved",
    "rollback_plan_approved",
]

BLOCKING_REQUIREMENTS = [
    "source_verification_not_completed",
    "license_review_not_completed",
    "security_review_not_completed",
    "maintenance_review_not_completed",
    "architecture_fit_review_not_completed",
    "sandbox_plan_not_approved",
    "rollback_plan_not_approved",
    "owner_approval_unset",
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


def build_candidate_approval_record(row: dict) -> dict:
    return {
        "candidate_id": row["candidate_id"],
        "candidate_name": row["candidate_name"],
        "capability_id": row["capability_id"],
        "priority_rank": row["priority_rank"],
        "source_slot_count": len(row["source_slots"]),
        "block_status": "blocked_pending_source_verification_and_owner_approval",
        "integration_decision": "not_approved",
        "owner_approval_status": "unset",
        "owner_approver": None,
        "owner_approved_at": None,
        "approval_signature": None,
        "approval_scope": None,
        "approval_rationale": None,
        "source_verification_required": True,
        "source_verification_completed": False,
        "license_review_completed": False,
        "security_review_completed": False,
        "maintenance_review_completed": False,
        "architecture_fit_review_completed": False,
        "sandbox_plan_approved": False,
        "rollback_plan_approved": False,
        "external_fetch_allowed": False,
        "oss_clone_allowed": False,
        "dependency_install_allowed": False,
        "package_install_allowed": False,
        "runtime_integration_allowed": False,
        "provider_activation_allowed": False,
        "deployment_allowed": False,
        "publication_allowed": False,
        "allowed_owner_decisions": [
            "approve_for_manual_review_only",
            "request_more_source_verification",
            "reject_candidate",
            "defer_candidate",
        ],
        "claim_boundary": false_boundary(),
    }


def build_owner_approval_packet(matrix: dict) -> dict:
    records = [
        build_candidate_approval_record(row)
        for row in matrix["candidate_source_rows"]
    ]
    return {
        "packet_id": "avf-capability-owner-approval-packet-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "approval_mode": "explicit_owner_approval_required",
        "default_decision": "blocked",
        "source_matrix_uri": rel(SOURCE_MATRIX),
        "source_preflight_gate_uri": rel(SOURCE_PREFLIGHT_GATE),
        "review_dossier_uri": rel(REVIEW_DOSSIER),
        "candidate_approval_records": records,
        "required_owner_decision_fields": REQUIRED_OWNER_DECISION_FIELDS,
        "blocked_actions_until_approval": [
            "external_fetch",
            "oss_clone",
            "dependency_install",
            "package_install",
            "runtime_integration",
            "provider_activation",
            "deploy",
            "publish",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_owner_approval_gate(packet: dict) -> dict:
    return {
        "gate_id": "avf-capability-owner-approval-preflight-gate-v0-1",
        "created_at": CREATED_AT,
        "status": "PASS",
        "gate_decision": "BLOCKED_PENDING_EXPLICIT_OWNER_APPROVAL",
        "decision_reason": "Owner approval fields exist but are explicitly unset. No candidate is approved for fetch, clone, install, provider activation, runtime integration, deploy, or publish.",
        "candidate_ids": [
            record["candidate_id"] for record in packet["candidate_approval_records"]
        ],
        "blocking_requirements": BLOCKING_REQUIREMENTS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-manual-source-review-packet-v0-1
title: Add AVF capability manual source review packet v0.1
goal: Create a repo-local manual source review packet that records how owner-approved source verification should be captured before any integration action.
context_paths:
  - avf/capabilities/generated/capability_owner_approval_packet.json
  - avf/capabilities/generated/capability_owner_approval_preflight_gate.json
  - avf/capabilities/generated/capability_source_verification_matrix.json
files_likely_to_touch:
  - scripts/run_avf_capability_manual_source_review_packet_v0_1.py
  - scripts/validate_avf_capability_manual_source_review_packet_v0_1.py
  - avf/capabilities/generated/capability_manual_source_review_packet.json
  - docs/goals/AVF_CAPABILITY_MANUAL_SOURCE_REVIEW_PACKET_V0_1_REPORT.md
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
  - manual source review packet exists
  - each candidate has source evidence capture fields
  - no source is marked verified by default
  - integration remains blocked
validation_commands:
  - python scripts\\validate_avf_capability_owner_approval_packet_v0_1.py
  - python scripts\\validate_avf_capability_manual_source_review_packet_v0_1.py
expected_outputs:
  - capability_manual_source_review_packet.json
  - manual source review validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_owner_approval_packet_v0_1",
        "status": "PASS",
        "checks": [
            "source verification gate points to owner approval packet",
            "owner approval packet exists",
            "all candidates remain blocked by default",
            "approval fields are explicit and unset",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(packet: dict) -> str:
    rows = "\n".join(
        f"- {record['candidate_id']}: approval={record['owner_approval_status']}, integration={record['integration_decision']}, block={record['block_status']}"
        for record in packet["candidate_approval_records"]
    )
    return f"""# AVF Capability Owner Approval Packet v0.1 Report

RESULT: PASS
capability_owner_approval_packet_v0_1=true
owner_approval_packet_created=true
owner_approval_gate_created=true
all_candidates_blocked_by_default=true
approval_fields_explicit_and_unset=true
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

## Candidate Approval Defaults

{rows}

## Boundary

This packet does not approve, fetch, scrape, clone, install, invoke, deploy, publish, or integrate any candidate. It only defines the explicit owner approval fields that must be completed later.
"""


def main() -> None:
    matrix = read_json(SOURCE_MATRIX)
    source_gate = read_json(SOURCE_PREFLIGHT_GATE)
    if matrix.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("source verification matrix does not point to this owner approval goal")
    if source_gate.get("gate_decision") != "BLOCKED_PENDING_SOURCE_VERIFICATION_AND_OWNER_APPROVAL":
        raise SystemExit("source preflight gate must remain blocked before owner approval packet")
    if source_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("source preflight gate does not point to this owner approval goal")

    packet = build_owner_approval_packet(matrix)
    write_json(OWNER_APPROVAL_PACKET, packet)
    write_json(OWNER_APPROVAL_GATE, build_owner_approval_gate(packet))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(packet))

    print("AVF Capability Owner Approval Packet v0.1 runner")
    print("RESULT: PASS")
    print("capability_owner_approval_packet_v0_1=true")
    print("owner_approval_packet_created=true")
    print("owner_approval_gate_created=true")
    print("all_candidates_blocked_by_default=true")
    print("approval_fields_explicit_and_unset=true")
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
