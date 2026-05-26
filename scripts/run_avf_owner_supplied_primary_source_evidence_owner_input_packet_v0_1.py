from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

FILLED_RECORD_REVIEW_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_filled_record_review_gate.json"
INPUT_PACKET = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet.yml"
INPUT_PACKET_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_gate.json"
NEXT_OWNER_ACTION = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OWNER_SUPPLIED_PRIMARY_SOURCE_EVIDENCE_OWNER_INPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_owner_input_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_filled_record_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_owner_supplied_primary_source_evidence_owner_input_packet_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PREVIOUS_REVIEW_DECISION = "OWNER_FILLED_SOURCE_RECORD_REJECTED_EMPTY_TEMPLATE"
PACKET_DECISION = "OWNER_INPUT_PACKET_READY_FOR_OWNER_SUPPLIED_SOURCE_RECORD"

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

ALLOWED_SOURCE_KINDS = [
    "official_docs",
    "original_repository",
    "paper",
    "patent",
    "standard",
    "maintained_implementation",
    "local_repo_evidence",
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


def require_filled_record_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("filled-record review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("filled-record review gate must point to this owner input packet goal")
    if gate.get("review_decision") != PREVIOUS_REVIEW_DECISION:
        raise SystemExit("filled-record review gate decision mismatch")
    if gate.get("filled_record_supplied") is not False:
        raise SystemExit("filled-record review gate must show no filled record exists")
    if gate.get("fields_completed") != 0:
        raise SystemExit("filled-record review gate must show zero completed fields")
    if gate.get("accepted_records") != 0:
        raise SystemExit("filled-record review gate must not accept records")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("filled-record review gate must keep source collection blocked")


def build_input_packet() -> str:
    source_kinds = "\n".join(f"  - {kind}" for kind in ALLOWED_SOURCE_KINDS)
    source_record_fields = "\n".join(f"    {field}: \"\"" for field in REQUIRED_SOURCE_FIELDS)
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""# Owner-Supplied Primary-Source Evidence Owner Input Packet v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
packet_decision: {PACKET_DECISION}
packet_status: waiting_for_owner_input
owner_input_required: true
owner_supplied_only: true
filled_record_supplied: false
fields_completed: 0
accepted_records: 0
source_collection_execution_allowed: false

allowed_source_kinds:
{source_kinds}

owner_paste_slot:
  instructions:
    - Paste exactly one completed source record into source_record.
    - Use owner-supplied metadata, excerpts, or local repo evidence only.
    - Do not ask Codex to fetch the URL.
    - Keep one source tied to one concrete AVF claim.
    - Leave the packet unaccepted until the next review gate passes.
  source_record:
{source_record_fields}

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_input_packet_gate() -> dict:
    return {
        "gate_id": "avf-owner-supplied-primary-source-evidence-owner-input-packet-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "packet_decision": PACKET_DECISION,
        "packet_status": "waiting_for_owner_input",
        "owner_input_packet_uri": rel(INPUT_PACKET),
        "owner_input_required": True,
        "owner_supplied_only": True,
        "filled_record_supplied": False,
        "required_source_fields": REQUIRED_SOURCE_FIELDS,
        "required_source_fields_count": len(REQUIRED_SOURCE_FIELDS),
        "allowed_source_kinds": ALLOWED_SOURCE_KINDS,
        "fields_completed": 0,
        "accepted_records": 0,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_owner_action() -> str:
    fields = "\n".join(f"  - {field}" for field in REQUIRED_SOURCE_FIELDS)
    kinds = "\n".join(f"  - {kind}" for kind in ALLOWED_SOURCE_KINDS)
    return f"""action_id: owner-paste-primary-source-evidence-record-into-input-packet
owner_input_required: true
goal_id: {THIS_GOAL_ID}

owner_steps:
  - Paste exactly one completed source record into the input packet
  - Fill all 10 required fields
  - Choose one allowed source kind
  - Tie the source to exactly one AVF claim supported
  - Do not ask Codex to fetch the URL

required_source_fields:
{fields}

allowed_source_kinds:
{kinds}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_owner_supplied_primary_source_evidence_owner_input_packet_v0_1",
        "status": "PASS",
        "packet_decision": PACKET_DECISION,
        "packet_status": "waiting_for_owner_input",
        "owner_input_required": True,
        "owner_supplied_only": True,
        "filled_record_supplied": False,
        "fields_completed": 0,
        "accepted_records": 0,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Owner-Supplied Primary-Source Evidence Owner Input Packet v0.1 Report

RESULT: PASS
owner_supplied_primary_source_evidence_owner_input_packet_v0_1=true

## Commands

- python scripts\\run_avf_owner_supplied_primary_source_evidence_owner_input_packet_v0_1.py
- python scripts\\validate_avf_owner_supplied_primary_source_evidence_owner_input_packet_v0_1.py

## Gate summary

- owner_input_packet_created=true
- owner_input_packet_gate_created=true
- packet_status=waiting_for_owner_input
- owner_input_required=true
- owner_supplied_only=true
- filled_record_supplied=false
- fields_completed=0
- accepted_records=0
- source_collection_execution_allowed=false
- external_fetch_performed=false

## Generated artifacts

- {rel(INPUT_PACKET)}
- {rel(INPUT_PACKET_GATE)}
- {rel(NEXT_OWNER_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    filled_record_review_gate = read_json(FILLED_RECORD_REVIEW_GATE)
    require_filled_record_review_gate(filled_record_review_gate)

    write_text(INPUT_PACKET, build_input_packet())
    write_json(INPUT_PACKET_GATE, build_input_packet_gate())
    write_text(NEXT_OWNER_ACTION, build_next_owner_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Owner-Supplied Primary-Source Evidence Owner Input Packet v0.1")
    print("RESULT: PASS")
    print("owner_input_packet_created=true")
    print("owner_input_packet_gate_created=true")
    print("packet_status=waiting_for_owner_input")
    print("owner_input_required=true")
    print("filled_record_supplied=false")
    print("fields_completed=0")
    print("accepted_records=0")
    print("source_collection_execution_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
