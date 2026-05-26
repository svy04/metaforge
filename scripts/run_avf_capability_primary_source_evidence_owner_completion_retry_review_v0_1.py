from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RETRY_PACKET = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry.yml"
RETRY_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_gate.json"
RETRY_REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_completion_retry_review_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_completion_retry_review_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_completion_retry_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_COMPLETION_RETRY_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_completion_retry_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_filled_authorization_packet_completion_retry_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_guide_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
RETRY_DECISION = "RETRY_PACKET_READY_OWNER_INPUT_REQUIRED_EXECUTION_BLOCKED"
RETRY_REVIEW_DECISION = "BLOCKED_OWNER_COMPLETION_RETRY_STILL_EMPTY"

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


def require_retry_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("retry gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("retry gate must point to this retry review goal")
    if gate.get("retry_decision") != RETRY_DECISION:
        raise SystemExit("retry gate decision mismatch")
    if gate.get("owner_input_required") is not True:
        raise SystemExit("retry gate must require owner input")
    if gate.get("authorization_retry_completed") is not False:
        raise SystemExit("retry gate must remain incomplete")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("retry gate must not grant owner authorization")
    if gate.get("authorization_fields_completed") != 0:
        raise SystemExit("retry gate must not complete authorization fields")
    if gate.get("missing_authorization_fields") != AUTHORIZATION_FIELDS:
        raise SystemExit("retry gate missing fields mismatch")
    if gate.get("selected_collection_modes") != []:
        raise SystemExit("retry gate selected collection modes must be empty")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("retry gate must keep collection blocked")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        raise SystemExit("retry gate must review 35 source records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("retry gate must not make source records executable")


def require_retry_packet_markers() -> None:
    text = RETRY_PACKET.read_text(encoding="utf-8")
    markers = [
        f"goal_id: {PREVIOUS_GOAL_ID}",
        f"retry_decision: {RETRY_DECISION}",
        "owner_input_required: true",
        "authorization_retry_completed: false",
        "owner_authorization_granted: false",
        "collection_execution_allowed: false",
        "source_records_executable: 0",
        "missing_authorization_fields_count: 11",
        "authorized_collection_modes: []",
        "max_records_to_collect: 0",
        f"next_safe_goal_id: {THIS_GOAL_ID}",
    ]
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise SystemExit("retry packet missing review-required markers: " + ", ".join(missing))


def build_retry_review_gate(retry_gate: dict) -> dict:
    counts = retry_gate["source_entry_counts"]
    return {
        "gate_id": "avf-capability-primary-source-evidence-owner-completion-retry-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "retry_review_decision": RETRY_REVIEW_DECISION,
        "reviewed_retry_packet_uri": rel(RETRY_PACKET),
        "reviewed_retry_gate_uri": rel(RETRY_GATE),
        "owner_input_required": True,
        "authorization_retry_completed": False,
        "authorization_retry_review_passed": False,
        "owner_authorization_granted": False,
        "authorization_fields_reviewed": len(AUTHORIZATION_FIELDS),
        "authorization_fields_present": 0,
        "missing_authorization_fields_count": len(AUTHORIZATION_FIELDS),
        "missing_authorization_fields": AUTHORIZATION_FIELDS,
        "collection_modes_available": COLLECTION_MODES,
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
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_owner_completion_retry_review_v0_1",
        "status": "PASS",
        "checks": [
            "owner completion retry packet reviewed",
            "owner input is still required",
            "authorization retry remains incomplete",
            "collection execution remains blocked",
            "protected-action flags remain false",
        ],
        "retry_review_decision": RETRY_REVIEW_DECISION,
        "owner_input_required": True,
        "authorization_retry_completed": False,
        "authorization_retry_review_passed": False,
        "owner_authorization_granted": False,
        "authorization_fields_reviewed": len(AUTHORIZATION_FIELDS),
        "authorization_fields_present": 0,
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
    missing = "\n".join(f"  - {field}" for field in AUTHORIZATION_FIELDS)
    return f"""task_id: avf-capability-primary-source-evidence-owner-manual-completion-guide-v0-1
title: Add AVF owner manual completion guide v0.1
goal: Give the owner a concise manual guide for completing the missing authorization fields without enabling source collection or external execution.
context_paths:
  - {rel(RETRY_PACKET)}
  - {rel(RETRY_REVIEW_GATE)}
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_manual_completion_guide.md
  - avf/capabilities/generated/capability_primary_source_evidence_owner_manual_completion_guide_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_MANUAL_COMPLETION_GUIDE_V0_1_REPORT.md
missing_authorization_fields:
{missing}
forbidden_changes:
{forbidden}
acceptance_criteria:
  - guide explains how owner should complete every missing authorization field
  - guide keeps collection execution blocked
  - guide does not perform source collection, provider calls, scraping, clone, install, runtime integration, deploy, publish, or readiness claims
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_owner_completion_retry_review_v0_1.py
expected_outputs:
  - owner manual completion guide
  - blocked guide gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    flag_rows = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Primary-Source Evidence Owner Completion Retry Review v0.1 Report

RESULT: PASS

## Commands

- python scripts\\run_avf_capability_primary_source_evidence_owner_completion_retry_review_v0_1.py
- python scripts\\validate_avf_capability_primary_source_evidence_owner_completion_retry_review_v0_1.py

## Generated artifacts

- {rel(RETRY_REVIEW_GATE)}
- {rel(NEXT_CODEX_TASK)}
- {rel(VALIDATION_RESULT)}
- {rel(VALIDATION_REPORT)}

## Gate summary

- capability_primary_source_evidence_owner_completion_retry_review_v0_1=true
- owner_completion_retry_review_gate_created=true
- owner_input_required=true
- authorization_retry_completed=false
- authorization_retry_review_passed=false
- authorization_fields_reviewed={len(AUTHORIZATION_FIELDS)}
- authorization_fields_present=0
- missing_authorization_fields={len(AUTHORIZATION_FIELDS)}
- collection_modes_selected=0
- source_records_reviewed={counts["source_records_reviewed"]}
- source_records_executable={counts["source_records_executable"]}
- collection_execution_allowed=false
- owner_authorization_granted=false
- retry_review_decision={RETRY_REVIEW_DECISION}

## Protected action flags

{flag_rows}

## Claim boundary

This is a repo-local review of an incomplete owner completion retry packet. It does not grant authorization and does not perform source collection, external calls, cloning, installation, runtime integration, deployment, publishing, or readiness claims.

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_retry_packet_markers()
    retry_gate = read_json(RETRY_GATE)
    require_retry_gate(retry_gate)

    retry_review_gate = build_retry_review_gate(retry_gate)
    validation_result = build_validation_result(retry_review_gate)

    write_json(RETRY_REVIEW_GATE, retry_review_gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, validation_result)
    write_text(VALIDATION_REPORT, build_report(retry_review_gate))

    print("AVF Capability Primary-Source Evidence Owner Completion Retry Review v0.1 generated")
    print(f"retry_review_gate={rel(RETRY_REVIEW_GATE)}")
    print(f"validation_report={rel(VALIDATION_REPORT)}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
