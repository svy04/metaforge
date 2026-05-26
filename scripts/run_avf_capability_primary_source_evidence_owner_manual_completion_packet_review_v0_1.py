from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

PACKET_TEMPLATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template.yml"
PACKET_TEMPLATE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_template_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_review_gate.json"
TERMINAL_BOUNDARY = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_review_protected_action_required_boundary.json"
NEXT_OWNER_ACTION = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_review_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_MANUAL_COMPLETION_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
TEMPLATE_DECISION = "MANUAL_COMPLETION_PACKET_TEMPLATE_READY_OWNER_INPUT_REQUIRED"
REVIEW_DECISION = "PROTECTED_ACTION_REQUIRED_OWNER_PACKET_STILL_UNFILLED"
TERMINAL_CONDITION = "PROTECTED_ACTION_REQUIRED"

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


def require_packet_template_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("packet template gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("packet template gate must point to this packet review goal")
    if gate.get("template_decision") != TEMPLATE_DECISION:
        raise SystemExit("packet template decision mismatch")
    if gate.get("owner_input_required") is not True:
        raise SystemExit("packet template must require owner input")
    if gate.get("manual_completion_packet_completed") is not False:
        raise SystemExit("packet template must remain uncompleted")
    if gate.get("authorization_fields_completed") != 0:
        raise SystemExit("packet template must not complete authorization fields")
    if gate.get("missing_authorization_fields") != AUTHORIZATION_FIELDS:
        raise SystemExit("packet template missing fields mismatch")
    if gate.get("selected_collection_modes") != []:
        raise SystemExit("packet template selected collection modes must be empty")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("packet template must keep collection blocked")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        raise SystemExit("packet template must cover 35 source records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("packet template must not make source records executable")


def build_review_gate(template_gate: dict) -> dict:
    counts = template_gate["source_entry_counts"]
    return {
        "gate_id": "avf-capability-primary-source-evidence-owner-manual-completion-packet-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "terminal_condition": TERMINAL_CONDITION,
        "review_decision": REVIEW_DECISION,
        "reviewed_packet_template_uri": rel(PACKET_TEMPLATE),
        "reviewed_packet_template_gate_uri": rel(PACKET_TEMPLATE_GATE),
        "owner_input_required": True,
        "manual_completion_packet_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_reviewed": len(AUTHORIZATION_FIELDS),
        "authorization_fields_completed": 0,
        "missing_authorization_fields_count": len(AUTHORIZATION_FIELDS),
        "missing_authorization_fields": AUTHORIZATION_FIELDS,
        "selected_collection_modes": [],
        "collection_modes_selected": 0,
        "source_entry_counts": {
            "source_records_reviewed": counts["source_records_reviewed"],
            "source_records_executable": 0,
            "trusted_source_records": 0,
            "ingested_source_records": 0,
            "integrated_source_records": 0,
        },
        "collection_execution_allowed": False,
        "integration_decision": "blocked",
        "claim_boundary": false_boundary(),
    }


def build_terminal_boundary(review_gate: dict) -> dict:
    return {
        "boundary_id": "avf-capability-primary-source-evidence-owner-manual-completion-packet-review-protected-action-required-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "terminal_condition": TERMINAL_CONDITION,
        "review_decision": REVIEW_DECISION,
        "owner_input_required": True,
        "reason": "The owner manual completion packet template is still unfilled. Source collection would require explicit owner authorization and a later review gate.",
        "required_owner_action_uri": rel(NEXT_OWNER_ACTION),
        "collection_execution_allowed": False,
        "claim_boundary": false_boundary(),
    }


def build_next_owner_action() -> str:
    fields = "\n".join(f"  - {field}" for field in AUTHORIZATION_FIELDS)
    forbidden = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    return f"""action_id: owner-fill-avf-primary-source-evidence-manual-completion-packet
terminal_condition: {TERMINAL_CONDITION}
owner_input_required: true
review_decision: {REVIEW_DECISION}
packet_template_to_fill: {rel(PACKET_TEMPLATE)}

owner_steps:
  - Fill all 11 authorization fields
  - Select at least one collection mode
  - Choose explicit source families, candidate ids, and source slot ids
  - Set a narrow max_records_to_collect value
  - Add collection boundaries and a revocation note
  - Do not ask Codex to collect sources until review passes

authorization_fields:
{fields}

blocked_until_owner_completion:
{forbidden}
"""


def build_validation_result(review_gate: dict) -> dict:
    counts = review_gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1",
        "status": "PASS",
        "terminal_condition": TERMINAL_CONDITION,
        "review_decision": REVIEW_DECISION,
        "checks": [
            "packet template remains unfilled",
            "owner input is required",
            "review returns protected-action-required boundary",
            "collection execution remains blocked",
            "protected-action flags remain false",
        ],
        "owner_input_required": True,
        "manual_completion_packet_completed": False,
        "authorization_fields_reviewed": len(AUTHORIZATION_FIELDS),
        "authorization_fields_completed": 0,
        "missing_authorization_fields": len(AUTHORIZATION_FIELDS),
        "collection_modes_selected": 0,
        "source_records_reviewed": counts["source_records_reviewed"],
        "source_records_executable": counts["source_records_executable"],
        "collection_execution_allowed": False,
        "owner_authorization_granted": False,
        "claim_boundary": false_boundary(),
    }


def build_report(review_gate: dict) -> str:
    counts = review_gate["source_entry_counts"]
    flag_rows = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Primary-Source Evidence Owner Manual Completion Packet Review v0.1 Report

RESULT: PASS
terminal_condition=PROTECTED_ACTION_REQUIRED

## Commands

- python scripts\\run_avf_capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1.py
- python scripts\\validate_avf_capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1.py

## Generated artifacts

- {rel(REVIEW_GATE)}
- {rel(TERMINAL_BOUNDARY)}
- {rel(NEXT_OWNER_ACTION)}
- {rel(VALIDATION_RESULT)}
- {rel(VALIDATION_REPORT)}

## Gate summary

- capability_primary_source_evidence_owner_manual_completion_packet_review_v0_1=true
- owner_manual_completion_packet_review_gate_created=true
- protected_action_required_boundary_created=true
- owner_input_required=true
- manual_completion_packet_completed=false
- authorization_fields_reviewed={len(AUTHORIZATION_FIELDS)}
- authorization_fields_completed=0
- missing_authorization_fields={len(AUTHORIZATION_FIELDS)}
- collection_modes_selected=0
- source_records_reviewed={counts['source_records_reviewed']}
- source_records_executable={counts['source_records_executable']}
- collection_execution_allowed=false
- owner_authorization_granted=false
- review_decision={REVIEW_DECISION}

## Protected action flags

{flag_rows}

## Claim boundary

The current source-evidence collection lane is stopped at PROTECTED_ACTION_REQUIRED because owner authorization is still absent. No protected action was executed.
"""


def main() -> None:
    packet_template_gate = read_json(PACKET_TEMPLATE_GATE)
    require_packet_template_gate(packet_template_gate)

    review_gate = build_review_gate(packet_template_gate)
    write_json(REVIEW_GATE, review_gate)
    write_json(TERMINAL_BOUNDARY, build_terminal_boundary(review_gate))
    write_text(NEXT_OWNER_ACTION, build_next_owner_action())
    write_json(VALIDATION_RESULT, build_validation_result(review_gate))
    write_text(VALIDATION_REPORT, build_report(review_gate))

    print("AVF Capability Primary-Source Evidence Owner Manual Completion Packet Review v0.1")
    print("RESULT: PASS")
    print("terminal_condition=PROTECTED_ACTION_REQUIRED")
    print("owner_input_required=true")
    print("manual_completion_packet_completed=false")
    print("collection_execution_allowed=false")
    print("source_records_executable=0")
    print(f"review_decision={REVIEW_DECISION}")


if __name__ == "__main__":
    main()
