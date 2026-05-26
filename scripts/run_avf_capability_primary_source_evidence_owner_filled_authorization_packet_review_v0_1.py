from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

TEMPLATE = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_template.yml"
TEMPLATE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_template_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_review_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_review_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_FILLED_AUTHORIZATION_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_filled_authorization_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
TEMPLATE_DECISION = "TEMPLATE_READY_UNFILLED_EXECUTION_STILL_BLOCKED"
REVIEW_DECISION = "BLOCKED_OWNER_AUTHORIZATION_PACKET_UNFILLED"

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


def require_template_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("template gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("template gate must point to this review goal")
    if gate.get("template_decision") != TEMPLATE_DECISION:
        raise SystemExit("template gate decision mismatch")
    if gate.get("authorization_template_completed") is not False:
        raise SystemExit("template gate must remain incomplete")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("template gate must not grant owner authorization")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("template gate must keep execution blocked")
    if gate.get("authorization_fields_in_template") != AUTHORIZATION_FIELDS:
        raise SystemExit("template gate authorization fields mismatch")
    if gate.get("missing_authorization_fields") != AUTHORIZATION_FIELDS:
        raise SystemExit("template gate missing fields mismatch")
    if gate.get("authorization_fields_completed") != 0:
        raise SystemExit("template gate must have no completed authorization fields")
    if gate.get("collection_modes_in_template") != COLLECTION_MODES:
        raise SystemExit("template gate collection modes mismatch")

    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        raise SystemExit("template gate must review 35 source records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("template gate must not make source records executable")


def require_template_markers() -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    markers = [
        f"goal_id: {PREVIOUS_GOAL_ID}",
        f"template_decision: {TEMPLATE_DECISION}",
        "authorization_template_completed: false",
        "owner_authorization_granted: false",
        "collection_execution_allowed: false",
        "source_records_executable: 0",
        "authorized_collection_modes: []",
        "max_records_to_collect: 0",
        f"next_safe_goal_id: {THIS_GOAL_ID}",
    ]
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise SystemExit("template missing review-required markers: " + ", ".join(missing))


def build_review_gate(template_gate: dict) -> dict:
    counts = template_gate["source_entry_counts"]
    return {
        "gate_id": "avf-capability-primary-source-evidence-owner-filled-authorization-packet-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "reviewed_template_uri": rel(TEMPLATE),
        "reviewed_template_gate_uri": rel(TEMPLATE_GATE),
        "authorization_template_completed": False,
        "authorization_review_passed": False,
        "owner_authorization_granted": False,
        "authorization_fields_reviewed": len(AUTHORIZATION_FIELDS),
        "authorization_fields_present": 0,
        "missing_authorization_fields": AUTHORIZATION_FIELDS,
        "collection_modes_available": COLLECTION_MODES,
        "requested_collection_modes": [],
        "collection_modes_authorized": 0,
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
        "validator_id": "validate_avf_capability_primary_source_evidence_owner_filled_authorization_packet_review_v0_1",
        "status": "PASS",
        "checks": [
            "owner-filled authorization packet template reviewed",
            "authorization remains incomplete",
            "no collection modes are authorized",
            "collection execution remains blocked",
            "protected-action flags remain false",
        ],
        "review_decision": REVIEW_DECISION,
        "authorization_template_completed": False,
        "authorization_review_passed": False,
        "owner_authorization_granted": False,
        "authorization_fields_reviewed": len(AUTHORIZATION_FIELDS),
        "authorization_fields_present": 0,
        "missing_authorization_fields": len(AUTHORIZATION_FIELDS),
        "collection_modes_authorized": 0,
        "source_records_reviewed": counts["source_records_reviewed"],
        "source_records_executable": counts["source_records_executable"],
        "collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    forbidden = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    missing = "\n".join(f"  - {field}" for field in AUTHORIZATION_FIELDS)
    return f"""task_id: avf-capability-primary-source-evidence-owner-filled-authorization-packet-completion-retry-v0-1
title: Add AVF owner-filled authorization packet completion retry v0.1
goal: Provide a repo-local retry packet for the owner to fill missing authorization fields without enabling source collection or external execution.
context_paths:
  - {rel(TEMPLATE)}
  - {rel(REVIEW_GATE)}
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry.yml
  - avf/capabilities/generated/capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_FILLED_AUTHORIZATION_PACKET_COMPLETION_RETRY_V0_1_REPORT.md
missing_authorization_fields:
{missing}
forbidden_changes:
{forbidden}
acceptance_criteria:
  - retry packet lists every missing authorization field
  - retry packet keeps collection execution blocked by default
  - retry packet does not perform source collection, provider calls, scraping, clone, install, runtime integration, deploy, publish, or readiness claims
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_owner_filled_authorization_packet_review_v0_1.py
expected_outputs:
  - owner-filled authorization packet completion retry packet
  - blocked retry gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    flag_rows = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Primary-Source Evidence Owner-Filled Authorization Packet Review v0.1 Report

RESULT: PASS

## Commands

- python scripts\\run_avf_capability_primary_source_evidence_owner_filled_authorization_packet_review_v0_1.py
- python scripts\\validate_avf_capability_primary_source_evidence_owner_filled_authorization_packet_review_v0_1.py

## Generated artifacts

- {rel(REVIEW_GATE)}
- {rel(NEXT_CODEX_TASK)}
- {rel(VALIDATION_RESULT)}
- {rel(VALIDATION_REPORT)}

## Gate summary

- capability_primary_source_evidence_owner_filled_authorization_packet_review_v0_1=true
- owner_filled_authorization_packet_review_gate_created=true
- authorization_template_completed=false
- authorization_review_passed=false
- authorization_fields_reviewed={len(AUTHORIZATION_FIELDS)}
- authorization_fields_present=0
- missing_authorization_fields={len(AUTHORIZATION_FIELDS)}
- collection_modes_authorized=0
- source_records_reviewed={counts["source_records_reviewed"]}
- source_records_executable={counts["source_records_executable"]}
- collection_execution_allowed=false
- owner_authorization_granted=false
- review_decision={REVIEW_DECISION}

## Protected action flags

{flag_rows}

## Claim boundary

This is a repo-local review of an unfilled owner authorization template. It does not grant authorization and does not perform source collection, external calls, cloning, installation, runtime integration, deployment, publishing, or readiness claims.

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_template_markers()
    template_gate = read_json(TEMPLATE_GATE)
    require_template_gate(template_gate)

    review_gate = build_review_gate(template_gate)
    validation_result = build_validation_result(review_gate)

    write_json(REVIEW_GATE, review_gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, validation_result)
    write_text(VALIDATION_REPORT, build_report(review_gate))

    print("AVF Capability Primary-Source Evidence Owner-Filled Authorization Packet Review v0.1 generated")
    print(f"review_gate={rel(REVIEW_GATE)}")
    print(f"validation_report={rel(VALIDATION_REPORT)}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
