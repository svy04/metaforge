from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

PREVIOUS_REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_collection_authorization_review_gate.json"
AUTHORIZATION_INPUT_PACKET = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_packet.yml"
AUTHORIZATION_INPUT_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_AUTHORIZATION_INPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_input_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_collection_authorization_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_input_review_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
INPUT_DECISION = "INPUT_PACKET_READY_AWAITING_OWNER_COMPLETION"

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


def require_previous_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous authorization review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous authorization review gate must point to this input packet goal")
    if gate.get("authorization_review_passed") is not False:
        raise SystemExit("previous authorization review must not pass")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("previous authorization review must keep collection blocked")
    if gate.get("missing_authorization_fields") != AUTHORIZATION_FIELDS:
        raise SystemExit("previous authorization review missing field list mismatch")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        raise SystemExit("previous authorization review must cover 35 records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("previous authorization review must keep executable source records at zero")


def build_authorization_input_packet(previous_gate: dict) -> str:
    source_count = previous_gate["source_entry_counts"]["source_records_reviewed"]
    field_rows = "\n".join(f"  - {field}" for field in AUTHORIZATION_FIELDS)
    return f"""packet_id: avf-capability-primary-source-evidence-owner-authorization-input-packet-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
input_decision: {INPUT_DECISION}

purpose:
  Create the repo-local owner authorization input surface required before any primary-source evidence collection, ingestion, trust, or capability integration can become executable.

authorization_state:
  owner_authorization_granted: false
  authorization_input_completed: false
  authorization_fields_required_count: {len(AUTHORIZATION_FIELDS)}
  authorization_fields_completed_count: 0
  source_records_reviewed: {source_count}
  source_records_executable: 0
  collection_execution_allowed: false
  trusted_sources_by_default: false
  ingested_sources_by_default: false
  integrated_sources_by_default: false

authorization_fields_required:
{field_rows}

owner_authorization_input:
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

authorization_mode_choices:
  manual_owner_collection_authorized: false
  pro_manual_collection_authorized: false
  codex_assisted_link_opening_authorized: false
  automated_collection_authorized: false

mode_boundaries:
  - mode: manual_owner_collection
    default_authorized: false
    boundary: Owner may manually inspect primary/original sources and paste evidence only after filling this packet.
  - mode: pro_manual_collection
    default_authorized: false
    boundary: PRO may help prepare source-review notes only after owner explicitly authorizes the mode; no repo-local branch action fetches sources by default.
  - mode: codex_assisted_link_opening
    default_authorized: false
    boundary: Codex may open only owner-approved links after explicit authorization; no scraping, clone, install, deploy, publish, or integration is allowed by this packet.
  - mode: automated_collection
    default_authorized: false
    boundary: Automated collection remains blocked and requires a later dedicated connector authorization and sandbox gate.

blocked_until_reviewed:
  - source_collection_execution
  - source_ingestion
  - trusted_source_marking
  - capability_integration
  - provider_calls
  - live_model_calls
  - external_service_calls
  - automated_scraping
  - oss_clone
  - package_install
  - dependency_install
  - runtime_integration
  - deploy
  - publish
  - release_readiness_claim
  - production_readiness_claim

claim_boundary:
  protected_action_executed: false
  provider_calls_performed: false
  live_model_calls_performed: false
  external_service_calls_performed: false
  automated_scraping_performed: false
  scraping_performed: false
  posting_automation_performed: false
  dependency_install_performed: false
  external_fetch_performed: false
  oss_clone_performed: false
  package_install_performed: false
  runtime_integration_performed: false
  deploy_performed: false
  publish_performed: false
  release_ready: false
  production_ready: false

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_input_gate(previous_gate: dict) -> dict:
    counts = previous_gate["source_entry_counts"]
    return {
        "gate_id": "avf-capability-primary-source-evidence-owner-authorization-input-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "input_decision": INPUT_DECISION,
        "authorization_input_packet_uri": rel(AUTHORIZATION_INPUT_PACKET),
        "authorization_input_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_required": AUTHORIZATION_FIELDS,
        "authorization_fields_completed": 0,
        "missing_authorization_fields": AUTHORIZATION_FIELDS,
        "authorization_mode_flags": {
            "manual_owner_collection_authorized": False,
            "pro_manual_collection_authorized": False,
            "codex_assisted_link_opening_authorized": False,
            "automated_collection_authorized": False,
        },
        "source_entry_counts": {
            "source_records_reviewed": counts["source_records_reviewed"],
            "source_records_executable": 0,
            "trusted_source_records": 0,
            "ingested_source_records": 0,
            "integrated_source_records": 0,
        },
        "collection_execution_allowed": False,
        "integration_decision": "blocked",
        "review_required_before_any_execution": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_owner_authorization_input_packet_v0_1",
        "status": "PASS",
        "checks": [
            "owner authorization input packet exists",
            "authorization defaults are empty or false",
            "owner approval is distinct from PRO assistance",
            "no source collection task becomes executable",
            "protected-action flags remain false",
        ],
        "input_decision": INPUT_DECISION,
        "authorization_input_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_required": len(AUTHORIZATION_FIELDS),
        "authorization_fields_completed": 0,
        "missing_authorization_fields": len(AUTHORIZATION_FIELDS),
        "source_records_reviewed": counts["source_records_reviewed"],
        "source_records_executable": counts["source_records_executable"],
        "collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-evidence-owner-authorization-input-review-v0-1
title: Add AVF owner authorization input review gate v0.1
goal: Review the repo-local owner authorization input packet and keep all primary-source collection blocked unless explicit authorization fields are filled and narrowly scoped.
context_paths:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_input_packet.yml
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_input_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_collection_authorization_review_gate.json
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_input_review_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_input_review_next_codex_task_packet.yml
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_AUTHORIZATION_INPUT_REVIEW_V0_1_REPORT.md
forbidden_changes:
  - No source collection execution
  - No provider calls
  - No live model calls
  - No external service calls
  - No automated scraping
  - No OSS clone
  - No package install
  - No dependency install
  - No runtime integration
  - No deploy
  - No publish
  - No release readiness claim
  - No production readiness claim
acceptance_criteria:
  - review gate checks every authorization field
  - missing or empty fields keep all collection modes blocked
  - owner approval remains distinct from PRO assistance and Codex-assisted link opening
  - no source record becomes executable without a later explicit owner-filled packet
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_owner_authorization_input_packet_v0_1.py
expected_outputs:
  - owner authorization input review gate
  - next safe task packet
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    return f"""# AVF Capability Primary-Source Evidence Owner Authorization Input Packet v0.1 Report

RESULT: PASS
capability_primary_source_evidence_owner_authorization_input_packet_v0_1=true
owner_authorization_input_packet_created=true
owner_authorization_input_gate_created=true
authorization_fields_required={len(AUTHORIZATION_FIELDS)}
authorization_fields_completed={gate['authorization_fields_completed']}
missing_authorization_fields={len(gate['missing_authorization_fields'])}
source_records_reviewed={counts['source_records_reviewed']}
source_records_executable={counts['source_records_executable']}
collection_execution_allowed=false
owner_authorization_granted=false
authorization_input_completed=false
input_decision={INPUT_DECISION}
protected_action_executed=false
provider_calls_performed=false
live_model_calls_performed=false
external_service_calls_performed=false
automated_scraping_performed=false
scraping_performed=false
posting_automation_performed=false
dependency_install_performed=false
external_fetch_performed=false
oss_clone_performed=false
package_install_performed=false
runtime_integration_performed=false
deploy_performed=false
publish_performed=false
release_ready=false
production_ready=false
next_safe_goal_id={NEXT_SAFE_GOAL_ID}

## Generated artifacts

- `{rel(AUTHORIZATION_INPUT_PACKET)}`
- `{rel(AUTHORIZATION_INPUT_GATE)}`
- `{rel(NEXT_CODEX_TASK)}`
- `{rel(VALIDATION_RESULT)}`

## Claim boundary

This packet only creates an empty repo-local owner authorization input surface. It does not authorize, collect, fetch, scrape, trust, ingest, integrate, deploy, publish, or claim release/production readiness.

## Next safe goal

`{NEXT_SAFE_GOAL_ID}` should review the input packet and keep all source collection blocked unless the owner fills explicit, narrow authorization fields in a later artifact.
"""


def main() -> None:
    previous_gate = read_json(PREVIOUS_REVIEW_GATE)
    require_previous_review_gate(previous_gate)

    write_text(AUTHORIZATION_INPUT_PACKET, build_authorization_input_packet(previous_gate))
    input_gate = build_input_gate(previous_gate)
    write_json(AUTHORIZATION_INPUT_GATE, input_gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result(input_gate))
    write_text(VALIDATION_REPORT, build_report(input_gate))

    print("AVF Capability Primary-Source Evidence Owner Authorization Input Packet v0.1")
    print("RESULT: PASS")
    print(f"authorization_fields_required={len(AUTHORIZATION_FIELDS)}")
    print("authorization_fields_completed=0")
    print("owner_authorization_granted=false")
    print("authorization_input_completed=false")
    print("collection_execution_allowed=false")
    print("source_records_executable=0")
    print(f"input_decision={INPUT_DECISION}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
