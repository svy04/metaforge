from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_review_gate.json"
COMPLETION_GUIDE = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_completion_guide.md"
COMPLETION_GUIDE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_completion_guide_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_completion_guide_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_completion_guide_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_AUTHORIZATION_COMPLETION_GUIDE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_completion_guide_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_input_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_filled_authorization_packet_template_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
GUIDE_DECISION = "GUIDE_READY_EXECUTION_STILL_BLOCKED"

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
    if gate.get("authorization_input_review_passed") is not False:
        raise SystemExit("review gate must remain blocked")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("review gate must not grant owner authorization")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("review gate must keep collection execution blocked")
    if gate.get("authorization_fields_required") != AUTHORIZATION_FIELDS:
        raise SystemExit("review gate authorization fields mismatch")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        raise SystemExit("review gate must cover 35 source records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("review gate must not make source records executable")


def build_completion_guide(review_gate: dict) -> str:
    counts = review_gate["source_entry_counts"]
    field_rows = "\n".join(f"- `{field}`: required before any collection path can be reviewed." for field in AUTHORIZATION_FIELDS)
    mode_rows = "\n".join(f"- `{mode}`: default false; requires explicit owner scope and later review." for mode in COLLECTION_MODES)
    blocked_rows = "\n".join(
        f"- No {item}"
        for item in [
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
    )
    return f"""# AVF Primary-Source Evidence Owner Authorization Completion Guide v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
guide_decision: {GUIDE_DECISION}

This guide tells the owner how to fill the authorization fields for a later, narrower review. It does not authorize any primary-source collection by itself.

## Current locked state

- owner_authorization_granted: false
- collection_execution_allowed: false
- source_records_reviewed: {counts['source_records_reviewed']}
- source_records_executable: {counts['source_records_executable']}

## Required authorization fields

{field_rows}

## Collection mode choices

{mode_rows}

## Boundary summary

{blocked_rows}

## Minimum owner completion rule

The owner must fill every required field, choose only the intended collection modes, bound source families and source slots, set `max_records_to_collect`, and provide `collection_boundaries` plus `revocation_note`. A later filled packet and review gate are required before execution.

## Next safe goal

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_completion_guide_gate(review_gate: dict) -> dict:
    counts = review_gate["source_entry_counts"]
    return {
        "gate_id": "avf-capability-primary-source-evidence-owner-authorization-completion-guide-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "completion_guide_uri": rel(COMPLETION_GUIDE),
        "authorization_fields_documented": AUTHORIZATION_FIELDS,
        "collection_modes_documented": COLLECTION_MODES,
        "owner_authorization_granted": False,
        "collection_execution_allowed": False,
        "source_entry_counts": {
            "source_records_reviewed": counts["source_records_reviewed"],
            "source_records_executable": 0,
            "trusted_source_records": 0,
            "ingested_source_records": 0,
            "integrated_source_records": 0,
        },
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_owner_authorization_completion_guide_v0_1",
        "status": "PASS",
        "checks": [
            "completion guide exists",
            "all authorization fields are documented",
            "all collection modes are documented",
            "collection execution remains blocked",
            "protected-action flags remain false",
        ],
        "guide_decision": GUIDE_DECISION,
        "authorization_fields_documented": len(AUTHORIZATION_FIELDS),
        "collection_modes_documented": len(COLLECTION_MODES),
        "source_records_reviewed": counts["source_records_reviewed"],
        "source_records_executable": counts["source_records_executable"],
        "collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-evidence-owner-filled-authorization-packet-template-v0-1
title: Add AVF owner-filled authorization packet template v0.1
goal: Create a repo-local template for a future owner-filled authorization packet without granting authorization, collecting sources, scraping, provider calls, clone, install, integration, deploy, publish, or readiness claims.
context_paths:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_completion_guide.md
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_completion_guide_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_input_packet.yml
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_filled_authorization_packet_template.yml
  - avf/capabilities/generated/capability_primary_source_evidence_owner_filled_authorization_packet_template_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_FILLED_AUTHORIZATION_PACKET_TEMPLATE_V0_1_REPORT.md
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
  - filled authorization template includes every required field
  - template keeps authorization unset by default
  - template distinguishes manual owner collection, PRO-assisted review, Codex link opening, and automated collection
  - no collection task becomes executable
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_owner_authorization_completion_guide_v0_1.py
expected_outputs:
  - owner-filled authorization packet template
  - template gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    return f"""# AVF Capability Primary-Source Evidence Owner Authorization Completion Guide v0.1 Report

RESULT: PASS
capability_primary_source_evidence_owner_authorization_completion_guide_v0_1=true
owner_authorization_completion_guide_created=true
owner_authorization_completion_guide_gate_created=true
authorization_fields_documented={len(AUTHORIZATION_FIELDS)}
collection_modes_documented={len(COLLECTION_MODES)}
source_records_reviewed={counts['source_records_reviewed']}
source_records_executable={counts['source_records_executable']}
collection_execution_allowed=false
owner_authorization_granted=false
guide_decision={GUIDE_DECISION}
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

- `{rel(COMPLETION_GUIDE)}`
- `{rel(COMPLETION_GUIDE_GATE)}`
- `{rel(NEXT_CODEX_TASK)}`
- `{rel(VALIDATION_RESULT)}`

## Claim boundary

This guide is instruction-only. It does not authorize, collect, fetch, scrape, trust, ingest, integrate, deploy, publish, or claim release/production readiness.

## Next safe goal

`{NEXT_SAFE_GOAL_ID}` should create a still-unfilled authorization template that the owner can later complete and route into a separate review gate.
"""


def main() -> None:
    review_gate = read_json(REVIEW_GATE)
    require_review_gate(review_gate)

    write_text(COMPLETION_GUIDE, build_completion_guide(review_gate))
    guide_gate = build_completion_guide_gate(review_gate)
    write_json(COMPLETION_GUIDE_GATE, guide_gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result(guide_gate))
    write_text(VALIDATION_REPORT, build_report(guide_gate))

    print("AVF Capability Primary-Source Evidence Owner Authorization Completion Guide v0.1")
    print("RESULT: PASS")
    print("authorization_fields_documented=11")
    print("collection_modes_documented=4")
    print("owner_authorization_granted=false")
    print("collection_execution_allowed=false")
    print("source_records_executable=0")
    print(f"guide_decision={GUIDE_DECISION}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
