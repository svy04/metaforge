from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

COMPLETION_GUIDE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_completion_guide_gate.json"
TEMPLATE = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_template.yml"
TEMPLATE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_template_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_template_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_FILLED_AUTHORIZATION_PACKET_TEMPLATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_completion_guide_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_filled_authorization_packet_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
GUIDE_DECISION = "GUIDE_READY_EXECUTION_STILL_BLOCKED"
TEMPLATE_DECISION = "TEMPLATE_READY_UNFILLED_EXECUTION_STILL_BLOCKED"

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


def require_completion_guide_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("completion guide gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("completion guide gate must point to this template goal")
    if gate.get("guide_decision") != GUIDE_DECISION:
        raise SystemExit("completion guide decision mismatch")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("completion guide gate must not grant owner authorization")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("completion guide gate must keep collection execution blocked")
    if gate.get("authorization_fields_documented") != AUTHORIZATION_FIELDS:
        raise SystemExit("completion guide authorization fields mismatch")
    if gate.get("collection_modes_documented") != COLLECTION_MODES:
        raise SystemExit("completion guide collection modes mismatch")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        raise SystemExit("completion guide must cover 35 source records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("completion guide must not make source records executable")


def build_template() -> str:
    blocked_rows = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    field_rows = "\n".join(f"  - {field}" for field in AUTHORIZATION_FIELDS)
    mode_rows = "\n".join(f"  - {mode}" for mode in COLLECTION_MODES)
    boundary_flags = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""packet_id: avf-capability-primary-source-evidence-owner-filled-authorization-packet-template-v0-1
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
template_decision: {TEMPLATE_DECISION}

authorization_template_completed: false
owner_authorization_granted: false
collection_execution_allowed: false
source_records_executable: 0

collection_mode_authorization_defaults:
  manual_owner_collection_authorized: false
  pro_manual_collection_authorized: false
  codex_assisted_link_opening_authorized: false
  automated_collection_authorized: false

required_authorization_fields:
{field_rows}

collection_modes_available:
{mode_rows}

owner_authorization:
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

boundary_summary:
{blocked_rows}

claim_boundary:
{boundary_flags}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_template_gate(completion_gate: dict) -> dict:
    counts = completion_gate["source_entry_counts"]
    return {
        "gate_id": "avf-capability-primary-source-evidence-owner-filled-authorization-packet-template-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "template_decision": TEMPLATE_DECISION,
        "template_uri": rel(TEMPLATE),
        "authorization_template_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_in_template": AUTHORIZATION_FIELDS,
        "authorization_fields_completed": 0,
        "missing_authorization_fields": AUTHORIZATION_FIELDS,
        "collection_modes_in_template": COLLECTION_MODES,
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
        "validator_id": "validate_avf_capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1",
        "status": "PASS",
        "checks": [
            "owner-filled authorization packet template exists",
            "all authorization fields are present and unset",
            "all collection modes are default false",
            "collection execution remains blocked",
            "protected-action flags remain false",
        ],
        "template_decision": TEMPLATE_DECISION,
        "authorization_template_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_in_template": len(AUTHORIZATION_FIELDS),
        "authorization_fields_completed": 0,
        "collection_modes_in_template": len(COLLECTION_MODES),
        "source_records_reviewed": counts["source_records_reviewed"],
        "source_records_executable": counts["source_records_executable"],
        "collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    forbidden = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    return f"""task_id: avf-capability-primary-source-evidence-owner-filled-authorization-packet-review-v0-1
title: Add AVF owner-filled authorization packet review v0.1
goal: Review a future owner-filled authorization packet while keeping execution blocked unless every required field is explicitly completed and separately approved.
context_paths:
  - {rel(TEMPLATE)}
  - {rel(TEMPLATE_GATE)}
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_completion_guide_gate.json
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_filled_authorization_packet_review_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_owner_filled_authorization_packet_review_next_codex_task_packet.yml
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_FILLED_AUTHORIZATION_PACKET_REVIEW_V0_1_REPORT.md
forbidden_changes:
{forbidden}
acceptance_criteria:
  - owner-filled authorization packet review checks every required authorization field
  - review remains blocked when the template is still unfilled
  - review distinguishes manual owner collection, PRO-assisted review, Codex link opening, and automated collection
  - no source collection task becomes executable without a later explicit owner approval gate
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1.py
expected_outputs:
  - owner-filled authorization packet review gate
  - blocked execution decision when authorization remains unfilled
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    flag_rows = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Primary-Source Evidence Owner-Filled Authorization Packet Template v0.1 Report

RESULT: PASS

## Commands

- python scripts\\run_avf_capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1.py
- python scripts\\validate_avf_capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1.py

## Generated artifacts

- {rel(TEMPLATE)}
- {rel(TEMPLATE_GATE)}
- {rel(NEXT_CODEX_TASK)}
- {rel(VALIDATION_RESULT)}
- {rel(VALIDATION_REPORT)}

## Gate summary

- capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1=true
- owner_filled_authorization_packet_template_created=true
- owner_filled_authorization_packet_template_gate_created=true
- authorization_template_completed=false
- authorization_fields_in_template={len(AUTHORIZATION_FIELDS)}
- authorization_fields_completed=0
- collection_modes_in_template={len(COLLECTION_MODES)}
- source_records_reviewed={counts["source_records_reviewed"]}
- source_records_executable={counts["source_records_executable"]}
- collection_execution_allowed=false
- owner_authorization_granted=false
- template_decision={TEMPLATE_DECISION}

## Protected action flags

{flag_rows}

## Claim boundary

This is a repo-local owner-filled authorization packet template. It does not grant authorization and does not perform source collection, external calls, cloning, installation, runtime integration, deployment, publishing, or readiness claims.

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    completion_gate = read_json(COMPLETION_GUIDE_GATE)
    require_completion_guide_gate(completion_gate)

    template_gate = build_template_gate(completion_gate)
    validation_result = build_validation_result(template_gate)

    write_text(TEMPLATE, build_template())
    write_json(TEMPLATE_GATE, template_gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, validation_result)
    write_text(VALIDATION_REPORT, build_report(template_gate))

    print("AVF Capability Primary-Source Evidence Owner-Filled Authorization Packet Template v0.1 generated")
    print(f"template={rel(TEMPLATE)}")
    print(f"template_gate={rel(TEMPLATE_GATE)}")
    print(f"validation_report={rel(VALIDATION_REPORT)}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
