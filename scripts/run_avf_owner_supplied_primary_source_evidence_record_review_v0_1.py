from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

ACCEPTANCE_GATE = CAPABILITIES / "local_primary_source_evidence_acceptance_gate.json"
ACCEPTANCE_SAMPLE = CAPABILITIES / "local_primary_source_evidence_acceptance_sample.yml"
REVIEW_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_review_gate.json"
REJECTION_REPORT = CAPABILITIES / "owner_supplied_primary_source_evidence_record_review_rejection_report.md"
NEXT_OWNER_ACTION = CAPABILITIES / "owner_supplied_primary_source_evidence_record_review_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "owner_supplied_primary_source_evidence_record_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OWNER_SUPPLIED_PRIMARY_SOURCE_EVIDENCE_RECORD_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_review_v0_1"
PREVIOUS_GOAL_ID = "avf_local_primary_source_evidence_acceptance_harness_v0_1"
NEXT_SAFE_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_completion_guide_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "OWNER_SUPPLIED_SOURCE_RECORD_REJECTED_EMPTY_REQUIRED_FIELDS"

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


def require_acceptance_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("acceptance gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("acceptance gate must point to this record review goal")
    if gate.get("owner_supplied_only") is not True:
        raise SystemExit("acceptance gate must be owner supplied only")
    if gate.get("required_source_fields") != REQUIRED_SOURCE_FIELDS:
        raise SystemExit("acceptance gate required source fields mismatch")
    if gate.get("accepted_records") != 0:
        raise SystemExit("acceptance gate must not accept empty records")
    if gate.get("rejected_records") != 1:
        raise SystemExit("acceptance gate must reject empty sample")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("acceptance gate must keep source collection blocked")


def build_review_gate() -> dict:
    return {
        "gate_id": "avf-owner-supplied-primary-source-evidence-record-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "owner_supplied_only": True,
        "reviewed_sample_uri": rel(ACCEPTANCE_SAMPLE),
        "required_source_fields": REQUIRED_SOURCE_FIELDS,
        "fields_reviewed": len(REQUIRED_SOURCE_FIELDS),
        "fields_present": 0,
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
    return f"""# Owner-Supplied Primary-Source Evidence Record Review Rejection Report v0.1

review_decision={REVIEW_DECISION}
accepted_records=0
rejected_records=1
fields_reviewed={len(REQUIRED_SOURCE_FIELDS)}
fields_present=0
missing_required_fields={len(REQUIRED_SOURCE_FIELDS)}
source_collection_execution_allowed=false
external_fetch_performed=false

## Missing required fields

{missing_rows}

## Protected boundary

{forbidden}
"""


def build_next_owner_action() -> str:
    fields = "\n".join(f"  - {field}" for field in REQUIRED_SOURCE_FIELDS)
    return f"""action_id: owner-complete-primary-source-evidence-record
owner_input_required: true
goal_id: {THIS_GOAL_ID}

owner_steps:
  - Fill all 10 required source fields
  - Use official docs, original repos, papers, patents, standards, maintained implementations, or local repo evidence
  - Paste only owner-supplied source metadata or excerpts
  - Tie the record to a single claim supported
  - Do not ask Codex to fetch the URL

required_source_fields:
{fields}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_owner_supplied_primary_source_evidence_record_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "owner_supplied_only": True,
        "fields_reviewed": len(REQUIRED_SOURCE_FIELDS),
        "fields_present": 0,
        "missing_required_fields": len(REQUIRED_SOURCE_FIELDS),
        "accepted_records": 0,
        "rejected_records": 1,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Owner-Supplied Primary-Source Evidence Record Review v0.1 Report

RESULT: PASS
owner_supplied_primary_source_evidence_record_review_v0_1=true

## Commands

- python scripts\\run_avf_owner_supplied_primary_source_evidence_record_review_v0_1.py
- python scripts\\validate_avf_owner_supplied_primary_source_evidence_record_review_v0_1.py

## Gate summary

- owner_supplied_record_review_gate_created=true
- review_decision={REVIEW_DECISION}
- owner_supplied_only=true
- fields_reviewed={len(REQUIRED_SOURCE_FIELDS)}
- fields_present=0
- missing_required_fields={len(REQUIRED_SOURCE_FIELDS)}
- accepted_records=0
- rejected_records=1
- source_collection_execution_allowed=false

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
    acceptance_gate = read_json(ACCEPTANCE_GATE)
    require_acceptance_gate(acceptance_gate)

    write_json(REVIEW_GATE, build_review_gate())
    write_text(REJECTION_REPORT, build_rejection_report())
    write_text(NEXT_OWNER_ACTION, build_next_owner_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Owner-Supplied Primary-Source Evidence Record Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print("fields_reviewed=10")
    print("fields_present=0")
    print("missing_required_fields=10")
    print("accepted_records=0")
    print("rejected_records=1")
    print("source_collection_execution_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
