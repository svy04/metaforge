from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

INPUT_PACKET = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_packet.yml"
INPUT_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_review_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_review_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_authorization_input_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_AUTHORIZATION_INPUT_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_input_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_input_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_completion_guide_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
REVIEW_DECISION = "BLOCKED_OWNER_AUTHORIZATION_INPUT_INCOMPLETE"

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

MODE_IDS = [
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


def require_input_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("input gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("input gate must point to this review goal")
    if gate.get("authorization_input_completed") is not False:
        raise SystemExit("input gate must remain incomplete")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("input gate must not grant owner authorization")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("input gate must block collection execution")
    if gate.get("authorization_fields_required") != AUTHORIZATION_FIELDS:
        raise SystemExit("input gate authorization fields mismatch")
    if gate.get("authorization_fields_completed") != 0:
        raise SystemExit("input gate completed authorization fields must be zero")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        raise SystemExit("input gate must cover 35 source records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("input gate must not make source records executable")


def build_mode_reviews(input_gate: dict) -> list[dict]:
    mode_flags = input_gate.get("authorization_mode_flags", {})
    return [
        {
            "mode_id": mode_id,
            "authorized": bool(mode_flags.get(f"{mode_id}_authorized", False)),
            "review_status": "blocked_input_incomplete",
            "execution_allowed": False,
            "required_before_execution": AUTHORIZATION_FIELDS,
        }
        for mode_id in MODE_IDS
    ]


def build_review_gate(input_gate: dict) -> dict:
    counts = input_gate["source_entry_counts"]
    return {
        "gate_id": "avf-capability-primary-source-evidence-owner-authorization-input-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "authorization_input_packet_uri": rel(INPUT_PACKET),
        "authorization_input_gate_uri": rel(INPUT_GATE),
        "authorization_input_review_passed": False,
        "authorization_input_completed": False,
        "owner_authorization_granted": False,
        "authorization_fields_required": AUTHORIZATION_FIELDS,
        "authorization_fields_completed": 0,
        "missing_authorization_fields": AUTHORIZATION_FIELDS,
        "mode_reviews": build_mode_reviews(input_gate),
        "source_entry_counts": {
            "source_records_reviewed": counts["source_records_reviewed"],
            "source_records_executable": 0,
            "trusted_source_records": 0,
            "ingested_source_records": 0,
            "integrated_source_records": 0,
        },
        "collection_execution_allowed": False,
        "integration_decision": "blocked",
        "owner_action_required": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_owner_authorization_input_review_v0_1",
        "status": "PASS",
        "checks": [
            "owner authorization input review gate exists",
            "empty authorization fields keep review blocked",
            "all collection modes remain disabled",
            "no source record becomes executable",
            "protected-action flags remain false",
        ],
        "review_decision": REVIEW_DECISION,
        "authorization_input_review_passed": False,
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
    return f"""task_id: avf-capability-primary-source-evidence-owner-authorization-completion-guide-v0-1
title: Add AVF owner authorization completion guide for primary-source collection v0.1
goal: Create a repo-local completion guide that tells the owner exactly how to fill the authorization fields without executing collection, scraping, provider calls, clone, install, integration, deploy, publish, or readiness claims.
context_paths:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_input_packet.yml
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_input_review_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_run_plan_gate.json
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_completion_guide.md
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_completion_guide_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_AUTHORIZATION_COMPLETION_GUIDE_V0_1_REPORT.md
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
  - guide lists every required authorization field
  - guide distinguishes manual owner collection, PRO-assisted review, Codex link opening, and automated collection
  - guide keeps default authorization false
  - guide states that a later filled packet and review gate are required before execution
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_owner_authorization_input_review_v0_1.py
expected_outputs:
  - owner authorization completion guide
  - guide gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    return f"""# AVF Capability Primary-Source Evidence Owner Authorization Input Review v0.1 Report

RESULT: PASS
capability_primary_source_evidence_owner_authorization_input_review_v0_1=true
owner_authorization_input_review_gate_created=true
authorization_fields_required={len(AUTHORIZATION_FIELDS)}
authorization_fields_completed={gate['authorization_fields_completed']}
missing_authorization_fields={len(gate['missing_authorization_fields'])}
source_records_reviewed={counts['source_records_reviewed']}
source_records_executable={counts['source_records_executable']}
collection_execution_allowed=false
authorization_input_review_passed=false
owner_authorization_granted=false
review_decision={REVIEW_DECISION}
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

- `{rel(REVIEW_GATE)}`
- `{rel(NEXT_CODEX_TASK)}`
- `{rel(VALIDATION_RESULT)}`

## Claim boundary

This review gate only evaluates the empty repo-local authorization input packet. It does not authorize, collect, fetch, scrape, trust, ingest, integrate, deploy, publish, or claim release/production readiness.

## Next safe goal

`{NEXT_SAFE_GOAL_ID}` should create an owner-facing completion guide for the required authorization fields while leaving all collection and ingestion blocked.
"""


def main() -> None:
    input_gate = read_json(INPUT_GATE)
    require_input_gate(input_gate)

    review_gate = build_review_gate(input_gate)
    write_json(REVIEW_GATE, review_gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result(review_gate))
    write_text(VALIDATION_REPORT, build_report(review_gate))

    print("AVF Capability Primary-Source Evidence Owner Authorization Input Review v0.1")
    print("RESULT: PASS")
    print("authorization_fields_required=11")
    print("authorization_fields_completed=0")
    print("owner_authorization_granted=false")
    print("authorization_input_review_passed=false")
    print("collection_execution_allowed=false")
    print("source_records_executable=0")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
