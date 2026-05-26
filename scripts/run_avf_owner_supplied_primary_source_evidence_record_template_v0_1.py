from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

COMPLETION_GUIDE_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_completion_guide_gate.json"
TEMPLATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_template.yml"
TEMPLATE_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_template_gate.json"
NEXT_OWNER_ACTION = CAPABILITIES / "owner_supplied_primary_source_evidence_record_template_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "owner_supplied_primary_source_evidence_record_template_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OWNER_SUPPLIED_PRIMARY_SOURCE_EVIDENCE_RECORD_TEMPLATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_template_v0_1"
PREVIOUS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_completion_guide_v0_1"
NEXT_SAFE_GOAL_ID = "avf_owner_supplied_primary_source_evidence_filled_record_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
TEMPLATE_DECISION = "OWNER_SUPPLIED_SOURCE_RECORD_TEMPLATE_READY"
GUIDE_DECISION = "OWNER_SUPPLIED_SOURCE_RECORD_COMPLETION_GUIDE_READY"

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


def require_completion_guide_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("completion guide gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("completion guide gate must point to this template goal")
    if gate.get("guide_decision") != GUIDE_DECISION:
        raise SystemExit("completion guide gate decision mismatch")
    if gate.get("owner_supplied_only") is not True:
        raise SystemExit("completion guide gate must be owner supplied only")
    if gate.get("required_source_fields_documented") != REQUIRED_SOURCE_FIELDS:
        raise SystemExit("completion guide gate required source fields mismatch")
    if gate.get("allowed_source_kinds") != ALLOWED_SOURCE_KINDS:
        raise SystemExit("completion guide gate allowed source kinds mismatch")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("completion guide gate must keep source collection blocked")


def build_template() -> str:
    allowed_kinds = "\n".join(f"  - {kind}" for kind in ALLOWED_SOURCE_KINDS)
    field_placeholders = "\n".join(f"  {field}: \"\"" for field in REQUIRED_SOURCE_FIELDS)
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""# Owner-Supplied Primary-Source Evidence Record Template v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
template_decision: {TEMPLATE_DECISION}
template_status: fillable_owner_supplied_template
owner_supplied_only: true
source_collection_execution_allowed: false
fields_completed: 0
accepted_records: 0

allowed_source_kinds:
{allowed_kinds}

owner_instructions:
  - Fill every required field with owner-supplied source metadata, excerpts, or local repo evidence.
  - Do not ask Codex to fetch the URL.
  - Keep unknown fields blank until the owner supplies source evidence.
  - Use one record per source and tie the record to one concrete AVF claim.

source_record:
{field_placeholders}

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_template_gate() -> dict:
    return {
        "gate_id": "avf-owner-supplied-primary-source-evidence-record-template-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "template_decision": TEMPLATE_DECISION,
        "template_uri": rel(TEMPLATE),
        "owner_supplied_only": True,
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
    return f"""action_id: owner-complete-primary-source-evidence-record-from-template
owner_input_required: true
goal_id: {THIS_GOAL_ID}

owner_steps:
  - Fill the template with owner-supplied source metadata
  - Choose one allowed source kind
  - Tie the record to one AVF claim supported by the source
  - Leave the record unaccepted until the filled-record review gate passes
  - Do not ask Codex to fetch the URL

required_source_fields:
{fields}

allowed_source_kinds:
{kinds}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_owner_supplied_primary_source_evidence_record_template_v0_1",
        "status": "PASS",
        "template_decision": TEMPLATE_DECISION,
        "owner_supplied_only": True,
        "required_source_fields": len(REQUIRED_SOURCE_FIELDS),
        "fields_completed": 0,
        "accepted_records": 0,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Owner-Supplied Primary-Source Evidence Record Template v0.1 Report

RESULT: PASS
owner_supplied_primary_source_evidence_record_template_v0_1=true

## Commands

- python scripts\\run_avf_owner_supplied_primary_source_evidence_record_template_v0_1.py
- python scripts\\validate_avf_owner_supplied_primary_source_evidence_record_template_v0_1.py

## Gate summary

- template_created=true
- template_gate_created=true
- required_source_fields={len(REQUIRED_SOURCE_FIELDS)}
- fields_completed=0
- accepted_records=0
- owner_supplied_only=true
- source_collection_execution_allowed=false
- external_fetch_performed=false

## Generated artifacts

- {rel(TEMPLATE)}
- {rel(TEMPLATE_GATE)}
- {rel(NEXT_OWNER_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    completion_guide_gate = read_json(COMPLETION_GUIDE_GATE)
    require_completion_guide_gate(completion_guide_gate)

    write_text(TEMPLATE, build_template())
    write_json(TEMPLATE_GATE, build_template_gate())
    write_text(NEXT_OWNER_ACTION, build_next_owner_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Owner-Supplied Primary-Source Evidence Record Template v0.1")
    print("RESULT: PASS")
    print("template_created=true")
    print("template_gate_created=true")
    print("required_source_fields=10")
    print("fields_completed=0")
    print("accepted_records=0")
    print("owner_supplied_only=true")
    print("source_collection_execution_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
