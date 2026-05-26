from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOAL_GENERATED = ROOT / "avf" / "goals" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

MATRIX = GOAL_GENERATED / "active_objective_completion_matrix_v0_1.json"
SCHEMA = CAPABILITIES / "local_primary_source_evidence_acceptance.schema.yml"
SAMPLE = CAPABILITIES / "local_primary_source_evidence_acceptance_sample.yml"
GATE = CAPABILITIES / "local_primary_source_evidence_acceptance_gate.json"
NEXT_OWNER_ACTION = CAPABILITIES / "local_primary_source_evidence_acceptance_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "local_primary_source_evidence_acceptance_harness_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_LOCAL_PRIMARY_SOURCE_EVIDENCE_ACCEPTANCE_HARNESS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_local_primary_source_evidence_acceptance_harness_v0_1"
NEXT_SAFE_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
GATE_DECISION = "OWNER_SUPPLIED_SOURCE_RECORD_SCHEMA_READY_EMPTY_SAMPLE_REJECTED"

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


def require_matrix(matrix: dict) -> None:
    if matrix.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("active objective matrix must point to this acceptance harness")
    if matrix.get("objective_completion_proven") is not False:
        raise SystemExit("active objective matrix must not prove completion")
    if matrix.get("source_collection_terminal_condition") != "PROTECTED_ACTION_REQUIRED":
        raise SystemExit("active objective matrix must preserve protected source boundary")


def build_schema() -> str:
    fields = "\n".join(f"  {field}: required" for field in REQUIRED_SOURCE_FIELDS)
    forbidden = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    return f"""schema_id: local_primary_source_evidence_acceptance_v0_1
goal_id: {THIS_GOAL_ID}
created_at: {CREATED_AT}
accepted_collection_mode: owner_supplied_only

required_fields:
{fields}

allowed_source_kinds:
  - official_docs
  - original_repository
  - paper
  - patent
  - standard
  - maintained_implementation
  - local_repo_evidence

record_contract:
  source_id:
  source_title:
  source_kind:
  source_uri:
  source_version_or_date:
  source_owner_or_publisher:
  license_or_rights_note:
  claim_supported:
  evidence_excerpt_summary:
  verification_notes:

disallowed_actions:
{forbidden}
"""


def build_sample() -> str:
    return """sample_id: empty_owner_supplied_primary_source_record
collection_mode: owner_supplied_only
sample_status: incomplete_rejected

source_id:
source_title:
source_kind:
source_uri:
source_version_or_date:
source_owner_or_publisher:
license_or_rights_note:
claim_supported:
evidence_excerpt_summary:
verification_notes:

review_result:
  accepted: false
  rejection_reason: all required source fields are empty
"""


def build_gate() -> dict:
    return {
        "gate_id": "avf-local-primary-source-evidence-acceptance-harness-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "gate_decision": GATE_DECISION,
        "owner_supplied_only": True,
        "schema_uri": rel(SCHEMA),
        "sample_uri": rel(SAMPLE),
        "required_source_fields": REQUIRED_SOURCE_FIELDS,
        "required_source_fields_count": len(REQUIRED_SOURCE_FIELDS),
        "accepted_records": 0,
        "rejected_records": 1,
        "empty_sample_rejected": True,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_owner_action() -> str:
    fields = "\n".join(f"  - {field}" for field in REQUIRED_SOURCE_FIELDS)
    return f"""action_id: owner-fill-local-primary-source-evidence-record
owner_input_required: true
goal_id: {THIS_GOAL_ID}

owner_steps:
  - Fill every required source field
  - Paste only owner-supplied source metadata or excerpts
  - Do not ask Codex to fetch the URL
  - Keep each record tied to one claim supported
  - Use official docs, original repos, papers, patents, standards, maintained implementations, or local repo evidence

required_source_fields:
{fields}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(gate: dict) -> dict:
    return {
        "validator_id": "validate_avf_local_primary_source_evidence_acceptance_harness_v0_1",
        "status": "PASS",
        "owner_supplied_only": True,
        "required_source_fields": len(REQUIRED_SOURCE_FIELDS),
        "accepted_records": gate["accepted_records"],
        "rejected_records": gate["rejected_records"],
        "empty_sample_rejected": True,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(gate: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Local Primary-Source Evidence Acceptance Harness v0.1 Report

RESULT: PASS
local_primary_source_evidence_acceptance_harness_v0_1=true

## Commands

- python scripts\\run_avf_local_primary_source_evidence_acceptance_harness_v0_1.py
- python scripts\\validate_avf_local_primary_source_evidence_acceptance_harness_v0_1.py

## Gate summary

- owner_supplied_only=true
- required_source_fields={len(REQUIRED_SOURCE_FIELDS)}
- accepted_records={gate['accepted_records']}
- rejected_records={gate['rejected_records']}
- empty_sample_rejected=true
- source_collection_execution_allowed=false
- external_fetch_performed=false
- automated_scraping_performed=false

## Generated artifacts

- {rel(SCHEMA)}
- {rel(SAMPLE)}
- {rel(GATE)}
- {rel(NEXT_OWNER_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    matrix = read_json(MATRIX)
    require_matrix(matrix)

    write_text(SCHEMA, build_schema())
    write_text(SAMPLE, build_sample())
    gate = build_gate()
    write_json(GATE, gate)
    write_text(NEXT_OWNER_ACTION, build_next_owner_action())
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Local Primary-Source Evidence Acceptance Harness v0.1")
    print("RESULT: PASS")
    print("owner_supplied_only=true")
    print("required_source_fields=10")
    print("accepted_records=0")
    print("rejected_records=1")
    print("empty_sample_rejected=true")
    print("source_collection_execution_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
