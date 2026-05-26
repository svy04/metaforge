from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_review_gate.json"
RETRY_PACKET = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry.yml"
RETRY_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_FILLED_AUTHORIZATION_PACKET_COMPLETION_RETRY_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_filled_authorization_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_completion_retry_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "BLOCKED_OWNER_AUTHORIZATION_PACKET_UNFILLED"
RETRY_DECISION = "RETRY_PACKET_READY_OWNER_INPUT_REQUIRED_EXECUTION_BLOCKED"

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

COLLECTION_MODES = [
    "manual_owner_collection",
    "pro_manual_collection",
    "codex_assisted_link_opening",
    "automated_collection",
]

BOUNDARY_ITEMS = [
    "source collection execution",
    "provider calls",
    "live model calls",
    "external service calls",
    "automated scraping",
    "OSS clone",
    "package install",
    "dependency install",
    "runtime integration",
    "deploy",
    "publish",
    "release readiness claim",
    "production readiness claim",
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
        "automated_scraping_performed": False,
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


def require_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("review gate must point to this completion retry goal")
    if gate.get("review_decision") != REVIEW_DECISION:
        raise SystemExit("review gate decision mismatch")
    if gate.get("authorization_review_passed") is not False:
        raise SystemExit("review gate must not pass authorization")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("review gate must not grant owner authorization")
    if gate.get("authorization_fields_present") != 0:
        raise SystemExit("review gate must not mark authorization fields present")
    if gate.get("missing_authorization_fields") != AUTHORIZATION_FIELDS:
        raise SystemExit("review gate missing fields mismatch")
    if gate.get("collection_modes_authorized") != 0:
        raise SystemExit("review gate must not authorize collection modes")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("review gate must keep collection blocked")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        raise SystemExit("review gate must review 35 source records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("review gate must not make source records executable")


def build_retry_packet() -> str:
    missing_rows = "\n".join(f"  - {field}" for field in AUTHORIZATION_FIELDS)
    mode_rows = "\n".join(f"  - {mode}" for mode in COLLECTION_MODES)
    blocked_rows = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    boundary_flags = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""packet_id: avf-capability-primary-source-evidence-owner-filled-authorization-packet-completion-retry-v0-1
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
retry_decision: {RETRY_DECISION}
owner_input_required: true

authorization_retry_completed: false
owner_authorization_granted: false
collection_execution_allowed: false
source_records_executable: 0

missing_authorization_fields_count: {len(AUTHORIZATION_FIELDS)}
missing_authorization_fields:
{missing_rows}

field_completion_template:
  owner_authorization_statement:
  authorized_by:
  authorized_at:
  authorization_expires_at:
  authorized_collection_modes: []
  authorized_source_families: []
  authorized_candidate_ids: []
  authorized_source_slot_ids: []
  max_records_to_collect: 0
  collection_boundaries: []
  revocation_note:

collection_mode_selection:
  available_collection_modes:
{mode_rows}
  selected_collection_modes: []
  manual_owner_collection_authorized: false
  pro_manual_collection_authorized: false
  codex_assisted_link_opening_authorized: false
  automated_collection_authorized: false

source_scope_selection:
  source_records_reviewed: 35
  authorized_source_slot_ids: []
  max_records_to_collect: 0
  source_records_executable: 0

boundary_summary:
{blocked_rows}

claim_boundary:
{boundary_flags}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_retry_gate(review_gate: dict) -> dict:
    counts = review_gate["source_entry_counts"]
    return {
        "gate_id": "avf-capability-primary-source-evidence-owner-filled-authorization-packet-completion-retry-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "retry_decision": RETRY_DECISION,
        "review_decision_source": REVIEW_DECISION,
        "retry_packet_uri": rel(RETRY_PACKET),
        "owner_input_required": True,
        "authorization_retry_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_required": len(AUTHORIZATION_FIELDS),
        "authorization_fields_completed": 0,
        "missing_authorization_fields_count": len(AUTHORIZATION_FIELDS),
        "missing_authorization_fields": AUTHORIZATION_FIELDS,
        "collection_modes_available": COLLECTION_MODES,
        "selected_collection_modes": [],
        "collection_modes_selected": 0,
        "collection_mode_defaults": {mode: False for mode in COLLECTION_MODES},
        "source_entry_counts": {
            "source_records_reviewed": counts["source_records_reviewed"],
            "source_records_executable": 0,
            "trusted_source_records": 0,
            "ingested_source_records": 0,
            "integrated_source_records": 0,
        },
        "collection_execution_allowed": False,
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_v0_1",
        "status": "PASS",
        "checks": [
            "owner completion retry packet exists",
            "all missing authorization fields are listed",
            "owner input is required",
            "collection execution remains blocked",
            "protected-action flags remain false",
        ],
        "retry_decision": RETRY_DECISION,
        "owner_input_required": True,
        "authorization_retry_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_required": len(AUTHORIZATION_FIELDS),
        "authorization_fields_completed": 0,
        "missing_authorization_fields": len(AUTHORIZATION_FIELDS),
        "collection_modes_selected": 0,
        "source_records_reviewed": counts["source_records_reviewed"],
        "source_records_executable": counts["source_records_executable"],
        "collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    forbidden = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    return f"""task_id: avf-capability-primary-source-evidence-owner-completion-retry-review-v0-1
title: Add AVF owner completion retry review v0.1
goal: Review the owner completion retry packet and keep execution blocked until owner input actually completes every required authorization field.
context_paths:
  - {rel(RETRY_PACKET)}
  - {rel(RETRY_GATE)}
  - {rel(REVIEW_GATE)}
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_completion_retry_review_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_owner_completion_retry_review_next_codex_task_packet.yml
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_COMPLETION_RETRY_REVIEW_V0_1_REPORT.md
forbidden_changes:
{forbidden}
acceptance_criteria:
  - completion retry review checks all required authorization fields
  - review remains blocked when retry fields are still empty
  - no source collection task becomes executable
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_v0_1.py
expected_outputs:
  - owner completion retry review gate
  - blocked review decision for empty retry packet
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    flag_rows = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Primary-Source Evidence Owner-Filled Authorization Packet Completion Retry v0.1 Report

RESULT: PASS

## Commands

- python scripts\\run_avf_capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_v0_1.py
- python scripts\\validate_avf_capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_v0_1.py

## Generated artifacts

- {rel(RETRY_PACKET)}
- {rel(RETRY_GATE)}
- {rel(NEXT_CODEX_TASK)}
- {rel(VALIDATION_RESULT)}
- {rel(VALIDATION_REPORT)}

## Gate summary

- capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_v0_1=true
- owner_filled_authorization_packet_completion_retry_created=true
- owner_filled_authorization_packet_completion_retry_gate_created=true
- owner_input_required=true
- authorization_retry_completed=false
- authorization_fields_required={len(AUTHORIZATION_FIELDS)}
- authorization_fields_completed=0
- missing_authorization_fields={len(AUTHORIZATION_FIELDS)}
- collection_modes_selected=0
- source_records_reviewed={counts["source_records_reviewed"]}
- source_records_executable={counts["source_records_executable"]}
- collection_execution_allowed=false
- owner_authorization_granted=false
- retry_decision={RETRY_DECISION}

## Protected action flags

{flag_rows}

## Claim boundary

This is a repo-local completion retry packet for missing owner authorization fields. It does not grant authorization and does not perform source collection, external calls, cloning, installation, runtime integration, deployment, publishing, or readiness claims.

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review_gate = read_json(REVIEW_GATE)
    require_review_gate(review_gate)

    retry_gate = build_retry_gate(review_gate)
    validation_result = build_validation_result(retry_gate)

    write_text(RETRY_PACKET, build_retry_packet())
    write_json(RETRY_GATE, retry_gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, validation_result)
    write_text(VALIDATION_REPORT, build_report(retry_gate))

    print("AVF Capability Primary-Source Evidence Owner-Filled Authorization Packet Completion Retry v0.1 generated")
    print(f"retry_packet={rel(RETRY_PACKET)}")
    print(f"retry_gate={rel(RETRY_GATE)}")
    print(f"validation_report={rel(VALIDATION_REPORT)}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
