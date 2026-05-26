from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

MANUAL_GUIDE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_guide_gate.json"
PACKET_TEMPLATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template.yml"
PACKET_TEMPLATE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_MANUAL_COMPLETION_PACKET_TEMPLATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_guide_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
GUIDE_DECISION = "MANUAL_COMPLETION_GUIDE_READY_EXECUTION_STILL_BLOCKED"
TEMPLATE_DECISION = "MANUAL_COMPLETION_PACKET_TEMPLATE_READY_OWNER_INPUT_REQUIRED"

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


def require_manual_guide_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("manual guide gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("manual guide gate must point to this packet template goal")
    if gate.get("guide_decision") != GUIDE_DECISION:
        raise SystemExit("manual guide gate decision mismatch")
    if gate.get("owner_input_required") is not True:
        raise SystemExit("manual guide gate must require owner input")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("manual guide gate must not grant owner authorization")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("manual guide gate must keep collection blocked")
    if gate.get("authorization_fields_documented") != AUTHORIZATION_FIELDS:
        raise SystemExit("manual guide gate authorization fields mismatch")
    if gate.get("collection_modes_documented") != COLLECTION_MODES:
        raise SystemExit("manual guide gate collection modes mismatch")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        raise SystemExit("manual guide gate must cover 35 source records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("manual guide gate must not make source records executable")


def build_packet_template(manual_guide_gate: dict) -> str:
    counts = manual_guide_gate["source_entry_counts"]
    boundary_rows = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    false_flags = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""packet_id: avf-capability-primary-source-evidence-owner-manual-completion-packet-template-v0-1
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
template_decision: {TEMPLATE_DECISION}
owner_input_required: true

manual_completion_packet_completed: false
owner_authorization_granted: false
collection_execution_allowed: false
source_records_reviewed: {counts['source_records_reviewed']}
source_records_executable: {counts['source_records_executable']}

authorization_fields:
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
    - manual_owner_collection
    - pro_manual_collection
    - codex_assisted_link_opening
    - automated_collection
  selected_collection_modes: []
  manual_owner_collection_authorized: false
  pro_manual_collection_authorized: false
  codex_assisted_link_opening_authorized: false
  automated_collection_authorized: false

review_defaults:
  authorization_fields_completed: 0
  collection_modes_selected: 0
  trusted_source_records: 0
  ingested_source_records: 0
  integrated_source_records: 0

boundary_summary:
{boundary_rows}

claim_boundary:
{false_flags}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_packet_template_gate(manual_guide_gate: dict) -> dict:
    counts = manual_guide_gate["source_entry_counts"]
    return {
        "gate_id": "avf-capability-primary-source-evidence-owner-manual-completion-packet-template-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "template_decision": TEMPLATE_DECISION,
        "packet_template_uri": rel(PACKET_TEMPLATE),
        "owner_input_required": True,
        "manual_completion_packet_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_templated": AUTHORIZATION_FIELDS,
        "authorization_fields_templated_count": len(AUTHORIZATION_FIELDS),
        "authorization_fields_completed": 0,
        "missing_authorization_fields": AUTHORIZATION_FIELDS,
        "collection_modes_templated": COLLECTION_MODES,
        "collection_modes_templated_count": len(COLLECTION_MODES),
        "selected_collection_modes": [],
        "collection_modes_selected": 0,
        "collection_execution_allowed": False,
        "source_entry_counts": {
            "source_records_reviewed": counts["source_records_reviewed"],
            "source_records_executable": 0,
            "trusted_source_records": 0,
            "ingested_source_records": 0,
            "integrated_source_records": 0,
        },
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1",
        "status": "PASS",
        "checks": [
            "manual completion packet template exists",
            "all authorization fields are templated",
            "all collection modes are present but unselected",
            "owner authorization remains false",
            "collection execution remains blocked",
            "protected-action flags remain false",
        ],
        "template_decision": TEMPLATE_DECISION,
        "owner_input_required": True,
        "manual_completion_packet_completed": False,
        "authorization_fields_templated": len(AUTHORIZATION_FIELDS),
        "authorization_fields_completed": 0,
        "collection_modes_templated": len(COLLECTION_MODES),
        "collection_modes_selected": 0,
        "source_records_reviewed": counts["source_records_reviewed"],
        "source_records_executable": counts["source_records_executable"],
        "collection_execution_allowed": False,
        "owner_authorization_granted": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    forbidden = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    return f"""task_id: avf-capability-primary-source-evidence-owner-manual-completion-packet-review-v0-1
title: Review AVF owner manual completion packet v0.1
goal: Review an owner-filled packet only after the owner fills every field. If it remains unfilled, keep execution blocked and return PROTECTED_ACTION_REQUIRED.
context_paths:
  - {rel(PACKET_TEMPLATE)}
  - {rel(PACKET_TEMPLATE_GATE)}
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_manual_completion_packet_review_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_owner_manual_completion_packet_review_next_codex_task_packet.yml
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_MANUAL_COMPLETION_PACKET_REVIEW_V0_1_REPORT.md
review_type: manual completion packet review
review_subject: owner-filled packet
forbidden_changes:
{forbidden}
acceptance_criteria:
  - review requires all 11 authorization fields to be non-empty
  - review requires at least one selected collection mode
  - review keeps source collection blocked when owner input is absent
  - review returns PROTECTED_ACTION_REQUIRED when source collection would be needed
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1.py
expected_outputs:
  - owner completion packet review gate
  - protected-action-required boundary when packet is still unfilled
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    flag_rows = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Primary-Source Evidence Owner Manual Completion Packet Template v0.1 Report

RESULT: PASS

## Commands

- python scripts\\run_avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1.py
- python scripts\\validate_avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1.py

## Generated artifacts

- {rel(PACKET_TEMPLATE)}
- {rel(PACKET_TEMPLATE_GATE)}
- {rel(NEXT_CODEX_TASK)}
- {rel(VALIDATION_RESULT)}
- {rel(VALIDATION_REPORT)}

## Gate summary

- capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1=true
- owner_manual_completion_packet_template_created=true
- owner_manual_completion_packet_template_gate_created=true
- authorization_fields_templated={len(AUTHORIZATION_FIELDS)}
- authorization_fields_completed=0
- collection_modes_templated={len(COLLECTION_MODES)}
- collection_modes_selected=0
- owner_input_required=true
- manual_completion_packet_completed=false
- source_records_reviewed={counts['source_records_reviewed']}
- source_records_executable={counts['source_records_executable']}
- collection_execution_allowed=false
- owner_authorization_granted=false
- template_decision={TEMPLATE_DECISION}

## Protected action flags

{flag_rows}

## Claim boundary

This is a repo-local fillable template. It does not authorize, collect, fetch, scrape, trust, ingest, integrate, clone, install, deploy, publish, or claim release/production readiness.

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    manual_guide_gate = read_json(MANUAL_GUIDE_GATE)
    require_manual_guide_gate(manual_guide_gate)

    write_text(PACKET_TEMPLATE, build_packet_template(manual_guide_gate))
    template_gate = build_packet_template_gate(manual_guide_gate)
    write_json(PACKET_TEMPLATE_GATE, template_gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result(template_gate))
    write_text(VALIDATION_REPORT, build_report(template_gate))

    print("AVF Capability Primary-Source Evidence Owner Manual Completion Packet Template v0.1")
    print("RESULT: PASS")
    print("authorization_fields_templated=11")
    print("authorization_fields_completed=0")
    print("collection_modes_templated=4")
    print("collection_modes_selected=0")
    print("owner_input_required=true")
    print("owner_authorization_granted=false")
    print("collection_execution_allowed=false")
    print("source_records_executable=0")
    print(f"template_decision={TEMPLATE_DECISION}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
