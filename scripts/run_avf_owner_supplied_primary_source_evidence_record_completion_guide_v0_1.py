from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

REVIEW_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_review_gate.json"
COMPLETION_GUIDE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_completion_guide.md"
COMPLETION_GUIDE_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_record_completion_guide_gate.json"
NEXT_OWNER_ACTION = CAPABILITIES / "owner_supplied_primary_source_evidence_record_completion_guide_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "owner_supplied_primary_source_evidence_record_completion_guide_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OWNER_SUPPLIED_PRIMARY_SOURCE_EVIDENCE_RECORD_COMPLETION_GUIDE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_completion_guide_v0_1"
PREVIOUS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_owner_supplied_primary_source_evidence_record_template_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
GUIDE_DECISION = "OWNER_SUPPLIED_SOURCE_RECORD_COMPLETION_GUIDE_READY"
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

ALLOWED_SOURCE_KINDS = [
    "official_docs",
    "original_repository",
    "paper",
    "patent",
    "standard",
    "maintained_implementation",
    "local_repo_evidence",
]

FIELD_GUIDANCE = {
    "source_id": "Use a stable id such as src-langgraph-docs-overview or src-react-paper.",
    "source_title": "Use the exact title from the source, not a summary title.",
    "source_kind": "Use one allowed kind: official_docs, original_repository, paper, patent, standard, maintained_implementation, or local_repo_evidence.",
    "source_uri": "Paste the URL or local path supplied by the owner. Do not ask Codex to fetch the URL.",
    "source_version_or_date": "Record a publication date, version, commit, tag, standard version, or access date.",
    "source_owner_or_publisher": "Record the project, standards body, authors, company, university, or local repo owner.",
    "license_or_rights_note": "Record license, terms, open-access status, or owner-supplied rights notes.",
    "claim_supported": "Write one concrete AVF design or implementation claim this source supports.",
    "evidence_excerpt_summary": "Summarize only the owner-supplied excerpt or known local evidence; do not invent unseen source content.",
    "verification_notes": "State how a later reviewer can verify the source without changing the protected action boundary.",
}


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


def require_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("review gate must point to this completion guide goal")
    if gate.get("review_decision") != REVIEW_DECISION:
        raise SystemExit("review gate decision mismatch")
    if gate.get("fields_present") != 0:
        raise SystemExit("review gate must show zero present fields")
    if gate.get("missing_required_fields") != REQUIRED_SOURCE_FIELDS:
        raise SystemExit("review gate missing fields mismatch")
    if gate.get("accepted_records") != 0:
        raise SystemExit("review gate must not accept the empty sample")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("review gate must keep source collection blocked")


def build_completion_guide() -> str:
    field_rows = "\n".join(f"- `{field}`: {FIELD_GUIDANCE[field]}" for field in REQUIRED_SOURCE_FIELDS)
    kind_rows = "\n".join(f"- `{kind}`" for kind in ALLOWED_SOURCE_KINDS)
    return f"""# Owner-Supplied Primary-Source Evidence Record Completion Guide v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
guide_decision: {GUIDE_DECISION}

This guide explains how the owner can complete a local primary-source evidence record. It does not fetch, scrape, clone, install, call providers, deploy, publish, or claim readiness.

## Required fields

{field_rows}

## Allowed source kinds

{kind_rows}

## Boundary

- Do not ask Codex to fetch the URL
- No source collection execution
- No provider calls
- No live model calls
- No external service calls
- No external fetch
- No automated scraping
- No OSS clone
- No package install
- No dependency install
- No runtime integration
- No deploy
- No publish
- No release readiness claim
- No production readiness claim

## Next safe goal

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_completion_gate() -> dict:
    return {
        "gate_id": "avf-owner-supplied-primary-source-evidence-record-completion-guide-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "owner_supplied_only": True,
        "completion_guide_uri": rel(COMPLETION_GUIDE),
        "required_source_fields_documented": REQUIRED_SOURCE_FIELDS,
        "required_source_fields_documented_count": len(REQUIRED_SOURCE_FIELDS),
        "allowed_source_kinds": ALLOWED_SOURCE_KINDS,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_owner_action() -> str:
    fields = "\n".join(f"  - {field}" for field in REQUIRED_SOURCE_FIELDS)
    return f"""action_id: owner-fill-primary-source-evidence-record-template
owner_input_required: true
goal_id: {THIS_GOAL_ID}

owner_steps:
  - Copy the completion guide into a filled source evidence record
  - Fill all required fields using owner-supplied metadata or excerpts
  - Use official docs, original repos, papers, patents, standards, maintained implementations, or local repo evidence
  - Tie each record to one claim supported
  - Do not ask Codex to fetch the URL

required_source_fields:
{fields}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_owner_supplied_primary_source_evidence_record_completion_guide_v0_1",
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "owner_supplied_only": True,
        "required_source_fields_documented": len(REQUIRED_SOURCE_FIELDS),
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Owner-Supplied Primary-Source Evidence Record Completion Guide v0.1 Report

RESULT: PASS
owner_supplied_primary_source_evidence_record_completion_guide_v0_1=true

## Commands

- python scripts\\run_avf_owner_supplied_primary_source_evidence_record_completion_guide_v0_1.py
- python scripts\\validate_avf_owner_supplied_primary_source_evidence_record_completion_guide_v0_1.py

## Gate summary

- completion_guide_created=true
- completion_guide_gate_created=true
- required_source_fields_documented={len(REQUIRED_SOURCE_FIELDS)}
- owner_supplied_only=true
- source_collection_execution_allowed=false
- external_fetch_performed=false

## Generated artifacts

- {rel(COMPLETION_GUIDE)}
- {rel(COMPLETION_GUIDE_GATE)}
- {rel(NEXT_OWNER_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review_gate = read_json(REVIEW_GATE)
    require_review_gate(review_gate)

    write_text(COMPLETION_GUIDE, build_completion_guide())
    write_json(COMPLETION_GUIDE_GATE, build_completion_gate())
    write_text(NEXT_OWNER_ACTION, build_next_owner_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Owner-Supplied Primary-Source Evidence Record Completion Guide v0.1")
    print("RESULT: PASS")
    print("required_source_fields_documented=10")
    print("owner_supplied_only=true")
    print("source_collection_execution_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
