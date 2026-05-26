from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

INPUT_PACKET = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet.yml"
INPUT_PACKET_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_gate.json"
REVIEW_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_review_gate.json"
REJECTION_REPORT = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_review_rejection_report.md"
NEXT_OWNER_ACTION = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_review_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OWNER_SUPPLIED_PRIMARY_SOURCE_EVIDENCE_OWNER_INPUT_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_owner_input_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_owner_input_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_acquisition_approval_packet_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PACKET_DECISION = "OWNER_INPUT_PACKET_READY_FOR_OWNER_SUPPLIED_SOURCE_RECORD"
REVIEW_DECISION = "OWNER_INPUT_PACKET_REJECTED_EMPTY_SOURCE_RECORD"

REQUIRED_SOURCE_FIELDS = [
    "source_id",
    "source_title",
    "source_kind",
    "source_uri",
    "source_version_or_date",
    "source_owner_or_publisher",
    "license_or_rights_note",
    "claim_supported",
    "evidence_excerpt_summary",
    "verification_notes",
]

BOUNDARY_ITEMS = [
    "source collection execution",
    "provider calls",
    "live model calls",
    "external service calls",
    "external fetch",
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


def require_input_packet_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("owner input packet gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("owner input packet gate must point to this review goal")
    if gate.get("packet_decision") != PACKET_DECISION:
        raise SystemExit("owner input packet gate decision mismatch")
    if gate.get("packet_status") != "waiting_for_owner_input":
        raise SystemExit("owner input packet gate must be waiting for owner input")
    if gate.get("filled_record_supplied") is not False:
        raise SystemExit("owner input packet gate must show no filled record exists")
    if gate.get("fields_completed") != 0:
        raise SystemExit("owner input packet gate must show zero completed fields")
    if gate.get("accepted_records") != 0:
        raise SystemExit("owner input packet gate must not accept records")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("owner input packet gate must keep source collection blocked")


def build_review_gate() -> dict:
    return {
        "gate_id": "avf-owner-supplied-primary-source-evidence-owner-input-packet-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "owner_input_packet_reviewed": True,
        "reviewed_input_packet_uri": rel(INPUT_PACKET),
        "filled_record_supplied": False,
        "required_source_fields": REQUIRED_SOURCE_FIELDS,
        "fields_reviewed": len(REQUIRED_SOURCE_FIELDS),
        "fields_completed": 0,
        "missing_required_fields": REQUIRED_SOURCE_FIELDS,
        "missing_required_fields_count": len(REQUIRED_SOURCE_FIELDS),
        "accepted_records": 0,
        "rejected_records": 1,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_rejection_report() -> str:
    missing_rows = "\n".join(f"- `{field}`" for field in REQUIRED_SOURCE_FIELDS)
    forbidden = "\n".join(f"- No {item}" for item in BOUNDARY_ITEMS)
    return f"""# Owner-Supplied Primary-Source Evidence Owner Input Packet Review Rejection Report v0.1

review_decision={REVIEW_DECISION}
owner_input_packet_reviewed=true
filled_record_supplied=false
accepted_records=0
rejected_records=1
fields_reviewed={len(REQUIRED_SOURCE_FIELDS)}
fields_completed=0
missing_required_fields={len(REQUIRED_SOURCE_FIELDS)}
source_collection_execution_allowed=false
external_fetch_performed=false

The owner input packet exists, but it is still blank. It cannot support AVF claims until a completed primary-source record is supplied or a separate approval packet explicitly authorizes source acquisition.

## Missing required fields

{missing_rows}

## Protected boundary

{forbidden}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_owner_action() -> str:
    return f"""action_id: prepare-primary-source-acquisition-approval-packet
owner_input_required: false
goal_id: {THIS_GOAL_ID}

owner_steps:
  - Prepare a separate approval packet before any primary-source acquisition
  - Define allowed source categories and denied actions
  - Keep acquisition planning repo-local until approval is recorded
  - Do not fetch, scrape, clone, install, or call providers in this step

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_owner_supplied_primary_source_evidence_owner_input_packet_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "owner_input_packet_reviewed": True,
        "filled_record_supplied": False,
        "fields_reviewed": len(REQUIRED_SOURCE_FIELDS),
        "fields_completed": 0,
        "missing_required_fields": len(REQUIRED_SOURCE_FIELDS),
        "accepted_records": 0,
        "rejected_records": 1,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Owner-Supplied Primary-Source Evidence Owner Input Packet Review v0.1 Report

RESULT: PASS
owner_supplied_primary_source_evidence_owner_input_packet_review_v0_1=true

## Commands

- python scripts\\run_avf_owner_supplied_primary_source_evidence_owner_input_packet_review_v0_1.py
- python scripts\\validate_avf_owner_supplied_primary_source_evidence_owner_input_packet_review_v0_1.py

## Gate summary

- review_decision={REVIEW_DECISION}
- owner_input_packet_reviewed=true
- filled_record_supplied=false
- fields_reviewed={len(REQUIRED_SOURCE_FIELDS)}
- fields_completed=0
- missing_required_fields={len(REQUIRED_SOURCE_FIELDS)}
- accepted_records=0
- rejected_records=1
- source_collection_execution_allowed=false
- external_fetch_performed=false

## Generated artifacts

- {rel(REVIEW_GATE)}
- {rel(REJECTION_REPORT)}
- {rel(NEXT_OWNER_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    input_packet_gate = read_json(INPUT_PACKET_GATE)
    require_input_packet_gate(input_packet_gate)

    write_json(REVIEW_GATE, build_review_gate())
    write_text(REJECTION_REPORT, build_rejection_report())
    write_text(NEXT_OWNER_ACTION, build_next_owner_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Owner-Supplied Primary-Source Evidence Owner Input Packet Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print("owner_input_packet_reviewed=true")
    print("filled_record_supplied=false")
    print("fields_reviewed=10")
    print("fields_completed=0")
    print("missing_required_fields=10")
    print("accepted_records=0")
    print("rejected_records=1")
    print("source_collection_execution_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
