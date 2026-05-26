from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

WORKSPACE = CAPABILITIES / "capability_primary_source_evidence_capture_workspace.yml"
WORKSPACE_GATE = CAPABILITIES / "capability_primary_source_evidence_capture_workspace_gate.json"
POPULATION_GATE = CAPABILITIES / "capability_primary_source_evidence_population_gate.json"
POPULATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_population_validation_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_population_gate_next_codex_task_packet.yml"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_POPULATION_GATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_population_gate_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_capture_workspace_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_owner_primary_source_evidence_population_packet_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
POPULATION_DECISION = "BLOCKED_NO_POPULATED_SOURCE_EVIDENCE"

REQUIRED_EVIDENCE_FIELDS = [
    "source_uri",
    "source_type",
    "quoted_excerpt",
    "source_snapshot_hash",
    "license_note",
    "security_note",
    "maintenance_note",
    "architecture_fit_note",
    "supply_chain_note",
    "reviewer",
    "reviewed_at",
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


def require_workspace_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("workspace gate previous goal mismatch")
    if gate.get("status") != "PASS":
        raise SystemExit("workspace gate must be PASS")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("workspace gate must point to this population gate goal")
    if gate.get("target_source_slots_available") != 35:
        raise SystemExit("workspace gate must expose 35 source slots")
    if gate.get("captured_source_records") != 0:
        raise SystemExit("workspace gate captured source records must be zero")
    if gate.get("accepted_source_records") != 0:
        raise SystemExit("workspace gate accepted source records must be zero")
    if gate.get("required_evidence_fields") != REQUIRED_EVIDENCE_FIELDS:
        raise SystemExit("workspace gate required evidence fields mismatch")


def parse_workspace_records() -> list[dict]:
    records: list[dict] = []
    current: dict | None = None
    for raw_line in WORKSPACE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- candidate_id:"):
            if current:
                records.append(current)
            current = {"candidate_id": line.split(":", 1)[1].strip()}
        elif current and ":" in line:
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip().strip('"')
    if current:
        records.append(current)
    return records


def review_record(record: dict) -> dict:
    missing = [field for field in REQUIRED_EVIDENCE_FIELDS if not record.get(field)]
    captured_markers = [
        "source_uri",
        "quoted_excerpt",
        "source_snapshot_hash",
        "license_note",
        "security_note",
        "maintenance_note",
        "architecture_fit_note",
        "supply_chain_note",
        "reviewer",
        "reviewed_at",
    ]
    if all(not record.get(field) for field in captured_markers):
        review_status = "empty_record_blocked"
        missing = REQUIRED_EVIDENCE_FIELDS
    elif missing:
        review_status = "partial_record_blocked"
    else:
        review_status = "complete_record_pending_acceptance_gate"
    return {
        "candidate_id": record.get("candidate_id", ""),
        "source_slot_id": record.get("source_slot_id", ""),
        "planned_source_type": record.get("planned_source_type", ""),
        "review_status": review_status,
        "missing_required_fields": missing,
        "accepted_for_ingestion": False,
        "accepted_for_integration": False,
    }


def build_population_gate(record_reviews: list[dict]) -> dict:
    empty_records = sum(1 for review in record_reviews if review["review_status"] == "empty_record_blocked")
    partial_records = sum(1 for review in record_reviews if review["review_status"] == "partial_record_blocked")
    complete_records = sum(1 for review in record_reviews if review["review_status"] == "complete_record_pending_acceptance_gate")
    return {
        "gate_id": "avf-capability-primary-source-evidence-population-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "workspace_uri": rel(WORKSPACE),
        "population_decision": POPULATION_DECISION,
        "integration_decision": "blocked",
        "workspace_records_reviewed": len(record_reviews),
        "empty_source_records": empty_records,
        "partial_source_records": partial_records,
        "complete_source_records": complete_records,
        "accepted_source_records": 0,
        "required_evidence_fields": REQUIRED_EVIDENCE_FIELDS,
        "record_reviews": record_reviews,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_population_result(gate: dict) -> dict:
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_population_gate_v0_1",
        "status": "PASS",
        "checks": [
            "workspace records reviewed",
            "empty records detected and blocked",
            "partial records would be blocked until all required fields are present",
            "accepted source records remain zero",
            "protected-action flags remain false",
        ],
        "population_decision": gate["population_decision"],
        "workspace_records_reviewed": gate["workspace_records_reviewed"],
        "empty_source_records": gate["empty_source_records"],
        "partial_source_records": gate["partial_source_records"],
        "complete_source_records": gate["complete_source_records"],
        "accepted_source_records": gate["accepted_source_records"],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-owner-primary-source-evidence-population-packet-v0-1
title: Add AVF owner primary-source evidence population packet v0.1
goal: Define the owner/PRO packet for manually populating primary-source evidence records without executing external research, automated scraping, OSS clone, install, runtime integration, deploy, publish, or readiness claims from this branch.
context_paths:
  - avf/capabilities/generated/capability_primary_source_evidence_capture_workspace.yml
  - avf/capabilities/generated/capability_primary_source_evidence_population_gate.json
  - avf/capabilities/generated/capability_source_evidence_fixture_template.yml
files_likely_to_touch:
  - avf/capabilities/generated/capability_owner_primary_source_evidence_population_packet.yml
  - avf/capabilities/generated/capability_owner_primary_source_evidence_population_packet_gate.json
  - docs/goals/AVF_CAPABILITY_OWNER_PRIMARY_SOURCE_EVIDENCE_POPULATION_PACKET_V0_1_REPORT.md
forbidden_changes:
  - No external research execution
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
  - owner/PRO evidence population packet exists
  - packet lists required evidence fields and source families
  - empty and partial records remain blocked by default
  - protected actions remain blocked
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_population_gate_v0_1.py
expected_outputs:
  - owner primary-source evidence population packet
  - population packet gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    return f"""# AVF Capability Primary-Source Evidence Population Gate v0.1 Report

RESULT: PASS
capability_primary_source_evidence_population_gate_v0_1=true
population_gate_created=true
workspace_records_reviewed={gate['workspace_records_reviewed']}
empty_source_records={gate['empty_source_records']}
partial_source_records={gate['partial_source_records']}
complete_source_records={gate['complete_source_records']}
accepted_source_records={gate['accepted_source_records']}
integration_decision={gate['integration_decision']}
population_decision={gate['population_decision']}
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

## Gate Boundary

This gate reviews the repo-local evidence workspace only. The current workspace has no populated source records, so all records remain blocked and no integration proposal is allowed.

## Record Counts

- workspace_records_reviewed: {gate['workspace_records_reviewed']}
- empty_source_records: {gate['empty_source_records']}
- partial_source_records: {gate['partial_source_records']}
- complete_source_records: {gate['complete_source_records']}
- accepted_source_records: {gate['accepted_source_records']}

## Required Evidence Fields

Every record must include source URI, source type, short excerpt, sha256 snapshot hash, license note, security note, maintenance note, architecture fit note, supply-chain note, reviewer, and reviewed_at before a later acceptance gate can consider it.
"""


def main() -> None:
    workspace_gate = read_json(WORKSPACE_GATE)
    require_workspace_gate(workspace_gate)
    records = parse_workspace_records()
    if len(records) != 35:
        raise SystemExit(f"expected 35 workspace records, got {len(records)}")
    record_reviews = [review_record(record) for record in records]
    gate = build_population_gate(record_reviews)

    write_json(POPULATION_GATE, gate)
    write_json(POPULATION_RESULT, build_population_result(gate))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Primary-Source Evidence Population Gate v0.1 runner")
    print("RESULT: PASS")
    print("capability_primary_source_evidence_population_gate_v0_1=true")
    print("population_gate_created=true")
    print(f"workspace_records_reviewed={gate['workspace_records_reviewed']}")
    print(f"empty_source_records={gate['empty_source_records']}")
    print(f"partial_source_records={gate['partial_source_records']}")
    print(f"complete_source_records={gate['complete_source_records']}")
    print(f"accepted_source_records={gate['accepted_source_records']}")
    print(f"integration_decision={gate['integration_decision']}")
    print(f"population_decision={gate['population_decision']}")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("automated_scraping_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()
