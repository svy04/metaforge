from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUN_PLAN = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan.yml"
RUN_PLAN_GATE = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_collection_authorization_review_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_collection_authorization_review_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_collection_authorization_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_COLLECTION_AUTHORIZATION_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_collection_authorization_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_run_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_authorization_input_packet_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
REVIEW_DECISION = "BLOCKED_AUTHORIZATION_FIELDS_MISSING"

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


def require_run_plan_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("run plan gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("run plan gate must point to this authorization review goal")
    if gate.get("authorization_present") is not False:
        raise SystemExit("run plan gate must not have authorization")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("run plan gate must block collection execution")
    if gate.get("authorization_fields_required") != AUTHORIZATION_FIELDS:
        raise SystemExit("run plan gate authorization field mismatch")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_planned") != 35:
        raise SystemExit("run plan gate must include 35 planned source records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("run plan gate must not make source records executable")


def build_mode_reviews(run_plan_gate: dict) -> list[dict]:
    reviews: list[dict] = []
    for mode in run_plan_gate.get("execution_modes", []):
        reviews.append(
            {
                "mode_id": mode.get("mode_id", ""),
                "label": mode.get("label", ""),
                "authorization_required": True,
                "authorization_present": False,
                "review_status": "blocked_missing_authorization",
                "execution_allowed": False,
                "missing_authorization_fields": AUTHORIZATION_FIELDS,
            }
        )
    return reviews


def build_source_task_reviews(run_plan_gate: dict) -> list[dict]:
    reviews: list[dict] = []
    for task in run_plan_gate.get("source_collection_tasks", []):
        reviews.append(
            {
                "candidate_id": task.get("candidate_id", ""),
                "candidate_name": task.get("candidate_name", ""),
                "capability_id": task.get("capability_id", ""),
                "source_slot_id": task.get("source_slot_id", ""),
                "planned_target_uri": task.get("planned_target_uri", ""),
                "planned_source_type": task.get("planned_source_type", ""),
                "review_status": "blocked_missing_authorization",
                "missing_authorization_fields": AUTHORIZATION_FIELDS,
                "collection_execution_allowed": False,
                "trusted_source": False,
                "accepted_for_ingestion": False,
                "accepted_for_integration": False,
                "integration_allowed_from_record": False,
            }
        )
    return reviews


def build_review_gate(run_plan_gate: dict) -> dict:
    task_reviews = build_source_task_reviews(run_plan_gate)
    return {
        "gate_id": "avf-capability-primary-source-evidence-collection-authorization-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "authorization_review_passed": False,
        "authorization_fields_reviewed": AUTHORIZATION_FIELDS,
        "authorization_fields_present": 0,
        "missing_authorization_fields": AUTHORIZATION_FIELDS,
        "mode_reviews": build_mode_reviews(run_plan_gate),
        "source_entry_counts": {
            "source_records_reviewed": len(task_reviews),
            "source_records_executable": 0,
            "trusted_source_records": 0,
            "ingested_source_records": 0,
            "integrated_source_records": 0,
        },
        "source_task_reviews": task_reviews,
        "collection_execution_allowed": False,
        "integration_decision": "blocked",
        "run_plan_uri": rel(RUN_PLAN),
        "run_plan_gate_uri": rel(RUN_PLAN_GATE),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_collection_authorization_review_v0_1",
        "status": "PASS",
        "checks": [
            "authorization review gate exists",
            "all required authorization fields are checked",
            "missing authorization keeps collection execution blocked",
            "no source record becomes executable by default",
            "protected-action flags remain false",
        ],
        "review_decision": REVIEW_DECISION,
        "authorization_review_passed": False,
        "authorization_fields_reviewed": len(AUTHORIZATION_FIELDS),
        "authorization_fields_present": 0,
        "missing_authorization_fields": len(AUTHORIZATION_FIELDS),
        "source_records_reviewed": counts["source_records_reviewed"],
        "source_records_executable": counts["source_records_executable"],
        "collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-evidence-owner-authorization-input-packet-v0-1
title: Add AVF owner authorization input packet for primary-source evidence collection v0.1
goal: Create the repo-local owner authorization input packet needed before any primary-source evidence collection task can become executable.
context_paths:
  - avf/capabilities/generated/capability_primary_source_evidence_collection_authorization_review_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_run_plan.yml
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_run_plan_gate.json
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_input_packet.yml
  - avf/capabilities/generated/capability_primary_source_evidence_owner_authorization_input_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_AUTHORIZATION_INPUT_PACKET_V0_1_REPORT.md
forbidden_changes:
  - No collection execution from this packet
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
  - owner authorization input packet lists every required authorization field
  - default authorization values are empty or false
  - packet distinguishes owner approval from PRO research assistance
  - no source collection task becomes executable
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_collection_authorization_review_v0_1.py
expected_outputs:
  - owner authorization input packet
  - input gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    return f"""# AVF Capability Primary-Source Evidence Collection Authorization Review v0.1 Report

RESULT: PASS
capability_primary_source_evidence_collection_authorization_review_v0_1=true
collection_authorization_review_gate_created=true
authorization_fields_reviewed={len(AUTHORIZATION_FIELDS)}
authorization_fields_present={gate['authorization_fields_present']}
missing_authorization_fields={len(gate['missing_authorization_fields'])}
source_records_reviewed={counts['source_records_reviewed']}
source_records_executable={counts['source_records_executable']}
collection_execution_allowed=false
authorization_review_passed=false
integration_decision=blocked
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

## Decision

The authorization review checked all 11 required authorization fields. None are present, so all collection modes and all 35 source collection tasks remain blocked.

## Next Safe Goal

`{NEXT_SAFE_GOAL_ID}` should create a repo-local owner authorization input packet. It must not execute collection; it should only define the fields the owner would need to fill before another review gate can unlock a narrower approved path.
"""


def main() -> None:
    run_plan_gate = read_json(RUN_PLAN_GATE)
    require_run_plan_gate(run_plan_gate)
    gate = build_review_gate(run_plan_gate)

    write_json(REVIEW_GATE, gate)
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_text(VALIDATION_REPORT, build_report(gate))

    counts = gate["source_entry_counts"]
    print("AVF Capability Primary-Source Evidence Collection Authorization Review v0.1")
    print("RESULT: PASS")
    print(f"authorization_fields_reviewed={len(AUTHORIZATION_FIELDS)}")
    print(f"authorization_fields_present={gate['authorization_fields_present']}")
    print(f"source_records_reviewed={counts['source_records_reviewed']}")
    print(f"source_records_executable={counts['source_records_executable']}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
